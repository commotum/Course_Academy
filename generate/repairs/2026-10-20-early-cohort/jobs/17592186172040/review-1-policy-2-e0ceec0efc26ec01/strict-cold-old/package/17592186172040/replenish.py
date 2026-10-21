"""Finite-domain inventory audit and additive generator registration for this KP."""
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

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts'))
from serve_graph_explorer import database_environment
from inventory_jobs import save
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database
from edn import dumps, loads, kw
from math_format import validate_generated_record
spec = importlib.util.spec_from_file_location('whole_field_validation', HERE / 'validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.G
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.SOURCE['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT / '.local/learning/inventory/math' / LEARNER / '4b6b9a6f6dc8a4cd373eb436ed892a09edce088e72097f22fc5f676b431c24de'
OUT = HERE / 'reference/replenishment'
OUT.mkdir(parents=True, exist_ok=True)
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
DB.env = database_environment('math')
NATIVE = Path((HERE / 'reference/initial/native-path.txt').read_text())
QUERY = (HERE / 'reference/initial/source-query.edn').read_text()
LOCK = ROOT / '.local/learning/requests/math/api.lock'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def plain(x):
    if isinstance(x, dict):
        return {str(k): plain(value) for k, value in x.items()}
    if isinstance(x, list):
        return [plain(value) for value in x]
    return str(x) if isinstance(x, uuid.UUID) else x

def equivalent_capture(actual, expected):
    """Compare every captured fact, ignoring additional Pull navigation keys/order."""
    if isinstance(expected, dict):
        assert all(k in actual for k in expected)
        for k, value in expected.items():
            equivalent_capture(actual[k], value)
    elif isinstance(expected, list):
        assert len(actual) == len(expected)
        if expected and isinstance(expected[0], dict):
            a = sorted(actual, key=lambda x: x[':db/id'])
            e = sorted(expected, key=lambda x: x[':db/id'])
            for left, right in zip(a, e):
                equivalent_capture(left, right)
        else:
            assert sorted(map(str, actual)) == sorted(map(str, expected))
    else:
        assert str(actual) == str(expected), (actual, expected)

def inventory(path):
    r = subprocess.run([str(NATIVE), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=DB.env, capture_output=True, text=True, check=True, timeout=55)
    x = json.loads(r.stdout)
    assert x['ok'] and x['data']['lineage'] == LINEAGE
    save(path, x['data'])
    return x['data']

def read(path, basis):
    return DB.query(QUERY, [KP], path, 'kp', basis)[0][0]

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f: f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a: a[':answer/id'])
    return q

def validate(record):
    m = record['generation']
    level = record['question'][':question/difficulty'].split('/')[-1]
    replay = g.generate(level, seed=m['seed'], template=m['template'], parameters=m['parameters'], profile=m['bank_profile'])
    assert ordered(record['question']) == ordered(replay['question'])
    assert record['generation'] == replay['generation']
    assert record['knowledge_point'] == replay['knowledge_point']
    v.inspect_record(record)
    validate_generated_record(copy.deepcopy(record))

def grade(records, path):
    checks = []
    for i, r in enumerate(records):
        f = r['question'][':question/answer-fields'][0]
        checks.append({'label': str(i), 'record': r, 'checks': [{'submitted_answer_id': a[':answer/id'], 'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected', 'purpose': 'Complete owned image bank through application grader'} for a in f[':answer-field/choices']]})
    save(path / 'grading-input.json', checks)
    subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(path / 'grading-input.json'), str(path / 'grading-report.json')], check=True, capture_output=True, text=True, timeout=55)

