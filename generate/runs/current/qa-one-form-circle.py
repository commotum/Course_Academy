"""Independent displayed one-form, path, complete bank and ordered-stage audit."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parent;K=17592186179673;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('parent_circle_math',R/'one-form-parser.py');g=module('parent_circle_gen',D.with_suffix('.py'));mp.mp.dps=60
counts={'printed_instances':0,'source_prompts':0,'source_solutions':0,'raw_source_banks':0,'raw_source_values':0,'raw_ambiguous_banks':0,'eligible_repaired_banks':0,'eligible_original_value_matches':0,'scalar_bank_values':0}
def number(expr):
 assert not expr.free_symbols,expr
 return mp.mpf(str(s.N(expr,65)))
def definite(f,lo,hi):
 f=s.simplify(s.trigsimp(f));a,b=number(lo),number(hi);fun=s.lambdify(p.t,f,'mpmath');return mp.quad(fun,[a,a+(b-a)/4,(a+b)/2,b-(b-a)/4,b])
def near(a,b):return abs(a-b)<mp.mpf('1e-40')*max(1,abs(a),abs(b))
def check(r,raw=False):
 q=r['question'];P,Q=p.oneform(q[':question/problem']);path,limits,points=p.ellipse(q[':question/problem']);f=p.evaluate_form(P,Q,path);I=definite(f,*limits)
 field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==5;values=[];structural=[]
 for a in field[':answer-field/choices']:
  text=p.blocks(a[':answer/value']) or [a[':answer/value']];assert len(text)==1
  if q[':question/difficulty'].endswith('/easy'):
   F,lo,hi=p.integral(text[0]);v=definite(F,lo,hi);structural.append(p.equivalent(F,f) and p.equivalent(lo,limits[0]) and p.equivalent(hi,limits[1]))
  else:v=number(p.scalar(text[0]));structural.append(near(v,I))
  values.append(v);counts['scalar_bank_values']+=1
 chosen=[n for n,a in enumerate(field[':answer-field/choices']) if a[':answer/id']==field[':answer-field/correct'][1]];assert len(chosen)==1 and structural[chosen[0]] and near(values[chosen[0]],I),(q,values,I)
 collisions=[(j,k) for j,v in enumerate(values) for k,w in enumerate(values[:j]) if near(v,w)]
 if raw and q.get(':question/math-academy-id')=='q-124656':assert len(collisions)==1;counts['raw_ambiguous_banks']+=1
 else:assert not collisions,(q[':question/problem'],values)
 for key,val in p.stages(q[':question/worked-solution'],P,Q,path,limits).items():counts[key]=counts.get(key,0)+val
 counts['printed_instances']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=sources[sid];r=g.generate(case['difficulty'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);q=r['question']
 # Explicit replay metadata may omit external MA id; ambiguity allowed only by source case.
 if sid=='q-124656':q=dict(q);q[':question/math-academy-id']=sid;r=dict(r,question=q)
 check(r,raw=True)
 for key,ct in ((':question/problem','source_prompts'),(':question/worked-solution','source_solutions')):assert q[key]==old[key],(sid,key);counts[ct]+=1
 field=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in field[':answer-field/choices'])==sorted(a[':answer/value'] for a in nf[':answer-field/choices']);counts['raw_source_banks']+=1;counts['raw_source_values']+=5
 oldcorrect=field[':answer-field/correct'][':answer/value'];nc=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert oldcorrect==nc
 eligible=g.generate(case['difficulty'],template=case['template'],parameters=case['parameters']);eq=check(eligible);counts['eligible_repaired_banks']+=1;newvals=[a[':answer/value'] for a in eq[':question/answer-fields'][0][':answer-field/choices']];counts['eligible_original_value_matches']+=sum(a[':answer/value'] in newvals for a in field[':answer-field/choices'])
for item in json.loads((D/'review.json').read_text()):
 r=item.get('record',item)
 # Raw ambiguous replay is already accounted separately.
 if r.get('generation',{}).get('profile')=='observed_q-124656':continue
 check(r)
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
