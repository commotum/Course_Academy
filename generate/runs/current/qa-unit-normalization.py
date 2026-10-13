"""Parent reads actual abstract-vector magnitudes/directions and whole banks."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=P.parents[2]/f'generate/scratch/{K}';summed=K==17592186096815
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_unit_scalar',P/'vector-math-parser.py');g=module('root_unit_gen',D.with_suffix('.py'));U,V=p.u,p.v
C=dict(records=0,actual_magnitude_tasks=0,choices=0,whole_method_banks=0,evidence_banks=0,solution_equalities=0,source_prompts=0,source_values=0,source_banks=0,raw_missing_assessments=0)
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def check(r):
 q=r['question'];meta=r['generation'];profile=meta.get('profile',meta.get('bank_profile'));prompt=q[':question/problem'];opaque=meta['evidence_only'];assert meta['eligible_for_learning']==(not opaque)
 if summed:
  dirs={'horizontally to the right':(1,0),'horizontally to the left':(-1,0),'vertically up':(0,1),'vertically down':(0,-1),'due north-east':(1,1),'due south-east':(1,-1),'due north-west':(-1,1),'due south-west':(-1,-1)};rows=[];magnitudes=[]
  for label in ('a','b'):
   m=re.search(r'vector \$'+label+r'\$ is directed (.*?) and (?:has magnitude \$(\d+)\$|\$\\mid '+label+r'\|=\s*(\d+)\$)',prompt);assert m;magnitude=s.Integer(m[2] or m[3]);magnitudes.append(magnitude);unit=s.Matrix(dirs[m[1]]);unit/=s.sqrt(unit.dot(unit));rows.append(magnitude*unit)
  A,B=magnitudes;assert rows[0].dot(rows[1])==0;actual=rows[0]+rows[1];L=s.sqrt(actual.dot(actual));target=(U+V)/L
  def expression(raw):
   raw=raw.strip().rstrip('.,').replace('&','');raw=raw.replace('|a+b|','('+s.latex(L)+')').replace('|a|','('+s.latex(A)+')').replace('|b|','('+s.latex(B)+')');raw=re.sub(r'\\[A-Za-z]+|[a-z]',lambda m:m[0] if m[0].startswith('\\') else {'a':'u','b':'v','u':'w'}.get(m[0],m[0]),raw);value=p.scalar(raw.replace('w','x'));return value.subs(p.x,target)
 else:
  m=re.search(r'The vector \$(.*?)\$ has magnitude \$(.*?)\$',prompt);assert m;vector=m[1];L=p.scalar(m[2]);assert L>1;target=U/L
  if vector.startswith(r'\overrightarrow{'):label=vector[len(r'\overrightarrow{'):-1];reverse=r'\overrightarrow{'+label[::-1]+'}'
  elif vector.endswith('^(→)'):reverse=vector[:-len('^(→)')][::-1]+'^(→)'
  else:reverse=None
  def expression(raw):
   raw=raw.strip().rstrip('.,').replace('&','').replace(r'\dfrac',r'\frac');pat=r'\\mid\s*(?:\\,)?\s*'+re.escape(vector)+r'\s*(?:\\,)?\s*\\mid';raw=re.sub(pat,lambda m:s.latex(L),raw);raw=raw.replace('|'+vector+'|',s.latex(L)).replace(r'\mathbf{u}','x')
   if reverse:raw=raw.replace(reverse,'(-u)')
   raw=re.sub(r'\\[A-Za-z]+|[A-Za-z]',lambda m:'u' if m[0]==vector else m[0],raw) if len(vector)==1 else raw.replace(vector,'u');return p.scalar(raw).subs(p.x,target)
 f=q[':question/answer-fields'][0];vals=[s.expand(expression(a[':answer/value'])) for a in f[':answer-field/choices']];assert len(vals)==5 and len(set(vals))==5
 if summed:
  def qualifies(value):
   actual_value=value.subs({U:rows[0][0],V:rows[1][0]}),value.subs({U:rows[0][1],V:rows[1][1]});w=s.Matrix(actual_value);return s.simplify(w.dot(w)-1)==0 and s.simplify(w[0]*actual[1]-w[1]*actual[0])==0
 else:
  def qualifies(value):
   poly=s.Poly(value,U);return poly.degree()==1 and poly.nth(0)==0 and s.simplify((poly.nth(1)*L)**2-1)==0
 assert sum(qualifies(z) for z in vals)==1
 if f.get(':answer-field/correct'):assert qualifies(next(v for a,v in zip(f[':answer-field/choices'],vals) if a[':answer/id']==f[':answer-field/correct'][1]))
 else:assert opaque and ':question/worked-solution' not in q and ':question/difficulty' not in q;C['raw_missing_assessments']+=1
 if ':question/worked-solution' in q:
  for block in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
   body=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','');prev=None
   for row in body.split(r'\\'):
    parts=row.strip().split('=');assert len(parts)>=2;values=[]
    for i,z in enumerate(parts):
     if not z.replace('&','').strip():assert i==0 and prev is not None;value=prev
     else:value=expression(z)
     values.append(value)
    assert all(s.simplify(z-values[0])==0 for z in values[1:]),(row,values,prompt);prev=values[-1];C['solution_equalities']+=len(values)-1
 if opaque:C['evidence_banks']+=1
 else:
  if summed:expected=[(U+V)/z for z in (L,A+B,A*A+B*B,A,B)]
  elif profile=='normalization':expected=[L*U,1/L,U/L**2,U,U/L]
  else:expected=[U,-U,L*U,-L*U,U/L]
  assert set(vals)=={s.expand(z) for z in expected};C['whole_method_banks']+=1
 C['records']+=1;C['actual_magnitude_tasks']+=1;C['choices']+=5;return q
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];assert ':question/worked-solution' not in q and ':question/difficulty' not in q and ':answer-field/correct' not in q[':question/answer-fields'][0];of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_prompts']+=1;C['source_values']+=5;C['source_banks']+=1
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
if not summed:
 for level,domain in g.PARAMETER_DOMAINS.items():
  for parameters in domain:
   for template in g.TEMPLATES:
    for profile in ('normalization','direction_errors'):check(g.generate(level,template=template,parameters=parameters,profile=profile))
else:
 for level in ('easy','moderate','hard'):
  for seed in range(30):check(g.generate(level,seed+96815))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
