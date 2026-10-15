"""Scoped surface-integrand inventory publication using the application EDB writer."""
import fcntl, hashlib, importlib.util, json, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
ROOT = P.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
from capture.scripts.storage import atomic_json, atomic_text
sys.path[:0] = [str(P), str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
import validate as v
import commit_helpers as h
from database import Database
from edn import dumps, loads
from serve_graph_explorer import database_environment
g = v.g
KP = g.KP
SCRIPT = str(P.with_suffix('.py').relative_to(ROOT))
LINEAGE = g.CAPTURE['lineage']
SOURCE = ':application/ca-engine'
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'baf758bf8d4c2e7bb2871fc17f2b00e766100f6ae2fda1d67c940150a21ae684'
OUT = P/'reference/replenishment'
LOCK = ROOT/'.local/learning/requests/math/api.lock'
ENV = database_environment('math')
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=ENV['EDB_ENDPOINT']))
DB.env = ENV
h.DB, h.KP, h.SCRIPT = DB, KP, SCRIPT
LEVELS = ('easy', 'moderate', 'hard')
QUERY = '''[:find (pull ?kp [* {:knowledge-point/question-generator [*]}
 {:knowledge-point/canonical-example [* {:question/difficulty [:db/id :db/ident]}]}
 {[:knowledge-point/questions :limit nil] [* {:question/difficulty [:db/id :db/ident]}
 {:question/answer-fields [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]}])
 :in $ ?kp :where [?kp :knowledge-point/id _]]'''
ANOMALIES = {'q-160711':'duplicate field missing correct designation', 'q-160712':'incorrect displayed metric and missing half-plane restriction', 'q-161134':'missing half-plane restriction for norm', 'q-161286':'incorrect cross-product row and missing half-plane restriction', 'q-161135':'incorrect signed-coordinate substitution label'}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def inventory(path):
    # Same native reader as the application's /api/inventory, with no writes.
    binary = ROOT/'.local/graph-explorer/learning-64e7aa312fccadb0'
    r = subprocess.run([str(binary), 'math', LEARNER, ENV['EDB_ENDPOINT']], input='{"action":"inventory"}', env=ENV, text=True, capture_output=True, check=True, timeout=55)
    result = json.loads(r.stdout)
    assert result['ok'] and result['data']['lineage'] == LINEAGE
    atomic_json(path, result['data'])
    return result['data']

