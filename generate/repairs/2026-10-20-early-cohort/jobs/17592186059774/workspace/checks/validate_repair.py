"""Affected validation: source banks, restored decisions, delivery and packaging."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from checks.independent import analyze, apply, mats, op, target
import generator as g

EVIDENCE = ROOT / 'evidence'
def load(p): return json.loads(p.read_text())
def save(name, value): (EVIDENCE / name).write_text(json.dumps(value, indent=2, default=str))


def prepare():
    source = load(ROOT.parent / 'source/source.json')
    replays = load(EVIDENCE / 'source-replays.json')
    # One current-generation witness for each independently eligible assignment.
    records, coverage = [], []
    for q in source['material']['kp'][':knowledge-point/questions']:
        f = q[':question/answer-fields'][0]
        if not f.get(':answer-field/correct') or not q.get(':question/worked-solution'):
            continue  # documented pre-existing incomplete capture, replay checked separately
        t, _ = target(q[':question/problem'])
        sid = q[':question/math-academy-id']
        eligible = []
        for i, v in enumerate(f[':answer-field/choices']):
            o = op(v[':answer/value'])
            if ((o[0] == 'swap' and t in o[1:]) or
                (o[0] == 'linear' and o[1] == t and o[2][t] == 1 and
                 sum(c != 0 for j, c in enumerate(o[2]) if j != t) == 1)):
                eligible.append(i)
        for i in eligible:
            r = g.generate(seed=9061 + i, template=sid, parameters={'winner': i})
            a = analyze(r)
            records.append(r)
            coverage.append({'profile': sid, 'winner': i, 'target': a['target'],
                             'semantic_fingerprint': r['generation']['mathematical_fingerprint']})
    batch = g.batch('hard', 5, 59774)
    cf = load(EVIDENCE / 'counterfactual-records.json')
    changed = load(EVIDENCE / 'changed-target-records.json')
    # Full restored-profile permutation checks are covered in the regression;
    # delivery/grader use the targeted counterfactuals and one case per winner.
    raw = records + cf + changed + batch
    checked = [analyze(r) for r in raw]
    save('validation-records.json', raw)
    save('sample-batch.json', batch)
    save('coverage.json', coverage)
    save('math-results.json', {'status': 'passed', 'sample_size': len(raw), 'visible_analysis': checked})
    save('grader-input.json', [
        {'label': r['question'][':question/id'], 'record': r,
         'checks': [{'field_index': 0, 'submitted_answer_id': v[':answer/id'],
                    'expected': 'accepted' if i == analyze(r)['position'] else 'rejected',
                    'purpose': 'independent Fraction calculation of each visible operation'}
                   for i, v in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices'])]}
        for r in raw + replays])
    # Exact restored replay, subtraction, swap, and changed-target witnesses.
    save('render-records.json', [g.replay('q-72858')] + cf[:2] + changed)
    manifest = load(ROOT / 'package.json')
    versions = {'python': platform.python_version(), 'packages': {
        p: importlib.metadata.version(p) for p in manifest['dependencies']['packages']}}
    assert versions == manifest['dependencies']
    relocated = EVIDENCE / 'relocated'
    relocated.mkdir(exist_ok=True)
    for name in manifest['files']:
        dst = relocated / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, dst)
    cmd = [sys.executable, str(relocated / manifest['entrypoint']), '--difficulty', 'hard',
           '--count', '5', '--seed', '59774', '--format', 'json']
    output = json.loads(subprocess.check_output(cmd, cwd='/tmp'))
    assert output == batch
    assert all(g.generate(seed=r['generation']['seed'], parameters=r['generation']['parameters'])['question'] == r['question'] for r in raw)
    save('packaging-results.json', {'status': 'passed', 'dependencies': versions,
        'relocation_command': cmd, 'relocation_matches': True,
        'deterministic_parameter_replay': len(raw),
        'runtime_hashes': {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in manifest['files']}})
    inventory(source)
    print(json.dumps({'records': len(raw), 'eligible_assignments': len(coverage),
                      'grader_cases': len(raw) + len(replays), 'render_cases': 5}))


def inventory(source):
    inv = load(ROOT.parent / 'source/inventory.json')
    source_ids = {q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
    extras = [q for q in inv['questions'] if q[':question/id'] not in source_ids]
    results = []
    for q in extras:
        a = mats(q[':question/problem'])[0]; t, c = target(q[':question/problem'])
        f = q[':question/answer-fields'][0]
        good = [v for v in f[':answer-field/choices'] if apply(a, op(v[':answer/value']))[t][c] == 0]
        assert len(good) == 1 and good[0][':answer/id'] == f[':answer-field/correct'][':answer/id']
        assert apply(a, op(good[0][':answer/value'])) == mats(q[':question/worked-solution'])[-1]
        results.append({'question_id': q[':question/id'], 'entity_id': q[':db/id'],
                        'key_and_matrix': 'passed', 'generation_metadata_available': False})
    assert any(q[':question/id'] == '372c1499-bf5a-558e-ad8a-af28e6ae7898' for q in inv['questions'])
    save('inventory-review.json', {'captured_basis': inv['basis'], 'stored_records_inspected': len(inv['questions']),
        'source_questions': len(source_ids), 'non_source_checks': results,
        'finding_scope': 'Missing source-bank supply is not a defect of an individual stored generated record. '
                         'The original q-72858 is present and is not classified as generated.',
        'conclusion': 'No individual stored question demonstrated affected by the retained omission finding.',
        'limits': ['No exact generation replay of the five non-source records: capture omits generation metadata.',
                   'No claim of absence of unrelated structural defects in all inventory records.']})
    save('affected-inventory.json', {'affected_questions': []})
    # Read-only selection reproduction; no fabricated publication/entity IDs.
    pool = sorted(q[':db/id'] for q in inv['questions']
        if q.get(':question/difficulty', {}).get(':db/ident') == ':question.difficulty/hard'
        and q.get(':question/worked-solution')
        and all(f.get(':answer-field/correct') for f in q[':question/answer-fields']))
    simulations = []
    for seen in [[], pool[:5]]:
        fresh = [q for q in pool if q not in seen]
        counts = Counter()
        for i in range(64):
            digest = hashlib.sha256(f'course-academy/question-selection/v1/repair-{i}'.encode()).digest()
            uniform = (int.from_bytes(digest[8:16], 'big') >> 11) / (1 << 53)
            counts[fresh[math.floor(uniform * len(fresh))]] += 1
        simulations.append({'seen': seen, 'fresh': fresh, 'draws': dict(counts),
                            'unconfigured_policy_first': fresh[0]})
    save('selection-results.json', {'basis': inv['basis'], 'simulations': simulations,
        'implementation': 'engine/rust/question_selection.rs::select: sorted unique fresh usable candidates, '
                          'difficulty-first weighted band; uniform(8) within selected band.',
        'implication': 'Positive hard weight does not further filter bank profiles; zero hard weight excludes hard questions. '
                       'An unconfigured policy chooses the lowest fresh entity ID.',
        'limits': ['Live policy and learner histories are not supplied.',
                   'No actual future publication IDs or live selection probabilities claimed.']})


def probes(records):
    profiles = defaultdict(list)
    for r in records:
        profiles[r['generation']['bank_profile']].append(r)
    result = {}
    for sid, rs in profiles.items():
        winners = Counter(r['generation']['parameters']['winner'] for r in rs)
        positions = Counter(analyze(r)['position'] for r in rs)
        kinds = Counter(analyze(r)['kind'] for r in rs)
        donors = Counter()
        for r in rs:
            a = analyze(r); o = op(a['correct']); t, _ = target(r['question'][':question/problem'])
            donor = next(i for i in o[1:] if i != t) if o[0] == 'swap' else next(i for i, v in enumerate(o[2]) if i != t and v)
            donors[donor] += 1
        result[sid] = {'count': len(rs), 'winner_counts': dict(winners),
            'best_fixed_bank_slot': max(winners.values()), 'position_counts': dict(positions),
            'best_fixed_stored_position': max(positions.values()),
            'operation_type_counts': dict(kinds), 'best_fixed_operation_type': max(kinds.values()),
            'donor_label_counts': dict(donors), 'best_fixed_donor_label': max(donors.values()),
            'five_choice_baseline': 0.2, 'eligible_slot_baseline': 1 / len(winners)}
        assert len(winners) >= 2, ('fixed bank winner', sid)
    return result


def after():
    raw = load(EVIDENCE / 'validation-records.json')
    accepted = load(EVIDENCE / 'delivery/accepted.json')
    before, after = probes(raw), probes(accepted)
    # Delivery may remove duplicates; all tested eligible assignments must remain.
    assert set(before) == set(after)
    for sid in before:
        assert set(before[sid]['winner_counts']) == set(after[sid]['winner_counts'])
    save('shortcut-results.json', {'raw_count': len(raw), 'accepted_count': len(accepted),
        'before_delivery': before, 'after_delivery': after,
        'conclusions': ['No bank identity or fixed source-bank slot predicts every answer within its bank.',
            'All eligible operations survive delivery; numerical changes determine the winning slot.',
            'Operation type or donor identity may eliminate candidates, as the lesson teaches; '
            'they do not identify one universally correct candidate within any bank.',
            'Stored-position counts use authored order; actual UI order is checked separately.'],
        'limits': ['Purposeful decision witnesses establish support, not natural frequency estimates.',
                   'Finite cue probes cannot exclude every conceivable incidental predictor.']})
    render = load(EVIDENCE / 'render-records.json')
    ui = []
    for i, r in enumerate(render):
        html = (EVIDENCE / f'render/question-{i+1:03}.html').read_text()
        ids = re.findall(r'<input\b[^>]*type="radio"[^>]*value="([^"]+)"', html)
        f = r['question'][':question/answer-fields'][0]
        assert len(ids) == 5 and f[':answer-field/correct'][1] in ids
        ui.append({'question_id': r['question'][':question/id'],
                   'position': ids.index(f[':answer-field/correct'][1]), 'answer_ids': ids})
    assert len({r['position'] for r in ui}) > 1
    save('ui-order-results.json', ui)
    print(json.dumps({'delivery': f'{len(accepted)}/{len(raw)}',
                      'banks': len(after), 'retained_winner_slots': sum(len(v['winner_counts']) for v in after.values()),
                      'ui_positions': [r['position'] for r in ui]}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--stage', choices=['prepare', 'after'], required=True)
    args = p.parse_args()
    (prepare if args.stage == 'prepare' else after)()
