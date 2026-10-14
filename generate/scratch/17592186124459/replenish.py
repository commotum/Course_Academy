"""Scoped replenishment through the application's EDB boundary and durable lock."""
import copy
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment,build_learning
import validate as v
import source_audit
g=v.g
KP=g.KP
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE=g.WRAPPER['lineage']
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'141daeb3d1c0c8a84f2e17bfb51d2cb360f832d98f743e7f5c8984fd301b90f3'
OUT=HERE/'reference/replenishment'
LEVELS=('easy','moderate','hard')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY=(HERE/'reference/initial/kp-query.edn').read_text()
INITIAL=json.loads((HERE/'reference/initial/kp.json').read_text())
UNAVAILABLE='''[:find ?q :in $ ?learner ?kp
 :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
   (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
   (and [?l :learner/activity ?t] [?t :learner-task/activity ?a]
     (or [?t :learner-task/status :learner-task.status/started]
         [?t :learner-task/status :learner-task.status/paused])
     (or [?a :activity/type :activity.type/lesson]
         [?a :activity/type :activity.type/review]
         [?a :activity/type :activity.type/assessment])
     [?a :activity/steps ?st] [?st :step/content ?q]))]'''

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
def plain(value):return json.loads(json.dumps(value,default=str))

def inventory(binary,path):
    proc=subprocess.run([str(binary),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=DB.env,capture_output=True,text=True,check=True,timeout=55)
    response=json.loads(proc.stdout)
    assert response['ok'] and response['data']['lineage']==LINEAGE
    save(path,response['data'])
    return response['data']

def normalize(q):
    def norm(z):
        if isinstance(z,dict):
            if set(z)-{':db/id'}=={':db/ident'}:return str(z[':db/ident'])
            return {k:norm(v) for k,v in z.items() if k not in (':db/id',':knowledge-point/_questions',':knowledge-point/_canonical-example')}
        if isinstance(z,list):return [norm(v) for v in z]
        return str(z) if isinstance(z,uuid.UUID) else z
    out=norm(q)
    for f in out.get(':question/answer-fields',[]):
        if isinstance(f.get(':answer-field/correct'),dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
        f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda a:a[':answer/id'])
    return out

def native(r):
    f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
    return {'label':str(r['question'][':question/id']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'every owned radio choice'} for a in f[':answer-field/choices']]}

def fingerprint(q):
    F,vs,P,d,E,target,unit=v.prompt({'question':q})
    first=next(e for e in target if e!=0)
    return g.digest([[str(v.S.simplify(e/v.S.Abs(first))) for e in target],unit])

