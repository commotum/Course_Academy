"""Root actual symbolic negative distribution, cancellation, matrix cells and full banks."""
import ast,copy,hashlib,importlib.util,itertools,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;K=17592186100992;D=R.parents[2]/f'generate/scratch/{K}-draft'
def mod(n,p):
 sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sys.modules[n]=m;sp.loader.exec_module(m);return m
G=mod('root_distrib_generator',D.with_suffix('.py'));P=mod('root_distrib_scalar',R/'ode-scalar-parser.py');F=mod('root_distrib_fidelity',R/'root-source-fidelity.py');originals,fidelity=F.check(G,K,D)
M=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
C=dict(records=0,actual_supplied_cells=0,symbolic_distribution_rows=0,canceled_pairs=0,unevaluated_subtraction_cells=0,collected_cells=0,matrix_values=0,scalar_values=0,bank_pairs=0,complete_method_banks=0,prose_masks=0,source_generalized_banks=0)
def matrix(t):return s.Matrix([[P.scalar(v) for v in row.split('&')] for row in t.split(chr(92)*2)])
def expr(text,env):
 text=re.sub(r'\\cancel\{([A-Z])\}',r'\1',text).replace('&','').strip().rstrip('.');matrices=[]
 def sub(m):
  name='_m'+str(len(matrices));matrices.append(matrix(m[1]));env[name]=matrices[-1];return name
 text=M.sub(sub,text)
 node=ast.parse(text,mode='eval').body
 def evaluate(n):
  if isinstance(n,ast.Name):assert n.id in env;return env[n.id]
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -evaluate(n.operand)
  assert isinstance(n,ast.BinOp) and isinstance(n.op,(ast.Add,ast.Sub));return evaluate(n.left)+evaluate(n.right) if isinstance(n.op,ast.Add) else evaluate(n.left)-evaluate(n.right)
 return evaluate(node)
def mask(t):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$','@DISPLAY@',t,flags=re.S)).strip()
def check(r,raw=False):
 q,m=r['question'],r['generation'];t=m['template'];env={l:matrix(body) for l,body in re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)};assert len(env)==(4 if t=='authored-hard' else 3) and len({a.shape for a in env.values()})==1
 target=re.search(r'Find \$(.*?)\$',q[':question/problem'])[1];correct=expr(target,dict(env));C['actual_supplied_cells']+=sum(len(v) for v in env.values())
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==2
  symbolic=blocks[0].strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}');rows=symbolic.split(chr(92)*2);assert len(rows)==3
  for row in rows:
   chain=[a.strip().replace('&','') for a in row.split('=')];assert expr(chain[-1],dict(env))==correct;C['symbolic_distribution_rows']+=1
  assert '(' not in rows[0].split('=')[-1] and rows[0].count('-')>=2
  cancellations=re.findall(r'\\cancel\{([A-Z])\}',rows[1]);assert len(cancellations)==(4 if t in ('q-13536','authored-hard') else 2) and all(cancellations.count(l)==2 for l in set(cancellations));C['canceled_pairs']+=len(cancellations)//2
  if t=='q-13536':
   displayed=M.findall(blocks[1]);assert len(displayed)==1 and matrix(displayed[0])==correct;C['collected_cells']+=len(correct)
  else:
   displayed=M.findall(blocks[1]);assert len(displayed)==4;a,b,ops,last=map(matrix,displayed);assert a-b==correct and ops==correct and last==correct
   cells=[v.strip() for row in displayed[2].split(chr(92)*2) for v in row.split('&')]
   for v,x,y in zip(cells,a,b):
    mt=re.fullmatch(r'(-?\d+)-\(?(-?\d+)\)?',v);assert mt and tuple(map(int,mt.groups()))==(x,y);C['unevaluated_subtraction_cells']+=1
   C['collected_cells']+=len(correct)
  old=originals.get(t)
  if old and ':question/worked-solution' in old:assert mask(sol)==mask(old[':question/worked-solution']);C['prose_masks']+=1
 fields=q.get(':question/answer-fields',[])
 for f in fields:
  radio=f[':answer-field/type'].endswith('/radio')
  if radio:
   vals=[matrix(M.fullmatch(a[':answer/value'])[1]) for a in f[':answer-field/choices']];assert len(vals)==5 and all(v.shape==correct.shape for v in vals) and sum(v==correct for v in vals)==1
   for a,b in itertools.combinations(vals,2):assert a!=b;C['bank_pairs']+=1
   if ':answer-field/correct' in f:assert [a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if v==correct]==[f[':answer-field/correct'][1]]
   if not raw:
    if t=='q-13536':a,b,c=env['A'],env['B'],env['C'];expected=[a,a-2*c,a+2*b,a-b,a-c]
    else:
     # Identify the surviving signed symbolic names by coefficient collection,
     # independently of the generator's template role table.
     symbols={l:s.Symbol(l) for l in env};poly=s.expand(s.sympify(target,locals=symbols));positive=next(l for l,v in symbols.items() if poly.coeff(v)==1);negative=next(l for l,v in symbols.items() if poly.coeff(v)==-1);canceled=next(l for l,v in symbols.items() if poly.coeff(v)==0);a,b,z=env[positive],env[negative],env[canceled];expected=[correct,a+b,b-a,correct+z,correct-z]
    assert all(v in vals for v in expected);C['complete_method_banks']+=1
   C['matrix_values']+=5
  else:
   idx=int(f[':answer-field/key'].split('-')[-1])-1;assert len(f[':answer-field/choices'])==1 and P.scalar(f[':answer-field/choices'][0][':answer/value'])==correct[idx];C['scalar_values']+=1
 C['records']+=1
