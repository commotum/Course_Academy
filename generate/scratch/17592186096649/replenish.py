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
spec = importlib.util.spec_from_file_location('validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '234c1114a39736e696d80424c603cf502e2eea7274bb7d0969dccc69bc2ee837'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
NATIVE = build_learning(ROOT.parent / 'EDB')
LEVELS = ('easy','moderate','hard')
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

def localize(rec):
    return replace_paths(rec, {a['path']:local for local,a in asset_index().items()})

def replace_paths(obj, mapping):
    if isinstance(obj,dict):return {k:replace_paths(x,mapping) for k,x in obj.items()}
    if isinstance(obj,list):return [replace_paths(x,mapping) for x in obj]
    if isinstance(obj,str):
        if obj in mapping:return mapping[obj]
        for old,new in mapping.items():
            if old in obj:obj=obj.replace(old,new)
        return obj
    return obj

_ASSETS=None
def asset_index():
    global _ASSETS
    if _ASSETS is None:
        _ASSETS={str(p.relative_to(ROOT)):{'path':'images/'+sha(p)[:2]+'/'+sha(p)+'.png','sha256':sha(p)} for p in (HERE/'plots').glob('*.png') if p.with_suffix('.json').exists() and 'patch_vertices_pixels' in json.loads(p.with_suffix('.json').read_text())}
    return _ASSETS

def validate_instance(rec):
    assert rec['knowledge_point']['db_id']==KP
    assert rec['generation']['eligible_for_learning'] and not rec['generation']['evidence_only']
    assert rec['generation']['version']==g.VERSION
    replay=g.generate(rec['generation']['actual_difficulty'],seed=rec['generation']['seed'],parameters=rec['generation']['parameters'],profile=rec['generation']['bank_profile'])
    # Match content-addressed pixels; historical cache keys can share raster bytes.
    published={local:a['path'] for local,a in asset_index().items()}
    assert ordered(replace_paths(replay['question'],published))==ordered(replace_paths(rec['question'],published)), 'Generated record differs from exact replay'
    v.mathematics(replay)
    assert replay['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']

def validate_existing(q):
    q=localize(normalize(q))
    level=q[':question/difficulty'].split('/')[-1]
    r={'knowledge_point':{'db_id':KP,'id':g.KP_UUID,'title':g.TITLE},'question':q,'generation':{'actual_difficulty':level,'eligible_for_learning':True}}
    v.mathematics(r)


USAGE_QUERY = """[:find ?q :in $ ?kp ?learner :where
 [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q]
 (or-join [?q ?l]
  (and [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q])
  (and [?l :learner/activity ?t] [?t :learner-task/status ?status]
   (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused])
   [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]))]"""

def fingerprint(q):
    import re,math
    sid=q.get(':question/math-academy-id')
    if sid in ('q-11324','q-12140'):
        _,template,p=next(x for x in g.RAW.values() if x[0]==sid)
    elif sid=='e-4280':
        return 'canonical-example-scales-2-and-minus-3'
    else:
        q=localize(q)
        image=re.findall(r'!\[\]\((.*?)\)',q[':question/problem'])[0]
        plot=v.from_plot(image);x,y=plot['vectors'][0]['vector']
        angle=round(math.degrees(math.atan2(y,x)))%360
        tail=q[':question/problem'].split('Which of the following diagrams shows ')[1]
        scales=[str(v.parse_scalar(x)) for x in re.findall(r'\$(.*?)\$',tail)]
        p={'angle':angle,'scales':scales};template='pair' if len(scales)==2 else 'single'
    return g.digest({'angle':p['angle'],'scales':p['scales'],'template':template,'response':'specified scalar multiple diagrams'})

def available_counts(path,kp,basis):
    unavailable={r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'unavailable',basis)}
    # Retained historical presentations and reservations stay excluded as well.
    unavailable.update(r[0] for r in DB.query(USAGE_QUERY,[KP,LEARNER],path,'historically-unavailable',basis,history=True))
    available={level:[] for level in LEVELS}
    excluded=[]
    for q in kp[':knowledge-point/questions']:
        level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
        reason=None
        if q[':db/id'] in unavailable:reason='Shown or reserved, including retained history'
        elif q.get(':knowledge-point/_canonical-example'):reason='Canonical example'
        elif level not in available:reason='Unrated or unsupported difficulty'
        elif not q.get(':question/worked-solution') or not q.get(':question/answer-fields'):reason='Incomplete solution or fields'
        else:
            try:validate_existing(q)
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
    assets=json.loads((path/'assets.json').read_text())
    for asset in assets.values():assert sha(Path('/media/jake/SSD/EDB/math')/asset['path'])==asset['sha256']
    records = json.loads((path/'generated.json').read_text())
    assert len(now) == len(old) + len(records)
    byid = {str(q[':question/id']):q for q in now.values()}
    for rec in records:
        q = byid[rec['question'][':question/id']]
        assert ':question/math-academy-id' not in q
        assert normalize(q) == ordered(rec['question'])
        assert fingerprint(q) == rec['generation']['mathematical_fingerprint']
        validate_instance(rec)
    assert not transaction([], kp, intent['generator_id'])
    counts=available_counts(path/'readback',kp,report[':edb/db-after-t'])
    for level in LEVELS:
        added=sum(r['question'][':question/difficulty']==':question.difficulty/'+level for r in records)
        previous=json.loads((path/'preparation.json').read_text())['available_counts']['levels'][level]['distinct_available_tasks']
        assert counts['levels'][level]['distinct_available_tasks']>=min(5,previous+added)
    result = {'available_counts_after':counts,'passed':True, 'basis_before':intent['basis'], 'basis_after':report[':edb/db-after-t'], 'new_questions':len(records), 'unchanged_source_questions':len(old), 'unchanged_canonical_example':True, 'only_additive_scoped_content_datoms':True, 'learner_history_unchanged':True, 'generator_registration_verified':True, 'repeat_preparation_content_changes':0}
    save(path/'verification.json', result)
    return result

