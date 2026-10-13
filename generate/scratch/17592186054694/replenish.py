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

spec = importlib.util.spec_from_file_location('line_table_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP, TOPIC = g.KP_ID, 17592186050790
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.S['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'3d19445a570edd44d53820a96788fa0c23b6df58d379a7a2235b2fee8b89e10b'
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
    jobs = [j for j in result['jobs'] if j['knowledgePoint']==KP and j['difficulty']=='easy']
    assert len(jobs)<=1
    return result, {'easy':jobs[0]['available'] if jobs else 5, 'moderate':0, 'hard':0}

def fingerprint(q):
    return g.fingerprint(q)

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

def finish(path, gid, verified, binary):
    inv,available=inventory(binary,path/'inventory-after.json')
    prep=json.loads((path/'preparation.json').read_text())
    remaining=max(0,5-available['easy'])
    if prep['unproduced_by_level']['easy']==0: assert remaining==0
    caps=json.loads((HERE/'capabilities.json').read_text())
    result={'outcome':'finite-limit' if remaining else 'generated','knowledgePoint':KP,'topic':TOPIC,'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_questions_by_level':verified['by_level'],'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'unsupported_levels_filled':False,'inventory_scope':'lesson requested KP','inventory_recheck_basis':inv['basis'],'available_by_level':available,'remaining_supported_shortages':{'easy':remaining},'capability_exceptions':caps['exceptions'],'finite_limits':caps['finite_limits'],'remaining_unclassified_source_questions':1,'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',path/'generated.json',path/'native-report.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md')],'note':'Easy reserve reaches five. Moderate/hard remain explicitly unfilled. Incomplete unrated original and learner history preserved; generated negative-slope key/solution/difficulty are documented authored additions.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps(result,indent=2),flush=True)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    validation=json.loads((HERE/'validation.json').read_text())
    assert validation['passed']
    assert sha(HERE.with_suffix('.py'))==validation['hashes'][SCRIPT]
    binary=build_learning(ROOT.parent/'EDB')
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE
            assert intent['transaction_sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path)
            finish(path,intent['generator_id'],verify(path,intent,report),binary)
            return
        inv,available=inventory(binary,OUT/'inventory-before.json')
        b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        current=json.loads(json.dumps(kp,default=str))
        source=g.S['record']
        existing={q[':db/id']:q for q in current[':knowledge-point/questions']}
        assert all(existing[q[':db/id']]==q for q in source[':knowledge-point/questions']), 'Source changed; reclassify'
        assert current[':knowledge-point/canonical-example']==source[':knowledge-point/canonical-example']
        contributor=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b)
        assert len(contributor)==1
        gen=kp.get(':knowledge-point/question-generator')
        registered=DB.query('[:find (pull ?g [*]) :in $ ?path :where [?g :question-generator/script ?path]]',[SCRIPT],path,'generator-by-script',b)
        assert len(registered)<=1
        gid=str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        collision=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-by-id',b)
        assert not collision or collision[0][0][':question-generator/script']==SCRIPT
        needed={l:max(0,5-available[l]) if l=='easy' else 0 for l in LEVELS};selected={l:0 for l in LEVELS}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records=[];checked=[]
        supplied_path=JOB.with_suffix('.generated')
        supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        def consider(rec):
            v.check(rec)
            assert rec['knowledge_point']['db_id']==KP and rec['knowledge_point']['id']==g.KP_UUID
            assert not rec['generation']['replay']
            l='easy';assert rec['question'][':question/difficulty']==':question.difficulty/easy'
            replay=g.generate(l,rec['generation']['seed'],rec['generation']['template'],parameters=rec['generation']['parameters'])
            assert normalized(replay['question'])==normalized(rec['question'])
            checked.append(rec)
            fp=fingerprint(rec['question'])
            if selected[l]<needed[l] and fp not in used:records.append(rec);used.add(fp);selected[l]+=1
        for rec in instances:consider(rec)
        previews=[g.generate('easy',1994,t,g.candidates(t)[0]) for t in g.TEMPLATES]
        for rec in previews:consider(rec)
        for rec in g.batch('easy',18,1994):
            if selected['easy']>=needed['easy']: break
            consider(rec)
        library=ImageLibrary(Path(database_environment('math')['EDB_MATH_ROOT']))
        published=[]
        for rec in records:
            mapping={}
            for asset in set(rec['generation']['assets']):
                local=Path(asset)
                if not local.is_absolute(): continue
                digest=sha(local)
                relative=library.put_file(local,expected_sha256=digest)
                assert sha(library.math_root/relative)==digest
                mapping[asset]=relative
                published.append({'local':asset,'relative':relative,'sha256':digest})
            for local,relative in mapping.items():
                rec['question'][':question/worked-solution']=rec['question'][':question/worked-solution'].replace(local,relative)
                for answer in rec['question'][':question/answer-fields'][0][':answer-field/choices']:
                    if answer[':answer/value']==local:answer[':answer/value']=relative
            rec['generation']['asset_rewrites']=mapping
            v.check(rec)
        save(path/'validated-previews.json',previews)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        save(path/'generated.json',records)
        (path/'validated-previews.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in previews)+'\n')
        save(path/'native-input.json',[v.native(r['question'][':question/id'],r) for r in checked])
        subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        if ids:assert not DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'generated-identities',b)
        save(path/'preparation.json',{'basis':b,'original_job_basis':1994,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'generator_sha256':sha(HERE.with_suffix('.py')),'missing_by_level':needed,'selected_by_level':selected,'unproduced_by_level':{l:needed[l]-selected[l] for l in LEVELS},'available_by_level_before':available,'inventory_scope':'lesson requested KP','source_evidence_unchanged':True,'assets':published,'validated_preview_count':len(previews),'supplied_generated_exists':supplied_path.exists(),'distinctness':'exact line slope/intercept mathematical fingerprint; canonical and every existing practice excluded; seed, identity and order do not add tasks'})
        forms=transaction(records,kp,gid)
        assert forms, 'Already registered; recover previous registration evidence'
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout)
        pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_datoms(pr,path/'preview-check',contributor[0][0])
        assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':contributor[0][0],'basis':b,'expected_basis':b,'request_key':'line-table-replenish-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        finish(path,gid,verify(path,intent,report),binary)

if __name__=='__main__':main()