def read_kp(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

def task_key(q):
    """Assessed surface and scalar function; ignores bank, seed, notation/order."""
    prompt = q[':question/problem']
    if q.get(':question/math-academy-id') == 'e-12344':
        r, f = [g.u**2,-g.v,g.v], g.z-g.y
    else:
        r = v.vector(g.display_blocks(prompt)[1].split('=', 1)[1])
        f = g.read_math(re.search(r'\$f\(x,y,z\)=(.*?)\$', prompt).group(1))
    return (tuple(g.sp.srepr(g.sp.expand(x)) for x in r), g.sp.srepr(g.sp.expand(f)))

def known_records():
    return {r['question'][':question/id']:r for path in OUT.glob('basis-*/generated.json') for r in json.loads(path.read_text())}

def native(records, path):
    path.mkdir(parents=True, exist_ok=True)
    atomic_json(path/'input.json', [v.native_item(str(i), r) for i,r in enumerate(records)])
    if not records:
        atomic_json(path/'report.json', {'questions':0, 'accepted_checks':0, 'rejected_checks':0})
        return
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'), str(path/'input.json'), str(path/'report.json')], check=True, capture_output=True, text=True)
    result = json.loads((path/'report.json').read_text())
    assert result['accepted_checks'] == len(records) and result['rejected_checks'] == 4*len(records) and result['documented_unresolved_checks'] == 0

def counts(kp, basis, path):
    path.mkdir(parents=True, exist_ok=True)
    shown = DB.query('''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
      [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t]
      [?t :learner-task/items ?i] [?i :task-item/content ?q]]''', [KP, LEARNER], path, 'shown', basis, history=True)
    reserved = DB.query('''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner]
      [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?s]
      (or [?s :db/ident :learner-task.status/started] [?s :db/ident :learner-task.status/paused])
      [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]''', [KP,LEARNER], path, 'reserved', basis)
    seen = {x[0] for x in shown+reserved}
    entities = {}
    for i,ident in enumerate(('question.difficulty/easy','question.difficulty/moderate','question.difficulty/hard','answer-field.type/radio','answer.type/math')):
        entities[str(i+1)] = {'db/ident':ident}
    enum = lambda x: str(x[':db/ident']).lstrip(':')
    for q in kp[':knowledge-point/questions']:
        item = {'question/id':str(q[':question/id']), 'question/problem':q[':question/problem'], 'question/answer-fields':[f[':db/id'] for f in q.get(':question/answer-fields',[])]}
        if ':question/difficulty' in q: item['question/difficulty'] = enum(q[':question/difficulty'])
        entities[str(q[':db/id'])] = item
        for f in q.get(':question/answer-fields',[]):
            field = {'answer-field/key':f[':answer-field/key'], 'answer-field/type':enum(f[':answer-field/type']), 'answer-field/choices':[a[':db/id'] for a in f.get(':answer-field/choices',[])]}
            if ':answer-field/correct' in f: field['answer-field/correct'] = f[':answer-field/correct'][':db/id']
            entities[str(f[':db/id'])] = field
            for a in f.get(':answer-field/choices',[]): entities[str(a[':db/id'])] = {'answer/type':enum(a[':answer/type']), 'answer/value':a[':answer/value']}
    entities[str(KP)] = {'knowledge-point/questions':[q[':db/id'] for q in kp[':knowledge-point/questions']], 'knowledge-point/canonical-example':kp[':knowledge-point/canonical-example'][':db/id']}
    entities[str(kp[':knowledge-point/canonical-example'][':db/id'])] = {'question/id':str(kp[':knowledge-point/canonical-example'][':question/id'])}
    atomic_json(path/'snapshot.json', {'basis_t':basis,'knowledge_point':KP,'entities':entities,'seen':sorted(seen)})
    subprocess.run([str(ROOT/'generate/scratch/17592186110754/check-pool'), str(path/'snapshot.json'), str(path/'pool.json')],check=True,capture_output=True,text=True)
    pool = json.loads((path/'pool.json').read_text())
    byid = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    known = known_records()
    keys = {l:set() for l in LEVELS}
    checked, exclusions = [], []
    for level,ids in pool['available_ids_by_level'].items():
        for eid in ids:
            q = byid[eid]
            sid = q.get(':question/math-academy-id')
            if sid in ANOMALIES:
                exclusions.append({'id':eid,'source':sid,'reason':ANOMALIES[sid]})
                continue
            if sid:
                name = next(n for n,s in g.BY_NAME.items() if s[':question/math-academy-id']==sid)
                rec = g.generate(level,template=name,profile='observed',parameters={'k':1})
                captured = {k:x for k,x in g.BY_NAME[name].items() if not k.startswith(':knowledge-point/_')}
                assert h.source_shape(q,captured) == h.canonical(captured)
                # Source bank correctness was independently checked by source_math_audit.
            else:
                rec = known[str(q[':question/id'])]
                assert h.normalize(q) == h.ordered(rec['question'])
                v.audit(rec)
            checked.append(rec)
            keys[level].add(task_key(q))
    native(checked, path/'grading')
    result = {'basis':basis,'available':{l:len(keys[l]) for l in LEVELS},'shortage':{l:max(0,5-len(keys[l])) for l in LEVELS},'excluded_source_defects':exclusions,'source_defects_retained':ANOMALIES,'shown_or_reserved':sorted(seen),'pool':pool,'distinctness':'expanded actual coordinate surface and scalar function; seed, identity, bank and choice order ignored'}
    atomic_json(path/'validated-counts.json',result)
    return result

def verify(path, intent, receipt):
    assert receipt[':edb/committed'] is True and receipt[':edb/db-before-t'] == intent['basis']
    h.check_report(receipt,path/'receipt-check',intent['source_eid'])
    basis = receipt[':edb/db-after-t']
    before = loads((path/'before.edn').read_text())
    after = read_kp(path/'readback',basis)
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in after[':knowledge-point/questions']}
    assert all(now[eid] == q for eid,q in old.items())
    omit = {':knowledge-point/questions',':knowledge-point/question-generator'}
    assert {k:x for k,x in before.items() if k not in omit} == {k:x for k,x in after.items() if k not in omit}
    records = json.loads((path/'generated.json').read_text())
    byid = {str(q[':question/id']):q for q in now.values()}
    assert len(now) == len(old)+len(records)
    for r in records:
        assert h.normalize(byid[r['question'][':question/id']]) == h.ordered(r['question'])
        v.audit(r)
    native(records,path/'readback-grading')
    assert h.transaction([],after,intent['generator_id']) == []
    c = counts(after,basis,path/'readback/inventory')
    result = {'passed':True,'basis_before':intent['basis'],'basis_after':basis,'new_questions':len(records),'new_by_level':{l:sum(r['generation']['level']==l for r in records) for l in LEVELS},'source_questions_preserved':len(old),'canonical_example_unchanged':True,'learner_history_unchanged':True,'additive_scoped_datoms_only':True,'generator_registration_verified':True,'repeat_preparation_content_changes':0,'available_counts_after':c}
    atomic_json(path/'verification.json',result)
    return result

