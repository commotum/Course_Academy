#!/usr/bin/env python3
"""Add only validated instances for this KP, under the application lock."""
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import threading
import uuid
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
sys.path.insert(0, str(ROOT / 'scripts/question_capture'))
from database import Database, QUESTION_PULL
from edn import dumps, kw, loads
from core import atomic_json

spec = importlib.util.spec_from_file_location('matrix_indices', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
REF = HERE / 'reference'
SOURCE = ':application/ca-engine'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
KEY = 'fb0557b5cc961bc78058c6c8f7982a2feca24eb4c360d243c1cccdfe5d8b93cd'
RESULT = ROOT / '.local/learning/inventory/math' / LEARNER / (KEY + '.result')
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math'))
PATTERN = '[* {:knowledge-point/question-generator [*]} {:knowledge-point/questions ' + QUESTION_PULL + '} {:knowledge-point/canonical-example ' + QUESTION_PULL + '}]'
LEARNING = ROOT / '.local/graph-explorer/learning-80371ed6e5f3669c'

def save(name, value):
    atomic_json(REF / name, value)

def durable_text(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('w') as stream:
        stream.write(value)
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)
    fd = os.open(path.parent, os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def inventory(name):
    # HTTP inventory also acquires api.lock: invoke the existing native reader
    # directly while we hold that lock, rather than deadlocking the HTTP route.
    reply = subprocess.run([str(LEARNING), 'math', LEARNER, '/tmp/edb-math/writer.sock'],
        input=json.dumps({'action': 'inventory'}), text=True, capture_output=True,
        check=True, env=DB.env, timeout=55)
    response = json.loads(reply.stdout)
    assert response['ok'], response
    data = response['data']
    assert data['lineage'] == LINEAGE
    save(name, data)
    return data

def pull(basis, name):
    path = REF / 'pull.edn'
    path.write_text(PATTERN)
    result = DB.command('pull', '--file', path, '--entity', g.KP_ID, '--as-of', basis)
    durable_text(REF / name, result)
    return loads(result)

def typed(value):
    if isinstance(value, dict):
        return {kw(k): typed(v) for k, v in value.items()}
    if isinstance(value, list):
        return list(map(typed, value))
    if isinstance(value, str) and value.startswith(':'):
        return kw(value)
    if isinstance(value, str) and re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', value):
        return uuid.UUID(value)
    return value

def existing_cell(question):
    # Numerical matrix values alone never identify a highlighted location.
    problem = question[':question/problem']
    if r'P=[\begin{aligned}' not in problem:
        return None
    matrix = re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', problem, re.S)
    if not matrix:
        return None
    stripped = re.sub(r'\\bbox\[lightgray, 2pt\]\{(-?\d+)\}', r'\1', matrix.group(1))
    if re.sub(r'\s+', '', stripped) != re.sub(r'\s+', '', r'0 & -2 & 2 \\ 2 & 0 & -2 \\ -2 & 2 & 0'):
        return None
    if '{{field-1}}' not in problem or '{{field-2}}' not in problem:
        return None
    fields = {f[':answer-field/key']: f for f in question.get(':question/answer-fields', [])}
    try:
        return tuple(int(fields[k][':answer-field/correct'][':answer/value']) for k in ('field-1', 'field-2'))
    except (KeyError, ValueError):
        return None

def prepare(native_preview):
    inv = inventory('inventory-locked-before.json')
    basis = inv['basis']
    assert DB.basis() == basis
    original = pull(basis, 'before.edn')
    source = loads((REF / 'source.edn').read_text())
    old_sources = {str(q[':question/id']): q for q in source[':knowledge-point/questions']}
    now_sources = {str(q[':question/id']): q for q in original[':knowledge-point/questions']}
    assert all(now_sources.get(qid) == q for qid, q in old_sources.items()), 'Source evidence changed: reclassify'
    assert original[':knowledge-point/canonical-example'] == source[':knowledge-point/canonical-example']
    registration = original.get(':knowledge-point/question-generator')
    generator_id = str(registration[':question-generator/id']) if registration else g.GENERATOR_ID
    if registration:
        assert registration.get(':question-generator/script') in (None, g.SCRIPT), 'Reuse the other registered generator rather than replacing it'
    jobs = [j for j in inv['jobs'] if j['knowledgePoint'] == g.KP_ID and j['difficulty'] == 'easy']
    assert len(jobs) <= 1
    missing = jobs[0]['missing'] if jobs else 0
    available = jobs[0]['available'] if jobs else 5
    cells = {existing_cell(q) for q in original[':knowledge-point/questions']}
    existing_ids = set(now_sources)
    prompts = {q[':question/problem'] for q in original[':knowledge-point/questions']}
    candidates = json.loads((HERE / 'generated.json').read_text())
    eligible = [r for r in candidates if tuple(r['generation']['parameters'][k] for k in ('i', 'j')) not in cells
        and r['question'][':question/id'] not in existing_ids and r['question'][':question/problem'] not in prompts]
    selected = eligible[:missing]
    forms = []
    for record in selected:
        expected = g.generate_easy(record['generation']['seed'], parameters=record['generation']['parameters'])
        assert expected == record, 'Only deterministic validated instances may be prepared'
        q = record['question']
        authored = typed(q)
        qref = 'q-' + q[':question/id']
        authored[kw('db/id')] = qref
        for f, tf in zip(q[':question/answer-fields'], authored[kw('question/answer-fields')]):
            tf[kw('db/id')] = 'f-' + f[':answer-field/id']
            for a, ta in zip(f[':answer-field/choices'], tf[kw('answer-field/choices')]):
                ta[kw('db/id')] = 'a-' + a[':answer/id']
            tf[kw('answer-field/correct')] = 'a-' + f[':answer-field/correct'][1]
        forms += [authored, [kw('db/add'), g.KP_ID, kw('knowledge-point/questions'), qref],
            [kw('db/ensure'), qref, kw('question/validate')]]
        for f in q[':question/answer-fields']:
            forms.append([kw('db/ensure'), 'f-' + f[':answer-field/id'], kw('answer-field/validate')])
            for a in f[':answer-field/choices']:
                forms.append([kw('db/ensure'), 'a-' + a[':answer/id'], kw('answer/validate')])
    forms += [{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(generator_id),
        kw('question-generator/script'): g.SCRIPT},
        [kw('db/add'), g.KP_ID, kw('knowledge-point/question-generator'), 'generator'],
        [kw('db/ensure'), g.KP_ID, kw('knowledge-point/validate')]]
    contributor = DB.query('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]', [kw(SOURCE)], REF, 'contributor', basis)
    assert len(contributor) == 1
    txpath = REF / 'transaction.edn'
    durable_text(txpath, dumps(forms) + '\n')
    sha = hashlib.sha256(txpath.read_bytes()).hexdigest()
    save('preparation.json', {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE,
        'records': selected, 'generator_id': generator_id, 'sha256': sha, 'requested_missing': missing,
        'plots': [], 'excluded_existing_cells': sorted(c for c in cells if c is not None),
        'remaining_finite_shortage': max(0, missing - len(selected))})
    result = subprocess.run([str(native_preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE],
        text=True, capture_output=True, check=True, env=DB.env, timeout=55)
    durable_text(REF / 'preview.edn', result.stdout)
    assert loads(result.stdout)[':edb/db-before-t'] == basis, 'Basis advanced: return to preparation'
    intent = {'database': 'math', 'endpoint': '/tmp/edb-math/writer.sock', 'lineage': LINEAGE,
        'basis': basis, 'source': SOURCE, 'source_entity': contributor[0][0], 'sha256': sha,
        'request_key': 'ca-kp-17592186100990-' + str(basis) + '-' + sha,
        'exact_edn': txpath.read_text(), 'generator_id': generator_id, 'records': selected,
        'available_before': available, 'requested_missing': missing, 'unique_candidates_remaining': len(eligible) - len(selected)}
    save('commit-intent.json', intent)
    return intent

def verify(receipt, intent):
    assert receipt[':edb/committed'] is True
    before, after = receipt[':edb/db-before-t'], receipt[':edb/db-after-t']
    assert before == intent['basis']
    attrs = dict(DB.attributes(REF / 'verification', before))
    allowed = {'question/id', 'question/problem', 'question/worked-solution', 'question/difficulty', 'question/answer-fields',
        'answer-field/id', 'answer-field/key', 'answer-field/type', 'answer-field/choices', 'answer-field/correct',
        'answer/id', 'answer/type', 'answer/value', 'knowledge-point/questions', 'knowledge-point/question-generator',
        'question-generator/id', 'question-generator/script', 'db/txInstant'}
    for row in receipt[':edb/tx-data']:
        name = str(attrs[row[1]])[1:]
        assert name in allowed and row[-1] is True, 'Unexpected attribute/retraction'
        assert row[-2] == intent['source_entity'], 'Unexpected contributor'
        if name.startswith('knowledge-point/'):
            assert row[0] == g.KP_ID, 'Another KP changed'
    original = loads((REF / 'before.edn').read_text())
    current = pull(after, 'readback.edn')
    old = {str(q[':question/id']): q for q in original[':knowledge-point/questions']}
    new = {str(q[':question/id']): q for q in current[':knowledge-point/questions']}
    assert all(new[qid] == q for qid, q in old.items()), 'Source questions changed'
    assert current[':knowledge-point/canonical-example'] == original[':knowledge-point/canonical-example']
    assert set(new) == set(old) | {r['question'][':question/id'] for r in intent['records']}
    registration = current[':knowledge-point/question-generator']
    assert str(registration[':question-generator/id']) == intent['generator_id']
    assert registration[':question-generator/script'] == g.SCRIPT
    for record in intent['records']:
        q = record['question']
        actual = new[q[':question/id']]
        for key in (':question/problem', ':question/worked-solution'):
            assert actual[key] == q[key]
        assert actual[':question/difficulty'][':db/ident'] == q[':question/difficulty']
        assert ':question/math-academy-id' not in actual
        fields = {str(f[':answer-field/id']): f for f in actual[':question/answer-fields']}
        assert set(fields) == {f[':answer-field/id'] for f in q[':question/answer-fields']}
        for ef in q[':question/answer-fields']:
            af = fields[ef[':answer-field/id']]
            assert af[':answer-field/key'] == ef[':answer-field/key']
            assert af[':answer-field/type'][':db/ident'] == ef[':answer-field/type']
            assert str(af[':answer-field/correct'][':answer/id']) == ef[':answer-field/correct'][1]
            assert len(af[':answer-field/choices']) == 1
            aa, ea = af[':answer-field/choices'][0], ef[':answer-field/choices'][0]
            assert str(aa[':answer/id']) == ea[':answer/id'] and aa[':answer/value'] == ea[':answer/value']
            assert aa[':answer/type'][':db/ident'] == ea[':answer/type']
    inv = inventory('inventory-after.json')
    shortages = [j for j in inv['jobs'] if j['knowledgePoint'] == g.KP_ID]
    short_easy = [j for j in shortages if j['difficulty'] == 'easy']
    added = len(intent['records'])
    remaining = max(0, intent['requested_missing'] - added)
    if remaining == 0:
        assert not short_easy
    # Repeat content selection against exact db_after: no submitted candidate survives.
    cells = {existing_cell(q) for q in current[':knowledge-point/questions']}
    assert all(tuple(r['generation']['parameters'][k] for k in ('i', 'j')) in cells for r in intent['records'])
    verified = {'committed': True, 'basis_before': before, 'verified_commit_basis': after,
        'inventory_basis_after': inv['basis'], 'questions_added': added, 'source': SOURCE,
        'request_key': intent['request_key'], 'exact_readback_verified': True,
        'preserved_source_questions_and_canonical_example': True, 'learner_or_engine_datoms': 0,
        'only_requested_kp_changed': True, 'repeat_preparation_content_changes': 0,
        'remaining_inventory_jobs': shortages, 'remaining_easy_shortage': remaining,
        'easy_available_after': short_easy[0]['available'] if short_easy else intent['available_before'] + added}
    save('verification.json', verified)
    exceptions = [{'difficulty': level, 'status': 'unclassified', 'generator_supported': False,
        'filled': False, 'available_validated_generated': 0, 'potential_minimum_shortage': 5,
        'reason': 'No observed source template or certified generator in this bounded package; absence is not proof of impossibility'}
        for level in ('moderate', 'hard')]
    exceptions.append({'difficulty': 'easy', 'finite_variant_limit': 9, 'original_cell_not_imported': [3, 2],
        'new_candidates_remaining': intent['unique_candidates_remaining'], 'remaining_shortage': remaining,
        'other_templates_certified': False, 'reason': 'Only distinct highlighted positions of the fixed source matrix; no identity/seed variants'})
    atomic_json(RESULT, {'outcome': 'finite-limit' if remaining else 'generated',
        'knowledgePoint': g.KP_ID, 'topic': 17592186050163, 'database': 'math', 'lineage': LINEAGE,
        'generator_path': g.SCRIPT, 'generator_id': intent['generator_id'], 'generator_version': g.VERSION,
        'verified_commit_basis': after, 'commit_basis_before': before, 'requested_basis': 1831,
        'source_basis': json.loads((HERE / 'source.json').read_text())['basis'],
        'generated': {'easy': added, 'moderate': 0, 'hard': 0},
        'easy_available_after': verified['easy_available_after'], 'remaining_easy_shortage': remaining,
        'capability_exceptions': exceptions, 'remaining_inventory_jobs': shortages,
        'preserved_source_questions_and_learner_history': True,
        'evidence': [str((HERE / name).relative_to(ROOT)) for name in ('classification.json', 'classification.md',
            'template-extraction.md', 'plot-extraction.md', 'validation.json', 'review.md',
            'reference/preparation.json', 'reference/transaction.edn', 'reference/preview.edn',
            'reference/commit-intent.json', 'reference/commit.edn', 'reference/readback.edn',
            'reference/inventory-after.json', 'reference/verification.json')]})
    print(json.dumps(verified, indent=2))

def main():
    validation = json.loads((HERE / 'validation.json').read_text())
    assert validation['status'] == 'passed'
    assert hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest() == validation['generator_sha256']
    assert hashlib.sha256((HERE / 'source.json').read_bytes()).hexdigest() == validation['source_sha256']
    native_preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT), threading.Event())
    with (ROOT / '.local/learning/requests/math/api.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        status = DB.command('status')
        assert 'lineage=' + LINEAGE in status
        durable_text(REF / 'locked-status.txt', status)
        if (REF / 'commit-intent.json').exists():
            intent = json.loads((REF / 'commit-intent.json').read_text())
            assert intent['database'] == 'math' and intent['lineage'] == LINEAGE and intent['source'] == SOURCE
            assert hashlib.sha256((REF / 'transaction.edn').read_bytes()).hexdigest() == intent['sha256']
            assert (REF / 'transaction.edn').read_text() == intent['exact_edn']
        else:
            intent = prepare(native_preview)
        receipt_path = REF / 'commit.edn'
        if receipt_path.exists() and loads(receipt_path.read_text()).get(':edb/committed') is True:
            receipt = loads(receipt_path.read_text())
        else:
            # Unknown outcomes always retry the identical durable intent/key.
            receipt_text = DB.command('transact', '--file', REF / 'transaction.edn', '--endpoint', intent['endpoint'],
                '--source', SOURCE, '--request-key', intent['request_key'], '--basis', intent['basis'], '--timeout-ms', 55000)
            durable_text(receipt_path, receipt_text)
            receipt = loads(receipt_text)
        verify(receipt, intent)

if __name__ == '__main__':
    main()
