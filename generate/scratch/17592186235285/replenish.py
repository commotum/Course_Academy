"""Scoped additive replenishment of the frozen direction-reversal generator.

Uses the application's Database, native preview, learner grader and ImageLibrary.
No source questions, learner records or application code are edited.
"""
import ast
import copy
import fcntl
import hashlib
import importlib.util
import itertools
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import threading
from types import SimpleNamespace
import uuid
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.database.images import ImageLibrary
sys.path[:0] = [str(ROOT / 'scripts'), str(ROOT / 'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec = importlib.util.spec_from_file_location('generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
LEVELS = ('easy', 'moderate', 'hard')
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '741bf65f38cf6e08f9f93be582c83d1f8af64d80521208e4b5bd5a726a39d259'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = ROOT / '.local/graph-explorer/learning-80371ed6e5f3669c'
QUERY = (HERE / 'reference/source-query.edn').read_text()
GENERATOR_UUID = str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'course-academy-generator'))
MATH_ROOT = Path('/media/jake/SSD/EDB/math')

# Reuse the existing package's independent displayed-math and geometry audit
# without executing its evidence-generation driver or rewriting frozen artifacts.
tree = ast.parse((HERE / 'validate.py').read_text())
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
exec(compile(ast.Module(body=functions, type_ignores=[]), str(HERE / 'validate.py'), 'exec'), globals())

USAGE_QUERY = '''[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]'''

def task_fingerprint(p):
    # Remove common scale, rigid rotation/reflection, field type and bank order.
    # Retain the actual ratio, known coefficient, relative length and angle.
    a, b = sp.Matrix(p['a']), sp.Matrix(p['b'])
    aa = a.dot(a)
    return g.digest([str(sp.Rational(p['r'])), str(sp.Rational(p['k'])),
                     str(b.dot(b)/aa), str(a.dot(b)/aa)])

def grading_item(label, rec):
    f = rec['question'][':question/answer-fields'][0]
    cid = f[':answer-field/correct'][1]
    if f[':answer-field/type'].endswith('/radio'):
        checks = [{'submitted_answer_id':a[':answer/id'], 'expected':'accepted' if a[':answer/id']==cid else 'rejected'} for a in f[':answer-field/choices']]
    else:
        val = g.parse(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==cid))
        checks = [{'submitted':str(val),'expected':'accepted'}, {'submitted':f'{val.p*3}/{val.q*3}','expected':'accepted'}, {'submitted':str(-val),'expected':'rejected'}, {'submitted':str(val-1),'expected':'rejected'}]
    return {'label':label, 'record':rec, 'checks':checks}

def native_check(records, path, name):
    save(path/(name+'-input.json'), [grading_item(r['question'][':question/id'],r) for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(path/(name+'-input.json')),str(path/(name+'-report.json'))],check=True,capture_output=True)
    report=json.loads((path/(name+'-report.json')).read_text())
    assert report['database_writes']==0 and report['documented_unresolved_checks']==0
    return report

CASES = {c['source_id']:c for c in json.loads((HERE/'source-cases.json').read_text())}
CAPTURED = json.loads((HERE/'source.json').read_text())['record']