for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):check(r)
for t,spec in G.SPECS.items():
 for seed in (38,96):check(G.generate(spec[0],seed,template=t))
for c in json.loads((D/'source-cases.json').read_text()):check(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c.get('bank_profile',c.get('profile'))),True)
# Actual identifiable source permutations/compound operations must continue to
# work with changed data; original-parameter algebra alone cannot prove this.
for t in ('q-69623','q-69627','q-13536'):
 for seed in (58,122,214):
  normal=G.generate(G.SPECS[t][0],seed,template=t);p=normal['generation']['parameters'];r=G.generate(G.SPECS[t][0],seed,template=t,parameters=p,profile='source-original');check(r,True);vals=[matrix(M.fullmatch(a[':answer/value'])[1]) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  if t=='q-69623':
   a,b=s.Matrix(p['G']),s.Matrix(p['F']);c=a-b;expected=[s.Matrix(2,3,[c[i] for i in (3,4,5,0,1,2)]),s.Matrix(2,3,[c[i] for i in (1,0,2,4,3,5)]),s.Matrix(2,3,[a[0]+b[0],a[1]+b[1],b[2]-a[2],a[3]+b[3],a[4],a[5]+b[5]]),c,s.Matrix(2,3,[c[0],c[1],c[2],-a[3]-b[3],-a[4]+b[4],a[5]+b[5]])]
  elif t=='q-69627':
   a,b,z=map(s.Matrix,(p['V'],p['N'],p['C']));c=a-b;compound=a+b;compound[4]=c[4];expected=[z,s.Matrix(3,2,[c[i] for i in (0,1,3,2,4,5)]),s.Matrix(3,2,[c[i] for i in (0,1,4,5,2,3)]),compound,c]
  else:
   a,b,c=map(s.Matrix,(p['A'],p['B'],p['C']));expected=[a,b,c,s.zeros(2,2),s.Matrix([[a[1,1],a[0,1]],[a[0,1],a[1,1]]])]
  assert all(v in vals for v in expected);C['source_generalized_banks']+=1
result={'status':'passed','source':fidelity,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
