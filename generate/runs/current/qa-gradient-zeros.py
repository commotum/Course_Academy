"""Independent complete zero-gradient sets, source banks and displayed derivatives."""
import importlib.util,json,re,sys,hashlib
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
sp=importlib.util.spec_from_file_location('zerosreadback',R/'qa-gradients.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
axes=p.axes;basis=p.basis
def points(text):
 result=[]
 for m in re.finditer(r'\(([^()]*)\)',text):
  if ',' not in m[1]:continue
  v=tuple(p.scalar(z) for z in m[1].replace(r'\,','').split(','))
  if any(a.free_symbols for a in v):continue
  result.append(v)
 assert result,text;return result
def pointset(a,b):return len(a)==len(b) and all(any(p.same(v,w) for w in b) for v in a)
def complete(F,D,n,prompt):
 if F.has(s.sin,s.cos):
  bound=re.search(r'0\\le y<([^$]+)\$',prompt);assert bound,prompt;upper=p.scalar(bound[1]);xform=s.solve(D[0],axes[0]);assert len(xform)==1
  expr=s.trigsimp(D[1].subs(axes[0],xform[0]));ys=s.solveset(expr,axes[1],domain=s.Interval(0,upper,right_open=True));assert isinstance(ys,s.FiniteSet),ys
  return [(s.simplify(xform[0].subs(axes[1],v)),v) for v in ys]
 if F.has(s.log):
  sols=s.solve(D,axes[:n],dict=True)
 else:sols=s.solve([s.together(d).as_numer_denom()[0] for d in D],axes[:n],dict=True)
 out=[]
 for sol in sols:
  assert set(sol)==set(axes[:n]),sol;v=tuple(sol[a] for a in axes[:n])
  if any(a.is_real is False for a in v):continue
  assert all(a.is_real for a in v),v
  sub=dict(zip(axes,v));good=all(p.equal(d.subs(sub),0) for d in D)
  if good:
   assert F.subs(sub).is_real is not False;out.append(v)
 assert out,(F,sols);return out
def expected_bank(template,F,true):
 x,y,z=axes;r=true[0]
 if template=='shifted_log':
  X,Y=r;return [[r],[(X-1,Y)],[(X-2,Y)],[(X,0)],[(X,-Y)]]
 if template=='quadratic':
  X,Y=r;poly=s.Poly(F,x,y);off=-poly.coeff_monomial(x)/(2*poly.coeff_monomial(y*y));return [[r],[(2*X,0)],[(-X,0)],[(0,X)],[(X,off)]]
 if template=='logquad':
  X,Y=r;a=s.diff(F,y,2)/2;return [[r],[(0,0)],[(0,-Y)],[(Y,0)],[(0,Y/(2*a))]]
 if template=='coupled':
  k=s.diff(F,x,y)/2;return [[r],[(k,1)],[(-k,1)],[(1,-k)],[(1,k)]]
 if template=='entropy':
  return [[r],[tuple(s.exp(-1) for _ in r)],[tuple(s.E*a for a in r)],[tuple(s.exp(-2)/a for a in r)],[tuple(1/a for a in r)]]
 if template=='branch3':
  zero=next(v for v in true if v[1]==0);nonzero=next(v for v in true if v[1]!=0);rr=nonzero[1];return [true,[zero],[nonzero],[(0,-rr,0)],[(rr,rr,rr)]]
 if template=='trig':
  first=next(v for v in true if v[1]==0);second=next(v for v in true if v[1]!=0);b=first[0];yy=second[1];return [true,[first],[second],[(b,yy)],[(-b,0),(b,yy)]]
 if template=='reciprocal2':
  X,Y=r;return [[(-X,-Y),r],[r],[(-X,Y),(X,-Y)],[(X,-Y)],[(-X,-Y)]]
 if template=='reciprocal3':
  X,Y,Z=next(v for v in true if v[2]==1);return [[(X,Y,1)],[(X,Y,-1),(X,-Y,1)],true,[(X,-Y,-1)],[(-X,Y,-1),(-X,-Y,1)]]
 raise AssertionError(template)

def check():
 k=17592186124445;g=p.load(ROOT/f'generate/scratch/{k}.py','zerosg');orig=json.loads((R/f'sources/{k}.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((ROOT/f'generate/scratch/{k}/source-cases.json').read_text());src=dict(prompts=0,solutions=0,values=0,keys=0)
 for c in cases:
  q0=next(q for q in orig if c['source_id'] in (q[':db/id'],q[':question/id'],q[':question/math-academy-id']));q=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question'];assert q[':question/problem']==q0[':question/problem'] and q[':question/worked-solution']==q0[':question/worked-solution'];src['prompts']+=1;src['solutions']+=1
  f=q[':question/answer-fields'][0];f0=q0[':question/answer-fields'][0];assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);src['values']+=len(f[':answer-field/choices']);F,D,V,pt,n=p.task(q);true=complete(F,D,n,q[':question/problem']);assert pointset(points(f0[':answer-field/correct'][':answer/value']),true);src['keys']+=1
 records=json.loads((R/f'qa/{k}-sampled.json').read_text());stats=dict(records=0,formal_partials=0,scalar_partial_stages=0,gradient_rows=0,complete_choice_sets=0)
 for r in records:
  q=r['question'];F,D,V,pt,n=p.task(q);assert pt is None;true=complete(F,D,n,q[':question/problem']);sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S);current=None
  for row in blocks[0].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
   lhs,rhs=re.split(r'&\s*=',row,maxsplit=1);rhs=rhs.strip().rstrip('.,');m=re.search(r'\{?[fgh]\}?_\{?([xyz])\}?|\\frac\{∂[fgh]\}\{∂([xyz])\}',lhs)
   if m:current='xyz'.index(m[1] or m[2])
   assert current is not None
   formal=re.fullmatch(r'\\frac\{∂\}\{∂([xyz])\}\((.*)\)',rhs,re.S)
   if formal:assert current=='xyz'.index(formal[1]) and p.equal(p.scalar(formal[2]),F);stats['formal_partials']+=1
   else:assert p.equal(p.scalar(rhs),D[current]),(r['generation']['template'],row,D[current]);stats['scalar_partial_stages']+=1
  # Every actual gradient-vector equality, including the solve-zero block,
  # must use the complete ordered partial vector and the correct basis.
  for m in re.finditer(r'(?:∇|\\nabla\s*)[fgh]\(x,y(?:,z)?\)\s*=([^$]*)\$',sol):
   rhs=m[1].strip().rstrip('.,:').replace(r'\mathbin{:}','');
   if rhs in ('0',r'\mathbf 0',r'\mathbf{0}'):continue
   assert p.same(p.vector(rhs),D+(s.S.Zero,)*(3-n)),(r['generation']['template'],rhs,D);stats['gradient_rows']+=1
  f=q[':question/answer-fields'][0];seen=[]
  for a in f[':answer-field/choices']:
   value=points(a[':answer/value']);assert pointset(value,true)==(a[':answer/id']==f[':answer-field/correct'][1]),(r['generation']['template'],a,true);assert not any(pointset(value,v) for v in seen);seen.append(value);stats['complete_choice_sets']+=1
  bank=expected_bank(r['generation']['template'],F,true);assert len(bank)==len(seen) and all(any(pointset(v,w) for w in bank) for v in seen),(r['generation']['template'],seen,bank);stats['complete_method_banks']=stats.get('complete_method_banks',0)+1
  # The concluding sentence must list the entire solution set, not just any
  # point that happens to make the gradient vanish.
  conclusion=re.split(r'(?:Therefore|Hence),',sol)[-1];assert pointset(points(conclusion),true),(r['generation']['template'],conclusion,true);stats['records']+=1
 out=dict(status='passed',kp_id=k,source=src,readback=stats,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
