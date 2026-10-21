"""Probe both demonstrated visible cues on every captured inventory record."""
import json,pathlib,sys
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent.parent;E=ROOT/'evidence'
inv=json.loads((ROOT.parent/'source/inventory.json').read_text());D=r'\frac{\text{d}y}{\text{d}x}';rows=[]
for q in inv['questions']:
 f=q[':question/answer-fields'][0];cs=f[':answer-field/choices'];k=f[':answer-field/correct'][':answer/id'];ki=next(i for i,a in enumerate(cs) if a[':answer/id']==k)
 ns=[a[':answer/value'].replace(D,'D').count(r'\frac') for a in cs]
 zero=ns.count(0)==1 and ns[ki]==0;most=ns.count(max(ns))==1 and ns[ki]==max(ns);is_source=':question/math-academy-id' in q
 rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'is_source':is_source,'fraction_counts_outside_derivative':ns,'unique_fractionless_success':zero,'unique_max_fractions_success':most})
 assert is_source or not(zero or most), 'Affected generated inventory needs exact complete-record reproduction'
(E/'inventory-probe.json').write_text(json.dumps({'basis':inv['basis'],'tested':rows,'generated_tested':sum(not r['is_source'] for r in rows),'generated_affected':0,'limits':'All six captured generated records tested for both demonstrated fraction-layout cues; verified absence of these cues in this captured pool, not a statement about uncaptured inventory or unrelated defects.'},indent=2)+'\n')
(E/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2)+'\n')
print('inventory: 16 complete records inspected; 6 generated tested, 0 affected by either demonstrated cue; source items remain source')
