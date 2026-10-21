"""Register/replenish only this KP, using the application lock and EDB boundary."""
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture'), str(ROOT/'generate/scripts')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
from image_library import ImageLibrary

spec = importlib.util.spec_from_file_location('equal_flow_inventory_validation', HERE/'validate_inventory.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP, TOPIC = g.KP_ID, 17592186049774
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'a6c880f17b9457670be97096d570f2feb4a6ae682efbd7b58e7f6629dbd2bb92'
OUT = HERE/'reference/replenishment'
LEVELS = ('easy', 'moderate', 'hard')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY = (HERE/'source-query.edn').read_text()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]

def inventory(binary, path):
    request = {'action':'inventory'}
    response = subprocess.run([str(binary), 'math', LEARNER, DB.args.endpoint], input=json.dumps(request), env=DB.env, capture_output=True, text=True, check=True, timeout=55)
    result = json.loads(response.stdout)
    assert result['ok'], result
    result = result['data']
    assert result['lineage'] == LINEAGE
    save(path, result)
    jobs = [j for j in result['jobs'] if j['knowledgePoint']==KP]
    # The native reader omits stocked bands and bands never observed in the DB.
    observed={q.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] for q in read_kp(path.parent/'inventory-kp',result['basis'])[':knowledge-point/questions']}
    counts={l:next((j['available'] for j in jobs if j['difficulty']==l),5 if l in observed else 0) for l in LEVELS}
    return result,counts

def fingerprint(q):
    return v.fingerprint(q)