def finish(path, gid, verified, inv):
    preparation=json.loads((path/'preparation.json').read_text())
    caps=json.loads((HERE/'capabilities.json').read_text())
    counts=verified['available_counts_after']
    remaining={level:max(0,5-counts['levels'][level]['distinct_available_tasks']) for level in LEVELS}
    result={'outcome':'finite-limit' if any(remaining.values()) else 'generated','knowledgePoint':KP,
            'generator_path':SCRIPT,'generator_id':gid,'lineage':LINEAGE,
            'verified_commit_basis':verified['basis_after'],'new_questions':verified['new_questions'],'new_by_level':preparation['new_by_level'],
            'supported_levels':list(LEVELS),'unsupported_levels':caps['unsupported_levels'],'capability_exceptions':caps['exceptions']+[{'level':level,'remaining':amount,'bounded_distinct_task_capacity':caps['finite_distinct_tasks'][level],'reason':'Exhaustive finite supported parameter catalog could not supply enough unused distinct tasks; shortage remains explicit.'} for level,amount in remaining.items() if amount],
            'available_counts_before':preparation['available_counts'],'available_counts_after':counts,
            'shortage_remaining':remaining,'unsupported_levels_filled':False,
            'inventory_recheck_basis':inv['basis'],'remaining_jobs':[j for j in inv['jobs'] if j['knowledgePoint']==KP],
            'evidence':[str(p.relative_to(ROOT)) for p in (path/'verification.json',path/'commit-intent.json',path/'transaction.edn',path/'commit.edn',path/'preview.edn',path/'preparation.json',path/'inventory-after.json',path/'native-report.json',path/'native-input.json',path/'assets.json',path/'generated.json',HERE/'batch-validation.json',HERE/'current-engine-build.json',HERE/'validation.json',HERE/'capabilities.json',HERE/'classification.md',HERE/'template-extraction.md',HERE/'plot-extraction.md',HERE/'source.json',HERE/'review.md',HERE/'freeze.json') if p.exists()],
            'note':'All three authored difficulty bands checked for validated distinct unseen and unreserved scalar-multiple diagram tasks. Both unrated incomplete original questions and learner history preserved. Finite catalog and evidence-only source completions documented in capabilities.json.'}
    save(path/'outcome.json',result);save(JOB.with_suffix('.result'),result)
    print(json.dumps({k:result[k] for k in ('outcome','verified_commit_basis','new_questions','remaining_jobs')}),flush=True)

