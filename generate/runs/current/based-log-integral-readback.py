"""Parent based-log grammar; function powers differ from argument powers."""
import importlib.util,re
from pathlib import Path
import sympy as s
def load(n,name):
 z=importlib.util.spec_from_file_location(n,Path(__file__).with_name(name));m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
E=load('root_based_elem','elementary-integral-readback.py');L=load('root_based_operand','log-chain-scalar-readback.py');x,u,C=E.x,E.u,E.C
def scalar(raw):
 text=E.clean(raw).replace(r'\displaystyle','').replace('[','(').replace(']',')').replace(r'\operatorname{log}',r'\log ').replace('{log}',r'\log ')
 while(m:=re.search(r'\\log(?![A-Za-z])',text)):
  i=m.end();base='10';power=None
  while i<len(text)and text[i].isspace():i+=1
  if text[i]=='^':power,i=L.operand(text,i+1)
  if text[i]=='_':
   i+=1
   if text[i]=='{':base,i=L.group(text,i)
   else:
    mm=re.match(r'\d+|e',text[i:]);assert mm,('unsupported log base',text);base=mm[0];i+=mm.end()
  while i<len(text)and text[i].isspace():i+=1
  if text[i]=='^':assert power is None;power,i=L.operand(text,i+1)
  arg,end=L.operand(text,i);replacement=r'(\ln('+arg+r')/\ln('+base+'))'
  if power is not None:replacement+='^{'+power+'}'
  text=text[:m.start()]+replacement+text[end:]
 return L.P.scalar(text)
E.scalar=scalar
