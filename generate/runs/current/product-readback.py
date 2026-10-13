"""Strict parent reader of displayed product-rule problems and formal primes."""
import importlib.util,re
from pathlib import Path
sp=importlib.util.spec_from_file_location('parent_product_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
s=p.s;x=p.x
def logs(text):
 text=text.replace(r'\operatorname{log}',r'\log').replace('{log}',r'\log')
 pattern=r'(?:\\log|log)(?:_(?:\{([^{}]+)\}|(\d+)))?\s*'
 position=0
 while True:
  m=re.search(pattern,text[position:])
  if not m:break
  start=position+m.start();end=position+m.end();base=m[1] or m[2] or '10';argstart=end
  assert end<len(text)
  if text[end] in '({':
   depth=0
   for n in range(end,len(text)):
    if text[n] in '({':depth+=1
    elif text[n] in ')}':
     depth-=1
     if depth==0:end=n+1;break
   else:raise AssertionError(('Unclosed logarithm',text))
  else:
   arg=re.match(r'x|\d+',text[end:]);assert arg,(text,end);end+=len(arg[0])
  argument=text[argstart:end];replacement=r'\frac{\ln('+argument+r')}{\ln('+base+')}'
  text=text[:start]+replacement+text[end:];position=start+len(replacement)
 return text
def normalize(text):
 text=text.replace('′',"'").replace('⁡','').replace('\\\\','\\')
 text=re.sub(r'\^\{\s*\x27\s*\}',"'",text)
 text=re.sub(r'\{([uvfghk])\}',r'\1',text)
 return logs(text)
def scalar(text,functions=None):
 text=normalize(text).strip().rstrip('.,');functions=functions or {}
 for name,expr in functions.items():
  text=re.sub(r'\b'+name+r"'\s*\(x\)",lambda m:'('+s.latex(s.diff(expr,x)).replace(r'\log',r'\ln')+')',text)
  text=re.sub(r'\b'+name+r'\s*\(x\)',lambda m:'('+s.latex(expr).replace(r'\log',r'\ln')+')',text)
 while "'" in text:
  at=text.index("'");end=at-1
  while end>=0 and text[end].isspace():end-=1
  assert text[end] in ')}',(text,end)
  depth=0;start=None
  for n in range(end,-1,-1):
   if text[n] in ')}':depth+=1
   elif text[n] in '({':
    depth-=1
    if depth==0:start=n;break
  assert start is not None
  expr=scalar(text[start+1:end],functions);text=text[:start]+'('+s.latex(s.diff(expr,x)).replace(r'\log',r'\ln')+')'+text[at+1:]
 return p.scalar(text)
def same(a,b):
 if s.expand(a-b)==0:return True
 return s.trigsimp(s.expand(a-b),method='fu')==0
def question_function(prompt):
 m=re.search(r'Differentiate\s*\$(.*?)\$',prompt,re.S);assert m,prompt
 return scalar(m[1])
def definitions(worked):
 found={name:scalar(raw) for name,raw in re.findall(r'\$([uv])\(x\)=(.*?)\$',worked,re.S)}
 assert set(found)=={'u','v'};return found
def stages(worked,F,allow_raw_wrong_lhs=False):
 functions=definitions(worked);assert same(functions['u']*functions['v'],F);functions['f']=F
 df=s.diff(F,x);n=0;formal=0;rawerrors=0
 for block in re.findall(r'\$\$(.*?)\$\$',worked,re.S):
  block=re.sub(r'\\(?:begin|end)\{aligned\}','',block);carry=None
  for row in block.split(r'\\'):
   parts=row.replace('&','').strip().rstrip('.,').split('=')
   if len(parts)<2:continue
   if not parts[0].strip():assert carry is not None;parts[0]=carry
   else:carry=parts[0]
   vals=[scalar(z,functions) for z in parts]
   if allow_raw_wrong_lhs:
    assert not same(vals[0],df) and all(same(z,df) for z in vals[1:]);rawerrors+=1
   else:assert all(same(z,df) for z in vals),(row,vals,df)
   n+=len(vals)-1;formal+=int("'" in normalize(row))
 return {'derivative_rows':n,'formal_rows':formal,'raw_lhs_error':rawerrors}
def blank_complete(prompt,value,F=None):
 prompt=prompt.replace('{{field-1}}',value)
 # Source blank equations span math delimiters and the supplied fragment.
 tail=prompt.split('\n\n',1)[1];text=tail.replace('$','').strip();parts=text.split('=');assert len(parts)==2
 return scalar(parts[0],{'f':F} if F is not None else None),scalar(parts[1])
