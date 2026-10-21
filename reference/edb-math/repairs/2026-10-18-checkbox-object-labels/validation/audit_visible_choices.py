"""Read-only audit of literal TeX in the final rendered checkbox labels."""
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TASK = HERE.parent


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def after_by_id(path):
    return {str(c['id']): c for c in read(path) if c['stage'] == 'after'}


def main():
    original = {str(q[':db/id']) for q in read(TASK / 'questions.json')}
    selected = {}
    sources = []
    sources.append((3704, 'already-complete', HERE / 'already-complete',
                    HERE / 'already-complete' / 'render-cases.json', None))
    batches = sorted(read(TASK / 'confirmed-batches.json'), key=lambda b: b['basis_after'])
    for batch in batches:
        assert batch['passed'] and batch['committed']
        directory = TASK / batch['directory']
        assert read(directory / 'commit-verification.json')['passed']
        render = TASK / read(directory / 'render-evidence.json')['directory']
        sources.append((batch['basis_after'], batch['directory'], render,
                        directory / 'validation/render-cases.json', batch))
    source_records = []
    for basis, name, render, expected_path, batch in sources:
        expected = after_by_id(expected_path)
        rendered = after_by_id(render / 'render-cases.json')
        report = read(render / 'rendering-report.json')
        measurements = {(str(m['id']), m['width']): m for m in report['measurements']
                        if m['stage'] == 'after'}
        for qid, payload in expected.items():
            assert payload == rendered[qid], (qid, name, 'render payload differs')
            rows = [measurements[(qid, width)] for width in [893, 375]]
            assert all(m['checkboxCount'] == len(payload['fields']) for m in rows)
            selected[qid] = {'basis': basis, 'source': name, 'render': str(render.relative_to(TASK)),
                             'payload': payload, 'measurements': rows,
                             'committed_batch': batch is not None}
        source_records.append({'name': name, 'basis_after': basis, 'questions': len(expected),
                               'render_directory': str(render.relative_to(TASK)),
                               'report_sha256': digest(render / 'rendering-report.json'),
                               'payload_sha256': digest(render / 'render-cases.json')})
    assert set(selected) == original, {'missing': sorted(original - set(selected)),
                                       'extra': sorted(set(selected) - original)}
    patterns = {
        'literal_backslash': re.escape(chr(92)),
        'literal_dollar_delimiter_or_currency': re.escape('$'),
        'literal_script_syntax': r'[_^](?:\{|[A-Za-z0-9])',
    }
    assert re.search(patterns['literal_backslash'], chr(92) + 'frac{1}{2}')
    assert re.search(patterns['literal_dollar_delimiter_or_currency'], '$x$')
    assert re.search(patterns['literal_script_syntax'], 'x^{2}')
    assert not any(re.search(regex, '𝑥² + 𝑦² ≤ 1') for regex in patterns.values())
    findings = []
    render_errors = []
    for qid, row in selected.items():
        for m in row['measurements']:
            if m['mathErrors'] or m['imageErrors']:
                render_errors.append({'question': int(qid), 'width': m['width'],
                                      'math': m['mathErrors'], 'images': m['imageErrors']})
            assert len(m['choices']) == len(row['payload']['fields'])
            for index, choice in enumerate(m['choices']):
                text = choice['text']
                reasons = [kind for kind, regex in patterns.items() if re.search(regex, text)]
                if reasons:
                    findings.append({'question': int(qid), 'width': m['width'], 'choice_index': index,
                                     'visible_text': text, 'reasons': reasons, 'source': row['source'],
                                     'field': row['payload']['fields'][index]})
    result = {
        'database_writes': 0,
        'passed': not findings and not render_errors,
        'original_census_basis': 3704,
        'latest_confirmed_basis': max(b['basis_after'] for b in batches),
        'checked_questions': len(selected),
        'checked_checkbox_choices': sum(len(row['payload']['fields']) for row in selected.values()),
        'checked_question_views': sum(len(row['measurements']) for row in selected.values()),
        'checked_choice_views': sum(len(m['choices']) for row in selected.values() for m in row['measurements']),
        'widths': [893, 375],
        'selection': 'Already-complete baseline, then only confirmed batches in basis order. Each later confirmed supplemental batch supersedes its earlier values automatically. Full after-render payload equality is required for every selected question.',
        'final_179_plan_sha256': digest(TASK / 'mapping/final-cases.json'),
        'scope': 'Visible checkbox choice text only; this detects leaked TeX syntax, not every possible mathematical omission or solution-formatting issue. Final179 additionally had independent visual inspection.',
        'patterns': patterns,
        'scanner_smoke_checks': {'single_backslash_command_detected': True,
                                'dollar_delimiter_detected': True,
                                'raw_superscript_detected': True,
                                'rendered_unicode_math_not_flagged': True},
        'findings': findings,
        'render_errors': render_errors,
        'source_coverage': dict(Counter(row['source'] for row in selected.values())),
        'sources': source_records,
        'questions': [{'question': int(qid), 'source': row['source'], 'render_directory': row['render'],
                       'choices': len(row['payload']['fields']),
                       'after_payload_sha256': hashlib.sha256(json.dumps(row['payload'], sort_keys=True).encode()).hexdigest()}
                      for qid, row in sorted(selected.items())],
    }
    output = HERE / 'final-visible-choice-audit.json'
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ['sources', 'questions']},
                     indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
