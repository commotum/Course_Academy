"""Root reads complete displayed polar bounds/integrands, independently of generators."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('root_polar_scalar',Path(__file__).with_name('polar-chain-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);X,Y,R,T=p.x,p.y,p.R,p.T
def scalar(text):
 text=text.replace(r'\!', '').replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac')
 return p.scalar(text)
def group(text,i):
 if text[i]!='{':
  m=re.match(r'-?\d+|\\[a-zA-Z]+|[xyruv]',text[i:]);assert m,(text,i);return m[0],i+m.end()
 j=i+1;depth=1
 while depth:
  assert j<len(text),text;depth+=(text[j]=='{')-(text[j]=='}');j+=1
 return text[i+1:j-1],j
def integral(raw):
 raw=raw.strip().rstrip('.,?').replace(r'\displaystyle','').replace(r'\left','').replace(r'\right','')
 raw=re.sub(r'\{\\int\s*\}',r'\\int',raw)
 starts=list(re.finditer(r'\\int\s*_',raw));assert len(starts)==2,raw
 vals=[];ends=[]
 for m in starts:
  pos=m.end()
  while raw[pos].isspace():pos+=1
  lo,pos=group(raw,pos);assert raw[pos]=='^';hi,pos=group(raw,pos+1);vals.extend((scalar(lo),scalar(hi)));ends.append(pos)
 body=raw[ends[1]:];match=re.search(r'(?:\\(?:text|mathrm|textrm)\s*\{?d\}?\s*r|dr)',body);assert match,(raw,body)
 f=body[:match.start()].strip().removesuffix(r'\,');tail=body[match.end():].replace(r'\,','').strip();assert re.fullmatch(r'(?:\\(?:text|mathrm|textrm)\s*\{?d\}?\s*(?:\\theta|θ)|d(?:\\theta|θ))',tail),tail
 prefix=raw[:starts[0].start()].strip();assert prefix in ('','{'),prefix
 gap=raw[ends[0]:starts[1].start()].strip()
 factor=1 if gap in ('','{') else scalar(gap)
 return tuple(vals),factor*scalar(f)
def equal(a,b):return s.simplify(s.refine(s.trigsimp(a-b),s.Q.nonnegative(R)))==0
def sector_equal(a,b,c,d):return equal(b-a,d-c) and s.simplify(s.Mod(a-c,2*s.pi))==0
def shape(bounds,f):
 a,b,lo,hi=bounds;return (s.srepr(s.Mod(a,2*s.pi)),s.srepr(b-a),s.srepr(lo),s.srepr(hi),s.srepr(s.trigsimp(f)))
