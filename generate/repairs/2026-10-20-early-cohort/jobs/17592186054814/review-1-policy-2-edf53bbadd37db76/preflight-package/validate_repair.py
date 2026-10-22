"""Reproducible targeted delivery, grading, rendering preparation and variation checks."""
import collections
import hashlib
from fractions import Fraction
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import generator as g
from source_acceptance import actual, oracle, prompt_value, save
REPO = Path('/home/jake/Developer/Course_Academy')
JOB = ROOT.parent
PY = REPO / '.venv/bin/python'


def profile(records):
    families = collections.defaultdict(collections.Counter)
    positions = collections.Counter()
    membership_counts = collections.Counter()
    negative_types = collections.Counter()
    for r in records:
        assert actual(r) == oracle(r)
        text = prompt_value(r)
        family = 'radical' if 'sqrt' in text else 'fraction' if 'frac' in text else 'pi' if 'pi' in text else 'decimal' if '.' in text else 'integer'
        families[family][actual(r)] += 1
        membership_counts[actual(r)] += 1
        fields = r['question'][':question/answer-fields']
        true_positions = tuple(i for i, f in enumerate(fields) if f[':answer-field/correct'][1] == next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value'] == 'true'))
        positions[str(true_positions)] += 1
        if text.startswith(r'\sqrt{-'):
            n = -int(re.search(r'\{(-?\d+)\}', text)[1])
            negative_types['square' if any(i*i == n for i in range(n+1)) else 'nonsquare'] += 1
    return {'count': len(records), 'families': dict(families), 'membership_counts': dict(membership_counts), 'true_position_patterns': dict(positions), 'negative_types': dict(negative_types)}


def prepare():
    sample = json.loads((ROOT / 'evidence/sample-records.json').read_text())
    params = ([{'family': 'radical', 'n': n} for n in [-144, -143, -12, -8, -4, -2, -1, 0, 1, 2, 4, 144, 150]] +
              [{'family': 'integer', 'n': n} for n in [-18, 0, 4]] +
              [{'family': 'fraction', 'n': n, 'd': 3} for n in [-27, -7, 0, 6, 7]] +
              [{'family': 'decimal', 'units': n} for n in [-2000, -1, 0, 1, 325, 2000]] +
              [{'family': 'pi', 'sign': n} for n in [-1, 1]])
    controlled = [g.build(p, seed=229174) for p in params]
    all_records = sample + controlled
    for r in all_records:
        assert actual(r) == oracle(r)
        assert actual(r) == ''.join(s for s in 'NZQRC' if s in r['question'][':question/worked-solution'].split('Therefore, the correct answer is ')[1])
    save('controlled-records.json', controlled)
    save('delivery-input.json', all_records)
    batch = g.generate(count=5, seed=419623)
    save('batch-records.json', batch)
    replay = g.replay_sources()
    cases = []
    # All newly recovered source banks, representative new negative coefficients,
    # controlled relevant changes, and a small ordinary sample.
    for i, r in enumerate(replay + controlled + batch):
        checks = []
        expected = oracle(r)
        for fi, f in enumerate(r['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:
                if f[':answer-field/type'].endswith('/checkbox'):
                    letter = re.search(r'\(\$([NZQRC])\$\)', f[':answer-field/key'])[1]
                    right = (a[':answer/value'] == 'true') == (letter in expected)
                else:
                    right = ''.join(s for s in 'NZQRC' if re.search(r'(?<![A-Za-z])' + s + r'(?![A-Za-z])', a[':answer/value'])) == expected
                checks.append({'field_index': fi, 'submitted_answer_id': a[':answer/id'], 'expected': 'accepted' if right else 'rejected', 'purpose': 'Independent prompt-derived complete membership, not stored key'})
        cases.append({'label': f'checked-{i}-{prompt_value(r)}', 'record': r, 'checks': checks})
    save('grader-input.json', cases)
    by_tex = {prompt_value(r): r for r in controlled}
    pairs = []
    for before, after, kind in [(r'\sqrt{4}', r'\sqrt{2}', 'relevant square status'), (r'\sqrt{2}', r'\sqrt{-2}', 'relevant sign'), (r'\sqrt{-2}', r'\sqrt{-4}', 'irrelevant to membership; exact imaginary coefficient changes'), (r'\sqrt{-2}', r'\sqrt{-8}', 'irrelevant to membership; exact imaginary coefficient changes'), ('-18', '4', 'relevant integer sign'), (r'-\frac{7}{3}', r'\frac{7}{3}', 'irrelevant rational sign')]:
        a, b = by_tex[before], by_tex[after]
        pairs.append({'before': before, 'after': after, 'kind': kind, 'before_membership': actual(a), 'after_membership': actual(b), 'prompt_changed': a['question'][':question/problem'] != b['question'][':question/problem'], 'solution_changed': a['question'][':question/worked-solution'] != b['question'][':question/worked-solution'], 'oracle_matches': actual(a) == oracle(a) and actual(b) == oracle(b)})
        assert pairs[-1]['prompt_changed'] and pairs[-1]['solution_changed'] and pairs[-1]['oracle_matches']
    # Layout only changes must preserve the mathematical key and explanation.
    a = g.build({'family': 'radical', 'n': -2}, 'NZQRC')
    b = g.build({'family': 'radical', 'n': -2}, 'CRQZN')
    assert actual(a) == actual(b) == 'C'
    assert a['question'][':question/worked-solution'] == b['question'][':question/worked-solution']
    save('counterfactual-results.json', {'pairs': pairs, 'field_permutation_preserves_response': True, 'grader_input': 'grader-input.json'})
    render = [by_tex[t] for t in [r'\sqrt{4}', r'\sqrt{2}', r'\sqrt{-2}', r'\sqrt{-8}']] + [r for r in replay if r['generation']['source_replay'] in ['48a2ffd6-1280-5b24-8f5a-4c13ac5f0fae', '5356b463-f0e3-5b2b-9ffc-35df47ad119b']]
    save('render-records.json', render)
    # Captured inventory inspected read-only; original source questions stay original.
    inv = json.loads((JOB / 'source/inventory.json').read_text())
    save('inventory-records.json', inv['questions'])
    source_ids = {q[':question/id'] for q in json.loads((ROOT / 'evidence/source-questions.json').read_text())}
    inspected = []
    for q in inv['questions']:
        inspected.append({'question_id': q[':question/id'], 'entity_id': q[':db/id'], 'prompt': q[':question/problem'], 'original_source': q[':question/id'] in source_ids, 'has_generation_metadata': any('generat' in k for k in q)})
    save('affected-inventory.json', {'affected_questions': []})
    save('inventory-analysis.json', {'basis': inv['basis'], 'tested': inspected, 'finding': 'All 13 captured prompts and provenance fields inspected. Eight are originals, including the newly restored radio sources. Five other stored prompts are 56/7, 34/3, -6.20, pi and -12.00; none demonstrates either the negative-nonsquare exclusion or omitted source replay. These construction/coverage failures do not show a wrong stored key.', 'limits': 'No generation metadata in captured records; cannot reproduce historical seeds or infer generated provenance. Verified absence of stored instances of these particular demonstrated defects only; not an audit of every stored behavior. No database writes.'})
    # Relocate declared runtime files only; no repository-dependent runtime imports.
    manifest = json.loads((ROOT / 'package.json').read_text())
    assert manifest['dependencies'] == {'python': platform.python_version(), 'packages': {}}
    relocated = ROOT / 'evidence/relocated-package'
    relocated.mkdir(exist_ok=True)
    for path in manifest['files']:
        shutil.copyfile(ROOT / path, relocated / path)
    cmd = [str(PY), '-B', 'generator.py', '--difficulty', 'easy', '--count', '5', '--seed', '419623', '--format', 'json']
    base = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)
    other = subprocess.run(cmd, cwd=relocated, text=True, capture_output=True, check=True)
    assert base.stdout == other.stdout
    for args in [['--difficulty', 'hard'], ['--count', '-1']]:
        assert subprocess.run(cmd[:3] + args, cwd=relocated, capture_output=True).returncode != 0
    assert g.generate(count=0) == []
    save('packaging-results.json', {'python': platform.python_version(), 'runtime_files': manifest['files'], 'relocated_identical': True, 'hard_and_negative_count_rejected': True, 'zero_count_empty': True, 'hashes': {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in manifest['files']}})
    print(json.dumps({'math': len(all_records), 'native_grader_records': len(cases), 'native_checks': sum(len(c['checks']) for c in cases), 'render': len(render), 'inventory': len(inspected), 'profile': profile(all_records)}))


def finalize():
    stages = {'ordinary_sample': 'sample-records.json', 'raw': 'delivery-input.json', 'delivered': 'delivery/accepted.json', 'raw_batch': 'batch-records.json', 'delivered_batch': 'delivery-batch/accepted.json'}
    results = {}
    probes = []
    for name, file in stages.items():
        records = json.loads((ROOT / 'evidence' / file).read_text())
        results[name] = profile(records)
        if name in ['raw', 'delivered']:
            assert set(results[name]['membership_counts']) == {'NZQRC', 'ZQRC', 'QRC', 'RC', 'C'}
            assert set(results[name]['families']['radical']) == {'NZQRC', 'ZQRC', 'RC', 'C'}
            assert set(results[name]['negative_types']) == {'square', 'nonsquare'}
        for family, masks in results[name]['families'].items():
            total = sum(masks.values())
            probes.append({'stage': name, 'cue': 'representation alone', 'family': family, 'best_constant_complete_answer': max(masks, key=masks.get), 'best_constant_accuracy': max(masks.values()) / total, 'classes': list(masks), 'justification': 'pi necessarily RC; integer representation only N-positive vs other integers; fraction/decimal may simplify; radical sign and square status are intended evidence'})
        # Probe every fixed subset of positions within each recognizable representation.
        family_records = collections.defaultdict(list)
        semantic_values = set()
        for r in records:
            text = prompt_value(r)
            family = 'radical' if 'sqrt' in text else 'fraction' if 'frac' in text else 'pi' if 'pi' in text else 'decimal' if '.' in text else 'integer'
            family_records[family].append(r)
            if family == 'radical':
                n = int(re.search(r'\{(-?\d+)\}', text)[1])
                exact = next((i for i in range(max(n, 0) + 1) if i*i == n), None)
                semantic_values.add(('rational', str(exact)) if exact is not None else ('root', n))
            elif family == 'fraction':
                n, d = map(int, re.search(r'frac\{(\d+)\}\{(\d+)\}', text).groups())
                semantic_values.add(('rational', str(Fraction(-n if text.startswith('-') else n, d))))
            elif family == 'pi':
                semantic_values.add(('pi', text.startswith('-')))
            else:
                semantic_values.add(('rational', str(Fraction(text))))
        results[name]['distinct_mathematical_values'] = len(semantic_values)
        for family, group in family_records.items():
            scores = []
            for bits in range(32):
                hits = 0
                for r in group:
                    fields = r['question'][':question/answer-fields']
                    predicted = ''.join(s for s in 'NZQRC' if any(bits & (1 << i) and s == re.search(r'\(\$([NZQRC])\$\)', f[':answer-field/key'])[1] for i, f in enumerate(fields)))
                    hits += predicted == actual(r)
                scores.append(hits)
            probes.append({'stage': name, 'cue': 'best_of_all_32_fixed_position_subsets', 'family': family, 'best_correct': max(scores), 'total': len(group), 'scores': scores})
            if name in ['raw', 'delivered'] and len(results[name]['families'][family]) > 1:
                assert max(scores) < len(group), ('within-family position shortcut', name, family)
        for label, predicted in [('always_C_only', 'C'), ('always_all', 'NZQRC')]:
            probes.append({'stage': name, 'cue': label, 'correct': sum(actual(r) == predicted for r in records), 'total': len(records)})
        position = []
        for n in range(6):
            hits = 0
            for r in records:
                fs = r['question'][':question/answer-fields']
                included = ''.join(s for s in 'NZQRC' if any(s == re.search(r'\(\$([NZQRC])\$\)', f[':answer-field/key'])[1] for f in fs[:n]))
                hits += included == actual(r)
            position.append({'select_first_n': n, 'correct': hits, 'total': len(records)})
        probes.append({'stage': name, 'cue': 'fixed_prefix_positions', 'results': position})
        assert all(p['correct'] < p['total'] for p in position), ('fixed positional full-answer shortcut', name)
    save('coverage-results.json', results)
    save('shortcut-results.json', {'probes': probes, 'limits': 'No claim that mathematical indicators such as negative radicands or pi should change their correct classification. Correct count is implied by the nested hierarchy, not supplied by incidental layout. Tests address full-answer shortcuts, not invariant correct C alone.'})
    # Read-only selection analysis from actual Rust source; no policy/history captured.
    selection = REPO / 'engine/rust/question_selection.rs'
    save('selection-results.json', {'implementation_hash': hashlib.sha256(selection.read_bytes()).hexdigest(), 'inspection': 'select deduplicates/sorts candidate entity IDs; positively weighted rated bands chosen first, uniform within each band. Caller excludes learner history/current task prefix. Unknown rating only used if no eligible positive-weight rated band remains. No policy selects smallest entity ID.', 'consequence': 'Delivered variants all easy. With positive easy weight and fresh/usable status, each has selection support regardless of representation or key. History can exclude individual cases. No policy/history was captured; no claim of a specific live selected distribution.', 'generator_rejection': 'generate rejects only repeated displayed values and invalid requests. No rejection depends on membership pattern. Negative nonsquares retained through check_delivery; source duplicates may be removed by inventory.', 'coverage_after_delivery': results['delivered']})
    print(json.dumps({name: {'count': r['count'], 'classes': r['membership_counts'], 'negative_types': r['negative_types']} for name, r in results.items()}))


if __name__ == '__main__':
    prepare() if len(sys.argv) == 1 or sys.argv[1] == 'prepare' else finalize()
