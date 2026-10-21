"""Add distinct, source-notation equivalents without assuming logarithm identities."""
import json
from pathlib import Path
import sympy as s
import generator as g
p=Path('evidence/engine-input.json');cases=json.loads(p.read_text());count=0
for c in cases:
 r=c['record'];f=r['question'][':question/answer-fields'][0]
 if not f[':answer-field/type'].endswith('/blank'):continue
 val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);expr=g.parse(val)
 args=expr.args if expr.is_Mul or expr.is_Add else [expr]
 join=r'\cdot ' if expr.is_Mul else '+'
 alt=join.join(r'\left('+g.tex(z)+r'\right)' for z in reversed(args))
 assert alt!=val and s.simplify(g.parse(alt)-expr)==0
 if not any(ch['purpose']=='reordered factors or sum terms' for ch in c['checks']):c['checks'].append({'submitted':alt,'expected':'accepted','purpose':'reordered factors or sum terms'})
 count+=1
p.write_text(json.dumps(cases,indent=2,ensure_ascii=False))
Path('evidence/equivalent-response-summary.json').write_text(json.dumps({'distinct_equivalents':count,'method':'Reverse product factors or additive terms, grouping each factor; preserve source ln constants.'},indent=2))
print('distinct equivalent responses',count)
