import re
from functools import lru_cache
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
X=sp.Symbol('x',real=True);U=sp.Symbol('u',real=True);C=sp.Symbol('C',real=True)
def latex(s):
 s=re.sub(r'(\\(?:operatorname|text|textrm)\{(?:arcsec|arcsin|arctan)\})\s*([ux])',r'\1(\2)',s)
 s=s.replace('\u2061','').replace('\u00a0',' ').replace(r'\,','').replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\\(?:operatorname|text|textrm)\{(arcsec|arcsin|arctan)\}',lambda m:{'arcsec':'asec','arcsin':'asin','arctan':'atan'}[m[1]],s)
 def group(s,start):
  assert s[start]=='{',s
  depth=1;i=start+1
  while depth:
   depth+=(s[i]=='{')-(s[i]=='}');i+=1
  return s[start+1:i-1],i
 def convert(s):
  out='';i=0
  while i<len(s):
   if s.startswith(r'\frac',i) or s.startswith(r'\dfrac',i):
    i+=6 if s.startswith(r'\dfrac',i) else 5;a,i=group(s,i);b,i=group(s,i);out+='(('+convert(a)+')/('+convert(b)+'))'
   elif s.startswith(r'\sqrt',i):
    i+=5;a,i=group(s,i);out+='sqrt('+convert(a)+')'
   elif s[i]=='|':
    j=s.index('|',i+1);out+='Abs('+convert(s[i+1:j])+')';i=j+1
   else:out+=s[i];i+=1
  return out
 s=convert(s).replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(s,local_dict={'x':X,'u':U,'C':C,'asec':sp.asec,'asin':sp.asin,'atan':sp.atan,'Abs':sp.Abs,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

def integrand(q):
 p=q[':question/problem'];p=p[p.index(r'\int')+4:];p=p.split('$')[0];p=re.sub(r'=\s*}*\s*$','',p).strip().rstrip('.')
 p=p.replace(r'\,','').replace(r'\frac{\text{d}x}',r'\frac{1}').replace(r'\dfrac{\textrm{d}x}',r'\frac{1}').replace(r'\text{d}x','').replace(r'\textrm{d}x','').strip()
 return sp.simplify(latex(p))


def clean(s):
 s=s.strip()
 for token in [r'\quad',r'\displaystyle',r'\,',r'\;',r'\!',r'\cdot',r'\left',r'\right']:
  s=s.replace(token,'*' if token==r'\cdot' else '')
 s=re.sub(r'\\(?:begin|end)\{aligned\}','',s).strip()
 s=s.replace(r'\operatorname{arcsec}',r'\text{arcsec}')
 s=s.replace(r'\text{arcsec\u00a0}',r'\text{arcsec}')
 s=re.sub(r'\\(?:text|textrm)\{arcsec\s*\}',r'\\text{arcsec}',s)
 return s.strip().rstrip('.,')

def term_derivative(text,slope):
 """Read each displayed formal integral or primitive as its x-derivative.

 An integral in u transforms with du/dx, including every rendered coefficient
 and every formal input. No sqrt(z**2)->z rule is used across signed x.
 """
 s=clean(text)
 if r'\int' in s:
  assert s.count(r'\int')==1,s
  diffs=re.findall(r'\\(?:text|textrm)\{d\}([ux])',s)
  assert len(diffs)==1,(s,diffs)
  variable=diffs[0]
  s=s.replace(r'\int','')
  s=re.sub(r'\\(?:text|textrm)\{d\}[ux]','(1)',s)
  e=latex(s)
  if variable=='u':return sp.simplify(e.subs(U,slope*X)*slope)
  assert not e.has(U),s
  return e
 e=latex(s).subs(U,slope*X)
 return sp.diff(e,X)

@lru_cache(maxsize=20000)
def equivalent_derivatives(a,b):
 if a==b:return True
 # Exact expressions are compared on both components. A high-precision witness
 # can disprove equality early; every potentially equal pair still gets the
 # independent exact signed-symbol simplification below.
 for sign in [-1,1]:
  witness=sp.N((a-b).subs(X,sign*sp.Integer(37)),35)
  if witness.is_number and abs(complex(witness))>1e-24:return False
 for sign in [-1,1]:
  y=sp.Symbol('positive_radius',positive=True)
  if sp.simplify((a-b).subs(X,sign*y))!=0:return False
 return True

def displayed_stages(q):
 s=q[':question/worked-solution'];blocks=re.findall(r'\$\$([\s\S]*?)\$\$',s)
 # The substitution is read from the prose, never taken from generation metadata.
 sub=re.search(r'(?:substitute|Let)\s*\$u\s*=\s*([^$]+)',s)
 assert sub,('missing substitution',s)
 rhs=sub[1].rstrip('.')
 slope=sp.simplify(latex(rhs)/X);assert not slope.has(X) and slope>0
 # Read du/dx and dx or n dx = du equality independently.
 diffblock=next(b for b in blocks if r'\frac{\text{d}u}{\text{d}x}' in b or r'\dfrac{\textrm{d}u}{\textrm{d}x}' in b)
 initial=re.split(r'\\(?:quad|Longrightarrow)|⟹',diffblock)[0]
 derivative=latex(clean(initial.split('=')[1]));assert derivative==slope
 after=re.split(r'\\Longrightarrow|⟹',diffblock)[-1]
 # Treat dx=du/n as equality of infinitesimal coefficients after du=n dx.
 after=clean(after);left,right=after.split('=')
 def differential_coefficient(z):
  z=re.sub(r'\\(?:text|textrm)\{d\}u','('+sp.sstr(slope)+')',z)
  z=re.sub(r'\\(?:text|textrm)\{d\}x','(1)',z)
  return latex(z)
 assert sp.simplify(differential_coefficient(left)-differential_coefficient(right))==0
 target=integrand(q);checked=[]
 for block in blocks:
  if r'\int' not in block:continue
  terms=[clean(z) for z in re.split(r'\\\\|&?\s*=',block)]
  terms=[z.lstrip('&').strip() for z in terms if z.strip().strip('&')]
  for term in terms:
   # Basic formula is an identity independently checked in both signs.
   d=term_derivative(term,slope)
   expected=target
   if len(terms)==2 and '|u|' in terms[0]:
    expected=slope/(sp.Abs(slope*X)*sp.sqrt((slope*X)**2-1))
   assert equivalent_derivatives(d,expected),('invalid displayed term',term,d,expected)
   checked.append(term)
 assert checked
 return {'slope':str(slope),'operative_terms_checked':len(checked),'terms':checked}
