"""Hard-only additive commit with application locking and exact-basis readback."""
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import threading
import uuid
from pathlib import Path
from types import SimpleNamespace

H=Path(__file__).resolve().parent;ROOT=H.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
from db_support import DB, KP, PATTERN, dumps, loads, kw
sys.path.insert(0,str(ROOT/'scripts'))
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
spec=importlib.util.spec_from_file_location('cotangent_validation',H/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051';LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE=':application/ca-engine';SCRIPT=str(H.with_suffix('.py').relative_to(ROOT))
LOCK=ROOT/'.local/learning/requests/math/api.lock'
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'40244c3974a8107ac3d36168e3e3c8bc2c442468b1da812315202b107c7b2682'
OUT=H/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
 [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
 [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status]
 (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
 [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]'''

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):
    if isinstance(x,dict):return {str(k):canonical(z) for k,z in x.items()}
    if isinstance(x,(list,tuple)):return sorted([canonical(z) for z in x],key=lambda z:json.dumps(z,sort_keys=True))
    return str(x) if isinstance(x,uuid.UUID) else x

def inventory(native,path):
    r=subprocess.run([str(native),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=database_environment('math'),capture_output=True,text=True,check=True,timeout=55)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
    save(path,x['data']);return x['data']

def read_kp(path,basis):
    return DB.query('[:find (pull ?k '+PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],path,'kp',basis)[0][0]

def fingerprint(q):
    p=q[':question/problem']
    if not re.search(r"\{f\}\^\{'\}\(\\frac\{\\pi \}\{6\}\)",p):return None
    m=re.search(r'f\(x\)=-([0-9]+)\\operatorname\{cot\}x',p)
    return g.mathematical_key(int(m[1])) if m else None

def normalized(q):
    out={k:str(q[k]) if k==':question/id' else q[k] for k in [':question/id',':question/problem',':question/worked-solution']}
    out[':question/difficulty']=str(q[':question/difficulty'][':db/ident']);out[':question/answer-fields']=[]
    for f in q[':question/answer-fields']:
        out[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])]})
    return out

def counts(kp,path,basis):
    shown={r[0] for r in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',basis,history=True)}
    reserved={r[0] for r in DB.query(RESERVED,[KP,LEARNER],path,'reserved',basis)}
    available=set();excluded=[]
    for q in kp[':knowledge-point/questions']:
        if str(q.get(':question/difficulty',{}).get(':db/ident',''))!=':question.difficulty/hard':continue
        if q[':db/id'] in shown|reserved:continue
        try:
            nq=normalized(q);n=int(re.search(r'f\(x\)=-([0-9]+)\\operatorname\{cot\}x',nq[':question/problem'])[1])
            r=g.generate('hard',0,n=n);r['question']=nq;v.check(r);available.add(fingerprint(q))
        except (KeyError,AssertionError,TypeError,ValueError) as e:
            excluded.append({'question':str(q[':question/id']),'reason':str(e) or type(e).__name__})
    out={'basis':basis,'distinct_available_hard':len(available),'shown_or_reserved':sorted(shown|reserved),'invalid_or_incomplete_hard':excluded}
    save(path/'available-counts.json',out);return out

def transaction(records,kp):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT,'Existing registered generator requires reconciliation'
    else:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(g.GENERATOR_ID),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def report_checks(report,path,source):
    attrs={eid:str(a) for eid,a in DB.attributes(path,report[':edb/db-before-t'])};new=set(report[':edb/tempids'].values())
    allowed={':answer/id',':answer/type',':answer/value',':answer-field/id',':answer-field/key',':answer-field/type',':answer-field/choices',':answer-field/correct',':question/id',':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':question-generator/id',':question-generator/script'}
    for e,a,value,t,s,added in report[':edb/tx-data']:
        assert added and s==source,'Unexpected retraction or attribution'
        name=attrs[a]
        if e==KP:assert name in {':knowledge-point/questions',':knowledge-point/question-generator'}
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected non-scoped datom'

def verify(report,path,intent):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    b=report[':edb/db-after-t'];report_checks(report,path/'receipt-check',intent['source_eid'])
    before=loads((path/'before.edn').read_text());after=read_kp(path/'readback',b)
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in after[':knowledge-point/questions']}
    assert all(canonical(q)==canonical(now[e]) for e,q in old.items())
    omit={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert canonical({k:z for k,z in before.items() if k not in omit})==canonical({k:z for k,z in after.items() if k not in omit})
    gen=after[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==g.GENERATOR_ID and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert canonical(normalized(q))==canonical(r['question']);assert fingerprint(q)==r['generation']['mathematical_key'];v.check(r)
    assert not transaction([],after),'Repeat preparation must produce no content changes'
    c=counts(after,path/'readback',b)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':b,'new_questions':len(records),
            'distinct_available_hard':c['distinct_available_hard'],'unchanged_source_questions':len(old),
            'canonical_example_unchanged':True,'learner_history_unchanged':True,'no_retractions':True,
            'only_requested_kp_additive_content':True,'source':SOURCE,'generator_registration_verified':True,
            'repeat_preparation_content_changes':0}
    save(path/'verification.json',result);return result

def finish(path,verified,inv):
    remaining=max(0,5-verified['distinct_available_hard'])
    result={'outcome':'finite-limit' if remaining else 'generated','knowledgePoint':KP,'difficulty':'hard',
            'generator_path':SCRIPT,'generator_id':g.GENERATOR_ID,'lineage':LINEAGE,
            'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],
            'supported_levels':['hard'],'available_after':{'hard':verified['distinct_available_hard']},
            'shortage_remaining':{'hard':remaining},'unsupported_levels_filled':False,
            'capability':json.loads((H/'capability.json').read_text()),'inventory_recheck_basis':inv['basis'],
            'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
            'evidence':[str(p.relative_to(ROOT)) for p in [H/'validation.json',H/'classification.md',H/'template-extraction.md',H/'capability.json',H/'historical-evidence.json',path/'preparation.json',path/'transaction.edn',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'verification.json',path/'inventory-after.json',path/'native-report.json']],
            'note':'Requested hard reserve verified. Numeric blank is an explicit source-anchored response adaptation. Easy/moderate implementations are deferred; remaining native shortages are explicit. All source questions and learner history preserved.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ['outcome','verified_commit_basis','new_questions','available_after','remaining_jobs']}),flush=True)

def main():
    val=json.loads((H/'validation.json').read_text());assert val['passed']
    assert all(sha(ROOT/p)==s for p,s in val['files'].items())
    native=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text());assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'));return
        inv=inventory(native,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b and LINEAGE in DB.command('status')
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True);kp=read_kp(path/'locked-source',b)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        captured=loads((H/'source.edn').read_text());current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(canonical(q)==canonical(current[q[':db/id']]) for q in captured[':knowledge-point/questions']),'Source evidence changed; reclassify'
        assert canonical(captured[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        reg=kp.get(':knowledge-point/question-generator')
        if reg:assert str(reg[':question-generator/id'])==g.GENERATOR_ID and reg[':question-generator/script']==SCRIPT
        orphan=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(g.GENERATOR_ID)],path,'generator-identity',b)
        assert not orphan or len(orphan)==1 and orphan[0][0][':question-generator/script']==SCRIPT
        c=counts(kp,path,b);job=next((j for j in inv['jobs'] if j['knowledgePoint']==KP and j['difficulty']=='hard'),{})
        needed=max(0,5-c['distinct_available_hard'],job.get('missing',0))
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];supplied=json.loads(JOB.with_suffix('.generated').read_text()) if JOB.with_suffix('.generated').exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        for r in instances:
            v.check(r)
            if len(records)<needed and r['generation']['mathematical_key'] not in used:
                records.append(r);used.add(r['generation']['mathematical_key'])
        # Execute the exact application protocol under its ordinary Python.
        p=subprocess.run([sys.executable,str(H.with_suffix('.py')),'--difficulty','hard','--count','24','--seed',str(int(JOB.name[:8],16)),'--format','json'],capture_output=True,text=True,check=True)
        for r in json.loads(p.stdout):
            v.check(r)
            if len(records)>=needed:break
            if r['generation']['mathematical_key'] not in used:
                records.append(r);used.add(r['generation']['mathematical_key'])
        for kind,ids in [('question',[uuid.UUID(r['question'][':question/id']) for r in records]),('answer-field',[uuid.UUID(f[':answer-field/id']) for r in records for f in r['question'][':question/answer-fields']]),('answer',[uuid.UUID(a[':answer/id']) for r in records for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']])]:
            assert len(ids)==len(set(ids))
            if ids:assert not DB.query('[:find ?e :in $ [?id ...] :where [?e :'+kind+'/id ?id]]',[ids],path,'identity-'+kind,b),'Existing identity requires reconciliation'
        save(path/'generated.json',records);save(path/'native-input.json',[v.engine_item(r['question'][':question/id'],r) for r in records])
        subprocess.run([str(H/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'source_evidence_unchanged':True,'available_before':c,'needed_hard':needed,'new_questions':len(records),'distinct_tasks':len({r['generation']['mathematical_key'] for r in records}),'finite_shortage':max(0,needed-len(records)),'supplied_generated_file_exists':JOB.with_suffix('.generated').exists(),'supplied_instances_validated':len(instances),'generator_version':g.VERSION,'generator_sha256':sha(H.with_suffix('.py')),'asset_hashes':[]})
        forms=transaction(records,kp)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'distinct_available_hard':c['distinct_available_hard']};finish(path,verified,inv);return
        txpath=path/'transaction.edn';text=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(text);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b;report_checks(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','lineage':LINEAGE,'endpoint':DB.args.endpoint,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'sha256':sha(txpath),'exact_edn':text,'request_key':'cotangent-hard-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'generator_id':g.GENERATOR_ID,'generator_path':SCRIPT,'generator_sha256':sha(H.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'lock':str(LOCK),'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(report,path,intent);finish(path,verified,inventory(native,path/'inventory-after.json'))

if __name__=='__main__':main()
