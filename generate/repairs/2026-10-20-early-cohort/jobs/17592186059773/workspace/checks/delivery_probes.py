"""Check shortcut and controlled-target claims on actual delivery survivors."""
import json
from collections import Counter, defaultdict
from pathlib import Path
import validate as checks

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'evidence'
g, v = checks.g, checks.v

def examine(records):
    banks = defaultdict(list)
    groups = defaultdict(list)
    exact_groups = defaultdict(list)
    for rec in records:
        q = rec['question']; f = q[':question/answer-fields'][0]
        a, b = checks.visible_matrices(q[':question/problem'])
        # Independent mathematical witness from the visible choices and matrices.
        positions = [i for i, choice in enumerate(f[':answer-field/choices'])
                     if v.evaluate(a, choice[':answer/value']) == b]
        assert len(positions) == 1
        position = positions[0]
        assert f[':answer-field/choices'][position][':answer/id'] == f[':answer-field/correct'][1]
        profile = rec['generation']['bank_profile']
        banks[profile].append(position)
        bank = tuple(x[':answer/value'] for x in f[':answer-field/choices'])
        changed = tuple(i for i in range(3) if a[i, :] != b[i, :])
        groups[(profile, bank, changed)].append(position)
        exact_groups[(profile, bank, tuple(a))].append(position)
    report = {}
    for sid, values in banks.items():
        counts = Counter(values)
        assert len(counts) >= 3, (sid, counts)
        report[sid] = {'positions': dict(counts), 'best_fixed_position_successes': max(counts.values()),
                       'attempts': len(values), 'uniform_eligible_baseline': 1 / len(g.eligible_keys(sid)),
                       'fixed_position_or_source_bank_deterministic': False}
    controlled = {}
    for sid in banks:
        variants = [set(values) for (profile, bank, a), values in exact_groups.items() if profile == sid]
        assert any(len(values) == len(g.eligible_keys(sid)) for values in variants), sid
        controlled[sid] = max(map(len, variants))
    # Mathematical row-change signatures can legitimately narrow the operation.
    # When a bank supplies competing choices for the same signature, require both.
    competing = []
    for (sid, bank, changed), values in groups.items():
        # Only make a completeness assertion on a controlled experiment.
        # Ordinary slot/boundary samples intentionally are not balance quotas.
        if not any(profile == sid and fixed_bank == bank and
                   len(set(keys)) == len(g.eligible_keys(sid))
                   for (profile, fixed_bank, fixed_a), keys in exact_groups.items()):
            continue
        options = []
        for k, text in enumerate(bank):
            op = g.operation(text)
            elementary = op[0] == 'swap' or (op[2][op[1]] == 1 and sum(bool(c) for j,c in enumerate(op[2]) if j != op[1]) == 1) or (all(not c for j,c in enumerate(op[2]) if j != op[1]) and op[2][op[1]] not in (0, 1))
            target = tuple(sorted(op[1:])) if op[0] == 'swap' else (op[1],)
            if elementary and target == changed: options.append(k)
        if len(options) > 1:
            assert set(options) <= set(values), (sid, changed, values, options)
            competing.append({'profile': sid, 'changed_rows': [i+1 for i in changed],
                              'competing_positions': options, 'observed_positions': sorted(set(values))})
    return {'count': len(records), 'profile_position_cues': report,
            'same_input_bank_layout_names_controlled_responses': controlled,
            'same_changed_rows_competing_cases': competing}

def main():
    raw = json.loads((OUT / 'records.json').read_text())
    accepted = json.loads((OUT / 'delivery/accepted.json').read_text())
    result = {'before_delivery': examine(raw), 'after_delivery': examine(accepted),
              'legitimate_inferences': 'Changed rows, a row swap, or whole-row proportionality are mathematical evidence required by the lesson. Swap-only q-72850 has three pairs; not choosing its non-elementary options is valid reasoning.',
              'claim_limits': 'Controlled samples disprove deterministic source-bank, answer-position, name, layout and input-zero-pattern cues. They do not prove absence of every possible learned statistical cue.'}
    checks.save(OUT / 'delivery-probes.json', result)
    controlled = []
    for sid in g.CASES:
        base = g.domain(sid)[0]
        expected = {g.generate(parameters=base+[key])['generation']['mathematical_fingerprint'] for key in g.eligible_keys(sid)}
        found = [r for r in accepted if r['generation']['bank_profile'] == sid and r['generation']['mathematical_fingerprint'] in expected]
        # Keep just one record per target, since source normalization deduplicates.
        found = list({r['generation']['mathematical_fingerprint']: r for r in found}.values())
        assert len(found) == len(expected)
        controlled.extend(found)
    checks.save(OUT / 'delivered-native-input.json', [v.native('delivered control '+str(n), r) for n,r in enumerate(controlled)])
    render = []
    for kind in ('swap', 'scale', 'addition'):
        for rec in accepted:
            q = rec['question']; f = q[':question/answer-fields'][0]
            text = next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id'] == f[':answer-field/correct'][1])
            op = g.operation(text)
            actual_kind = 'swap' if op[0] == 'swap' else 'scale' if sum(bool(c) for c in op[2]) == 1 else 'addition'
            if actual_kind == kind and (kind != 'scale' or '\\frac' in q[':question/problem']):
                render.append(rec); break
        else: raise AssertionError('No render case '+kind)
    checks.save(OUT / 'render-records.json', render)
    print(json.dumps({'before': len(raw), 'after': len(accepted), 'all_48_controlled_targets_survive': len(controlled) == 48,
                      'native_delivered_cases': len(controlled), 'render_records': len(render)}))

if __name__ == '__main__':
    main()
