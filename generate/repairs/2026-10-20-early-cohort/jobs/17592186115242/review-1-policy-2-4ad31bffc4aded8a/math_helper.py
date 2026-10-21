import sys,os,json,pathlib,importlib.util,re,hashlib,collections,platform,shutil,subprocess
os.environ['PYTHONDONTWRITEBYTECODE']='1';sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent; W=R.parent/'workspace'; PY='/home/jake/Developer/Course_Academy/.venv/bin/python'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(W));spec=importlib.util.spec_from_file_location('reviewed_generator',W/'17592186115242.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
import sympy as s
x,y,k=s.symbols('x y k')
def write(n,obj):(R/n).write_text(json.dumps(obj,indent=2,default=str))
def expr(t):
 t=t.strip().replace(' ','').replace('\\,','').replace('−','-')
 while '\\frac' in t:
  t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 t=re.sub(r'(\d)([xyk])',r'\1*\2',t); t=re.sub(r'([xyk]|\))([xyk])',r'\1*\2',t)
 return s.sympify(t,locals={'x':x,'y':y,'k':k})
def rows(q):
 body=q[':question/problem'].split('\\begin{aligned}')[1].split('\\end{aligned}')[0]
 out=[]
 for line in body.split('\\\\'):
  a,b=line.replace('&','').replace(',','').split('=');out.append(s.expand(expr(a)-expr(b)))
 return out

def audit(rec):
 q=rec['question']; rr=rows(q);A,b=s.linear_eq_to_matrix(rr,[x,y]);roots=s.solve(A.det(),k);assert len(roots)==1
 root=roots[0];f=q[':question/answer-fields'][0]; choices=f[':answer-field/choices'];good=[z for z in choices if s.simplify(expr(z[':answer/value'].split('=')[1])-root)==0]
 assert len(good)==1 and good[0][':answer/id']==f[':answer-field/correct'][1]
 rank=A.subs(k,root).rank(); aug=A.row_join(b).subs(k,root).rank();dep='consistent dependent' in q[':question/problem'];assert (rank==aug==1) if dep else (rank<aug)
 # Every printed augmented matrix must be row-equivalent at a nonsingular and the singular k value.
 matrices=re.findall(r'\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}',q[':question/worked-solution'],re.S)
 for m in matrices:
  M=s.Matrix([[expr(z) for z in row.split('&')] for row in m.split('\\\\')]);assert M.shape==(2,3)
  for t in [root,root+1]: assert M.subs(k,t).rref()[0]==A.row_join(b).subs(k,t).rref()[0]
 final=re.findall(r'when\s+\$(.*?)\$',q[':question/worked-solution'])[-1].rstrip('.,');assert s.simplify(expr(final.split('=')[1])-root)==0
 return {'id':q[':question/id'],'root':str(root),'rank':rank,'augmented_rank':aug,'matrices_checked':len(matrices),'correct_position':choices.index(good[0]),'template':rec['generation']['template']}

