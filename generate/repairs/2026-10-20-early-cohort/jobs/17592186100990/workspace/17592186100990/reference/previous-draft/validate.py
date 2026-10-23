#!/usr/bin/env python3
"""Exact finite-domain validation and native application grading, without writes."""
import hashlib
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('matrix_indices', HERE.with_suffix('.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)

def save(name, value):
    (HERE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def main():
    source = json.loads((HERE / 'source.json').read_text())
    original = next(q for q in source['record'][':knowledge-point/questions']
        if q.get(':question/math-academy-id') == g.SOURCE_ID)
    values = {f[':answer-field/key']: f[':answer-field/correct'][':answer/value']
        for f in original[':question/answer-fields']}
    assert values == {'field-1': '3', 'field-2': '2'}
    assert '$3$rd row and $2$nd column' in original[':question/worked-solution']
    replay = g.generate_easy(parameters={'i': 3, 'j': 2})
    assert replay['question'][':question/worked-solution'] == original[':question/worked-solution']
    # Strip the authored highlight and compare all wording/TeX; normalize capture whitespace.
    stripped = re.sub(r'\\bbox\[lightgray, 2pt\]\{(-?\d+)\}', r'\1', replay['question'][':question/problem'])
    assert re.sub(r'\s+', ' ', stripped) == re.sub(r'\s+', ' ', original[':question/problem'])
    by_key = {f[':answer-field/key']: f for f in replay['question'][':question/answer-fields']}
    for f in original[':question/answer-fields']:
        rf = by_key[f[':answer-field/key']]
        assert [a[':answer/value'] for a in rf[':answer-field/choices']] == [a[':answer/value'] for a in f[':answer-field/choices']]
        assert rf[':answer-field/type'] == f[':answer-field/type'][':db/ident']
        assert rf[':answer-field/choices'][0][':answer/value'] == f[':answer-field/correct'][':answer/value']
    signatures = set()
    questions = []
    checks = []
    for i, j in g.DOMAIN:
        record = g.generate_easy(seed=11, parameters={'i': i, 'j': j})
        q = record['question']
        assert g.generate_easy(seed=999, parameters={'i': i, 'j': j})['question'] == q
        key = record['generation']['mathematical_key']
        assert key not in signatures
        signatures.add(key)
        assert q[':question/problem'].count(r'\bbox') == 1
        matrix_text = re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}', q[':question/problem'], re.S).group(1)
        rows = matrix_text.split(r'\\')
        assert len(rows) == 3
        highlight = []
        for row_n, row in enumerate(rows, 1):
            cells = row.split('&')
            assert len(cells) == 3
            for col_n, cell in enumerate(cells, 1):
                if r'\bbox' in cell:
                    highlight.append((row_n, col_n))
                raw = re.sub(r'\\bbox\[lightgray, 2pt\]\{(-?\d+)\}', r'\1', cell).strip()
                assert sp.Integer(raw) == g.MATRIX[row_n - 1, col_n - 1]
        assert highlight == [(i, j)]
        assert q[':question/problem'].count('$') % 2 == 0
        assert q[':question/worked-solution'].count('$') % 2 == 0
        item_checks = []
        for index, (field, expected) in enumerate(zip(q[':question/answer-fields'], (i, j))):
            assert '{{' + field[':answer-field/key'] + '}}' in q[':question/problem']
            answer = field[':answer-field/choices'][0]
            assert field[':answer-field/correct'][1] == answer[':answer/id']
            assert sp.Integer(answer[':answer/value']) == expected
            item_checks += [
                {'field_index': index, 'submitted': str(expected), 'expected': 'accepted', 'purpose': 'correct rendered cell coordinate'},
                {'field_index': index, 'submitted': f'{expected+1}-1', 'expected': 'accepted', 'purpose': 'equivalent numerical expression'},
                {'field_index': index, 'submitted': str(expected+1), 'expected': 'rejected', 'purpose': 'incorrect coordinate'},
                {'field_index': index, 'submitted': '0', 'expected': 'rejected', 'purpose': 'zero-based indexing error'}]
        checks.append({'label': f'cell ({i},{j})', 'record': record, 'checks': item_checks})
        questions.append(record)
    for bad in ({'i': 0, 'j': 1}, {'i': 4, 'j': 1}, {'i': True, 'j': 1}, {'i': 1.0, 'j': 1}, {'i': 1}):
        try:
            g.generate_easy(parameters=bad)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid index accepted')
    for level in ('moderate', 'hard'):
        try:
            g.generate(level)
        except ValueError:
            pass
        else:
            raise AssertionError('Uncertified band accepted')
    save('engine-input.json', checks)
    engine = HERE.parents[1] / 'runs/current/check-engine'
    subprocess.run([str(engine), str(HERE / 'engine-input.json'), str(HERE / 'engine-report.json')], check=True)
    cli = subprocess.run([str(HERE.parents[2] / '.venv/bin/python'), str(HERE.with_suffix('.py')),
        '--difficulty', 'easy', '--count', '9', '--seed', '11'], capture_output=True, text=True, check=True)
    cli_records = json.loads(cli.stdout)
    assert len({r['generation']['mathematical_key'] for r in cli_records}) == 9
    excess = subprocess.run([str(HERE.parents[2] / '.venv/bin/python'), str(HERE.with_suffix('.py')),
        '--difficulty', 'easy', '--count', '10'], capture_output=True, text=True)
    assert excess.returncode != 0
    # Pick different highlighted cells, never the unchanged original cell (3,2).
    batch = [r for r in questions if r['generation']['parameters'] != {'i': 3, 'j': 2}]
    save('generated.json', batch)
    save('review.json', {'source': original, 'source_replay_with_restored_highlight': replay, 'variants': batch})
    (HERE / 'review.md').write_text('# Source and corrected replay\n\n' + original[':question/problem'] + '\n\n' +
        original[':question/worked-solution'] + '\n\n' + g.markdown(replay) + '\n\n# Distinct cells\n\n' +
        '\n\n---\n\n'.join(map(g.markdown, batch)) + '\n')
    save('validation.json', {'status': 'passed', 'source_basis': source['basis'],
        'supported_difficulties': ['easy'], 'supported_templates': ['two-index-blanks'],
        'finite_variant_limit': 9, 'validated_distinct_cells': 9, 'source_cell_excluded_from_import': [3, 2],
        'new_candidates': len(batch), 'source_bank_replay': {'source': g.SOURCE_ID,
            'matched_fields': 2, 'total_fields': 2, 'matched_values': 2, 'total_values': 2,
            'complete_banks': '2/2 singleton blank banks', 'missing_options': [], 'extra_options': [],
            'distractors': '0/0; blanks have no distractor profile'},
        'fidelity': {'prompt': 'Source wording and TeX unchanged after removing restored highlight and normalizing capture indentation',
            'solution': 'Exact source sequence and wording; index parameters vary',
            'fields': 'Both original numeric blank keys, response shapes and values replay exactly',
            'excluded_source_banks': 'Radio and symbolic-subscript blank templates classified but uncertified'},
        'mathematics': 'Independently parsed rendered matrix; exactly one highlighted cell; row/column answer verified',
        'grading': json.loads((HERE / 'engine-report.json').read_text()),
        'identity': 'Unique highlighted cells; questions unchanged across seed changes; finite CLI rejects count >9',
        'plots': 'None: standalone matrix LaTeX with MathJax bbox, no raster asset',
        'generator_sha256': hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),
        'source_sha256': hashlib.sha256((HERE / 'source.json').read_bytes()).hexdigest(),
        'engine_sha256': hashlib.sha256(engine.read_bytes()).hexdigest()})
    print('PASS: nine distinct cells; exact two-field source replay; 72 native grading checks')

if __name__ == '__main__':
    main()