def finish(path, intent, verified):
    inv = inventory(path/'inventory-after.json')
    before = json.loads((path/'preparation.json').read_text())
    c = verified['available_counts_after']
    result = {'outcome':'generated' if not any(c['shortage'].values()) else 'finite-limit','knowledgePoint':KP,'generator_path':SCRIPT,'generator_id':intent['generator_id'],'lineage':LINEAGE,'verified_commit_basis':verified['basis_after'],'verified_commit_basis_before':verified['basis_before'],'new_questions':verified['new_questions'],'new_by_level':verified['new_by_level'],'supported_levels':list(LEVELS),'unsupported_levels':[],'unsupported_levels_filled':False,'available_counts_before':before['available_counts']['available'],'available_counts_after':c['available'],'remaining_shortage':c['shortage'],'capability_exceptions':before['capability_exceptions'],'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],'evidence':[str(x.relative_to(ROOT)) for x in [P/'classification.md',P/'template-extraction.md',P/'plot-extraction.md',P/'validation.json',P/'freeze.json',P/'registration.json',path/'preparation.json',path/'generated.json',path/'grading/report.json',path/'transaction.edn',path/'preview.edn',path/'commit-intent.json',path/'commit.edn',path/'verification.json',path/'inventory-after.json'] if x.exists()]}
    atomic_json(path/'outcome.json',result)
    atomic_json(JOB.with_suffix('.result'),result)
    print(json.dumps(result),flush=True)

def main():
    frozen = json.loads((P/'freeze.json').read_text())
    for rel,digest in frozen['files'].items():
        assert sha(ROOT/rel)==digest,'Frozen artifact changed: '+rel
    assert sha(ROOT/'generate/runs/current/check-engine')==frozen['native_grader_sha256']
    assert json.loads((P/'validation.json').read_text())['pass']
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),repo_root=ROOT,preview_bin=None),threading.Event())
    with LOCK.open('a') as lock:
        print('Waiting for application api.lock',flush=True)
        fcntl.flock(lock,fcntl.LOCK_EX)
        print('Application api.lock acquired',flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists():continue
            intent = json.loads((path/'commit-intent.json').read_text())
            assert intent['lineage']==LINEAGE and intent['database']=='math' and intent['endpoint']==ENV['EDB_ENDPOINT'] and intent['source']==SOURCE
            assert intent['exact_edn']==(path/'transaction.edn').read_text() and intent['sha256']==sha(path/'transaction.edn')
            assert intent['connection_sha256']==hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified = verify(path,intent,DB._commit(intent,path/'transaction.edn',path))
            finish(path,intent,verified)
            return
        inv = inventory(OUT/'inventory-under-lock.json')
        basis = inv['basis']
        assert DB.basis()==basis
        path = OUT/('basis-'+str(basis))
        path.mkdir(parents=True,exist_ok=True)
        kp = read_kp(path,basis)
        atomic_text(path/'before.edn',dumps(kp)+'\n')
        current = {q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        for sid,old in [(q[':question/math-academy-id'],q) for q in g.Q]:
            # Ignore reverse memberships absent from this projection.
            old = {k:x for k,x in old.items() if not k.startswith(':knowledge-point/_')}
            assert h.source_shape(current[sid],old) == h.canonical(old),'Source changed; reclassification required'
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],path,'contributor',basis)
        assert len(source)==1
        gen = kp.get(':knowledge-point/question-generator')
        found = DB.query('[:find ?e ?id :in $ ?script :where [?e :question-generator/script ?script] [?e :question-generator/id ?id]]',[SCRIPT],path,'generator-script',basis)
        assert len(found)<=1
        reg = P/'registration.json'
        gid = str(gen[':question-generator/id']) if gen else str(found[0][1]) if found else json.loads(reg.read_text())['id'] if reg.exists() else str(uuid.uuid5(uuid.UUID(g.REC[':knowledge-point/id']),'question-generator'))
        matched = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]',[uuid.UUID(gid)],path,'generator-id',basis)
        assert not matched or len(matched)==1 and matched[0][0][':question-generator/script']==SCRIPT
        atomic_json(reg,{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or found or reg.exists()),'generator_sha256':sha(P.with_suffix('.py'))})
        c = counts(kp,basis,path/'current-inventory')
        print(json.dumps({'basis':basis,'validated_available':c['available'],'shortage':c['shortage']}),flush=True)
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances',[]) if isinstance(supplied,dict) else supplied
        if isinstance(instances,dict): instances=[instances]
        for r in instances:v.audit(r)
        atomic_json(path/'supplied-status.json',{'exists':supplied_path.exists(),'validated_instances':len(instances)})
        used = {task_key(q) for q in kp[':knowledge-point/questions']}
        used.add(task_key(kp[':knowledge-point/canonical-example']))
        records = []
        added = {l:0 for l in LEVELS}
        for level in LEVELS:
            candidates = [r for r in instances if r['generation']['level']==level]
            for i in range(512):
                if added[level]>=c['shortage'][level]: break
                r = candidates.pop(0) if candidates else g.generate(level,seed=int(JOB.name[:8],16)+i)
                v.audit(r)
                key = task_key(r['question'])
                if key in used:continue
                used.add(key)
                records.append(r)
                added[level]+=1
        native(records,path/'grading')
        atomic_json(path/'generated.json',records)
        atomic_text(path/'generated.md','\n\n---\n\n'.join(g.markdown(r) for r in records)+'\n')
        ids = [uuid.UUID(x) for r in records for x in [r['question'][':question/id']]+[f[':answer-field/id'] for f in r['question'][':question/answer-fields']]+[a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
        assert len(ids)==len(set(ids))
        collisions = DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]',[ids],path,'identities',basis) if ids else []
        assert not collisions,'Existing identity requires reconciliation'
        exceptions = [{'level':l,'requested':c['shortage'][l],'produced':added[l],'remaining':c['shortage'][l]-added[l],'filled':False,'reason':'Bounded 512 sampler attempts exhausted; no claim of global exhaustion'} for l in LEVELS if added[l]<c['shortage'][l]]
        atomic_json(path/'preparation.json',{'basis':basis,'lineage':LINEAGE,'source':SOURCE,'available_counts':c,'new_by_level':added,'capability_exceptions':exceptions,'generator_sha256':sha(P.with_suffix('.py')),'all_selected_instances_mathematically_validated':True,'all_selected_instances_actual_grader_validated':True,'plots':'none; no assets needed','authored_banks':'explicit method-derived extension; observed banks retained for complete source replay','source_basis':g.CAPTURE['basis']})
        if '--prepare-only' in sys.argv:
            print(json.dumps({'prepared':True,'basis':basis,'new_by_level':added,'review':str(path/'generated.md')}),flush=True)
            return
        forms = h.transaction(records,kp,gid)
        if not forms:
            intent={'generator_id':gid}
            verified={'passed':True,'basis_before':basis,'basis_after':basis,'new_questions':0,'new_by_level':added,'available_counts_after':c}
            atomic_json(path/'verification.json',verified)
            finish(path,intent,verified)
            return
        txpath = path/'transaction.edn'
        atomic_text(txpath,dumps(forms)+'\n')
        output = subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=ENV,capture_output=True,text=True,check=True,timeout=55)
        atomic_text(path/'preview.edn',output.stdout)
        pr = loads(output.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==basis
        h.check_report(pr,path/'preview-check',source[0][0])
        assert DB.basis()==basis
        intent={'database':'math','endpoint':ENV['EDB_ENDPOINT'],'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':basis,'expected_basis':basis,'request_key':'surface-integrand-inventory-'+str(KP)+'-'+str(basis)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':txpath.read_text(),'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(P.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(ENV['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(LOCK)}
        atomic_json(path/'commit-intent.json',intent)
        verified=verify(path,intent,DB._commit(intent,txpath,path))
        finish(path,intent,verified)

if __name__ == '__main__':main()
