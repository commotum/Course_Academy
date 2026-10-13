"""Root independent displayed-field, full-bank, formal-row and real-domain QA."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186133876'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'divergence-readback.py','root_readback');g=load(D.with_suffix('.py'),'g')
n=dict(records=0,choices=0,whole_method_banks=0,formal_component_inputs=0,printed_equalities=0,raw_nonreal_domain_records=0,raw_inherited_context_records=0,source_banks=0,source_values=0,source_solutions=0,source_designations=0,source_missing_designations=0)
def equal(a,b):return s.simplify(a-b)==0
def check(r):
 q=r['question'];gm=r['generation'];raw=gm.get('evidence_only',gm.get('eligible_learner') is False);assert gm.get('eligible_for_learning')==not_raw(raw)
 prompt=q[':question/problem'];sol=q.get(':question/worked-solution','');components=p.field(prompt,raw);pt=p.point(prompt,raw)
 if components is None:
  assert raw;_,inputs=p.derivative_inputs(sol);assert len(inputs)>=2;components=tuple(p.scalar(t[1],True) for t in inputs[:2])+(s.Integer(0),);n['raw_inherited_context_records']+=1
 assert components[2]==0
 px,qy=s.diff(components[0],p.p.x),s.diff(components[1],p.p.y);div=px+qy
 subs=dict(zip(p.variables,pt)) if pt else {}
 ev=lambda t:s.simplify(t.subs(subs,simultaneous=True))
 expected=ev(div);domain_bad=False
 if pt:
  for z in components[:2]:
   v=ev(z)
   if v.is_real is False or v.has(s.zoo,s.nan,s.oo):domain_bad=True
  if domain_bad:assert raw and gm['source_id']=='q-123175';n['raw_nonreal_domain_records']+=1
 for f in q.get(':question/answer-fields',[]):
  vals=[p.scalar(z[':answer/value'],raw) for z in f[':answer-field/choices']]
  assert all(not equal(z,t) for i,z in enumerate(vals) for t in vals[:i])
  good=[i for i,z in enumerate(vals) if not z.has(*p.basis) and equal(z,expected)];assert len(good)==1
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][1]==f[':answer-field/choices'][good[0]][':answer/id']
  n['choices']+=len(vals)
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
  if not raw and f[':answer-field/type'].endswith('/radio'):
   bank=[expected,ev(px-qy),ev(-px-qy),ev(px),ev(2*px+qy)];assert all(sum(equal(z,t) for z in vals)==1 for t in bank);n['whole_method_banks']+=1
 # Check generic formal definition and every ordered derivative/reduction/evaluation row.
 for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
  if r'\begin{aligned}' not in block:
   rhs=block.strip().split('=')[-1]
   if re.match(r'[FV]\(x,y\)=',block):assert all(equal(z,c) for z,c in zip(p.vector(rhs,raw),components))
   else:
    v,_=p.operator_rhs(rhs,components,raw);assert equal(v,div),(gm['template'],block,v,div)
   n['printed_equalities']+=1;continue
  body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=body.split(r'\\')
  for ix,row in enumerate(rows):
   row=row.strip();assert '& =' in row,row;left,rhs=row.split('& =',1)
   value,inputs=p.operator_rhs(rhs,components,raw)
   if inputs:
    assert [t[0] for t in inputs]==['x','y'];assert all(equal(p.scalar(t[1],raw),c) for t,c in zip(inputs,components[:2]));n['formal_component_inputs']+=2
   # The numeric block's first LHS explicitly displays evaluation at a tuple or |.
   if ix==0:evaluated=('|' in left or re.search(r'\)\s*\(',left) is not None)
   assert equal(value,expected if evaluated else div),(left,rhs,div,expected);n['printed_equalities']+=1
 if not raw:
  assert p.field(prompt) is not None
  assert sol.count('When differentiating')==1
 n['records']+=1

def not_raw(value):return not value

if __name__=='__main__':
 cases=json.load(open(D/'source-cases.json'));old={q[':question/id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in cases:
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']];assert q[':question/problem']==o[':question/problem']
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in o)
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
  for of,gf in zip(o[':question/answer-fields'],q.get(':question/answer-fields',[])):
   assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in gf[':answer-field/choices']);n['source_banks']+=1;n['source_values']+=len(gf[':answer-field/choices']);assert (':answer-field/correct' in of)==(':answer-field/correct' in gf)
   if ':answer-field/correct' in of:assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1]);n['source_designations']+=1
   else:n['source_missing_designations']+=1
  for scale in (2,-3):check(g.generate(c['level'],profile=c['bank_profile'],parameters={'c':scale}))
 for template,spec in g.TEMPLATES.items():
  for seed in range(9):
   r=g.generate(spec['level'],seed+6000,template=template);check(r);z=g.generate(spec['level'],seed+3000,template=template,profile=r['generation']['bank_profile'],parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id']
 review=json.load(open(D/'review.json'))
 for r in review:check(r.get('record',r))
 (R/'qa/17592186133876-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