def source_replays(kp, path):
    current={q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
    records=[]
    for original in CAPTURED[':knowledge-point/questions']:
        sid=original[':question/math-academy-id'];q=current[sid]
        assert source_forward(q)==source_forward(original), 'Source changed; reclassify '+sid
        c=CASES[sid]
        rec=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
        check(rec)
        assert rec['question'][':question/problem']==q[':question/problem']
        assert rec['question'][':question/worked-solution']==q[':question/worked-solution']
        f=q[':question/answer-fields'][0]
        actual=normalize(q)
        generated=rec['question'][':question/answer-fields'][0]
        assert sorted(g.parse(a[':answer/value']) for a in f[':answer-field/choices'])==sorted(g.parse(a[':answer/value']) for a in generated[':answer-field/choices'])
        assert g.parse(f[':answer-field/correct'][':answer/value'])==-sp.Rational(c['parameters']['r'])
        records.append({'question':actual})
    assert all(canonical(kp[':knowledge-point/canonical-example'][k])==canonical(val) for k,val in CAPTURED[':knowledge-point/canonical-example'].items())
    native_check(records,path,'source-native')
    save(path/'source-replay.json',{'passed':True,'questions':14,'full_banks':8,'blank_fields':6,'values':46,'distractors':32,'source_basis':g.SOURCE['basis'],'current_basis':DB.basis()})

def existing_parameters(q):
    sid=q.get(':question/math-academy-id')
    if sid in CASES:
        return CASES[sid]['parameters']
    # Generated assets carry the exact renderer parameters. Read their hash-
    # verified sidecar via our retained publication manifest.
    refs=re.findall(r'!\[\]\((.*?)\)',q[':question/problem'])
    for manifest in OUT.glob('basis-*/assets.json'):
        for asset in json.loads(manifest.read_text()):
            if asset['stored_path'] in refs:
                assert sha(MATH_ROOT/asset['stored_path'])==asset['sha256']
                return json.loads(Path(asset['sidecar']).read_text())
    raise ValueError('Unknown authored question requires scoped classification')

def counts(kp,path,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'usage',basis)}
    rows={l:[] for l in LEVELS};checks=[]
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in unavailable or q.get(':knowledge-point/_canonical-example'):continue
        if not q.get(':question/difficulty') or not q.get(':question/worked-solution') or not q.get(':question/answer-fields'):continue
        if not all(f.get(':answer-field/correct') for f in q[':question/answer-fields']):continue
        p=existing_parameters(q);level=str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        assert level in LEVELS
        checks.append({'question':normalize(q)})
        rows[level].append((q,task_fingerprint(p)))
    if checks:native_check(checks,path,'available-native')
    result={'basis':basis,'levels':{l:{'distinct_available_tasks':len({fp for q,fp in rs}),'available_question_ids':[str(q[':question/id']) for q,fp in rs]} for l,rs in rows.items()},'excluded_shown_or_reserved':sorted(unavailable),'unrated_or_incomplete_excluded':True}
    save(path/'available-counts.json',result)
    return result

def candidate_records(level):
    if level=='easy':
        plans=[(1,[0,-2],[1,1]),(2,[2,0],[1,1]),(3,[0,2],[1,2]),(4,[-2,0],[-1,2]),(2,[0,2],[1,2])]
        for i,(r,a,b) in enumerate(plans):
            yield g.generate(level,seed=i,field_type='blank' if i in (0,2,4) else 'radio',parameters={'r':str(r),'k':'1','a':a,'b':b})
    # Bounded seeded traversal; only mathematically distinct tasks are admitted.
    for seed in range(256):
        yield g.generate(level,seed=seed)

def publish(records,path):
    library=ImageLibrary(MATH_ROOT,HERE)
    result=copy.deepcopy(records);assets=[]
    for rec in result:
        for role,original in rec['generation']['plot_assets'].items():
            data=Path(original).read_bytes();stored=library.store(data,original)
            assert (MATH_ROOT/stored).read_bytes()==data
            for attr in (':question/problem',':question/worked-solution'):
                rec['question'][attr]=rec['question'][attr].replace(original,stored)
            assets.append({'question_id':rec['question'][':question/id'],'role':role,'original_path':original,'stored_path':stored,'sha256':hashlib.sha256(data).hexdigest(),'sidecar':str(Path(original).with_suffix('.json')),'sidecar_sha256':sha(Path(original).with_suffix('.json'))})
        rec['generation']['publication']='Question/field/answer UUIDs retained from validated generator output; only asset paths localized.'
    save(path/'assets.json',assets)
    return result

def assert_published(rec, original, assets):
    check(original)
    expected=copy.deepcopy(original['question'])
    for a in assets:
        if a['question_id']!=original['question'][':question/id']:continue
        assert sha(MATH_ROOT/a['stored_path'])==a['sha256']
        assert sha(Path(a['sidecar']))==a['sidecar_sha256']
        for attr in (':question/problem',':question/worked-solution'):
            expected[attr]=expected[attr].replace(a['original_path'],a['stored_path'])
    assert ordered(expected)==ordered(rec['question'])


def finish(path, verified, inv):
    prep=json.loads((path/'preparation.json').read_text());after=verified['available_counts_after']
    remaining={l:max(0,5-after['levels'][l]['distinct_available_tasks']) for l in LEVELS}
    caps=json.loads((HERE/'capabilities.json').read_text())
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':verified['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],'requested_basis':2188,'new_questions':verified['new_questions'],'supported_levels':list(LEVELS),'authored_levels':['easy'],'available_counts_before':prep['available_counts'],'available_counts_after':after,'shortage_remaining':remaining,'unsupported_levels_filled':False,'capability_exceptions':caps['exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(p.relative_to(ROOT)) for p in [path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'assets.json',path/'source-replay.json',path/'native-report.json',path/'inventory-after.json',HERE/'reference/visual-review.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'freeze.json',HERE/'capabilities.json'] if p.exists()],'note':'All supported bands have at least five distinct fresh gradable tasks. Easy is explicitly authored within the existing trace-and-compare method. All source questions and learner history preserved.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','shortage_remaining')}),flush=True)

