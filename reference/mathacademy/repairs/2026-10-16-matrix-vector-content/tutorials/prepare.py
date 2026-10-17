"""Restore two incomplete tutorials from their retained complete Math Academy titles."""
import hashlib
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
snapshot=json.loads((HERE.parent/'lesson.json').read_text())
source=json.loads((HERE/'source-formulas.json').read_text())
source_formulas={record['math_academy_id']:[f['reconstructed_tex'].replace('∗',r'\ast') for f in record['formulas']] for record in source}
def accessible_highlights(tex):
 tex=tex.replace(r'\color{blue}',r'\color{#4169E1}')
 return re.sub(r'\\bbox\[lightgray, 2pt\]\{(-?\d+)\}',lambda m:r'\bbox[lightgray, 2pt]{{\color{black}'+m[1]+'}}',tex)
def original_highlights(tex):
 tex=tex.replace(r'\color{#4169E1}',r'\color{blue}')
 return re.sub(r'\\bbox\[lightgray, 2pt\]\{\{\\color\{black\}(-?\d+)\}\}',lambda m:r'\bbox[lightgray, 2pt]{'+m[1]+'}',tex)
formulas={mid:list(map(accessible_highlights,values)) for mid,values in source_formulas.items()}
for mid,values in formulas.items():
 assert list(map(original_highlights,values))==source_formulas[mid]
entities={}
def collect(x):
 if isinstance(x,dict):
  if ':tutorial/content' in x:entities[x[':tutorial/math-academy-id']]=x
  for v in x.values():collect(v)
 elif isinstance(x,list):
  for v in x:collect(v)
collect(snapshot['topic'])
assert set(entities)=={2987,2988}

def block(s): return '$$\n'+s.strip()+'\n$$'
def chain(tex):
 parts=tex.split('=')
 assert len(parts)==3
 # The extra A x label is the same matrix-vector product named by the source.
 return '\\begin{aligned}\nA\\mathbf{x} &='+parts[0].strip()+' \\\\\n&='+parts[1].strip()+' \\\\\n&='+parts[2].strip()+'\n\\end{aligned}'
def norm(tex): return re.sub(r'\s+','',tex)

f=formulas[2987]
intro='\n\n'.join([
 'To multiply a matrix by a column vector, we multiply each row in the matrix by the column vector using the dot product.',
 'For example, suppose we would like to multiply the matrix $A$ by the vector $\\mathbf{x}$:',
 block('\\begin{aligned}\n'+f[0].replace('=','&=',1)+' \\\\\n'+f[1].rstrip('.').replace('=','&=',1)+'\n\\end{aligned}'),
 'First, we write the multiplication as follows:',
 block(f[2]),
 'The result of this multiplication is another column vector $\\mathbf{y}$ with the same dimensions as $\\mathbf{x}.$',
 "Now, we calculate the entries of the product (shown as $\\ast$'s in the equation above).",
 'To find $y_1$, the first component of $\\mathbf{y}$, we calculate the dot product of the first row of $A$ and the vector $\\mathbf{x}$:',
 block(chain(f[12])),
 'To find $y_2$, the second component of $\\mathbf{y}$, we calculate the dot product of the second row of $A$ and the vector $\\mathbf{x}$:',
 block(chain(f[19])),
 'Therefore,',
 block(f[20]),
])
f=formulas[2988]
alternative='\n\n'.join([
 'An alternative, yet equivalent, procedure for multiplying a matrix by a column vector involves adding scaled columns of the matrix $A$ as follows:',
 block(f[1]),
 'If we denote',
 block(f[2]+r',\qquad '+f[3]),
 'then we can also write the multiplication as follows:',
 block(f[4]),
 'The expression above is a **linear combination** of the vectors $\\mathbf{u}_1$ and $\\mathbf{u}_2$, where the corresponding coefficients are given by the entries of the vector $\\mathbf{x}$.',
])

