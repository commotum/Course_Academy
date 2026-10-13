"""Parent reads exponential ODE forcing, trial, derivative and all scalar stages."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;K=int(sys.argv[1]);D=P.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('root_exponential_parser',P/'ode-scalar-parser.py');g=module('root_particular'+str(K),D.with_suffix('.py'));x=p.x;alpha,beta=p.u,p.v;A=p.z;der=p.i;y=p.y;Y=p.j
C=dict(records=0,answers=0,actual_odes=0,complementary_solutions=0,trials=0,derivatives=0,substitution_sides=0,coefficient_equations=0,final_solutions=0,prose_forcing=0,source_prompts=0,source_full_solutions=0,source_values=0,source_keys=0,missing_raw_banks=0)
def expr(raw):
 raw=raw.strip().rstrip('.,').replace(r'\alpha','u').replace(r'\beta','v')
 raw=raw.replace(r'\frac{\text{d}y}{\text{d}x}','i').replace(r'\frac{dy}{dx}','i').replace(r'\frac{\text{d}{y}_{p}}{\text{d}x}','i')
 raw=raw.replace('{y}_{p}(x)','j').replace('{y}_{p}','j').replace('y_{p}(x)','j').replace('y_{p}','j').replace('{y}_{c}(x)','j').replace('y_{c}(x)','j')
 raw=re.sub(r'\\[A-Za-z]+|A',lambda m:'z' if m[0]=='A' else m[0],raw)
 return p.scalar(raw)
def same(a,b):assert s.expand(a-b)==0 or s.simplify(a-b)==0,(a,b)
def check(r):
 q=r['question'];prompt=q[':question/problem'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',prompt,re.S)
 ode=blocks[0] if blocks else re.search(r'\$(.*?)\$',prompt,re.S)[1];lhs,rhs=ode.split('=');left,force=expr(lhs),expr(rhs);a,b=left.coeff(der),left.coeff(y);assert left==a*der+b*y and a>0 and b!=0
 terms=list(force.atoms(s.exp));assert len(terms) in (1,2);ks=[e.args[0]/x for e in terms];cs=[s.expand(force).coeff(e) for e in terms];assert all(not k.has(x) and k!=0 and a*k+b!=0 for k in ks) and all(c!=0 for c in cs);same(force,sum(c*e for c,e in zip(cs,terms)))
 if q.get(':question/difficulty')==':question.difficulty/hard' and not r['generation'].get('raw_evidence'):assert a/s.gcd_list([a,b,*cs])>=4
 correct=sum(c*e/(a*k+b) for c,k,e in zip(cs,ks,terms));same(a*s.diff(correct,x)+b*correct,force)
 complement=expr(re.search(r'complementary solution \$(.*?)\$',prompt)[1].split('=',1)[1]);same(a*s.diff(complement,x)+b*complement,0);C['complementary_solutions']+=1;C['actual_odes']+=1
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/blank' and '{{'+f[':answer-field/key']+'}}' in prompt
 if ':answer-field/choices' not in f:
  assert ':answer-field/correct' not in f and ':question/worked-solution' not in q and ':question/difficulty' not in q;C['missing_raw_banks']+=1;C['records']+=1;return q
 assert len(f[':answer-field/choices'])==1
 for option in f[':answer-field/choices']:same(expr(option[':answer/value']),correct);assert option[':answer/id']==f[':answer-field/correct'][1];C['answers']+=1
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==(4 if len(terms)==1 else 6)
 trial=expr(blocks[0].split('=',1)[1]);dt=expr(blocks[1].split('=',1)[1]);same(dt,s.diff(trial,x));assert trial.free_symbols==({x,alpha} if len(terms)==1 else {x,alpha,beta});C['trials']+=1;C['derivatives']+=1
 # Solve unknown trial coefficients from the ACTUAL operator and forcing.
 operator=a*dt+b*trial;equations=[s.expand(operator-force).coeff(e) for e in terms];solution=s.solve(equations,(alpha,beta)[:len(terms)]);assert isinstance(solution,dict);same(trial.subs(solution),correct)
 rows=blocks[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==(4 if len(terms)==1 else 3)
 for row in rows[:3]:
  lhs,rhs=row.replace('&','').split('=',1);same(expr(lhs),operator);same(expr(rhs),force);C['substitution_sides']+=2
 if len(terms)==1:
  lhs,rhs=rows[3].replace('&','').split('=',1);same(expr(lhs),alpha);same(expr(rhs),solution[alpha]);C['coefficient_equations']+=1
 else:
  for block in blocks[3:5]:
   parts=re.split(r',\\,\\,|,\\,|\\,\\text\{and\}\\,',block.rstrip('.,'));assert len(parts)==2
   for part in parts:
    lhs,rhs=part.split('=',1);same(expr(lhs).subs(solution),expr(rhs));C['coefficient_equations']+=1
 same(expr(blocks[-1].split('=',1)[1]),correct);C['final_solutions']+=1
 same(expr(re.search(r'right-hand side is \$(.*?)\$',sol)[1]),force);C['prose_forcing']+=1
 if not r['generation'].get('raw_evidence'):assert 'linear combination of the displayed forcing exponentials' in prompt
 C['records']+=1;return q
sources={q[':question/math-academy-id']:q for q in json.loads((P/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for case in json.loads((D/'source-cases.json').read_text()):
 q=check(g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']));old=sources[case['source_id']];assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 assert q.get(':question/worked-solution')==old.get(':question/worked-solution');C['source_full_solutions']+=int(':question/worked-solution' in old)
 for of,f in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  assert [z[':answer/value'] for z in f.get(':answer-field/choices',[])]==[z[':answer/value'] for z in of.get(':answer-field/choices',[])];C['source_values']+=len(of.get(':answer-field/choices',[]))
  if of.get(':answer-field/correct'):assert of[':answer-field/correct'][':answer/value']==f[':answer-field/choices'][0][':answer/value'];C['source_keys']+=1
for group in json.loads((D/'review.json').read_text()).values():
 for item in group:check(item)
for template,level in g.TEMPLATES.items():
 for seed in range(36):check(g.generate(level,seed+71,template=template))
for r in json.loads((P/'qa'/f'{K}-sampled.json').read_text()):check(r)
C['database_writes']=0;(P/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
