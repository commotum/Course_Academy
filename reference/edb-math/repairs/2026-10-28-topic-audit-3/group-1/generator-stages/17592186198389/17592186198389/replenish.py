"""Replenish only Cartesian flux setup; serialize with the application writer."""
import copy, fcntl, hashlib, importlib.util, json, os, re, subprocess, sys, threading, uuid
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from serve_graph_explorer import database_environment
from inventory_jobs import save
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database, QUESTION_PULL
from edn import dumps, loads, kw
spec = importlib.util.spec_from_file_location('flux_validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.RAW['lineage']
SOURCE = ':application/ca-engine'
LEVELS = ('easy', 'moderate', 'hard')
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '3a43279257fafd8600d3466b4100c80ff1b56ff03518a8ab7051bdf55f20e6de'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env = database_environment('math')
NATIVE = ROOT / '.local/graph-explorer/learning-1275f16a95dc6372'
POOL = HERE / 'reference/native/check-pool'
QUERY = '[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
exec(compile((HERE / 'replenish_helpers.py').read_text(), str(HERE / 'replenish_helpers.py'), 'exec'))

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(p):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=DB.env, capture_output=True, text=True, check=True, timeout=55)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(p, x['data']); return x['data']

def read(p, b): return DB.query(QUERY, [KP], p, 'kp', b)[0][0]

def fp(q):
    F = v.vectors(q[':question/problem'])[0]
    G = g.parse(re.search(r'defined by \$z=(.*?)\$', q[':question/problem']).group(1))
    return g.digest({'F':[g.sp.srepr(g.sp.expand(e)) for e in F], 'g':g.sp.srepr(g.sp.expand(G)), 'orientation':'upward'})

def validate(r):
    assert r['knowledge_point']['db_id'] == KP
    meta = r['generation']; level = r['question'][':question/difficulty'].split('/')[-1]
    assert level in LEVELS and meta['version'] == g.VERSION
    replay = g.generate(level, meta['seed'], meta['template'], parameters=meta['parameters'], profile=meta['profile'])
    assert ordered(replay['question']) == ordered(r['question']) and replay['generation'] == meta
    v.independent(r)
    assert fp(r['question']) == meta['mathematical_fingerprint']
    return fp(r['question'])

def counts(kp, b, p):
    p.mkdir(parents=True, exist_ok=True)
    shown = DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]', [KP, LEARNER], p, 'ever-shown', b, history=True)
    reserved = DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]', [KP, LEARNER], p, 'reserved', b)
    seen = {r[0] for r in shown + reserved}
    save(p / 'scoped.json', scoped(kp, b, seen))
    subprocess.run([str(POOL), str(p / 'scoped.json'), str(p / 'native-pool.json')], check=True, capture_output=True, text=True, timeout=55)
    pool = json.loads((p / 'native-pool.json').read_text())
    ids = {q for band in pool['available_ids_by_level'].values() for q in band}
    known = {r['question'][':question/id']:r for f in OUT.glob('basis-*/generated.json') for r in json.loads(f.read_text())}
    levels = {l:set() for l in LEVELS}; accepted = []; excluded = []
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] not in ids: continue
        try:
            r = {'question':normalize(q), 'knowledge_point':{'db_id':KP, 'title':kp[':knowledge-point/title']}}
            assert len(r['question'][':question/answer-fields']) == 1
            v.independent(r)
            if ':question/math-academy-id' not in q:
                old = known[str(q[':question/id'])]
                assert ordered(r['question']) == ordered(old['question']); validate(old); r = old
            native([r], p / ('grading-' + str(q[':db/id'])))
            level = r['question'][':question/difficulty'].split('/')[-1]
            levels[level].add(fp(q)); accepted.append(str(q[':question/id']))
        except (AssertionError, KeyError, ValueError, RuntimeError) as e:
            excluded.append({'question_id':str(q[':question/id']), 'source_id':q.get(':question/math-academy-id'), 'reason':str(e) or 'independent displayed mathematics or field shape failed'})
    result = {'basis':b, 'distinct_available':{l:len(s) for l,s in levels.items()}, 'validated_question_ids':accepted, 'excluded':excluded, 'shown_or_reserved':sorted(seen), 'native_pool':pool, 'deduplication':'exact vector field and graph; seed, bounds, template identity, bank and option order excluded'}
    save(p / 'counts.json', result); return result

