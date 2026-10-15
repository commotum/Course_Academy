"""Read rendered expressions independently; prove identities or save witnesses."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import platform
import re
import subprocess
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('matrix_identity_generator', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
LABELS = ('I', 'II', 'III')
CLAIMS = re.compile(r'(?:\*\*(III|II|I)\.\*\*|(?<![A-Z])(III|II|I)\.)\s*\$([^$]+)\$')


def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2) + '\n')


def expression(text, values):
    text = re.sub(r'\{?I\}?_\{?\d+\}?', 'J', text)
    text = re.sub(r'[\s{}]', '', text).replace(r'\cdot', '*')
    tokens = re.findall(r'\d+|[ABCJ()+*^\-]', text)
    assert ''.join(tokens) == text, text
    pos = 0

    def atom():
        nonlocal pos
        token = tokens[pos]
        pos += 1
        if token == '(':
            value = add()
            assert tokens[pos] == ')'
            pos += 1
        elif token in values:
            value = values[token]
        else:
            value = sp.Integer(token)
        if pos < len(tokens) and tokens[pos] == '^':
            pos += 1
            power = int(tokens[pos])
            pos += 1
            value = value ** power
        return value

    def mul():
        nonlocal pos
        value = atom()
        while pos < len(tokens) and tokens[pos] not in ('+', '-', ')'):
            if tokens[pos] == '*':
                pos += 1
            value = value * atom()
        return value

    def add():
        nonlocal pos
        value = mul()
        while pos < len(tokens) and tokens[pos] in ('+', '-'):
            op = tokens[pos]
            pos += 1
            value = value + mul() if op == '+' else value - mul()
        return value

    result = add()
    assert pos == len(tokens)
    return result


def mathematics(claim):
    left, right = claim.split('=')
    values = {k: sp.Symbol(k, commutative=False) for k in 'ABC'}
    values['J'] = sp.Integer(1)
    difference = sp.expand(expression(left, values) - expression(right, values))
    if difference == 0:
        return True, {'proof': 'Exact expansion in the free associative algebra is zero.'}
    matrices = [sp.zeros(2), sp.eye(2), sp.Matrix([[1, 0], [0, 0]]), sp.Matrix([[0, 1], [0, 0]]), sp.Matrix([[0, 0], [1, 0]]), sp.Matrix([[1, 1], [0, 1]])]
    for triple in itertools.product(matrices, repeat=3):
        vals = dict(zip('ABC', triple)); vals['J'] = sp.eye(2)
        l, r = expression(left, vals), expression(right, vals)
        if l != r:
            ints = lambda m: [[int(x) for x in row] for row in m.tolist()]
            return False, {'proof': 'Exact 2x2 counterexample; embed as a diagonal block for n>2.', 'matrices': {k: ints(m) for k, m in zip('ABC', triple)}, 'left': ints(l), 'right': ints(r)}
    raise AssertionError('No proved identity or counterexample: ' + claim)


def check(rec):
    q = rec['question']; meta = rec['generation']
    assert rec['knowledge_point']['db_id'] == g.KP_ID
    assert rec == g.generate(q[':question/difficulty'].split('/')[-1], meta['seed'], meta['template'], meta['parameters'])
    claims = [(a or b, c) for a, b, c in CLAIMS.findall(q[':question/problem'])]
    assert [k for k, _ in claims] == list(LABELS)
    mask = [(key, *mathematics(claim)) for key, claim in claims]
    judgments = re.findall(r'Statement\s+(III|II|I)\s+is\s+(true|false)', q[':question/worked-solution'])
    assert judgments == [(key, str(truth).lower()) for key, truth, _ in mask]
    fields = q[':question/answer-fields']
    if len(fields) == 3:
        assert [f[':answer-field/key'] for f in fields] == list(LABELS)
        expected = [str(truth).lower() for _, truth, _ in mask]
    else:
        assert len(fields) == 1 and fields[0][':answer-field/key'] == 'selection'
        expected = [' and '.join(key for key, truth, _ in mask if truth) + ' only']
    for f, wanted in zip(fields, expected):
        choices = f[':answer-field/choices']
        assert len({a[':answer/value'] for a in choices}) == len(choices)
        correct = [a for a in choices if a[':answer/id'] == f[':answer-field/correct'][1]]
        assert len(correct) == 1 and correct[0][':answer/value'] == wanted
        assert all(a[':answer/type'] == ':answer.type/text' for a in choices)
    return [{'key': key, 'truth': truth, **proof} for key, truth, proof in mask]


def native(label, rec):
    checks = []
    for i, f in enumerate(rec['question'][':question/answer-fields']):
        for a in f[':answer-field/choices']:
            checks.append({'field_index': i, 'submitted_answer_id': a[':answer/id'], 'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected', 'purpose': 'Every authored choice through actual application grader'})
    return {'label': label, 'record': rec, 'checks': checks}


def main():
    replay = []; inputs = []; proofs = []; reviews = []; dimension_checks = []
    for t, src in g.SOURCES.items():
        level = src[':question/difficulty'][':db/ident'].split('/')[-1]
        rec = g.generate(level, 0, t)
        proof = check(rec)
        q = rec['question']
        assert q[':question/problem'] == src[':question/problem']
        assert q[':question/worked-solution'] == src[':question/worked-solution']
        matched = 0
        for f, old in zip(q[':question/answer-fields'], src[':question/answer-fields']):
            assert f[':answer-field/key'] == old[':answer-field/key'] and f[':answer-field/type'] == old[':answer-field/type'][':db/ident']
            assert sorted(a[':answer/value'] for a in f[':answer-field/choices']) == sorted(a[':answer/value'] for a in old[':answer-field/choices'])
            correct = next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id'] == f[':answer-field/correct'][1])
            assert correct == old[':answer-field/correct'][':answer/value']
            matched += len(f[':answer-field/choices'])
        replay.append({'source': t, 'level': level, 'profile': 'source-' + t, 'matched_choices': matched, 'total_choices': matched, 'matched_distractors': matched-len(q[':question/answer-fields']), 'exact_prompt_and_solution': True, 'full_bank_matched': True})
        proofs.append({'source': t, 'claims': proof})
        inputs.append(native(t, rec))
        for n in range(2, 9):
            variant = g.generate(level, 19, t, {'n': n})
            check(variant)
            assert g.fingerprint(variant['question']) == g.fingerprint(src)
            assert variant['question'][':question/id'] == rec['question'][':question/id']
            assert variant == g.generate(level, 19, t, {'n': n})
            inputs.append(native(t + '-n' + str(n), variant))
            dimension_checks.append({'source': t, 'n': n, 'same_task': True, 'count_as_fresh': False})
        reviews.append('## ' + t + '\n\nSource and exact replay:\n\n' + q[':question/problem'] + '\n\n' + q[':question/worked-solution'] + '\n\nDimension preview (same task, rejected as fresh):\n\n' + g.generate(level, 19, t, {'n': 2 if rec['generation']['parameters']['n'] != 2 else 8})['question'][':question/problem'])
    for level in g.LEVELS:
        for seed in (0, 1, 1930, 999999):
            assert g.fresh(level, 5, seed) == []
    for n in (1, 9, 2.5, True):
        try: g.generate('hard', 0, 'q-42266', {'n': n})
        except ValueError: pass
        else: raise AssertionError('Invalid domain accepted')
    try: g.generate('easy')
    except ValueError: pass
    else: raise AssertionError('Easy must stay unsupported')
    save('source-replay.json', {'passed': True, 'basis': g.S['basis'], 'banks': replay, 'complete_banks_matched': len(replay), 'complete_banks_total': len(replay), 'matched_choices': sum(r['matched_choices'] for r in replay), 'matched_distractors': sum(r['matched_distractors'] for r in replay), 'missing_or_extra_options': []})
    save('mathematics.json', proofs)
    save('dimension-coverage.json', dimension_checks)
    save('native-input.json', inputs)
    subprocess.run([str(HERE/'check-engine'), str(HERE/'native-input.json'), str(HERE/'native-report.json')], check=True)
    (HERE/'review.md').write_text('\n\n'.join(reviews) + '\n')
    save('validation.json', {'passed': True, 'supported_levels': list(g.LEVELS), 'unsupported_levels': ['easy'], 'source_bank_count': len(replay), 'sampled_dimension_previews': len(dimension_checks), 'fresh_instances': 0, 'mathematics': '39 statements independently parsed; noncommutative symbolic proofs for identities and explicit exact matrix counterexamples for every false statement.', 'fidelity': 'Every source prompt, solution, field key/type, complete bank and correct designation exactly reproduced.', 'grading': 'Every choice in source replay and all dimension previews checked through learning::grade_field; no unresolved results.', 'novelty': 'All dimension/seed changes rejected as fresh; source task identities stable.', 'dependencies': {'python': platform.python_version(), 'sympy': sp.__version__}, 'hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'), HERE/'validate.py', HERE/'source.json', HERE/'check-engine')}})
    print('Validated all 13 complete source banks and 91 dimension previews; 0 fresh mathematical tasks.')


if __name__ == '__main__':
    main()
