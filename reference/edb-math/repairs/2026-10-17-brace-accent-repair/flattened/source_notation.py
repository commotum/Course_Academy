"""Recover accent structure while retaining historical non-accent math spelling."""
import sys
sys.dont_write_bytecode=True
import importlib.util,re,copy
from pathlib import Path
from bs4 import BeautifulSoup,Tag
ROOT=Path(__file__).resolve().parents[5]
def load(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
lj=load('brace_old_json',Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py'))
md=load('brace_old_markdown',Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/5-MD/md.py'))
history=load('brace_source_history',ROOT/'scripts/import_historical_question_content.py')
def children(n):return n.find_all(recursive=False)
def bare(n):
 while n.name in ('mrow','mstyle','mpadded','semantics') and len(children(n))==1:n=children(n)[0]
 return n
def is_accent(n):
 n=bare(n)
 if n.name not in ('munder','mover')or len(children(n))!=2:return False
 a,b=children(n)
 return b.name=='mo' and b.text.strip() in ('⏟','⏞') or is_accent(a)
def label_tex(n):
 # Labels preserve words as text; old flattening merged 'N terms' into Nterms.
 c=copy.deepcopy(n)
 for text in [c] if c.name=='mtext' else c.find_all('mtext'):
  if '[math]' in text.text:
   parts=re.split(r'(\[math\].*?\[/math\])',text.text,flags=re.S)
   fragments=[]
   for part in parts:
    if not part:continue
    if part.startswith('[math]'):fragments.append('{'+part[6:-7]+'}')
    else:fragments.append(r'\text{'+part+'}')
   replacement=BeautifulSoup('<mi>BRACELABELTEX</mi>','html.parser').mi
   replacement.string=''.join(fragments)
   text.replace_with(replacement)
   if text is c:c=replacement
 r=history.Renderer(None);value=r.m(c)
 assert not r.errors,r.errors
 value=re.sub(r'\\operatorname\{(sin|cos|tan|csc|sec|cot|log|ln|exp)\}',r'\\\1 ',value)
 value=re.sub(r'\{(sin|cos|tan|csc|sec|cot|log|ln|exp)\}(?=\^)',r'\\\1 ',value)
 return value

def recover(n):
 n=bare(n)
 if is_accent(n):
  base,mark=children(n)
  if mark.name=='mo' and mark.text.strip() in ('⏟','⏞'):
   command=r'\underbrace' if mark.text.strip()=='⏟' else r'\overbrace'
   return command+'{'+recover(base)+'}'
  return recover(base)+('_' if n.name=='munder' else '^')+'{'+label_tex(mark)+'}'
 c=copy.deepcopy(n);replacements=[]
 def walk(cur):
  for child in list(children(cur)):
   if is_accent(child):
    token='BRACERECOVERY'+str(len(replacements))+'TOKEN'
    replacements.append((token,recover(child)))
    placeholder=BeautifulSoup('<mi></mi>','html.parser').mi;placeholder.string=token;child.replace_with(placeholder)
   else:walk(child)
 walk(c)
 result=md.normalize_math_tex(lj.mathml_to_text(c))
 for token,replacement in replacements:
  assert result.count(token)==1,(token,result)
  result=result.replace(token,replacement)
 return result

def source_tex(mathml):return recover(BeautifulSoup(mathml,'html.parser').find())
