"""Independent displayed-data checks; also used on isolated durable refills."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def fingerprint(q):
    # Exact shared content_fingerprint projection for this single-blank contract.
    f = q[':question/answer-fields'][0]
    key = f[':answer-field/correct']
    key = key[1] if isinstance(key, list) else key
    a = next(a for a in f[':answer-field/choices'] if a[':answer/id'] == key)
    projected = {':question/problem': q[':question/problem'], ':question/answer-fields': [
        {':answer-field/key': f[':answer-field/key'], ':answer-field/type': f[':answer-field/type'],
         ':answer-field/correct': {':answer/type': a[':answer/type'], ':answer/value': a[':answer/value']}}]}
    if ':question/requires-calculator' in q:
        projected[':question/requires-calculator'] = q[':question/requires-calculator']
    return hashlib.sha256(json.dumps(projected, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()


def inspect(record):
    q = record['question']
    prompt = q[':question/problem']
    match = re.search(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}', prompt, re.S)
    assert match, 'Missing given matrix'
    rows = match[1].split(r'\\')
    matrix = [[int(v.strip()) for v in row.split('&')] for row in rows]
    assert len(matrix) == 2 and all(len(row) == 2 for row in matrix)
    targets = re.findall(r'find \$a_\{([12])([12])\}\$', prompt)
    assert len(targets) == 1
    i, j = (int(v) for v in targets[0])
    # Restrict full prompt to neutral layout; no interpretation, highlight or hint.
    plain = re.sub(r'<[^>]+>', '', prompt)
    assert re.fullmatch(r'For the matrix\s+\$A=\\begin\{pmatrix\}.*?\\end\{pmatrix\}\$\s+find \$a_\{[12][12]\}\$\.\s+\{\{answer\}\}', plain, re.S)
    assert 'style=' not in prompt and 'color' not in prompt
    f, = q[':question/answer-fields']
    assert f[':answer-field/type'] == ':answer-field.type/blank' and f[':answer-field/key'] == 'answer'
    a, = f[':answer-field/choices']
    assert a[':answer/type'] == ':answer.type/math'
    key = f[':answer-field/correct']
    assert (key[1] if isinstance(key, list) else key) == a[':answer/id']
    result = matrix[i-1][j-1]
    assert str(result) == a[':answer/value'], 'Key differs from independently located entry'
    solution = q[':question/worked-solution']
    assert solution == (f'The first index is {i}, so use row {i}. The second index is {j}, '
                        f'so use column {j} of that row. $a_{{{i}{j}}}={result}$.')
    # Wrong other-cell reading when distinguishable; sign loss when available.
    others = [v for row in matrix for v in row if v != result]
    wrong = others[0] if others else result + 1
    checks = [{'field_index': 0, 'submitted': rf'\frac{{{2*result}}}{{2}}', 'expected': 'accepted',
               'control': 'equivalent', 'purpose': 'Same exact integer as an unreduced integer-valued fraction; no form restriction'},
              {'field_index': 0, 'submitted': str(wrong), 'expected': 'rejected', 'control': 'wrong',
               'purpose': 'A different displayed cell value' if others else 'Independent non-equal integer for constant matrix'}]
    if result:
        checks.append({'field_index': 0, 'submitted': str(-result), 'expected': 'rejected', 'control': 'wrong',
                       'purpose': 'Sign reversal changes the requested integer'})
    return matrix, i, j, result, checks


def check(records):
    native = []
    for record in records:
        _, _, _, _, checks = inspect(record)
        native.append({'fingerprint': fingerprint(record['question']), 'checks': checks})
    fingerprints = sorted(row['fingerprint'] for row in native)
    return {'status': 'passed', 'checked_fingerprints': fingerprints,
            'check_results': [{'id': name, 'status': 'passed', 'checked_fingerprints': fingerprints}
                              for name in ['independent-entry', 'independent-prompt', 'response-controls']],
            'native_checks': native}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--records', required=True)
    parser.add_argument('--inventory', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    # Inventory is supplied by the runner. This per-record contract imposes no population quota.
    json.loads(Path(args.inventory).read_text())
    report = check(json.loads(Path(args.records).read_text()))
    Path(args.output).write_text(json.dumps(report, indent=2) + '\n')
