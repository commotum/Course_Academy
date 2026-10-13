"""Root independent 3D printed-field, formal-input, complete-bank and ordered-row QA."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186133889'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'divergence-readback.py','root_readback');g=load(D.with_suffix('.py'),'g')
# The source's bare multivariable sin yz / ln xy notation groups the full product.
# Normalize those complete function arguments before parsing, independently of worker masks.
original_scalar=p.scalar
original_operator=p.operator_rhs
def function_products(t):
 return re.sub(r'(\\operatorname\{(?:ln|sin)\}⁡)\s*([xyz]{2})(?![A-Za-z])',lambda m:m[1]+'('+m[2]+')',t)
def scalar(t,evidence=False):return original_scalar(function_products(t),evidence)
def operator(t,components,evidence=False):return original_operator(function_products(t),components,evidence)
p.scalar=scalar;p.operator_rhs=operator
n=dict(records=0,choices=0,whole_method_banks=0,formal_component_inputs=0,printed_equalities=0,raw_inherited_context_records=0,supported_prompt_repairs=0,source_banks=0,source_values=0,source_solutions=0,source_designations=0)
def eq(a,b):return s.simplify(a-b)==0
def field(prompt,raw=False):
 m=re.search(r'\$([FG])=([^$]+)\$',prompt)
 if m:
  t=m[2].strip().rstrip('.,')
  if t.startswith('⟨'):return tuple(p.scalar(z,raw) for z in t[1:-1].replace(r'\,','').split(','))
  return p.vector(t,raw)
 return None
def check(r):
 q=r['question'];gm=r['generation'];raw=gm['evidence_only'];assert gm['eligible_for_learning']==(not raw)
 prompt=q[':question/problem'];sol=q[':question/worked-solution'];components=field(prompt,raw);pt=p.point(prompt,raw)
 if components is None:
  assert raw;_,inputs=p.derivative_inputs(sol);assert len(inputs)==3;components=tuple(p.scalar(t[1],True) for t in inputs);n['raw_inherited_context_records']+=1
 assert len(components)==3
 derivatives=[s.diff(c,v) for c,v in zip(components,p.variables)];div=sum(derivatives);subs=dict(zip(p.variables,pt)) if pt else {};ev=lambda t:s.simplify(t.subs(subs,simultaneous=True));expected=ev(div)
 if pt:assert all(ev(c).is_real is not False and not ev(c).has(s.zoo,s.nan,s.oo) for c in components)
 if gm['template']=='product_log':assert 'Assume $2+xz>0.$' in prompt
 for f in q[':question/answer-fields']:
  vals=[p.scalar(z[':answer/value'],raw) for z in f[':answer-field/choices']];assert all(not eq(z,t) for i,z in enumerate(vals) for t in vals[:i])
  good=[i for i,z in enumerate(vals) if not z.has(*p.basis) and eq(z,expected)];assert len(good)==1,(gm['template'],expected,vals)
  assert f[':answer-field/correct'][1]==f[':answer-field/choices'][good[0]][':answer/id'];n['choices']+=len(vals)
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
  elif not raw:
   if eq(derivatives[2],0):
    a,b=derivatives[:2];bank=[expected,ev(a),ev(b),ev(-a+b),ev(div+components[2])]
   else:bank=[expected,*[ev(div-d) for d in derivatives],ev(-div)]
   assert all(sum(eq(z,t) for z in vals)==1 for t in bank);n['whole_method_banks']+=1
 for block in re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S):
  if r'\begin{aligned}' not in block:
   value,_=p.operator_rhs(block.strip().split('=')[-1],components,raw);assert eq(value,div);n['printed_equalities']+=1;continue
  rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
  for ix,row in enumerate(rows):
   left,rhs=row.strip().split('& =',1);value,inputs=p.operator_rhs(rhs,components,raw)
   if inputs:
    assert [t[0] for t in inputs]==list('xyz');assert all(eq(p.scalar(t[1],raw),c) for t,c in zip(inputs,components));n['formal_component_inputs']+=3
   if ix==0:evaluated=bool(pt and (re.search(r'\)\s*\(',left) or re.search(r'F\(',left)))
   assert eq(value,expected if evaluated else div),(gm['template'],left,rhs,value,div,expected);n['printed_equalities']+=1
 if not raw:
  assert field(prompt) is not None
  assert 'the divergence' in sol and 'scalar field' in sol
  if gm['profile_origin']=='supported_presentation_repair':n['supported_prompt_repairs']+=1
 n['records']+=1
if __name__=='__main__':
 frozen=json.load(open(D/'frozen-shas.json'))
 for k,v in frozen['artifacts'].items():assert hashlib.sha256((R.parents[2]/k).read_bytes()).hexdigest()==v,k
 cases=json.load(open(D/'source-cases.json'));old={q[':question/id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in cases:
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']];assert q[':question/problem']==o[':question/problem'];assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_solutions']+=1
  for of,gf in zip(o[':question/answer-fields'],q[':question/answer-fields']):
   assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in gf[':answer-field/choices']);n['source_banks']+=1;n['source_values']+=len(gf[':answer-field/choices']);assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in gf[':answer-field/choices'] if z[':answer/id']==gf[':answer-field/correct'][1]);n['source_designations']+=1
  for scale in (2,-3):check(g.generate(c['level'],profile=c['bank_profile'],parameters={'scale':scale}))
 for level,templates in g.TEMPLATES.items():
  for template in templates:
   for seed in range(9):
    r=g.generate(level,seed+6300,template=template);check(r);z=g.generate(level,seed+8000,template=template,profile=r['generation']['bank_profile'],parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id'];check(g.generate(level,seed+6300,template=template,field_type='blank'))
 for template in ('zero_terms','axial'):
  for scale in (1,2,-3):check(g.generate('easy',template=template,parameters={'scale':scale}))
 for r in json.load(open(D/'review.json')):check(r.get('record',r))
 for level,templates in g.TEMPLATES.items():
  for template in templates:
   bad={'a':1,'b':1,'c':4}
   if level=='moderate':bad['point']=[1,0,1] if template=='evaluated_exp_trig' else [1,1,1]
   try:g.generate(level,template=template,parameters=bad)
   except ValueError:pass
   else:raise AssertionError('Out-of-scope coefficients admitted')
 (R/'qa/17592186133889-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
