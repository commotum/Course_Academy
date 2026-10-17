"""Focused before/after validation; all durable outputs stay in this repair."""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys
import types

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
SCRIPTS = ['17592186100869-draft', '17592186100870', '17592186100871']
registrations = json.loads((HERE / 'registrations.json').read_text())
active = {row[0][':knowledge-point/question-generator'][':question-generator/script'] for row in registrations['rows']}


def load(path, name, source=None):
    m = types.ModuleType(name)
    m.__file__ = str(path)
    sys.modules[name] = m
    exec(compile(path.read_text() if source is None else source, str(path), 'exec'), m.__dict__)
    return m


def save(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def native(record, label):
    checks = []
    for i, f in enumerate(record['question'][':question/answer-fields']):
        correct = f[':answer-field/correct'][1]
        for answer in f[':answer-field/choices']:
            if f[':answer-field/type'].endswith('/blank'):
                checks.extend([{'field_index': i, 'submitted': answer[':answer/value'], 'expected': 'accepted'},
                               {'field_index': i, 'submitted': '987654321', 'expected': 'rejected'}])
            else:
                checks.append({'field_index': i, 'submitted_answer_id': answer[':answer/id'],
                               'expected': 'accepted' if answer[':answer/id'] == correct else 'rejected'})
    return {'label': label, 'record': record, 'checks': checks}


report = {'database_writes': 0, 'generators': []}
native_cases = []
render_samples = []
for name in SCRIPTS:
    path = ROOT / f'generate/scratch/{name}.py'
    assert str(path.relative_to(ROOT)) in active
    old_source = (HERE / 'before' / path.name).read_text()
    old = load(path, 'before_' + name.replace('-', '_'), old_source)
    new = load(path, 'after_' + name.replace('-', '_'))
    vp = path.with_suffix('') / 'validate.py'
    vs = vp.read_text()
    if name.endswith('draft'):
        vs = vs.split('\nsources=[]', 1)[0]
    validator = load(vp, 'validator_' + name.replace('-', '_'), vs)
    configs = []
    if name.endswith('draft'):
        configs = [(old.source_level(mid), mid) for mid in old.SOURCES] + [('hard', 'mixed-orientations')]
        check = validator.read_display
    elif name.endswith('870'):
        configs = [(old.level_of(mid), mid) for mid in old.DEFAULTS]
        check = validator.independent
    else:
        configs = [(t['level'], mid) for mid, t in old.TEMPLATES.items()]
        check = validator.audit
    count = changed = raw = 0
    coverage = {}
    for level, template in configs:
        for seed in range(12):
            before = old.generate(level, seed, template=template)
            after = new.generate(level, seed, template=template)
            assert after == new.generate(level, seed, template=template)
            expected = copy.deepcopy(before)
            expected['question'][':question/problem'] = after['question'][':question/problem']
            assert expected == after, (name, template, seed, 'non-prompt content or identity changed')
            check(after)
            a = before['question'][':question/problem']
            b = after['question'][':question/problem']
            assert re.findall(r'\{\{[^{}]+\}\}', a) == re.findall(r'\{\{[^{}]+\}\}', b)
            assert re.findall(r'([A-Z])\s*=\s*(\\begin\{bmatrix\}.*?\\end\{bmatrix\})', a, re.S) == re.findall(r'([A-Z])\s*=\s*(\\begin\{bmatrix\}.*?\\end\{bmatrix\})', b, re.S)
            if name.endswith('draft') or name.endswith('871'):
                assert 'matrix-operands' in b
            if '{{field-1}}' in b:
                assert 'are <span' in b and 'display: inline-flex' in b and '$\\times$' in b
            count += 1
            changed += a != b
            coverage[level + ':' + template] = coverage.get(level + ':' + template, 0) + 1
            if seed == 0:
                label = name + ':' + level + ':' + template
                native_cases.append(native(after, label))
                if a != b:
                    render_samples.append({'generator': name, 'label': label, 'record': after})
    if name.endswith('draft'):
        for case in json.loads((path.with_suffix('') / 'source-cases.json').read_text()):
            kwargs = {'template': case['template'], 'parameters': case['parameters'], 'profile': case['bank_profile']}
            before = old.generate(case['level'], **kwargs)
            after = new.generate(case['level'], **kwargs)
            assert before == after
            validator.read_display(after)
            raw += 1
    if name.endswith('871'):
        for level, mid in configs:
            before = old.generate(level, template=mid, replay=True)
            after = new.generate(level, template=mid, replay=True)
            assert before == after
            validator.audit(after)
            raw += 1
    report['generators'].append({'script': str(path.relative_to(ROOT)), 'registration_basis': registrations['identity']['basis'],
        'active_registration_verified': True, 'before_sha256': hashlib.sha256(old_source.encode()).hexdigest(),
        'after_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'instances_checked': count,
        'changed_prompts': changed, 'raw_source_replays_unchanged': raw, 'coverage': coverage,
        'only_learner_prompt_display_changed': True, 'question_field_choice_and_correct_identities_unchanged': True,
        'solutions_sampling_difficulty_and_all_metadata_unchanged': True, 'existing_independent_math_validator_passed': True})

save('verification.json', report)
save('native-input.json', native_cases)
save('render-samples.json', render_samples)
print(json.dumps({'instances': sum(g['instances_checked'] for g in report['generators']),
                  'changed_prompts': sum(g['changed_prompts'] for g in report['generators']),
                  'raw_replays': sum(g['raw_source_replays_unchanged'] for g in report['generators']),
                  'native_cases': len(native_cases), 'native_checks': sum(len(c['checks']) for c in native_cases)}))