def validate_sources(kp):
    current={q[':db/id']:plain(q) for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    expected={q[':db/id']:q for q in INITIAL[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    assert current==expected,'Current source changed; reopen classification'
    assert plain(kp[':knowledge-point/canonical-example'])==INITIAL[':knowledge-point/canonical-example']

AUDIT={r['id']:r for r in json.loads((HERE/'reference/initial/source-audit.json').read_text())}
def counts(kp,path,basis,records=()):
    unavailable={r[0] for r in DB.query(UNAVAILABLE,[LEARNER,KP],path,'unavailable',basis)}
    unavailable.update(r[0] for r in DB.query(UNAVAILABLE,[LEARNER,KP],path,'historically-unavailable',basis,history=True))
    byid={r['question'][':question/id']:r for r in records}
    for manifest in OUT.glob('basis-*/generated.json'):
        for r in json.loads(manifest.read_text()):byid[r['question'][':question/id']]=r
    used=set();available={l:{} for l in LEVELS};excluded=[]
    for q in kp[':knowledge-point/questions']:
        ident=str(q[':question/id']);level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if ident in byid:
            r=byid[ident];assert normalize(q)==normalize(r['question']);fp=fingerprint(r['question']);valid=True
        else:
            audit=AUDIT[q[':db/id']];valid=audit['validated']
            fp=g.digest([audit['direction'],False]) if 'direction' in audit else 'invalid:'+ident
        used.add(fp)
        if not valid or level not in LEVELS:
            excluded.append({'id':q[':db/id'],'errors':AUDIT.get(q[':db/id'],{}).get('errors',[])});continue
        if q[':db/id'] not in unavailable:available[level][fp]=ident
    result={'basis':basis,'available_by_level':{l:len(z) for l,z in available.items()},
        'available_question_ids':{l:sorted(z.values()) for l,z in available.items()},
        'excluded_sources':excluded,'shown_or_reserved_ids':sorted(unavailable),
        'distinctness':'Oriented direction modulo positive scale; same answer demand. Seed, profile, choice order and context aliases do not enlarge counts.'}
    save(path/'validated-inventory.json',result)
    return result,used

def transaction(records,kp,gid):
    forms=[]
    for r in records:
        q=r['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw(a[':answer/type']),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'],kw('answer-field/id'):uuid.UUID(f[':answer-field/id']),kw('answer-field/key'):f[':answer-field/key'],kw('answer-field/type'):kw(f[':answer-field/type']),kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']],kw('answer-field/correct'):f[':answer-field/correct'][1],kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'],kw('question/id'):uuid.UUID(q[':question/id']),kw('question/problem'):q[':question/problem'],kw('question/worked-solution'):q[':question/worked-solution'],kw('question/difficulty'):kw(q[':question/difficulty']),kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']],kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator',kw('question-generator/id'):uuid.UUID(gid),kw('question-generator/script'):SCRIPT},[kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_datoms(report,path,source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')}|{':answer-field/'+s for s in ('id','key','type','choices','correct')}|{':answer/'+s for s in ('id','type','value')}|{':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added,'Unexpected attribution or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed,'Unexpected existing entity change'

def verify(path,intent,report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_datoms(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    omit={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:z for k,z in before.items() if k not in omit}=={k:z for k,z in kp.items() if k not in omit}
    records=json.loads((path/'generated.json').read_text())
    assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for r in records:
        v.check(r)
        q=byid[r['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q)==normalize(r['question'])
    assert not transaction([],kp,intent['generator_id'])
    stock,_=counts(kp,path/'post-inventory',report[':edb/db-after-t'],records)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],
        'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty'].endswith('/'+l) for r in records) for l in LEVELS},
        'unchanged_existing_questions':len(old),'unchanged_canonical_example':True,
        'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,
        'generator_registration_verified':True,'repeat_preparation_content_changes':0,'inventory':stock}
    save(path/'verification.json',result)
    return result

def finish(path,intent,verified,binary):
    inv=inventory(binary,path/'inventory-after.json')
    kp=read_kp(path/'final-inventory',inv['basis']);validate_sources(kp)
    stock,_=counts(kp,path/'final-inventory',inv['basis'])
    shortage={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(shortage.values()) else 'generated',
        'knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],
        'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],
        'new_questions':verified['new_questions'],'new_questions_by_level':verified['new_by_level'],
        'supported_levels':list(LEVELS),'hard_is_authored_extension':True,
        'available_by_level':stock['available_by_level'],'shortage_remaining':shortage,
        'unsupported_levels_filled':False,'inventory_recheck_basis':inv['basis'],
        'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
        'capability_exceptions':[{'type':'source-template-scope','filled':False,'reason':'Eight later source families are classified but are outside the frozen six-family generator; no generation or source fidelity is claimed for them.'},
            {'type':'source-errors','filled':False,'excluded':stock['excluded_sources'],'reason':'Current captured solution/format errors remain preserved and do not count as validated inventory.'},
            {'type':'finite-domain','filled':False,'reason':'42 trig oriented directions and 296 hard oriented unit directions in the documented bounded domains; aliases cannot enlarge counts.'}],
        'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'native-report.json',path/'source-native-report.json',path/'inventory-after.json',path/'final-inventory/validated-inventory.json',HERE/'validation.json',HERE/'reference/initial/kp.json',HERE/'reference/initial/source-audit.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'current-classification.md')],
        'note':'Supported reserves count mathematically validated gradable fresh questions. Later source templates are preserved and not claimed as generator coverage.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions_by_level','available_by_level','shortage_remaining','remaining_jobs')}),flush=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['passed'] and validation['native']['engine_sha256']==sha(ROOT/'generate/runs/current/check-engine')
    binary=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['transaction_sha256']==sha(path/'transaction.edn')
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path)
            finish(path,intent,verify(path,intent,report),binary)
            return
        inv=inventory(binary,OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);validate_sources(kp)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source_checks=[]
        for q in kp[':knowledge-point/questions']:
            if AUDIT.get(q[':db/id'],{}).get('validated'):
                source_checks.append(native({'knowledge_point':{'db_id':KP,'id':str(kp[':knowledge-point/id']),'title':kp[':knowledge-point/title']},'question':normalize(q)}))
        save(path/'source-native-input.json',source_checks)
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'source-native-input.json'),str(path/'source-native-report.json')],check=True)
        assert json.loads((path/'source-native-report.json').read_text())['documented_unresolved_checks']==0
        stock,used=counts(kp,path,b)
        needed={l:max(0,5-stock['available_by_level'][l]) for l in LEVELS}
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(contributor)==1
        registered=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',b);assert len(registered)<=1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else str(uuid.uuid5(uuid.UUID(g.SOURCE[':knowledge-point/id']),'question-generator'))
        collisions=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
        assert not collisions or collisions[0][0][':question-generator/script']==SCRIPT
        selected={l:0 for l in LEVELS};records=[];checked=[]
        supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        def consider(r):
            v.check(r)
            assert not r['generation']['evidence_only'] and r['generation']['eligible_for_learning']
            replay=g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])
            assert normalize(replay['question'])==normalize(r['question'])
            checked.append(r)
            l=r['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(r['question'])
            if selected[l]<needed[l] and fp not in used:
                records.append(r);used.add(fp);selected[l]+=1
        for r in instances:consider(r)
        for l in LEVELS:
            for i in range(max(needed[l]*8,1)):
                if selected[l]>=needed[l]:break
                consider(g.generate(l,int(JOB.name[:8],16)+i))
        assert all(selected[l]<=needed[l] for l in LEVELS)
        assets=[]  # This generator has no plots.
        save(path/'generated.json',records)
        save(JOB.with_suffix('.generated'),{'request':json.loads(JOB.with_suffix('.json').read_text())['request'],'instances':records,'preparation_basis':b})
        save(path/'native-input.json',[native(r) for r in checked])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        if ids:assert not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'generated-identities',b)
        save(path/'preparation.json',{'basis':b,'original_job_basis':1831,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'missing_by_level':needed,'selected_by_level':selected,'unproduced_by_level':{l:needed[l]-selected[l] for l in LEVELS},'available_before':stock,'source_evidence_unchanged':True,'asset_hashes':assets,'supplied_generated_exists':bool(supplied),'instances_validated':len(checked),'generator_sha256':sha(HERE.with_suffix('.py'))})
        forms=transaction(records,kp,gid);assert forms,'No changes: existing generator and inventory already sufficient'
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        proc=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(proc.stdout);pr=loads(proc.stdout)
        assert not pr[':edb/committed'] and pr[':edb/db-before-t']==b
        check_datoms(pr,path/'preview-check',contributor[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],
            'basis':b,'expected_basis':b,'request_key':'maximum-direction-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),
            'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,
            'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],
            'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),
            'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        finish(path,intent,verify(path,intent,report),binary)

if __name__=='__main__':main()
