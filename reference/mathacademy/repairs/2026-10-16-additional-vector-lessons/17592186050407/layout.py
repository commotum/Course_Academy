"""Scoped display changes for the source-verified matrix multiplication lesson."""
import re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import MATH,cells,matrix_operands,normalize_tex
MATRIX=re.compile(r'\\begin\{bmatrix\}[\s\S]*?\\end\{bmatrix\}')
DEFINITION=re.compile(r'([A-Z])\s*=\s*(\\begin\{bmatrix\}[\s\S]*?\\end\{bmatrix\})')
def compact(tex):return re.sub(r'\s+',' ',tex).strip()
def block(tex):return '$$\n'+tex.strip()+'\n$$'
def highlight(tex):
 tex=tex.replace(r'\color{blue}',r'\color{#4169E1}').replace(r'\color{lightgray}',r'\color{gray}').replace(r'\color{green}',r'\color{#2E8B57}')
 return re.sub(r'\\bbox\[lightgray, 2pt\]\{(-?\d+)\}',lambda m:r'\bbox[lightgray, 2pt]{{\color{black}'+m[1]+'}}',tex)
def operands(text):
 matches=[]
 for span in MATH.finditer(text):
  for definition in DEFINITION.finditer(span[0]):matches.append((span,definition))
 if len(matches)!=2:return text
 first,last=matches[0][0],matches[-1][0]
 middle=text[first.start():last.end()]
 # Between the mathematical definitions only the source conjunction is allowed.
 residual=MATH.sub('',middle).strip()
 assert not residual or residual=='and',residual
 values=[compact(m[1][1]+'='+m[1][2]) for m in matches]
 tail=last[0].strip('$').strip()
 punctuation=re.search(r'([.?,])\s*$',tail)
 if punctuation:values[-1]+=punctuation[1]
 return text[:first.start()].rstrip()+'\n\n'+matrix_operands(values,stacked=True)+'\n\n'+text[last.end():].lstrip()
def entry_solution(solution,problem):
 product=re.search(r'Let\s+\$([A-Z])\s*=',problem)
 assert product,problem
 spans=[m for m in MATH.finditer(solution) if r'\begin{aligned}' in m[0]]
 assert len(spans)==1
 span=spans[0];tex=span[0].strip('$').strip()
 assert tex.startswith(r'\begin{aligned}') and tex.endswith(r'\end{aligned}')
 rows=cells(tex[len(r'\begin{aligned}'):-len(r'\end{aligned}')]);assert len(rows)>=3
 scalar,full=rows[0];assert full.startswith('=') and len(MATRIX.findall(full))==2
 assert rows[1][0]=='' and rows[1][1].startswith('=')
 rows[1][0]=scalar
 selected=r'\begin{aligned}'+r' \\ '.join(' & '.join(r) for r in rows[1:])+r'\end{aligned}'
 product_display=block(product[1]+full)
 return 'The full matrix product is\n\n'+product_display+'\n\n'+solution[:span.start()]+block(selected)+solution[span.end():]
def matrix_table_solution(tex):
 """Stack wide source matrix-product/entry-calculation pairs without losing terms."""
 inner=tex.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
 rows=cells(inner);assert rows
 blocks=[]
 for row in rows:
  significant=[s for s in row if s.strip()]
  assert len(significant)==2,significant
  chain,dot=significant
  parts=chain.rstrip(',').split('=');assert len(parts)==2
  blocks.append(block(r'\begin{aligned}&'+parts[0].strip()+r' \\ &='+parts[1].strip()+r'\end{aligned}'))
  blocks.append(block(dot.strip().removeprefix(r'\,').removeprefix(r'\quad').strip()))
 return '\n\n'.join(blocks)