def normalized(q):
    q = json.loads(json.dumps(q, default=str))
    q = {k:q[k] for k in (':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields')}
    if isinstance(q[':question/difficulty'], dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
    fields=[]
    for f in q[':question/answer-fields']:
        kind=f[':answer-field/type']
        correct=f[':answer-field/correct']
        fields.append({':answer-field/id':f[':answer-field/id'], ':answer-field/key':f[':answer-field/key'], ':answer-field/type':kind[':db/ident'] if isinstance(kind,dict) else kind,
            ':answer-field/correct':[':answer/id',correct[':answer/id']] if isinstance(correct,dict) else correct,
            ':answer-field/choices':sorted([{':answer/id':a[':answer/id'], ':answer/value':a[':answer/value'], ':answer/type':a[':answer/type'][':db/ident'] if isinstance(a[':answer/type'],dict) else a[':answer/type']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/value'])})
    q[':question/answer-fields']=sorted(fields,key=lambda f:f[':answer-field/key'])
    return q

def transaction(records, kp, gid):
    forms=[]
    for rec in records:
        q=rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen=kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'),KP,kw('knowledge-point/question-generator'),'generator']])
    else:assert str(gen[':question-generator/id'])==gid and gen[':question-generator/script']==SCRIPT
    if records:forms.append({kw('db/id'):KP,kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:forms.append([kw('db/ensure'),KP,kw('knowledge-point/validate')])
    return forms

def check_datoms(report, path, source):
    attrs={e:str(a) for e,a in DB.attributes(path,report[':edb/db-before-t'])}
    new=set(report[':edb/tempids'].values())
    allowed={':question/'+s for s in ('id','problem','worked-solution','difficulty','answer-fields')} | {':answer-field/'+s for s in ('id','key','type','choices','correct')} | {':answer/'+s for s in ('id','type','value')} | {':question-generator/id',':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s==source and added, 'Unexpected source or retraction'
        name=attrs[a]
        if e==KP:assert name in (':knowledge-point/questions',':knowledge-point/question-generator')
        elif name!=':db/txInstant':assert e in new and name in allowed

def verify(path, intent, report):
    assert report[':edb/committed'] and report[':edb/db-before-t']==intent['basis']
    check_datoms(report,path/'receipt-check',intent['source_eid'])
    kp=read_kp(path/'readback',report[':edb/db-after-t'])
    before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']}
    now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    omit={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:x for k,x in before.items() if k not in omit}=={k:x for k,x in kp.items() if k not in omit}
    records=json.loads((path/'generated.json').read_text())
    assert len(now)==len(old)+len(records)
    byid={str(q[':question/id']):q for q in now.values()}
    for rec in records:
        v.check(rec)
        q=byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalized(q)==normalized(rec['question'])
    assert not transaction([],kp,intent['generator_id'])
    verification={'passed':True,'basis_before':intent['basis'],'basis_after':report[':edb/db-after-t'],'new_questions':len(records),'by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0}
    save(path/'verification.json',verification)
    return verification

def finish(path,gid,verified,binary):
    inv,available=inventory(binary,path/'inventory-after.json')
    prep=json.loads((path/'preparation.json').read_text())
    remaining={l:max(0,5-available[l]) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'topic':TOPIC,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'available_by_level_before':prep['available_by_level_before'],'available_by_level_after':available,'available_counts_are_lower_bounds':True,'remaining_shortages':remaining,'capability_exceptions':[],'finite_limits':json.loads((HERE/'validation.json').read_text())['default_sampler_meaningful_tasks'],'remaining_incomplete_source_questions':1,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'generated.json',path/'native-report.json',path/'inventory-after.json',HERE/'validation.json',HERE/'reference/current-source-validation.json',HERE/'classification.md',HERE/'template-extraction.md'] if p.exists()],'note':'Only deficits generated. Hard is the previously validated authored feed-unit-conversion variant of the same IVP. All ten existing source questions, canonical example and learner history preserved. The incomplete unrated original remains excluded.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions_by_level','remaining_shortages')},indent=2),flush=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    validation=json.loads((HERE/'validation.json').read_text());assert validation['status']=='pass' and validation['source_banks_matched']==7 and validation['native']['documented_unresolved_checks']==0
    binary=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    print('Waiting for application api.lock',flush=True)
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);print('Application lock acquired',flush=True)
        inv,available=inventory(binary,OUT/'inventory-under-lock.json')
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['endpoint']==DB.args.endpoint and intent['lineage']==inv['lineage']==LINEAGE and intent['source']==SOURCE
            assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path)
            finish(path,intent['generator_id'],verify(path,intent,report),binary);return
        b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        current=json.loads(json.dumps(kp,default=str));reviewed=json.loads((OUT/'initial.json').read_text())['kp']
        assert current==reviewed,'Live source changed since reviewed basis; reclassify'
        evidence=[];checks=[]
        for q in current[':knowledge-point/questions']:
            ev=v.source_check(q);evidence.append(ev)
            if ev['gradable']:
                rec={'question':q}
                f=rec['question'][':question/answer-fields'][0]
                f[':answer-field/type']=f[':answer-field/type'][':db/ident']
                f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
                for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
                q[':question/difficulty']=q[':question/difficulty'][':db/ident']
                checks.append(v.native(rec))
        save(path/'current-source-validation.json',{'basis':b,'rows':evidence})
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        registered=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',b);assert len(registered)<=1
        gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
        assert not collision or collision[0][0][':question-generator/script']==SCRIPT
        needed={l:max(0,5-available[l]) for l in LEVELS};selected={l:0 for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[]
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        def consider(rec):
            v.check(rec)
            l=rec['question'][':question/difficulty'].split('/')[-1]
            fp=fingerprint(rec['question'])
            if selected[l]<needed[l] and fp not in used:
                records.append(rec);used.add(fp);selected[l]+=1
        for rec in instances:consider(rec)
        # No changes to targets or task meaning merely for distinctness: normalize IVP and requested demand.
        for l in LEVELS:
            for i in range(300):
                if selected[l]>=needed[l]:break
                consider(g.generate(l,seed=183100+i))
        save(path/'generated.json',records)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        checks.extend(v.native(rec) for rec in records)
        save(path/'native-input.json',checks)
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        native=json.loads((path/'native-report.json').read_text());assert native['documented_unresolved_checks']==0
        (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(rec) for rec in records)+'\n')
        ids=[uuid.UUID(x) for rec in records for x in [rec['question'][':question/id']]+[f[':answer-field/id'] for f in rec['question'][':question/answer-fields']]+[a[':answer/id'] for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        if ids:assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',b)
        save(path/'preparation.json',{'basis':b,'original_job_basis':1831,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(HERE/'validate_inventory.py'),'missing_by_level':needed,'selected_by_level':selected,'unproduced_by_level':{l:needed[l]-selected[l] for l in LEVELS},'available_by_level_before':available,'available_counts_are_lower_bounds':True,'source_evidence_unchanged':True,'assets':[],'mathematical_fingerprints':[list(fingerprint(rec['question'])) for rec in records],'distinctness':'normalized equilibrium, removal coefficient, initial mass, time and response/unit demand; excludes all prior source and canonical tasks, context aliases, seed and choice order'})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'basis_after':b,'new_questions':0,'by_level':{l:0 for l in LEVELS},'no_changes':True}
            save(path/'verification.json',verified);finish(path,gid,verified,binary);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        fresh,available_now=inventory(binary,path/'inventory-precommit.json');assert fresh['basis']==b and available_now==available and DB.basis()==b
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout)
        pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_datoms(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'equal-flow-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[rec['question'][':question/id'] for rec in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        print('Submitting prepared transaction at basis '+str(b),flush=True)
        report=DB._commit(intent,txpath,path)
        finish(path,gid,verify(path,intent,report),binary)

if __name__=='__main__':main()
