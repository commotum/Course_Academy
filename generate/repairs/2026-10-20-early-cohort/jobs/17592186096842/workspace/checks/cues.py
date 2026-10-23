from audit_helpers import *
OUT=PKG/'evidence'
def inspect(records):
 groups={}
 for r in records:
  f=field(r)
  if not f[':answer-field/type'].endswith('/radio'):continue
  prompt=r['question'][':question/problem'].replace('y =','y=')
  y=latex(prompt.split('$y=',1)[1].split('$')[0].rstrip(',.'))
  vals=[s.simplify(latex(a[':answer/value'])) for a in f[':answer-field/choices']];key=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
  # Compare values at a positive-domain witness, never generator exact metadata.
  if any(v.has(X) for v in vals):
   for t in range(-100,101):
    if all(v.subs(X,t).is_real and v.subs(X,t).is_finite for v in vals):break
   numeric=[v.subs(X,t) for v in vals]
  else:numeric=vals
  order=sorted(range(5),key=lambda i:float(numeric[i]));absorder=sorted(range(5),key=lambda i:abs(float(numeric[i])))
  lengths=[len(a[':answer/value']) for a in f[':answer-field/choices']]
  tests={
   'uniquely_shortest':lengths.count(min(lengths))==1 and lengths[key]==min(lengths),
   'uniquely_longest':lengths.count(max(lengths))==1 and lengths[key]==max(lengths),
   'unique_sign':sum(s.sign(v)==s.sign(numeric[key]) for v in numeric)==1,
  }
  if all(v.is_Rational for v in vals):
   den=[v.q for v in vals];num=[abs(v.p) for v in vals]
   tests['unique_smallest_denominator']=den.count(min(den))==1 and den[key]==min(den)
   tests['unique_largest_denominator']=den.count(max(den))==1 and den[key]==max(den)
   tests['unique_smallest_numerator']=num.count(min(num))==1 and num[key]==min(num)
  name=r['generation']['template'];g=groups.setdefault(name,{'n':0,'positions':[0]*5,'numeric_ranks':[0]*5,'absolute_ranks':[0]*5,'signs':{},'cues':{},'semantic_instances':set()})
  g['n']+=1;g['positions'][key]+=1;g['numeric_ranks'][order.index(key)]+=1;g['absolute_ranks'][absorder.index(key)]+=1
  sign=str(s.sign(numeric[key]));g['signs'][sign]=g['signs'].get(sign,0)+1
  for k,v in tests.items():g['cues'][k]=g['cues'].get(k,0)+int(v)
  g['semantic_instances'].add(prompt)
 for g in groups.values():
  g['semantic_instances']=len(g['semantic_instances'])
  assert max(g['positions'])<g['n'] and max(g['numeric_ranks'])<g['n']
  assert all(v<g['n'] for v in g['cues'].values()),g
 return groups
raw=inspect(json.load(open(OUT/'radio-sample.json')))
delivered=inspect(sum([json.load(open(OUT/f'delivery-radio-{level}/accepted.json')) for level in ['easy','moderate','hard']],[]))
assert raw==delivered
result={'raw':raw,'delivered':delivered,'all_samples_survived':True,'random_position_baseline':0.2,'limits':'These are specific cue probes, not a proof against every possible strategy. Sign and coefficient recognition using differentiation are legitimate mathematical reasoning; zero blank slopes remain allowed.'}
(OUT/'cue-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(raw,indent=2))
# Current inventory: only known generated records are probed, not original sources.
inv=json.load(open(PKG.parent/'source/inventory.json'));src=json.load(open(PKG.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions'];original={q[':question/id'] for q in src}
known={'90db644a-fd4a-5c58-b43a-e0452a6336d1','ab67789f-4616-5914-aa8d-59736a54c4f6','f48647ea-8ebd-5583-b713-aef1cac5a291'}
rows=[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'retired':q.get(':question/retired',False),'field_types':[f[':answer-field/type'][':db/ident'] for f in q[':question/answer-fields']]} for q in inv['questions'] if q[':question/id'] not in original]
assert all(q['retired'] for q in rows if q['question_id'] in known)
assert all(q['retired'] or not any(t.endswith('/radio') for t in q['field_types']) for q in rows)
(OUT/'inventory-status.json').write_text(json.dumps({'basis':inv['basis'],'generated_records':rows,'eligible_generated_radios':0,'finding_history':'ab222f0376dcbf24176c: three affected radios are now retired; source radios are not generated and remain unchanged.'},indent=2))
(PKG/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2))
