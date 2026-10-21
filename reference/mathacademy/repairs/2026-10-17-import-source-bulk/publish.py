"""Guarded bulk content repair: exact CAS, native preview, retained request, readback."""
import argparse, copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
from snapshot import QUESTION, USES, READ, SOURCE, save
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps,loads,kw
DB=Publisher.from_environment(source=SOURCE).client
NATIVE=ROOT/'reference/edb-math/imports/authored-checkboxes/2026-10-16/lesson-17592186492056/native/preview'
ALLOWED={':question/problem',':question/worked-solution',':tutorial/content',':answer/value'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def check_reviewed_ui(validation):
    for name,expected_hash in validation['ui_sha256'].items():
        assert digest(ROOT/name)==expected_hash,('Reviewed UI changed',name)
def canonical(v):
    if isinstance(v,dict):return {str(k):canonical(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return sorted((canonical(x) for x in v),key=lambda x:json.dumps(x,sort_keys=True))
    return v if isinstance(v,(str,int,float,bool)) or v is None else str(v)
def read_native(out,basis):
    run=subprocess.run([str(READ),str(out),str(basis)],env=DB.environment,capture_output=True,text=True,timeout=240)
    (out/'native-read.stderr').write_text(run.stderr);run.check_returncode()
def expected(before,changes):
    result=copy.deepcopy(before);by_id={}
    for c in changes:by_id.setdefault(c['entity'],[]).append(c)
    def walk(v):
        if isinstance(v,list):
            for x in v:walk(x)
        elif isinstance(v,dict):
            for c in by_id.get(v.get(':db/id'),[]):
                if c['attribute'] in v:
                    assert v[c['attribute']]==c['before'];v[c['attribute']]=c['after']
            for x in v.values():walk(x)
    walk(result);return result
def report_check(report,plan,committed):
    assert report[':edb/committed'] is committed
    assert report[':edb/db-before-t']==plan['basis']
    attrs={e:str(a) for e,a,t in plan['schema']['attributes']}
    source=next(e for e,i in plan['schema']['idents'] if str(i)==SOURCE)
    expected_datoms={(c['entity'],c['attribute'],c[side],added) for c in plan['changes'] for side,added in [('before',False),('after',True)]}
    observed=set()
    for e,a,v,tx,s,added in report[':edb/tx-data']:
        assert s==source
        if attrs[a]==':db/txInstant':assert added;continue
        assert attrs[a] in ALLOWED
        observed.add((e,attrs[a],v,added))
    assert observed==expected_datoms,('Unexpected transaction datoms',len(observed),len(expected_datoms))
def prepare(out):
    assert not (out/'commit-intent.json').exists(),'Recover saved intent first'
    integrated=HERE/'integrated-changes.json';review=HERE/'review/verification.json'
    content=json.loads(integrated.read_text());validation=json.loads(review.read_text())
    assert validation['passed'] and validation['input_sha256']==digest(integrated),'Content review differs from publication input'
    check_reviewed_ui(validation)
    grading=json.loads((HERE/'grading/verification.json').read_text())
    assert grading['passed'] and grading['input_sha256']==digest(integrated),'Grading review differs from publication input'
    assert content['changes'],'No changes'
    snapshot=Path(content['snapshot']);identity=DB.status();assert identity['lineage']==content['identity']['lineage']
    groups=loads((snapshot/'native-pulls.edn').read_text())
    (out/'native-pulls.edn').write_text(dumps(groups)+'\n');read_native(out,identity['basis'])
    fresh={v[':db/id']:v for v in loads((out/'entities.edn').read_text()) if v}
    for c in content['changes']:assert fresh[c['entity']][c['attribute']]==c['before'],('Reviewed field changed',c['entity'],c['attribute'])
    specs={'attributes':('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[]),'idents':('[:find ?e ?ident :where [?e :db/ident ?ident]]',[])}
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures={n:pool.submit(DB.query,q,i,out/'schema',n,identity['basis']) for n,(q,i) in specs.items()};schema={n:f.result() for n,f in futures.items()}
    forms=[[kw('db/cas'),c['entity'],kw(c['attribute']),c['before'],c['after']] for c in content['changes']]
    (out/'transaction.edn').write_text(dumps(forms)+'\n');txsha=digest(out/'transaction.edn')
    concise_changes=[{k:c[k] for k in ('entity','attribute','before','after')} for c in content['changes']]
    plan={**identity,'source':SOURCE,'endpoint':DB.config.endpoint,'schema':schema,'changes':concise_changes,'content_sha256':digest(integrated),'validation_sha256':digest(review),'grading_sha256':digest(HERE/'grading/verification.json'),
        'transaction_file':str(out/'transaction.edn'),'sha256':txsha,'request_key':f'import-source-bulk-b{identity["basis"]}-{txsha}'}
    save(out/'plan.json',plan);print(json.dumps({'prepared':True,'basis':identity['basis'],'fields':len(forms),'transaction_bytes':(out/'transaction.edn').stat().st_size}))
def preview(out):
    plan=json.loads((out/'plan.json').read_text());assert digest(out/'transaction.edn')==plan['sha256']
    run=subprocess.run([str(NATIVE),str(out),SOURCE,str(plan['basis'])],env=DB.environment,capture_output=True,text=True,timeout=240)
    (out/'preview.stderr').write_text(run.stderr);run.check_returncode();(out/'preview.edn').write_text(run.stdout)
    report=loads(run.stdout);report_check(report,plan,False)
    for name,_,_ in loads((out/'native-pulls.edn').read_text()):
        before=loads((out/f'preview-{name}-before.edn').read_text());after=loads((out/f'preview-{name}-after.edn').read_text())
        assert canonical(expected(before,plan['changes']))==canonical(after),name
        assert canonical(before)==canonical(loads((out/f'{name}.edn').read_text())),('Prepared snapshot differs',name)
    save(out/'preview-verification.json',{'passed':True,'transaction_sha256':plan['sha256'],'exact_allowed_datoms':True,'all_other_pulled_values_unchanged':True})
    print('Native preview and exact change whitelist passed')
def commit(out):
    plan=json.loads((out/'plan.json').read_text());assert digest(out/'transaction.edn')==plan['sha256']
    checks=json.loads((out/'preview-verification.json').read_text());assert checks['passed'] and checks['transaction_sha256']==plan['sha256']
    assert digest(HERE/'integrated-changes.json')==plan['content_sha256'] and digest(HERE/'review/verification.json')==plan['validation_sha256']
    check_reviewed_ui(json.loads((HERE/'review/verification.json').read_text()))
    assert digest(HERE/'grading/verification.json')==plan['grading_sha256']
    assert DB.status()['lineage']==plan['lineage']
    intent=out/'commit-intent.json'
    if intent.exists():assert json.loads(intent.read_text())==plan
    else:save(intent,plan)
    receipt=out/'receipt.edn'
    if not receipt.exists():
        try:
            result=DB.command('transact','--source',SOURCE,'--file',plan['transaction_file'],'--basis',plan['basis'],'--endpoint',plan['endpoint'],
                '--request-key',plan['request_key'],'--timeout-ms','180000',timeout=210)
        except Exception as e:
            save(out/'submission-error.json',{'type':type(e).__name__,'message':str(e),'stdout':getattr(e,'stdout',None),'stderr':getattr(e,'stderr',None)})
            raise
        receipt.write_text(result)
    report=loads(receipt.read_text());report_check(report,plan,True);after_basis=report[':edb/db-after-t']
    for stage,basis in [('before',plan['basis']),('after',after_basis)]:
        target=out/f'readback-{stage}';target.mkdir(exist_ok=True);(target/'native-pulls.edn').write_text((out/'native-pulls.edn').read_text());read_native(target,basis)
        for name,_,_ in loads((out/'native-pulls.edn').read_text()):
            assert canonical(loads((target/f'{name}.edn').read_text()))==canonical(loads((out/f'preview-{name}-{stage}.edn').read_text())),(stage,name)
    result={'committed':True,'basis_before':plan['basis'],'basis_after':after_basis,'fields_repaired':len(plan['changes']),'entities_repaired':len({c['entity'] for c in plan['changes']}),
        'source':SOURCE,'request_key':plan['request_key'],'transaction_sha256':plan['sha256'],'exact_committed_and_historical_readback':True,
        'only_reviewed_content_attributes_changed':True,'answer_identities_correct_links_difficulty_and_learner_state_preserved':True}
    save(out/'verification.json',result);save(HERE/'verification.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['prepare','preview','commit']);p.add_argument('--attempt',required=True);a=p.parse_args()
    out=HERE/a.attempt;out.mkdir(exist_ok=True);globals()[a.action](out)
