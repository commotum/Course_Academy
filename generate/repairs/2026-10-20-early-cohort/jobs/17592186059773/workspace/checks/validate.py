"""Focused source, visible-math, target-role, boundary and inventory checks."""
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = ROOT.parent
OUT = ROOT / 'evidence'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

g = load('g', ROOT / '17592186059773.py')
v = load('v', ROOT / '17592186059773/validate.py')

def save(path, data):
    path.write_text(json.dumps(data, indent=2) + '\n')

def visible_matrices(text):
    def entry(value):
        value = re.sub(r'\\frac\{(\d+)\}\{(\d+)\}', r'\1/\2', value.strip())
        return Fraction(value.replace(' ', ''))
    return [g.sp.Matrix([[entry(c) for c in row.split('&')]
                         for row in body.split(r'\\')])
            for body in re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S)]

def inspect(record):
    v.independent(record)  # Retain prior independent columnwise operation checks.
    q = record['question']; f = q[':question/answer-fields'][0]
    a, b = visible_matrices(q[':question/problem'])
    assert visible_matrices(q[':question/worked-solution']) == [a, b]
    hits = [c for c in f[':answer-field/choices'] if v.evaluate(a, c[':answer/value']) == b]
    assert len(hits) == 1 and hits[0][':answer/id'] == f[':answer-field/correct'][1]
    return hits[0][':answer/value']