def available(kp, basis, path):
    """Current native question counts plus finite mathematical task counts."""
    path.mkdir(parents=True, exist_ok=True)
    shown = DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]', [KP, LEARNER], path, 'ever-shown', basis, history=True)
    reserved = DB.query('[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused]) [?t :learner-task/activity ?a] [?a :activity/steps ?step] [?step :step/content ?q]]', [KP, LEARNER], path, 'reserved', basis)
    excluded = {r[0] for r in shown + reserved}
    # Complete source bank replay and independent dependence validation establish
    # gradability. The unrated source is explicitly excluded, even though its key
    # was inferred in the generation package; the original remains untouched.
    levels = {level: [] for level in g.TEMPLATES}
    demands = {level: set() for level in g.TEMPLATES}
    for q in kp[':knowledge-point/questions']:
        if q[':db/id'] in excluded or ':question/difficulty' not in q or not all(':answer-field/correct' in f for f in q.get(':question/answer-fields', [])):
            continue
        level = str(q[':question/difficulty'][':db/ident']).split('/')[-1]
        sid = q[':question/math-academy-id']
        assert sid in g.SPECS and g.SPECS[sid][0] == level
        levels[level].append(str(q[':question/id']))
        demands[level].add('possible_both' if level != 'hard' else g.SPECS[sid][1])
    result = {'basis': basis, 'available_question_counts': {l: len(qs) for l, qs in levels.items()}, 'available_question_ids': levels, 'distinct_available_task_counts': {l: len(ds) for l, ds in demands.items()}, 'seen_or_reserved_eids': sorted(excluded), 'unrated_ungradable_excluded': ['q-96477'], 'canonical_excluded': True}
    save(path / 'available.json', result)
    return result

