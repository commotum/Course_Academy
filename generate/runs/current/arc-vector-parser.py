"""Root reads arc-length vectors and complete integral expressions from TeX."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('parent_arc_scalar',Path(__file__).with_name('vector-math-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
MATH=re.compile(r'\$\$.*?\$\$|\$[^$]*\$',re.S)
def blocks(text):return [m[0][2:-2] if m[0].startswith('$$') else m[0][1:-1] for m in MATH.finditer(text)]
def math(raw):
 raw=raw.strip().rstrip('.,?').replace('\u2061','').replace(r'\displaystyle','')
 raw=re.sub(r'\\(?:big|Big|bigg|Bigg)(?:l|r)?', '',raw).replace('[','(').replace(']',')')
 raw=re.sub(r'\\(?:operatorname|mathrm)\{(sin|cos|tan|ln|log)\}',r'\1',raw)
 if '|' in raw:
  a=raw.index('|');b=raw.index('|',a+1);inside=s.Abs(math(raw[a+1:b]))
  command_free=re.sub(r'\\[A-Za-z]+','',raw)
  slot=next(letter for letter in ('u','v','z','x','y','i','j') if letter not in command_free)
  replaced=raw[:a]+'('+slot+')'+raw[b+1:]
  return math(replaced).subs(p.locals_[slot],inside)
 return p.scalar(raw)
def vector(raw):
 raw=raw.strip().rstrip('.,?').replace(r'\langle','⟨').replace(r'\rangle','⟩')
 raw=re.sub(r'\\(?:big|Big|bigg|Bigg)(?:l|r)?','',raw)
 if '⟨' in raw:
  prefix,inside=raw.split('⟨',1);assert inside.endswith('⟩')
  factor=math(prefix) if prefix.strip() else s.Integer(1)
  return tuple(factor*math(z) for z in inside[:-1].replace(r'\,','').strip().rstrip(',').split(','))
 values=p.vector(raw);return tuple(values)
def prompt(text):
 chunks=blocks(text);body=next(z for z in chunks if re.match(r'[rfgh]\(t\)\s*=',z));curve=vector(body.split('=',1)[1])
 endpoints=[math(z.split('=',1)[1]) for z in chunks if re.match(r't\s*=',z)];assert len(endpoints)==2 and s.simplify(endpoints[1]-endpoints[0])>0,text
 return curve,tuple(endpoints)
def group(raw,start):
 assert raw[start]=='{';depth=1;i=start+1
 while depth:
  assert i<len(raw),raw;depth+=(raw[i]=='{')-(raw[i]=='}');i+=1
 return raw[start+1:i-1],i
def integral(raw):
 raw=raw.strip().rstrip('.,?').replace(r'\displaystyle','').replace(r'{\int }',r'\int').replace(r'{\int}',r'\int')
 start=raw.index(r'\int');prefactor=raw[:start].strip();factor=math(prefactor) if prefactor else s.Integer(1)
 pos=start+len(r'\int');assert raw[pos]=='_';lo,pos=group(raw,pos+1);assert raw[pos]=='^';hi,pos=group(raw,pos+1)
 tail=raw[pos:].strip();match=re.search(r'(?:\\(?:text|mathrm)\{d\}\s*t|dt)\s*$',tail);assert match,raw
 fn=math(tail[:match.start()].rstrip().removesuffix(r'\,'));return math(lo),math(hi),s.simplify(factor*fn)
def radical(expr):
 replacements={z:s.sqrt(s.factor(s.trigsimp(s.expand(z.base)))) for z in s.preorder_traversal(expr) if isinstance(z,s.Pow) and z.exp==s.Rational(1,2)}
 return expr.xreplace(replacements)
def same(a,b):return s.simplify(s.trigsimp(radical(a)-radical(b)))==0
def on_interval(expr,interval):
 lo,hi=interval
 assumption=s.Q.positive(p.t) if lo>0 else s.Q.nonnegative(p.t) if lo>=0 else s.Q.negative(p.t) if hi<0 else s.Q.nonpositive(p.t) if hi<=0 else s.true
 flags={'positive':True} if lo>0 else {'nonnegative':True} if lo>=0 else {'negative':True} if hi<0 else {'nonpositive':True} if hi<=0 else {'real':True}
 domain=s.Symbol('_arc_interval_t',**flags)
 return s.refine(radical(expr),assumption).subs(p.t,domain).subs(domain,p.t)
def same_on(a,b,interval):return same(on_interval(a,interval),on_interval(b,interval))

def speed(curve):return s.sqrt(s.factor(s.trigsimp(s.expand(sum(s.diff(z,p.t)**2 for z in curve)))))
