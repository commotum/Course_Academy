"""Independent diagram-sign, rendered-claim, source-bank and native grading checks."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('flux_catalog', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

# Independently read from the inspected original diagrams, not from answer keys.
OBSERVATIONS = {
    'q-126726': ('circle', 'outward'), 'q-126728': ('circle', 'tangent'),
    'q-127025': ('ellipse', 'outward'), 'q-127029': ('circle', 'tangent'),
    'q-127030': ('ellipse', 'balanced-saddle'), 'q-127032': ('ellipse', 'tangent'),
    'q-127026': ('ellipse', 'outward'), 'q-127024': ('circle', 'inward'),
    'q-127027': ('ellipse', 'outward'), 'q-127028': ('circle', 'balanced-saddle')}


def write(path, value):
    path.write_text(json.dumps(value, indent=2, default=str) + '\n')


def flux_proofs():
    """Representative fields verify the visually identified relationships.

    These equations model the qualitative diagrams; they do not claim to recover
    exact field coefficients or dimensions from unscaled pixels. Outward n ds
    is geometric and does not change when traversal is reversed.
    """
    t = sp.symbols('t', real=True)
    a, b = sp.symbols('a b', positive=True)
    x, y = a * sp.cos(t), b * sp.sin(t)
    normal_ds = sp.Matrix([b * sp.cos(t), a * sp.sin(t)])
    fields = {'outward': sp.Matrix([x, y]), 'inward': sp.Matrix([-x, -y]),
              'tangent': sp.Matrix([a * y / b, -b * x / a]),
              'balanced-saddle': sp.Matrix([x, -y])}
    proofs = {}
    for family, field in fields.items():
        dot = sp.trigsimp(field.dot(normal_ds))
        integral = sp.simplify(sp.integrate(dot, (t, 0, 2 * sp.pi)))
        expected = {'outward': 2 * sp.pi * a * b, 'inward': -2 * sp.pi * a * b,
                    'tangent': 0, 'balanced-saddle': 0}[family]
        assert sp.simplify(integral - expected) == 0
        if family == 'tangent':
            assert dot == 0
        proofs[family] = {'representative_field': str(field), 'normal_ds': str(normal_ds),
                          'dot': str(dot), 'integral': str(integral),
                          'sign': {'outward': 'positive', 'inward': 'negative'}.get(family, 'zero')}
    return proofs


def check(rec):
    t = rec['generation']['template']
    q = rec['question']
    assert t in OBSERVATIONS
    assert rec['knowledge_point'] == {'db_id': g.KP_ID, 'id': g.KP_UUID, 'title': g.TITLE}
    assert q == g.normalize(g.QUESTIONS[t]), 'Finite output must reuse the exact source identity/content'
    z = g.SPECS[t]
    shape, family = OBSERVATIONS[t]
    assert (z['shape'], z['relation']) == (shape, family)
    assert ('ellipse' if 'ellipse' in q[':question/problem'] else 'circle') == shape
    claims = re.findall(r'The flux of \$F\$ across \$(C|-C)\$ is (positive|negative|zero)', q[':question/problem'])
    assert [dict(path=p, sign=s) for p, s in claims] == z['claims'] and len(claims) == 3
    sign = {'outward': 'positive', 'inward': 'negative'}.get(family, 'zero')
    expected = [s == sign for _, s in claims]
    fields = q[':question/answer-fields']
    assert [f[':answer-field/key'] for f in fields] == ['I', 'II', 'III']
    for f, truth in zip(fields, expected):
        assert f[':answer-field/type'] == ':answer-field.type/checkbox'
        choices = f[':answer-field/choices']
        assert len(choices) == 2 and {a[':answer/value'] for a in choices} == {'true', 'false'}
        assert all(a[':answer/type'] == ':answer.type/text' for a in choices)
        assert len({a[':answer/id'] for a in choices}) == 2
        selected = [a[':answer/value'] for a in choices if a[':answer/id'] == f[':answer-field/correct'][1]]
        assert selected == [str(truth).lower()]
    solution = q[':question/worked-solution']
    final = re.search(r'correct answer is "(.*?)"', solution)[1]
    assert re.findall(r'\b(?:III|II|I)\b', final) == [k for k, v in zip(('I', 'II', 'III'), expected) if v]
    for roman, truth in re.findall(r'Statement (III|II|I) is (true|false)', solution):
        assert (truth == 'true') == expected[('I', 'II', 'III').index(roman)]
    for roman, truth in re.findall(r'while statement (III|II|I) is (true|false)', solution):
        assert (truth == 'true') == expected[('I', 'II', 'III').index(roman)]
    equations = re.findall(r'\\text\{d\}s([<>=])0', solution)
    assert len(equations) == 2 and set(equations) == {{'positive': '>', 'negative': '<', 'zero': '='}[sign]}
    assert 'orientation of the curve does not matter' in solution
    if family == 'tangent':
        assert 'perpendicular to $n$ at every point' in solution
    if family == 'balanced-saddle':
        assert re.search(r'flows in through \$C\$ is the same that flows out through \$C\.?\$', solution)
    assert rec['generation']['mathematical_fingerprint'] == g.fingerprint(t)
    assert rec['generation']['novel_variant'] is False and rec['generation']['existing_identity_reused']
    assert q[':question/difficulty'] == ':question.difficulty/' + z['level']
    for text in (q[':question/problem'], solution):
        assert text.count('$') % 2 == 0 and text.count('{') == text.count('}')
        assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', text)
    return expected


def grade(records, path):
    path.mkdir(parents=True, exist_ok=True)
    items = []
    for r in records:
        checks = []
        for i, f in enumerate(r['question'][':question/answer-fields']):
            for a in f[':answer-field/choices']:
                checks.append({'field_index': i, 'submitted_answer_id': a[':answer/id'],
                               'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
                               'purpose': 'Actual checkbox grading for every owned true/false answer'})
        items.append({'label': r['generation']['template'], 'record': r, 'checks': checks})
    write(path / 'native-input.json', items)
    result = subprocess.run([str(HERE / 'check-engine'), str(path / 'native-input.json'),
                             str(path / 'native-report.json')], capture_output=True, text=True, check=True, timeout=55)
    (path / 'native.log').write_text(result.stdout + result.stderr)
    report = json.loads((path / 'native-report.json').read_text())
    assert report['accepted_checks'] == report['rejected_checks'] == 3 * len(records)
    assert report['documented_unresolved_checks'] == 0
    return report


def main():
    proofs = flux_proofs()
    records, fidelity, components, assets = [], [], [], {}
    for template, level in sorted(g.TEMPLATES.items()):
        rec = g.generate(level, seed=20261015, template=template)
        expected = check(rec)
        assert rec['question'] == g.generate(level, seed=98765, template=template)['question']
        records.append(rec)
        src = g.QUESTIONS[template]
        fidelity.append({'source_id': template, 'difficulty': level, 'complete_banks_matched': 3,
                         'complete_banks_total': 3, 'options_matched': 6, 'options_total': 6,
                         'correct_designations_matched': 3, 'missing_options': [], 'extra_options': [],
                         'prompt_solution_exact': True, 'existing_uuids_reused': True})
        components.append({'source_id': template, 'source_uuid': src[':question/id'],
                           'backbone': g.SPECS[template], 'variable_slots': [],
                           'question': rec['question'], 'independent_truths': expected,
                           'choice_mapping': [{'field': f[':answer-field/key'], 'source_answer_id': a[':answer/id'],
                                               'exact_value': a[':answer/value'], 'recipe': 'literal Boolean ' + a[':answer/value'],
                                               'profile': 'three-checkbox-true-false'}
                                              for f in rec['question'][':question/answer-fields'] for a in f[':answer-field/choices']]})
    # Verify all references, including the excluded canonical example, by bytes.
    from PIL import Image
    for q in list(g.QUESTIONS.values()) + [g.SOURCE['record'][':knowledge-point/canonical-example']]:
        for ref in re.findall(r'!\[.*?\]\((.*?)\)', q[':question/problem'] + '\n' + q[':question/worked-solution']):
            path = Path('/media/jake/SSD/EDB/math') / ref
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            assert digest == path.stem
            with Image.open(path) as im:
                im.verify()
            with Image.open(path) as im:
                assets[ref] = {'sha256': digest, 'dimensions': list(im.size), 'reused_unchanged': True}
    capacities = {}
    for level in g.SUPPORTED_LEVELS:
        batch = g.batch(level, 1000, 20261015)
        assert len(batch) == len({r['generation']['mathematical_fingerprint'] for r in batch}) == 5
        capacities[level] = len(batch)
        assert g.batch(level, 0) == []
        assert g.batch(level, 5, 12) == g.batch(level, 5, 12)
    for level, params, template in [('hard', None, None), ('easy', {'scale': 2}, None),
                                     ('easy', None, 'q-126728')]:
        try:
            g.generate(level, parameters=params, template=template)
        except ValueError:
            pass
        else:
            raise AssertionError('Unsupported level, scale or template accepted')
    bad = copy.deepcopy(records[0])
    f = bad['question'][':question/answer-fields'][0]
    f[':answer-field/correct'][1] = next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id'] != f[':answer-field/correct'][1])
    try:
        check(bad)
    except AssertionError:
        pass
    else:
        raise AssertionError('Wrong key mutation escaped validation')
    # Shuffled claims/field keys and seed cannot create another fingerprint.
    assert len({g.fingerprint(t) for t in g.TEMPLATES}) == 10
    native = grade(records, HERE / 'reference/validation')
    write(HERE / 'source-components.json', components)
    write(HERE / 'source-fidelity.json', fidelity)
    write(HERE / 'reference/assets.json', assets)
    write(HERE / 'reference/flux-proofs.json', proofs)
    write(HERE / 'review.json', [{'source': g.QUESTIONS[r['generation']['template']], 'catalog_replay': r} for r in records])
    (HERE / 'review.md').write_text('\n\n---\n\n'.join('## ' + r['generation']['template'] + '\n\nOriginal and exact catalog replay (same existing identity):\n\n' + g.markdown(r) for r in records) + '\n')
    report = {'status': 'passed', 'version': g.VERSION,
              'script_sha256': hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),
              'source_basis': g.SOURCE['basis'], 'lineage': g.SOURCE['lineage'],
              'source_replay': {'questions': 10, 'complete_banks_matched': 30, 'complete_banks_total': 30,
                                'options_matched': 60, 'options_total': 60, 'correct_designations_matched': 30,
                                'prompt_solution_exact': True, 'missing_options': [], 'extra_options': []},
              'mathematics': {'diagram_observations': OBSERVATIONS, 'representative_exact_proofs': proofs,
                              'rendered_claim_truths_checked': 30, 'worked_solution_flux_signs_checked': 20,
                              'wrong_key_mutation_rejected': True, 'coefficient_inference_from_pixels': False},
              'grading': {'accepted': native['accepted_checks'], 'rejected': native['rejected_checks'], 'unresolved': 0,
                          'build': json.loads((HERE / 'check-engine-build.json').read_text())},
              'supported_levels': list(g.SUPPORTED_LEVELS), 'unsupported_levels': ['hard'],
              'finite_catalog': capacities, 'additional_distinct_tasks_at_source_basis': 0,
              'variable_slots': [], 'deterministic_identity': True, 'seed_does_not_change_question': True,
              'changed_target_test': 'Not applicable: this bounded package fixes complete source situations; new targets are rejected.',
              'plots': {'new_required': False, 'existing_assets_verified': sorted(assets)},
              'sympy': sp.__version__, 'database_writes': 0}
    write(HERE / 'validation.json', report)
    print(json.dumps({'status': report['status'], 'source_replay': report['source_replay'],
                      'native_accepted': native['accepted_checks'], 'native_rejected': native['rejected_checks']}))


if __name__ == '__main__':
    main()
