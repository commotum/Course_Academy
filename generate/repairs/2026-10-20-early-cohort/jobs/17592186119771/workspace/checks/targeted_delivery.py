#!/usr/bin/env python3
"""Inspect sparse support and shortcut probes after the actual shared filter."""
import collections
import json
import re
import validate as v


def probes(records):
    density = collections.defaultdict(collections.Counter)
    first_pair = collections.Counter()
    first_pair_attempts = 0
    for r in records:
        q = r['question']; m = v.matrix(q[':question/problem'])
        answer = v.verify(r)
        count = sum(x != 0 for i,row in enumerate(m) for j,x in enumerate(row) if i != j)
        density[(len(m), count)][answer] += 1
        if len(m) == 3 and m[0][1] == m[1][0] == 0:
            first_pair[answer] += 1
            first_pair_attempts += 1
    for (n,count), answers in density.items():
        if count: assert {'Upper triangular matrix','Lower triangular matrix'} <= answers.keys()
    assert {'Upper triangular matrix','Lower triangular matrix','Diagonal matrix'} <= first_pair.keys()
    return {'density_groups': [{'size': n, 'off_diagonal_nonzeros': c,
             'answer_counts': dict(a), 'constant_label_successes': max(a.values()),
             'attempts': sum(a.values())} for (n,c), a in sorted(density.items())],
            'first_pair_both_zero_3x3': {'answer_counts': dict(first_pair),
              'best_constant_successes': max(first_pair.values()), 'attempts': first_pair_attempts},
            'mathematical_cue': 'An empty off-diagonal support correctly implies diagonal; the location of nonzeros relative to the diagonal is the intended decisive evidence.'}


def main():
    before = json.loads((v.OUT/'single-witness-records.json').read_text())
    after = json.loads((v.OUT/'sparse-delivery/accepted.json').read_text())
    assert len(after) == len(before)
    assert collections.Counter((tuple(map(tuple,v.matrix(r['question'][':question/problem']))),v.key(r['question'])) for r in before) == collections.Counter((tuple(map(tuple,v.matrix(r['question'][':question/problem']))),v.key(r['question'])) for r in after)
    for r in after: v.verify(r)
    results = {}
    for stage, path in [('before', 'delivery-input.json'), ('after', 'delivery/accepted.json')]:
        records = json.loads((v.OUT/path).read_text())
        results[stage] = probes(records)
    assert results['before'] == results['after']
    results['sparse_records_surviving'] = len(after)
    v.save('targeted-delivery-probes.json', results)
    print(json.dumps({'sparse_accepted': len(after), 'density_and_first_pair_probes': 'passed'}))


if __name__ == '__main__': main()
