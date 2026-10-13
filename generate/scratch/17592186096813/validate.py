#!/usr/bin/env python3
"""Independent printed-math, source-fidelity and actual native-grading checks.

This parser reads displayed TeX, including vector/reversed-endpoint objects and
every solution equality. It never takes the magnitude, answer or solution from
generation metadata. Exhaustive finite parameter domains are checked for both
layouts and both authored banks. Source keys absent in raw evidence remain absent.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import copy
import sys
from pathlib import Path

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCRIPT = HERE.with_suffix('.py')
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('unit_vectors', SCRIPT)
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
V = sp.Symbol('V', real=True)


def write(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def group(text, i):
    assert text[i] == '{', (text, i)
    depth, start = 1, i + 1
    i += 1
    while depth:
        assert i < len(text), text
        depth += (text[i] == '{') - (text[i] == '}')
        i += 1
    return text[start:i - 1], i


def scalar(text):
    """Translate the small actually emitted exact-number grammar independently."""
    text = text.replace(r'\,', '').replace(r'\left', '').replace(r'\right', '')
    out, i = '', 0
    while i < len(text):
        command = next((c for c in (r'\dfrac', r'\frac', r'\sqrt') if text.startswith(c, i)), None)
        if command:
            i += len(command)
            a, i = group(text, i)
            aa = str(scalar(a))
            if command == r'\sqrt':
                out += '*sqrt(' + aa + ')' if out and out[-1].isdigit() else 'sqrt(' + aa + ')'
            else:
                b, i = group(text, i)
                out += '((' + aa + ')/(' + str(scalar(b)) + '))'
        else:
            out += text[i]
            i += 1
    assert '\\' not in out, out
    out = out.replace('{', '(').replace('}', ')').replace('^', '**')
    return parse_expr(out, local_dict={'V': V, 'sqrt': sp.sqrt},
                      transformations=standard_transformations + (implicit_multiplication_application,))


def context(record):
    prompt = record['question'][':question/problem']
    match = re.fullmatch(r'The vector \$(.*?)\$ has magnitude \$(.*?)\$\. (.*)', prompt)
    assert match, prompt
    vector, mtext, remainder = match.groups()
    m = scalar(mtext)
    assert m > 1 and m.is_real
    assert remainder in (f'Find a unit vector that is parallel to ${vector}$.',
                         f'Which of the following is a unit vector that is parallel to ${vector}$?')
    if '^(→)' in vector:
        label = vector.split('^')[0]
        reverse = label[::-1] + '^(→)'
    elif 'overrightarrow' in vector:
        label = re.fullmatch(r'\\overrightarrow\{([A-Z]{2})\}', vector)[1]
        reverse = r'\overrightarrow{' + label[::-1] + '}'
    else:
        reverse = None
    return vector, reverse, m


def expression(text, vector, reverse, m):
    # Norm replacement happens before replacing its mathematical argument.
    text = text.replace(r'\mid \,' + vector + r'\, \mid', sp.sstr(m))
    if reverse:
        text = text.replace(reverse, '(-V)')
    if len(vector) == 1:
        # Raw named vectors occur only as a complete final vector component;
        # replacing the letter globally would corrupt the command \\frac.
        if text.endswith(vector):
            text = text[:-1] + 'V'
    else:
        text = text.replace(vector, 'V')
    return sp.simplify(scalar(text))


def formatted(text, raw=False):
    assert text.count('$') % 2 == 0
    depth = 0
    for c in text:
        depth += (c == '{') - (c == '}')
        assert depth >= 0
    assert depth == 0
    assert not any(token in text for token in ('+-', '--', 'NaN', 'nan', 'zoo', 'undefined'))
    # Decoded text: adjacent backslashes are NOT inferred from serialized output.
    assert '\\\\' not in text
    if not raw:
        assert '^(→)' not in text


def verify(record):
    assert record['knowledge_point'] == {'db_id': g.KP_ID, 'id': g.KP_UUID, 'title': g.TITLE}
    q, generation = record['question'], record['generation']
    vector, reverse, m = context(record)
    raw = generation['evidence_only']
    f, = q[':question/answer-fields']
    assert f[':answer-field/type'] == ':answer-field.type/radio'
    assert f[':answer-field/key'] == 'selection'
    assert len(f[':answer-field/choices']) == 5
    ids = [a[':answer/id'] for a in f[':answer-field/choices']]
    assert len(set(ids)) == 5
    formatted(q[':question/problem'], raw)
    values = []
    for a in f[':answer-field/choices']:
        assert a[':answer/type'] == ':answer.type/math'
        assert '$' not in a[':answer/value']
        formatted(a[':answer/value'], raw)
        value = expression(a[':answer/value'], vector, reverse, m)
        assert not value.has(sp.zoo, sp.oo, sp.nan)
        assert all(sp.simplify(value - other) != 0 for other in values)
        values.append(value)
    # Both orientations meet the actual source criterion "unit and parallel".
    eligible = [i for i, value in enumerate(values)
                if sp.simplify(value - V / m) == 0 or sp.simplify(value + V / m) == 0]
    assert len(eligible) == 1, (record, eligible)
    if raw:
        assert generation['eligible_for_learning'] is False
        assert ':answer-field/correct' not in f
        assert ':question/worked-solution' not in q
        assert ':question/difficulty' not in q
    else:
        assert generation['eligible_for_learning'] is True
        assert f[':answer-field/correct'] == [':answer/id', ids[eligible[0]]]
        solution = q[':question/worked-solution']
        formatted(solution)
        opening = f'To obtain the unit vector that is parallel to ${vector}$, we divide ${vector}$ by its length:'
        assert solution.startswith(opening + '\n\n$$\n')
        math_block = re.fullmatch(re.escape(opening) + r'\n\n\$\$\n(.*?)\n\$\$', solution, re.S)[1]
        lhs, *stages = math_block.split('=')
        assert lhs == r'\mathbf{u}'
        expected_count = 2 if q[':question/difficulty'].endswith('/easy') else 3
        assert len(stages) == expected_count
        assert stages[0] == r'\dfrac{' + vector + r'}{\mid \,' + vector + r'\, \mid}'
        assert stages[1] == r'\dfrac{1}{' + re.search(r'has magnitude \$(.*?)\$', q[':question/problem'])[1] + '}' + vector
        for stage in stages:
            assert sp.simplify(expression(stage, vector, reverse, m) - V / m) == 0, stage
    return m, values


def run():
    source_path = ROOT / 'generate/runs/current/sources/17592186096813.json'
    shutil.copyfile(source_path, HERE / 'source.json')
    capture = json.loads(source_path.read_text())
    sources = capture['record'][':knowledge-point/questions']
    cases, reviews, source_audit = [], [], []
    engine_input = []
    for source, template, magnitude in zip(sources, ('named', 'directed'), (5, 7)):
        sid = source[':question/math-academy-id']
        case = {'source_id': sid, 'template': template, 'level': 'easy',
                'parameters': {'m': magnitude, 'label': 'a' if template == 'named' else 'AB'},
                'bank_profile': 'raw_' + template, 'authored_level_assignment': True,
                'raw_source': source}
        cases.append(case)
        replay = g.generate('easy', template=template, parameters=case['parameters'], profile=case['bank_profile'])
        verify(replay)
        q = replay['question']
        assert q[':question/problem'] == source[':question/problem']
        original_field, = source[':question/answer-fields']
        generated_field, = q[':question/answer-fields']
        original_bank = sorted(a[':answer/value'] for a in original_field[':answer-field/choices'])
        generated_bank = sorted(a[':answer/value'] for a in generated_field[':answer-field/choices'])
        assert generated_bank == original_bank
        for key in (':question/difficulty', ':question/worked-solution'):
            assert (key in q) == (key in source)
        assert ':answer-field/correct' not in original_field and ':answer-field/correct' not in generated_field
        source_audit.append({'source_id': sid, 'exact_prompt': True, 'exact_all_options': 5,
                             'original_correct_designation_present': False,
                             'missing_solution_and_rating_preserved': True,
                             'inferred_eligible_unit_parallel_options': 1,
                             'designation_fidelity': 'not applicable: source designation absent'})
        reviews.append({'label': sid + ' original evidence replay', 'record': replay})
        # The original cannot be graded without its absent key. This explicit
        # memory-only fixture adds the independently derived key for harness QA;
        # the raw replay and source evidence are left unmodified.
        fixture = copy.deepcopy(replay)
        ff = fixture['question'][':question/answer-fields'][0]
        vv, rr, mm = context(fixture)
        inferred = next(a[':answer/id'] for a in ff[':answer-field/choices']
                        if sp.simplify(expression(a[':answer/value'], vv, rr, mm) - V / mm) == 0)
        ff[':answer-field/correct'] = [':answer/id', inferred]
        fixture['generation']['native_fixture_added_key'] = 'independent mathematics, not observed designation'
        engine_input.append({'label': sid + ' memory-only independently keyed original-bank fixture',
                             'record': fixture, 'checks': [
                                 {'submitted_answer_id': a[':answer/id'],
                                  'expected': 'accepted' if a[':answer/id'] == inferred else 'rejected',
                                  'purpose': 'original complete bank; key inferred for memory-only fixture'}
                                 for a in ff[':answer-field/choices']]})
        changed = g.generate('easy', seed=19, template=template, parameters={'m': 11}, profile=case['bank_profile'])
        verify(changed)
        reviews.append({'label': sid + ' changed-parameter evidence-only mask variant', 'record': changed})
    write('source-cases.json', cases)

    # The canonical example supplies the authored prose and two-stage easy mask.
    canonical = capture['record'][':knowledge-point/canonical-example']
    canonical_replay = g.generate_easy(template='named', parameters={'m': 3})
    assert canonical_replay['question'][':question/problem'] == canonical[':question/problem']
    assert canonical_replay['question'][':question/worked-solution'] == canonical[':question/worked-solution']
    verify(canonical_replay)
    raw_tested = 0
    for template in g.TEMPLATES:
        for p in g.PARAMETER_DOMAINS['easy']:
            verify(g.generate_easy(template=template, parameters=p, profile='raw_' + template))
            raw_tested += 1

    tested = 0
    task_counts = {}
    for level, domain in g.PARAMETER_DOMAINS.items():
        mathematical_ids = set()
        for template in g.TEMPLATES:
            for profile in ('normalization', 'direction_errors'):
                for p in domain:
                    record = g.generate(level, 29, template, parameters=p, profile=profile)
                    verify(record)
                    mathematical_ids.add(record['generation']['mathematical_fingerprint'])
                    # Determinism, field ownership and seed/order invariance.
                    assert record == g.generate(level, 29, template, parameters=p, profile=profile)
                    shuffled = g.generate(level, 91, template, parameters=p, profile=profile)
                    assert record['question'][':question/id'] == shuffled['question'][':question/id']
                    assert record['generation']['content_fingerprint'] == shuffled['generation']['content_fingerprint']
                    assert record['generation']['mathematical_fingerprint'] == shuffled['generation']['mathematical_fingerprint']
                    tested += 1
                    if p in (domain[0], domain[-1]):
                        label = f'Authored {level} / {template} / {profile} / {p}'
                        reviews.append({'label': label, 'record': record})
                        f = record['question'][':question/answer-fields'][0]
                        engine_input.append({'label': label, 'record': record, 'checks': [
                            {'submitted_answer_id': a[':answer/id'], 'expected':
                             'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
                             'purpose': 'all owned radio choices after independent displayed-math audit'}
                            for a in f[':answer-field/choices']]})
        task_counts[level] = len(mathematical_ids)
        assert len(mathematical_ids) == len(domain)
    # Label/endpoint spelling changes presentation, never assessed mathematical identity.
    a = g.generate_easy(parameters={'m': 5, 'label': 'a'}, template='named')
    b = g.generate_easy(parameters={'m': 5, 'label': 'b'}, template='named')
    c = g.generate_easy(parameters={'m': 5, 'label': 'AB'}, template='directed')
    assert a['generation']['mathematical_fingerprint'] == b['generation']['mathematical_fingerprint'] == c['generation']['mathematical_fingerprint']
    assert len({r['question'][':question/id'] for r in (a, b, c)}) == 3
    alt = g.generate_easy(parameters={'m': 5}, template='named', profile='direction_errors')
    assert a['question'][':question/id'] != alt['question'][':question/id']
    assert a['generation']['mathematical_fingerprint'] == alt['generation']['mathematical_fingerprint']
    # All supported labels under each level, signed negative distractors included.
    for level, domain in g.PARAMETER_DOMAINS.items():
        for template, labels in [('named', ('a', 'b', 'c', 'v', 'w')), ('directed', ('AB', 'CD', 'PQ', 'RS'))]:
            for label in labels:
                verify(g.generate(level, template=template, parameters={**domain[-1], 'label': label}))
    # Reject explicit inputs that erase each authored number-form workload.
    bad = [('easy', {'m': 1}), ('easy', {'m': 31}), ('easy', {'m': -5}),
           ('moderate', {'p': 4, 'q': 2}), ('moderate', {'p': 2, 'q': 3}),
           ('moderate', {'p': 21, 'q': 2}), ('hard', {'k': 1, 'd': 4}),
           ('hard', {'k': 6, 'd': 2}), ('hard', {'k': -2, 'd': 3})]
    for level, p in bad:
        try:
            g.generate(level, parameters=p)
        except ValueError:
            pass
        else:
            raise AssertionError(('invalid explicit parameters accepted', level, p))
    # Shuffle is not always correct-first.
    positions = set()
    for seed in range(20):
        r = g.generate_easy(seed, template='named', parameters={'m': 5})
        f = r['question'][':question/answer-fields'][0]
        positions.add(next(i for i, a in enumerate(f[':answer-field/choices']) if a[':answer/id'] == f[':answer-field/correct'][1]))
    assert len(positions) == 5
    write('review.json', reviews)
    review_md = ['# Originals and generated variants', '',
                 'The first four records are unkeyed evidence replay. All subsequent levels and solutions are authored.', '']
    for item in reviews:
        review_md.extend(['## ' + item['label'], '', g.markdown(item['record']), ''])
    (HERE / 'review.md').write_text('\n'.join(review_md))
    write('engine-input.json', engine_input)
    engine = ROOT / 'generate/runs/current/check-engine'
    subprocess.run([str(engine), str(HERE / 'engine-input.json'), str(HERE / 'engine-report.json')], check=True)
    native = json.loads((HERE / 'engine-report.json').read_text())
    decoded = {'canonical_problem_adjacent_backslash_pairs': canonical[':question/problem'].count('\\\\'),
               'canonical_solution_adjacent_backslash_pairs': canonical[':question/worked-solution'].count('\\\\')}
    assert all(v == 0 for v in decoded.values())
    validation = {'status': 'passed', 'generator_sha256': hashlib.sha256(SCRIPT.read_bytes()).hexdigest(), 'source': g.SOURCE, 'database_writes': 0,
                  'raw_exact_prompts': {'matched': 2, 'total': 2},
                  'raw_exact_bank_values': {'matched': 10, 'total': 10},
                  'raw_complete_banks': {'matched': 2, 'total': 2},
                  'observed_correct_designations': {'matched': 0, 'total_present': 0, 'absent': 2},
                  'observed_practice_solutions': {'matched': 0, 'total_present': 0, 'absent': 2},
                  'observed_difficulty_ratings': {'total_present': 0, 'absent': 2},
                  'source_audit': source_audit, 'decoded_source_byte_audit': decoded,
                  'normal_presentation_repairs': ['directed-vector AB^(→) to overrightarrow{AB}'],
                  'source_math_repairs': 0, 'authored_levels': ['easy', 'moderate', 'hard'],
                  'canonical_prompt_and_solution_exact': True,
                  'raw_exhaustive_evidence_instances': raw_tested,
                  'normal_exhaustive_instances': tested, 'meaningful_finite_tasks': task_counts,
                  'level_bound_negative_tests': len(bad), 'shuffle_correct_positions': sorted(positions),
                  'native_grading': {'accepted': native['accepted_checks'], 'rejected': native['rejected_checks'],
                                     'unresolved': native['documented_unresolved_checks'],
                                     'original_bank_key_fixture_count': 2,
                                     'original_bank_fixture_keys': 'mathematically inferred, never observed key matches',
                                     'engine_sha256': hashlib.sha256(engine.read_bytes()).hexdigest()},
                  'remaining_findings': ['Original practice keys, ratings and worked solutions absent; retained as omissions.',
                                         'q-11376 2m/4m scaling error intent underdetermined; evidence-only masks.']}
    write('validation.json', validation)
    print(json.dumps(validation, indent=2))


if __name__ == '__main__':
    run()
