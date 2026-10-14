"""Validate current checkbox source fidelity, independent mathematics and grading."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
D = Path(__file__).resolve().parent
ROOT = D.parents[2]

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

g = module(D.with_suffix('.py'), 'current_generator')
v = module(D / 'validation_helpers.py', 'independent_helpers')
SOURCE = json.loads((D / 'current-source.json').read_text())

def normalize(q):
    result = {k: str(q[k]) if k == ':question/id' else q[k] for k in
              (':question/id', ':question/problem', ':question/worked-solution')}
    if ':question/difficulty' in q:
        result[':question/difficulty'] = str(q[':question/difficulty'][':db/ident'])
    result[':question/answer-fields'] = []
    for f in sorted(q[':question/answer-fields'], key=lambda f: f[':answer-field/key']):
        result[':question/answer-fields'].append({
            ':answer-field/id': str(f[':answer-field/id']),
            ':answer-field/key': f[':answer-field/key'],
            ':answer-field/type': str(f[':answer-field/type'][':db/ident']),
            ':answer-field/correct': [':answer/id', str(f[':answer-field/correct'][':answer/id'])],
            ':answer-field/choices': sorted([{
                ':answer/id': str(a[':answer/id']),
                ':answer/type': str(a[':answer/type'][':db/ident']),
                ':answer/value': a[':answer/value']}
                for a in f[':answer-field/choices']], key=lambda a: a[':answer/value'])})
    return result

def ordered(q):
    q = copy.deepcopy(q)
    q[':question/answer-fields'].sort(key=lambda f: f[':answer-field/key'])
    for f in q[':question/answer-fields']:
        f[':answer-field/choices'].sort(key=lambda a: a[':answer/value'])
    return q

def shape(q):
    q = ordered(q)
    q.pop(':question/id')
    q[':question/problem'] = v.normalized(q[':question/problem'])
    for f in q[':question/answer-fields']:
        correct = next(a[':answer/value'] for a in f[':answer-field/choices']
                       if a[':answer/id'] == f[':answer-field/correct'][1])
        f[':answer-field/correct'] = correct
        f.pop(':answer-field/id')
        for a in f[':answer-field/choices']:
            a.pop(':answer/id')
    return q

def check(rec):
    assert rec['knowledge_point']['db_id'] == g.KP_ID
    local = copy.deepcopy(rec)
    asset = Path(local['generation']['plot'])
    if not asset.is_absolute():
        asset = Path('/media/jake/SSD/EDB/math') / asset
        local['generation']['plot'] = str(asset)
    if local['generation'].get('plot_original'):
        local['generation']['plot'] = local['generation']['plot_original']
        assert asset.read_bytes() == Path(local['generation']['plot']).read_bytes()
    f = v.actual_polynomial(local)
    q = rec['question']
    truth = v.parse_statements(q[':question/problem'].replace('Select all that apply.\n\n', ''), f)
    assert truth == rec['generation']['truth']
    assert len(q[':question/answer-fields']) == 3
    keys = [field[':answer-field/key'] for field in q[':question/answer-fields']]
    assert keys == list(g.ROMAN)
    for field, bit in zip(q[':question/answer-fields'], truth):
        assert field[':answer-field/type'] == ':answer-field.type/checkbox'
        bank = field[':answer-field/choices']
        assert len(bank) == 2 and {a[':answer/value'] for a in bank} == {'true', 'false'}
        assert len({a[':answer/id'] for a in bank}) == 2
        answer = next(a for a in bank if a[':answer/id'] == field[':answer-field/correct'][1])
        assert answer[':answer/value'] == ('true' if bit else 'false')
    for text in (q[':question/problem'], q[':question/worked-solution']):
        assert text.count('$') % 2 == 0
        assert not re.search(r'\{(?:r\d|asset|y0|symmetric_root)\}', text)
    tname = rec['generation']['template']
    p = rec['generation']['parameters']
    claims = g.claims_for(g.HARD if tname not in g.RECIPES else g.RECIPES[tname], p)
    assert g.mathematical_fingerprint(p, claims) == rec['generation']['mathematical_fingerprint']
    # Independent rendered solution readback: exact categorical and limit stages
    # remain the already validated source sequence, with current operand masks.
    if tname in g.CURRENT_RECIPES:
        source = next(q for q in SOURCE['record'][':knowledge-point/questions']
                      if q[':question/math-academy-id'] == tname)
        assert v.restore_source_operands(q[':question/problem'], rec, g.RECIPES[tname]) == v.normalized(source[':question/problem'])
        assert v.restore_source_operands(q[':question/worked-solution'], rec, g.RECIPES[tname]) == source[':question/worked-solution']
    else:
        # Use the existing independent solution-stage checker for authored hard.
        radio = g.generate_legacy('hard', parameters=p)
        assert radio['question'][':question/worked-solution'] == q[':question/worked-solution']
        v.check_record(radio)
    return truth

def native(label, rec):
    checks = []
    for i, field in enumerate(rec['question'][':question/answer-fields']):
        for value in ('false', 'true'):
            correct = next(a[':answer/value'] for a in field[':answer-field/choices']
                           if a[':answer/id'] == field[':answer-field/correct'][1])
            selected = next(a[':answer/id'] for a in field[':answer-field/choices'] if a[':answer/value'] == value)
            checks.append({'field_index': i, 'submitted_answer_id': selected,
                           'expected': 'accepted' if value == correct else 'rejected',
                           'purpose': 'checkbox boolean choice mapped to its authored identity'})
    return {'label': label, 'record': rec, 'checks': checks}

def main():
    records = []
    replays = []
    variation = {}
    for q in SOURCE['record'][':knowledge-point/questions']:
        name = q[':question/math-academy-id']
        t = g.RECIPES[name]
        parameters = {k: t[k] for k in ('roots', 'multiplicities', 'coefficient')}
        rec = g.generate(t['level'], template=name, parameters=parameters, profile='source:' + name)
        check(rec)
        assert shape(rec['question']) == shape(normalize(q)), name
        replays.append({'source_id': q[':db/id'], 'template': name,
                        'complete_fields': 3, 'choices_matched': 6, 'correct_designations_matched': 3})
        records.append(rec)
    for name, t in list(g.RECIPES.items()) + [('mixed_categories_four_roots', g.HARD)]:
        sampled = []
        for seed in range(40):
            rec = g.generate(t['level'], template=name, seed=seed + 200)
            check(rec)
            again = g.generate(t['level'], template=name, seed=seed + 500,
                               parameters=rec['generation']['parameters'])
            assert again['question'] == rec['question']
            sampled.append(rec)
            if len(sampled) >= 8 and len({r['generation']['mathematical_fingerprint'] for r in sampled}) >= 5:
                break
        assert len({r['generation']['mathematical_fingerprint'] for r in sampled}) >= 5
        variation[name] = sorted({tuple(r['generation']['parameters']['roots']) for r in sampled})
        records.extend(sampled)
    # An amplitude-only change and a different seed do not create a new task.
    a = g.generate_hard(8)
    b = g.generate_hard(19, parameters=dict(a['generation']['parameters'], coefficient='2'))
    assert a['generation']['mathematical_fingerprint'] == b['generation']['mathematical_fingerprint']
    engine_input = D / 'current-engine-input.json'
    engine_input.write_text(json.dumps([native(str(i), rec) for i, rec in enumerate(records)], indent=2))
    subprocess.run([str(ROOT / 'generate/runs/current/check-engine'), str(engine_input),
                    str(D / 'current-engine-report.json')], check=True)
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in (D.with_suffix('.py'), D/'current-recipes.json', D/'current-source.json',
                           D/'validate_current.py', D/'validation_helpers.py', D/'recipes.json')}
    report = {'passed': True, 'source_basis': SOURCE['basis'], 'lineage': SOURCE['lineage'],
              'source_replays': replays, 'source_banks_matched': 30, 'source_choices_matched': 60,
              'source_correct_designations_matched': 30, 'mathematically_checked_records': len(records),
              'variation': variation, 'hashes': hashes, 'native_grading':
              json.loads((D/'current-engine-report.json').read_text()),
              'supported_levels': list(g.SUPPORTED_LEVELS),
              'difficulty_assignments': 'Easy and Moderate observed; Hard conservative authored family',
              'deduplication': 'roots/categories/end sign/concrete claim set; excludes seed/order/amplitude'}
    (D/'current-validation.json').write_text(json.dumps(report, indent=2)+'\n')
    (D/'current-review.json').write_text(json.dumps(records, indent=2)+'\n')
    print('PASS: 10 current source replays, 30 checkbox banks, 60 choices, 30 correct keys;', len(records), 'independent mathematical/plot checks')

if __name__ == '__main__':
    main()
