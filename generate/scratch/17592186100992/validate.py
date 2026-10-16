"""Check rendered algebra independently, role coverage, replay, and native grading."""
import copy
import hashlib
import importlib.util
import itertools
import json
import re
import subprocess
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[2]
spec = importlib.util.spec_from_file_location('distributivity', H.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
sp = g.sp
ENGINE = ROOT / 'generate/runs/current/check-engine'


def parse_matrix(text):
    match = re.fullmatch(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S)
    assert match, 'Invalid matrix'
    rows = [[sp.Integer(c.strip()) for c in row.split('&')] for row in match[1].split('\\\\')]
    assert len(rows) == 2 and all(len(row) == 2 for row in rows)
    return sp.Matrix(rows)


def parameters(problem):
    matches = re.findall(r'([ABC])=(\\begin\{bmatrix\}.*?\\end\{bmatrix\})', problem, re.S)
    assert [name for name, _ in matches] == list('ABC')
    return {n: [[int(x) for x in row] for row in parse_matrix(m).tolist()] for n, m in matches}


def symbolic(expression):
    # Independent of the generator's AST traversal and role metadata.
    assert re.fullmatch(r'[ABC()+\-]+', expression)
    return sp.expand(sp.sympify(expression, locals=dict(zip('ABC', sp.symbols('A B C')))))


def check(record):
    q, meta = record['question'], record['generation']
    expression = re.fullmatch(r'Find \$([ABC()+\-]+)\$, if', q[':question/problem'].splitlines()[0])[1]
    p = parameters(q[':question/problem'])
    reduced = symbolic(expression)
    assert str(reduced) in 'ABC' and len(str(reduced)) == 1
    survivor = str(reduced)
    value = sum((reduced.coeff(sp.Symbol(n)) * sp.Matrix(p[n]) for n in 'ABC'), sp.zeros(2))
    assert expression == meta['expression'] and survivor == meta['survivor'] and p == meta['parameters']
    assert all(type(x) is int and 0 <= x <= 9 for m in p.values() for row in m for x in row)
    assert q[':question/difficulty'] == ':question.difficulty/moderate'
    assert 'class="matrix-operands"' in q[':question/problem']
    fields = q[':question/answer-fields']
    assert len(fields) == 1
    f = fields[0]
    assert f[':answer-field/key'] == 'selection' and f[':answer-field/type'] == ':answer-field.type/radio'
    choices = f[':answer-field/choices']
    assert len(choices) == len({a[':answer/id'] for a in choices}) == 5
    assert all(a[':answer/type'] == ':answer.type/math' for a in choices)
    matrices = [parse_matrix(a[':answer/value']) for a in choices]
    assert len({tuple(m) for m in matrices}) == 5
    correct = [a for a in choices if a[':answer/id'] == f[':answer-field/correct'][1]]
    assert len(correct) == 1 and parse_matrix(correct[0][':answer/value']) == value
    altered = sp.Matrix([[value[0,0]-1, value[0,1]], [value[0,1], value[1,1]]])
    expected = [sp.Matrix(p[n]) for n in 'ABC'] + [sp.zeros(2), altered]
    assert {tuple(m) for m in matrices} == {tuple(m) for m in expected}
    solution = q[':question/worked-solution']
    stages = re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', solution, re.S)
    assert len(stages) == 2
    steps = [s.strip() for s in stages[0].split('\\\\')]
    assert len(steps) == 3
    assert steps[0].split('&')[0].strip() == expression
    expanded = steps[0].split('& =')[1].strip()
    assert '(' not in expanded and ')' not in expanded and symbolic(expanded) == reduced
    assert len(re.findall('[ABC]', expanded)) == 5
    canceled = steps[1].removeprefix('& =')
    assert len(re.findall(r'\\cancel\{[ABC]\}', canceled)) == 4
    assert symbolic(re.sub(r'\\cancel\{([ABC])\}', r'\1', canceled)) == reduced
    remaining = re.sub(r'\\cancel\{[ABC]\}', '0', canceled)
    # Check the crossed-out terms really cancel, not just the full equality.
    assert sp.expand(sp.sympify(remaining, locals=dict(zip('ABC', sp.symbols('A B C'))))) == reduced
    assert steps[-1] == '& =' + survivor
    final_label, final_matrix = stages[1].split('& =')
    assert final_label.strip() == survivor and parse_matrix(final_matrix.strip()) == value
    assert meta['mathematical_key'] == g.mathematical_key(p, expression, survivor)
    replay = g.generate(seed=meta['seed'], parameters=p, template=meta['structure'], roles=meta['roles'])
    assert replay == record, 'Full deterministic replay differs'
    return survivor


def engine_item(label, record):
    f = record['question'][':question/answer-fields'][0]
    return {'label': label, 'record': record, 'checks': [
        {'submitted_answer_id': a[':answer/id'],
         'expected': 'accepted' if a[':answer/id'] == f[':answer-field/correct'][1] else 'rejected',
         'purpose': 'independently evaluated displayed expression'} for a in f[':answer-field/choices']]}


def main():
    evidence = H / 'structural-fix'
    evidence.mkdir(exist_ok=True)
    source = json.loads((H / 'reference/source.json').read_text())
    source_question = next(q for q in source['record'][':knowledge-point/questions'] if q[':question/math-academy-id'] == 'q-13536')
    replay = g.generate(parameters=g.ORIGINAL, template=0, roles='ABC')
    check(replay)
    assert replay['question'][':question/problem'].splitlines()[0] == source_question[':question/problem'].splitlines()[0]
    assert replay['question'][':question/worked-solution'] == source_question[':question/worked-solution']
    replay_bank = sorted(a[':answer/value'] for a in replay['question'][':question/answer-fields'][0][':answer-field/choices'])
    for f in source_question[':question/answer-fields']:
        assert replay_bank == sorted(a[':answer/value'] for a in f[':answer-field/choices'])

    # Exercise every structure/role pair with the SAME numeric matrices.
    fixed = [g.generate(seed=17, parameters=g.ORIGINAL, template=t, roles=''.join(roles))
             for t in range(6) for roles in itertools.permutations('ABC')]
    for record in fixed:
        check(record)
    assert len({r['generation']['expression'] for r in fixed}) == 36
    assert {r['generation']['survivor'] for r in fixed} == set('ABC')
    assert len({r['question'][':question/id'] for r in fixed}) == 36
    # Same structure and matrices, role change must change correct matrix and solution.
    assert fixed[0]['generation']['survivor'] != fixed[2]['generation']['survivor']
    assert fixed[0]['question'][':question/worked-solution'] != fixed[2]['question'][':question/worked-solution']

    records = [g.generate(seed=i) for i in range(600)]
    for record in records:
        check(record)
    assert {(r['generation']['structure'], r['generation']['roles']) for r in records} == set(itertools.product(range(6), g.ROLES))
    assert all({r['generation']['parameters'][n][i][j] for r in records} == set(range(10))
               for n in 'ABC' for i in range(2) for j in range(2))
    for t in range(6):
        group = [r['generation'] for r in records if r['generation']['structure'] == t]
        assert {r['survivor'] for r in group} == set('ABC')
    # No first-operand or first-given-matrix shortcut works across this bank.
    assert {r['generation']['expression'].index(r['generation']['survivor']) for r in fixed} >= {1, 3, 5, 9}

    for kind in ('key', 'solution', 'expression'):
        bad = copy.deepcopy(fixed[0]); q = bad['question']; f = q[':question/answer-fields'][0]
        if kind == 'key':
            f[':answer-field/correct'][1] = next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/id'] != f[':answer-field/correct'][1])
        elif kind == 'solution':
            q[':question/worked-solution'] = q[':question/worked-solution'].replace('6 & 7', '9 & 7')
        else:
            q[':question/problem'] = q[':question/problem'].replace('(A+B)-C-(B-C)', '(B-C)-(B-A)-C')
        try:
            check(bad)
        except (AssertionError, ValueError):
            pass
        else:
            raise AssertionError('Corruption escaped: ' + kind)
    for value in (-1, 10):
        p = copy.deepcopy(g.ORIGINAL); p['A'][0][0] = value
        try:
            g.generate(parameters=p, template=0, roles='ABC')
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid numeric domain accepted')
    p = copy.deepcopy(g.ORIGINAL); p['B'] = p['A']
    try:
        g.generate(parameters=p, template=0, roles='ABC')
    except ValueError:
        pass
    else:
        raise AssertionError('Duplicate choices accepted')
    for level in ('easy', 'hard'):
        try:
            g.generate(level)
        except ValueError:
            pass
        else:
            raise AssertionError('Unsupported band emitted')
    a = g.generate(seed=1, parameters=g.ORIGINAL, template=0, roles='ABC')
    b = g.generate(seed=2, parameters=g.ORIGINAL, template=0, roles='ABC')
    assert a['question'][':question/id'] == b['question'][':question/id']
    p = copy.deepcopy(g.ORIGINAL); p['B'][0][0] = 9
    b = g.generate(parameters=p, template=0, roles='ABC')
    assert a['generation']['mathematical_key'] == b['generation']['mathematical_key']

    batch = [g.generate(seed=20261015+t, template=t, roles=('ABC','BAC','CAB')[t%3]) for t in range(6)]
    for record in batch:
        check(record)
    grading = [replay] + fixed + records + batch
    input_path = evidence / 'native-input.json'
    input_path.write_text(json.dumps([engine_item(str(i), r) for i, r in enumerate(grading)]))
    subprocess.run([str(ENGINE), str(input_path), str(evidence / 'native-report.json')], check=True)
    native = json.loads((evidence / 'native-report.json').read_text())
    review = [g.generate(seed=100+t, parameters=g.ORIGINAL, template=t, roles=('ABC','BAC','CAB')[t%3]) for t in range(6)]
    (evidence / 'review.md').write_text('\n\n---\n\n'.join(g.markdown(r) for r in review))
    (evidence / 'batch.json').write_text(json.dumps(batch, indent=2))
    result = {'passed': True, 'version': g.VERSION, 'fixed_matrix_structures_and_roles': len(fixed),
              'sampled_questions': len(records), 'survivors': sorted({r['generation']['survivor'] for r in records}),
              'source_replay': {'banks': 2, 'options': 10, 'exact_solution': True},
              'native_grading': {k: native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
              'sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in [H.with_suffix('.py'), Path(__file__)]}}
    (evidence / 'validation.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))


if __name__ == '__main__':
    main()
