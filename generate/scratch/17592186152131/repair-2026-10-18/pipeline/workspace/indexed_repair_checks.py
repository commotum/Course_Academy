#!/usr/bin/env python3
"""Validate the 2026-10-18 indexed bank repair; no database writes.

Run with project Python from any directory. Evidence goes beside this workspace,
not into the immutable runtime package. The original square-repair tests remain
historical evidence; this script exercises the current indexed and square code.
"""
import collections
from itertools import product
import json
from pathlib import Path
import random
import re
import subprocess
import sys
import tempfile

import generator as g
import validate as v

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / 'validation'
OUT.mkdir(exist_ok=True)
v.E = OUT


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')


def choices(record):
    return record['question'][':question/answer-fields'][0][':answer-field/choices']


def signature(record):
    return sorted(c[':answer/value'] for c in choices(record))


def reported_shortcut(record):
    # Reconstruct the rejected answer-only rule from served choices, not metadata.
    for c in choices(record):
        match = re.fullmatch(r'\{1\}\^\{(\d+)/(\d+)\}', c[':answer/value'])
        if match:
            return g.normalize_tex(g.power(match[1], 1, match[2]))
    raise AssertionError('Missing unit-base foil')


def main():
    source_replay = v.source_checks()
    indexed, counterfactuals, probe_counts = [], [], collections.defaultdict(collections.Counter)
    semantic = set()
    for i, (bases, indices) in enumerate(g.indexed_profiles()):
        # Every distinct choice-bank signature has all four eligible keys.
        # Cycle through all four independent unit-base foil assignments.
        for u, denominator in product(bases, indices):
            bank = {'bases': bases, 'indices': indices,
                    'foil_numerator': u, 'foil_denominator': denominator}
            group = []
            for j, (x, n) in enumerate(product(bases, indices)):
                template = ('indexed-equation', 'indexed-what')[i % 2]
                record = g.generate(x, n, template, indexed_bank=bank,
                                    order_seed=100000*i + 100*u + denominator*4 + j)
                checked = v.inspect(record)
                semantic.add((x, n))
                group.append(record)
                key = checked['key']
                hit = reported_shortcut(record) == key
                for label in ('overall', template, f'base-{x}', f'index-{n}'):
                    probe_counts[label]['correct'] += hit
                    probe_counts[label]['total'] += 1
            assert len({tuple(signature(r)) for r in group}) == 1
            assert len({v.inspect(r)['key'] for r in group}) == 4
            assert len({r['question'][':question/problem'] for r in group}) == 4
            assert len({r['question'][':question/worked-solution'] for r in group}) == 4
            # Keep one foil assignment per bank for delivered/native checks.
            if (u, denominator) == (bases[0], indices[0]):
                indexed.extend(group)
            if i in (0, len(g.indexed_profiles()) - 1):
                counterfactuals.extend(group)
    assert semantic == set(g.domain('indexed-equation'))
    assert all(c['correct'] * 4 == c['total'] for c in probe_counts.values())
    # Irrelevant foil and order changes preserve prompt, exact key and solution.
    fixed = [r for r in counterfactuals if r['generation']['parameters'] ==
             counterfactuals[0]['generation']['parameters']]
    assert len({v.inspect(r)['key'] for r in fixed}) == 1
    assert len({r['question'][':question/problem'] for r in fixed}) == 1
    assert len({r['question'][':question/worked-solution'] for r in fixed}) == 1
    square = [g.generate(x, n, 'square-equation', foil_index=m, base_direction=d,
                         inverted_base=b, order_seed=991 + i*19 + m)
              for i, (x,n) in enumerate(g.domain('square-equation'))
              for m in (1,3,4,5) for d in g.square_neighbors(x) for b in ('target','other')]
    for record in square:
        v.inspect(record)
    # Both radicands are eligible keys within every identical square bank.
    groups = collections.defaultdict(set)
    for record in square:
        groups[tuple(signature(record))].add(v.inspect(record)['key'])
    assert len(groups) == 168 and all(len(keys) == 2 for keys in groups.values())
    seeds = (0,1,7,25,92718,1033798965,1287419,9125308)
    normal = []
    for seed in seeds:
        batch = g.generate_batch(count=126, seed=seed)
        assert batch == g.generate_batch(count=126, seed=seed)
        assert len({(str(r['generation']['parameters']['x']),r['generation']['parameters']['n'])
                    for r in batch}) == 126
        for r in batch:
            v.inspect(r)
            assert r['generation']['profile'] not in ('unit-base', 'square-division')
        normal.extend(batch)
    assert g.generate_batch(count=0) == []
    for kwargs in ({'count':127}, {'count':-1}, {'difficulty':'moderate'}, {'difficulty':'hard'}):
        try:
            g.generate_batch(**kwargs)
            raise AssertionError('Unsupported request accepted')
        except ValueError:
            pass
    # Relocate only declared runtime files; no hidden workspace dependency.
    with tempfile.TemporaryDirectory() as temp:
        target = Path(temp)
        manifest = json.loads((ROOT/'package.json').read_text())
        for name in manifest['files']:
            (target/name).write_bytes((ROOT/name).read_bytes())
        result = subprocess.run([sys.executable,'-E','-s','-B',str(target/'generator.py'),
                                 '--count','5','--seed','1033798965'],
                                cwd=target,check=True,capture_output=True,text=True)
        assert json.loads(result.stdout) == json.loads(json.dumps(g.generate_batch(count=5,seed=1033798965)))
    raw = indexed + square + normal
    save('test-records.json',raw)
    save('counterfactual-records.json',counterfactuals)
    save('seeded-records.json',normal)
    save('shortcut-probes.json',dict(probe_counts))
    save('native-input.json',v.grader_cases(raw + source_replay + counterfactuals,'radical-repair'))
    render = counterfactuals[:4] + [g.generate('3.5',2,'square-equation'),
              g.generate(2,2,'square-equation'), g.generate(4,2,'square-equation')] + source_replay
    save('render-records.json',render)
    save('summary.json',{'source_banks':3,'source_choices':15,
         'indexed_complete_banks':len(g.indexed_profiles()),
         'indexed_foil_assignments':4,'indexed_counterfactual_records':sum(c['total'] for k,c in probe_counts.items() if k=='overall'),
         'indexed_delivered_audit_records':len(indexed),'square_records':len(square),
         'square_same_bank_pairs':len(groups),'semantic_capacity':126,'seeded_records':len(normal),
         'all_exact_mathematical_checks':'passed','determinism':'passed','relocation':'passed',
         'reported_shortcut':dict(probe_counts['overall']),
         'shortcut_comparison':'25% among the four unit-fraction choices, versus 100% before repair; 20% is blind guessing among all five choices. Base 1 can legitimately be eliminated mathematically.',
         'limitations':['Finite audit; no claim to rule out every shortcut.',
                        'Live publication requires an independent policy review.']})
    print((OUT/'summary.json').read_text())