def source_refresh(kp, b, p):
    current = {q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id' in q}
    assert set(current) == set(g.SOURCES), 'Source coverage changed; reclassify'
    changes = []
    for sid, original in g.SOURCES.items():
        q = current[sid]
        for k in (':question/problem', ':question/worked-solution'):
            # Existing capture cleanup escaped the set braces in three domains.
            normalize_braces = lambda s:s.replace(r'\{', '{').replace(r'\}', '}')
            assert normalize_braces(q[k]) == normalize_braces(original[k]), (sid, k, 'source changed')
            if q[k] != original[k]:
                changes.append({'source_id':sid, 'attribute':k, 'change':'preexisting LaTeX set-brace escaping only'})
        assert str(q[':question/difficulty'][':db/ident']) == ':question.difficulty/easy'
        # The capture schema may already have removed the documented incomplete duplicate.
        a = copy.deepcopy(original)
        a[':question/worked-solution'] = q[':question/worked-solution']
        a[':question/difficulty'] = {':db/ident':kw('question.difficulty/easy')}
        for f in a[':question/answer-fields']:
            f[':answer-field/type'] = {':db/ident':kw('answer-field.type/radio')}
            for ans in f[':answer-field/choices']: ans[':answer/type'] = {':db/ident':kw('answer.type/math')}
        af = [f for f in a[':question/answer-fields'] if ':answer-field/correct' in f]
        qf = [f for f in q[':question/answer-fields'] if ':answer-field/correct' in f]
        a[':question/answer-fields'] = af
        qc = copy.deepcopy(q); qc[':question/answer-fields'] = qf
        assert ordered(normalize(a)) == ordered(normalize(qc)), (sid, 'complete source field changed')
        if len(q[':question/answer-fields']) != len(original[':question/answer-fields']):
            changes.append({'source_id':sid, 'change':'documented incomplete duplicate removed before this job; valid bank unchanged'})
    save(p / 'source-refresh.json', {'basis':b, 'frozen_basis':g.RAW['basis'], 'all_sources_matched':True, 'preexisting_repairs':changes, 'source_writes':0})

def select(kp, needed, p):
    used = {fp(q) for q in kp[':knowledge-point/questions']}
    try: used.add(fp(kp[':knowledge-point/canonical-example']))
    except (AttributeError, IndexError, ValueError): pass
    supplied_path = JOB.with_suffix('.generated')
    supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    rows = supplied.get('instances', [])
    if isinstance(rows, dict): rows = [rows]
    for r in rows: validate(r)
    save(p / 'supplied-status.json', {'exists':supplied_path.exists(), 'validated_instances':len(rows), 'generator_error':supplied.get('generatorError')})
    records = []; added = {l:0 for l in LEVELS}
    for level in LEVELS:
        if not needed[level]: continue
        run = subprocess.run([sys.executable, str(HERE.with_suffix('.py')), '--difficulty', level, '--count', '30', '--seed', str(int(JOB.name[:8],16)), '--format', 'json'], capture_output=True, text=True, check=True, timeout=55)
        candidates = json.loads(run.stdout); save(p / ('cli-'+level+'.json'), candidates)
        for r in rows + candidates:
            if added[level] >= needed[level]: break
            if r['question'][':question/difficulty'] != ':question.difficulty/'+level: continue
            sig = validate(r)
            if sig in used: continue
            used.add(sig); records.append(r); added[level] += 1
    assert all(added[l] == needed[l] for l in LEVELS), 'Bounded sampler exhausted; capability exception required'
    ids = [uuid.UUID(s) for r in records for s in [r['question'][':question/id']] + [f[':answer-field/id'] for f in r['question'][':question/answer-fields']] + [a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']]]
    if ids: assert not DB.query('[:find ?e ?id :in $ [?id ...] :where (or-join [?e ?id] [?e :question/id ?id] [?e :answer-field/id ?id] [?e :answer/id ?id])]', [ids], p, 'generated-identities', DB.basis())
    save(p / 'generated.json', records)
    (p / 'generated.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in records))
    native(records, p / 'selected-grading')
    return records, added

def verify(p, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, p / 'receipt-check', intent['source_eid'])
    b = report[':edb/db-after-t']; kp = read(p / 'readback', b)
    before = loads((p / 'before.edn').read_text())
    old = {q[':db/id']:q for q in before[':knowledge-point/questions']}
    now = {q[':db/id']:q for q in kp[':knowledge-point/questions']}
    assert all(now[e] == q for e,q in old.items()), 'Preexisting question changed'
    ignore = {':knowledge-point/questions', ':knowledge-point/question-generator'}
    assert {k:v for k,v in before.items() if k not in ignore} == {k:v for k,v in kp.items() if k not in ignore}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    records = json.loads((p / 'generated.json').read_text()); assert len(now) == len(old)+len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for r in records:
        q = byid[r['question'][':question/id']]
        assert ':question/math-academy-id' not in q and normalize(q) == ordered(r['question'])
        validate(r)
    assert not transaction([], kp, intent['generator_id'])
    native(records, p / 'readback-grading')
    c = counts(kp, b, p / 'verified-inventory')
    result = {'passed':True, 'basis_before':intent['basis'], 'basis_after':b, 'new_questions':len(records), 'unchanged_source_questions':len(old), 'canonical_example_unchanged':True, 'learner_history_unchanged':True, 'scoped_additive_datoms_only':True, 'configured_application_contributor_verified':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0, 'available_counts_after':c}
    save(p / 'verification.json', result); return result

def finish(p, gid, verified, inv):
    c = verified['available_counts_after']; remaining = {l:max(0, 5-c['distinct_available'][l]) for l in LEVELS}
    assert not any(remaining.values())
    result = {'outcome':'generated', 'knowledgePoint':KP, 'generator_path':SCRIPT, 'generator_id':gid, 'lineage':LINEAGE, 'verified_commit_basis':verified['basis_after'], 'new_questions':verified['new_questions'], 'supported_levels':list(LEVELS), 'unsupported_levels':[], 'shortage_remaining':remaining, 'available_distinct':c['distinct_available'], 'inventory_recheck_basis':inv['basis'], 'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP], 'source_questions_and_learner_history_preserved':True, 'application_contributor':SOURCE, 'difficulty_evidence':'Easy source-backed; moderate/hard bounded authored workload assignments documented in classification.md', 'evidence':[str(f.relative_to(ROOT)) for f in [p/'verification.json',p/'commit-intent.json',p/'transaction.edn',p/'commit.edn',p/'preview.edn',p/'preparation.json',p/'source-refresh.json',p/'generated.json',p/'selected-grading/report.json',p/'inventory-after.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'validation.json',HERE/'reference/native/build.json'] if f.exists()]}
    save(p / 'outcome.json', result); save(JOB.with_suffix('.result'), result)
    print(json.dumps({k:result[k] for k in ('outcome','new_questions','verified_commit_basis','available_distinct','shortage_remaining')}), flush=True)

def main():
    assert json.loads((HERE / 'validation.json').read_text())['passed']
    frozen = json.loads((HERE / 'validated-package.json').read_text())
    assert all(sha(ROOT / name) == digest for name,digest in frozen['file_hashes'].items()), 'Validated package changed; revalidate before reuse'
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    with (ROOT / '.local/learning/requests/math/api.lock').open('a') as lock:
        print('Waiting for application api.lock', flush=True); fcntl.flock(lock, fcntl.LOCK_EX)
        print('Application api.lock acquired', flush=True)
        for p in sorted(OUT.glob('basis-*')):
            if not (p / 'commit-intent.json').exists(): continue
            intent = json.loads((p / 'commit-intent.json').read_text())
            assert intent['database']=='math' and intent['lineage']==LINEAGE and intent['endpoint']==DB.args.endpoint and intent['source']==SOURCE
            assert intent['sha256']==sha(p/'transaction.edn') and intent['exact_edn']==(p/'transaction.edn').read_text()
            assert intent['connection_sha256']==hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified=verify(p,intent,DB._commit(intent,p/'transaction.edn',p))
            finish(p,intent['generator_id'],verified,inventory(p/'inventory-after.json')); return
        inv=inventory(OUT/'inventory-before.json'); b=inv['basis']; assert DB.basis()==b
        p=OUT/('basis-'+str(b)); p.mkdir(exist_ok=True); kp=read(p,b)
        assert str(kp[':knowledge-point/id'])==g.KP_UUID
        source_refresh(kp,b,p); (p/'before.edn').write_text(dumps(kp)+'\n')
        source=DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]',[],p,'source',b); assert len(source)==1
        gen=kp.get(':knowledge-point/question-generator')
        gid=str(gen[':question-generator/id']) if gen else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        existing=DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]',[uuid.UUID(gid),SCRIPT],p,'generator-identity',b)
        if existing:
            assert len(existing)==1 and existing[0][0][':question-generator/script']==SCRIPT
            gid=str(existing[0][0][':question-generator/id'])
        save(HERE/'registration.json',{'id':gid,'script':SCRIPT,'existing_identity_reused':bool(gen or existing)})
        c=counts(kp,b,p/'current-inventory'); needed={l:max(0,5-c['distinct_available'][l]) for l in LEVELS}
        print(json.dumps({'basis':b,'available':c['distinct_available'],'missing':needed}),flush=True)
        records,added=select(kp,needed,p)
        save(p/'preparation.json',{'basis':b,'lineage':LINEAGE,'source':SOURCE,'generator_version':g.VERSION,'generator_sha256':sha(HERE.with_suffix('.py')),'available_counts':c,'missing_by_level':needed,'new_by_level':added,'asset_hashes':[],'mathematics_validated':True,'actual_grader_validated':True,'source_unchanged':True})
        forms=transaction(records,kp,gid)
        if not forms:
            verified={'passed':True,'basis_after':b,'new_questions':0,'available_counts_after':c}
            save(p/'verification.json',verified); finish(p,gid,verified,inv); return
        tx=dumps(forms)+'\n'; txpath=p/'transaction.edn'
        with txpath.open('w') as f: f.write(tx); f.flush(); os.fsync(f.fileno())
        assert DB.basis()==b
        r=subprocess.run([str(preview),'with','--database','math','--file',str(txpath),'--source',SOURCE],env=DB.env,capture_output=True,text=True,timeout=55)
        (p/'preview.log').write_text(r.stderr)
        if r.returncode: raise RuntimeError(r.stderr)
        (p/'preview.edn').write_text(r.stdout); pr=loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t']==b
        check_report(pr,p/'preview-check',source[0][0]); assert DB.basis()==b
        intent={'database':'math','endpoint':DB.args.endpoint,'lineage':LINEAGE,'source':SOURCE,'source_eid':source[0][0],'basis':b,'expected_basis':b,'request_key':'flux-setup-inventory-'+str(KP)+'-'+str(b)+'-'+sha(txpath),'sha256':sha(txpath),'exact_edn':tx,'generator_id':gid,'generator_path':SCRIPT,'generator_sha256':sha(HERE.with_suffix('.py')),'question_uuids':[r['question'][':question/id'] for r in records],'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(),'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(p/'commit-intent.json',intent)
        verified=verify(p,intent,DB._commit(intent,txpath,p))
        finish(p,gid,verified,inventory(p/'inventory-after.json'))

if __name__=='__main__': main()
