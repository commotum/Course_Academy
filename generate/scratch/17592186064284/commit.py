#!/usr/bin/env python3
"""Serialize this KP's additive, guarded content submission and exact readback."""
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

spec = importlib.util.spec_from_file_location('trig_tangent', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
REF = HERE / 'reference'
SOURCE = ':application/ca-engine'
LINEAGE = '01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
LEARNER = '59d5cf13-351c-4114-be19-4c3bb64ee051'
SCRIPT = 'generate/scratch/17592186064284.py'
RESULT = ROOT / '.local/learning/inventory/math' / LEARNER / '48b49101f6154d3698285949a2f9bde9e7e04d5224915d4a431b6ef0e6a86061.result'
DB = Database(SimpleNamespace(edb_bin=str(ROOT / '.local/edb/capture-runtime/math-edb'), database='math'))
PATTERN = '[* {:knowledge-point/question-generator [*]} {:knowledge-point/questions ' + QUESTION_PULL + '} {:knowledge-point/canonical-example ' + QUESTION_PULL + '}]'

def save(name, value): atomic_json(REF / name, value)

def inventory(name):
    binary = Path((REF / 'learning-binary.txt').read_text())
    reply = subprocess.run([str(binary), 'math', LEARNER, '/tmp/edb-math/writer.sock'],
        input=json.dumps({'action': 'inventory'}), text=True, capture_output=True, check=True, env=DB.env, timeout=55)
    data = json.loads(reply.stdout); assert data['ok'], data
    assert data['data']['lineage'] == LINEAGE
    save(name, data['data'])
    return data['data']

def pull(basis, name):
    f = REF / 'pull.edn'; f.write_text(PATTERN)
    text = DB.command('pull', '--file', f, '--entity', g.KP_ID, '--as-of', basis)
    (REF / name).write_text(text)
    return loads(text)

def typed(v, key=None):
    if isinstance(v, dict): return {kw(k): typed(val, k) for k, val in v.items()}
    if isinstance(v, list): return [typed(val) for val in v]
    if isinstance(v, str) and v.startswith(':'): return kw(v)
    if key and key.endswith('/id'): return uuid.UUID(v)
    # UUIDs in answer lookup refs must be typed as UUID, too.
    if isinstance(v, str) and re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}', v): return uuid.UUID(v)
    return v

