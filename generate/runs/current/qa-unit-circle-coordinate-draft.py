"""Root reads actual given coordinates, seven identity stages and full scalar/equation banks."""
import hashlib,importlib.util,itertools,json,math,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186110754;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
G=mod('root_circle_coord_generator',D.with_suffix('.py'));P=mod('root_circle_coord_scalar',R/'ode-scalar-parser.py');F=mod('root_circle_coord_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
C=dict(records=0,actual_givens=0,operative_identity_rows=0,substitution_values=0,positive_conclusions=0,values=0,pairs=0,whole_method_banks=0,level_guards=0,prose_masks=0)
def scalar(t):return P.scalar(t.strip().rstrip('.,'))
def choice(v,target):
 if '=' in v:
  lhs,rhs=v.split('=');assert lhs.strip()==target;return scalar(rhs)
 return scalar(v)
def mask(t):
 t=re.sub(r'\$\$.*?\$\$','@DISPLAY@',t,flags=re.S);return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',t)).strip()
def check(r,raw=False):
 q,m=r['question'],r['generation'];prompt=q[':question/problem'];assert 'first quadrant' in prompt and 'unit circle' in prompt
 match=re.search(r'\$(x|y)\$-coordinate of \$A\$ is \$(.*?)\$',prompt);assert match;known,given=match.groups();given=scalar(given);target=re.search(r'What is the \$(x|y)',prompt)[1];assert known!=target and 0<given<1;answer=s.sqrt(1-given**2);C['actual_givens']+=1
 if not raw:
  level=q[':question/difficulty'].split('/')[-1];sq=s.factor(given**2);num,den=sq.as_numer_denom();assert num.is_Integer and den.is_Integer and math.isqrt(int(den))**2==den
  d=math.isqrt(int(den));coef,rad=given.as_coeff_Mul();rad=s.simplify(rad**2);othercoef,otherrad=answer.as_coeff_Mul();otherrad=s.simplify(otherrad**2)
  if level=='easy':assert d<=8 and (rad==1 or s.simplify(coef*d)==1) and (s.simplify(othercoef*d)==1 or otherrad==1)
  elif level=='moderate':assert given.is_Rational and not answer.is_Rational and s.simplify(othercoef*d)>1
  else:assert not given.is_Rational and 2<=s.simplify(coef*d)<=4 and rad<=15 and not answer.is_Rational
  C['level_guards']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==2 and blocks[0].strip()==r'{x}^{2}+{y}^{2}=1'
  subst=re.search(r'Substituting \$(x|y)=(.*?)\$ into the above and solving for \$(x|y)\$',sol);assert subst and subst[1]==known and scalar(subst[2])==given and subst[3]==target;C['substitution_values']+=1
  rows=blocks[1].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2);assert len(rows)==7
  env={P.x:given if known=='x' else answer,P.y:given if known=='y' else answer}
  for i,row in enumerate(rows):
   lhs,rhs=row.split('=');lhs=lhs.replace('&','').strip();rhs=rhs.strip();pm=r'\pm' in rhs;rhs=rhs.replace(r'\pm','')
   assert s.simplify(scalar(lhs).subs(env)-scalar(rhs).subs(env))==0,(i,row,given,answer);C['operative_identity_rows']+=1
   assert pm==(i==6)
  # Operative signed-square, evaluated-square, rearrangement and root stages
  # remain explicit; seven repeated final equalities cannot pass these checks.
  assert r'^{2}' in rows[1] and '((' not in rows[1] and r'({\frac' not in rows[1]
  groups=re.findall(r'\{\((.*?)\)\}\^\{2\}',rows[1]);assert len(groups)==1 and scalar(groups[0])==given
  lhs=rows[2].split('=')[0].replace('&','');expr=scalar(lhs);other=P.y if target=='y' else P.x;assert s.simplify(expr-other**2)==given**2
  assert rows[3].split('=')[1].strip().startswith('1-') and scalar(rows[4].split('=')[1])==1-given**2
  assert rows[5].split('=')[1].strip().startswith(r'\sqrt{')
  final=re.search(r'final answer is \$(x|y)=(.*?)\$',sol);assert final and final[1]==target and scalar(final[2])==answer
  assert f'${target}$ must be positive' in sol and 'select the positive answer' in sol;C['positive_conclusions']+=1
  sid=m.get('source_ids',[None])[0] if m.get('source_ids') else 'q-124608';old=originals[sid];assert mask(sol)==mask(old[':question/worked-solution']);C['prose_masks']+=1
 f=q[':question/answer-fields'][0];vals=[choice(a[':answer/value'],target) for a in f[':answer-field/choices']];assert len(vals)==5 and all(v.is_real and v.is_finite for v in vals) and sum(s.simplify(v-answer)==0 for v in vals)==1
 for v,w in itertools.combinations(vals,2):assert s.simplify(v-w)!=0;C['pairs']+=1
 if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if s.simplify(v-answer)==0]==[f[':answer-field/correct'][1]]
 if not raw:
  expected=[answer,-answer,1-given**2,s.sqrt(1-given),s.sqrt(1+given**2)];assert all(sum(s.simplify(v-e)==0 for v in vals)==1 for e in expected);C['whole_method_banks']+=1
 C['values']+=5;C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for level in ('easy','moderate','hard'):
 for template in ('coordinate-value','coordinate-equation'):
  for seed in (38,97):check(G.generate(level,seed,template=template))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile'))),True)
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
