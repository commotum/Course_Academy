"""Parent parses displayed finite intervals, compound inequalities and unions."""
import importlib.util,re
from pathlib import Path
import sympy as s
P=Path(__file__).resolve().parent;sp=importlib.util.spec_from_file_location('root_interval_scalar',P/'ode-scalar-parser.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
def clean(text):
 text=text.strip().rstrip('.').replace('$','').replace(r'\,','').replace(r'\left','').replace(r'\right','')
 text=re.sub(r'\{\\color\{[^{}]+\}\{([^{}]*)\}\}',r'\1',text)
 return text.strip()
def endpoint(text):
 text=clean(text).strip()
 if text.replace(' ','') in ('-∞',r'-\infty'):return -s.oo
 if text.replace(' ','') in ('∞',r'\infty'):return s.oo
 e=p.scalar(text);assert not e.free_symbols and e.is_real and e.is_finite;return e
def meaning(raw):
 text=clean(raw)
 if ' or ' in text:return s.Union(*(meaning(z) for z in text.split(' or ')))
 text=re.sub(r'^[xyutz]\s*(?:∈|\\in)\s*','',text)
 if text.startswith(('(', '[')) and text.endswith((')',']')) and ',' in text:
  a,b=text[1:-1].split(',');return s.Interval(endpoint(a),endpoint(b),left_open=text[0]=='(',right_open=text[-1]==')')
 parts=re.split(r'(\\leq?|\\geq?|≤|≥|<|>)',text);assert len(parts) in (3,5),(raw,parts)
 intervals=[]
 for pos in range(0,len(parts)-2,2):
  lhs,rel,rhs=[z.strip() for z in parts[pos:pos+3]];le=rel in (r'\le',r'\leq','≤','<');strict=rel in ('<','>')
  if re.fullmatch('[xyutz]',lhs):value=endpoint(rhs);upper=le
  else:assert re.fullmatch('[xyutz]',rhs);value=endpoint(lhs);upper=not le
  intervals.append(s.Interval(-s.oo,value,right_open=strict) if upper else s.Interval(value,s.oo,left_open=strict))
 return s.Intersection(*intervals)
def task(prompt):
 inline=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',prompt,re.S);assert len(inline)==1,(prompt,inline)
 desired=meaning(inline[0]);assert isinstance(desired,s.Interval) and desired.start.is_finite and desired.end.is_finite and desired.start<desired.end
 return desired
