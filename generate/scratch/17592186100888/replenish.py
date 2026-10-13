"""Scoped additive replenishment with retained requests and exact-basis readback."""
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
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate-current.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP['db_id']
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '4f5829fdc2da79db86c39d3b23d5985b08646371a50696f26088c7efc1125fc1'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = build_learning(ROOT.parent / 'EDB')
QUERY = (HERE / 'reference/source-query.edn').read_text()

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

def validate_instance(rec):
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    v.displayed(rec)

USAGE_QUERY = """[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

def available_counts(path,kp,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    # Retained historical presentations and reservations stay excluded as well.
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    available={level:[] for level in ('moderate',)}
    excluded=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        reason=None
        if q[':db/id'] in unavailable:reason='Shown or reserved, including retained history'
        elif q.get(':knowledge-point/_canonical-example'):reason='Canonical example'
        elif level not in available:reason='Unrated or outside requested moderate inventory scope'
        elif not q.get(':question/worked-solution') or not q.get(':question/answer-fields'):reason='Incomplete solution or fields'
        else:
            try:source_or_generated_check(q)
            except (AssertionError,ValueError,KeyError,TypeError) as error:reason='Mathematical/gradation validation exclusion: '+str(error)
        if reason:excluded.append({'db_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'reason':reason})
        else:available[level].append(q)
    counts={'basis':basis,'levels':{level:{'rated_gradable_unseen_unreserved':len(rows),
        'distinct_available_tasks':len({fingerprint(q) for q in rows}),
        'available_question_ids':[str(q[':question/id']) for q in rows],
        'available_task_fingerprints':sorted({fingerprint(q) for q in rows})} for level,rows in available.items()},
        'excluded_shown_or_reserved':sorted(unavailable),'excluded_questions':excluded}
    save(path/'available-counts.json',counts)
    return counts

def fingerprint(q):
    # Canonicalize actual mathematical task, independent of seed, UUID and fields.
    if q.get(':question/math-academy-id') == 'e-525':
        f,claim,rhs=1/g.x,-1/g.x**2,-g.y/g.x
    else:
        p=q[':question/problem']
        rhs=v.v.parse(__import__('re').search(r'\$\$\n\{y\}\^\{′\}=(.*?)\n\$\$',p,__import__('re').S)[1].split(r',\,')[0])
        f=v.v.parse(__import__('re').search(r'Let \$f\(x\)=(.*?)\$',p)[1].rstrip('.,'))
        claim=v.v.parse(__import__('re').search(r'- (?:\*\*I\.\*\* )?\$\{f\}\^\{′\}\(x\)=(.*?)\$',p)[1].rstrip('.'))
    logs=sorted(str(z.args[0]) for z in f.atoms(g.sp.log))
    domain=('positive log arguments',logs) if logs else ('x != 0' if g.sp.denom(f).has(g.x) or g.sp.denom(rhs).has(g.x) else 'all real x')
    return hashlib.sha256(json.dumps([g.sp.srepr(g.sp.simplify(z)) for z in (f,claim,rhs)]+[domain],sort_keys=True).encode()).hexdigest()

def canonical(value):
    if isinstance(value, dict):
        return {str(k):canonical(x) for k,x in value.items() if str(k) != ':db/id' and not str(k).startswith(':knowledge-point/_')}
    if isinstance(value, (list, tuple)):
        return sorted((canonical(x) for x in value), key=lambda x:json.dumps(x, sort_keys=True))
    if isinstance(value, uuid.UUID): return str(value)
    return value

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
        assert str(gen[':question-generator/id']) == gid
        if gen.get(':question-generator/script') != SCRIPT:
            forms.append({kw('db/id'):gen[':db/id'],kw('question-generator/script'):SCRIPT})
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

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path/'receipt-check', intent['source_eid'])
    kp = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items())
    assert {k:v for k,v in before.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')} == {k:v for k,v in kp.items() if k not in (':knowledge-point/questions', ':knowledge-point/question-generator')}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q) == ordered(rec['question'])
        assert fingerprint(q) == fingerprint(rec['question'])
        validate_instance(rec)
    assert not transaction([], kp, intent['generator_id'])
    counts=available_counts(path/'readback',kp,report[':edb/db-after-t'])
    for level in ('moderate',):
        added=sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records)
        previous=json.loads((path/'preparation.json').read_text())['available_counts']['levels'][level]['distinct_available_tasks']
        assert counts['levels'][level]['distinct_available_tasks']>=min(5,previous+added)
    result = {'available_counts_after':counts,'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result


CASES={c['source_id']:c for c in json.loads((HERE/'source-cases.json').read_text())}
def source_or_generated_check(q):
    if q.get(':question/math-academy-id') in CASES:
        c=CASES[q[':question/math-academy-id']]
        r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])
        assert normalize(q)==ordered({**r['question'],':question/id':str(q[':question/id']),':question/answer-fields':[
            {**f,':answer-field/id':str(sf[':answer-field/id']),':answer-field/choices':[
                {**a,':answer/id':str(next(z[':answer/id'] for z in sf[':answer-field/choices'] if z[':answer/value']==a[':answer/value']))} for a in f[':answer-field/choices']],
             ':answer-field/correct':[':answer/id',str(sf[':answer-field/correct'][':answer/id'])]}
             for f in r['question'][':question/answer-fields'] for sf in q[':question/answer-fields'] if sf[':answer-field/key']==f[':answer-field/key']]})
        v.displayed(r)
    else:
        # Reconstruct reproducibility from exact bounded tasks, not UUID claims.
        r=next((r for r in json.loads((HERE/'reference/moderate-domain.json').read_text()) if normalize(q)==ordered(r['question'])),None)
        assert r is not None,'Unknown question; classify before counting'
        validate_instance(r)

def finish(path,gid,verified,inv):
    prep=json.loads((path/'preparation.json').read_text())
    counts=verified['available_counts_after']
    shortage=max(0,5-counts['levels']['moderate']['distinct_available_tasks'])
    result={'outcome':'finite-limit' if shortage else 'generated','knowledgePoint':KP,'difficulty':'moderate',
      'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],
      'new_questions':verified['new_questions'],'available_moderate_after':counts['levels']['moderate']['distinct_available_tasks'],
      'shortage_remaining':shortage,'unsupported_levels_filled':False,'evidence':[
      str((HERE/'validation-current.json').relative_to(ROOT)),str((path/'preparation.json').relative_to(ROOT)),
      str((path/'commit-intent.json').relative_to(ROOT)),str((path/'commit.edn').relative_to(ROOT)),
      str((path/'verification.json').relative_to(ROOT)),str((path/'inventory-after.json').relative_to(ROOT))],
      'capability_bounds':{'moderate_distinct_tasks':15,'moderate_error_recipe':'Authored a-n assertion reproduces the single observed scalar; historical diagnosis underdetermined','hard':'Authored design with no rated source evidence; this job neither generates hard content nor claims its inventory filled'}}
    save(JOB.with_suffix('.result'),result)
    print(json.dumps(result,indent=2))

def main():
    validation=json.loads((HERE/'validation-current.json').read_text())
    assert validation['passed'] and validation['generator_sha256']==sha(HERE.with_suffix('.py'))
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    # The same application lock protects refreshed reads, original request,
    # submission, exact-basis readback, and inventory verification.
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE
                assert intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'));return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP['id']
        (path/'before.edn').write_text(dumps(kp)+'\n')
        initial=loads((HERE/'reference/initial/kp.edn').read_text())[0][0]
        for q in initial[':knowledge-point/questions']:
            current=next(z for z in kp[':knowledge-point/questions'] if z[':question/id']==q[':question/id'])
            assert canonical(current)==canonical(q),'Source changed; return to classification'
        assert canonical(initial[':knowledge-point/canonical-example'])==canonical(kp[':knowledge-point/canonical-example'])
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        counts=available_counts(path,kp,b)
        needed=max(0,5-counts['levels']['moderate']['distinct_available_tasks'])
        used={fingerprint(q) for q in kp[':knowledge-point/questions']};used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[]);assert isinstance(instances,list)
        for r in instances:validate_instance(r)
        # Execute the validated CLI, then bounded enumeration for any collisions.
        local=[]
        if needed:
            run=subprocess.run([str(ROOT/'.venv/bin/python'),str(HERE.with_suffix('.py')),'--difficulty','moderate','--count',str(needed),'--seed',str(int(JOB.name[:8],16)),'--format','json'],capture_output=True,text=True,check=True)
            local=json.loads(run.stdout)
        candidates=instances+local+json.loads((HERE/'reference/moderate-domain.json').read_text())
        records=[]
        for r in candidates:
            validate_instance(r)
            assert r['question'][':question/difficulty']==':question.difficulty/moderate'
            fp=fingerprint(r['question'])
            if len(records)<needed and fp not in used:records.append(r);used.add(fp)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances),'generator_error':supplied.get('generatorError')})
        save(path/'generated.json',records)
        (path/'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records))
        save(path/'native-input.json',[{'label':r['question'][':question/id'],'record':r,'checks':v.checks(r)} for r in records])
        subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        native=json.loads((path/'native-report.json').read_text());assert native['documented_unresolved_checks']==0
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,
          'missing_by_level':{'moderate':needed},'new_questions':len(records),'available_counts':counts,
          'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),
          'source_evidence_unchanged':True,'asset_hashes':[],'source_replays':'validation-current.json',
          'native_grading':'native-report.json','finite_remaining':max(0,needed-len(records)),
          'generator_version':g.CURRENT_VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),
          'supplied_generated_path':str(supplied_path),'application_lock':str(ROOT/'.local/learning/requests/math/api.lock')})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'available_counts_after':counts}
            save(path/'verification.json',verified);finish(path,gid,verified,inventory(path/'inventory-after.json'));return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        prun=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(prun.stdout);pr=loads(prun.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],
          'basis':b,'expected_basis':b,'request_key':'ode-checkbox-inventory-17592186100888-'+str(b)+'-'+sha(txpath),
          'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,
          'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],
          'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),
          'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path)
        verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

if __name__=='__main__':main()
