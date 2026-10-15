"""Private recursive TeX scalar reader; preserves trig function operands."""
import re
import sympy as sp
X,U,C=sp.symbols('x u C',real=True)
FUNCTIONS={name:getattr(sp,name) for name in ('sin','cos','tan','cot','sec','csc','log')}
def group(s,i,opening='{',closing='}'):
 if s[i]!=opening:raise ValueError(('expected group',s,i))
 depth=1;j=i+1
 while j<len(s) and depth:
  depth+=(s[j]==opening)-(s[j]==closing);j+=1
 if depth:raise ValueError(('unclosed group',s,i))
 return s[i+1:j-1],j

def latex(s):
 s=s.strip().rstrip('.,').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\!','').replace(r'\cdot','*').replace(r'\dfrac',r'\frac')
 s=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc|ln|log)\}',lambda m:'@'+m[1],s)
 s=re.sub(r'\{(sin|cos|tan|cot|sec|csc)\}',lambda m:'@'+m[1],s)
 s=re.sub(r'\\(sin|cos|tan|cot|sec|csc|ln|log)\b',lambda m:'@'+m[1],s)
 s=re.sub(r'(?<![@A-Za-z])(sin|cos|tan|cot|sec|csc|ln|log)(?![A-Za-z])',lambda m:'@'+m[1],s)
 s=s.replace(r'\pi','P').replace(' ','')
 def atom(i):
  if i>=len(s):raise ValueError(('missing atom',s,i))
  if s.startswith(r'\frac',i):
   a,j=group(s,i+5);b,j=group(s,j);return '('+str(latex(a))+')/('+str(latex(b))+')',j
  if s.startswith(r'\sqrt',i):
   a,j=group(s,i+5);return 'sqrt('+str(latex(a))+')',j
  if s[i] in '{(':
   a,j=group(s,i,s[i],'}'if s[i]=='{'else')');return '('+str(latex(a))+')',j
  if s[i]=='|':
   j=i+1;depth=0
   while j<len(s):
    if s[j]=='|' and depth==0:break
    depth+=(s[j]in'{(')-(s[j]in'})');j+=1
   if j==len(s):raise ValueError(('unclosed absolute value',s))
   return 'Abs('+str(latex(s[i+1:j]))+')',j+1
  if s[i]=='@':
   m=re.match('@(sin|cos|tan|cot|sec|csc|ln|log)',s[i:]);name=m[1];j=i+len(m[0]);power=None
   if j<len(s)and s[j]=='^':power,j=atom(j+1)
   # Unparenthesized trig arguments consume one numeric scale followed by x/u.
   if j<len(s)and(s[j].isdigit()or(s[j]in'+-'and j+1<len(s)and s[j+1].isdigit())):
    n=re.match(r'[+-]?\d+(?:\.\d+)?',s[j:]);arg=n[0];j+=len(n[0])
    if j<len(s)and s[j]in'xu':arg+='*'+s[j];j+=1
   else:arg,j=atom(j)
   val=('log'if name=='ln'else name)+'('+arg+')'
   if power is not None:val='('+val+')**('+power+')'
   return val,j
  m=re.match(r'\d+(?:\.\d+)?',s[i:])
  if m:return m[0],i+len(m[0])
  if s[i]in'xuCP':return ('pi'if s[i]=='P'else s[i]),i+1
  if s[i]in'+-':
   a,j=atom(i+1);return s[i]+'('+a+')',j
  raise ValueError(('unknown atom',s,i,s[i:]))
 out=[];i=0;previous=False
 while i<len(s):
  if s[i]in'+-*/^':out.append('**'if s[i]=='^'else s[i]);i+=1;previous=False;continue
  a,i=atom(i)
  if previous:out.append('*')
  out.append('('+a+')');previous=True
 return sp.sympify(''.join(out),locals={'x':X,'u':U,'C':C,'pi':sp.pi,'Abs':sp.Abs,'sqrt':sp.sqrt,**FUNCTIONS},rational=True)

def clean(s):
 for t in (r'\text{d}x',r'\text{d}u',r'\textrm{d}x',r'\textrm{d}u'):s=s.replace(t,'1')
 return s.replace(r'\,','').replace(r'\cdot','*').strip().rstrip('.')

def log_derivative(z,v):
 # d ln|f| = f'/f on each open domain component; no log identity rewrite.
 return sp.diff(z.replace(lambda t:t.func==sp.log and t.args[0].func==sp.Abs,lambda t:sp.log(t.args[0].args[0])),v)
