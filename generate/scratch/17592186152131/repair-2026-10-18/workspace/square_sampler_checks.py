#!/usr/bin/env python3
"""Probe the square-root target bias found by the independent reviewer."""
from collections import Counter, defaultdict
import json
from pathlib import Path
import re

import generator as g

OUT = Path(__file__).resolve().parent.parent / 'validation'


def measure(records):
    groups = defaultdict(Counter)
    for record in records:
        q = record['question']
        match = re.search(r'\\sqrt\{([^}]+)\}', q[':question/problem'])
        if not match:
            continue
        target = match[1]
        field = q[':question/answer-fields'][0]
        # Parse the served half-power bases, without reading generation metadata.
        bases = sorted({m[1] for c in field[':answer-field/choices']
                        if (m := re.fullmatch(r'\{([^}]+)\}\^\{1/2\}', c[':answer/value']))},
                       key=float)
        assert len(bases) == 2 and target in bases
        key = next(c[':answer/value'] for c in field[':answer-field/choices']
                   if c[':answer/id'] == field[':answer-field/correct'][1])
        assert key == g.normalize_tex(g.power(target, 1, 2))
        groups['|'.join(bases)][target] += 1
    return {pair:dict(counts) for pair,counts in groups.items()}


def main():
    records, first_square = [], []
    for seed in range(2560):
        batch = g.generate_batch(count=5, seed=seed)
        records.extend(batch)
        squares = [q for q in batch if re.search(r'\\sqrt\{', q['question'][':question/problem'])]
        if squares:
            first_square.append(squares[0])
    all_groups, first_groups = measure(records), measure(first_square)
    for groups in (all_groups, first_groups):
        assert set(groups) == {'|'.join(map(str,pair)) for pair in g.square_pairs()}
        assert all(len(counts) == 2 for counts in groups.values())
        # A broad regression bound detects the old 34/37 (~92%) preference;
        # it does not claim exact empirical balance in a random sample.
        counts = groups['2|3']
        p2 = counts['2'] / sum(counts.values())
        assert 0.30 < p2 < 0.70, (counts,p2)
    result = {'seeds':'0..2559','batch_count':2560,'records':len(records),
              'first_square_items':len(first_square),'all_square_pair_targets':all_groups,
              'first_square_pair_targets':first_groups,
              'old_first_square_conditional_probability':'34/37 for choosing base 2 in a {2,3} bank',
              'new_first_square_conditional_probability':'1/2 exactly: bank and inverted foil drawn before a uniform choice of either unused target; no square target has been used before the first square item.',
              'limits':'Later items exclude targets already used in the batch; learner-history filtering can also remove candidates. Random sample proportions need not be exactly 1/2.'}
    OUT.mkdir(exist_ok=True)
    (OUT/'square-sampler-records.json').write_text(json.dumps(records)+'\n')
    (OUT/'square-sampler-report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'records':len(records),'first_square_items':len(first_square),
                      'pair_2_3_all':all_groups['2|3'],'pair_2_3_first':first_groups['2|3']}))


if __name__ == '__main__':
    main()
