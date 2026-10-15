"""Additive, locked publication of this KP only through the existing EDB integration."""
import copy, fcntl, hashlib, importlib.util, json, os, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps,loads,kw
from inventory_jobs import save
from serve_graph_explorer import database_environment
spec=importlib.util.spec_from_file_location('validation',HERE/'validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);g=v.g
KP=g.KP_ID
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE=':application/ca-engine'
SCRIPT=str(HERE.with_suffix('.py').relative_to(ROOT))
JOB=ROOT/'.local/learning/inventory/math'/LEARNER/'7da4ef3de4d6b65435fbc288094ba4a2a771c65b310b350c9b08c741b1926117'
OUT=HERE/'reference/replenishment';OUT.mkdir(parents=True,exist_ok=True)
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE=ROOT/'.local/graph-explorer/learning-c9743ced043e1fd7'
sys.path.insert(0,str(HERE))
from db_support import PATTERN
QUERY='[:find (pull ?kp '+PATTERN+') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=database_environment('math'), capture_output=True, text=True, check=True, timeout=90)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read_kp(path, basis):
    return DB.query(QUERY, [[KP]], path, 'kp', basis)[0][0]

def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in (':question/id', ':question/problem', ':question/worked-solution')}
    result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        result[':question/answer-fields'].append({':answer-field/id':str(f[':answer-field/id']), ':answer-field/key':f[':answer-field/key'], ':answer-field/type':str(f[':answer-field/type'][':db/ident']), ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])], ':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']), ':answer/type':str(a[':answer/type'][':db/ident']), ':answer/value':a[':answer/value']} for a in f[':answer-field/choices']], key=lambda a:a[':answer/value'])})
    return result