def main():
    validation = json.loads((HERE/'validation.json').read_text())
    assert validation['status']=='pass'
    freeze=json.loads((HERE/'freeze.json').read_text())
    assert freeze['generator_sha256']==sha(HERE.with_suffix('.py'))
    assert freeze['validator_sha256']==sha(HERE/'validate.py')
    assert freeze['renderer_sha256']==sha(HERE/'render.py')
    assert freeze['review_status']=='passed'
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    with (ROOT/'.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        for path in sorted(OUT.glob('basis-*')):
            if (path/'commit-intent.json').exists():
                intent = json.loads((path/'commit-intent.json').read_text())
                assert intent['lineage'] == LINEAGE and intent['source'] == SOURCE and intent['transaction_sha256'] == sha(path/'transaction.edn')
                assert intent['exact_edn'] == (path/'transaction.edn').read_text()
                assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
                inventory(path/'recovery-inventory.json')  # Check immutable target lineage before recovery.
                report = DB._commit(intent, path/'transaction.edn', path)
                verified = verify(path, intent, report)
                finish(path, intent['generator_id'], verified, inventory(path/'inventory-after.json'))
                return
        inv = inventory(OUT/'inventory-before.json')
        b = inv['basis']
        assert DB.basis() == b
        path = OUT / ('basis-'+str(b))
        path.mkdir(exist_ok=True)
        kp = read_kp(path, b)
        assert str(kp[':knowledge-point/id']) == g.KP_UUID
        caps=json.loads((HERE/'capabilities.json').read_text())
        (path/'before.edn').write_text(dumps(kp)+'\n')
        captured = json.loads((HERE/'source.json').read_text())['record']
        expected = {q[':question/math-academy-id']:q for q in captured[':knowledge-point/questions']}
        current = {q.get(':question/math-academy-id'):q for q in kp[':knowledge-point/questions']}
        assert set(expected) <= set(current)
        for mid, q in expected.items():
            assert canonical(current[mid]) == canonical(q), 'Source evidence changed; reclassify '+mid
        assert canonical(captured[':knowledge-point/canonical-example']) == canonical(kp[':knowledge-point/canonical-example'])
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', b)
        assert len(source) == 1
        gen = kp.get(':knowledge-point/question-generator')
        existing_generators=DB.query('[:find ?g ?id :in $ ?script :where [?g :question-generator/script ?script] [?g :question-generator/id ?id]]',[SCRIPT],path,'generator-identity',b)
        assert len(existing_generators)<=1, 'Ambiguous registered generator identity'
        gid = str(gen[':question-generator/id']) if gen else str(existing_generators[0][1]) if existing_generators else str(uuid.uuid5(uuid.UUID(g.KP_UUID),'question-generator'))
        jobs = {j['difficulty']:j for j in inv['jobs'] if j['knowledgePoint'] == KP}
        counts=available_counts(path,kp,b)
        needed={level:max(jobs.get(level,{}).get('missing',0),5-counts['levels'][level]['distinct_available_tasks'],0) for level in LEVELS}
        used = {fingerprint(q) for q in kp[':knowledge-point/questions']}
        used.add(fingerprint(kp[':knowledge-point/canonical-example']))
        records = []
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances', [])
        if isinstance(instances,dict):instances=instances.get('instances',[])
        assert isinstance(instances, list)
        rejected = []
        eligible = []
        for rec in instances:
            if rec['question'][':question/difficulty'].split('/')[-1] not in LEVELS:
                rejected.append({'question_id':rec['question'][':question/id'],'reason':'Unsupported difficulty; not committed'})
                continue
            validate_instance(rec)
            eligible.append(rec)
        save(path/'supplied-status.json', {'exists':supplied_path.exists(), 'instances_validated':len(eligible), 'unsupported_rejected':rejected, 'generator_error':supplied.get('generatorError')})
        # Bounded search; mathematical fingerprints exclude seed, IDs, variable naming and option order.
        local=[];added={level:0 for level in LEVELS}
        for rec in eligible:
            level=rec['question'][':question/difficulty'].split('/')[-1]
            fp=fingerprint(rec['question'])
            if added[level]<needed[level] and fp not in used:
                records.append(rec);used.add(fp);added[level]+=1
        for level in LEVELS:
            if added[level]>=needed[level]:continue
            # Bounded seeded search over parameter tuples; duplicates are excluded by scalar-multiple diagram task fingerprint.
            # Request enough distinct candidates to cover all already-used tasks.
            candidates=g.batch(level, min(caps['bounded_candidate_scan'][level], needed[level]+len(used)), int(JOB.name[:8],16))
            for rec in candidates:
                if added[level]>=needed[level]:break
                validate_instance(rec);local.append(rec)
                assert fingerprint(rec['question'])==rec['generation']['mathematical_fingerprint']
                fp=fingerprint(rec['question'])
                if fp not in used:
                    records.append(rec);used.add(fp);added[level]+=1
        # Refuse identity collisions globally, including component IDs.
        identities={kind:[item[':'+kind+'/id'] for rec in records for item in ([rec['question']] if kind=='question' else rec['question'][':question/answer-fields'] if kind=='answer-field' else [a for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']])] for kind in ('question','answer-field','answer')}
        for kind,ids in identities.items():
            assert len(ids)==len(set(ids))
            collision=DB.query('[:find ?e :in $ [?id ...] :where [?e :'+kind+'/id ?id]]', [list(map(uuid.UUID,ids))],path,'identity-'+kind,b)
            assert not collision,'Identity already present; reconcile before commit'
        save(path/'local-preview.json',local);save(path/'generated-local.json',records)
        subprocess.run(['/usr/bin/python3',str(HERE/'publish_assets.py'),str(path)],check=True)
        records=json.loads((path/'generated.json').read_text())
        assets=json.loads((path/'assets.json').read_text())
        for local_path,asset in assets.items():
            assert sha(ROOT/local_path)==asset['sha256']==sha(Path('/media/jake/SSD/EDB/math')/asset['path'])

        native=[]
        for rec in records+eligible:
            validate_instance(rec)
            f=rec['question'][':question/answer-fields'][0]
            native.append({'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned option after asset publication'} for a in f[':answer-field/choices']]})
        save(path/'native-input.json',native)
        if native:
            subprocess.run([str(HERE/'check-current-engine'),str(path/'native-input.json'),str(path/'native-report.json')],check=True)
            assert json.loads((path/'native-report.json').read_text())['documented_unresolved_checks']==0
        save(path/'preparation.json', {'basis':b, 'lineage':LINEAGE, 'source':SOURCE, 'generator_id':gid,
            'missing_by_level':needed,'new_by_level':added,'local_previews':len(local),'new_questions':len(records),
            'source_evidence_unchanged':True,'asset_hashes':assets,
            'used_tasks_before':len({fingerprint(q) for q in kp[':knowledge-point/questions']}),
            'distinct_generated_tasks':len({fingerprint(r['question']) for r in records}),
            'available_counts':counts,'inventory_count_evidence':'Native inventory plus conservative distinct mathematical task count at the same basis',
            'finite_remaining':{level:max(0,needed[level]-added[level]) for level in LEVELS}})
        forms = transaction(records, kp, gid)
        if not forms:
            save(path/'verification.json', {'passed':True, 'basis_before':b, 'basis_after':b, 'new_questions':0, 'no_changes':True, 'generator_registration_verified':True,'available_counts_after':counts})
            finish(path, gid, json.loads((path/'verification.json').read_text()), inv)
            return
        txpath = path/'transaction.edn'
        tx = dumps(forms)+'\n'
        with txpath.open('w') as f:
            f.write(tx); f.flush(); os.fsync(f.fileno())
        r = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, check=True, timeout=90)
        (path/'preview.edn').write_text(r.stdout)
        pr = loads(r.stdout)
        assert pr[':edb/committed'] is False and pr[':edb/db-before-t'] == b
        check_report(pr, path/'preview-check', source[0][0])
        assert DB.basis() == b
        intent = {'database':'math', 'endpoint':DB.args.endpoint, 'lineage':LINEAGE, 'source':SOURCE, 'source_eid':source[0][0], 'basis':b, 'expected_basis':b, 'request_key':'parallel-vectors-inventory-17592186096649-'+str(b)+'-'+sha(txpath), 'transaction_sha256':sha(txpath), 'sha256':sha(txpath), 'exact_edn':tx, 'generator_id':gid, 'generator_path':SCRIPT, 'generator_sha256':sha(HERE.with_suffix('.py')), 'question_uuids':[rec['question'][':question/id'] for rec in records], 'connection_sha256':hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock':str(ROOT/'.local/learning/requests/math/api.lock')}
        save(path/'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        verified = verify(path, intent, report)
        finish(path, gid, verified, inventory(path/'inventory-after.json'))

if __name__ == '__main__':
    main()
