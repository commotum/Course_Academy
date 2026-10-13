"""Read actual standard equations, each isolation node, and complete answer banks."""
import json,re,hashlib,sys,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'qa-line-intersections.py','standardparser');x,y,u=map(p.symbols.get,'xyu')
def expr(t):return p.expr(t.replace(r'\dfrac',r'\frac').replace('k','u'))
def eq(t):return tuple(expr(v) for v in t.split('='))
def coefficients(E):
 L,D=E;z=s.expand(L-D);return z.coeff(x),z.coeff(y),-z.subs({x:0,y:0})
def line(t):
 L,D=eq(t);assert L==y;return D.coeff(x),D.subs(x,0)
def check(k):
 g=load(ROOT/f'generate/scratch/{k}.py','standardgen'+str(k));raw=load(R/'qa-elimination-solution.py','standardraw');source=raw.raw(g,k);C=dict(records=0,isolation_stages=0,slope_statements=0,choices=0,whole_banks=0,coefficient_equalities=0)
 for r in json.loads((R/f'qa/{k}-sampled.json').read_text()):
  q=r['question'];t=q[':question/problem'];sol=q[':question/worked-solution'];f=q[':question/answer-fields'][0];level=q[':question/difficulty'].split('/')[-1];bs=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)
  if k==17592186087687:
   match=re.search(r'parallel to \$(.*?)\$',t);assert match;E=eq(match[1]);a,b,c=coefficients(E);m=-a/b;h=c/b
   if level=='easy':assert abs(b)==1
   elif level=='moderate':assert 2<=abs(b)<=6 and s.igcd(a,b)>1
   else:assert 5<=abs(a)<=12 and 3<=abs(b)<=6 and s.igcd(a,b)==1 and m.q>1
   assert len(bs)==2 and list(map(eq,p.aligned(bs[0])))==[E,(b*y,-a*x+c),(y,m*x+h)];C['isolation_stages']+=3
   stated=re.search(r'So, the slope is \$(.*?)\$',sol);assert stated and expr(stated[1])==m;C['slope_statements']+=1
   vals=[line(z[':answer/value']) for z in f[':answer-field/choices']];profile=r['generation']['bank_profile'];fourth=a if profile=='method-sign-reciprocal' else -a;expected={(m,h+1),(-m,h-1),(1/m,h+2),(-1/m,h-2),(fourth,h+3)};assert len(vals)==5 and set(vals)==expected
   for choice in f[':answer-field/choices']:
    z,j=line(choice[':answer/value']);assert (z==m and j!=h)==(choice[':answer/id']==f[':answer-field/correct'][1]);C['choices']+=1
   assert line(bs[1])==(m,h+1);C['whole_banks']+=1
  else:
   match=re.search(r'lines \$(.*?)\$ and \$(.*?)\$',t);assert match;known,unknown=list(map(eq,match.groups()));a,b,c=coefficients(known);A,B,D=coefficients(unknown);assert A==u;m=-a/b;h=c/b;answer=-B*m;assert D/B!=h
   converted=bs[:-1];expected_count=1 if level=='easy' else 2;assert len(converted)==expected_count
   if level!='easy':
    z=list(map(eq,p.aligned(converted.pop(0))));want=[known,(b*y,-a*x+c)]+([(-b*y,a*x-c)] if b<-1 else [])+[(y,m*x+h)];assert z==want;C['isolation_stages']+=len(z)
   else:assert known==(y,m*x+h) and m.q==1
   z=list(map(eq,p.aligned(converted[0])));want=[unknown,(B*y,-u*x+D)]+([(-B*y,u*x-D)] if B<0 else [])+[(y,-u*x/B+D/B)];assert z==want;C['isolation_stages']+=len(z)
   assert eq(bs[-1])==(-u/B,m);C['coefficient_equalities']+=1
   if level=='moderate':assert m.q==1
   if level=='hard':assert m.q>1 and s.igcd(abs(B),m.q)==1 and answer.q>1
   assert len(f[':answer-field/choices'])==1 and '{{field-1}}' in t;choice=f[':answer-field/choices'][0];assert expr(choice[':answer/value'])==answer and choice[':answer/id']==f[':answer-field/correct'][1];C['choices']+=1
   conclusion=re.search(r'Consequently, \$k=(.*?)\$',sol);assert conclusion and expr(conclusion[1])==answer
   for value in re.findall(r'So, the slope is \$(.*?)\$',sol):assert expr(value) in (m,-u/B);C['slope_statements']+=1
  assert sol.startswith('For two lines to be parallel, they must have the same slope.');C['records']+=1
 out=dict(status='passed',kp_id=k,source=source,readback=C,script_sha256=hashlib.sha256((ROOT/f'generate/scratch/{k}.py').read_bytes()).hexdigest());(R/f'qa/{k}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':
 for k in map(int,sys.argv[1:]):check(k)
