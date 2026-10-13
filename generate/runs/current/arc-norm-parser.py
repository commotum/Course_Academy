"""Parent checks derivative inputs/components and each nonnegative norm stage."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('root_norm_arc',Path(__file__).with_name('arc-vector-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)

def vector(raw):
 raw=raw.replace(r'\left','').replace(r'\right','').replace(r'\langle','⟨').replace(r'\rangle','⟩').strip().rstrip('.,?')
 if '⟨' not in raw:return p.vector(raw)
 prefix,rest=raw.split('⟨',1);inside,suffix=rest.split('⟩',1);balance=prefix.count('(')-prefix.count(')')
 assert suffix.strip()==')'*balance,(raw,prefix,suffix);factor=p.math(prefix+('1' if balance else '')+')'*balance) if prefix else 1
 return tuple(factor*p.math(v) for v in inside.replace(r'\,','').split(','))

def operator(raw):
 normalized=raw.replace(r'\left','').replace(r'\right','').replace(r'\langle','⟨').replace(r'\rangle','⟩')
 factor=1
 if '⟨' in normalized:
  prefix=normalized.split('⟨')[0];balance=prefix.count('(')-prefix.count(')');factor=p.math(prefix+('1' if balance else '')+')'*balance) if prefix else 1
 values=[]
 for m in re.finditer(r'\\frac\{\\(?:mathrm|text)\{d\}\}\{\\(?:mathrm|text)\{d\}t\}\(',raw):
  start=m.end();i=start;depth=1
  while depth:
   assert i<len(raw),raw;depth+=(raw[i]=='(')-(raw[i]==')');i+=1
  values.append(factor*p.math(raw[start:i-1]))
 assert values,raw;return tuple(values)

def stages(text,curve,bounds):
 group=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)[0];rows=re.split(r'\\\\',group);speed=p.speed(curve);der=tuple(s.diff(z,p.p.t) for z in curve);roles=[]
 counts=dict(derivative_operator_components=0,derivative_components=0,norm_stages=0)
 for n,row in enumerate(rows):
  raw=row.split('=',1)[1].replace('&','').strip().rstrip('.,?')
  if '⟨' in raw or r'\langle' in raw:
   is_operator=bool(re.search(r'\\frac\{\\(?:mathrm|text)\{d\}\}\{\\(?:mathrm|text)\{d\}t\}',raw));values=operator(raw) if is_operator else vector(raw);expected=curve if is_operator else der
   assert len(values)==len(expected) and all(p.same(a,b) for a,b in zip(values,expected)),(raw,values,expected)
   name='derivative_operator_components' if is_operator else 'derivative_components';counts[name]+=len(values);roles.append('operator' if is_operator else 'derivative')
  else:
   value=p.math(raw);assert p.same_on(value,speed,bounds),(raw,value,speed,bounds);counts['norm_stages']+=1;roles.append('norm')
 return tuple(roles),counts