def delivered():
    raw = json.loads((OUT/'test-records.json').read_text())
    rows = json.loads((OUT/'delivery/accepted.json').read_text())
    groups = {'indexed-grid':collections.defaultdict(set),
              'square-index-confusion':collections.defaultdict(set)}
    for record in rows:
        groups[record['generation']['profile']][tuple(signature(record))].add(v.inspect(record)['key'])
    indexed = groups['indexed-grid']
    square = groups['square-index-confusion']
    assert sum(len(keys)==4 for keys in indexed.values()) == len(g.indexed_profiles())
    assert len(square)==168 and all(len(keys)==2 for keys in square.values())
    semantic = lambda records: {(v.inspect(r)['x'],v.inspect(r)['n']) for r in records}
    assert semantic(rows) == semantic(raw)
    report = {'raw_count':len(raw),'delivered_count':len(rows),'duplicate_count':len(raw)-len(rows),
              'complete_indexed_banks_retained':len(g.indexed_profiles()),
              'complete_square_bank_pairs_retained':len(square),'semantic_instances_retained':len(semantic(rows)),
              'inventory_basis':json.loads((OUT/'delivery/delivery.json').read_text())['inventory_basis'],
              'selection_limits':'Captured-inventory filtering, not a live learner draw. History may remove candidates; positive-weight bands use hash selection, unconfigured policies choose the first candidate.'}
    save('delivery-comparison.json', report)
    native = v.grader_cases(rows,'delivered-radicals')
    controls = json.loads((OUT/'counterfactual-records.json').read_text())[:4]
    former_key = v.inspect(controls[0])['key']
    for record in controls[1:]:
        choice = next(c for c in choices(record) if c[':answer/value']==former_key)
        native.append({'label':'prompt-change-rejects-former-key','record':record,
                       'checks':[{'submitted_answer_id':choice[':answer/id'],'expected':'rejected',
                                  'purpose':'Same complete bank; changed target radical makes former key wrong.'}]})
    save('delivered-native-input.json',native)
    print(json.dumps(report))


if __name__ == '__main__':
    if sys.argv[1:] == ['--delivered']:
        delivered()
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit('Usage: indexed_repair_checks.py [--delivered]')
