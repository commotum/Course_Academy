"""Repair only generated answer spellings, retaining identities and response meaning."""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import threading
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT))
from capture.scripts.database.preview import preview_executable
from migrate_learner_history import connection, dumps, loads, kw
sys.path.insert(0, str(ROOT / 'generate/scratch/17592186064281'))
from db_support import PATTERN, plain
spec = importlib.util.spec_from_file_location('validation', ROOT / 'generate/scratch/17592186064281/validate.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
g = v.g


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def check_datoms(report, changes):
    attributes = dict(loads((HERE / 'attributes.edn').read_text()))
    instant = attributes[kw('db/txInstant')]
    answer_value = attributes[kw('answer/value')]
    expected = collections.Counter(
        (r['entity'], value, added) for r in changes
        for value, added in [(r['before'], False), (r['after'], True)])
    datoms = report[':edb/tx-data']
    actual = collections.Counter((d[0], d[2], d[-1]) for d in datoms
                                 if d[1] != instant)
    assert actual == expected
    assert all(d[1] == answer_value for d in datoms if d[1] != instant)
    assert all(d[-2] == attributes[kw('agent/codex')] for d in datoms)
    assert len(datoms) == len(changes) * 2 + 1


def prepare():
    assert not (HERE / 'commit-intent.json').exists(), 'Recover saved submission first'
    before = loads((HERE / 'before.edn').read_text())[0][0]
    changes, questions, forms = [], [], []
    for question in before[':knowledge-point/questions']:
        match = re.search(r'\((\d+)-2x\)-6', question[':question/problem'])
        if not match or ':question/math-academy-id' in question:
            continue
        record = g.generate('moderate', 0, 'q-31163', int(match[1]))
        v.independent(record)
        new = record['question']
        assert str(question[':question/id']) == new[':question/id']
        assert question[':question/problem'] == new[':question/problem']
        assert question[':question/worked-solution'] == new[':question/worked-solution']
        field = question[':question/answer-fields'][0]
        new_field = new[':question/answer-fields'][0]
        assert str(field[':answer-field/id']) == new_field[':answer-field/id']
        assert str(field[':answer-field/correct'][':answer/id']) == new_field[':answer-field/correct'][1]
        values = {a[':answer/id']: a[':answer/value'] for a in new_field[':answer-field/choices']}
        assert set(values) == {str(a[':answer/id']) for a in field[':answer-field/choices']}
        for answer in field[':answer-field/choices']:
            old, new_value = answer[':answer/value'], values[str(answer[':answer/id'])]
            assert v.sp.simplify(v.expr(old) - v.expr(new_value)) == 0
            if old == new_value:
                continue
            changes.append({'entity': answer[':db/id'], 'question': question[':db/id'],
                            'before': old, 'after': new_value})
            forms += [[kw('db/cas'), answer[':db/id'], kw('answer/value'), old, new_value],
                      [kw('db/ensure'), answer[':db/id'], kw('answer/validate')]]
        forms += [[kw('db/ensure'), field[':db/id'], kw('answer-field/validate')],
                  [kw('db/ensure'), question[':db/id'], kw('question/validate')]]
        questions.append(question[':db/id'])
    assert questions == [17592186491432] and len(changes) == 5
    save('changes.json', changes)
    (HERE / 'transaction.edn').write_text(dumps(forms))
    db = connection()
    db.query('[:find ?ident ?e :in $ [?ident ...] :where [?e :db/ident ?ident]]',
             [[kw('db/txInstant'), kw('answer/value'), kw('agent/codex')]], HERE, 'attributes')
    executable = preview_executable(SimpleNamespace(math_root=Path('/media/jake/SSD/EDB/math'),
                                    repo_root=ROOT, preview_bin=None), threading.Event())
    preview = subprocess.run([str(executable), 'with', '--database', 'math', '--source', ':agent/codex',
                              '--file', str(HERE / 'transaction.edn')],
                             env=db.env, check=True, capture_output=True, text=True).stdout
    (HERE / 'preview.edn').write_text(preview)
    report = loads(preview)
    assert report[':edb/committed'] is False
    check_datoms(report, changes)
    save('preparation.json', {'questions': questions, 'answers': len(changes),
         'preview_basis': report[':edb/db-before-t'], 'preview_exact_diff_verified': True,
         'generator_sha256': hashlib.sha256(Path(g.__file__).read_bytes()).hexdigest()})
    print('Prepared and previewed five equivalent answer spelling changes.')


def apply():
    changes = json.loads((HERE / 'changes.json').read_text())
    prep = json.loads((HERE / 'preparation.json').read_text())
    validation = json.loads((ROOT / 'generate/scratch/17592186064281/validation.json').read_text())
    assert validation['status'] == 'pass' and validation['representation']
    assert prep['generator_sha256'] == hashlib.sha256(Path(g.__file__).read_bytes()).hexdigest()
    digest = hashlib.sha256((HERE / 'transaction.edn').read_bytes()).hexdigest()
    intent = {'database': 'math', 'source': ':agent/codex', 'endpoint': '/tmp/edb-math/writer.sock',
              'file': str(HERE / 'transaction.edn'), 'sha256': digest,
              'request_key': 'repair-trig-answer-form-2026-10-23-' + digest[:24]}
    if (HERE / 'commit-intent.json').exists():
        assert json.loads((HERE / 'commit-intent.json').read_text()) == intent
    else:
        save('commit-intent.json', intent)
    db = connection()
    if (HERE / 'receipt.edn').exists():
        report = loads((HERE / 'receipt.edn').read_text())
        assert report[':edb/committed'] is True
    else:
        # A failed observation leaves this exact saved intent available for retry.
        receipt = db.command('transact', '--source', intent['source'], '--endpoint', intent['endpoint'],
                             '--file', intent['file'], '--request-key', intent['request_key'])
        (HERE / 'receipt.edn').write_text(receipt)
        report = loads(receipt)
    assert report[':edb/committed'] is True
    check_datoms(report, changes)
    after = db.query('[:find (pull ?k ' + PATTERN + ') :in $ ?k :where [?k :knowledge-point/id _]]',
                     [g.KP_ID], HERE, 'after', report[':edb/db-after-t'])[0][0]
    expected = loads((HERE / 'before.edn').read_text())[0][0]
    values = {r['entity']: r['after'] for r in changes}
    for question in expected[':knowledge-point/questions']:
        for field in question.get(':question/answer-fields', []):
            for answer in field.get(':answer-field/choices', []) + [field.get(':answer-field/correct', {})]:
                if answer.get(':db/id') in values:
                    answer[kw('answer/value')] = values[answer[':db/id']]
    assert after == expected, 'Unexpected change in KP/question/answer ownership closure'
    save('verification.json', {'committed': True, 'basis_t': report[':edb/db-after-t'],
         'answers_repaired': len(changes), 'questions_repaired': prep['questions'],
         'exact_content_diff_verified': True, 'complete_ownership_readback_verified': True,
         'identities_correct_links_and_learner_state_preserved': True})
    print((HERE / 'verification.json').read_text())


if __name__ == '__main__':
    {'prepare': prepare, 'apply': apply}[sys.argv[1]]()
