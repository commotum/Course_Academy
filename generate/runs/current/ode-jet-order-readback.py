"""Root full implicit-ODE reader: independent jet coordinates and surviving order."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('root_order_base',Path(__file__).with_name('ode-scalar-parser.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
X=P.x;Y=s.Symbol('root_y',real=True);J={n:s.Symbol('root_jet'+str(n),real=True) for n in range(1,9)};aliases=dict(zip(range(1,9),('t','u','v','z','i','j','k','e')));P.locals_['y']=Y
for n,a in aliases.items():P.locals_[a]=J[n]
P.locals_['pi']=s.Function('source_f')(X)
FRACTION=re.compile(r'\\(?:d?frac)\{(.*?)\}\{\\text\{d\}(?:\{x\}|x)(?:\^\{(\d+)\})?\}')
PRIME=re.compile(r'\{y\}\^\{([′″‴\']+)\}')
def tokens(t):
 result=[]
 for m in FRACTION.finditer(t):
  top,n=m[1],int(m[2] or 1);powers=re.findall(r'\^\{(\d+)\}',top);assert (int(powers[0]) if powers else 1)==n and top.endswith('y') and 1<=n<=8
  assert re.sub(r'\\text\{d\}|\^\{\d+\}|[{}y\s]','',top)=='';result.append((m.start(),m.end(),n))
 for m in PRIME.finditer(t):
  n=sum({'′':1,'″':2,'‴':3,"'":1}[c] for c in m[1]);assert 1<=n<=8;result.append((m.start(),m.end(),n))
 assert result,t;return sorted(result)
def equation(t):
 assert '\\partial' not in t and not re.search(r'\\text\{d\}\{?[tuz]\}?',t),t
 ds=tokens(t);text=t
 for a,b,n in reversed(ds):text=text[:a]+'('+aliases[n]+')'+text[b:]
 # Euler's constant in these sources has a simple x/y exponent; f(x) is a
 # supplied forcing function, never an independent jet of the dependent y.
 text=re.sub(r'\{e\}\^\{([xy])\}',r'exp(\1)',text).replace('f(x)','pi')
 lhs,rhs=text.strip().rstrip('?.').split('=');res=s.simplify(P.scalar(lhs)-P.scalar(rhs));live=[n for n,j in J.items() if res.has(j)];assert live and max(live)==max(n for a,b,n in ds),('zero/cancelled highest derivative',t,res)
 assert res.free_symbols<={X,Y,*J.values()};return res,max(live),ds,text
