"""Validate, prepare and add only this KP's inventory through the existing EDB boundary."""
import argparse
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
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture'), str(HERE)]
from database import Database
from edn import dumps, loads
from image_library import ImageLibrary
from inventory_jobs import save
from serve_graph_explorer import database_environment
import db_support as support

# The full source-replay validator also provides the independent rendered-math check.
spec = importlib.util.spec_from_file_location('slope_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP, SCRIPT = g.KP_ID, support.SCRIPT
LEVELS = ('easy', 'moderate', 'hard')
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'197ba0efa9ddcb651b1ed47bfa831e761bc033a8b91c3f54afd1876dd2fbee5b'
OUT = HERE/'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT'], postgres_url=ENV['EDB_POSTGRES_URL']))
support.DB = DB
QUERY = (HERE/'reference/source-query.edn').read_text()
USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(ROOT/'.local/graph-explorer/learning-1275f16a95dc6372'), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=ENV, text=True, capture_output=True, check=True, timeout=55)
    result = json.loads(r.stdout)
    assert result['ok'] and result['data']['lineage'] == LINEAGE
    save(path, result['data'])
    return result['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value, (tuple,list)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value, uuid.UUID):
        return str(value)
    return value

def source_projection(actual, expected):
    """Compare every captured field while allowing extra current Pull selectors."""
    if isinstance(expected, dict):
        return {str(k):source_projection(actual[k],x) for k,x in expected.items()}
    if isinstance(expected, list):
        if expected and isinstance(expected[0], dict):
            identity = next(k for k in (':db/id', ':answer/id', ':answer-field/id', ':question/id', ':db/ident') if all(k in x for x in expected))
            lookup = {str(x[identity]):x for x in actual}
            assert len(actual)==len(expected)
            return [source_projection(lookup[str(x[identity])],x) for x in expected]
    return actual

def source_refresh(kp, path, basis):
    assert str(kp[':knowledge-point/id']) == g.KP_UUID
    current = {q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
    for q in g.SOURCE['record'][':knowledge-point/questions']:
        assert canonical(source_projection(current[q[':question/math-academy-id']],q)) == canonical(q), 'Source changed; reclassification required'
    expected = g.SOURCE['record'][':knowledge-point/canonical-example']
    assert canonical(source_projection(kp[':knowledge-point/canonical-example'],expected))==canonical(expected)
    save(path/'source-refresh.json', {'passed':True,'current_basis':basis,'source_basis':g.SOURCE['basis'],'practice_questions':7,'canonical_example_unchanged':True})

def checks(rec):
    f=rec['question'][':question/answer-fields'][0]
    return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete image radio bank'} for a in f[':answer-field/choices']]

def grade(records, path):
    save(path/'native-input.json', [{'label':r['question'][':question/id'],'record':r,'checks':checks(r)} for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'), str(path/'native-input.json'), str(path/'native-report.json')], check=True, timeout=55)

def known_records():
    return [r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())]

def localize(rec):
    rec=copy.deepcopy(rec)
    for asset in rec['generation'].get('published_assets',[]):
        for f in rec['question'][':question/answer-fields']:
            for a in f[':answer-field/choices']:
                if a[':answer/value']==asset['database_path']:a[':answer/value']=asset['local_path']
        rec['question'][':question/worked-solution']=rec['question'][':question/worked-solution'].replace(asset['database_path'],asset['local_path'])
    return rec

def fingerprint_question(q):
    mid=q.get(':question/math-academy-id')
    if mid in g.PROFILES:
        t,p,_=g.PROFILES[mid]
        return g.digest({'equation':str(g.eq(t,p)),'points':sorted(p['points'])})
    if mid=='e-8505':
        return g.digest({'equation':str(2*g.X**2-g.Y),'points':sorted([[1,1],[0,1],[1,2]])})
    for r in known_records():
        if r['question'][':question/id']==str(q[':question/id']):
            assert support.normalize(q)==support.ordered(r['question'])
            return r['generation']['mathematical_fingerprint']
    raise ValueError('Unrecognized existing mathematical content; reconcile before generation')

def counts(kp, path, basis):
    seen={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    seen.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historical-unavailable',basis,history=True))
    save(path/'scoped-snapshot.json', support.scoped(kp,basis,seen))
    subprocess.run([str(HERE/'check-pool'),str(path/'scoped-snapshot.json'),str(path/'native-pool.json')],check=True,timeout=55,capture_output=True)
    structural=json.loads((path/'native-pool.json').read_text())['available_ids_by_level']
    admitted={q for ids in structural.values() for q in ids}
    rows={level:[] for level in LEVELS};excluded=[];sources=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        if q[':db/id'] not in admitted or level not in LEVELS or not q.get(':question/worked-solution'):
            excluded.append({'id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':'shown, reserved, canonical, unrated, incomplete or excluded by native pool'})
            continue
        fp=fingerprint_question(q)
        if q.get(':question/math-academy-id'):
            for f in q[':question/answer-fields']:
                for a in f[':answer-field/choices']:
                    assert (Path(ENV['EDB_MATH_ROOT'])/a[':answer/value']).is_file()
            sources.append({'question':support.normalize(q),'knowledge_point':{'title':g.TITLE},'generation':{'template':g.PROFILES[q[':question/math-academy-id']][0]}})
        else:
            rec=next(r for r in known_records() if r['question'][':question/id']==str(q[':question/id']))
            v.check(localize(rec))
        rows[level].append((q,fp))
    if sources:grade(sources,path)
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({fp for q,fp in qs}),'question_ids':[str(q[':question/id']) for q,fp in qs]} for level,qs in rows.items()},'excluded':excluded,'historical_or_reserved':sorted(seen),'entry_point':'assessment_sampling::pool plus mathematical/source validation'}
    save(path/'available-counts.json',result)
    return result

def publish(records):
    library=ImageLibrary(ENV['EDB_MATH_ROOT']);result=copy.deepcopy(records);assets=[]
    for rec in result:
        rec_assets=[]
        for f in rec['question'][':question/answer-fields']:
            for a in f[':answer-field/choices']:
                local=a[':answer/value'];relative=library.put_file(ROOT/local)
                asset={'local_path':local,'database_path':relative,'sha256':sha(ROOT/local)}
                assert sha(Path(ENV['EDB_MATH_ROOT'])/relative)==asset['sha256']
                a[':answer/value']=relative
                rec['question'][':question/worked-solution']=rec['question'][':question/worked-solution'].replace(local,relative)
                rec_assets.append(asset);assets.append(asset)
        rec['generation']['published_assets']=rec_assets
        v.check(localize(rec))
    return result,assets

def prepare_candidates():
    inv=inventory(OUT/'inventory-before.json');kp=read_kp(OUT/'initial',inv['basis'])
    source_refresh(kp,OUT/'initial',inv['basis']);c=counts(kp,OUT/'initial',inv['basis'])
    supplied=JOB.with_suffix('.generated');data=json.loads(supplied.read_text()) if supplied.exists() else {}
    candidates=data.get('instances',[]) if isinstance(data,dict) else data
    assert isinstance(candidates,list)
    for r in candidates:v.check(r)
    save(OUT/'supplied-status.json',{'exists':supplied.exists(),'validated_instances':len(candidates)})
    used={fingerprint_question(q) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]}
    for r in candidates:used.add(r['generation']['mathematical_fingerprint'])
    # Retain a small reserve so a newer inventory basis can consume fresh candidates.
    for level in LEVELS:
        n=sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in candidates)
        target=max(0,5-c['levels'][level]['distinct_available_tasks'])
        for seed in range(720380,720480):
            if n>=target:break
            r=g.generate(level,seed);fp=r['generation']['mathematical_fingerprint']
            if fp in used:continue
            v.check(r);candidates.append(r);used.add(fp);n+=1
        assert n>=target, 'Bounded sampler unable to fill; record a capability exception'
    # Explicit slot test: hold coefficients fixed and vary one queried coordinate.
    first=g.generate('easy',parameters={'a':1,'b':2,'points':[[-2,1],[1,1],[2,1]]},template='affine')
    second=g.generate('easy',parameters={'a':1,'b':2,'points':[[-1,1],[1,1],[2,1]]},template='affine')
    for r in (first,second):v.check(r)
    assert first['generation']['exact_slopes'][0]!=second['generation']['exact_slopes'][0]
    assert first['question'][':question/worked-solution']!=second['question'][':question/worked-solution']
    save(OUT/'changed-target.json',{'passed':True,'records':[first,second],'held_fixed':['template','coefficients','second and third coordinates'],'changed_slot':'first point x coordinate; prompt choice geometry, worked substitution and answer agree'})
    grade(candidates,OUT)
    save(OUT/'candidates.json',candidates)
    save(OUT/'candidate-validation.json',{'passed':True,'generator_sha256':sha(HERE.with_suffix('.py')),'distinct_tasks':len({r['generation']['mathematical_fingerprint'] for r in candidates}),'count':len(candidates),'each_rendered_prompt_and_solution_parsed':True,'five_distinct_choice_geometries':True,'actual_learner_grader':True})
    print(json.dumps({'candidate_count':len(candidates),'current_counts':c['levels']}),flush=True)

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    support.check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis);before=loads((path/'before.edn').read_text())
    old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    ignore={':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in ignore}=={k:v for k,v in kp.items() if k not in ignore}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    for r in records:
        q=byid[r['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert support.normalize(q)==support.ordered(r['question']);v.check(localize(r))
        for a in r['generation']['published_assets']:assert sha(Path(ENV['EDB_MATH_ROOT'])/a['database_path'])==a['sha256']
    assert not support.transaction([],kp,intent['generator_id'])
    grade(records,path/'readback')
    c=counts(kp,path/'after-counts',basis)
    verified={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'new_by_level':{l:sum(r['question'][':question/difficulty']==':question.difficulty/'+l for r in records) for l in LEVELS},'unchanged_source_questions':len(old),'unchanged_canonical_example':True,'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'application_contributor':SOURCE,'generator_registration_verified':True,'stored_asset_hashes_verified':True,'repeat_preparation_changes':0,'available_counts_after':c}
    save(path/'verification.json',verified)
    return verified

def finish(path,gid,verified,inv):
    c=verified['available_counts_after'];remaining={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'topic':17592186048489,'database':'math','lineage':LINEAGE,'generator_path':SCRIPT,'generator_id':gid,'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_by_level':verified.get('new_by_level',{}),'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'shortage_remaining':remaining,'available_after':c,'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_questions_and_learner_history_preserved':True,'application_contributor':SOURCE,'note':'The legacy unrated source questions are preserved, including missing keys and solutions. Moderate/hard use the documented authored arithmetic workload; no global slope-field reasoning is introduced.','evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'source-refresh.json',path/'inventory-after.json',OUT/'candidate-validation.json',OUT/'changed-target.json',OUT/'native-report.json',HERE/'validation.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'capabilities.json'] if p.exists()]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','new_by_level','shortage_remaining','remaining_jobs')}),flush=True)

def commit():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed'] and validation['script_sha256']==sha(HERE.with_suffix('.py'))
    candidates=json.loads((OUT/'candidates.json').read_text())
    for r in candidates:v.check(r)
    preview=preview_executable(SimpleNamespace(math_root=Path(ENV['EDB_MATH_ROOT']),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['endpoint']==DB.args.endpoint
                assert intent['sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report);finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-locked.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True);kp=read_kp(path,basis);source_refresh(kp,path,basis)
        (path/'before.edn').write_text(dumps(kp)+'\n')
        gen=kp.get(':knowledge-point/question-generator')
        caps=json.loads((HERE/'capabilities.json').read_text())
        gid=str(gen[':question-generator/id']) if gen else caps['generator_id']
        assert gid==caps['generator_id']
        orphan=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',basis)
        if orphan:assert gen and orphan[0][0]==gen
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used={fingerprint_question(q) for q in kp[':knowledge-point/questions']+[kp[':knowledge-point/canonical-example']]}
        records=[];added={l:0 for l in LEVELS}
        for r in candidates:
            l=r['question'][':question/difficulty'].split('/')[-1];fp=r['generation']['mathematical_fingerprint']
            if added[l]<needed[l] and fp not in used:
                records.append(r);used.add(fp);added[l]+=1
        assert added==needed, 'Inventory changed beyond prepared capacity; prepare again before committing'
        ids=[uuid.UUID(x) for r in records for x in [r['question'][':question/id'],r['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]]
        existing=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not existing, 'Identity collision requires reconciliation, never overwrite'
        save(path/'generated-local.json',records);records,assets=publish(records);save(path/'generated.json',records);grade(records,path)
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'asset_hashes':assets,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'distinct_tasks':len(records),'source_unchanged':True,'supplied_instances_status':json.loads((OUT/'supplied-status.json').read_text())})
        forms=support.transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'no_changes':True,'available_counts_after':c}
            save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=55)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis
        support.check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'isolated-slope-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'transaction_sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report);finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--commit',action='store_true');args=parser.parse_args()
    commit() if args.commit else prepare_candidates()
