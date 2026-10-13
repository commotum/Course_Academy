"""Independent read-only review of augmented REF interpretation and q-31919."""
import hashlib
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SNAPSHOT = BASE / 'snapshot.json'
snapshot = json.loads(SNAPSHOT.read_text())
current = {row[0][':db/id']: row[0] for row in snapshot['questions']}
review = json.loads((BASE / 'reviews/text-cases.json').read_text())


def ref(rows):
    leading = [next((i + 1 for i, entry in enumerate(row) if entry), None) for row in rows]
    previous = 0
    zero_seen = False
    issues = []
    for i, column in enumerate(leading, 1):
        if column is None:
            zero_seen = True
        else:
            if zero_seen:
                issues.append(f'Nonzero row {i} follows a zero row.')
            if column <= previous:
                issues.append(f'Row {i} leading column {column} is not right of preceding leading column {previous}.')
            previous = column
    return {'is_ref': not issues, 'leading_columns': leading, 'issues': issues}


questions = []
for record in review['questions']:
    if 'augmented matrices' not in record['source_problem']:
        continue
    source = current[record['id']]
    problem = source[':question/problem']
    solution = source[':question/worked-solution']
    negative = '**not**' in problem
    objects = []
    for option in record['atomic_options']:
        body = re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', option['text'])[1]
        matrix = [[int(entry.strip()) for entry in row.split('&')] for row in body.split('\\\\')]
        full = ref(matrix)
        coefficient = ref([row[:-1] for row in matrix])
        objects.append({'label': option['label'], 'rows': matrix,
                        'full_augmented_matrix': full, 'coefficient_matrix': coefficient,
                        'selected_under_stored_predicate': not coefficient['is_ref'] if negative else coefficient['is_ref']})
    coefficient_labels = [obj['label'] for obj in objects if obj['selected_under_stored_predicate']]
    full_labels = [obj['label'] for obj in objects if (not obj['full_augmented_matrix']['is_ref'] if negative else obj['full_augmented_matrix']['is_ref'])]
    assert coefficient_labels == record['correct_labels']
    assert 'coefficient matrix' in solution
    necessary = coefficient_labels != full_labels
    first = ('Which of the following augmented matrices have coefficient matrices that are **not** in row echelon form?'
             if negative else 'Which of the following augmented matrices have coefficient matrices in row echelon form?')
    first += ' Treat the final column of each augmented matrix as its constants column.'
    clarified = first + problem[problem.index('\n\n'):] if necessary else problem
    prompt = clarified + '\n\nSelect all that apply.'
    questions.append({
        'id': record['id'], 'ma_id': record['ma_id'], 'decision': 'convert',
        'classification': 'finite_named_matrices', 'source_problem': problem,
        'proposed_prompt': prompt, 'correct_labels': coefficient_labels,
        'atomic_options': record['atomic_options'], 'choice_mapping': record['choice_mapping'],
        'conventional_full_matrix_correct_labels': full_labels, 'matrix_verification': objects,
        'necessary_prompt_clarification': necessary,
        'reason': 'Stored solution explicitly tests coefficient matrix REF. Exact independent computation agrees with the stored key. '
                  + ('Full augmented matrix REF gives a different subset, requiring an explicit coefficient-matrix question.' if necessary
                     else 'Both interpretations give the same subset; optional clarification omitted.'),
        'prompt_repair': {'before': problem, 'after': clarified,
                          'reason': 'Clarify the explicitly solution-supported coefficient-block predicate and preserve the existing key.'} if necessary else None,
        'content_repairs': [], 'key_evidence': {'kind': 'existing_database_key',
            'answer_eid': source[':question/answer-fields'][0][':answer-field/correct'][':db/id'],
            'value': source[':question/answer-fields'][0][':answer-field/correct'][':answer/value'],
            'solution': solution, 'coefficient_block_key_agreement': True},
    })

record = next(q for q in review['questions'] if q['ma_id'] == 'q-31919')
source = current[record['id']]
problem = source[':question/problem']
questions.append({**record, 'decision': 'convert',
    'classification': 'finite_independently_testable_statement_completions',
    'source_problem': problem, 'proposed_prompt': problem + '\n\nSelect all that apply.',
    'reason': 'The finite list supplies three independently testable completions. II (not invertible) and III (singular) are equivalent predicates for square matrices and can both apply. They are not mutually exclusive. Under det(A)!=0 only I applies, which remains checkbox-eligible and matches determinant/singularity statement migrations.',
    'atomic_options': [
        {'label': 'I', 'text': 'invertible', 'truth': True,
         'proof': 'For A=[[a,b],[c,d]], det(A)=ad-bc!=0 gives inverse (1/det(A))*[[d,-b],[-c,a]], so invertibility always follows.'},
        {'label': 'II', 'text': '**not ** invertible', 'truth': False,
         'proof': 'The explicit inverse exists under the stated nonzero determinant hypothesis, so not invertible is false.'},
        {'label': 'III', 'text': 'singular', 'truth': False,
         'proof': 'Singular means not invertible for a square matrix. The hypothesis implies invertibility, so singular is false. A matrix with zero determinant would satisfy both II and III, proving those options are not mutually exclusive.'}],
    'prompt_repair': None, 'content_repairs': [],
})

snapshot_hash = hashlib.sha256(SNAPSHOT.read_bytes()).hexdigest()
for question in questions:
    question['basis'] = snapshot['basis']
    question['source_problem_sha256'] = hashlib.sha256(question['source_problem'].encode()).hexdigest()
    question['evidence'] = [{'path': str(SNAPSHOT), 'sha256': snapshot_hash}]
    # Matrix byte content and original predicate polarity must survive each clarification.
    if question['classification'] == 'finite_named_matrices':
        assert question['proposed_prompt'][question['proposed_prompt'].index('\n\n'):].startswith(question['source_problem'][question['source_problem'].index('\n\n'):])
        assert ('**not**' in question['source_problem']) == ('**not**' in question['proposed_prompt'])

result = {
    'state': 'independent_semantic_audit_complete', 'basis': snapshot['basis'], 'lineage': snapshot['lineage'],
    'counts': {'augmented_matrix_questions': 11, 'necessary_augmented_prompt_clarifications': 3,
               'optional_augmented_clarifications_omitted': 8, 'retained_radio_reclassified_convert': 1,
               'database_writes': 0},
    'conclusions': {
        'augmented_matrix_definition': 'Conventional REF applies to the entire matrix, including an augmented final column. The source explicitly applies REF to the coefficient block. Existing keys confirm that intended operation in the three distinguishing cases. Explicitly ask about coefficient matrices in those cases rather than silently changing the stored key.',
        'necessary_clarification_ids': ['q-42028', 'q-72574', 'q-72575'],
        'q_31919': 'Convert: finite completions; II and III are equivalent rather than mutually exclusive.'},
    'definition_sources': [{'title': 'University of Nebraska–Lincoln, Row Echelon Forms, Definition 1.2.2',
        'url': 'https://mathbooks.unl.edu/LinearAlgebra/Section-Row-Echelon-Forms.html',
        'support': 'REF requires rightward leading entries and zero rows below nonzero rows; it applies to augmented and coefficient matrices separately.'}],
    'questions': questions,
    'overlays': [question for question in questions if question.get('necessary_prompt_clarification') or question['ma_id'] == 'q-31919'],
}
assert len(result['overlays']) == 4
(BASE / 'reviews/independent-semantic-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result['counts']))
