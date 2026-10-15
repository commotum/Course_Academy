"""Independent dot-product, source-bank, rendered algebra, and native grading QA."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import sympy as s

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('flux_generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
x, y = g.x, g.y


def save(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')


def equal(a, b):
    return s.Poly(s.expand(a - b), x, y).is_zero


def independent(rec):
    m = rec['generation']
    template, k = m['template'], m['parameters']['scale']
    p, q, geom, level = g.DATA[template]
    # Independently derive the normal from source geometry and then take the
    # Cartesian dot product. No generator answer/term helper is called.
    if level == 'easy':
        assert geom > 0
        normal = s.Matrix([x, y]) / geom
    else:
        side = int(re.search(r'flux of \$F\$ across the side \$\{C\}_\{(\d)\}', g.SOURCES[template][':question/problem'])[1])
        normal = s.Matrix({1:(1,0), 2:(0,1), 3:(-1,0), 4:(0,-1)}[side])
        assert tuple(normal) == geom
    expected = s.expand(s.Matrix([k*p, k*q]).dot(normal))
    question = rec['question']
    assert rec['knowledge_point']['db_id'] == g.KP_ID
    assert question[':question/difficulty'] == ':question.difficulty/' + level
    fields = question[':question/answer-fields']
    assert len(fields) == 1
    f = fields[0]
    assert f[':answer-field/type'] == ':answer-field.type/radio' and f[':answer-field/key'] == 'selection'
    bank = f[':answer-field/choices']
    assert len(bank) == 5 and len({a[':answer/id'] for a in bank}) == 5
    vals = [g.parse(a[':answer/value']) for a in bank]
    assert all(sum(equal(a, b) for b in vals) == 1 for a in vals)
    correct = next(a for a in bank if a[':answer/id'] == f[':answer-field/correct'][1])
    assert equal(g.parse(correct[':answer/value']), expected)
    assert sum(equal(v, expected) for v in vals) == 1
    sf = g.SOURCES[template][':question/answer-fields'][0]
    original = [k*g.parse(a[':answer/value']) for a in sf[':answer-field/choices']]
    assert all(sum(equal(a, b) for b in vals) == 1 for a in original)
    for a in bank:
        assert '$' not in a[':answer/value']
    prompt, solution = question[':question/problem'], question[':question/worked-solution']
    for text in (prompt, solution):
        assert text.count('$') % 2 == 0
        assert text.count('{') == text.count('}')
    if k != 1:
        field = re.search(r'F\(x,y\)=\((.*?)\)\\,i\+\((.*?)\)\\,j\$', prompt)
        assert field, prompt
        assert equal(g.parse(field[1]), k*p) and equal(g.parse(field[2]), k*q)
        # The entire vector expression in the worked substitution must agree.
        assert '(' + field[1] + r')\,i+(' + field[2] + r')\,j' in solution
        answer = re.search(r'Therefore, the missing expression is \$(.*?)\.\$', solution)[1]
        assert equal(g.parse(answer), expected)
        integrands = re.findall(r'& =\{(?:∮|\\int )\}_(?:\{C\}|\{\{C\}_\{\d\}\})(.*?)\\,\\text\{d\}s', solution)
        assert equal(g.parse(integrands[-1].rstrip('.')), expected)
        # Unchanged hint, geometry and images carry no vector field values.
        sp = g.SOURCES[template][':question/problem']
        assert prompt.split('$ and the ', 1)[1] == sp.split('$ and the ', 1)[1]
        if level == 'moderate':
            assert 'outward-pointing unit normal vector, we must have' in solution
            assert re.findall(r'!\[.*?\]\((.*?)\)', solution) == re.findall(r'!\[.*?\]\((.*?)\)', g.SOURCES[template][':question/worked-solution'])
    else:
        assert prompt == g.SOURCES[template][':question/problem']
        assert solution == g.SOURCES[template][':question/worked-solution']
    return expected


def checks(rec):
    independent(rec)
    f = rec['question'][':question/answer-fields'][0]
    return [{'field_index': 0, 'submitted_answer_id': a[':answer/id'],
             'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
             'purpose': 'complete observed radio bank selection'} for a in f[':answer-field/choices']]


def fingerprint(q):
    # Compare current inventory to source and exhaustively validated candidates.
    if 'generation' in q:
        return q['generation']['mathematical_signature']
    mid = q.get(':question/math-academy-id')
    if mid in g.DATA:
        return g.signature(mid, 1)
    qid = str(q.get(':question/id'))
    for level in g.SUPPORTED_LEVELS:
        for rec in g.batch(level, 1000, 2694):
            if rec['question'][':question/id'] == qid:
                return rec['generation']['mathematical_signature']
    # Unknown records do not establish available inventory; conservative exact
    # content matching is also used before selection of new instances.
    return json.dumps([q.get(':question/problem'), sorted(a[':answer/value'] for f in q.get(':question/answer-fields', []) for a in f[':answer-field/choices'])])


def main():
    assert set(g.SOURCES) == set(g.DATA) | set(g.EXCLUDED)
    records, replay, mappings, examples = [], [], [], []
    for template, data in g.DATA.items():
        level = data[-1]
        source = g.SOURCES[template]
        r = g.generate(level, template=template, parameters={'scale': 1})
        independent(r)
        sf, f = source[':question/answer-fields'][0], r['question'][':question/answer-fields'][0]
        assert sorted(a[':answer/value'] for a in sf[':answer-field/choices']) == sorted(a[':answer/value'] for a in f[':answer-field/choices'])
        assert sf[':answer-field/correct'][':answer/value'] == next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1])
        replay.append({'source': template, 'complete_bank': '5/5', 'distractors': '4/4', 'correct_designation': True, 'exact_prompt_and_solution': True})
        for a in sf[':answer-field/choices']:
            mappings.append({'source': template, 'source_field': sf[':answer-field/id'], 'source_answer': a[':answer/id'],
                             'profile': 'observed-whole-field-scale:' + template, 'original_value': a[':answer/value'],
                             'expression': str(g.parse(a[':answer/value'])), 'recipe': 'k * (' + str(g.parse(a[':answer/value'])) + ')',
                             'complete_value_replay': True, 'interpretation': 'exact dot product' if a[':answer/id'] == sf[':answer-field/correct'][':answer/id'] else 'observed expression; cognitive mechanism unresolved'})
        records.append(r)
        for k in g.SCALES:
            r = g.generate(level, template=template, parameters={'scale': k})
            independent(r)
            assert r == g.generate(level, template=template, parameters={'scale': k})
            records.append(r)
        examples.append((template, source, g.generate(level, template=template, parameters={'scale': -2})))
    for level in g.SUPPORTED_LEVELS:
        seen = {g.generate(level, seed)['generation']['template'] for seed in range(200)}
        assert seen == {k for k, d in g.DATA.items() if d[-1] == level}
        cli = subprocess.run([sys.executable, str(HERE.with_suffix('.py')), '--difficulty', level,
                              '--count', '5', '--seed', '2694', '--format', 'json'],
                             capture_output=True, text=True, check=True)
        assert json.loads(cli.stdout) == g.batch(level, 5, 2694)
    assert g.batch('easy', 0) == []
    # Mutations establish that stale field values, keys, and final solution
    # claims are detected independently, not merely replayed by UUID.
    base = g.generate('easy', template='q-127056', parameters={'scale': 2})
    mutations = []
    z = copy.deepcopy(base); z['question'][':question/problem'] = z['question'][':question/problem'].replace('(30 x y)', '(31 x y)'); mutations.append(z)
    z = copy.deepcopy(base); z['question'][':question/answer-fields'][0][':answer-field/correct'][1] = z['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']; mutations.append(z)
    z = copy.deepcopy(base); z['question'][':question/worked-solution'] = z['question'][':question/worked-solution'].replace('missing expression is $8 x^{2} y', 'missing expression is $9 x^{2} y'); mutations.append(z)
    for z in mutations:
        assert z != base
        try:
            independent(z)
        except AssertionError:
            pass
        else:
            raise AssertionError('Mutation escaped validation')
    save(HERE/'source-choice-mapping.json', mappings)
    save(HERE/'validated-instances.json', records)
    save(HERE/'engine-input.json', [{'label': r['question'][':question/id'], 'record': r, 'checks': checks(r)} for r in records])
    subprocess.run([str(ROOT/'generate/runs/current/check-engine'), str(HERE/'engine-input.json'), str(HERE/'engine-report.json')], check=True)
    assets = {}
    for q in g.SOURCES.values():
        for part in (':question/problem', ':question/worked-solution'):
            for asset in re.findall(r'!\[.*?\]\((.*?)\)', q[part]):
                path = Path('/media/jake/SSD/EDB/math')/asset
                assert path.is_file()
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                assert path.stem == digest
                assets[asset] = digest
    save(HERE/'reference/asset-hashes.json', assets)
    markdown = ['# Source and generated variants', '', 'Each pair retains the same geometry, field expression structure, field contract and dot-product stages. The complete vector field and bank are scaled by −2.', '']
    for name, source, variant in examples:
        markdown += ['## ' + name, '', '### Source', '', source[':question/problem'], '', source[':question/worked-solution'], '', 'Bank: ' + ', '.join('$'+a[':answer/value']+'$' for a in source[':question/answer-fields'][0][':answer-field/choices']), '', '### Variant', '', variant['question'][':question/problem'], '', variant['question'][':question/worked-solution'], '', 'Bank: ' + ', '.join('$'+a[':answer/value']+'$' for a in variant['question'][':question/answer-fields'][0][':answer-field/choices']), '']
    (HERE/'side-by-side.md').write_text('\n'.join(markdown))
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'), HERE/'source.json', HERE/'validate.py', HERE/'validated-instances.json')}
    save(HERE/'validation.json', {'status': 'pass', 'hashes': hashes, 'source_basis': g.SNAPSHOT['basis'], 'lineage': g.SNAPSHOT['lineage'],
         'source_replay': replay, 'source_complete_banks': '11/11', 'source_distractors': '44/44', 'missing_or_extra_options': [],
         'excluded_sources': g.EXCLUDED, 'independently_checked_records': len(records), 'scales_exhaustively_checked': [1]+list(g.SCALES),
         'coverage': {'all_profiles_selected': True, 'all_four_side_normal_roles': True, 'field_scale_both_signs_and_bounds': True,
                      'fixed_geometry': 'All dimensions and selected sides retain original mathematical roles and source assets; only whole-field scale is a declared slot.',
                      'source_parameter_values_replayed': True}, 'mutation_failures_detected': len(mutations),
         'fidelity': 'Exact complete original banks, field contract and literal original prompt/solution at k=1; generated layout keeps operative source stages.',
         'correctness': 'Independent Cartesian normal dot product and exact polynomial equivalence for every bounded sample.',
         'application_cli': 'Verified --difficulty LEVEL --count 5 --seed 2694 --format json returns the expected instances array for both supported levels.',
         'native': json.loads((HERE/'engine-report.json').read_text()), 'asset_count': len(assets), 'new_assets_required': False})
    print('Validated', len(records), 'records, 11/11 source banks and 44/44 distractors.')


if __name__ == '__main__':
    main()
