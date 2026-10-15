"""Independent rendered-TeX reader; does not import generator or use parameter metadata."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('otherlog_elem',Path(__file__).parent/'reference/elementary-integral-readback.py');E=importlib.util.module_from_spec(z);z.loader.exec_module(E)
x,u,C=E.x,E.u,E.C

def atom(t,i):
 while i<len(t)and t[i].isspace():i+=1
 assert i<len(t),t
 if t[i]in'{(':
  opener=t[i];closer='}'if opener=='{'else')';depth=1;j=i+1
  while depth:
   assert j<len(t),t;depth+=(t[j]==opener)-(t[j]==closer);j+=1
  return t[i+1:j-1],j
 m=re.match(r'\d+|[xu]',t[i:]);assert m,(t,i);j=i+len(m[0]);a=m[0]
 if j<len(t)and t[j]=='^':p,j=atom(t,j+1);a+='^{'+p+'}'
 return a,j

def preprocess(t):
 t=t.replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\operatorname{ln}',r'\ln').replace(r'{ln}',r'\ln').replace(r'\operatorname{log}',r'\log ').replace('{log}',r'\log').replace(r'\Longrightarrow','⟹').replace(r'\,','').replace(r'\quad','')
 while(m:=re.search(r'\\log_\{?(\d+)\}?',t)):
  base=m[1];j=m.end();power='1'
  if j<len(t)and t[j]=='^':power,j=atom(t,j+1)
  arg,end=atom(t,j)
  replacement=r'(\frac{\ln('+arg+r')}{\ln('+base+r')})'
  if power!='1':replacement+='^{'+power+'}'
  t=t[:m.start()]+replacement+t[end:]
 # Unsubscripted log in observed q31399 is common logarithm. Its scale changes
 # only an integration constant inside ln|log x|; preserve that operator role.
 while(m:=re.search(r'\\log(?![_A-Za-z])',t)):
  arg,end=atom(t,m.end());t=t[:m.start()]+r'(\frac{\ln('+arg+r')}{\ln(10)})'+t[end:]
 return t
_original_scalar=E.scalar
def scalar(t):return _original_scalar(preprocess(t))
E.scalar=scalar
def derivative(v,var,inner=None):
 if inner is not None:v=v.subs(u,inner)
 v=v.replace(lambda z:z.func==s.log and z.args[0].has(s.Abs),lambda z:E.RealLogAbs(z.args[0].replace(s.Abs,lambda a:a)))
 return s.diff(v,var).replace(lambda z:z.func==E.RealLogAbs,lambda z:s.log(s.Abs(z.args[0])))
E.derivative=derivative

def same(a,b):
 d=s.expand(s.expand_log(a-b));return d==0 or s.cancel(d)==0 or s.simplify(d)==0

def check(record,allow_source_error=False):
 q=record['question'];F,var=E.prompt(q[':question/problem']);assert var==x
 sol=preprocess(q[':question/worked-solution']);m=re.search(r'\$u\s*=([^$]+)\$',sol);assert m,sol;U=scalar(m[1]);du=s.diff(U,x)
 block=next(b for b in re.findall(r'\$\$(.*?)\$\$',sol,re.S)if'⟹'in b);left,right=block.split('⟹');left=left.strip();assert left.split('=',1)[0].strip()==r'\frac{\text{d}u}{\text{d}x}'
 assert same(scalar(left.split('=',1)[1]),du),('actual derivative',left)
 dl,dr=right.strip().rstrip('.').split('=');matches=[re.fullmatch('(.*?)'+E.DIFF,t.strip())for t in(E.fraction_measure(dl),E.fraction_measure(dr))];assert all(matches),right
 def diffvalue(m):return(scalar(m[1])if m[1].strip()else s.Integer(1))*(du if m[2]=='u'else 1)
 assert same(diffvalue(matches[0]),diffvalue(matches[1])),('actual differential',right)
 counts=E.stages(sol,F,x,U)
 f=q[':question/answer-fields'][0];assert f[':answer-field/type'].endswith('/radio')
 vals=[scalar(a[':answer/value'])for a in f[':answer-field/choices']];ds=[E.derivative(v,x)for v in vals];correct=[a[':answer/id']for a,d in zip(f[':answer-field/choices'],ds)if same(d,F)];duplicates=[]
 for i,d in enumerate(ds):
  for j,e in enumerate(ds[:i]):
   if same(d,e):duplicates.append([j,i])
 assert f[':answer-field/correct'][1]in correct,('wrong key',correct)
 if not allow_source_error:assert correct==[f[':answer-field/correct'][1]]and not duplicates,('equivalent bank',correct,duplicates)
 counts.update({'answer_values':len(vals),'correct_choices':len(correct),'duplicate_pairs':duplicates,'differentials':2})
 return F,U,counts
