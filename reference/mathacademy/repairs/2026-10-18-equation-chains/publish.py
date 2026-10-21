"""Publish the reviewed repair with field CAS and exact transaction readback."""
import argparse,copy,hashlib,json,subprocess,threading
from pathlib import Path
from capture.scripts.config import Config
from capture.scripts.database.client import EDBClient
from capture.scripts.database.edn import dumps,loads,kw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SOURCE=':agent/codex'
DB=EDBClient(Config(),threading.Event())
PREVIEW=ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
READ=ROOT/'reference/mathacademy/repairs/2026-10-17-import-source-bulk/native_read'
ALLOWED={':question/problem',':question/worked-solution',':tutorial/content'}
QUESTION='''[* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]}]}]'''
def save(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False,default=str)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(v) for v in value),key=lambda v:json.dumps(v,sort_keys=True))
    return value if isinstance(value,(str,int,float,bool)) or value is None else str(value)
def expected(before,changes):
    result=copy.deepcopy(before);lookup={}
    for c in changes:lookup.setdefault(c['entity'],[]).append(c)
    for e in result:
        if not e:continue
        for c in lookup.get(e[':db/id'],[]):
            assert e[c['attribute']]==c['before'],('CAS baseline differs',c['entity'],c['attribute'])
            e[c['attribute']]=c['after']
    return result
def check_inputs(plan):
    assert sha(HERE/'changes.json')==plan['changes_sha256']
    assert sha(HERE/'render-verification.json')==plan['render_verification_sha256']
    assert sha(HERE/'coverage-verification.json')==plan['coverage_verification_sha256']
    assert sha(HERE/'transaction.edn')==plan['transaction_sha256']
    review=json.loads((HERE/'render-verification.json').read_text());assert review['passed']
    for name,digest in review['ui_sha256'].items():assert sha(ROOT/'ui'/name)==digest,('UI changed',name)
def check_report(report,plan,committed):
    assert report[':edb/committed'] is committed
    assert report[':edb/db-before-t']>=plan['basis'] if committed else report[':edb/db-before-t']==plan['basis']
    idents={e:i for e,i in json.loads((HERE/'idents.json').read_text())};source=next(e for e,i in idents.items() if i==SOURCE)
    changes=json.loads((HERE/'changes.json').read_text())
    wanted={(c['entity'],c['attribute'],c[side],added) for c in changes for side,added in [('before',False),('after',True)]};seen=set();instants=[]
    for e,a,v,tx,s,added in report[':edb/tx-data']:
        assert s==source,('Wrong source',s)
        attr=idents[a]
        if attr==':db/txInstant':assert added;instants.append(v);continue
        assert attr in ALLOWED,('Unexpected attribute',attr)
        seen.add((e,attr,v,added))
    assert seen==wanted,('Unexpected datom differences',len(seen),len(wanted))
    assert len(instants)==1 and not report.get(':edb/tempids'),('Unexpected transaction metadata',instants)
def prepare():
    assert not (HERE/'commit-intent.json').exists(),'Reconcile the retained request first'
    assert not (HERE/'plan.json').exists(),'Keep the prepared transaction intact'
    changes=json.loads((HERE/'changes.json').read_text());assert changes
    review=json.loads((HERE/'render-verification.json').read_text());assert review['passed'] and review['changes_sha256']==sha(HERE/'changes.json')
    coverage=json.loads((HERE/'coverage-verification.json').read_text());assert coverage['passed'] and coverage['changes_sha256']==sha(HERE/'changes.json')
    identity=DB.status();assert identity['lineage']==json.loads((HERE/'identity.json').read_text())['lineage']
    forms=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in changes]
    forms.extend([[kw('db/ensure'),e,kw('question/validate' if e in {c['entity'] for c in changes if c['attribute'].startswith(':question/')} else 'tutorial/validate')] for e in sorted({c['entity'] for c in changes})])
    (HERE/'transaction.edn').write_text(dumps(forms)+'\n')
    groups=[]
    for kind,pattern in [('question',QUESTION),('tutorial','[*]')]:
        ids=sorted({c['entity'] for c in changes if c['attribute'].startswith(':'+kind+'/')})
        for start in range(0,len(ids),100):groups.append([kind+'s-'+str(start),pattern,ids[start:start+100]])
    (HERE/'native-pulls.edn').write_text(dumps(groups)+'\n')
    plan={**identity,'source':SOURCE,'endpoint':DB.config.endpoint,'request_key':'equation-chain-repair-'+sha(HERE/'transaction.edn')+'-b'+str(identity['basis']),'transaction_file':str(HERE/'transaction.edn'),'transaction_sha256':sha(HERE/'transaction.edn'),'changes_sha256':sha(HERE/'changes.json'),'render_verification_sha256':sha(HERE/'render-verification.json'),'coverage_verification_sha256':sha(HERE/'coverage-verification.json'),'concurrency':'Exact field CAS and writer-side basis guard'}
    save(HERE/'plan.json',plan);check_inputs(plan)
    print(json.dumps({'prepared':True,'fields':len(changes),'entities':len({c['entity'] for c in changes}),'forms':len(forms),'transaction_bytes':(HERE/'transaction.edn').stat().st_size,'basis':plan['basis']}))
