"""Assemble the read-only checkbox audit and its manual adjudications."""
import collections
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
candidates = json.loads((OUT / 'candidates.json').read_text())
screening = json.loads((OUT / 'screening.json').read_text())
topics_by_kp = collections.defaultdict(list)
for topic in candidates['topics']:
    for kp in topic['knowledge_points']:
        topics_by_kp[kp['db/id']].append({
            k: topic[k] for k in ('db/id', 'topic/id', 'topic/math-academy-id', 'topic/title')
        })

# Numerical pairs are not subsets of independently listed cases. Conversely,
# OCR's lowercase l/ll in q-86896 still refers to the listed Roman labels.
direct = [r for r in screening['banks'] if r['ma_id'] != 'q-7598']
direct += [r for r in screening['other_review'] if r['ma_id'] == 'q-86896']
direct += screening['fieldless']
groups = collections.defaultdict(list)
for original in direct:
    row = dict(original)
    fields = row['fields']
    keys = [f[':answer-field/correct'] for f in fields
            if isinstance(f.get(':answer-field/correct'), dict)
            and f[':answer-field/correct'].get(':answer/value') is not None]
    flags = []
    if not fields:
        flags.append('no_answer_fields_reconstruct_key_from_worked_solution')
    elif not keys:
        flags.append('no_stored_correct_answer_or_worked_solution')
        assert not row['solution']
    if len(fields) > 1:
        flags.append('duplicate_selection_fields_reconcile_before_migration')
    if row['ma_id'] == 'q-86896':
        flags.append('normalize_OCR_l_and_ll_to_I_and_II')
    if '![' in row['problem']:
        flags.append('prompt_contains_image')
    row['recommendation'] = 'checkbox'
    row['current_type'] = 'radio' if fields else 'no_answer_fields'
    row['review_flags'] = flags
    row['source_snapshot'] = 'sources/' + str(row['kp']) + '.json'
    row['reason'] = 'independently_listed_cases_with_subset_response'
    groups[row['kp']].append(row)

kps = []
for eid, rows in sorted(groups.items()):
    kps.append({
        'db/id': eid, 'title': rows[0]['kp_title'], 'topics': topics_by_kp[eid],
        'radio_count': sum(r['current_type'] == 'radio' for r in rows),
        'fieldless_count': sum(r['current_type'] == 'no_answer_fields' for r in rows),
        'candidate_count': len(rows), 'questions': sorted(rows, key=lambda r: r['id']),
    })

secondary = collections.defaultdict(list)
for kp, title, eid, ma_id, prompt, values in json.loads((OUT / 'residual-review.json').read_text()):
    record = json.loads((OUT / 'sources' / (str(kp) + '.json')).read_text())
    question = next(q for q in record[':knowledge-point/questions'] if q[':db/id'] == eid)
    secondary[kp].append({
        'db/id': eid, 'ma_id': ma_id, 'title': title,
        'question': question,
        'reason': 'set_of_values_or_points_without_independently_enumerated_cases_in_prompt',
        'recommendation': 'consider_separately_requires_explicit_atomic_checkbox_options',
    })
secondary_kps = [{
    'db/id': eid, 'title': rows[0]['title'], 'topics': topics_by_kp[eid],
    'question_count': len(rows), 'questions': rows,
} for eid, rows in sorted(secondary.items())]

records = [json.loads((OUT / 'sources' / (str(eid) + '.json')).read_text())
           for eid in topics_by_kp]
questions = {q[':db/id']: q for r in records for q in r.get(':knowledge-point/questions', [])}
existing_checkbox_ids = sorted(q[':db/id'] for q in questions.values()
    if q.get(':question/answer-fields') and all(
        f.get(':answer-field/type', {}).get(':db/ident') == ':answer-field.type/checkbox'
        for f in q[':question/answer-fields']))
flat = [r for kp in kps for r in kp['questions']]
report = {
    'database': candidates['database'], 'basis': candidates['basis'],
    'cursor': candidates['cursor'], 'finder_at': candidates['at'],
    'finder_script': 'generate/scripts/find_candidates.py',
    'scope': {
        'topic_count': len(candidates['topics']), 'kp_count': len(records),
        'unique_practice_question_count': len(questions),
        'canonical_examples_excluded': True,
        'already_checkbox_question_count': len(existing_checkbox_ids),
        'already_checkbox_question_ids': existing_checkbox_ids,
    },
    'method': {
        'criterion': 'A finite list of independently assessable statements, equations, matrices, graphs, points, intervals, or vector fields; response is the subset satisfying the prompt.',
        'review': 'All practice question prompts and answer-field structures were screened at a fixed database basis. Flagged banks, fieldless prompts, and residual subset cues were reviewed semantically.',
        'limits': 'This is an answer-format audit, not independent mathematical validation of every key or inspection of embedded images. No database transactions were submitted.',
        'migration': 'Use one field per actual listed case, preserve imported entities and historical learner responses, map saved combination answers to Boolean selections, and attribute local edits to the agent. Confirm keys where missing; reconcile duplicate selection fields. Do not hardcode three Roman-labeled cases.',
    },
    'counts': {
        'direct_candidate_kps': len(kps), 'direct_candidate_questions': len(flat),
        'radio_questions': sum(kp['radio_count'] for kp in kps),
        'fieldless_questions': sum(kp['fieldless_count'] for kp in kps),
        'radio_questions_without_stored_key_or_solution': sum(
            'no_stored_correct_answer_or_worked_solution' in r['review_flags'] for r in flat),
        'questions_with_duplicate_selection_fields': sum(
            'duplicate_selection_fields_reconcile_before_migration' in r['review_flags'] for r in flat),
        'secondary_kps': len(secondary_kps),
        'secondary_questions': sum(kp['question_count'] for kp in secondary_kps),
    },
    'direct_candidates': kps, 'secondary_candidates': secondary_kps,
    'manual_adjudications': [
        {'ma_id': 'q-7598', 'decision': 'exclude', 'reason': 'Major/minor ellipse axis lengths are an ordered numerical pair, not independently listed cases.'},
        {'ma_id': 'q-86896', 'decision': 'include', 'reason': 'Combination bank with OCR l/ll representing Roman I/II.'},
        {'kp': 17592186129253, 'ma_ids': [r['ma_id'] for r in screening['other_review'] if r['ma_id'] != 'q-86896'],
         'decision': 'exclude', 'reason': 'Mutually exclusive descriptions of one root; appropriate single-answer radio classification.'},
        {'decision': 'exclude_other_bulleted_prompts', 'reason': 'Lists defining variables or curve segments do not make a single relationship or area result a subset answer.'},
    ],
}
assert report['counts']['direct_candidate_questions'] == 256
assert report['counts']['radio_questions'] == 251
assert report['counts']['fieldless_questions'] == 5
assert report['counts']['direct_candidate_kps'] == 30
assert report['counts']['secondary_questions'] == 55
assert len(questions) == 3788 and len(records) == 384
assert len({r['id'] for r in flat}) == len(flat)
(OUT / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(report['counts'], indent=2))