def main():
    OUT.mkdir(exist_ok=True)
    source = json.loads((JOB / 'source/source.json').read_text())['material']['kp']
    official = {q.get(':question/math-academy-id'): q for q in source[':knowledge-point/questions']}
    records = []; replay = []; coverage = {}; pairs = []; irrelevant = []
    for sid, old in g.CASES.items():
        r = g.generate(parameters=g.DEFAULTS[sid]); value = inspect(r)
        public = r['question']; original = official[sid]
        assert public[':question/problem'] == original[':question/problem']
        assert public[':question/worked-solution'] == original[':question/worked-solution']
        field = public[':question/answer-fields'][0]; orig_field = original[':question/answer-fields'][0]
        assert Counter(a[':answer/value'] for a in field[':answer-field/choices']) == Counter(a[':answer/value'] for a in orig_field[':answer-field/choices'])
        assert value == orig_field[':answer-field/correct'][':answer/value']
        replay.append({'source': sid, 'uuid': old[':question/id'], 'prompt_exact': True,
                       'solution_exact': True, 'choices_matched': 5, 'distractors_matched': 4})
        records.append(r)
        # Same A, bank, names, layout and row mapping; only target decision varies.
        base = g.domain(sid)[0]
        controlled = [g.generate(parameters=base + [k]) for k in g.eligible_keys(sid)]
        answers = [inspect(rec) for rec in controlled]
        assert len(set(answers)) == len(controlled) >= 3
        assert len({tuple(visible_matrices(rec['question'][':question/problem'])[0]) for rec in controlled}) == 1
        for rec in controlled:
            assert [a[':answer/value'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']] == [a[':answer/value'] for a in controlled[0]['question'][':question/answer-fields'][0][':answer-field/choices']]
        records.extend(controlled)
        pairs.append({'profile': sid, 'record_ids': [x['question'][':question/id'] for x in controlled],
                      'distinct_targets_and_responses': len(set(answers)), 'input_and_bank_held_constant': True})
        # Cover every numeric cell and all row permutations with a small cross-sample.
        slots = sorted({tuple(p[1:3]) for p in g.domain(sid)})
        ps = list(g.itertools.permutations(range(3)))
        numeric = []
        for n, cell in enumerate(slots):
            candidates = [p for p in g.domain(sid) if tuple(p[1:3]) == cell and p[4] == list(ps[n % 6])]
            p = candidates[n % len(candidates)]
            rec = g.generate(parameters=p); inspect(rec); numeric.append(rec)
        # Explicit extremes, not just a typical random delta.
        for delta in (-3, 3):
            p = next(p for p in g.domain(sid) if p[3] == delta)
            rec = g.generate(parameters=p); inspect(rec); numeric.append(rec)
        records.extend(numeric)
        a, _ = visible_matrices(controlled[0]['question'][':question/problem'])
        op = g.operation(answers[0])
        untouched = next(i for i in range(3) if (op[0] == 'swap' and i not in op[1:]) or
                         (op[0] == 'replace' and i != op[1] and not op[2][i]))
        # Existing input slot in a row not consumed or changed by the operation.
        p = next(p for p in g.domain(sid) if p[1] == untouched and p[4] == [0, 1, 2]) + [g.eligible_keys(sid)[0]]
        rec = g.generate(parameters=p); assert inspect(rec) == answers[0]
        records.append(rec)
        irrelevant.append({'profile': sid, 'record_id': rec['question'][':question/id'],
                           'unused_input_row': untouched + 1, 'response_preserved': True})
        coverage[sid] = {'eligible_keys_tested': len(controlled), 'numeric_cells_tested': slots,
                         'row_permutations_tested': sorted({tuple(x['generation']['parameters'][4]) for x in numeric}),
                         'delta_boundaries_tested': [-3, 3], 'unavailable_elementary_keys': 5 - len(controlled)}
    # Exercise CLI-produced sampling, not only explicit parameter paths.
    sampled = g.batch('moderate', 5, 0)
    for rec in sampled: inspect(rec)
    assert sampled == g.batch('moderate', 5, 0)
    records.extend(sampled)
    for band in ('easy', 'hard', 'unclassified'):
        try: g.batch(band, 1)
        except ValueError: pass
        else: raise AssertionError(band)
    save(OUT / 'records.json', records)
    save(OUT / 'sample.json', sampled)
    save(OUT / 'source-replay.json', {'banks': replay, 'complete_banks_matched': len(replay), 'distractors_matched': 4 * len(replay)})
    save(OUT / 'native-input.json', [v.native(str(n), r) for n, r in enumerate(records)])
    save(OUT / 'pedagogical-variation.json', {'controlled_targets': pairs, 'irrelevant_changes': irrelevant, 'slot_coverage': coverage,
         'semantic_instances': len({r['generation']['mathematical_fingerprint'] for r in records}),
         'counting_rule': 'Matrix-pair canonicalization ignores row permutations, uniform scale, names, IDs and bank order.',
         'selection_limit': 'Shared delivery tests capture difficulty, inventory and duplicate filters. Live learner history and selection policy are unavailable; question_selection.rs selects fresh candidates by weighted difficulty then hash draw (or first candidate for an unconfigured policy). No database writes.'})
    inv = json.loads((JOB / 'source/inventory.json').read_text())
    original_ids = {q[':question/id'] for q in official.values()}
    inspected = []
    for q in inv['questions']:
        inspected.append({'question_id': q[':question/id'], 'entity_id': q[':db/id'],
                          'math_academy_id': q.get(':question/math-academy-id'),
                          'is_supplied_original': q[':question/id'] in original_ids,
                          'generation_metadata_present': any('generat' in k for k in q)})
    assert all(q['is_supplied_original'] and not q['generation_metadata_present'] for q in inspected)
    save(OUT / 'affected-inventory.json', {'affected_questions': []})
    save(OUT / 'inventory-audit.json', {'basis': inv['basis'], 'inspected': inspected,
         'conclusion': 'All 12 captured inventory records are supplied original questions, not generated records. No stored generated instance of the demonstrated CLI or fixed-profile sampling defect is present in this capture. Original questions were not marked generated. No live inventory claim.'})
    save(OUT / 'validation.json', {'passed': True, 'records_checked': len(records),
         'source_banks': len(replay), 'choice_evaluations': len(records) * 5,
         'fidelity': 'Exact original prompts, worked solutions, all banks and correct designations.',
         'correctness': 'Independent columnwise evaluation plus Fraction parsing of visible matrices and solution consistency.',
         'grading': 'Pending native harness; see native-report.json after execution.',
         'regression_history': 'No history finding IDs. Retain event code legacy_packaging_or_sampling and author-fixed-profile-key.'})
    print(json.dumps({'records': len(records), 'source_banks': len(replay), 'controlled_roles': sum(len(g.eligible_keys(sid)) for sid in g.CASES), 'inventory_originals': len(inspected)}))

if __name__ == '__main__':
    main()
