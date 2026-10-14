"""Root independently reads rendered vector operands/operators and solution rows."""
import hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186059713;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
G=mod('root_alt_generator',D.with_suffix('.py'));P=mod('root_alt_scalar',R/'ode-scalar-parser.py');F=mod('root_alt_fidelity',R/'root-source-fidelity.py')
originals,fidelity=F.check(G,K,D)
C=dict(records=0,printed_operand_vectors=0,operative_solution_rows=0,whole_banks=0,values=0,pair_checks=0,prose_masks=0,level_checks=0)
def vector(raw):return s.Matrix([P.scalar(x) for x in raw.strip()[1:-1].split(',')])
def names(t):return re.sub(r'\\overset\{\\to \}\{([uUvVwW])\}',lambda m:m[1].lower(),t).replace('u^(→)','u').replace('v^(→)','v').replace('w^(→)','w')
def calc(t,env):
 t=names(t).replace('&','').replace(r'\cdot','*').strip().rstrip('.')
 vectors=re.findall(r'⟨[^⟩]+⟩',t)
 out=[]
 for i in range(2):
  e=t
  for token in vectors:e=e.replace(token,'('+str(vector(token)[i])+')')
  for k,v in env.items():e=re.sub(r'\b'+k+r'\b','('+str(v[i])+')',e)
  e=re.sub(r'(\d)([uvw])',r'\1*\2',e)
  # Adjacent scalar and vector parentheses denote ordinary multiplication.
  e=re.sub(r'(\d|\))(?=\()',r'\1*',e)
  for k,v in env.items():e=e.replace(k,'('+str(v[i])+')')
  out.append(s.sympify(e))
 return s.Matrix(out)
def eq(a,b):return a==b

def check(r,raw=False):
 q,m=r['question'],r['generation'];prompt=names(q[':question/problem']);defs=re.findall(r'\$([uvw])\s*=\s*(⟨[^⟩]+⟩)\$',prompt);assert defs
 env={k:vector(v) for k,v in defs};C['printed_operand_vectors']+=len(env)
 target=re.search(r'then \$(.*?)=\$',prompt).group(1);result=calc(target,env);t=m['template']
 if not raw:
  level=q[':question/difficulty'].split('/')[-1];vals=list(itertools.chain.from_iterable(env.values()));assert all(v.is_Integer and abs(v)<= (9 if level=='easy' else 6) for v in vals)
  if level=='easy':assert t in ('sum_lower','sum_upper','subtract','scalar') and len(env)==(1 if t=='scalar' else 2)
  elif level=='moderate':assert t=='linear_combination' and len(env)==2 and all(v!=0 for v in vals) and '(' not in target and len(re.findall(r'[2-6][uv]',target))==2
  else:assert t=='nested_combination' and len(env)==3 and all(v!=0 for v in vals) and '-(' in target and len(re.findall(r'[2-4][uvw]',target))==3
  C['level_checks']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==1
  rows=blocks[0].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(chr(92)*2)
  assert len(rows)==(4 if t=='linear_combination' else 6 if t=='nested_combination' else 3)
  for row in rows:assert eq(calc(row.split('=')[-1],env),result),(t,row,result);C['operative_solution_rows']+=1
  if t.startswith('sum'):assert '+' in rows[1] and '⟨' in rows[1] and '+' in rows[0]
  elif t=='linear_combination':assert rows[0].count(r'\cdot')==2 and rows[1].count(r'\cdot')==4 and rows[2].count('⟨')==1
  elif t=='nested_combination':assert rows[0].count(r'\cdot')==3 and rows[1].count(r'\cdot')==6 and rows[2].count('⟨')==3 and rows[3].count('⟨')==2 and rows[4].count('⟨')==1
  if t in ('sum_lower','sum_upper'):
   old=originals['q-1300' if t=='sum_lower' else 'q-1324'];mask=lambda x:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$','@DISPLAY@',x,flags=re.S)).strip();assert mask(sol)==mask(old[':question/worked-solution']);C['prose_masks']+=1
 if q.get(':question/answer-fields'):
  f=q[':question/answer-fields'][0];values=[vector(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5 and sum(v==result for v in values)==1
  if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],values) if v==result]==[f[':answer-field/correct'][1]]
  for a,b in itertools.combinations(values,2):assert a!=b;C['pair_checks']+=1
  if not raw:
   a=env.get('u',env.get('v'));b=env.get('v');c=env.get('w');coeff=[int(x) for x in re.findall(r'(\d+)[uvw]',target)];sign=1 if '+' in target else -1
   if t.startswith('sum'):expected=[result,a-b,b-a,s.Matrix([a[0]+b[0],a[1]-b[1]]),s.Matrix([a[0]-b[0],a[1]+b[1]])]
   elif t=='subtract':expected=[result,a+b,b-a,s.Matrix([a[0]-b[0],a[1]+b[1]]),s.Matrix([a[0]+b[0],a[1]-b[1]])]
   elif t=='scalar':
    n=int(re.match(r'(-?\d+)',target)[1]);expected=[result,-result,n*s.ones(2,1)+a,s.Matrix([-result[0],result[1]]),-a-n*s.ones(2,1)]
   elif t=='linear_combination':
    n,h=coeff;expected=[result,n*a-sign*h*b,a+sign*h*b,n*a+sign*b,s.Matrix([n*a[0]+sign*h*b[0],a[1]+sign*b[1]])]
   else:
    n,h,j=coeff;sign=1 if '+' in target else -1;expected=[result,n*a-h*b+sign*j*c,n*a+h*b+sign*j*c,a-(h*b+sign*j*c),n*a-(b+sign*c)]
   assert all(v in values for v in expected);C['whole_banks']+=1
  C['values']+=5
 C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for t,l in G.TEMPLATES.items():
 for seed in (42,72,112):check(G.generate(l,seed,template=t))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']),True)
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
