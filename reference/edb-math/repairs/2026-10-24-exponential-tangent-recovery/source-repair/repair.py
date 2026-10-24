"""Guarded distractor repair for the unserved original q-107463.

Preserve its question, correct answer, solution, difficulty and identities.
All five candidate lines pass through the stated point; differentiation chooses
the unique tangent. No original source question is retired or deleted.
"""
import copy
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / 'scripts'))
from generator_publish import Publisher, GeneratorCommitter, jsonable, kw, digest, file_lock, normalized_question
from inventory_jobs import save

KP, QUESTION, FIELD, CORRECT = 17592186092261, 17592186524997, 17592186524890, 17592186524441
L = '\\operatorname{ln}\u2061(2)'
VALUES = {
    17592186524506: 'y=2'+L+r'\,x+2'+L+r'+\frac{1}{4}',
    17592186524605: 'y=-'+L+r'\,x-'+L+r'+\frac{1}{4}',
    17592186524650: 'y=-2'+L+r'\,x-2'+L+r'+\frac{1}{4}',
    17592186524774: r'y=\frac{1}{2}'+L+r'\,x+\frac{1}{2}'+L+r'+\frac{1}{4}',
}
OLD = json.loads((HERE / 'before.json').read_text())['question']


def candidate(question):
    assert question == OLD, 'Source changed since review; do not overwrite'
    q = copy.deepcopy(question)
    field, = q[':question/answer-fields']
    assert field[':db/id'] == FIELD and field[':answer-field/correct'][':db/id'] == CORRECT
    for answer in field[':answer-field/choices']:
        if answer[':db/id'] in VALUES:
            answer[':answer/value'] = VALUES[answer[':db/id']]
    return q


def prepare():
    from fractions import Fraction
    proposed = candidate(OLD)
    # Each displayed candidate is y = r*ln(2)*(x+1)+1/4. Only r=1
    # matches d/dx[4^(2x+1)] at x=-1: 2*4^(-1)*ln(4)=ln(2).
    slopes = {CORRECT: Fraction(1), 17592186524506: Fraction(2),
              17592186524605: Fraction(-1), 17592186524650: Fraction(-2),
              17592186524774: Fraction(1, 2)}
    assert len(set(slopes.values())) == 5
    save(HERE / 'candidate.json', proposed)
    save(HERE / 'math-verification.json', {'passed': True,
        'point': [-1, '1/4'], 'derivative': '2*4^(-1)*ln(4)=ln(2)',
        'slopes_in_units_of_ln2': {str(k): str(v) for k, v in slopes.items()},
        'all_five_pass_point': True, 'unique_tangent': CORRECT,
        'same_bank_alternative_prompts': ['y=4^x at x=-1 (slope ln(2)/2)',
                                         'y=4^(4x+3) at x=-1 (slope 2ln(2))']})
    save(HERE / 'render-input.json', [{'question': proposed}])
    graded = normalized_question(proposed)
    for field in graded[':question/answer-fields']:
        field[':answer-field/correct'] = [':answer/id', field[':answer-field/correct']]
    save(HERE / 'grader-input.json', [{'label': 'Repaired source tangent: every choice',
        'record': {'question': graded}, 'checks': [
            {'field_index': 0, 'submitted_answer_id': a[':answer/id'],
             'expected': 'accepted' if a[':db/id'] == CORRECT else 'rejected'}
            for a in proposed[':question/answer-fields'][0][':answer-field/choices']]}])
    print('Prepared four distractor edits; question, key and solution unchanged.')


def commit():
    review = json.loads((HERE / 'independent-review.json').read_text())
    assert review['accepted']
    assert review['bindings']['before_question_hash'] == digest(OLD)
    assert review['bindings']['candidate_question_hash'] == digest(candidate(OLD))
    assert json.loads((HERE / 'candidate.json').read_text()) == candidate(OLD)
    assert json.loads((HERE / 'render/rendering.json').read_text())['passed']
    grade = json.loads((HERE / 'grader-verification.json').read_text())
    assert (grade['accepted_checks'], grade['rejected_checks'], grade['documented_unresolved_checks']) == (1, 4, 0)
    pub = Publisher.from_environment(source=':agent/codex')
    committer = GeneratorCommitter(pub.config, pub.client, HERE / 'commit')
    with file_lock(Path(pub.config.request_directory) / 'api.lock'):
        request = committer.pending()
        if not request:
            status = pub.client.status()
            kp = pub.read_kp(KP, HERE / 'live', status['basis'])
            question = jsonable(next(q for q in kp[':knowledge-point/questions'] if q[':db/id'] == QUESTION))
            candidate(question)
            served = pub.client.query('[:find ?item :in $ ?q :where [?item :task-item/content ?q]]',
                                      [QUESTION], HERE / 'live', 'served-history', status['basis'])
            responses = pub.client.query('[:find ?item ?a :in $ [?a ...] :where [?item :task-item/responses ?a]]',
                                          [list(VALUES)], HERE / 'live', 'answer-history', status['basis'])
            assert not served and not responses, 'Preserve all existing learner-history content'
            attributes = pub.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]', [], HERE / 'live', 'attributes', status['basis'])
            idents = pub.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]', [], HERE / 'live', 'idents', status['basis'])
            snapshot = {'basis': status['basis'], 'lineage': status['lineage'], 'attributes': attributes, 'idents': idents}
            old = {a[':db/id']: a[':answer/value'] for a in question[':question/answer-fields'][0][':answer-field/choices']}
            batch = {'source': pub.config.source,
                'assertions': [[e, kw('answer/value'), value] for e, value in VALUES.items()],
                'retractions': [[e, kw('answer/value'), old[e]] for e in VALUES],
                'forms': [[kw('db/cas'), e, kw('answer/value'), old[e], value] for e, value in VALUES.items()]
                         + [[kw('db/ensure'), e, kw('answer/validate')] for e in VALUES]
                         + [[kw('db/ensure'), QUESTION, kw('question/validate')]]}
            committer.preview(batch, snapshot)
            request = committer.save_request(batch, snapshot, digest(batch))
        receipt = committer.submit(request)
        proof = committer.verify_receipt(request, receipt)
        basis = receipt[':edb/db-after-t']
        after = jsonable(pub.read_kp(KP, HERE / 'readback', basis))
        question = next(q for q in after[':knowledge-point/questions'] if q[':db/id'] == QUESTION)
        assert question == candidate(OLD)
        save(HERE / 'verification.json', {'committed': True, 'basis': basis,
             'exact_readback': True, 'changed_distractors': list(VALUES),
             'question_key_solution_difficulty_and_ids_preserved': True,
             'question_had_no_task_items_or_responses': True, **proof})
        print(json.dumps({'committed': True, 'basis': basis, **proof}))


if __name__ == '__main__':
    {'prepare': prepare, 'commit': commit}[sys.argv[1]]()