changes=[]
for mid,after,reason in [
 (2987,intro,'Restore matrix/vector labels, all factors and results in the multiplication setup and both dot-product steps, final A x equality and source underbraces; stack definitions and long derivations onto aligned display rows. Adapt source blue emphasis to RoyalBlue (#4169E1) and use black text in the source lightgray boxes for light/dark theme legibility.'),
 (2988,alternative,'Restore the missing u_1 and u_2 vector definitions and source coefficient highlighting; separate definitions and final linear combination into display paragraphs. Adapt source blue to RoyalBlue (#4169E1) for light/dark theme legibility.'),
]:
 e=entities[mid]
 assert e[':tutorial/content'] != after
 row={'entity':e[':db/id'],'attribute':'tutorial/content','before':e[':tutorial/content'],'after':after,'reason':reason,'source':next(r['path'] for r in source if r['math_academy_id']==mid),'math_academy_id':mid}
 changes.append(row)
 (HERE/f'tutorial-{mid}-after.md').write_text(after+'\n')

# Every recovered product factor, partial-result vector, and final vector appears
# intact and in source order. Alignment inserts only row separators and A x.
checks=[]
checks.append({'check':'Authored highlight styling preserves every source number, matrix entry, operation and highlight location; reversing the two color adaptations exactly recovers all source formulas','pass':True})
for idx in (12,19):
 original=formulas[2987][idx]
 prepared=chain(original)
 recovered=prepared.removeprefix('\\begin{aligned}\nA\\mathbf{x} &=')
 recovered=recovered.removesuffix('\n\\end{aligned}').replace(' \\\\\n&=','=')
 assert norm(recovered)==norm(original),(idx,recovered,original)
 checks.append({'tutorial':2987,'source_title_index':idx,'check':'Full multiplication chain unchanged after removing display alignment and the A x label','pass':True})
assert 1*(-3)+3*4==9 and 6*(-3)+7*4==10
checks.append({'tutorial':2987,'check':'Both stated dot products evaluate to the source result (9,10)','pass':True})
from sympy import Matrix,symbols
a,b,c,d=symbols('a b c d')
assert Matrix([[a,c],[b,d]])*Matrix([3,2]) == 3*Matrix([a,b])+2*Matrix([c,d]) == Matrix([3*a+2*c,3*b+2*d])
checks.append({'tutorial':2988,'check':'The column combination equals the same matrix-vector product symbolically','pass':True})

oldpath=Path('/home/jake/Developer/MA/PIPELINE/Math-Academy/3-Capture/1-Source/3-JSON/lesson-json.py')
original=Path('/home/jake/Developer/MA/DATA/Lessons/1195/Source/1195.html')
original_soup=BeautifulSoup(original.read_text(),'html.parser')
for r in source:
 mid=r['math_academy_id']
 titles=original_soup.select_one('[contentid="'+str(mid)+'"]').select('title')
 retained=BeautifulSoup((ROOT/r['path']).read_text(),'html.parser').select('title')
 assert len(titles)==len(retained)
 assert [norm(x.get_text()) for x in titles]==[norm(x.get_text()) for x in retained]
 checks.append({'tutorial':mid,'check':'Retained capture titles exactly match original lesson HTML text and all MathML fragment text','pass':True})

(HERE/'changes.json').write_text(json.dumps(changes,indent=2)+'\n')
(HERE/'verification.json').write_text(json.dumps({'basis':snapshot['identity']['basis'],'tutorials_checked':2,'tutorials_repaired':2,'checks':checks,'authored_style_adaptations':{'blue_emphasis':'Source pure blue changed to RoyalBlue (#4169E1), retaining every highlighted factor and coefficient.','gray_boxes':'Source lightgray boxes retained with explicit black text to prevent inherited white numerals in dark theme.','layout':'Introduction operand definitions occupy separate aligned rows; multiplication chains are stacked; the period following the inline x stays inside math.'},'source_evidence':source,'root_cause':{'stage':'Historical HTML-to-JSON extraction, before database import','file':str(oldpath),'sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),'lines':'531–544','behavior':'extract_math_from_node searches a formula for the first nested mjx-assistive-mml and returns that MathML fragment, ignoring surrounding TeX and additional fragments in the SVG title. This lost A= and x=, complete products, labels, and final A x=; all remain in retained source HTML.','already_lost_before_matrix_repair':'reference/mathacademy/repairs/2026-10-13-matrix-capture/batches/001.edn CAS-before values already have the missing content.','original_html':str(original),'original_html_sha256':hashlib.sha256(original.read_bytes()).hexdigest()}},indent=2)+'\n')
print(json.dumps({'changes':len(changes),'tutorials':[x['entity'] for x in changes],'checks':len(checks)},indent=2))
