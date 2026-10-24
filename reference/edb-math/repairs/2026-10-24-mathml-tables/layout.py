"""Match table cells independently of formatting; preserve their current bytes."""
import json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'))
from math_format import cells,environment,mathml_ruled_table
FENCES={'bmatrix':('[',']'),'pmatrix':('(',')'),'Bmatrix':(r'\{',r'\}'),'vmatrix':('|','|'),'Vmatrix':(r'\Vert',r'\Vert')}
def key_cell(text):
 s=re.sub(r'\\(?:displaystyle|textstyle)|\\hline|\\left|\\right|\\[,!]','',text)
 s=re.sub(r'\\begin\{array\}\{[^{}]*\}',r'\\begin{TABLE}',s)
 for env in ['aligned','matrix','array',*FENCES]:
  f=FENCES.get(env,('',''))
  s=s.replace('\\begin{'+env+'}',f[0]+r'\begin{TABLE}').replace('\\end{'+env+'}',r'\end{TABLE}'+f[1])
 s=re.sub(r'\{([A-Za-z0-9])\}(?=[_^])',r'\1',s)
 s=s.replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac')
 return re.sub(r'\s+','',s)
def grid_key(rows):
 clean=list(rows)
 if clean and all(not key_cell(c) for c in clean[-1]) and any(r'\hline' in c for c in clean[-1]):clean.pop()
 return tuple(tuple(key_cell(c) for c in row) for row in clean)
def expected_layout(source):
 a=source['source_attributes'];rows=source['rows'];placeholder=[[str(i)+'Z'+str(j) for j in range(len(r))] for i,r in enumerate(rows)];tex=mathml_ruled_table(placeholder,a)
 return tex

def array_with_current_cells(rows,attrs):return mathml_ruled_table(rows,attrs)

def changed_tex(span,source):
 tex=array_with_current_cells(span['rows'],source['source_attributes'])
 if span['env'] in FENCES:
  f=source.get('source_fences')
  if f is None:raise ValueError('Need source fence evidence')
  if f:tex=r'\left'+f[0]+tex+r'\right'+f[1]
 return tex
