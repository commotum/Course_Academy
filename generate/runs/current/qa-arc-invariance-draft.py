"""Root reads parameterized curves/domains, locus proof and all claimed invariant values."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186162083;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
G=mod('root_invar_generator',D.with_suffix('.py'));P=mod('root_invar_scalar',R/'ode-scalar-parser.py');F=mod('root_invar_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
z=s.Symbol('z',nonnegative=True);C=dict(records=0,actual_curve_components=0,domain_bounds=0,normalized_curve_equalities=0,once_traversed_circle_checks=0,claims=0,choices=0,wrong_pairs=0,verdicts=0,locus_relations=0,locus_bounds=0,integral_conclusions=0,prose_masks=0)
def scalar(t):return P.scalar(t.strip().rstrip('.,').replace('θ','u'))
def vectors(prompt):return [P.vector(v.replace('θ','u')) for v in re.findall(r'⟨[^⟩]+⟩',prompt)]
def bounds(prompt):
 out=[]
 for m in re.finditer(r'0\s*\\le\s*([tuθ])\s*\\le\s*',prompt):
  rest=prompt[m.end():];ends=[rest.find(v) for v in (chr(92)*2,r'\end','$','\n',',','.') if rest.find(v)>=0];end=scalar(rest[:min(ends)] if ends else rest);out.append((P.t if m[1]=='t' else P.u,end))
 return out

def integral_value(token):
 assert 'int' in token and '=' in token;return scalar(token.rsplit('=',1)[-1])
def mask(t):
 t=re.sub(r'\$\$.*?\$\$','@DISPLAY@',t,flags=re.S);return re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','@MATH@',t)).strip()
def check(r,raw=False):
 q,m=r['question'],r['generation'];prompt=q[':question/problem'];vs=vectors(prompt);bs=bounds(prompt);assert len(vs)==2 and len(bs)==2 and all(b>0 for v,b in bs)
 normalized=[]
 for v,(symbol,end) in zip(vs,bs):
  assert v.shape==(2,1) and v.free_symbols<={symbol};normalized.append(v.subs(symbol,end*z));C['actual_curve_components']+=2;C['domain_bounds']+=1
 assert all(s.simplify(s.trigsimp(a-b))==0 for a,b in zip(*normalized));C['normalized_curve_equalities']+=2
 for v,(symbol,end) in zip(vs,bs):
  funcs=v.atoms(s.sin,s.cos)
  if funcs:assert len(funcs)==2 and all(s.simplify(fun.args[0].subs(symbol,end))==(2*s.pi if m['template']=='q-122571' else s.pi) for fun in funcs);C['once_traversed_circle_checks']+=1
 tokens=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S);given=next(integral_value(token) for token in tokens if 'int' in token and '=' in token)
 statements=[]
 for line in prompt.splitlines():
  if re.match(r'^(?:[123]\. |\s*- \*\*(?:I|II|III)\.\*\*)',line):
   token=re.search(r'\$(.*?)\$',line).group(1);value=integral_value(token);statements.append(s.simplify(value-given)==0);C['claims']+=1
 assert len(statements)==3;chosen={name for name,truth in zip(('I','II','III'),statements) if truth}
 for f in q[':question/answer-fields']:
  vals=[a[':answer/value'] for a in f[':answer-field/choices']]
  if f[':answer-field/type'].endswith('checkbox'):
   assert set(vals)=={'true','false'};correct='true' if f[':answer-field/key'] in chosen else 'false'
   assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==correct
  else:
   sets=[set(re.findall(r'\b(?:III|II|I)\b',v)) for v in vals];assert len(sets)==5 and sum(v==chosen for v in sets)==1
   for a,b in itertools.combinations(sets,2):assert a!=b;C['wrong_pairs']+=1
   if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],sets) if v==chosen]==[f[':answer-field/correct'][1]]
  C['choices']+=len(vals)
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];verdicts=re.findall(r'[Ss]tatement (III|II|I) is (true|false)',sol);assert len(verdicts)==3 and all((truth=='true')==(name in chosen) for name,truth in verdicts);C['verdicts']+=3
  final=re.search(r'correct answer is "(.*?)"',sol)[1];assert set(re.findall(r'\b(?:III|II|I)\b',final))==chosen
  for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
   if 'int' in block:
    end=scalar(block.rsplit('=',1)[-1]);assert s.simplify(end-given)==0;C['integral_conclusions']+=1
   elif '=' in block:
    relation=block.split(',',1)[0].strip();lhs,rhs=relation.split('=',1);env={P.x:normalized[0][0],P.y:normalized[0][1]};assert s.simplify(scalar(lhs).subs(env)-scalar(rhs).subs(env))==0;C['locus_relations']+=1
    ranges=re.search(r'0\s*\\le\s*([xy])\s*\\le\s*(.*?)\.?\s*$',block);assert ranges;component=normalized[0][0 if ranges[1]=='x' else 1];assert component.subs(z,0)==0 and s.simplify(component.subs(z,1)-scalar(ranges[2]))==0 and component.diff(z).is_nonnegative;C['locus_bounds']+=1
  radius=re.search(r'radius \$(.*?)\$',sol)
  if radius:assert s.simplify(sum(v*v for v in normalized[0])-scalar(radius[1])**2)==0;C['locus_relations']+=1
  old=originals[m['template']]
  if ':question/worked-solution' in old:assert mask(sol)==mask(old[':question/worked-solution']);C['prose_masks']+=1
 C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for level,templates in G.LEVELS.items():
 for template in templates:
  for seed in (38,94):check(G.generate(level,seed,template=template))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile'))),True)
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
