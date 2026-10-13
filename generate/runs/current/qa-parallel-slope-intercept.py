"""Actual visible slopes, canonical reading prose, and all compared choices."""
import json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2];K=17592186087686
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'qa-line-intersections.py','parallelparser');expr=p.expr;eq=p.eq;x,y=p.symbols['x'],p.symbols['y']
def line(t):
 L,D=eq(t);assert L==y;assert s.diff(D,x,2)==0;return D.coeff(x),D.subs(x,0)
def check():
 g=load(ROOT/f'generate/scratch/{K}.py','parallelgen');raw=load(R/'qa-elimination-solution.py','parallelraw');source=raw.raw(g,K);C=dict(records=0,slope_prose=0,choice_equations=0,scalar_choices=0,whole_banks=0,distinct_lines=0)
 for r in json.loads((R/f'qa/{K}-sampled.json').read_text()):
  q=r['question'];t=q[':question/problem'];f=q[':question/answer-fields'][0];sol=q[':question/worked-solution'];choice_lines=t.startswith('Which of');given=re.findall(r'\$(y=[^$]*)\$',t);assert given;m,b=line(given[0]);level=q[':question/difficulty'].split('/')[-1]
  if level=='easy':assert m.q==1 and 1<=abs(m)<=12
  elif level=='moderate':assert abs(m.p)==1 and 2<=m.q<=12
  else:assert 2<=abs(m.p)<=12 and 2<=m.q<=12
  assert sol.startswith('For two lines to be parallel, they must have the same slope.')
  if choice_lines:
   vals=[line(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vals)==5;ks={k for v,k in vals};assert len(ks)==1;k=next(iter(ks));assert b!=k;expected={m,-m,b,k,1/m};assert {v for v,k in vals}==expected
   for a in f[':answer-field/choices']:
    z,j=line(a[':answer/value']);assert (z==m and j!=b)==(a[':answer/id']==f[':answer-field/correct'][1]);C['choice_equations']+=1
   conclusion=re.search(r'The only choice with the same slope is \$(.*?)\$',sol);assert conclusion and line(conclusion[1])==(m,k)
  else:
   assert len(given)==2;unknown=given[1].replace('mx','ux');uu=p.symbols['u'];L,D=eq(unknown);assert L==y and D.coeff(x)==uu;k=D.subs({x:0,uu:0});assert b!=k
   vals=[expr(a[':answer/value']) for a in f[':answer-field/choices']];assert set(vals)==({m} if len(vals)==1 else {m,-m,b,k,1/m})
   for a in f[':answer-field/choices']:assert (expr(a[':answer/value'])==m)==(a[':answer/id']==f[':answer-field/correct'][1]);C['scalar_choices']+=1
   assert 'Both lines are in slope-intercept form' in sol;conclusion=re.search(r'we must have \$m=(.*?)\$',sol);assert conclusion and expr(conclusion[1])==m
  bullets=re.findall(r'The slope of the line \$(.*?)\$ is \$(.*?)\$',sol)
  for printed,stated in bullets:
   if 'mx' in printed:assert stated=='m'
   else:assert line(printed)[0]==expr(stated)
   C['slope_prose']+=1
  assert len(bullets)==(6 if choice_lines else 2);C['distinct_lines']+=1;C['whole_banks']+=1;C['records']+=1
 # Intercepts affect content and distinctness, but cannot create new coefficient
 # read-off mathematics; explicit changed offsets must share the task identity.
 for L,m in [('easy','3'),('moderate','-1/7'),('hard','5/7')]:
  r1=g.generate(L,template='coefficient_blank',parameters={'slope':m,'b':'2','k':'4'});r2=g.generate(L,template='coefficient_blank',parameters={'slope':m,'b':'-3','k':'8'});assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint'];assert r1['question'][':question/id']!=r2['question'][':question/id']
 out=dict(status='passed',kp_id=K,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{K}.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':check()
