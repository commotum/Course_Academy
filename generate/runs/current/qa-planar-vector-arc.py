"""Parent verifies actual planar curve, all length choices and full worked stages."""
import argparse,importlib.util,json,re,sys
from pathlib import Path
import sympy as s
import mpmath as mp
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('kp',type=int,nargs='?',default=17592186119744);K=ap.parse_args().kp;assert K in (17592186119744,17592186119860);D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
n=module('parent_planar_norm',R/'arc-norm-parser.py');e=module('parent_planar_eval',R/'arc-evaluation-parser.py');p=n.p;g=module('parent_planar_generator',D.with_suffix('.py'));t=p.p.t
counts=dict(source_questions=0,source_banks=0,source_values=0,source_designations=0,source_missing_designations=0,source_prompts=0,source_solutions=0,source_solution_repairs=0,printed_instances=0,bank_values=0,quadratures=0,derivative_operator_components=0,derivative_components=0,norm_stages=0,integral_stages=0,antiderivative_stages=0,evaluation_stages=0,substitutions=0)
def check(record):
 q=record['question'];curve,bounds=p.prompt(q[':question/problem']);assert len(curve)==(2 if K==17592186119744 else 3)
 normroles,nc=n.stages(q[':question/worked-solution'],curve,bounds);length,evalroles,ec=e.stages(q[':question/worked-solution'],curve,bounds)
 for k,v in {**nc,**ec}.items():counts[k]+=v
 # Independent numerical integration uses only the differentiated printed coordinates.
 mp.mp.dps=45;fn=s.lambdify(t,s.sqrt(sum(s.diff(v,t)**2 for v in curve)),'mpmath');a,b=[mp.mpf(str(s.N(v,45))) for v in bounds];numeric=mp.quad(fn,[a,(a+b)/2,b]);assert abs(numeric-mp.mpf(str(s.N(length,45))))<mp.mpf('1e-32'),(numeric,length)
 counts['quadratures']+=1
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];assert f[':answer-field/type'].endswith('/radio');bank=f[':answer-field/choices'];assert len(bank)==5
 values=[p.math(a[':answer/value']) for a in bank];assert all(v.is_real is not False and s.N(v,30)>0 for v in values)
 assert all(not p.same(v,w) for i,v in enumerate(values) for w in values[:i])
 assert [a[':answer/id'] for a,v in zip(bank,values) if p.same(v,length)]==[f[':answer-field/correct'][1]]
 counts['bank_values']+=5;counts['printed_instances']+=1;return curve,bounds,normroles,evalroles

def mask(text):return re.sub(r'\s+',' ',p.MATH.sub('$MATH$',re.sub(r'!\[[^\]]*\]\([^)]*\)','IMAGE',text))).strip()
qs={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 sid=case['source_id'];old=qs[sid];r=g.generate(case.get('level',case.get('difficulty')),template=case['template'],parameters=case['parameters'],profile=case.get('bank_profile',case.get('profile')));curve,bounds,nroles,eroles=check(r);oc,ob=p.prompt(old[':question/problem']);assert len(oc)==len(curve) and all(p.same(a,b) for a,b in zip(oc,curve)) and ob==bounds
 assert mask(old[':question/problem'])==mask(r['question'][':question/problem']);counts['source_prompts']+=1
 sol=old.get(':question/worked-solution')
 if sol:
  if sid=='q-77220':sol=sol.replace(r'16{t}^{2}{cos}^{2}⁡t+16{t}^{2}{sin}^{2}',r'16{t}^{2}{cos}^{2}⁡2t+16{t}^{2}{sin}^{2}⁡2t');counts['source_solution_repairs']+=1
  assert mask(sol)==mask(r['question'][':question/worked-solution']);assert n.stages(sol,oc,ob)[0]==nroles and e.stages(sol,oc,ob)[1]==eroles;counts['source_solutions']+=1
 f=old[':question/answer-fields'][0];nf=r['question'][':question/answer-fields'][0];remaining=[p.math(v[':answer/value']) for v in nf[':answer-field/choices']]
 for answer in f[':answer-field/choices']:
  val=p.math(answer[':answer/value']);indices=[i for i,v in enumerate(remaining) if p.same(val,v)];assert len(indices)==1,(sid,answer,remaining);remaining.pop(indices[0]);counts['source_values']+=1
 assert not remaining;counts['source_banks']+=1
 if f.get(':answer-field/correct'):
  selected=next(v[':answer/value'] for v in nf[':answer-field/choices'] if v[':answer/id']==nf[':answer-field/correct'][1]);assert p.same(p.math(selected),p.math(f[':answer-field/correct'][':answer/value']));counts['source_designations']+=1
 else:counts['source_missing_designations']+=1
 counts['source_questions']+=1
for item in json.loads((D/'review.json').read_text()):check(item.get('record',item))
for item in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(item)
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
