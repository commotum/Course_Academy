"""Combine full before/after rendering with the final label-boundary delta."""
import collections, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
full = json.loads((HERE / 'browser-report.json').read_text())
delta = json.loads((HERE / 'browser-label-boundaries/browser-report.json').read_text())
changes = json.loads((HERE / 'changes.json').read_text())
current = {(c['entity'], c['attribute']): c for c in changes}
delta_inputs = json.loads((HERE / 'browser-label-boundaries/browser-inputs.json').read_text())
assert len(delta_inputs) == 14
assert all(c == current[c['entity'], c['attribute']] for c in delta_inputs)
merged = {}
for report in [full, delta]:
    assert not report['errors']
    for batch in report['report']:
        assert not batch['exceptions']
        for item in batch['items']:
            merged[batch['width'], batch['stage'], item['entity'], item['attribute']] = item
assert len(merged) == len(changes) * 4
findings = {'unchanged_math_errors': [], 'preexisting_overflow': [], 'resolved_math_errors': []}
for (width, stage, entity, attribute), after in merged.items():
    if stage != 'after':
        continue
    before = merged[width, 'before', entity, attribute]
    assert not collections.Counter(after['errors']) - collections.Counter(before['errors'])
    assert not after['overflow'] or before['overflow']
    assert not after['proseOverflow'] or before['proseOverflow']
    assert not after['literalBraceText']
    assert after['mathCount'] == before['mathCount']
    item = {'width': width, 'entity': entity, 'attribute': attribute}
    if after['errors']:
        findings['unchanged_math_errors'].append({**item, 'errors': sorted(set(after['errors']))})
    elif before['errors']:
        findings['resolved_math_errors'].append({**item, 'errors': sorted(set(before['errors']))})
    if after['overflow'] or after['proseOverflow']:
        findings['preexisting_overflow'].append(item)
(HERE / 'preexisting-render-findings.json').write_text(json.dumps(findings, indent=2) + '\n')
plan = json.loads((HERE / 'plan.json').read_text())
result = {
    'passed': True, 'transaction_sha256': plan['transaction_sha256'],
    'fields_checked': len(changes), 'widths': [893, 375],
    'full_before_after_renders': len(changes) * 4, 'final_label_delta_renders': len(delta_inputs) * 4,
    'full_run_transaction_sha256_before_label_grouping': '8c53d1ebb5f79df87f78d90c33a4cd70e47f9727fc3ae989901fb25852d22c1a',
    'final_label_delta_fields': 14, 'no_new_math_errors_or_overflow': True,
    'no_raw_brace_glyph_text': True, 'math_expression_counts_unchanged': True,
    'unchanged_error_fields': len({(v['entity'], v['attribute']) for v in findings['unchanged_math_errors']}),
    'preexisting_overflow_fields': len({(v['entity'], v['attribute']) for v in findings['preexisting_overflow']}),
    'resolved_math_error_fields': len({(v['entity'], v['attribute']) for v in findings['resolved_math_errors']}),
    'note': 'The 20 remaining parse-error fields contain preexisting overset-of-caret hat errors. '
            'They are unchanged by this brace repair. The assistive-MathML brace metric in raw reports '
            'is unavailable in the app configuration and is not used as a check. '
            'Geometry is covered by importer regression tests and inspected sample screenshots.'
}
(HERE / 'browser-validation.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
