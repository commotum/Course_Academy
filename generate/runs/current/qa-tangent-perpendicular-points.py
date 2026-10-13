"""Root complete polynomial point sets, actual partials and elimination stages."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','parent');x,y=p.x,p.y
n=dict(records=0,choices=0,whole_sets=0,formal_inputs=0,tangent_rows=0,orthogonality_rows=0,elimination_rows=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def read(z):
 z=z.strip().rstrip('.,?').replace('&','').replace(r'\ ','').replace(r'\mathbf','').replace(r'\text{ }','')
 z=re.sub(r'\\(?:cancel|text)\{([^{}]*)\}',r'\1',z)
 return p.scalar(z)
def eq(z):
 a,b=z.split('=',1);return s.expand(read(a)-read(b))
def pointset(text):
 out=frozenset((s.simplify(read(a)),s.simplify(read(b))) for a,b in re.findall(r'\(([^(),]+),([^(),]+)\)',text));assert out,text;return out
def proportional(a,b):
 if a==0 or b==0:return a==b
 a=s.cancel(a).as_numer_denom()[0];b=s.cancel(b).as_numer_denom()[0]
 ratio=s.cancel(a/b);return not ratio.free_symbols and ratio!=0

def check(rec):
 q=rec['question'];g=rec['generation'];pieces=re.findall(r'(\$\$|\$)(.*?)\1',q[':question/problem'],re.S);F=eq(next(z for _,z in pieces if '=' in z));V=read(pieces[-1][1]);u,v=s.expand(V).coeff(p.i),s.expand(V).coeff(p.j);assert u or v
 fx,fy=s.diff(F,x),s.diff(F,y);condition=s.expand(u*fy-v*fx)
 # Independent elimination establishes completeness, beyond checking each option point.
 G=s.groebner([F,condition],y,x,domain='EX');assert G.is_zero_dimensional
 sols=s.solve_poly_system(list(G),x,y);assert sols is not None
 real=frozenset((s.simplify(a),s.simplify(b)) for a,b in sols if a.is_real is True and b.is_real is True);assert real
 assert all(not (s.simplify(fx.subs({x:a,y:b}))==0 and s.simplify(fy.subs({x:a,y:b}))==0) for a,b in real)
 f=q[':question/answer-fields'][0];banks=[pointset(z[':answer/value']) for z in f[':answer-field/choices']];assert len(banks)==5 and len(set(banks))==5 and sum(z==real for z in banks)==1
 if ':answer-field/correct' in f:assert next(z[':answer/id'] for z,b in zip(f[':answer-field/choices'],banks) if b==real)==f[':answer-field/correct'][1]
 if g['eligible_for_learning']:
  lv=q[':question/difficulty'].split('/')[-1]
  if lv=='easy':
   assert len(real)==1;r,z=next(iter(real));B=-s.Poly(F,x,y).coeff_monomial(y);assert B>1 and z==-r
   expected=[real,frozenset([(r,r)]),frozenset([(-r,r)]),frozenset([(B*r,-B*r)]),frozenset([(r,0)])]
  elif lv=='moderate':
   assert len(real)==2;ordered=sorted(real,key=str);r,z=next((a,b) for a,b in real if a>0);m=s.cancel(z/r);assert m>=2
   expected=[real,*[frozenset([pt]) for pt in ordered],frozenset([(r,-m*r),(-r,m*r)]),frozenset([(m*r,r),(-m*r,-r)])]
  else:
   assert lv=='hard' and len(real)==2;ordered=sorted(real,key=str);ys=[b for a,b in ordered];assert all(a==-b for a,b in ordered)
   expected=[real,*[frozenset([pt]) for pt in ordered],frozenset([(b,b) for b in ys]),frozenset([(b,-b) for b in ys])]
  assert set(expected)==set(banks)
 sol=q.get(':question/worked-solution')
 if sol:
  displays=[z for delim,z in re.findall(r'(\$\$|\$)(.*?)\1',sol,re.S) if delim=='$$'];assert pointset(sol.split('Finally',1)[1])==real
  derivatives=[z for z in displays if r'\frac{∂}{∂' in z];assert len(derivatives)==1;rows=derivatives[0].split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
  formal=next(row for row in rows if r'\frac{∂}{∂' in row);inputs=[]
  for m in re.finditer(r'\\frac\{∂\}\{∂([xy])\}\(',formal):
   start=m.end();end=start;depth=1
   while depth:depth+=(formal[end]=='(')-(formal[end]==')');end+=1
   body=read(formal[start:end-1]);inputs.append((m[1],body));assert s.expand(s.diff(body,x if m[1]=='x' else y)-(fx if m[1]=='x' else fy))==0
  assert [z for z,_ in inputs]==['y','x'];assert s.expand(read(rows[-1].split('=',1)[1])-(fy*p.i-fx*p.j))==0;n['formal_inputs']+=2;n['tangent_rows']+=1
  orth=next(z for z in displays if r'\cdot' in z and r'\begin{aligned}' in z);orows=orth.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\');scalar=[row for row in orows if '=' in row and r'\cdot' not in row];relation=scalar[-1].replace('&','')
  for row in scalar:
   if r'\text' not in row:assert proportional(eq(row),condition),(g['template'],row,condition);n['orthogonality_rows']+=1
  branches=re.split(r'\\text\{ or \}',relation)
  for branch in branches:
   rel=eq(branch);assert s.cancel(condition/rel).as_numer_denom()[1]==1 or proportional(rel,condition)
  after=displays[displays.index(orth)+1:];assert after
  for branch,display in zip(branches,after) if len(branches)>1 else [(relation,z) for z in after]:
   rel=eq(branch);lhs=read(branch.split('=',1)[0]);variable=x if lhs.free_symbols=={x} else y;replacements=s.solve(rel,variable);assert len(replacements)==1;sub={variable:replacements[0]};reference=s.factor(F.subs(sub));other=y if variable==x else x
   rows=display.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0].split(r'\\')
   for row in rows:
    if '=' not in row or r'\pm' in row or r'\text' in row or ',' in row.split('=')[1]:continue
    actual=eq(row).subs(sub)
    if len(branches)>1:assert set(s.solve(actual,other))==set(s.solve(reference,other))
    else:assert proportional(actual,reference),(g['template'],row,actual,reference)
    n['elimination_rows']+=1
 n['records']+=1;n['choices']+=5;n['whole_sets']+=1
if __name__=='__main__':
 kp=17592186124456;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');source=json.load(open(D/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  z=g.generate(c['level'],parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(z);q=z['question'];o=olds[c['source_id']]
  for k in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (k in q)==(k in o)
   if k in o:assert q[k]==(o[k][':db/ident'] if k.endswith('difficulty') else o[k])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted((a[':answer/value'],a[':answer/type']) for a in f[':answer-field/choices'])==sorted((a[':answer/value'],a[':answer/type'][':db/ident']) for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert value==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for z in json.load(open(D/'review.json')):check(z.get('record',z))
 for lv in ('easy','moderate','hard'):
  for seed in range(12):check(g.generate(lv,seed=88000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
