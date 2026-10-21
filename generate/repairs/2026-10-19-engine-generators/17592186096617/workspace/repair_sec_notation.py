"""Refresh only q-1931 after preserving tan'=sec² in its correct option."""
import json,re
from pathlib import Path
import sympy as s
import generator as g
E=Path('evidence');changed=0

def fresh(r):
 global changed
 if r['generation']['template']!='q-1931':return r
 m=r['generation'];out=g.generate('easy',seed=m['seed'],template=m['template'],parameters=m['parameters'],missing_term=m['missing_term'])
 # Read the displayed product, then independently differentiate it and each solution stage.
 product=g.parse(re.search(r'\$([^$]*)\$',out['question'][':question/problem'])[1].rstrip('.'))
 full=s.diff(product,g.X);f=out['question'][':question/answer-fields'][0]
 for a in f[':answer-field/choices']:
  actual=s.trigsimp(s.simplify(g.parse(a[':answer/value'])-full))==0
  assert actual==(a[':answer/id']==f[':answer-field/correct'][1])
 assert r'\sec^{2}' in next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 changed+=1;return out
records=json.loads((E/'test-records.json').read_text());records=[fresh(r) for r in records];(E/'test-records.json').write_text(json.dumps(records,indent=2,ensure_ascii=False))
pairs=json.loads((E/'counterfactuals.json').read_text())
for p in pairs:
 for side in ['before','after']:p[side]=fresh(p[side])
(E/'counterfactuals.json').write_text(json.dumps(pairs,indent=2,ensure_ascii=False))
cases=json.loads((E/'engine-input.json').read_text())
for c in cases:
 if c['record']['generation']['template']=='q-1931':
  c['record']=fresh(c['record']);f=c['record']['question'][':question/answer-fields'][0]
  c['checks']=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete bank key and distractors after sec notation repair'} for a in f[':answer-field/choices']]
(E/'engine-input.json').write_text(json.dumps(cases,indent=2,ensure_ascii=False))
(E/'sec-notation-repair.json').write_text(json.dumps({'passed':True,'affected_template':'q-1931','updated_records_including_evidence_copies':changed,'check':'independent differentiation of displayed product, all five bank choices and source sec-squared notation','reason':'Unexpanded CAS tan-squared-plus-one created a longest-option cue and diverged from the taught derivative notation.'},indent=2))
print('affected notation repair PASS',changed)
