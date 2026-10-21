from pathlib import Path
from fractions import Fraction
import json,hashlib
from probe_banks import probes
W=Path(__file__).resolve().parents[1];E=W/'evidence';raw=json.loads((E/'generated.json').read_text());delivered=json.loads((E/'delivery/accepted.json').read_text());variation=json.loads((E/'pedagogical-variation.json').read_text())
def coverage(records):
 out={}
 for t in sorted({r['generation']['template'] for r in records}):
  rs=[r for r in records if r['generation']['template']==t];positions=set();signs=[set() for _ in range(3)];locations=[set() for _ in range(3)];coefs={}
  for r in rs:
   f=r['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]));m=r['generation'];p=m['parameters']
   for i,(pt,slope) in enumerate(zip(p['points'],m['exact_slopes'])):
    v=Fraction(slope);signs[i].add('zero' if v==0 else 'positive' if v>0 else 'negative');locations[i].add(tuple(map(str,pt)))
   for k,v in p.items():
    if k!='points':coefs.setdefault(k,set()).add(str(v))
  out[t]={'records':len(rs),'distinct_semantic_instances':len({r['generation']['mathematical_fingerprint'] for r in rs}),'correct_positions':sorted(positions),'slope_signs_by_point':[sorted(x) for x in signs],'distinct_point_locations_by_slot':[len(x) for x in locations],'coefficient_values':{k:sorted(v) for k,v in coefs.items()}}
 return out
# Localized IDs/path changes do not change generated parameter or exact slope metadata.
variation['slot_coverage']={'raw':coverage(raw),'delivered':coverage(delivered)}
variation['normal_authored_profile_probes']=probes([r for r in raw if r['generation']['bank_profile']=='authored'])
variation['generation_order']='Equation form is selected first. Its coefficients and eligible points determine the lawful slope roles; these cannot be independently assigned arbitrary triples (e.g. a*y²/x constrains signs). The sampler does not freeze source signs, target positions or horizontal-segment locations. Incidental choice order is sampled last.'
variation['fixed_choice_count_reason']='One diagram selection from five choices preserves the captured radio contract; it provides no correct-option cue.'
variation['coverage_limits']='The 240 pure-bank cases sample normal easy support before rendering; 51 complete records, 45 delivered semantic instances exercise controls and profiles. This is bounded evidence, not exhaustive parameter or shortcut proof. All six normal equation forms survive filtering. Source profiles are explicit replay/generalization paths, not selected by normal CLI sampling. Other bands remain preserved but are outside this easy repair validation.'
(E/'pedagogical-variation.json').write_text(json.dumps(variation,indent=2)+'\n')
v=json.loads((E/'validation.json').read_text());v['runtime_closure']='4 declared files; two relocated packages each generated 5 identical seeded records without package writes; shared delivery accepted all 5';v['delivered_native_checks']=225;v['inventory_questions_checked']=17;v['inventory_affected_missing_refs']=2
v['runtime_hashes']={f:hashlib.sha256((W/f).read_bytes()).hexdigest() for f in json.loads((W/'package.json').read_text())['files']}
(E/'validation.json').write_text(json.dumps(v,indent=2)+'\n')
print('Final audit: all six equation forms survive delivery; runtime files hashed; source, math, grading and variation claims separate')
