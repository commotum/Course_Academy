"""Root checks exact setup/stages and high-precision complete integral banks."""
import importlib.util,json,re,functools
from pathlib import Path
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parent;K=17592186152159;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('independent_scalar_setup_reader',R/'scalar-line-parser.py');g=module('reviewed_scalar_setup_generator',D.with_suffix('.py'))
counts={'printed_instances':0,'complete_choices_evaluated':0,'source_banks':0,'source_values':0,'source_existing_refs':0,'source_missing_ref_derived':0,'source_full_prose_and_stage_sequences':0,'source_ambiguous_banks':0}
@functools.lru_cache(maxsize=2048)
def value(fn,a,b,dps=70):
 with mp.workdps(dps):
  lo,hi=mp.mpf(str(s.N(a,dps+10))),mp.mpf(str(s.N(b,dps+10)));f=s.lambdify(p.t,fn,'mpmath');v=mp.quad(f,[lo+(hi-lo)*i/8 for i in range(9)]);assert mp.isfinite(v) and not isinstance(v,mp.mpc),(fn,a,b,v);return +v
def same(a,b):
 with mp.workdps(70):return abs(a-b)<=mp.mpf('1e-45')*max(1,abs(a),abs(b))
def setup(raw):
 raw=re.sub(r'^-\s*(?=\{?\\int)','-1',raw);a,b,fn,var=p.e.integral(raw);assert var==p.t;return fn,a,b
def check(r):
 q=r['question'];details=p.prompt(q[':question/problem']);c=p.stages(q[':question/worked-solution'],details)
 assert c['primitive_rows']==c['evaluation_rows']==0,'setup KP must stop at definite integral'
 for key,n in c.items():counts[key]=counts.get(key,0)+n
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/type']==':answer-field.type/radio';choices=f[':answer-field/choices'];forms=[setup(a[':answer/value']) for a in choices];vs=[value(*v) for v in forms];assert len(vs)==5
 expected=value(details[6],*details[3]);good=[same(v,expected) for v in vs];selected=[i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1]];assert len(selected)==1 and good[selected[0]] and sum(good)==1,(q,vs,expected)
 fn,a,b=forms[selected[0]];assert p.equal(a,details[3][0]) and p.equal(b,details[3][1]) and p.equal(fn,details[6],details[3]),'correct setup structure must match actual graph method'
 collisions=[(i,j) for i,v in enumerate(vs) for j,w in enumerate(vs[:i]) if same(v,w)]
 if collisions:
  assert r['generation'].get('evidence_only') and r['generation']['template'] in ('quadratic_ratio','linear_difference'),(q,collisions)
  # Confirm the near-equality again at 100 digits before recording source defect.
  for i,j in collisions:
   with mp.workdps(100):assert abs(value(*forms[i],dps=100)-value(*forms[j],dps=100))<mp.mpf('1e-75')
  counts['source_ambiguous_banks']+=1
 counts['printed_instances']+=1;counts['complete_choices_evaluated']+=5;return q,details,c
def mask(text):return re.sub(r'\s+',' ',p.p.MATH.sub('$MATH$',text)).strip()
sources={key:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions'] for key in (q[':question/math-academy-id'],q[':db/id'],q[':question/id'])}
for case in json.loads((D/'source-cases.json').read_text()):
 old=sources[case['source_id']];r=g.generate(case.get('level','easy'),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile'));q,details,c=check(r);od=p.prompt(old[':question/problem']);assert p.equal(od[0],details[0]) and p.equal(od[1],details[1]) and all(p.equal(a,b) for a,b in zip(od[3],details[3]))
 of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];vs=[setup(a[':answer/value']) for a in nf[':answer-field/choices']]
 for a in of[':answer-field/choices']:
  fn,lo,hi=setup(a[':answer/value']);matches=[i for i,(F,A,B) in enumerate(vs) if p.equal(A,lo) and p.equal(B,hi) and p.equal(F,fn,(lo,hi))];assert matches,(case,a,vs);vs.pop(matches[0]);counts['source_values']+=1
 assert not vs;counts['source_banks']+=1
 selected=next(setup(a[':answer/value']) for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1])
 if of.get(':answer-field/correct'):
  fn,lo,hi=setup(of[':answer-field/correct'][':answer/value']);assert p.equal(selected[0],fn,(lo,hi)) and p.equal(selected[1],lo) and p.equal(selected[2],hi);counts['source_existing_refs']+=1
 else:counts['source_missing_ref_derived']+=1
 if old.get(':question/worked-solution'):assert mask(old[':question/worked-solution'])==mask(q[':question/worked-solution']);assert p.stages(old[':question/worked-solution'],od)==c;counts['source_full_prose_and_stage_sequences']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts.update(database_writes=0,complete_value_check='70-digit subdivided quadrature, relative tolerance1e-45; source collisions rechecked100digits1e-75; exact correct integrands/bounds and displayed stages independently symbolic');(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
