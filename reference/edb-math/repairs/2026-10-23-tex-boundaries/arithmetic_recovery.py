"""Use immutable source column declarations, not the damaged matrix conversion."""
import json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts/question_capture'));from math_format import MATH,normalize_math_boundaries,source_multiplication_tex

def blocks(text):
 out=[];offset=0
 while (start:=text.find('[MATH:',offset))>=0:
  depth,end=1,start+6
  while depth and end<len(text):depth+=(text[end]=='[')-(text[end]==']');end+=1
  assert not depth;body=text[start+6:end-1].strip()
  if re.search(r';\s*[×⋅]\|\d',body):out.append(body)
  offset=end
 return out

def repair_arithmetic(entity,attribute,before):
 example=json.loads((HERE/'arithmetic-sources.json').read_text())[str(entity)]['example'];data=json.loads((HERE/f'arithmetic-source-{example}.json').read_text());kind='example_question' if attribute=='question/problem' else 'example_explanation';section=next(s for s in data['sections'] if s['section_type']==kind);decls=blocks(section['readable_text']);spans=[m for m in MATH.finditer(before) if m[0].startswith('$$') and (r'\begin{' in m[0] or r'\lef' in m[0])];assert len(decls)==len(spans),(entity,attribute,len(decls),len(spans));after=before
 for match,body in reversed(list(zip(spans,decls))):after=after[:match.start()]+'$$\n'+source_multiplication_tex(body)+'\n$$'+after[match.end():]
 return normalize_math_boundaries(after)

def source_mathml_tables(example,attribute):
 from bs4 import BeautifulSoup
 from import_historical_question_content import Renderer
 soup=BeautifulSoup((HERE/f'arithmetic-source-{example}.html').read_text(),'html.parser');section=soup.find(class_='exampleQuestion' if attribute=='question/problem' else 'exampleExplanation');assert section is not None
 result=[]
 for math in section.find_all('math'):
  grid=next((t for t in math.find_all('mtable') if t.get('rowlines') and 'solid' in t['rowlines']),None)
  if grid is None:continue
  renderer=Renderer(None);rows=[]
  for row in grid.find_all('mtr',recursive=False):
   cells=[]
   for cell in row.find_all('mtd',recursive=False):
    tex=renderer.m(cell);tex=re.sub(r'\\[,!]|\s+', '',tex);tex=re.sub(r'\{\}_\{(\d)\}',lambda m:r'\scriptstyle '+m[1],tex);cells.append(tex)
   rows.append(cells)
  width=max(map(len,rows));assert all(len(r)==width for r in rows)
  keep=[i for i in range(width) if any(r[i].replace('{}','') for r in rows)];rows=[[r[i] for i in keep] for r in rows];rules=grid['rowlines'].split();parts=[]
  for i,row in enumerate(rows):
   parts.append(' & '.join(row))
   if i<len(rules) and rules[i]=='solid':parts[-1]+=r' \\ \hline'
   elif i<len(rows)-1:parts[-1]+=r' \\'
  tex=r'\begin{array}{'+'r'*len(keep)+'}'+''.join(parts)+r'\end{array}'
  outer=grid.find_parent('mtable')
  if outer:
   for cell in outer.find_all('mtd',recursive=False):pass
   for row in outer.find_all('mtr',recursive=False):
    for cell in row.find_all('mtd',recursive=False):
     if cell.find('mtable') is None:
      caption=renderer.m(cell).strip()
      if caption:tex+=r'\qquad '+caption
  assert not renderer.errors,renderer.errors
  result.append(tex)
 return result

# Use complete MathML tables when the old readable-text projection lost hidden
# cells or captions. The literal column parser remains the future-source fallback.
_readable_repair=repair_arithmetic
def repair_arithmetic(entity,attribute,before):
 example=json.loads((HERE/'arithmetic-sources.json').read_text())[str(entity)]['example']
 try:return _readable_repair(entity,attribute,before)
 except (ValueError,AssertionError):
  tex=source_mathml_tables(example,attribute);spans=[m for m in MATH.finditer(before) if m[0].startswith('$$') and (r'\begin{' in m[0] or r'\lef' in m[0])];assert len(tex)==len(spans),(entity,attribute,len(tex),len(spans));after=before
  for m,t in reversed(list(zip(spans,tex))):after=after[:m.start()]+'$$\n'+t+'\n$$'+after[m.end():]
  return normalize_math_boundaries(after)
