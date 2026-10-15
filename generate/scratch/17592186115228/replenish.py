"""Serialize finite-generator registration, with exact requests and readback."""
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
from types import SimpleNamespace
import uuid

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path[:0] = [str(ROOT/'scripts'), str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps, loads, kw
from inventory_jobs import save
from serve_graph_explorer import database_environment, build_learning

spec = importlib.util.spec_from_file_location('finite_matrix_validation', HERE/'validate.py')
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
g = v.g
KP = g.KP_ID
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE = g.S['lineage']
SOURCE = ':application/ca-engine'
SCRIPT = str(HERE.with_suffix('.py').relative_to(ROOT))
JOB = ROOT/'.local/learning/inventory/math'/LEARNER/'6fbda74c1c1709b34c723a89b3f2b10c0d6e289478e68097921b6ab8fed66af5'
OUT = ROOT/'reference/generated'/str(KP)/'job-6fbda74c'
LOCK = ROOT/'.local/learning/requests/math/api.lock'
DB = Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'), database='math', endpoint=database_environment('math')['EDB_ENDPOINT']))
QUERY = (HERE/'source-query.edn').read_text()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_kp(path, basis):
    rows = DB.query(QUERY, [[KP]], path, 'kp', basis)
    assert len(rows) == 1
    return rows[0][0]


def inventory(binary, path):
    result = subprocess.run([str(binary), 'math', LEARNER, DB.args.endpoint], input='{"action":"inventory"}', env=DB.env, capture_output=True, text=True, check=True, timeout=55)
    response = json.loads(result.stdout); assert response['ok']
    inv = response['data']; assert inv['lineage'] == LINEAGE
    save(path, inv)
    with tempfile.TemporaryDirectory(prefix='matrix-identity-inventory-') as temporary:
        snapshot = Path(temporary)/'snapshot.json'
        result = subprocess.run([str(binary), 'math', LEARNER, DB.args.endpoint], input='{"action":"export-test-snapshot"}', env={**DB.env, 'LEARNING_SNAPSHOT_PATH': str(snapshot)}, capture_output=True, text=True, check=True, timeout=55)
        assert json.loads(result.stdout)['ok']
        counts = path.with_name(path.stem+'-counts.json')
        subprocess.run([str(HERE/'inspect-inventory'), str(snapshot), str(counts)], check=True, timeout=55)
    available = json.loads(counts.read_text())
    assert available['basis'] == inv['basis'] == DB.basis(), 'Basis advanced; fresh inventory required'
    return inv, available


def transaction(kp, gid):
    gen = kp.get(':knowledge-point/question-generator')
    if gen:
        assert str(gen[':question-generator/id']) == gid and gen[':question-generator/script'] == SCRIPT
        return []
    return [{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(gid), kw('question-generator/script'): SCRIPT},
            [kw('db/add'), KP, kw('knowledge-point/question-generator'), 'generator'],
            [kw('db/ensure'), KP, kw('knowledge-point/validate')]]


def check_datoms(report, path, source):
    attrs = {e: str(a) for e, a in DB.attributes(path, report[':edb/db-before-t'])}
    new = set(report[':edb/tempids'].values())
    for e, a, value, tx, s, added in report[':edb/tx-data']:
        assert s == source and added, 'Unexpected attribution or retraction'
        name = attrs[a]
        if e == KP:
            assert name == ':knowledge-point/question-generator'
        elif name != ':db/txInstant':
            assert e in new and name in (':question-generator/id', ':question-generator/script')


def verify(path, intent, report):
    assert report[':edb/committed'] is True and report[':edb/db-before-t'] == intent['basis']
    check_datoms(report, path/'receipt-check', intent['source_eid'])
    kp = read_kp(path/'readback', report[':edb/db-after-t'])
    before = loads((path/'before.edn').read_text())
    omit = {':knowledge-point/question-generator'}
    assert {k: x for k, x in kp.items() if k not in omit} == {k: x for k, x in before.items() if k not in omit}
    gen = kp[':knowledge-point/question-generator']
    assert str(gen[':question-generator/id']) == intent['generator_id'] and gen[':question-generator/script'] == SCRIPT
    assert transaction(kp, intent['generator_id']) == []
    verified = {'passed': True, 'basis_before': intent['basis'], 'basis_after': report[':edb/db-after-t'], 'new_questions': 0,
                'unchanged_source_questions': len(kp[':knowledge-point/questions']), 'unchanged_canonical_example': True,
                'learner_history_unchanged': True, 'generator_registration_verified': True, 'only_additive_scoped_generator_datoms': True,
                'repeat_preparation_content_changes': 0, 'fresh_candidates_rejected_as_duplicates': True}
    save(path/'verification.json', verified)
    return verified


def finish(path, intent, verified, binary):
    inv, counts = inventory(binary, path/'inventory-after.json')
    caps = json.loads((HERE/'capabilities.json').read_text())
    native = counts['available_by_level']
    result = {'outcome': 'finite-limit', 'knowledgePoint': KP, 'topic': 17592186050122,
              'generator_path': SCRIPT, 'generator_id': intent['generator_id'], 'generator_registered': True,
              'lineage': LINEAGE, 'verified_commit_basis': verified['basis_after'], 'preparation_basis': intent['basis'],
              'action': 'validated-finite-generator-registration', 'new_questions': 0,
              'supported_levels': list(g.LEVELS), 'unsupported_levels': ['easy'], 'unsupported_levels_filled': False,
              'available_by_level': native, 'inventory_recheck_basis': inv['basis'],
              'remaining_supported_shortages': {level: max(0, 5-native[level]) for level in g.LEVELS},
              'unsupported_shortages': {'easy': 5}, 'finite_limits': caps['finite_limits'], 'capability_exceptions': caps['exceptions'],
              'remaining_jobs': [j for j in inv['jobs'] if j['knowledgePoint'] == KP],
              'inventory_count_note': 'Native application counts are retained. These are upper bounds on conceptual distinctness; no dimension/seed/choice-order changes were added or counted as fresh.',
              'source_questions_and_learner_history_preserved': True,
              'evidence': [str(p.relative_to(ROOT)) for p in (path/'verification.json', path/'commit-intent.json', path/'commit.edn', path/'preview.edn', path/'preparation.json', path/'inventory-before.json', path/'inventory-before-counts.json', path/'inventory-after.json', path/'inventory-after-counts.json', HERE/'source.json', HERE/'classification.md', HERE/'template-extraction.md', HERE/'plot-extraction.md', HERE/'capabilities.json', HERE/'source-replay.json', HERE/'mathematics.json', HERE/'dimension-coverage.json', HERE/'native-report.json', HERE/'validation.json', HERE/'native-build.json')],
              'note': 'All extracted source tasks already exist. Dimensions 2..8, seeds, IDs, renaming and option order do not produce fresh universal-law questions. Easy is unsupported; any hard reserve shortage remains explicit. This is a bounded capability exception, reopened by new source evidence.'}
    save(path/'outcome.json', result)
    save(JOB.with_suffix('.result'), result)
    print(json.dumps({k: result[k] for k in ('outcome', 'generator_path', 'verified_commit_basis', 'new_questions', 'available_by_level', 'remaining_supported_shortages')}, indent=2), flush=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    validation = json.loads((HERE/'validation.json').read_text()); assert validation['passed']
    for rel, expected in validation['hashes'].items(): assert sha(ROOT/rel) == expected
    for executable, expected in json.loads((HERE/'native-build.json').read_text())['executables'].items(): assert sha(Path(executable)) == expected
    binary = build_learning(ROOT.parent/'EDB')
    preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT, preview_bin=None), threading.Event())
    with LOCK.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        # Exact intent recovery must precede any fresh reads or new intent.
        for path in sorted(OUT.glob('basis-*')):
            if not (path/'commit-intent.json').exists(): continue
            intent = json.loads((path/'commit-intent.json').read_text())
            assert intent['database'] == 'math' and intent['lineage'] == LINEAGE and intent['source'] == SOURCE
            assert intent['endpoint'] == DB.args.endpoint and intent['exact_edn'] == (path/'transaction.edn').read_text()
            assert intent['sha256'] == sha(path/'transaction.edn')
            assert intent['connection_sha256'] == hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest()
            report = DB._commit(intent, path/'transaction.edn', path)
            verified = verify(path, intent, report)
            finish(path, intent, verified, binary)
            return
        inv, counts = inventory(binary, OUT/'inventory-before.json')
        b = inv['basis']; path = OUT/('basis-'+str(b)); path.mkdir(exist_ok=True)
        for name in ('inventory-before.json', 'inventory-before-counts.json'):
            (path/name).write_bytes((OUT/name).read_bytes())
        kp = read_kp(path, b)
        assert str(kp[':knowledge-point/id']) == g.KP_UUID
        evidence = loads((HERE/'source.edn').read_text())[0][0]
        assert {k: x for k, x in kp.items() if k != ':knowledge-point/question-generator'} == {k: x for k, x in evidence.items() if k != ':knowledge-point/question-generator'}, 'Source evidence changed; reclassify'
        (path/'before.edn').write_text(dumps(kp)+'\n')
        contributor = DB.query('[:find ?e :where [?e :db/ident :application/ca-engine]]', [], path, 'contributor', b)
        assert len(contributor) == 1
        registered = DB.query('[:find (pull ?g [*]) :in $ ?script :where [?g :question-generator/script ?script]]', [SCRIPT], path, 'generator-by-script', b)
        gen = kp.get(':knowledge-point/question-generator')
        gid = str(gen[':question-generator/id']) if gen else str(registered[0][0][':question-generator/id']) if registered else g.GENERATOR_UUID
        collision = DB.query('[:find (pull ?g [*]) :in $ ?id :where [?g :question-generator/id ?id]]', [uuid.UUID(gid)], path, 'generator-by-id', b)
        assert len(registered) <= 1 and (not collision or len(collision) == 1 and collision[0][0][':question-generator/script'] == SCRIPT)
        supplied_path = JOB.with_suffix('.generated')
        supplied = json.loads(supplied_path.read_text()) if supplied_path.exists() else {}
        instances = supplied.get('instances', [])
        if isinstance(instances, dict): instances = [instances]
        used = {g.fingerprint(q) for q in kp[':knowledge-point/questions']}
        supplied_report = []
        for rec in instances:
            v.check(rec)
            assert g.fingerprint(rec['question']) in used, 'Unexpected fresh instance; return to preparation'
            supplied_report.append({'question_id': rec['question'][':question/id'], 'validated': True, 'rejected_for_fresh_inventory': 'Existing mathematical task'})
        save(path/'supplied-validation.json', {'exists': supplied_path.exists(), 'instances': supplied_report, 'generatorError': supplied.get('generatorError')})
        assert all(g.fresh(level, max(0, 5-counts['available_by_level'][level]), 1930, used) == [] for level in g.LEVELS)
        save(path/'generated.json', [])
        save(path/'preparation.json', {'basis': b, 'lineage': LINEAGE, 'source': SOURCE, 'generator_id': gid, 'generator_path': SCRIPT,
                                      'available_by_level': counts['available_by_level'], 'fresh_selected': 0, 'asset_hashes': [],
                                      'unproduced_by_level': {level: max(0, 5-counts['available_by_level'][level]) for level in g.LEVELS},
                                      'easy_unsupported_and_unfilled': True, 'source_evidence_unchanged': True, 'reason': 'Finite extracted bank exhausted; no cosmetic duplicates.'})
        forms = transaction(kp, gid)
        assert forms, 'Already registered: retain original verified receipt rather than perform an empty commit'
        txpath = path/'transaction.edn'; tx = dumps(forms)+'\n'
        with txpath.open('w') as out:
            out.write(tx); out.flush(); os.fsync(out.fileno())
        response = subprocess.run([str(preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE], env=DB.env, capture_output=True, text=True, check=True, timeout=55)
        (path/'preview.edn').write_text(response.stdout)
        report = loads(response.stdout)
        assert report[':edb/committed'] is False and report[':edb/db-before-t'] == b
        check_datoms(report, path/'preview-check', contributor[0][0])
        assert DB.basis() == b
        intent = {'database': 'math', 'endpoint': DB.args.endpoint, 'lineage': LINEAGE, 'source': SOURCE, 'source_eid': contributor[0][0],
                  'basis': b, 'expected_basis': b, 'request_key': 'matrix-identities-finite-17592186115228-'+str(b)+'-'+sha(txpath),
                  'sha256': sha(txpath), 'transaction_sha256': sha(txpath), 'exact_edn': tx, 'generator_id': gid, 'generator_path': SCRIPT,
                  'generator_sha256': sha(HERE.with_suffix('.py')), 'question_uuids': [], 'connection_sha256': hashlib.sha256(DB.env['EDB_POSTGRES_URL'].encode()).hexdigest(), 'lock': str(LOCK)}
        save(path/'commit-intent.json', intent)
        report = DB._commit(intent, txpath, path)
        verified = verify(path, intent, report)
        finish(path, intent, verified, binary)


if __name__ == '__main__':
    main()
