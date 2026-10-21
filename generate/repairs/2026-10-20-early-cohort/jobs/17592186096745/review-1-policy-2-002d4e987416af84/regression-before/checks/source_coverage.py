"""Regression cc3b2fd1aa8232988d0e: externally anchored source completeness.

No writes to runtime files; no services. Reuses the reviewer's visible-record
parser and independent rank/solution checks, not generator math helpers.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generator as g
from review_math import check, correct_index, prompt, semantic


def save(name, value):
    (ROOT / 'evidence' / name).write_text(json.dumps(value, indent=2, default=str) + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=ROOT.parent / 'source/source.json')
    args = parser.parse_args()
    supplied = json.loads(args.source.read_text())
    expected = supplied['material']['kp'][':knowledge-point/questions']
    by_profile = {q[':question/math-academy-id']: q for q in expected}
    assert len(by_profile) == len(expected), 'Duplicate source profile IDs'
    actual = g.sources()
    missing = sorted(set(by_profile) - set(actual))
    extra = sorted(set(actual) - set(by_profile))
    report = {'source': str(args.source), 'expected_count': len(expected),
              'missing': missing, 'extra': extra, 'profiles': []}
    save('source-coverage-results.json', report)
    assert not missing and not extra, f'Registry differs: missing={missing}, extra={extra}'
    assert {q[':question/id'] for q in actual.values()} == {q[':question/id'] for q in expected}
    assert set(g.PROFILES) == set(by_profile) and len(g.PROFILES) == len(by_profile)
    records = []
    for i, (profile, source) in enumerate(by_profile.items()):
        replay = g.generate(template=profile, seed=96745, replay=True)
        sampled = g.generate(template=profile, seed=718993 + i)
        records += [replay, sampled]
        q = replay['question']
        original = source[':question/answer-fields'][0]
        field = q[':question/answer-fields'][0]
        expected_bank = [(a[':answer/type'][':db/ident'], semantic(a[':answer/value']))
                         for a in original[':answer-field/choices']]
        bank = [(a[':answer/type'], semantic(a[':answer/value']))
                for a in field[':answer-field/choices']]
        # Exact ordered full bank equality is stronger than unordered matching.
        assert bank == expected_bank, f'{profile}: incomplete or altered bank'
        assert len(bank) == 5
        assert field[':answer-field/type'] == original[':answer-field/type'][':db/ident']
        assert field[':answer-field/key'] == original[':answer-field/key']
        assert q[':question/difficulty'] == source[':question/difficulty'][':db/ident']
        assert correct_index(q) == correct_index(source), profile
        assert prompt(q) == prompt(source), profile
        assert ('and then solve' in q[':question/problem']) == ('and then solve' in source[':question/problem'])
        # Compare retained instructional wording plus every displayed matrix;
        # allowed formatter changes include augmented separators and row notation.
        def prose(text):
            return ' '.join(re.sub(r'\$\$.*?\$\$|\$[^$]*\$', '', text, flags=re.S).split())
        assert prose(q[':question/worked-solution']) == prose(source[':question/worked-solution']), profile
        for record in (replay, sampled):
            result = check(record)
            assert not result['errors'], (profile, result['errors'])
            assert record['generation']['source_question'] == source[':question/id']
            assert record['generation']['source_db_id'] == source[':db/id']
        report['profiles'].append({'profile': profile, 'source_id': source[':question/id'],
                                   'bank_choices_matched': len(bank), 'replay': 'passed',
                                   'sampled': 'passed', 'math': 'passed'})
    # Check the ordinary random profile-selection path without a forced template.
    # Stop as soon as every supplied profile is observed; this tests real selection.
    selected = set()
    for seed in range(250):
        record = g.generate(seed=seed)
        assert not check(record)['errors']
        selected.add(record['generation']['template'])
        if selected == set(by_profile):
            break
    assert selected == set(by_profile), f'Unsampled profiles: {set(by_profile) - selected}'
    report.update({'passed': True, 'choices_matched': sum(p['bank_choices_matched'] for p in report['profiles']),
                   'random_selection_profiles': sorted(selected), 'selection_draws': seed + 1})
    save('source-records.json', records)
    save('source-coverage-results.json', report)
    print(json.dumps({'passed': True, 'replays': len(expected), 'sampled_profiles': len(expected),
                      'choices_matched': report['choices_matched'], 'selection_draws': seed + 1}))


if __name__ == '__main__':
    main()