USAGE_QUERY = """[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

def available_counts(path,kp,basis,generated=()):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    known={q[':db/id'] for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions'] if q.get(':question/math-academy-id') in {s for ids in g.SOURCE_IDS.values() for s in ids}}
    accepted={level:[] for level in g.TEMPLATES};excluded=[]
    authored={r['question'][':question/id']:r for r in generated}
    for folder in OUT.glob('basis-*'):
        if (folder/'verification.json').exists() and (folder/'generated.json').exists():
            authored.update({r['question'][':question/id']:r for r in json.loads((folder/'generated.json').read_text())})
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        reason=None
        if q[':db/id'] in unavailable:reason='Shown or reserved, including retained history'
        elif level not in accepted:reason='Unrated or unsupported band'
        elif not q.get(':question/worked-solution'):reason='Missing worked solution'
        elif q[':db/id'] not in known:
            r=authored.get(str(q[':question/id']))
            if r is None or normalize(q)!=ordered(r['question']):reason='No validated generated record'
            else:v.check(r)
        if reason:excluded.append({'db_id':q[':db/id'],'reason':reason})
        else:accepted[level].append(q)
    result={'basis':basis,'levels':{level:{'distinct_available_tasks':len({fingerprint(q) for q in rows}),'question_ids':[str(q[':question/id']) for q in rows]} for level,rows in accepted.items()},'excluded':excluded,'unavailable_ids':sorted(unavailable)}
    save(path/'available-counts.json',result)
    return result

def finish(path,gid,verified,inv):
    counts=available_counts(path/'after-counts',read_kp(path/'count-readback',inv['basis']),inv['basis'])
    shortages=[{'difficulty':level,'missing':max(0,5-c['distinct_available_tasks'])} for level,c in counts['levels'].items() if c['distinct_available_tasks']<5]
    exceptions=json.loads((HERE/'capabilities.json').read_text())['exceptions']
    evidence=[p for p in (path/'verification.json',path/'commit-intent.json',path/'commit.edn',path/'preview.edn',path/'inventory-after.json',path/'preparation.json',path/'transaction.edn',path/'native-report.json',HERE/'source-components.json',HERE/'validation.json',HERE/'source-replay.json',HERE/'native-grading.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'review.md',HERE/'capabilities.json') if p.exists()]
    result={'outcome':'finite-limit' if shortages else 'generated','knowledgePoint':KP,'topic':17592186048863,'database':'math','lineage':LINEAGE,'generator_path':SCRIPT,'generator_id':gid,'verified_commit_basis':verified['basis_after'],'commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_questions_by_level':verified.get('by_level',{}),'supported_levels':['easy','moderate'],'unsupported_levels':['hard'],'unsupported_levels_filled':False,'capability_exceptions':exceptions,'unsupported_shortages':[{'difficulty':'hard','nominal_reserve':5,'available_validated':0,'filled':False,'reason':'No source-backed hard template'}],'available_after':counts,'inventory_recheck_basis':inv['basis'],'remaining_supported_shortages':shortages,'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'source_questions_and_learner_history_preserved':True,'evidence':[str(p.relative_to(ROOT)) for p in evidence]}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','new_questions_by_level','remaining_supported_shortages','remaining_jobs')}),flush=True)

def main():
    validation=json.loads((HERE/'validation.json').read_text());assert validation['passed']
    assert all(sha(ROOT/p)==digest for p,digest in validation['hashes'].items())
    preview=preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        # Reconcile complete saved requests before making any new content decisions.
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent=json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage']==LINEAGE and intent['source']==SOURCE and intent['transaction_sha256']==sha(path/'transaction.edn')
                assert intent['exact_edn']==(path/'transaction.edn').read_text()
                assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                report=DB._commit(intent,path/'transaction.edn',path)
                verified=verify(path,intent,report)
                finish(path,intent['generator_id'],verified,inventory(path/'inventory-after.json'))
                return
        inv=inventory(OUT/'inventory-before.json');b=inv['basis'];assert DB.basis()==b
        path=OUT/('basis-'+str(b));path.mkdir(exist_ok=True)
        kp=read_kp(path,b);assert str(kp[':knowledge-point/id'])==g.KP_UUID
        (path/'before.edn').write_text(dumps(kp)+'\n')
        evidence=loads((HERE/'source.edn').read_text())
        expected={q[':db/id']:q for q in evidence[':knowledge-point/questions']};current={q[':db/id']:q for q in kp[':knowledge-point/questions']}
        assert all(current[e]==q for e,q in expected.items()),'Source evidence changed; reclassify'
        assert kp[':knowledge-point/canonical-example']==evidence[':knowledge-point/canonical-example']
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',b);assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator');gid=str(gen[':question-generator/id']) if gen else g.GENERATOR_UUID
        counts=available_counts(path,kp,b)
        jobs={j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint']==KP}
        needed={level:max(jobs.get(level,{}).get('missing',0),5-counts['levels'][level]['distinct_available_tasks'],0) for level in g.TEMPLATES}
        used={fingerprint(q) for q in kp[':knowledge-point/questions']}
        # Canonical prompt is truncated, so also compare its complete solution's first
        # three substituted matrices against each supported expression profile.
        canonical=kp.get(':knowledge-point/canonical-example',{})
        if canonical:
            mats=[[[int(value) for value in row] for row in matrix.tolist()] for matrix in v.matrices(canonical.get(':question/worked-solution',''))[:3]]
            if len(mats)==3:
                for t in g.EXPR:used.add(g.task_fingerprint(t,mats))
        supplied_path=JOB.with_suffix('.generated');supplied=json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances=supplied.get('instances',[])
        if isinstance(instances,dict):instances=[instances]
        assert isinstance(instances,list)
        for rec in instances:v.check(rec)
        save(path/'supplied-status.json',{'exists':supplied_path.exists(),'instances_validated':len(instances),'generator_error':supplied.get('generatorError')})
        records=[];selected={level:0 for level in needed};local=[];commands=[]
        # Execute the public CLI after the locked current inventory read, retaining
        # exact invocation and stdout. Oversampling permits content deduplication.
        for index,(level,n) in enumerate(needed.items()):
            if not n:continue
            command=[sys.executable,str(HERE.with_suffix('.py')),'--difficulty',level,'--count',str(max(10,n*3)),'--seed',str(int(JOB.name[:8],16)+index*100),'--format','json']
            r=subprocess.run(command,capture_output=True,text=True,check=True,timeout=120)
            (path/(level+'-cli-output.json')).write_text(r.stdout)
            commands.append({'command':command,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()})
            local.extend(json.loads(r.stdout))
        save(path/'generator-commands.json',commands)
        for rec in instances+local:
            v.check(rec);level=rec['question'][':question/difficulty'].split('/')[-1];fp=fingerprint(rec['question'])
            assert rec['knowledge_point']['db_id']==KP and fp==rec['generation']['mathematical_fingerprint']
            if selected[level]<needed[level] and fp not in used:
                records.append(copy.deepcopy(rec));used.add(fp);selected[level]+=1
        finite_remaining={level:needed[level]-selected[level] for level in needed}
        save(path/'local-preview.json',local);save(path/'generated.json',records)
        ids=[uuid.UUID(r['question'][':question/id']) for r in records]
        collisions=DB.query('[:find ?q ?id :in $ [?id ...] :where [?q :question/id ?id]]',[ids],path,'generated-identities',b) if ids else []
        assert not collisions,'Identity already exists; reconcile'
        registered=DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-identity',b)
        assert not registered or (len(registered)==1 and registered[0][0][':question-generator/script']==SCRIPT)
        save(path/'native-input.json',[v.native(rec['question'][':question/id'],rec) for rec in instances+local+records])
        subprocess.run([str(HERE/'check-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
        save(path/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_id':gid,'available_counts':counts,'missing_by_level':needed,'selected_by_level':selected,'finite_remaining':finite_remaining,'new_questions':len(records),'source_evidence_unchanged':True,'asset_hashes':[],'inventory_count_evidence':{level:jobs.get(level,{'missing':0}) for level in needed},'distinctness':'Parsed operand matrices and signed operation; seeds, labels, identities and option order excluded','generator_commands':'generator-commands.json','unsupported_levels_filled':False})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_before':b,'basis_after':b,'new_questions':0,'no_changes':True,'generator_registration_verified':True}
            save(path/'verification.json',verified);finish(path,gid,verified,inv);return
        txpath=path/'transaction.edn';tx=dumps(forms)+'\n'
        with txpath.open('w') as stream:stream.write(tx);stream.flush();os.fsync(stream.fileno())
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,check=True,timeout=90)
        (path/'preview.edn').write_text(r.stdout);pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,path/'preview-check',source[0][0]);assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'three-matrix-replenish-17592186100991-'+str(b)+'-'+sha(txpath),'transaction_sha256':sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[rec['question'][':question/id'] for rec in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json',intent)
        report=DB._commit(intent,txpath,path);verified=verify(path,intent,report)
        finish(path,gid,verified,inventory(path/'inventory-after.json'))

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a:a[':answer/value'])
    return q

def fingerprint(q):
    return g.fingerprint(q)

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
        assert fingerprint(q) == rec['generation']['mathematical_fingerprint']
        v.check(rec)
    assert not transaction([], kp, intent['generator_id'])
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'by_level':{level:sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records) for level in ('easy','moderate')}, 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

if __name__=='__main__':main()
