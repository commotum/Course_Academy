"""Root evaluates printed general-family ODE stages and formal derivatives."""
import importlib.util,re,json
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186229164;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_general_parser',P/'ode-scalar-parser.py');g=module('root_general_generator',D.with_suffix('.py'));x,A,alpha,beta=p.x,p.z,p.u,p.v
C=dict(records=0,actual_odes=0,complementary_models=0,complete_families=0,answer_values=0,exact_stages=0,formal_derivative_rows=0,source_prompts=0,source_solutions=0,source_values=0,source_banks=0,source_keys=0,raw_missing_fields=0)
def expr(raw,ctx=None):
 ctx=ctx or {};raw=raw.strip().rstrip('.,').replace(r'\alpha','u').replace(r'\beta','v')
 for name,token in (('c','k'),('p','j')):
  if name in ctx:
   raw=raw.replace('{y}_{'+name+'}^{′}','('+s.latex(s.diff(ctx[name],x))+')')
  raw=raw.replace('{y}_{'+name+'}(x)',token).replace('y_{'+name+'}(x)',token).replace('{y}_{'+name+'}',token).replace('y_{'+name+'}',token)
 raw=raw.replace('{y}^{′}','i').replace('y^{′}','i').replace('y(x)','y');raw=re.sub(r'\\[A-Za-z]+|A',lambda m:'z' if m[0]=='A' else m[0],raw)
 while ')^{′}' in raw:
  end=raw.index(')^{′}');start=end-1;depth=1
  while depth:
   if raw[start]==')':depth+=1
   elif raw[start]=='(':depth-=1
   start-=1
  start+=1;value=s.diff(expr(raw[start+1:end],ctx),x);raw=raw[:start]+'('+s.latex(value)+')'+raw[end+len(')^{′}'):]
 value=p.scalar(raw);sub={}
 for name,token in (('c',p.k),('p',p.j),('y',p.y)):
  if name in ctx:sub[token]=ctx[name]
 if 'y' in ctx:sub[p.i]=s.diff(ctx['y'],x)
 return value.subs(sub,simultaneous=True)
def same(a,b):assert s.expand(a-b)==0 or s.simplify(a-b)==0,(a,b)
def family(v,w,rate):
 same(s.diff(v,x)-rate*v,s.diff(w,x)-rate*w);assert s.diff(v,A,2)==0 and s.diff(w,A,2)==0
 ratio=s.simplify(s.diff(v,A)/s.diff(w,A));shift=s.simplify((v.subs(A,0)-w.subs(A,0))/s.exp(rate*x));assert not ratio.free_symbols and ratio!=0 and not shift.free_symbols
def check(r):
 q=r['question'];prompt=q[':question/problem'];spans=re.findall(r'\$\$\s*(.*?)\s*\$\$|(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S);maths=[a or b for a,b in spans];lhs,rhs=maths[0].split('=',1);left,force=expr(lhs),expr(rhs);rate=-left.coeff(p.y);assert left==p.i-rate*p.y and rate.is_Integer and rate!=0
 yc=expr(next(z for z in maths if 'y}_{c}' in z or 'y_{c}' in z).split('=',1)[1]);same(s.diff(yc,x)-rate*yc,0);assert s.diff(yc,A)==s.exp(rate*x)
 terms=list(force.atoms(s.exp));rates=[e.args[0]/x for e in terms];cs=[s.expand(force).coeff(e) for e in terms];assert all(v.is_Integer and v!=0 for v in rates) and all(c.is_Integer and c!=0 for c in cs);same(force,sum(c*e for c,e in zip(cs,terms)))
 particular=sum(c*x*e if k==rate else c*e/(k-rate) for c,k,e in zip(cs,rates,terms));expected=yc+particular;same(s.diff(expected,x)-rate*expected,force);C['actual_odes']+=1;C['complementary_models']+=1
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/blank' and '{{'+f[':answer-field/key']+'}}' in prompt
 if ':answer-field/choices' not in f:
  assert ':answer-field/correct' not in f and ':question/worked-solution' not in q and ':question/difficulty' not in q;C['raw_missing_fields']+=1;C['records']+=1;return q
 level=q[':question/difficulty'].split('/')[-1];assert len(terms)==(2 if level=='hard' else 1);assert (rate in rates)==(level!='easy')
 for option in f[':answer-field/choices']:
  value=expr(option[':answer/value']);family(value,expected,rate);same(s.diff(value,A),s.exp(rate*x));C['answer_values']+=1
 assert f[':answer-field/correct'][1] in [z[':answer/id'] for z in f[':answer-field/choices']];C['complete_families']+=1
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==(10 if level=='hard' else 8)
 trial=expr(blocks[2].split('=',1)[1]);wanted=alpha*x*s.exp(rate*x) if level!='easy' else alpha*terms[0]
 if level=='hard':other=next(e for e,k in zip(terms,rates) if k!=rate);wanted+=beta*other
 same(trial,wanted)
 # Determine coefficients from actual trial response and forcing, not metadata.
 operator=s.diff(trial,x)-rate*trial;coefficients=s.solve([s.expand(operator-force).coeff(e) for e in terms],(alpha,beta)[:len(terms)]);assert isinstance(coefficients,dict);same(trial.subs(coefficients),particular)
 context=dict(c=yc,p=trial,y=expected)
 for bi,block in enumerate(blocks):
  rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','').split(r'\\');previous=None
  for row in rows:
   for segment in row.strip().rstrip('.,').split(r'\quad \text{and} \quad'):
    vals=[]
    for index,side in enumerate(segment.split('=')):
     if not side.strip():assert index==0 and previous is not None;value=previous
     else:value=expr(side,context)
     vals.append(value)
    assert len(vals)>1
    for value in vals[1:]:same(value-vals[0],0) if bi==3 else same((value-vals[0]).subs(coefficients),0)
    previous=vals[-1];C['exact_stages']+=len(vals)-1
    if bi==3:C['formal_derivative_rows']+=1
 same(expr(re.search(r'right-hand side is \$(.*?)\$',sol)[1]),force)
 # The closing general-family sum is a full family, not just a particular.
 final=expr(blocks[-1].split('=',1)[1]);family(final,expected,rate);same(s.diff(final,A),s.exp(rate*x))
 if not r['generation']['bank_profile'].startswith('raw:'):assert 'Write the arbitrary constant term as' in prompt
 C['records']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_prompts']+=1;C['source_solutions']+=int(':question/worked-solution' in old)
 of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f.get(':answer-field/choices',[]))==sorted(z[':answer/value'] for z in of.get(':answer-field/choices',[]));C['source_values']+=len(of.get(':answer-field/choices',[]))
 if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1;C['source_banks']+=1
for item in json.loads((D/'review.json').read_text()):check(item['record'])
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(50):check(g.generate(level,seed+80))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