def verify(receipt, intent):
    before = receipt[':edb/db-before-t']; after = receipt[':edb/db-after-t']
    assert receipt[':edb/committed'] is True and before == intent['basis']
    attrs = dict(DB.attributes(REF / 'verification', before))
    source = intent['source_entity']
    allowed = {'question/id','question/problem','question/worked-solution','question/difficulty','question/answer-fields',
        'answer-field/id','answer-field/key','answer-field/type','answer-field/choices','answer-field/correct',
        'answer/id','answer/type','answer/value','knowledge-point/questions','knowledge-point/question-generator',
        'question-generator/id','question-generator/script','db/txInstant'}
    for row in receipt[':edb/tx-data']:
        assert str(attrs[row[1]])[1:] in allowed, row
        assert row[-1] is True, 'Only additive assertions are authorized'
        assert row[-2] == source, 'Wrong content contributor'
        if str(attrs[row[1]]).startswith(':knowledge-point/'):
            assert row[0] == g.KP_ID, 'Other KP mutation'
    original = loads((REF / 'before.edn').read_text())
    current = pull(after, 'readback.edn')
    old_questions = {str(q[':question/id']): q for q in original[':knowledge-point/questions']}
    new_questions = {str(q[':question/id']): q for q in current[':knowledge-point/questions']}
    assert all(new_questions[qid] == q for qid, q in old_questions.items()), 'Source question changed'
    assert original[':knowledge-point/canonical-example'] == current[':knowledge-point/canonical-example']
    selected = intent['records']
    assert set(new_questions) == set(old_questions) | {r['question'][':question/id'] for r in selected}
    registration = current[':knowledge-point/question-generator']
    assert str(registration[':question-generator/id']) == intent['generator_id']
    assert registration[':question-generator/script'] == SCRIPT
    for r in selected:
        expected = r['question']; actual = new_questions[expected[':question/id']]
        assert actual[':question/problem'] == expected[':question/problem']
        assert actual[':question/worked-solution'] == expected[':question/worked-solution']
        assert actual[':question/difficulty'][':db/ident'] == expected[':question/difficulty']
        assert ':question/math-academy-id' not in actual
        assert len(actual[':question/answer-fields']) == 1
        ef = expected[':question/answer-fields'][0]; af = actual[':question/answer-fields'][0]
        assert str(af[':answer-field/id']) == ef[':answer-field/id']
        assert af[':answer-field/key'] == ef[':answer-field/key']
        assert af[':answer-field/type'][':db/ident'] == ef[':answer-field/type']
        assert str(af[':answer-field/correct'][':answer/id']) == ef[':answer-field/correct'][1]
        assert len(af[':answer-field/choices']) == 1
        ea = ef[':answer-field/choices'][0]; aa = af[':answer-field/choices'][0]
        assert str(aa[':answer/id']) == ea[':answer/id'] and aa[':answer/value'] == ea[':answer/value']
        assert aa[':answer/type'][':db/ident'] == ea[':answer/type']
    inv = inventory('inventory-after.json')
    shortages = [j for j in inv['jobs'] if j['knowledgePoint'] == g.KP_ID]
    hard = [j for j in shortages if j['difficulty'] == 'hard']
    assert not hard, 'Hard inventory shortage remains'
    verified = {'committed': True, 'basis_before': before, 'basis_after': after, 'verified_commit_basis': after,
        'request_key': intent['request_key'], 'source': SOURCE, 'generator_id': intent['generator_id'], 'generator_path': SCRIPT,
        'questions_added': len(selected), 'hard_available_at_least': 5, 'learner_and_engine_facts_changed': False,
        'source_questions_and_canonical_example_preserved': True, 'remaining_supported_jobs': shortages,
        'repeat_preparation_content_changes': 0, 'exact_readback_verified': True}
    save('verification.json', verified)
    outcome = {'outcome': 'generated', 'knowledgePoint': g.KP_ID, 'topic': 17592186050789, 'database': 'math', 'lineage': LINEAGE,
        'generator_path': SCRIPT, 'generator_id': intent['generator_id'], 'verified_commit_basis': after, 'commit_basis_before': before,
        'generated': {'hard': len(selected), 'easy': 0, 'moderate': 0}, 'hard_available_at_least': 5,
        'capability_exceptions': [
            {'difficulty': 'easy', 'status': 'unclassified', 'available': 0, 'potential_minimum_shortage': 5,
             'filled': False, 'reason': 'No easy source template or certified easy generator; absence does not prove impossibility'},
            {'difficulty': 'moderate', 'status': 'existing_inventory_sufficient', 'generator_supported': False,
             'reason': 'Bounded package certifies hard only; classified moderate source banks require implementation/replay if future inventory needs them'},
            {'difficulty': 'hard', 'finite_variant_limit': 54, 'source_variant_not_imported': 1, 'filled': True,
             'reason': 'Bounded coefficient/phase domain; no seed or identity variants'}],
        'evidence': [str((HERE / n).relative_to(ROOT)) for n in ('classification.json','classification.md','validation.json','review.md',
            'reference/commit-intent.json','reference/transaction.edn','reference/preview.edn','reference/commit.edn','reference/readback.edn','reference/verification.json')],
        'remaining_incomplete_sources': ['q-31356','q-48644','q-72163','q-72170'],
        'preserved_source_questions_and_history': True}
    atomic_json(RESULT, outcome)
    print(json.dumps(verified, indent=2))

