#!/usr/bin/env python3
"""Regression for the x-only coordinate repair. Does not access the database."""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FOLDER = HERE.parent
SCRIPT = FOLDER.with_suffix('.py')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


g = load(SCRIPT, 'x_only_generator')
old = load(HERE / 'before.py', 'before_x_only_generator')
validator = load(FOLDER / 'validate.py', 'x_only_validator')
validator.g = g


def replace_variable(value, variable):
    return re.sub(r'(?<![A-Za-z\\])' + variable + r'(?![A-Za-z])', 'x', value)


def content(record, rename=False):
    q = copy.deepcopy(record['question'])
    variable = record['generation']['parameters']['variable']
    if rename and variable != 'x':
        for attr in (':question/problem', ':question/worked-solution'):
            if attr not in q:
                continue
            q[attr] = q[attr].replace(f'\n\nLet ${variable}=x$ be the free coordinate.', '')
            q[attr] = re.sub(r'\$\$(.*?)\$\$|(?<!\$)\$([^$]*?)\$(?!\$)',
                             lambda m: replace_variable(m[0], variable), q[attr], flags=re.S)
        for field in q[':question/answer-fields']:
            for answer in field.get(':answer-field/choices', []):
                answer[':answer/value'] = replace_variable(answer[':answer/value'], variable)
    fields = []
    for field in q[':question/answer-fields']:
        correct = field.get(':answer-field/correct', [None, None])[1]
        fields.append({
            'key': field[':answer-field/key'], 'type': field[':answer-field/type'],
            'choices_present': ':answer-field/choices' in field,
            'correct_present': ':answer-field/correct' in field,
            'choices': [(a[':answer/type'], a[':answer/value'], a[':answer/id'] == correct)
                        for a in field.get(':answer-field/choices', [])],
        })
    return {attr: q.get(attr) for attr in (':question/problem', ':question/worked-solution', ':question/difficulty')} | {'fields': fields}


preserved = 0
old_aliases = set()
examples = []
for level in g.LEVELS:
    for template in (None, *g.TEMPLATES):
        for seed in range(40):
            before = old.generate(level, seed, template=template)
            after = g.generate(level, seed, template=template)
            old_aliases.add(before['generation']['parameters']['variable'])
            assert after['generation']['parameters'] == {**before['generation']['parameters'], 'variable': 'x'}
            for key in ('parameter_fingerprint', 'template', 'bank_profile', 'recipes', 'authored_level'):
                assert after['generation'][key] == before['generation'][key], key
            assert content(after) == content(before, rename=True), (level, template, seed)
            assert after == g.generate(level, seed, template=template)
            if seed == 0 and template is not None:
                examples.append(after)
            preserved += 1
    for profile in ('raw_25524', 'raw_208832'):
        for seed in range(12):
            before = old.generate(level, seed, profile=profile)
            after = g.generate(level, seed, profile=profile)
            validator.check(after)
            assert after['generation']['parameters'] == {**before['generation']['parameters'], 'variable': 'x'}
            assert content(after) == content(before, rename=True)
            preserved += 1
assert old_aliases == {'x', 't', 'u'}

rejected = 0
explicit_x = 0
for level in g.LEVELS:
    for profile, template in (('method', 'radio_family'), ('method', 'blank_coordinate'),
                              ('raw_25524', 'radio_family'), ('raw_208832', 'blank_coordinate')):
        rec = g.generate(level, 27, profile=profile, template=template)
        parameters = rec['generation']['parameters']
        replay = g.generate(level, 27, parameters=parameters, profile=profile, template=template)
        assert replay['question'][':question/id'] == rec['question'][':question/id']
        replay_content, sampled_content = content(replay), content(rec)
        for item in (replay_content, sampled_content):
            for field in item['fields']:
                field['choices'].sort()
        assert replay_content == sampled_content
        validator.check(replay)
        explicit_x += 1
        for variable in ('t', 'u'):
            for entry in (lambda **kwargs: g.generate(level, **kwargs), getattr(g, 'generate_' + level)):
                try:
                    entry(parameters={**parameters, 'variable': variable}, profile=profile, template=template)
                except ValueError as exc:
                    assert 'variable must be x' in str(exc)
                    rejected += 1
                else:
                    raise AssertionError('Rejected notation returned a generated question')

cli = json.loads(subprocess.check_output([sys.executable, str(SCRIPT), '--difficulty', 'all',
                                         '--seed', '17', '--count', '2', '--format', 'json'], text=True))
for record in cli:
    validator.check(record)
    assert record['generation']['parameters']['variable'] == 'x'

full = json.loads((HERE / 'full-validation/validation.json').read_text())
assert full['passed'] and full['native']['unresolved'] == 0
save('examples.json', examples)
save('verification.json', {
    'passed': True,
    'knowledge_point': g.KP_ID,
    'version': g.VERSION,
    'script_sha256': sha(SCRIPT),
    'before_script_sha256': sha(HERE / 'before.py'),
    'validator_sha256': sha(FOLDER / 'validate.py'),
    'source_sha256': sha(FOLDER / 'source.json'),
    'widget_evidence_sha256': sha(FOLDER / 'widget-evidence.json'),
    'sampling_comparisons': preserved,
    'preserved_seed_properties': ['a', 'b', 'c', 'r', 'template', 'difficulty', 'bank profile',
                                  'option order', 'correct option position', 'mathematical fingerprint'],
    'old_aliases_exercised': sorted(old_aliases),
    'explicit_x_calls': explicit_x,
    'explicit_t_u_calls_rejected': rejected,
    'cli_records': len(cli),
    'full_validation': full,
    'database_writes': 0,
    'historical_evidence_mutations': 0,
    'entry_points': ['generate', 'generate_easy', 'generate_moderate', 'generate_hard', 'CLI'],
    'other_active_generator_modules_in_folder': [],
    'replenish_py': 'Historical publication driver; imports this generator. Not executed.',
})
print(json.dumps({'passed': True, 'sampling_comparisons': preserved, 'aliases_rejected': rejected,
                  'native': full['native'], 'script_sha256': sha(SCRIPT)}, indent=2))
