"""Independent derivative readback from displayed function and operator rows."""
import importlib.util,re
from pathlib import Path
sp=importlib.util.spec_from_file_location('exp_readback_scalar',Path(__file__).with_name('separable-ode-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
s,x=p.s,p.x
def scalar(raw):
 return p.scalar(raw.strip().rstrip('.,:'))
def operator_value(raw):
 raw=raw.replace(r'\left','').replace(r'\right','');slots={}
 marker=re.compile(r'\\frac\{\\(?:text|mathrm)\{d\}\}\{\\(?:text|mathrm)\{d\}x\}')
 while match:=marker.search(raw):
  pos=match.end()
  while raw[pos].isspace():pos+=1
  assert raw[pos]=='(',raw
  start=pos+1;depth=1;pos+=1
  while depth:
   depth+=(raw[pos]=='(')-(raw[pos]==')');pos+=1
  inside=raw[start:pos-1];slot=next(v for v in ('i','j','k','u','v','z','t','y') if v not in re.sub(r'\\[A-Za-z]+','',raw) and v not in slots)
  slots[slot]=s.diff(scalar(inside),x);raw=raw[:match.start()]+'('+slot+')'+raw[pos:]
 result=scalar(raw)
 for key,value in slots.items():result=result.subs(p.p.locals_[key],value)
 return result
def function_and_point(prompt):
 functions={};point=None
 for b in p.blocks(prompt):
  clean=b.strip().rstrip('.,');m=re.fullmatch(r'([fghk])\(x\)\s*=\s*(.+)',clean,re.S)
  if m and '{{' not in m[2]:
   expression=m[2];subs={}
   for n,(name,F) in enumerate(functions.items()):
    slot=('i','j','k')[n];expression=expression.replace(name+'(x)','('+slot+')');subs[p.p.locals_[slot]]=F
   functions[m[1]]=scalar(expression).subs(subs)
  elif clean.startswith('x='):point=scalar(clean[2:])
 assert functions,(prompt,functions)
 if len(functions)>1:assert list(functions)[-1]=='k' and len(functions)==3,(prompt,functions)
 name=list(functions)[-1];return name,functions[name],point
def stages(text,F,point):
 derivative=s.diff(F,x);expected=derivative;counts={'derivative_rows':0,'evaluation_rows':0,'operator_rows':0}
 for block in p.blocks(text):
  raw=p.clean(block)
  direct=re.search(r"[fghk]'\(([^)]*)\)",raw)
  if '=' not in raw or not (direct or any(label in raw for label in ('′}(x)',r'\frac{\text{d}',r'\frac{\mathrm{d}'))):continue
  evaluation=r'|}_{x=' in raw or r'|_{x=' in raw or bool(direct and direct[1]!='x')
  if direct and direct[1]!='x':assert point is not None and p.equal(scalar(direct[1]),point)
  if evaluation:assert point is not None;expected=derivative.subs(x,point)
  else:expected=derivative
  rows=raw.split(r'\\')
  for row in rows:
   if '=' not in row:continue
   # The first equals in an evaluation row can belong to its x=subscript.
   if evaluation and ('|}_{x=' in row or '|_{x=' in row):
    parts=re.split(r'\}\s*=',row,maxsplit=1);assert len(parts)==2,row;right=parts[1]
    m=re.fullmatch(r'\{?\((.+)\)\\?\,?\s*\|\}?_\{x=(.+)\}',right.strip().rstrip('.,'))
    assert m,(row,'unrecognized evaluation mask')
    displayed_point=scalar(m[2]);assert p.equal(displayed_point,point);value=scalar(m[1]).subs(x,displayed_point)
   else:
    _,right=row.split('=',1);right=right.strip().rstrip('.,');value=operator_value(right)
   assert p.equal(value,expected),(row,value,expected)
   counts['evaluation_rows' if evaluation else 'derivative_rows']+=1
   if r'\frac{\text{d}}' in row or r'\frac{\mathrm{d}}' in row:counts['operator_rows']+=1
 return counts