def main():
    validation = json.loads((HERE / 'validation.json').read_text())
    assert validation['status'] == 'passed'
    assert hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest() == validation['generator_sha256']
    native_preview = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'), repo_root=ROOT), threading.Event())
    lockpath = ROOT / '.local/learning/requests/math/api.lock'
    with lockpath.open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        status = DB.command('status'); assert 'lineage=' + LINEAGE in status
        (REF / 'locked-status.txt').write_text(status)
        intent_path = REF / 'commit-intent.json'; txpath = REF / 'transaction.edn'
        if intent_path.exists():
            intent = json.loads(intent_path.read_text())
            assert intent['lineage'] == LINEAGE and intent['database'] == 'math' and intent['source'] == SOURCE
            assert hashlib.sha256(txpath.read_bytes()).hexdigest() == intent['sha256']
        else:
            inv = inventory('inventory-locked-before.json'); basis = inv['basis']
            assert DB.basis() == basis, 'Fresh inventory basis required'
            original = pull(basis, 'before.edn')
            jobs = [j for j in inv['jobs'] if j['knowledgePoint'] == g.KP_ID and j['difficulty'] == 'hard']
            assert len(jobs) == 1 and jobs[0]['missing'] > 0, 'No hard replenishment required; reprepare without content'
            source = DB.query('[:find ?s :in $ ?ident :where [?s :db/ident ?ident]]', [kw(SOURCE)], REF, 'contributor', basis)
            assert len(source) == 1
            generator = original.get(':knowledge-point/question-generator')
            generator_id = str(generator[':question-generator/id']) if generator else g.GENERATOR_ID
            if generator: assert generator.get(':question-generator/script') in (None, SCRIPT), 'Existing generator needs reuse/reconciliation'
            existing = {str(q[':question/id']) for q in original[':knowledge-point/questions']}
            prompts = {q[':question/problem'] for q in original[':knowledge-point/questions']}
            records = json.loads((HERE / 'generated.json').read_text())
            selected = [r for r in records if r['question'][':question/id'] not in existing and r['question'][':question/problem'] not in prompts][:jobs[0]['missing']]
            assert len(selected) == jobs[0]['missing'], 'Finite batch insufficient; do not duplicate'
            forms = []
            for r in selected:
                q = r['question']; authored = typed(q)
                qref = 'q-' + q[':question/id']; authored[kw('db/id')] = qref
                for f, tf in zip(q[':question/answer-fields'], authored[kw('question/answer-fields')]):
                    tf[kw('db/id')] = 'f-' + f[':answer-field/id']
                    for a, ta in zip(f[':answer-field/choices'], tf[kw('answer-field/choices')]):
                        ta[kw('db/id')] = 'a-' + a[':answer/id']
                    tf[kw('answer-field/correct')] = 'a-' + f[':answer-field/correct'][1]
                forms.append(authored)
                forms += [[kw('db/add'), g.KP_ID, kw('knowledge-point/questions'), qref], [kw('db/ensure'), qref, kw('question/validate')]]
                for f in q[':question/answer-fields']:
                    forms.append([kw('db/ensure'), 'f-' + f[':answer-field/id'], kw('answer-field/validate')])
                    for a in f[':answer-field/choices']:
                        forms.append([kw('db/ensure'), 'a-' + a[':answer/id'], kw('answer/validate')])
            forms += [{kw('db/id'): 'generator', kw('question-generator/id'): uuid.UUID(generator_id), kw('question-generator/script'): SCRIPT},
                [kw('db/add'), g.KP_ID, kw('knowledge-point/question-generator'), 'generator'],
                [kw('db/ensure'), g.KP_ID, kw('knowledge-point/validate')]]
            txpath.write_text(dumps(forms) + '\n')
            sha = hashlib.sha256(txpath.read_bytes()).hexdigest()
            save('preparation.json', {'basis': basis, 'lineage': LINEAGE, 'source': SOURCE, 'sha256': sha,
                'generator_id': generator_id, 'records': selected, 'identity_reuse': 'existing generator UUID reused if registered; otherwise deterministic KP-scoped UUID',
                'plots': [], 'duplicate_existing_content': 0, 'validation': str(HERE / 'validation.json')})
            preview = subprocess.run([str(native_preview), 'with', '--database', 'math', '--file', str(txpath), '--source', SOURCE],
                env=DB.env, check=True, text=True, capture_output=True, timeout=55)
            (REF / 'preview.edn').write_text(preview.stdout)
            assert loads(preview.stdout)[':edb/db-before-t'] == basis
            intent = {'database': 'math', 'endpoint': '/tmp/edb-math/writer.sock', 'lineage': LINEAGE, 'basis': basis,
                'sha256': sha, 'exact_edn': txpath.read_text(), 'source': SOURCE, 'source_entity': source[0][0],
                'request_key': 'ca-kp-17592186064284-' + str(basis) + '-' + sha, 'generator_id': generator_id, 'records': selected}
            save('commit-intent.json', intent)
        receiptpath = REF / 'commit.edn'
        if receiptpath.exists() and loads(receiptpath.read_text()).get(':edb/committed') is True:
            receipt = loads(receiptpath.read_text())
        else:
            text = DB.command('transact', '--file', txpath, '--endpoint', intent['endpoint'], '--source', intent['source'],
                '--request-key', intent['request_key'], '--basis', intent['basis'], '--timeout-ms', 55000)
            receiptpath.write_text(text); receipt = loads(text)
        verify(receipt, intent)

if __name__ == '__main__': main()