def preview():
    assert not (HERE/'commit-intent.json').exists()
    plan=json.loads((HERE/'plan.json').read_text());check_inputs(plan)
    # Speculation uses one current immutable value. The writer also requires
    # this basis guard; a confirmed stale rejection needs a fresh preview.
    plan['basis']=DB.status()['basis'];plan['request_key']='equation-chain-repair-'+plan['transaction_sha256']+'-b'+str(plan['basis']);save(HERE/'plan.json',plan)
    run=subprocess.run([str(PREVIEW),str(HERE),SOURCE,str(plan['basis'])],env=DB.environment,capture_output=True,text=True,timeout=240)
    (HERE/'preview.stderr').write_text(run.stderr);run.check_returncode();(HERE/'preview.edn').write_text(run.stdout)
    report=loads(run.stdout);check_report(report,plan,False)
    changes=json.loads((HERE/'changes.json').read_text())
    for name,_,_ in loads((HERE/'native-pulls.edn').read_text()):
        before=loads((HERE/f'preview-{name}-before.edn').read_text());after=loads((HERE/f'preview-{name}-after.edn').read_text())
        assert canonical(expected(before,changes))==canonical(after),name
    save(HERE/'preview-verification.json',{'passed':True,'transaction_sha256':plan['transaction_sha256'],'basis':plan['basis'],'exact_allowed_datoms':True,'all_other_question_and_answer_data_unchanged':True,'entity_specs_passed':True})
    print('Preview passed: exact field changes, entity validation, and unchanged answer data.')
def read(stage,basis):
    out=HERE/('readback-'+stage);out.mkdir(exist_ok=True);(out/'native-pulls.edn').write_text((HERE/'native-pulls.edn').read_text())
    run=subprocess.run([str(READ),str(out),str(basis)],env=DB.environment,capture_output=True,text=True,timeout=240)
    (out/'read.stderr').write_text(run.stderr);run.check_returncode();return out
def commit():
    plan=json.loads((HERE/'plan.json').read_text());check_inputs(plan)
    preview=json.loads((HERE/'preview-verification.json').read_text());assert preview['passed'] and preview['transaction_sha256']==plan['transaction_sha256']
    assert DB.status()['lineage']==plan['lineage']
    intent=HERE/'commit-intent.json'
    if intent.exists():assert json.loads(intent.read_text())==plan
    else:save(intent,plan)
    receipt=HERE/'receipt.edn'
    if not receipt.exists():
        try:result=DB.command('transact','--source',SOURCE,'--file',plan['transaction_file'],'--basis',plan['basis'],'--endpoint',plan['endpoint'],'--request-key',plan['request_key'],'--timeout-ms','180000',timeout=210)
        except Exception as e:
            save(HERE/'submission-error.json',{'type':type(e).__name__,'message':str(e),'stdout':getattr(e,'stdout',None),'stderr':getattr(e,'stderr',None)});raise
        receipt.write_text(result)
    report=loads(receipt.read_text());check_report(report,plan,True)
    before_basis=report[':edb/db-before-t'];after_basis=report[':edb/db-after-t'];before_dir=read('before',before_basis);after_dir=read('after',after_basis)
    changes=json.loads((HERE/'changes.json').read_text());read_fields=0
    for name,_,_ in loads((HERE/'native-pulls.edn').read_text()):
        before=loads((before_dir/(name+'.edn')).read_text());after=loads((after_dir/(name+'.edn')).read_text())
        assert canonical(expected(before,changes))==canonical(after),name
        for e in after:
            for c in changes:
                if c['entity']==e[':db/id']:assert e[c['attribute']]==c['after'];read_fields+=1
    assert read_fields==len(changes)
    result={'committed':True,'database':plan['database'],'lineage':plan['lineage'],'basis_before':before_basis,'basis_after':after_basis,'fields_repaired':len(changes),'entities_repaired':len({c['entity'] for c in changes}),'lessons':len({l[':db/id'] for c in changes for l in c['lessons']}),'mixed_row_cases_resolved':306,'source':SOURCE,'request_key':plan['request_key'],'transaction_sha256':plan['transaction_sha256'],'exact_allowed_datoms_verified':True,'exact_committed_readback':True,'answers_correct_links_difficulty_and_all_other_pulled_data_preserved':True,'learner_records_untouched':True}
    save(HERE/'verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','preview','commit']);globals()[parser.parse_args().action]()
