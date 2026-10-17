"""Classify captured questions and map every old option without writing to EDB."""
import collections
import hashlib
import json
import re
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def subset(value, width):
    if value.lower().startswith('all the columns'):
        return list(range(1, width + 1))
    if value.lower() in ('none', 'none of the columns'):
        return []
    selected = [int(n) for n in re.findall(r'\$(\d+)\$(?:st|nd|rd|th)', value)]
    rest = re.sub(r'\$\d+\$(?:st|nd|rd|th)', '', value)
    rest = re.sub(r'\b(?:and|only)\b|[\s,]', '', rest)
    assert not rest and selected, value
    assert len(selected) == len(set(selected)) and set(selected) <= set(range(1, width + 1)), value
    return sorted(selected)


def main():
    s = json.loads((HERE / 'snapshot.json').read_text())
    incoming = json.loads((HERE / 'incoming-references.json').read_text())
    topic = s['scope'][0][0]
    kp_info = {kp[':db/id']: kp for kp in topic[':topic/knowledge-points']}
    items_by_question = collections.defaultdict(list)
    incoming_by_target = collections.defaultdict(list)
    sources = collections.defaultdict(list)
    for qid, item in s['items']:
        items_by_question[qid].append(item)
    for entity, attribute, target, ident in incoming:
        incoming_by_target[target].append({'entity': entity, 'attribute': ident[':db/ident']})
    for qid, tx, source in s['question_sources']:
        sources[qid].append({'transaction': tx, 'contributor': source})
    ledger = []
    for [q] in sorted(s['questions'], key=lambda row: row[0][':db/id']):
        eid = q[':db/id']
        prompt = q[':question/problem']
        bodies = re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', prompt, re.S)
        assert len(bodies) == 1
        matrix = sp.Matrix([[sp.Rational(x.strip()) for x in row.split('&')]
                            for row in bodies[0].split(r'\\')])
        rref, pivots_zero_based = matrix.rref()
        pivots = [col + 1 for col in pivots_zero_based]
        universe = list(range(1, matrix.cols + 1))
        count_task = 'number of pivot columns' in prompt.lower()
        non_pivot = 'non**-pivot' in prompt.lower() or 'non-pivot' in prompt.lower()
        expected = len(pivots) if count_task else [col for col in universe if col not in pivots] if non_pivot else pivots
        practice_kps = [kp[':db/id'] for kp in q.get(':knowledge-point/_questions', [])]
        canonical_kps = [kp[':db/id'] for kp in q.get(':knowledge-point/_canonical-example', [])]
        fields = q.get(':question/answer-fields', [])
        row = {'question_eid': eid, 'math_academy_id': q.get(':question/math-academy-id'),
               'kp_ids': practice_kps or canonical_kps, 'topic_ids': [topic[':db/id']],
               'canonical_memberships': canonical_kps, 'practice': bool(practice_kps),
               'basis': s['basis'], 'lineage': s['lineage'], 'source_snapshot': 'snapshot.json',
               'provenance': sources[eid], 'problem': prompt,
               'difficulty': q.get(':question/difficulty', {}).get(':db/ident'),
               'worked_solution_present': bool(q.get(':question/worked-solution')),
               'worked_solution_sha256': hashlib.sha256(q.get(':question/worked-solution', '').encode()).hexdigest(),
               'matrix': [[str(matrix[i, j]) for j in range(matrix.cols)] for i in range(matrix.rows)],
               'rref': [[str(rref[i, j]) for j in range(rref.cols)] for i in range(rref.rows)],
               'pivot_columns': pivots, 'rank': len(pivots), 'computed_answer': expected,
               'response_meaning': 'count' if count_task else 'non_pivot_subset' if non_pivot else 'pivot_subset',
               'field_ids': [f[':db/id'] for f in fields], 'choice_mapping': [],
               'incoming_question_references': incoming_by_target[eid], 'learner_uses': [], 'blockers': []}
        if not practice_kps:
            assert canonical_kps and not fields
            row.update(decision='retain_canonical_example', strong_candidate=False,
                       reason='Worked example with no answer fields; no radio response to convert.',
                       subset_semantics=not count_task, database_key_verified=None)
        else:
            assert len(fields) == 1 and row['difficulty'] and row['worked_solution_present']
            f = fields[0]
            assert f[':answer-field/type'][':db/ident'] == ':answer-field.type/radio'
            assert [ref['entity'] for ref in incoming_by_target[f[':db/id']]
                    if ref['attribute'] == ':question/answer-fields'] == [eid]
            correct = f[':answer-field/correct']
            answers = f[':answer-field/choices']
            assert correct[':db/id'] in {a[':db/id'] for a in answers}
            answer_map = {}
            for answer in answers:
                value = answer[':answer/value']
                decoded = int(value) if count_task else subset(value, matrix.cols)
                assert not answer.get(':answer/feedback')
                owners = [ref['entity'] for ref in incoming_by_target[answer[':db/id']]
                          if ref['attribute'] == ':answer-field/choices']
                assert owners == [f[':db/id']]
                answer_map[answer[':db/id']] = decoded
                row['choice_mapping'].append({'old_answer_eid': answer[':db/id'], 'old_value': value,
                                               'count' if count_task else 'selected_columns': decoded})
            assert len({json.dumps(v) for v in answer_map.values()}) == len(answers)
            assert answer_map[correct[':db/id']] == expected, (eid, correct, expected)
            row.update(database_key_verified=True, database_correct_answer_eid=correct[':db/id'],
                       database_correct_value=correct[':answer/value'],
                       strong_candidate=not count_task,
                       decision='retain_radio' if count_task else 'convert',
                       reason='One numerical count is a mutually exclusive answer, not a subset.' if count_task else
                              'Every matrix column is an independently selectable object; all five radio answers decode unambiguously to subsets.',
                       metadata_mapping_issues=False, shared_field_or_answer_ownership=False)
            if not count_task:
                row['universe'] = [{'column': col, 'label': f'Column {col}', 'correct': col in expected} for col in universe]
                row['recommended_prompt_addition'] = 'Select all that apply.'
            for item in items_by_question[eid]:
                responses = item.get(':task-item/responses', [])
                assert len(responses) <= 1
                mapped = answer_map[responses[0][':db/id']] if responses else None
                row['learner_uses'].append({'task_item_eid': item[':db/id'],
                    'status': item.get(':task-item/status', {}).get(':db/ident'),
                    'old_answer_eids': [r[':db/id'] for r in responses],
                    'mapped_count' if count_task else 'mapped_selected_columns': mapped,
                    'learner_state_must_be_preserved': True})
        if canonical_kps:
            row['learner_uses'] = [{'task_item_eid': item[':db/id'],
                                   'status': item.get(':task-item/status', {}).get(':db/ident'),
                                   'old_answer_eids': [r[':db/id'] for r in item.get(':task-item/responses', [])]}
                                  for item in items_by_question[eid]]
        ledger.append(row)
    assert len(ledger) == 68
    counts = dict(collections.Counter(row['decision'] for row in ledger))
    summary = {'database': s['database'], 'lineage': s['lineage'], 'basis': s['basis'],
               'requested_entity': s['requested_entity'], 'topic_eid': topic[':db/id'],
               'topic_title': topic[':topic/title'], 'questions': len(ledger),
               'practice_questions': sum(row['practice'] for row in ledger), 'decision_counts': counts,
               'candidate_ids': [row['question_eid'] for row in ledger if row['strong_candidate']],
               'all_practice_keys_verified': all(row['database_key_verified'] for row in ledger if row['practice']),
               'candidate_options_mapped': sum(len(row['choice_mapping']) for row in ledger if row['strong_candidate']),
               'candidate_learner_responses': sum(len(row['learner_uses']) for row in ledger if row['strong_candidate']),
               'candidate_checkbox_fields': sum(len(row.get('universe', [])) for row in ledger if row['strong_candidate']),
               'knowledge_points': [], 'database_writes': 0, 'generator_source_edits': 0,
               'stage': 'candidate_audit', 'transactions_prepared': False, 'committed_ids': [],
               'snapshot_sha256': hashlib.sha256((HERE / 'snapshot.json').read_bytes()).hexdigest()}
    for kpid, kp in kp_info.items():
        rows = [row for row in ledger if kpid in row['kp_ids']]
        summary['knowledge_points'].append({'id': kpid, 'title': kp[':knowledge-point/title'],
            'practice_questions': sum(row['practice'] for row in rows),
            'candidates': sum(row['strong_candidate'] for row in rows),
            'canonical_examples': sum(bool(row['canonical_memberships']) for row in rows),
            'generator': kp.get(':knowledge-point/question-generator')})
    independent = json.loads((HERE / 'independent-review.json').read_text())
    assert independent['basis'] == summary['basis']
    assert independent['source_sha256'] == summary['snapshot_sha256']
    reviewed = {row['question_eid']: row for row in independent['questions']}
    assert set(reviewed) == {row['question_eid'] for row in ledger}
    for row in ledger:
        other = reviewed[row['question_eid']]
        assert row['strong_candidate'] == other['strong_checkbox_candidate']
        assert row['computed_answer'] == other['mathematical_answer']
        assert other['solution_answer_matches_exact_math']
        row['solution_conclusion_verified'] = True
        row['separate_solution_issues'] = other['separate_solution_issues']
    generators = json.loads((HERE / 'generator-audit.json').read_text())
    assert generators['basis'] == summary['basis'] and generators['snapshot_sha256'] == summary['snapshot_sha256']
    assert generators['all_independent_key_checks_passed']
    assert {g['kp_id'] for g in generators['generators']} == set(kp_info)
    for generator in generators['generators']:
        if generator['registration']:
            path = Path(generator['registration'][':question-generator/script'])
            assert hashlib.sha256(path.read_bytes()).hexdigest() == generator['script_sha256']
    summary.update(stage='audit_complete', independent_review_verified=True,
                   generator_decisions=generators['decision_counts'], generator_outputs_checked=generators['sample_count'],
                   separate_solution_issue_question_ids=independent['summary']['separate_solution_issue_question_ids'],
                   evidence=['snapshot.json', 'ledger.json', 'independent-review.json', 'generator-audit.json',
                             'incoming-references.json', 'all-kp-topic-memberships.json'],
                   conversion_blockers=[], next_action='Convert the 47 strong candidates and update the two subset generators if requested.')
    save('ledger.json', ledger)
    save('audit-summary.json', summary)
    text = [f"{topic[':topic/title']} — radio-to-checkbox candidate audit", f"Database basis {s['basis']}; read-only.", '',
            'All 64 practice keys checked using exact rational row reduction.',
            '47 strong candidates; 17 count questions retain radio; 4 fieldless worked examples remain examples.',
            'Full per-option and saved-response mappings: ledger.json', '']
    for kpid, kp in kp_info.items():
        text += [f"KP {kpid}: {kp[':knowledge-point/title']}", 'Question entity | Source ID | Decision | Correct columns/count']
        for row in ledger:
            if kpid in row['kp_ids']:
                text.append(f"{row['question_eid']} | {row['math_academy_id']} | {row['decision']} | {row['computed_answer']}")
        text.append('')
    text += ['Generator audit (240 local outputs checked; no source edits)', '']
    for generator in generators['generators']:
        text.append(f"{generator['kp_id']} | {generator['decision']} | {generator['reason']}")
    text += ['', 'Separate worked-solution issues (no content changes made)', '']
    for row in ledger:
        if row['separate_solution_issues']:
            text.append(f"{row['question_eid']} ({row['math_academy_id']}): {json.dumps(row['separate_solution_issues'])}")
    (HERE / 'question-audit.txt').write_text('\n'.join(text) + '\n')
    print(json.dumps({k: summary[k] for k in ('basis', 'questions', 'practice_questions', 'decision_counts',
          'all_practice_keys_verified', 'candidate_options_mapped', 'candidate_learner_responses', 'candidate_checkbox_fields')}, indent=2))


if __name__ == '__main__':
    main()
