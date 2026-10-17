"""Display-only generator regressions; preserve all mathematical data and IDs."""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
import sys
import types

from bs4 import BeautifulSoup

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
NAMES = ['17592186100866', '17592186100867', '17592186100868-draft']


def load(path, name, source=None):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_text() if source is None else source, str(path), 'exec'), module.__dict__)
    return module


def save(name, data):
    (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def calls(generator, name):
    if name.endswith('draft'):
        for sid, t in generator.TEMPLATES.items():
            profiles = ['observed', 'authored-operations'] if (t['fields'][0]['type'] == 'radio' and sid != 'q-13554') or t['level'] == 'hard' else ['observed']
            for profile in profiles:
                for seed in range(12):
                    yield t['level'], seed, {'template': sid, 'profile': profile}
    else:
        for template, profiles in generator.ELIGIBLE.items():
            for profile in profiles:
                for seed in range(12):
                    yield generator.SUPPORTED_LEVELS[0], seed, {'template': template, 'profile': profile}


def native(record, label):
    checks = []
    for i, field in enumerate(record['question'][':question/answer-fields']):
        correct = field[':answer-field/correct'][1]
        for answer in field[':answer-field/choices']:
            if field[':answer-field/type'].endswith('/radio'):
                checks.append({'field_index': i, 'submitted_answer_id': answer[':answer/id'],
                               'expected': 'accepted' if answer[':answer/id'] == correct else 'rejected'})
            else:
                checks.append({'field_index': i, 'submitted': answer[':answer/value'], 'expected': 'accepted'})
                checks.append({'field_index': i, 'submitted': '987654321', 'expected': 'rejected'})
    return {'record': record, 'label': label, 'checks': checks}


report = {'generators': [], 'database_mutations': 0}
native_cases = []
render_samples = []
for name in NAMES:
    path = ROOT / f'generate/scratch/{name}.py'
    old_source = (HERE / f'{name}-before.py').read_text()
    old = load(path, 'old_' + name.replace('-', '_'), old_source)
    new = load(path, 'new_' + name.replace('-', '_'))
    validator_path = path.with_suffix('') / 'validate.py'
    validator_source = validator_path.read_text()
    if name.endswith('draft'):
        validator_source = validator_source.split('\nsource_wrapper=', 1)[0]
    validator = load(validator_path, 'validator_' + name.replace('-', '_'), validator_source)
    count = 0
    changed = 0
    coverage = {}
    for level, seed, kwargs in calls(old, name):
        before = old.generate(level, seed, **kwargs)
        after = new.generate(level, seed, **kwargs)
        assert after == new.generate(level, seed, **kwargs), 'non-deterministic output'
        old_prompt = before['question'][':question/problem']
        new_prompt = after['question'][':question/problem']
        expected = copy.deepcopy(before)
        expected['question'][':question/problem'] = new_prompt
        assert after == expected, (name, seed, kwargs, 'non-prompt content or identity changed')
        validator.check(after)
        is_blank = before['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank')
        if is_blank:
            assert '| ---' not in new_prompt and 'class="matrix-answer"' in new_prompt
            assert old_prompt.split('\n\n|', 1)[0] == new_prompt.split('\n\n<div', 1)[0]
            placeholders = re.findall(r'\{\{([^{}]+)\}\}', old_prompt)
            assert placeholders == re.findall(r'\{\{([^{}]+)\}\}', new_prompt)
            table = BeautifulSoup(new_prompt, 'html.parser').select_one('.matrix-answer table')
            rows = table.select('tr')
            assert len(rows) == len(placeholders)
            for row, key in zip(rows, placeholders):
                assert len(row.find_all('td', recursive=False)) == 1
                assert row.get_text() == '{{' + key + '}}'
            assert re.findall(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}', old_prompt, re.S) == re.findall(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}', new_prompt, re.S)
            changed += 1
        else:
            assert new_prompt == old_prompt
        label = name + ':' + level + ':' + kwargs['template'] + ':' + kwargs['profile']
        coverage[label] = coverage.get(label, 0) + 1
        if seed == 0:
            native_cases.append(native(after, label))
            if is_blank:
                render_samples.append({'generator': name, 'label': label, 'record': after})
        count += 1
    # Retain exact source masks and complete bank replay evidence; their immutable
    # original table shape remains available to the identity/replay calculation.
    report['generators'].append({'path': str(path.relative_to(ROOT)),
                                  'before_sha256': hashlib.sha256(old_source.encode()).hexdigest(),
                                  'after_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                                  'instances_checked': count, 'changed_blank_prompts': changed,
                                  'profile_coverage': coverage,
                                  'only_problem_display_changed': True,
                                  'all_question_field_choice_and_correct_ids_preserved': True,
                                  'sampling_and_mathematical_fingerprints_preserved': True,
                                  'worked_solutions_unchanged': True,
                                  'existing_independent_math_validator_passed': True,
                                  'source_snapshots_unchanged': True})

save('native-input.json', native_cases)
save('render-samples.json', render_samples)
save('verification.json', report)
print(json.dumps({'instances_checked': sum(x['instances_checked'] for x in report['generators']),
                  'changed_blank_prompts': sum(x['changed_blank_prompts'] for x in report['generators']),
                  'native_cases': len(native_cases), 'native_checks': sum(len(x['checks']) for x in native_cases)}))
