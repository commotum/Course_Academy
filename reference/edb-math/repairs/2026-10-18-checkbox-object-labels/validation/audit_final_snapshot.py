"""Independently reconcile the complete final census, identities and rendered inputs."""
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASK = HERE.parent


def read(path):
    return json.loads(path.read_text())


def canon(value):
    if isinstance(value, dict):
        return {k: canon(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        return sorted((canon(v) for v in value), key=lambda v: json.dumps(v, sort_keys=True))
    return value


def protected(question):
    value = copy.deepcopy(question)
    value.pop(':question/problem', None)
    value.pop(':question/worked-solution', None)
    for field in value[':question/answer-fields']:
        field.pop(':answer-field/key', None)
    return canon(value)


def payload(q):
    ident = lambda x: x[':db/ident']
    return {'id': str(q[':db/id']), 'stage': 'after',
            'label': f"Question {q[':db/id']} (after)",
            'problem': q.get(':question/problem', ''),
            'solution': q.get(':question/worked-solution', ''),
            'fields': [{'id': f[':db/id'], 'key': f[':answer-field/key'],
                        'type': ident(f[':answer-field/type']), 'answerType': 'text',
                        'choices': [{'id': a[':db/id'], 'value': a[':answer/value'],
                                     'type': ident(a[':answer/type'])}
                                    for a in f[':answer-field/choices']]}
                       for f in sorted(q[':question/answer-fields'], key=lambda f: f[':db/id'])]}


def main():
    census = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else TASK / 'final-census'
    initial_path, final_path = TASK / 'questions.json', census / 'questions.json'
    initial = {q[':db/id']: q for q in read(initial_path)}
    final = {q[':db/id']: q for q in read(final_path)}
    added, removed = sorted(set(final) - set(initial)), sorted(set(initial) - set(final))
    protected_mismatches, saved_mismatches = [], []
    for qid in set(initial) & set(final):
        before, after = initial[qid], final[qid]
        if protected(before) != protected(after):
            protected_mismatches.append(qid)
        if canon(before.get(':task-item/_content', [])) != canon(after.get(':task-item/_content', [])):
            saved_mismatches.append(qid)
    expected = {}
    for b in sorted(read(TASK / 'confirmed-batches.json'), key=lambda b: b['basis_after']):
        assert b['committed'] and b['passed']
        assert read(TASK / b['directory'] / 'commit-verification.json')['passed']
        for c in read(TASK / b['directory'] / 'cases.json')['cases']:
            expected[c['question']] = c['after']
    latest_value_mismatches = [qid for qid, after in expected.items()
                               if qid not in final or canon(payload(final[qid])) != canon(payload(after))]
    unchanged = sorted(set(initial) - set(expected))
    unchanged_mismatches = [qid for qid in unchanged if canon(initial[qid]) != canon(final.get(qid))]
    render_audit = read(HERE / 'final-visible-choice-audit.json')
    render_inputs = {}
    rendered_mismatches = []
    for row in render_audit['questions']:
        d = row['render_directory']
        if d not in render_inputs:
            render_inputs[d] = {int(x['id']): x for x in read(TASK / d / 'render-cases.json')
                                if x['stage'] == 'after'}
        qid = row['question']
        if qid not in final or canon(payload(final[qid])) != canon(render_inputs[d][qid]):
            rendered_mismatches.append(qid)
    render_coverage_missing = sorted(set(final) - {x['question'] for x in render_audit['questions']})
    result = {
        'passed': not (added or removed or protected_mismatches or saved_mismatches
                       or latest_value_mismatches or unchanged_mismatches
                       or rendered_mismatches or render_coverage_missing),
        'database_writes': 0,
        'basis': read(census / 'audit-summary.json')['basis'],
        'census_directory': str(census.relative_to(TASK)),
        'initial_sha256': hashlib.sha256(initial_path.read_bytes()).hexdigest(),
        'final_sha256': hashlib.sha256(final_path.read_bytes()).hexdigest(),
        'questions': len(final),
        'fields': sum(len(q[':question/answer-fields']) for q in final.values()),
        'choice_entities': sum(len(f[':answer-field/choices']) for q in final.values()
                               for f in q[':question/answer-fields']),
        'questions_with_saved_uses': sum(bool(q.get(':task-item/_content')) for q in final.values()),
        'saved_items': sum(len(q.get(':task-item/_content', [])) for q in final.values()),
        'repaired_questions': len(expected),
        'unchanged_questions': len(unchanged),
        'identity_bank_correct_reference_and_metadata_mismatches': protected_mismatches,
        'saved_item_state_or_response_mismatches': saved_mismatches,
        'latest_committed_value_mismatches': latest_value_mismatches,
        'unchanged_question_mismatches': unchanged_mismatches,
        'rendered_payload_mismatches': rendered_mismatches,
        'render_coverage_missing': render_coverage_missing,
        'new_questions': added,
        'missing_questions': removed,
        'protected_scope': 'Every original pulled attribute remains exactly equal, with unordered relationships canonicalized, except question problem/worked-solution and answer-field key. Full question/field/answer UUIDs, entity IDs, field types, answer values, correct refs, memberships, metadata, task-item state and saved responses are included.',
        'rendering_scope': 'Every final question problem, solution, field key, type and choice ID/value equals its selected latest actual-render input. Literal-TeX findings are reported separately in final-visible-choice-audit.json.',
        'native_grading': 'No redundant regrading: immutable field IDs, Boolean banks, correct links and saved responses exactly preserved; each confirmed repair batch already passed pinned native grading and exact committed readback.',
    }
    output = HERE / 'final-invariant-audit.json'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
