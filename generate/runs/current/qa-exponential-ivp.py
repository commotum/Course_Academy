"""Independent root readback of printed ODEs, IVP conditions and every solution stage."""
import importlib.util,json,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186229165;D=P.parents[2]/f'generate/scratch/{K}'
def module(n,path):
 sp=importlib.util.spec_from_file_location(n,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_ivp_scalar',P/'ode-scalar-parser.py');g=module('root_ivp_generator',D.with_suffix('.py'));x,A,alpha,beta=p.x,p.z,p.u,p.v
C=dict(records=0,actual_odes=0,initial_conditions=0,complementary_models=0,unique_ivps=0,answer_values=0,exact_stages=0,formal_derivative_rows=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_assessments=0)
def expr(raw,ctx=None):
 ctx=ctx or {};raw=raw.strip().rstrip('.,').replace(r'\alpha','u').replace(r'\beta','v')
 for name,token in (('c','k'),('p','j')):
  if name in ctx:raw=raw.replace('{y}_{'+name+'}^{′}','('+s.latex(s.diff(ctx[name],x))+')')
  raw=raw.replace('{y}_{'+name+'}(x)',token).replace('y_{'+name+'}(x)',token).replace('{y}_{'+name+'}',token).replace('y_{'+name+'}',token)
 if 'y' in ctx:raw=raw.replace('y(0)','('+s.latex(ctx['y'].subs(x,0))+')')
 raw=raw.replace('{y}^{′}','i').replace('y^{′}','i').replace('y(x)','y');raw=re.sub(r'\\[A-Za-z]+|A',lambda m:'z' if m[0]=='A' else m[0],raw)
 while ')^{′}' in raw:
  end=raw.index(')^{′}');start=end-1;depth=1
  while depth:
   if raw[start]==')':depth+=1
   elif raw[start]=='(':depth-=1
   start-=1
  start+=1;v=s.diff(expr(raw[start+1:end],ctx),x);raw=raw[:start]+'('+s.latex(v)+')'+raw[end+len(')^{′}'):]
 v=p.scalar(raw);sub={}
 for name,token in (('c',p.k),('p',p.j),('y',p.y)):
  if name in ctx:sub[token]=ctx[name]
 if 'y' in ctx:sub[p.i]=s.diff(ctx['y'],x)
 return v.subs(sub,simultaneous=True)
def same(a,b):assert s.expand(a-b)==0 or s.simplify(a-b)==0,(a,b)
def check(r):
 q=r['question'];prompt=q[':question/problem'];maths=[a or b for a,b in re.findall(r'\$\$\s*(.*?)\s*\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S)]
 ode,condition=maths[0].split(',',1);condition=condition.replace(r'\,','').strip().rstrip('.')
 assert condition.startswith('y(0)');initial=expr(condition.split('=',1)[1]);assert initial.is_Integer
 lhs,rhs=ode.split('=',1);left,force=expr(lhs),expr(rhs);h=-left.coeff(p.y);assert left==p.i-h*p.y and h.is_Integer and 1<=abs(h)<=6
 repeat=maths[1].rstrip('.');l2,r2=repeat.split('=',1);same(expr(l2),left);same(expr(r2),force)
 yc=expr(next(z for z in maths if 'y}_{c}' in z or 'y_{c}' in z).split('=',1)[1].rstrip(','));same(yc,A*s.exp(h*x))
 terms=list(force.atoms(s.exp));rates=[e.args[0]/x for e in terms];cs=[s.expand(force).coeff(e) for e in terms];assert all(k.is_Integer and 1<=abs(k)<=6 for k in rates) and all(c.is_Integer and 1<=abs(c)<=15 for c in cs);same(force,sum(c*e for c,e in zip(cs,terms)))
 particular=sum(c*x*e if k==h else c*e/(k-h) for c,k,e in zip(cs,rates,terms));general=yc+particular;A0=initial-particular.subs(x,0);expected=general.subs(A,A0);same(s.diff(expected,x)-h*expected,force);same(expected.subs(x,0),initial)
 C['actual_odes']+=1;C['initial_conditions']+=1;C['complementary_models']+=1;f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/blank' and '{{'+f[':answer-field/key']+'}}' in prompt
 if ':answer-field/choices' not in f:
  assert ':answer-field/correct' not in f and ':question/worked-solution' not in q and ':question/difficulty' not in q;C['raw_missing_assessments']+=1;C['records']+=1;return q
 level=q[':question/difficulty'].split('/')[-1];assert len(terms)==(2 if level=='hard' else 1);assert abs(initial)<=(8 if level=='hard' else 10)
 if level=='easy':assert h not in rates
 if level=='moderate':assert rates==[h]
 if level=='hard':assert all(abs(c)<=12 for c in cs)
 for option in f[':answer-field/choices']:
  v=expr(option[':answer/value']);assert v.free_symbols<= {x};same(v,expected);same(s.diff(v,x)-h*v,force);same(v.subs(x,0),initial);C['answer_values']+=1
 assert f[':answer-field/correct'][1] in [z[':answer/id'] for z in f[':answer-field/choices']];C['unique_ivps']+=1
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==(12 if level=='hard' else 10)
 trial=expr(blocks[2].split('=',1)[1]);coefficients=s.solve([s.expand(s.diff(trial,x)-h*trial-force).coeff(e) for e in terms],(alpha,beta)[:len(terms)]);assert isinstance(coefficients,dict);same(trial.subs(coefficients),particular)
 # Formal derivative rows must be true with arbitrary trial coefficients; later
 # equations solve those coefficients. A stays arbitrary until the initial rows.
 context=dict(c=yc,p=trial,y=general)
 for bi,block in enumerate(blocks):
  rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').split(r'\\');previous=None
  for row in rows:
   for segment in row.strip().rstrip('.,').split(r',\qquad '):
    vals=[]
    for index,side in enumerate(segment.split('=')):
     if not side.strip():assert index==0 and previous is not None;v=previous
     else:v=expr(side,context)
     vals.append(v)
    assert len(vals)>1
    for v in vals[1:]:
     delta=v-vals[0]
     if bi!=3:delta=delta.subs(coefficients)
     if bi>=len(blocks)-2:delta=delta.subs(A,A0)
     same(delta,0)
    previous=vals[-1];C['exact_stages']+=len(vals)-1
    if bi==3:C['formal_derivative_rows']+=1
 explicit_general=expr(blocks[-3].split('=',1)[1]);same(explicit_general,general);same(s.diff(explicit_general,A),s.exp(h*x));final=expr(blocks[-1].split('=',1)[1]);same(final,expected)
 if len(terms)==1:same(expr(re.search(r'right-hand side is \$(.*?)\$',sol)[1]),force)
 C['records']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old)
 of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f.get(':answer-field/choices',[]))==sorted(z[':answer/value'] for z in of.get(':answer-field/choices',[]));C['source_values']+=len(of.get(':answer-field/choices',[]))
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1;C['source_banks']+=1
for item in json.loads((D/'review.json').read_text()):check(item['record'])
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for template,level in g.TEMPLATES.items():
 for seed in range(40):check(g.generate(level,seed+350,template=template))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
