"""Parent independent readback of printed normal-vector tasks and all stages."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);g=importlib.util.module_from_spec(z);z.loader.exec_module(g);return g
p=load(R/'ode-scalar-parser.py','root_gradient_parser');axes=(p.x,p.y,p.z);basis=(p.i,p.j,p.k)
def equal(a,b):return s.simplify(a-b)==0
def scalar(raw):
 raw=re.sub(r'\\(?:text|mathrm)\{[^}]*\}', '',raw).replace('\xa0','').replace(r'\;','').replace(r'\!','').replace(r'\:','')
 return p.scalar(raw)
def vexpr(v):return sum(a*b for a,b in zip(v,basis))
def vector(raw):
 raw=raw.strip().rstrip('.,')
 if raw.startswith('⟨'):return s.Matrix([scalar(z) for z in raw[1:-1].split(',')]+[s.S.Zero]*(3-len(raw[1:-1].split(','))))
 expr=s.expand(scalar(raw));v=s.Matrix([expr.coeff(b) for b in basis]);assert equal(expr,vexpr(v)),('nonlinear vector',raw,expr);return v
def parens(text,start):
 assert text[start]=='(';depth=0
 for j in range(start,len(text)):
  depth+=(text[j]=='(')-(text[j]==')')
  if depth==0:return text[start+1:j],j+1
 raise AssertionError(text)
def transform(raw,function,point,grad,n):
 # Actual formal operators must contain the printed function, not metadata.
 count=0
 pattern=r'\\frac\{(?:∂|\\partial)\}\{(?:∂|\\partial)\s*([xyz])\}'
 while (m:=re.search(pattern,raw)):
  operand,end=parens(raw,m.end());f=scalar(operand);assert equal(f,function),(operand,function)
  d=s.diff(f,axes['xyz'.index(m[1])]);raw=raw[:m.start()]+'('+s.latex(d,ln_notation=True)+')'+raw[end:];count+=1
 # Named symbolic partials and the gradient are evaluated at their own arguments.
 pattern=r'\{?([fg])\}?_\{?([xyz])\}?\(([^()]*)\)'
 def partial(m):
  args=[scalar(z) for z in m[3].split(',')];assert len(args)==n
  return '('+s.latex(s.diff(function,axes['xyz'.index(m[2])]).subs(dict(zip(axes[:n],args)),simultaneous=True),ln_notation=True)+')'
 raw=re.sub(pattern,partial,raw)
 pattern=r'(?:∇|\\nabla\s*)([fg])\(([^()]*)\)'
 def gradient(m):
  args=[scalar(z) for z in m[2].split(',')];assert len(args)==n
  vals=[s.diff(function,a).subs(dict(zip(axes[:n],args)),simultaneous=True) for a in axes[:n]]+[s.S.Zero]*(3-n)
  return '('+s.latex(vexpr(vals),ln_notation=True)+')'
 raw=re.sub(pattern,gradient,raw)
 while '‖' in raw:
  a=raw.index('‖');b=raw.index('‖',a+1);v=vector(raw[a+1:b]);raw=raw[:a]+'('+s.latex(s.sqrt(v.dot(v)))+')'+raw[b+1:]
 return raw,count

def source(g,k,n):
 orig=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());counts=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,exact_solution_strings=0)
 for c in cases:
  q0=next(q for q in orig if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));lv=q0.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1]
  q=g.generate(lv,template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
  assert q[':question/problem']==q0[':question/problem'];counts['prompts']+=1
  for key in (':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in q0),(k,c,key)
  if ':question/worked-solution' in q0:
   counts['solutions']+=1;counts['exact_solution_strings']+=q[':question/worked-solution']==q0[':question/worked-solution']
   # Mathematical-notation normalization is allowed only with exact prose and
   # identical ordered stage count; full stages checked separately below.
   assert q[':question/worked-solution'].split('$$')[::2]==q0[':question/worked-solution'].split('$$')[::2]
   for a,b in zip(q[':question/worked-solution'].split('$$')[1::2],q0[':question/worked-solution'].split('$$')[1::2]):assert len(a.split(r'\\'))==len(b.split(r'\\'))
  assert len(q[':question/answer-fields'])==len(q0[':question/answer-fields'])
  for f,f0 in zip(q[':question/answer-fields'],q0[':question/answer-fields']):
   assert f[':answer-field/key']==f0[':answer-field/key'];assert f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];counts['fields']+=1
   vals=[vector(a[':answer/value']) for a in f[':answer-field/choices']];expected=[vector(a[':answer/value']) for a in f0[':answer-field/choices']]
   for v in vals:
    j=next((j for j,w in enumerate(expected) if all(equal(a,b) for a,b in zip(v,w))),None);assert j is not None,(k,c,v,expected);expected.pop(j);counts['values']+=1
   assert not expected;assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   if ':answer-field/correct' in f:
    v=vector(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]));w=vector(f0[':answer-field/correct'][':answer/value']);assert all(equal(a,b) for a,b in zip(v,w));counts['keys']+=1
 return counts

def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','g'+str(k));n=2 if k==17592186124461 else 3;src=source(g,k,n);records=json.loads((R/f'qa/{k}-sampled.json').read_text());stats=dict(records=0,formal_partials=0,gradient_stages=0,normalization_stages=0,choices=0,prose_points=0,conclusion_vectors=0)
 for r in records:
  q=r['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];m=re.search(r'\$[fg]\(x,\s*y(?:,\s*z)?\)\s*=\s*(.*?)\$',prompt);assert m,prompt
  function=scalar(m[1]);ptmatch=re.search(r'\(x,\s*y(?:,\s*z)?\)\s*=\s*\((.*?)\)',prompt);assert ptmatch,prompt
  point=tuple(scalar(z) for z in ptmatch[1].split(','));assert len(point)==n
  subs=dict(zip(axes[:n],point));grad=s.Matrix([s.simplify(s.diff(function,a).subs(subs)) for a in axes[:n]]+[s.S.Zero]*(3-n));assert grad.dot(grad)>0
  for m in re.finditer(r'(?:∇|\\nabla\s*)[fg]\(([^()]*)\)',sol):
   if m[1] in ('x,y','x,y,z'):continue
   actual=tuple(scalar(z) for z in m[1].split(','));assert all(equal(a,b) for a,b in zip(actual,point)) and len(actual)==n;stats['prose_points']+=1
  for m in re.finditer(r'\(x,\s*y(?:,\s*z)?\)\s*=\s*\(([^()]*)\)',sol):
   actual=tuple(scalar(z) for z in m[1].split(','));assert len(actual)==n and all(equal(a,b) for a,b in zip(actual,point));stats['prose_points']+=1
  blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);assert len(blocks)==(2 if n==2 else 1)
  for block_index,block in enumerate(blocks):
   evaluated=False
   for row in block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
    lhs,rhs=re.split(r'&\s*=',row,maxsplit=1)
    if lhs.strip() and '(x,y)' not in lhs and '(x,y,z)' not in lhs:evaluated=True
    transformed,count=transform(rhs,function,point,grad,n);stats['formal_partials']+=count
    expected=grad/s.sqrt(grad.dot(grad)) if block_index else (grad if evaluated else s.Matrix([s.diff(function,a) for a in axes[:n]]+[s.S.Zero]*(3-n)))
    # One original axis-normal source uses an extra = on a single row.
    for expr in transformed.split('='):
     actual=vector(expr);assert all(equal(a,b) for a,b in zip(actual,expected)),(k,r['generation']['template'],expr,expected)
     stats['normalization_stages' if block_index else 'gradient_stages']+=1
  if n==3:
   conclusion=re.search(r'Therefore,\s*\$(.*?)\$',sol);assert conclusion,sol;actual=vector(conclusion[1]);assert all(equal(a,b) for a,b in zip(actual,grad));stats['conclusion_vectors']+=1
  f=q[':question/answer-fields'][0];vals=[]
  for a in f[':answer-field/choices']:
   v=vector(a[':answer/value']);parallel=all(equal(z,0) for z in v.cross(grad));valid=parallel and not all(equal(z,0) for z in v)
   if n==2:valid=valid and equal(v.dot(v),1) and equal(v[2],0)
   assert valid==(a[':answer/id']==f[':answer-field/correct'][1]),(k,a,grad)
   assert not any(all(equal(a,b) for a,b in zip(v,w)) for w in vals);vals.append(v);stats['choices']+=1
  stats['records']+=1
 out=dict(status='passed',kp_id=k,source=src,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