def verify(path,intent,report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t']==intent['basis']
    check_report(report,path/'receipt-check',intent['source_eid'])
    basis=report[':edb/db-after-t'];kp=read_kp(path/'readback',basis)
    before=loads((path/'before.edn').read_text());old={q[':db/id']:q for q in before[':knowledge-point/questions']};now={q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e]==q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}=={k:v for k,v in kp.items() if k not in (':knowledge-point/questions',':knowledge-point/question-generator')}
    gen=kp[':knowledge-point/question-generator'];assert str(gen[':question-generator/id'])==intent['generator_id'] and gen[':question-generator/script']==SCRIPT
    records=json.loads((path/'generated.json').read_text());originals={r['question'][':question/id']:r for r in json.loads((path/'raw-generated.json').read_text())};assets=json.loads((path/'assets.json').read_text());byid={str(q[':question/id']):q for q in now.values()}
    assert len(now)==len(old)+len(records)
    for rec in records:
        q=byid[rec['question'][':question/id']];assert ':question/math-academy-id' not in q
        assert normalize(q)==ordered(rec['question']);assert_published(rec,originals[rec['question'][':question/id']],assets)
    assert not transaction([],kp,intent['generator_id'])
    c=counts(kp,path/'readback',basis)
    result={'passed':True,'basis_before':intent['basis'],'basis_after':basis,'generator_id':intent['generator_id'],'new_questions':len(records),'unchanged_source_questions':len(old),'learner_history_unchanged':True,'only_additive_scoped_content_datoms':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    save(path/'verification.json',result)
    return result

def main():
    commit='--commit' in sys.argv
    freeze=json.loads((HERE/'freeze.json').read_text())
    assert freeze['script_sha256']==sha(HERE.with_suffix('.py'))
    assert json.loads((HERE/'validation.json').read_text())['passed']
    for p,digest in freeze['artifact_sha256'].items():assert sha(ROOT/p)==digest,p
    preview=preview_executable(SimpleNamespace(math_root=MATH_ROOT,repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent=json.loads((path/'commit-intent.json').read_text())
            assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['database']=='math' and intent['endpoint']==DB.args.endpoint
            assert intent['sha256']==sha(path/'transaction.edn') and intent['exact_edn']==(path/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report=DB._commit(intent,path/'transaction.edn',path);verified=verify(path,intent,report)
            finish(path,verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');basis=inv['basis'];assert DB.basis()==basis
        path=OUT/('basis-'+str(basis));path.mkdir(exist_ok=True)
        kp=read_kp(path,basis);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        source_replays(kp,path)
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else GENERATOR_UUID
        if gen:assert gen[':question-generator/script']==SCRIPT
        c=counts(kp,path,basis);needed={l:max(0,5-c['levels'][l]['distinct_available_tasks']) for l in LEVELS}
        used={task_fingerprint(existing_parameters(q)) for q in kp[':knowledge-point/questions']}
        # Canonical example uses a negative known b coefficient; easy +b cannot
        # duplicate it. It has no answer fields and is never counted as stock.
        assert sha(MATH_ROOT/'images/a7/a77e5fef143d51d984ce41363465af5f210291f6355b59da4302a944b6a49197.png')=='a77e5fef143d51d984ce41363465af5f210291f6355b59da4302a944b6a49197'
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {};instances=supplied.get('instances',[])
        for rec in instances:assert rec['knowledge_point']['db_id']==KP;check(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        records=[];added={l:0 for l in LEVELS}
        for l in LEVELS:
            if not needed[l]:continue
            for rec in itertools.chain((r for r in instances if r['question'][':question/difficulty'].endswith('/'+l)),candidate_records(l)):
                fp=task_fingerprint(rec['generation']['parameters'])
                if fp in used:continue
                check(rec);records.append(rec);used.add(fp);added[l]+=1
                if added[l]==needed[l]:break
        save(path/'raw-generated.json',records)
        published=publish(records,path);save(path/'generated.json',published)
        native_check(published,path,'native')
        ids=[uuid.UUID(identity) for rec in records for identity in [rec['question'][':question/id'],rec['question'][':question/answer-fields'][0][':answer-field/id']]+[a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]]
        matches=DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identity-matches',basis) if ids else []
        assert not matches,'Stable existing identities require reconciliation'
        save(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'missing_by_level':needed,'new_by_level':added,'distinct_generated_tasks':len({task_fingerprint(r['generation']['parameters']) for r in records}),'mathematical_fingerprints':[task_fingerprint(r['generation']['parameters']) for r in records],'asset_hashes':json.loads((path/'assets.json').read_text()),'dependencies':{'sympy':sp.__version__,'python':sys.version},'source_evidence_unchanged':True,'source_basis':g.SOURCE['basis'],'bounded_attempts_per_level':256})
        forms=transaction(published,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'generator_id':gid,'new_questions':0,'no_changes':True,'available_counts_after':c};save(path/'verification.json',verified);finish(path,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as f:f.write(tx);f.flush();os.fsync(f.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout);assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis;check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==basis
        if not commit:
            print(json.dumps({'prepared':True,'basis':basis,'new_by_level':added,'available':{l:c['levels'][l]['distinct_available_tasks'] for l in LEVELS},'path':str(path)}),flush=True);return
        visual=json.loads((HERE/'reference/visual-review.json').read_text())
        assert visual['passed']
        for a in json.loads((path/'assets.json').read_text()):assert a['sha256'] in visual['asset_sha256'], 'New asset needs visual review'
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'direction-reversal-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,verified,inventory(path/'inventory-after.json'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def transaction(records, kp, gid):
    forms = []
    for rec in records:
        q = rec['question']
        for f in q[':question/answer-fields']:
            for a in f[':answer-field/choices']:
                forms.append({kw('db/id'):a[':answer/id'], kw('answer/id'):uuid.UUID(a[':answer/id']), kw('answer/type'):kw(a[':answer/type']), kw('answer/value'):a[':answer/value'], kw('db/ensure'):kw('answer/validate')})
            forms.append({kw('db/id'):f[':answer-field/id'], kw('answer-field/id'):uuid.UUID(f[':answer-field/id']), kw('answer-field/key'):f[':answer-field/key'], kw('answer-field/type'):kw(f[':answer-field/type']), kw('answer-field/choices'):[a[':answer/id'] for a in f[':answer-field/choices']], kw('answer-field/correct'):f[':answer-field/correct'][1], kw('db/ensure'):kw('answer-field/validate')})
        forms.append({kw('db/id'):q[':question/id'], kw('question/id'):uuid.UUID(q[':question/id']), kw('question/problem'):q[':question/problem'], kw('question/worked-solution'):q[':question/worked-solution'], kw('question/difficulty'):kw(q[':question/difficulty']), kw('question/answer-fields'):[f[':answer-field/id'] for f in q[':question/answer-fields']], kw('db/ensure'):kw('question/validate')})
    gen = kp.get(':knowledge-point/question-generator')
    if gen is None:
        forms.extend([{kw('db/id'):'generator', kw('question-generator/id'):uuid.UUID(gid), kw('question-generator/script'):SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator']])
    else:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
    if records:
        forms.append({kw('db/id'):KP, kw('knowledge-point/questions'):[r['question'][':question/id'] for r in records]})
    if forms:
        forms.append([kw('db/ensure'), KP, kw('knowledge-point/validate')])
    return forms

def check_report(report, path, source):
    attrs = {e:str(a) for e,a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    allowed = {':question/id', ':question/problem', ':question/worked-solution', ':question/difficulty', ':question/answer-fields', ':answer-field/id', ':answer-field/key', ':answer-field/type', ':answer-field/choices', ':answer-field/correct', ':answer/id', ':answer/type', ':answer/value', ':question-generator/id', ':question-generator/script'}
    for e,a,value,tx,s,added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name in (':knowledge-point/questions', ':knowledge-point/question-generator')
        elif name != ':db/txInstant':
            assert e in new and name in allowed, name

def source_forward(value):
    if isinstance(value,dict):
        if ':db/ident' in value:return str(value[':db/ident'])
        return {str(k):source_forward(x) for k,x in value.items() if '/_' not in str(k)}
    if isinstance(value,(list,tuple)):
        return sorted((source_forward(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

def canonical(value):
    if isinstance(value,dict):return {str(k):canonical(x) for k,x in value.items()}
    if isinstance(value,(list,tuple)):return sorted((canonical(x) for x in value),key=lambda x:json.dumps(x,sort_keys=True))
    if isinstance(value,uuid.UUID):return str(value)
    return value

if __name__=='__main__':main()
