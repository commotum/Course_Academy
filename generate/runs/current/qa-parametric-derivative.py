"""Root actual coordinate derivatives, all family stages, banks and identities."""
import importlib.util,json,re,hashlib,itertools,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186083240;D=R.parents[2]/f'generate/scratch/{K}'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','parent_parametric');t=p.t
def math(raw):return p.scalar(raw.replace(r'\theta','t').strip().removesuffix(r'\,.').removesuffix(r'\,').rstrip('.,'))
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0
def blocks(text):return re.findall(r'\$\$\s*(.*?)\s*\$\$',text,re.S)
def resolve(raw):
 return re.sub(r'\\frac\{d\}\{dt\}\\left\((.*?)\\right\)',lambda m:'('+s.latex(s.diff(math(m[1]),t))+')',raw)
def curve(prompt):
 b=blocks(prompt)[0];separator=r'\quad ' if r'\quad' in b else r'\,';coords=b.split(','+separator);assert len(coords)==3;assert coords[0].startswith('x=') and coords[1].startswith('y=');return math(coords[0][2:]),math(coords[1][2:]),coords[2]
C={key:0 for key in ('records','actual_coordinates','coordinate_derivatives','formal_rule_operands','quotient_stages','evaluated_stages','choices','complete_method_banks','source_operative_sequences','common_amplitude_identity_checks','derivative_exclusions','plot_geometries')}
def check(rec,old):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];family=rec['generation']['template'];X,Y,domain=curve(prompt);dx,dy=s.diff(X,t),s.diff(Y,t);ratio=dy/dx;point=re.search(r'where \$t=(.*?)\.\$',prompt);point=math(point[1]) if point else None;answer=s.simplify(ratio.subs(t,point) if point is not None else ratio);C['actual_coordinates']+=2
 B=blocks(sol);assert len(B)>=3;assert r'\frac{dy}{dx}' in B[0] and (r'\frac{y\'(t)}{x\'(t)}'.replace("\\'","'") in B[0] or '{y}^{′}' in B[0])
 if old:
  original=blocks(old[':question/worked-solution']);assert len(B)==len(original)
  prose=lambda text:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$.*?\$','',text,flags=re.S)).strip();assert prose(sol)==prose(old[':question/worked-solution'])
  for current,source in zip(B[2:],original[2:]):assert current.count(' & =')==source.count(' & =') and current.count('=')==source.count('=')
  C['source_operative_sequences']+=1
 for b in B[1:]:
  if "x'(t)=" in b or '{x}^{′}' in b:
   fields=re.split(r',\\(?:quad |,).*?=',b,maxsplit=1);assert len(fields)==2;actual=[fields[0].split('=',1)[1],fields[1]]
   for text,derived in zip(actual,(dx,dy)):
    operators=re.findall(r'\\frac\{d\}\{dt\}\\left\((.*?)\\right\)',text)
    for operand in operators:assert math(operand).has(t);s.diff(math(operand),t);C['formal_rule_operands']+=1
    assert equal(math(resolve(text)),derived);C['coordinate_derivatives']+=1
  elif r'\begin{aligned}' in b:
   rows=b.split(' & =')[1:]
   assert point is not None
   for row in rows:assert equal(math(row.split(chr(92)*2)[0].removesuffix(r'\end{aligned}')),answer);C['evaluated_stages']+=1
  else:
   for row in b.split('=')[1:]:assert equal(math(row),ratio);C['quotient_stages']+=1
 if family=='product_pair':
  zeros=s.solve(dx,t);assert len(zeros)==1;excluded=math(re.search(r'for \$t\\ne (.*?)\.\$',prompt)[1]);assert excluded==zeros[0] and dy.subs(t,excluded)!=0 and ('defined for $t'+r'\ne '+s.latex(excluded)+'.$') in sol;assert rec['generation']['derivative_domain']['excluded_parameters']==[str(excluded)];C['derivative_exclusions']+=1
 elif family=='quotient_pair':assert domain.strip().rstrip(',')==r't>0' and not s.solve(dx,t)
 for f in q[':question/answer-fields']:
  choices=f[':answer-field/choices'];values=[math(a[':answer/value'].split('=',1)[-1]) for a in choices];assert all(not equal(a,b) for a,b in itertools.combinations(values,2));assert [a[':answer/id'] for a,v in zip(choices,values) if equal(v,answer)]==[f[':answer-field/correct'][1]]
  ev=lambda expr:s.simplify(expr.subs(t,point) if point is not None else expr)
  if f[':answer-field/type'].endswith('/radio'):
   if family=='line_quad' and point==0:wanted=[answer,ev(s.diff(Y,t,2)/dx),ev(dx/s.diff(Y,t,2)),ev(X/dx),ev(s.diff(Y,t,2))]
   elif family=='product_sin':wanted=[answer,ev(-dy/dx),ev(dx/dy),ev(-dx/dy),ev(Y/X)]
   elif family=='exp_poly':wanted=[answer,ev(dx/dy),ev(Y/X),ev(dx*dy),ev(s.diff(Y,t,2)/dx)]
   else:wanted=[answer,ev(dx/dy),ev(Y/X),ev(dx*dy),ev(dy/X)]
   assert len(values)==5 and all(sum(equal(v,w) for w in wanted)==1 for v in values);C['complete_method_banks']+=1
  else:assert len(values)==1 and '{{'+f[':answer-field/key']+'}}' in prompt
  C['choices']+=len(values)
 for asset in re.findall(r'!\[\]\((.*?)\)',prompt):
  path=Path(asset);side=json.loads(path.with_suffix('.json').read_text());assert path.stat().st_size>1000
  # Sidecar shapes are independently derived from actual printed coordinates.
  assert equal(s.sympify(side['x'],locals={'t':t}),X) and equal(s.sympify(side['y'],locals={'t':t}),Y);C['plot_geometries']+=1
 C['records']+=1
