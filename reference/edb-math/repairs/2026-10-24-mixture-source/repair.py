"""Narrow, guarded repair of the mixture source question and its missing key."""
import copy
import json
from fractions import Fraction
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_publish import Publisher, GeneratorCommitter, jsonable, kw, digest, file_lock, normalized_question
from inventory_jobs import save

KP, QUESTION, FIELD, ANSWER = 17592186092285, 17592186092502, 17592186089183, 17592186089187
OLD = '$4.8$ tons and $3.2$ tons'
NEW = '$3.2$ tons and $4.8$ tons'
SOLUTION = (HERE / 'solution.md').read_text().strip()


def candidate(question):
    q = copy.deepcopy(question)
    field, = q[':question/answer-fields']
    answer = next(a for a in field[':answer-field/choices'] if a[':db/id'] == ANSWER)
    assert answer[':answer/value'] == OLD
    assert ':answer-field/correct' not in field and ':question/worked-solution' not in q
    answer[':answer/value'] = NEW
    field[':answer-field/correct'] = copy.deepcopy(answer)
    q[':question/worked-solution'] = SOLUTION
    checks = []
    for choice in field[':answer-field/choices']:
        a, b = map(Fraction, re.findall(r'\$([\d.]+)\$', choice[':answer/value']))
        valid = a + b == 8 and Fraction(55, 100)*a + Fraction(30, 100)*b == Fraction(40, 100)*8
        assert valid == (choice[':db/id'] == ANSWER)
        checks.append({'choice': choice[':db/id'], 'total': str(a+b), 'carbon': str(Fraction(55, 100)*a+Fraction(30, 100)*b), 'correct': valid})
    return q, checks


def prepare_local():
    before = json.loads((HERE / 'before.json').read_text())
    q = next(q for q in before['kp'][':knowledge-point/questions'] if q[':db/id'] == QUESTION)
    proposed, checks = candidate(q)
    save(HERE / 'candidate.json', proposed)
    save(HERE / 'math-verification.json', {'passed': True, 'checks': checks,
         'equation': '0.55x + 0.30(8-x) = 0.40*8', 'solution': ['16/5', '24/5']})
    save(HERE / 'render-input.json', [{'question': proposed}])
    grading = normalized_question(proposed)
    for f in grading[':question/answer-fields']:
        f[':answer-field/correct'] = [':answer/id', f[':answer-field/correct']]
    save(HERE / 'grader-input.json', [{'label': 'Corrected mixture source: every choice',
         'record': {'question': grading}, 'checks': [
             {'field_index': 0, 'submitted_answer_id': a[':answer/id'],
              'expected': 'accepted' if a[':db/id'] == ANSWER else 'rejected'}
             for a in proposed[':question/answer-fields'][0][':answer-field/choices']]}])
    print('Prepared corrected answer, complete solution, and all-choice checks.')


def commit():
    assert json.loads((HERE / 'render/rendering.json').read_text())['passed']
    graded = json.loads((HERE / 'grader-verification.json').read_text())
    assert graded['accepted_checks'] == 1 and graded['rejected_checks'] == 4
    assert graded['documented_unresolved_checks'] == 0
    pub = Publisher.from_environment(source=':agent/codex')
    committer = GeneratorCommitter(pub.config, pub.client, HERE / 'commit')
    with file_lock(Path(pub.config.request_directory) / 'api.lock'):
        request = committer.pending()
        if not request:
            status = pub.client.status()
            kp = pub.read_kp(KP, HERE / 'live', status['basis'])
            q = next(q for q in kp[':knowledge-point/questions'] if q[':db/id'] == QUESTION)
            candidate(jsonable(q))
            responses = pub.client.query('[:find ?item :in $ ?a :where [?item :task-item/responses ?a]]',
                                         [ANSWER], HERE / 'live', 'answer-responses', status['basis'])
            assert not responses, 'Do not change an answer referenced by learner history'
            attributes = pub.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]', [], HERE / 'live', 'attributes', status['basis'])
            idents = pub.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], HERE / 'live', 'idents', status['basis'])
            snapshot = {'basis': status['basis'], 'lineage': status['lineage'], 'attributes': attributes, 'idents': idents}
            changes = [(ANSWER, 'answer/value', OLD, NEW), (FIELD, 'answer-field/correct', None, ANSWER),
                       (QUESTION, 'question/worked-solution', None, SOLUTION)]
            batch = {'source': pub.config.source,
                'assertions': [[e, kw(a), new] for e, a, old, new in changes],
                'retractions': [[e, kw(a), old] for e, a, old, new in changes if old is not None],
                'forms': [[kw('db/cas'), e, kw(a), old, new] for e, a, old, new in changes]
                         + [[kw('db/ensure'), e, kw(spec)] for e, spec in
                            [(ANSWER, 'answer/validate'), (FIELD, 'answer-field/validate'), (QUESTION, 'question/validate')]]}
            committer.preview(batch, snapshot)
            request = committer.save_request(batch, snapshot, digest(batch))
        receipt = committer.submit(request)
        proof = committer.verify_receipt(request, receipt)
        basis = receipt[':edb/db-after-t']
        after = jsonable(pub.read_kp(KP, HERE / 'readback', basis))
        q = next(q for q in after[':knowledge-point/questions'] if q[':db/id'] == QUESTION)
        assert q == json.loads((HERE / 'candidate.json').read_text())
        save(HERE / 'after.json', {'basis': basis, 'question': q})
        save(HERE / 'verification.json', {'committed': True, 'basis': basis, 'exact_readback': True,
             'question': QUESTION, 'unchanged_question_field_answer_identities': True, **proof})
        print(json.dumps({'committed': True, 'basis': basis, 'question': QUESTION, **proof}))


if __name__ == '__main__':
    {'prepare': prepare_local, 'commit': commit}[sys.argv[1]]()
