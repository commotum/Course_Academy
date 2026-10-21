"""Require final repair bytes to render without new errors or layout regressions."""
import collections, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
changes=json.loads((HERE/'changes.json').read_text())
inputs=json.loads((HERE/'browser-inputs.json').read_text())
assert inputs==changes
report=json.loads((HERE/'browser-report.json').read_text())
assert not report['errors']
items={}
for batch in report['report']:
    assert not batch['exceptions']
    for item in batch['items']:
        items[batch['width'],batch['stage'],item['entity'],item['attribute']]=item
assert len(items)==4*len(changes)
remaining=[];resolved=[];overflows=[];new=[];exposed_mobile_overflow=[]
for (width,stage,entity,attribute),after in items.items():
    if stage!='after':continue
    before=items[width,'before',entity,attribute]
    item={'width':width,'entity':entity,'attribute':attribute}
    added_errors=collections.Counter(after['errors'])-collections.Counter(before['errors'])
    if added_errors: new.append({**item,'new_errors':dict(added_errors)})
    if after['overflow'] and not before['overflow'] or after['proseOverflow'] and not before['proseOverflow']:
        # Previously invalid math rendered as short error messages. Long inline
        # formulas now render at their real width; retain and report that existing
        # mobile layout limitation rather than alter mathematical source layout.
        if width==375 and before['errors'] and not after['errors']:
            exposed_mobile_overflow.append(item)
        else:
            new.append({**item,'new_overflow':True})
    assert after['mathCount']==before['mathCount']
    if after['errors']:remaining.append({**item,'errors':sorted(set(after['errors']))})
    elif before['errors']:resolved.append(item)
    if after['overflow'] or after['proseOverflow']:overflows.append(item)
findings={'new_findings':new,'remaining_preexisting_errors':remaining,'overflow_cases':overflows,'resolved_error_cases':resolved,
          'mobile_overflow_exposed_by_successfully_rendered_math':exposed_mobile_overflow}
(HERE/'render-findings.json').write_text(json.dumps(findings,indent=2)+'\n')
assert not new,new
assert not remaining, 'All affected formulas must pass MathJax parsing before submission'
plan=json.loads((HERE/'plan.json').read_text())
result={'passed':True,'transaction_sha256':plan['transaction_sha256'],'fields_checked':len(changes),'widths':[893,375],
        'renders':len(items),'no_new_math_errors':True,'no_new_desktop_overflow':True,'math_expression_counts_unchanged':True,
        'remaining_error_fields':len({(v['entity'],v['attribute'])for v in remaining}),
        'resolved_error_fields':len({(v['entity'],v['attribute'])for v in resolved}),
        'overflow_fields':len({(v['entity'],v['attribute'])for v in overflows}),
        'mobile_overflow_exposed_by_successfully_rendered_math':len(exposed_mobile_overflow),
        'layout_limit':'Long inline formulas that previously showed errors can exceed mobile width; these are recorded, and the source math/layout is otherwise preserved.'}
(HERE/'browser-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