def forms(kp, gid):
    gen = kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
        return []
    return [{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid), kw('question-generator/script'): SCRIPT}, [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator'], [kw('db/ensure'), KP, kw('knowledge-point/validate')]]

def check_report(report, path, source_eid, gid):
    attrs = dict(DB.attributes(path, report[':edb/db-before-t']))
    expected = {':question-generator/id', ':question-generator/script', ':knowledge-point/question-generator', ':db/txInstant'}
    for e, a, value, tx, source, added in report[':edb/tx-data']:
        name = str(attrs[a])
        assert source == source_eid and added and name in expected
        if name == ':knowledge-point/question-generator':
            assert e == KP
        if name == ':question-generator/id':
            assert str(value) == gid
        if name == ':question-generator/script':
            assert value == SCRIPT
    assert len(report[':edb/tx-data']) == 4

def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_report(report, path / 'receipt-check', intent['source_eid'], intent['generator_id'])
    b = report[':edb/db-after-t']
    kp = read(path / 'readback', b)
    before = loads((path / 'before.edn').read_text())
    assert {k: value for k, value in kp.items() if k != ':knowledge-point/question-generator'} == {k: value for k, value in before.items() if k != ':knowledge-point/question-generator'}
    assert not forms(kp, intent['generator_id'])
    counts = available(kp, b, path / 'readback')
    result = {'passed': True, 'basis_before': intent['basis'], 'basis_after': b, 'new_questions': 0, 'generator_registration_verified': True, 'source_questions_unchanged': 8, 'canonical_example_unchanged': True, 'learner_history_unchanged': True, 'only_generator_registration_datoms': True, 'repeat_preparation_content_changes': 0, 'inventory': counts}
    save(path / 'verification.json', result)
    return result

def finish(path, gid, verification):
    inv = inventory(path / 'inventory-after.json')
    assert inv['basis'] == DB.basis()
    counts = verification['inventory']['available_question_counts']
    result = {'outcome': 'finite-limit', 'knowledgePoint': KP, 'generator_path': SCRIPT, 'generator_id': gid, 'generator_sha256': sha(HERE.with_suffix('.py')), 'lineage': LINEAGE, 'verified_commit_basis': verification['basis_after'], 'inventory_recheck_basis': inv['basis'], 'new_questions': 0, 'supported_levels': list(g.TEMPLATES), 'unsupported_levels': [], 'unsupported_levels_filled': False, 'available_counts_after': counts, 'shortage_remaining': {l: max(0, 5 - n) for l, n in counts.items()}, 'finite_distinct_task_domain': 3, 'unrepresented_task_categories': 0, 'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP], 'capability_exception': 'All three validated categorical tasks already occur in the original pool. Changed seeds, coefficients, curve geometry, source aliases or choice order are not counted as new assessed tasks by this bounded generator. No source question or learner history was edited. q-96477 remains unrated and ungradable; its inferred repair was not imported.', 'evidence': [str(p.relative_to(ROOT)) for p in [path / 'verification.json', path / 'commit-intent.json', path / 'transaction.edn', path / 'preview.edn', path / 'commit.edn', path / 'preparation.json', path / 'inventory-after.json', OUT / 'candidate-validation.json', OUT / 'duplicate-audit.json', OUT / 'grading-report.json', HERE / 'capabilities.json', HERE / 'classification.md', HERE / 'template-extraction.md', HERE / 'validation.json'] if p.exists()]}
    save(path / 'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k: result[k] for k in ('outcome', 'verified_commit_basis', 'new_questions', 'shortage_remaining')}), flush=True)

def main():
    qa = json.loads((ROOT / 'generate/runs/current/qa/17592186172040.json').read_text())
    assert qa['parent_review'] == 'passed' and qa['generator_sha256'] == sha(HERE.with_suffix('.py'))
    assert json.loads((HERE / 'validation.json').read_text())['status'] == 'passed'
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    inv = inventory(OUT / 'inventory-before-generation.json')
    kp = read(OUT / 'before-generation', inv['basis'])
    equivalent_capture(kp, g.SOURCE['record'])
    # Execute every validated normal template, plus all original bank replays.
    supplied_path = JOB.with_suffix('.generated')
    supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
    instances = supplied.get('instances', [])
    instances = [instances] if isinstance(instances, dict) else instances
    candidates = instances + [g.generate(l, seed=19, template=t) for l, ts in g.TEMPLATES.items() for t in ts]
    source_records = [g.generate(l, template=t, profile=sid, parameters={'scale': 1}) for sid, (l, t, *_rest) in g.SPECS.items()]
    for record in source_records + candidates:
        validate(record)
    geometry = v.source_geometry_check()
    used = {r['generation']['mathematical_fingerprint'] for r in source_records}
    assert len(used) == 3
    assert all(r['generation']['mathematical_fingerprint'] in used for r in candidates)
    save(OUT / 'candidates.json', candidates)
    save(OUT / 'source-geometry-validation.json', geometry)
    grade(source_records + candidates, OUT)
    save(OUT / 'duplicate-audit.json', {'finite_task_fingerprints_in_source': sorted(used), 'rejected': [{'question_id': r['question'][':question/id'], 'template': r['generation']['template'], 'fingerprint': r['generation']['mathematical_fingerprint'], 'reason': 'Assessed dependence category already present in immutable source pool'} for r in candidates], 'accepted_new_questions': 0})
    save(OUT / 'candidate-validation.json', {'passed': True, 'generator_sha256': sha(HERE.with_suffix('.py')), 'pre_generation_inventory_basis': inv['basis'], 'source_bank_replays': 8, 'source_options_matched': 40, 'source_options_total': 40, 'source_geometry_checks': len(geometry), 'normal_templates_executed': 6, 'supplied_generated_file_exists': supplied_path.exists(), 'supplied_instances_validated': len(instances), 'supplied_generator_error': supplied.get('generatorError'), 'validated_candidate_count': len(candidates), 'native_grader_sha256': sha(ROOT / 'generate/runs/current/check-engine'), 'normal_generation_math_and_format_checks': True, 'source_fidelity_evidence': 'validation.json and original frozen parent QA', 'accepted_new_questions': 0, 'asset_publications_required': 0})
    save(HERE / 'capabilities.json', {'generator_path': SCRIPT, 'generator_sha256': sha(HERE.with_suffix('.py')), 'supported_levels': list(g.TEMPLATES), 'finite_meaningful_tasks': {'possible_both': 1, 'impossible_x': 1, 'impossible_y': 1}, 'shared_easy_moderate_category': 'possible_both', 'all_categories_present_in_source': True, 'further_genuinely_distinct_questions': 0, 'fresh_reserve_target_per_supported_level': 5, 'exception': 'The package deliberately fingerprints assessed whole-field dependence categories, not incidental coefficient or image changes. Its three-task domain cannot supply five distinct tasks per level. Existing sources and unrated legacy entry remain unchanged.', 'reopen_when': 'New source evidence supports a genuinely different same-skill task within the intended scope.'})
    with LOCK.open('a') as lock:
        print('Acquiring application api.lock', flush=True)
        fcntl.flock(lock, fcntl.LOCK_EX)
        print('Application api.lock acquired', flush=True)
        for path in sorted(OUT.glob('basis-*')):
            if not (path / 'commit-intent.json').exists():
                continue
            intent = json.loads((path / 'commit-intent.json').read_text())
            assert intent['database'] == 'math' and intent['lineage'] == LINEAGE and intent['endpoint'] == DB.args.endpoint and intent['source'] == SOURCE
            assert intent['sha256'] == sha(path / 'transaction.edn') and intent['exact_edn'] == (path / 'transaction.edn').read_text()
            assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            verified = verify(path, intent, DB._commit(intent, path / 'transaction.edn', path))
            finish(path, intent['generator_id'], verified)
            return
        inv = inventory(OUT / 'inventory-under-lock.json')
        b = inv['basis']
        assert DB.basis() == b
        path = OUT / ('basis-' + str(b))
        path.mkdir(exist_ok=True)
        kp = read(path, b)
        equivalent_capture(kp, g.SOURCE['record'])
        (path / 'before.edn').write_text(dumps(kp) + '\n')
        counts = available(kp, b, path / 'current-inventory')
        source = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', b)
        assert len(source) == 1
        gen = kp.get(':knowledge-point/question-generator')
        registration = HERE / 'registration.json'
        gid = str(gen[':question-generator/id']) if gen else json.loads(registration.read_text())['id'] if registration.exists() else str(uuid.uuid5(uuid.UUID(g.KP_UUID), 'question-generator'))
        existing = DB.query('[:find (pull ?g [*]) :in $ ?id ?script :where (or-join [?g ?id ?script] [?g :question-generator/id ?id] [?g :question-generator/script ?script])]', [uuid.UUID(gid), SCRIPT], path, 'generator-identity', b)
        if existing:
            assert len(existing) == 1 and existing[0][0][':question-generator/script'] == SCRIPT
            gid = str(existing[0][0][':question-generator/id'])
        save(registration, {'id': gid, 'script': SCRIPT, 'existing_identity_reused': bool(gen or existing), 'generator_sha256': sha(HERE.with_suffix('.py'))})
        save(path / 'preparation.json', {'basis': b, 'lineage': LINEAGE, 'source': SOURCE, 'available': counts, 'generated_questions_accepted': 0, 'generator_registration_only': True, 'asset_hashes': [], 'finite_capability_exception': str((HERE / 'capabilities.json').relative_to(ROOT))})
        transaction = forms(kp, gid)
        if not transaction:
            verified = {'passed': True, 'basis_after': b, 'new_questions': 0, 'generator_registration_verified': True, 'inventory': counts, 'no_change': True}
            save(path / 'verification.json', verified)
            finish(path, gid, verified)
            return
        tx = dumps(transaction) + '\n'
        txpath = path / 'transaction.edn'
        with txpath.open('w') as stream:
            stream.write(tx)
            stream.flush()
            os.fsync(stream.fileno())
        r = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, check=True, timeout=55)
        (path / 'preview.edn').write_text(r.stdout)
        report = loads(r.stdout)
        assert report[':edb/committed'] is False and report[':edb/db-before-t'] == b
        check_report(report, path / 'preview-check', source[0][0], gid)
        assert DB.basis() == b
        intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': source[0][0], 'basis': b, 'expected_basis': b, 'request_key': 'whole-field-type-register-' + str(KP) + '-' + str(b) + '-' + sha(txpath), 'sha256': sha(txpath), 'exact_edn': tx, 'generator_id': gid, 'generator_path': SCRIPT, 'generator_sha256': sha(HERE.with_suffix('.py')), 'question_uuids': [], 'lock': str(LOCK), 'connection_sha256': hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()}
        save(path / 'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        verified = verify(path, intent, report)
        finish(path, gid, verified)

if __name__ == '__main__':
    main()
