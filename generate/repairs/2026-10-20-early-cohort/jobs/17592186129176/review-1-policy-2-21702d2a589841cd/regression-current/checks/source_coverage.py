"""Replay every independently captured source bank, including finding a0b02658254fd1e9493c."""
import ast
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import generator as g


def read_task(text):
    body = re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}', text, re.S)[1]
    matrix = [[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
    rows = [int(n)-1 for n in re.findall(r'\$(\d)(?:\$|\\text\{)', text.split('rows')[0])]
    assert len(rows) in (2, 3) and len(set(rows)) == len(rows)
    return matrix, rows


def integer_sum(expression):
    def evaluate(node):
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -evaluate(node.operand)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return evaluate(node.left) + evaluate(node.right)
        raise AssertionError('Unexpected arithmetic: ' + ast.dump(node))
    return evaluate(ast.parse(expression, mode='eval'))


def witness(record):
    q = record['question']
    matrix, rows = read_task(q[':question/problem'])
    entries = [next(x for x in matrix[row] if x != 0) for row in rows]
    total = sum(entries)
    field = q[':question/answer-fields'][0]
    choices = field[':answer-field/choices']
    bank = [int(a[':answer/value']) for a in choices]
    key_id = field[':answer-field/correct'][1]
    keyed = [a for a in choices if a[':answer/id'] == key_id]
    assert len(keyed) == 1 and int(keyed[0][':answer/value']) == total
    assert len(set(bank)) == len(bank) == 5 and bank.count(total) == 1
    solution = q[':question/worked-solution']
    solution_rows = [int(n)-1 for n in re.findall(r'\$(\d)(?:\$|\\text\{)', solution.split('rows')[0])]
    assert solution_rows == rows, (solution_rows, rows)
    stated = re.search(r'rows of\s+\$A\$ are (.*?), respectively', solution)[1]
    assert [int(n) for n in re.findall(r'\$(-?\d+)[,$]', stated)] == entries
    equation = re.search(r'So, the answer is \$(.*?)\.\$', solution)[1]
    lhs, rhs = equation.split('=')
    terms = '+'.join(str(x) if i == 0 or x >= 0 else '('+str(x)+')' for i, x in enumerate(entries))
    assert lhs == terms and integer_sum(lhs) == int(rhs) == total
    return {'matrix': matrix, 'rows': rows, 'entries': entries, 'total': total,
            'bank': bank, 'position': choices.index(keyed[0]), 'rank': sorted(bank).index(total),
            'columns': [next(j for j, x in enumerate(matrix[r]) if x) for r in rows]}


def main():
    sources = json.loads((ROOT / 'evidence/source-cases.json').read_text())
    results, records = [], []
    for source in sources:
        profile = source[':question/math-academy-id']
        matrix, rows = read_task(source[':question/problem'])
        record = g.generate(seed=817, profile=profile,
                            parameters={'matrix': matrix, 'rows': rows}, replay=True)
        observed = witness(record)
        original_field = source[':question/answer-fields'][0]
        bank = sorted(int(a[':answer/value']) for a in original_field[':answer-field/choices'])
        assert sorted(observed['bank']) == bank, profile
        original_key = original_field.get(':answer-field/correct')
        if original_key:
            assert observed['total'] == int(original_key[':answer/value'])
        assert record['question'][':question/problem'] == g.normalize_prose(source[':question/problem'])
        if ':question/worked-solution' in source:
            assert record['question'][':question/worked-solution'] == g.normalize_prose(source[':question/worked-solution'])
        original_level = source.get(':question/difficulty', {}).get(':db/ident')
        assert record['question'].get(':question/difficulty') == original_level
        records.append(record)
        results.append({'profile': profile, 'question_id': source[':question/id'],
                        'bank': bank, 'answer': observed['total'], 'matched_choices': 5,
                        'original_key_available': original_key is not None,
                        'original_solution_available': ':question/worked-solution' in source})
    assert len(results) == 15 and any(r['profile'] == 'q-129207' for r in results)
    (ROOT / 'evidence/source-replay-records.json').write_text(json.dumps(records, indent=2)+'\n')
    (ROOT / 'evidence/source-replay-results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(f'{len(results)} complete source banks replay; 75/75 choices matched; visible math and keys pass.')


if __name__ == '__main__':
    main()