if __name__=='__main__':
 g=load(D.with_suffix('.py'),'parent_parametric_generator');frozen=json.load(open(R/f'sources/{K}.json'));assert json.load(open(D/'source.json'))==frozen;originals={str(q[':db/id']):q for q in frozen['record'][':knowledge-point/questions']};S=dict(prompts=0,solutions=0,fields=0,values=0,refs=0,missing_refs=0)
 for case in json.load(open(D/'source-cases.json')):
  o=originals[str(case['source_id'])];q=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])['question'];assert set(q)==set(o)-{':db/id'} and q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'];S['prompts']+=1;S['solutions']+=1
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);S['fields']+=1;S['values']+=len(of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];S['refs']+=1
   else:S['missing_refs']+=1
 records=json.load(open(R/f'qa/{K}-sampled.json'))
 for family,c in g.TEMPLATES.items():records.extend(g.generate(c['level'],seed=seed,template=family) for seed in (631,917))
 for rec in records:check(rec,originals.get(str(g.TEMPLATES[rec['generation']['template']].get('source_id'))))
 for family,c in g.TEMPLATES.items():
  pairs=[(dict(a=1,b=2,c=1,d=3),dict(a=2,b=2,c=2,d=3))] if c['level']=='hard' else [(dict(r=str(a),s=str(b)),dict(r=str(2*a),s=str(2*b))) for a,b in itertools.product((s.Rational(1,2),s.Integer(1),s.Rational(3,2),s.Integer(2),s.Integer(3)),repeat=2)]
  for oneparams,twoparams in pairs:
   try:one=g.generate(c['level'],template=family,parameters=oneparams);two=g.generate(c['level'],template=family,parameters=twoparams)
   except ValueError:continue
   assert one['generation']['mathematical_fingerprint']==two['generation']['mathematical_fingerprint'] and one['question'][':question/id']!=two['question'][':question/id'];C['common_amplitude_identity_checks']+=1;break
  else:raise AssertionError(('no eligible amplitude pair',family))
 out=dict(status='passed',source=S,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
