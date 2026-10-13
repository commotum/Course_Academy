"""Independent actual-line classification and each printed substitution component."""
import json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186073777
symbols={v:s.Symbol(v,real=True) for v in 'xyuvst'}
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
def expr(t):
 t=t.replace(r'\left','').replace(r'\right','').replace('&','').strip()
 def group(t,start):
  assert t[start]=='{';end=start+1;depth=1
  while depth:depth+=(t[end]=='{')-(t[end]=='}');end+=1
  return t[start+1:end-1],end
 while r'\frac' in t:
  start=t.index(r'\frac');a,end=group(t,start+5);b,end2=group(t,end);t=t[:start]+'(('+str(expr(a))+')/('+str(expr(b))+'))'+t[end2:]
 assert re.fullmatch(r'[xyuvst0-9+*/().\s-]+',t),t
 return s.expand(parse_expr(t,local_dict=symbols,transformations=standard_transformations+(implicit_multiplication_application,)))
def eq(t):return tuple(expr(v) for v in t.split('='))
def aligned(t):return t.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip().split(r'\\')
def rows(t):return [eq(z) for z in aligned(t)]
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','intersectionsgenerator');parent=load(R/'qa-solution-count.py','rawparent');parent.K=K;source=parent.raw(g);C=dict(records=0,system_equations=0,isolation_stages=0,substituted_equations=0,distributed_components=0,collected_statements=0,whole_banks=0,choices=0,branches={})
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];text=q[':question/problem'];match=re.search(r'\$l_\{1\}: (.*), l_\{2\}: (.*)\$',text);assert match
  E=list(map(eq,match.groups()));v=sorted(set().union(*(a.free_symbols|b.free_symbols for a,b in E)),key=str);assert len(v)==2
  u,w=(symbols['u'],symbols['v']) if set(v)=={symbols['u'],symbols['v']} else (symbols['s'],symbols['t']) if set(v)=={symbols['s'],symbols['t']} else (symbols['x'],symbols['y'])
  coef=[(s.expand(L-D).coeff(u),s.expand(L-D).coeff(w),-s.expand(L-D).subs({u:0,w:0})) for L,D in E];a,b,c=coef[0];d,e,f=coef[1];m=-a/b;h=c/b;A=d+e*m;B=e*h
  mat=s.Matrix([z[:2] for z in coef]);aug=mat.row_join(s.Matrix([z[2] for z in coef]));answer='do not intersect' if mat.rank()<aug.rank() else 'intersect at one point' if mat.rank()==2 else 'intersect at infinitely many points'
  level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert E[0]==(w,m*u+h) and b==1 and m.q==1
  elif level=='moderate':assert abs(b)==1 and m.q==1
  else:assert 2<=abs(a)<=5 and 2<=abs(b)<=5 and s.igcd(a,b)==1 and m.q>1
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==4
  sys=blocks[0].replace(r'\left\{','').replace(r'\right.','');assert rows(sys)==E;C['system_equations']+=2
  iso=rows(blocks[1]);expected=[(w,m*u+h)] if level=='easy' else [(a*u+b*w,c),(b*w,-a*u+c)]+([(w,(-a*u+c)/b)] if abs(b)!=1 else [])+([(w,m*u+h)] if b!=1 else []);assert iso==expected;C['isolation_stages']+=len(iso)
  assert eq(blocks[2])==(w,m*u+h)
  stages=aligned(blocks[3]);actual=list(map(eq,stages));expected=[E[1],(d*u+e*(m*u+h),f),(d*u+e*m*u+e*h,f),(A*u+B,f)]+([(A*u,f-B)] if A else []);assert actual==expected;C['substituted_equations']+=1;C['collected_statements']+=1
  # Read the unevaluated distribution terms separately: correct totals alone
  # would miss compensating wrong coefficients or a repeated operation.
  lhs=stages[2].split('=')[0].replace('&','').strip();tokens=re.findall(r'(?:^|\s)([+-]?\s*(?:\\frac\{[^}]+\}\{[^}]+\}|\d+)?[xyuvst]|[+-]?\s*(?:\\frac\{[^}]+\}\{[^}]+\}|\d+))',lhs)
  components=[expr(z) for z in tokens];want=[z for z in (d*u,e*m*u,e*h) if z!=0];assert components==want,(lhs,components,want);C['distributed_components']+=len(want)
  field=q[':question/answer-fields'][0];vals=[z[':answer/value'] for z in field[':answer-field/choices']];assert set(vals)=={'do not intersect','intersect at one point','intersect at infinitely many points'} and len(vals)==3
  for choice in field[':answer-field/choices']:assert (choice[':answer/value']==answer)==(choice[':answer/id']==field[':answer-field/correct'][1]);C['choices']+=1
  assert 'Consequently, the lines '+answer in sol
  if not A:assert ("always true" if B==f else "always false") in sol
  else:assert 'nonzero' in sol
  C['whole_banks']+=1;C['records']+=1;C['branches'][answer]=C['branches'].get(answer,0)+1
 assert len(C['branches'])==3
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
