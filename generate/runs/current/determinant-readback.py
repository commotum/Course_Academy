"""Parent parser for actual two-by-two arrays and nested worked displays."""
import importlib.util,re
from pathlib import Path
spec=importlib.util.spec_from_file_location('root_det_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);s=p.s
def scalar(raw,mapping=None):
 mapping=mapping or {'r':'t','s':'u','t':'v','u':'k','w':'x','p':'x','q':'x','m':'x','n':'x','a':'x','b':'y','c':'z','d':'t'}
 raw=raw.replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac').replace(r'\cancel','')
 pieces=re.split(r'(\\[A-Za-z]+)',raw)
 raw=''.join(piece if piece.startswith('\\') else re.sub('[a-z]',lambda m:mapping.get(m[0],m[0]),piece) for piece in pieces)
 return p.scalar(raw)
def arrays(text,mapping=None):
 found=[]
 for m in re.finditer(r'\\begin\{(aligned|bmatrix|vmatrix)\}((?:(?!\\begin\{).)*?)\\end\{\1\}',text,re.S):
  body=m[2]
  if '& =' in body or len(body.split(chr(92)*2))!=2:continue
  cells=[z for row in body.split(chr(92)*2) for z in row.split('&')]
  if len(cells)==4:found.append((m.span(),tuple(scalar(z,mapping) for z in cells)))
 return found
def array(text,mapping=None):
 found=arrays(text,mapping);assert len(found)==1,(text,found);return found[0][1]
def displays(text):
 return [m[1] for m in re.finditer(r'\$\$(.*?)\$\$',text,re.S)]
def rows(block):
 # Protect nested arrays before splitting the outer teaching rows.
 for n,(span,_) in reversed(list(enumerate(arrays(block)))):
  a,b=span;block=block[:a]+'MATRIX'+str(n)+block[b:]
 if block.strip().startswith(r'\begin{aligned}'):
  block=block.strip()[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
 return [z.strip() for z in block.split(chr(92)*2)]
