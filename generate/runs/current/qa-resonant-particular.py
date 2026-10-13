"""Root prompt-first resonance derivation including formal derivative operators."""
import importlib.util,re,json,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=17592186229163;D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
p=module('root_resonance_math',P/'ode-scalar-parser.py');g=module('root_resonance_gen',D.with_suffix('.py'));x,alpha,beta=p.x,p.u,p.v
C=dict(records=0,answers=0,source_prompts=0,source_solutions=0,source_banks=0,source_values=0,source_keys=0,actual_odes=0,complementary_models=0,trials=0,formal_derivative_stages=0,substitution_sides=0,coefficient_equations=0,final_particulars=0)
def expr(raw):
 raw=raw.strip().rstrip('.,').replace(r'\alpha','u').replace(r'\beta','v').replace('{y}^{′}','i')
 raw=raw.replace('{y}_{p}(x)','j').replace('{y}_{p}','j').replace('{y}_{c}(x)','j');raw=re.sub(r'\\[A-Za-z]+|A',lambda m:'z' if m[0]=='A' else m[0],raw)
 # Interpret each ACTUAL formal derivative argument before elementary parsing.
 while ')^{′}' in raw:
  end=raw.index(')^{′}');start=end-1;depth=1
  while depth:
   if raw[start]==')':depth+=1
   elif raw[start]=='(':depth-=1
   start-=1
  start+=1;value=s.diff(expr(raw[start+1:end]),x);raw=raw[:start]+'('+s.latex(value)+')'+raw[end+len(')^{′}'):]
 return p.scalar(raw)
def same(a,b):assert s.expand(a-b)==0 or s.simplify(a-b)==0,(a,b)
def check(r):
 q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];level=q[':question/difficulty'].split('/')[-1];raw=r['generation']['bank_profile']!='normal'
 ode=re.findall(r'\$\$\s*(.*?)\s*\$\$',prompt,re.S)[0];lhs,rhs=ode.split('=',1);left,force=expr(lhs),expr(rhs);c=left.coeff(p.y);assert left==p.i+c*p.y and c!=0;rate=-c
 terms=list(force.atoms(s.exp));assert len(terms)==(1 if level=='easy' else 2);rates=[e.args[0]/x for e in terms];assert all(v.is_Integer and v!=0 for v in rates);forcing={r:s.expand(force).coeff(e) for r,e in zip(rates,terms)};same(force,sum(forcing[r]*s.exp(r*x) for r in rates));assert rate in forcing and all(v!=0 and v.is_Integer for v in forcing.values());av=forcing[rate]
 if len(terms)==2:sv=next(v for v in rates if v!=rate);bv=forcing[sv];bval=bv/(sv-rate)
 if not raw:
  if level=='easy':assert 2<=abs(rate)<=6 and 2<=av<=12
  elif level=='moderate':assert -6<=rate<=-2 and 2<=av<=30 and 1<=sv<=3 and 1<=abs(bv)<=12
  else:assert 1<=abs(rate)<=6 and 1<=abs(sv)<=6 and 2<=abs(av)<=12 and 1<=abs(bv)<=12 and 2<=s.denom(bval)<=7 and abs(s.numer(bval))<=12 and (av<0 or bv<0) and (rate>0 or sv<0)
 complement=expr(re.search(r'complementary solution \$(.*?)\$',prompt)[1].split('=',1)[1]);same(s.diff(complement,x)+c*complement,0);C['complementary_models']+=1;C['actual_odes']+=1
 expected=av*x*s.exp(rate*x)+(bval*s.exp(sv*x) if len(terms)==2 else 0);same(s.diff(expected,x)+c*expected,force)
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/blank' and '{{'+f[':answer-field/key']+'}}' in prompt
 for z in f[':answer-field/choices']:same(expr(z[':answer/value']),expected);C['answers']+=1
 assert f[':answer-field/correct'][1] in [z[':answer/id'] for z in f[':answer-field/choices']]
 if not raw:assert len(f[':answer-field/choices'])==1 and 'no added complementary-solution term' in prompt
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==(4 if len(terms)==1 else 6)
 trial=expr(blocks[0].split('=',1)[1]);same(trial,alpha*x*s.exp(rate*x)+(beta*s.exp(sv*x) if len(terms)==2 else 0));C['trials']+=1
 drows=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(drows)==4
 for row in drows:
  right=row.replace('&','').split('=',1)[1];same(expr(right),s.diff(trial,x));C['formal_derivative_stages']+=1
 operator=s.diff(trial,x)+c*trial;rows=blocks[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==(4 if len(terms)==1 else 3)
 for row in rows[:3]:
  lhs,rhs=row.replace('&','').split('=',1);same(expr(lhs),operator);same(expr(rhs),force);C['substitution_sides']+=2
 if len(terms)==1:
  lhs,rhs=rows[3].replace('&','').split('=',1);same(expr(lhs),alpha);same(expr(rhs),av);C['coefficient_equations']+=1
 else:
  for block,wanted in zip(blocks[3:5],(((alpha,av),((sv-rate)*beta,bv)),((alpha,av),(beta,bval)))):
   parts=block.rstrip('.,').split(r'\,\text{and}\,');assert len(parts)==2
   for part,(left,right) in zip(parts,wanted):
    lhs,rhs=part.split('=',1);same(expr(lhs),left);same(expr(rhs),right);C['coefficient_equations']+=1
 same(expr(blocks[-1].split('=',1)[1]),expected);C['final_particulars']+=1
 same(expr(re.search(r'right-hand side is \$(.*?)\$',sol)[1]),force);C['records']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'] and q[':question/worked-solution']==old[':question/worked-solution'];C['source_prompts']+=1;C['source_solutions']+=1
 of,f=old[':question/answer-fields'][0],q[':question/answer-fields'][0];assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(of[':answer-field/choices']);assert of[':answer-field/correct'][':answer/value']==next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);C['source_keys']+=1
for item in json.loads((D/'review.json').read_text()):check(item['record'])
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for seed in range(50):check(g.generate(level,seed+901))
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
