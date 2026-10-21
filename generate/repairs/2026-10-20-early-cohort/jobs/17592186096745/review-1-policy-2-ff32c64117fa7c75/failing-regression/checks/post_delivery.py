"""Visible-record coverage, shortcut probes and one native-grader input batch."""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from review_math import check, correct_index, prompt

E = ROOT / 'evidence'


def load(name):
    return json.loads((E / name).read_text())


def save(name, value):
    (E / name).write_text(json.dumps(value, indent=2, default=str) + '\n')


def family(record):
    return 'vector' if 'and then solve' in record['question'][':question/problem'] else 'matrix'


def visible_signature(record):
    q = record['question']
    return (q[':question/problem'], correct_index(q),
            tuple((a[':answer/type'], a[':answer/value'])
                  for a in q[':question/answer-fields'][0][':answer-field/choices']))


def probes(records):
    groups = {}
    for record in records:
        name = record['generation']['template']
        group = groups.setdefault(name, {'records': 0, 'family': family(record), 'slots': Counter(),
                                          'first': 0, 'last': 0, 'shortest': 0, 'longest': 0,
                                          'fewest_minus_signs': 0, 'most_minus_signs': 0})
        q = record['question']; index = correct_index(q)
        values = [a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
        group['records'] += 1; group['slots'][index] += 1
        for name, chosen in [('first', 0), ('last', 4),
                             ('shortest', min(range(5), key=lambda i: len(values[i]))),
                             ('longest', max(range(5), key=lambda i: len(values[i]))),
                             ('fewest_minus_signs', min(range(5), key=lambda i: values[i].count('-'))),
                             ('most_minus_signs', max(range(5), key=lambda i: values[i].count('-')))]:
            group[name] += chosen == index
    return groups


def main():
    raw = load('delivery-input.json'); accepted = load('delivery/accepted.json')
    accepted_ids = {r['question'][':question/id'] for r in accepted}
    # Publication assigns content identities; compare visible content rather than
    # assuming raw generator UUIDs survive normalization.
    accepted_by_content = {visible_signature(r): r for r in accepted}
    controls = load('counterfactual-records.json')
    # Every sixth control is the irrelevant row-presentation change. Exclude it
    # when measuring balanced target-assignment tests within the fixed bank.
    targets = [r for i, r in enumerate(controls) if i % 6 != 5]
    survived = [accepted_by_content[visible_signature(r)] for r in targets
                if visible_signature(r) in accepted_by_content]
    assert len(survived) == len(targets) == 15
    before = probes(targets); after = probes(survived)
    assert before == after
    for group in after.values():
        assert set(group['slots']) == set(range(5))
        assert all(group[name] == 1 for name in ('first', 'last', 'shortest', 'longest', 'fewest_minus_signs', 'most_minus_signs'))
    normal = [r for r in raw if not r['generation']['replay'] and r not in controls]
    normal_after = [accepted_by_content[visible_signature(r)] for r in normal
                    if visible_signature(r) in accepted_by_content]
    assert len(normal_after) == len(normal) == 22
    for record in accepted:
        assert not check(record)['errors']
    summary = {
        'delivery_counts': {'input': len(raw), 'accepted': len(accepted), 'source_replay_duplicates': 17},
        'fixed_bank_target_controls_before': before, 'fixed_bank_target_controls_after': after,
        'ordinary_sample_profiles_before': probes(normal), 'ordinary_sample_profiles_after': probes(normal_after),
        'interpretation': 'Within each affected template and the retained vector template, every option-only deterministic probe scores 1/5, because the same bank is exercised with all five mathematical targets. Prompts and worked solutions change and all options are checked mathematically. This is controlled coverage, not an imposed sampling quota.',
        'limits': 'Ordinary per-profile sample counts are small and do not estimate future response frequencies or rule out every possible arithmetic shortcut. Existing unchanged profiles retain prior review evidence. Finite parameter bounds are documented.'}
    save('pedagogical-variation.json', summary)

    # Native grading expectations come from check(record)'s independently read
    # prompt/bank witness, then each keyed radio ID is tested once.
    unique = {visible_signature(r): r for r in raw + accepted}
    cases = []
    for record in unique.values():
        q = record['question']; assert not check(record)['errors']
        index = correct_index(q)
        cases.append({'label': q[':question/id'], 'record': record, 'checks': [
            {'field_index': 0, 'submitted_answer_id': a[':answer/id'],
             'expected': 'accepted' if i == index else 'rejected',
             'purpose': 'Independent visible-system RREF / affine substitution witness'}
            for i, a in enumerate(q[':question/answer-fields'][0][':answer-field/choices'])]})
    save('grader-input.json', cases)

    # Read-only support reproduction of question_selection.rs for a fresh learner,
    # all-hard pool, and positive hard weight. No future database IDs are assumed.
    pool = sorted(accepted_ids)
    selected = Counter()
    for seed in range(120):
        digest = hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest()
        uniform = (int.from_bytes(digest[8:16], 'big') >> 11) / (1 << 53)
        selected[pool[int(uniform * len(pool))]] += 1
    save('learner-selection-results.json', {
        'policy': 'engine/rust/question_selection.rs:132-216; configured positive hard weight, no history',
        'eligible_records': len(pool), 'simulated_draws': 120, 'observed_distinct': len(selected),
        'eligible_families': dict(Counter(family(r) for r in accepted)),
        'support': 'Every index in the all-hard pool remains eligible; key, signs and source profile are not read by selection.',
        'limits': 'UUID order stands in for unknown future entity order. No frequency claim for a live learner. Zero hard weight excludes this rated pool. Unconfigured policy picks smallest entity; historical exclusions can exhaust finite pools. Captured inventory has no generation metadata.'})
    print(json.dumps({'accepted': len(accepted), 'target_controls_surviving': len(survived),
                      'native_cases': len(cases), 'native_responses': sum(len(c['checks']) for c in cases),
                      'shortcut_probes': 'all six deterministic option-only probes 1/5 within each tested template'}))


if __name__ == '__main__':
    main()
