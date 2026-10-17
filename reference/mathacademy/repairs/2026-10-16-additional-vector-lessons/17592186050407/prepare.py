"""Source-backed content and display proposals. Never transacts EDB."""
import hashlib,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import MATH,cells,matrix_answer,matrix_operands,normalize_tex,validate_prose
from layout import MATRIX,block,compact,highlight,operands,entry_solution,matrix_table_solution
snap=json.loads((HERE/'lesson.json').read_text())
source=json.loads((HERE/'source/tutorial-formulas.json').read_text())
f={r['mid']:[x['tex'] for x in r['formulas']] for r in source}
CAPTURE=ROOT/'reference/mathacademy/question-capture/13989257'
WORKER=ROOT/'reference/mathacademy/question-capture-workers/linear/14043519'
entities={}
def collect(v):
 if isinstance(v,dict):
  if ':db/id' in v:entities.setdefault(v[':db/id'],{}).update(v)
  for a in v.values():collect(a)
 elif isinstance(v,list):
  for a in v:collect(a)
collect(snap['topic'])
changes=[];checks=[];reviews=[]
def add(e,a,after,reason,evidence=None):
 before=entities[e][a]
 after=after.strip()
 if before==after:return
 validate_prose(after)
 changes.append({'entity':e,'attribute':a,'before':before,'after':after,'reason':reason,'source_proof':evidence or {}})

def matrices(text):
 return [cells(m[0][len(r'\begin{bmatrix}'):-len(r'\end{bmatrix}')]) for m in MATRIX.finditer(text)]
def simple_matrix(rows):return sp.Matrix([[sp.sympify(c.strip().replace('{','').replace('}','')) for c in row] for row in rows])
def tokens(tex):return re.sub(r'\s+','',tex)
def source_proof(mid):
 p=CAPTURE/(f'tutorial-{mid}.html' if mid in (2993,2994) else f'example-{mid}.json')
 return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

# Introduction: restore full source titles, remove actual TeX comments, then reflow.
a=f[2993]
setup=a[5].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
left,right=setup.split('&=');setup=r'\begin{aligned}&'+left.strip()+r' \\ &='+right.strip()+r'\end{aligned}'
intro=[
 'When multiplying two matrices in general, we apply the same approach as usual:',
 '- First, we verify that the two matrices are conformable for multiplication.\n- Then, we multiply each row in the first matrix by each column in the second.',
 "For example, let's find $AB$, where",
 matrix_operands([compact(a[1]),compact(a[2])],stacked=True),
 'First, we verify the conformability for multiplication:',block(highlight(a[3])),
 "So the matrices are conformable for multiplication, and the product is a $2 \\times 2$ matrix. Let's set up the multiplication:",
 block(setup),
 "Now, we calculate the entries of the product matrix (shown as $\\ast$'s in the equation above).",
]
for index,caption in [
 (14,'To find $c_{11}$, the entry at the intersection of the first row and first column, we calculate the dot product of the first row of $A$ and the first column of $B$:'),
 (20,'To find $c_{12}$, we calculate the dot product of the first row of $A$ and the second column of $B$:'),
 (26,'To find $c_{21}$, we calculate the dot product of the second row of $A$ and the first column of $B$:'),
 (32,'Finally, to find $c_{22}$, we calculate the dot product of the second row of $A$ and the second column of $B$:'),
]:
 intro.extend([caption,highlight(matrix_table_solution(a[index]))])
intro.extend(['Therefore, we have',block(a[33])])
add(17592186101959,':tutorial/content','\n\n'.join(intro),'Restore missing B= and final AB= from complete source titles; remove source-only TeX comments that were mistakenly escaped into visible math; retain every matrix and dot-product term while stacking matrix products and entry calculations. Adapt source highlight colors and black-on-gray boxed text for theme legibility.',source_proof(2993))

before=entities[17592186101960][':tutorial/content'];old=MATH.findall(before)[-1]
parts=f[2994][12].split('=');assert len(parts)==3
expanded=parts[2].strip();terms=expanded.split('+');assert len(terms)==4
restored=r'\begin{aligned}'+parts[0].strip()+' &='+parts[1].strip()+r' \\ &='+'+'.join(terms[:2])+r' \\ &\quad +'+'+'.join(terms[2:])+r'\end{aligned}'
add(17592186101960,':tutorial/content',highlight(before.replace(old,block(restored))),'Restore scalar entry label, column vector, and complete dot-product expansion omitted by first-fragment extraction; reflow expansion and preserve source index-color relationships.',source_proof(2994))

entry_ids=set();canonical_ids=set();practice=[];answer_layouts=[]
for kp in snap['topic'][':topic/knowledge-points']:
 ex=kp[':knowledge-point/canonical-example'];canonical_ids.add(ex[':db/id'])
 if kp[':db/id']==17592186100873:entry_ids.update(q[':db/id'] for q in [ex]+kp[':knowledge-point/questions'])
 for q in [ex]+kp[':knowledge-point/questions']:
  eid=q[':db/id'];mid=q.get(':question/math-academy-id');before=q[':question/problem'];after=operands(before)
  evidence={'matrix_operands_unchanged':matrices(before)==matrices(after)}
  assert evidence['matrix_operands_unchanged']
  if eid in canonical_ids:evidence.update(source_proof(int(mid[2:])))
  reason='Group each labelled matrix operand into its own responsive row, retaining all operand values and labels.'
  if '| ---' in before:
   p=next(p for p in [CAPTURE/f'{mid}-before.json',WORKER/f'{mid}-before.json'] if p.exists())
   captured=json.loads(p.read_text());soup=BeautifulSoup(captured['html'],'html.parser')
   table=next(t for t in soup.select('table') if t.select('[id^=freeResponseTextbox]'))
   srcfields={v['dom_id']:v['key'] for v in captured['fields']}
   rows=[];mapping=[];label=None
   for rowidx,tr in enumerate(table.select('tbody > tr'),1):
    row=[]
    for td in tr.find_all('td',recursive=False):
     field=td.select_one('[id^=freeResponseTextbox]')
     if field:
      key=srcfields[field['id']];row.append('{{'+key+'}}');mapping.append({'row':rowidx,'column':len(row),'field_key':key,'source_dom_id':field['id']})
     else:
      math=td.select_one('math')
      if math:
       value=math.get_text().replace('−','-').strip()
       if '=' in value:label=value.split('=')[0].strip()
       else:assert re.fullmatch(r'-?\d+',value),value;row.append(value)
    rows.append(row)
   assert label and rows and len(set(map(len,rows)))==1
   keys=re.findall(r'\{\{([^{}]+)\}\}',before)
   assert keys==[m['field_key'] for m in mapping]
   prefix,_=after.split('\n\n|',1)
   after=prefix+'\n\n'+matrix_answer(label,rows)
   assert re.findall(r'\{\{([^{}]+)\}\}',after)==keys
   assert set(keys)=={x[':answer-field/key'] for x in q[':question/answer-fields']}
   evidence.update({'source':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_answer_table_html':str(table),'source_rows':rows,'source_mapping':mapping,'label':label})
   reason+=' Restore source answer-matrix cell placement, supplied entries and exterior brackets with matrix_answer; retain every field key and order.'
   answer_layouts.append(eid)
  add(eid,':question/problem',after,reason,evidence)
  solution=q.get(':question/worked-solution')
  if eid in entry_ids and solution:
   after_solution=entry_solution(solution,before)
   assert matrices(solution)==matrices(after_solution)
   filename=f'example-{mid[2:]}.json' if mid.startswith('e-') else f'history-{mid}.json'
   provenance=next(p for p in (CAPTURE/filename,WORKER/filename) if p.exists())
   add(eid,':question/worked-solution',after_solution,'Correct source-level scalar-versus-matrix notation: present the full matrix product separately under its uppercase matrix label, then begin the scalar entry chain at the selected row/column dot product. Preserve every matrix factor and subsequent calculation.',{'source_level_notation_correction':True,'matrix_inventory_unchanged':True,'source':str(provenance.relative_to(ROOT)),'source_sha256':hashlib.sha256(provenance.read_bytes()).hexdigest()})
  if eid not in canonical_ids:practice.append(q)

# Source-complete canonical examples still benefit from readable display spacing.
ex=entities[17592186100694];solution=ex[':question/worked-solution']
wide=next(m[0] for m in MATH.finditer(solution) if r' &  & ' in m[0])
reflow=matrix_table_solution(wide.strip('$').strip())
assert matrices(wide)==matrices(reflow)
add(ex[':db/id'],':question/worked-solution',highlight(solution.replace(wide,reflow)),'Stack the four source matrix products and dot-product calculations, preserving all factors, partial matrices and final result; use explicit black text inside gray dimension boxes.',source_proof(4406))
ex=entities[17592186100741]
prompt=ex[':question/problem'];math=MATH.findall(prompt)[0]
add(ex[':db/id'],':question/problem','Compute the product\n\n'+block(compact(math.strip('$').strip())),'Show the complete source outer product as a display equation with canonical brackets.',source_proof(5885))
solution=ex[':question/worked-solution'];span=next(m for m in MATH.finditer(solution) if r'\begin{aligned}' in m[0]);tex=span[0].strip('$').strip();inner=tex.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
rows=cells(inner);assert len(rows)==2 and len(rows[0])==2
assert rows[1][0]=='[5pt]'
rows[1][0]=''
rows=[[ '',rows[0][0] ],['',rows[0][1]],*rows[1:]]
reflow=r'\begin{aligned}'+r' \\ '.join(' & '.join(row) for row in rows)+r'\end{aligned}'
assert matrices(tex)==matrices(reflow)
add(ex[':db/id'],':question/worked-solution',highlight(solution[:span.start()]+block(reflow)+solution[span.end():]),'Stack the source outer product, expanded entry products and final matrix on separate display rows; preserve all six scalar products and dimension information.',source_proof(5885))

# No duplicate field changes; preserve all unchanged metadata and missing solutions.
assert len({(c['entity'],c['attribute']) for c in changes})==len(changes)
assert len(practice)==34 and len(answer_layouts)==8
for c in changes:
 if c['attribute']==':question/problem':
  assert matrices(c['before'])==matrices(c['after'])
  assert re.findall(r'\{\{[^{}]+\}\}',c['before'])==re.findall(r'\{\{[^{}]+\}\}',c['after'])

# Verify all operands and all present mathematical results, including undefined products.
for q in [entities[e] for e in canonical_ids]+practice:
 mats=matrices(q[':question/problem']);assert len(mats)==2,q[':db/id']
 A,B=map(simple_matrix,mats);defined=A.cols==B.rows
 sol=q.get(':question/worked-solution');result=A*B if defined else None
 detail={'entity':q[':db/id'],'ma_id':q[':question/math-academy-id'],'operand_shapes':[list(A.shape),list(B.shape)],'product_defined':defined,'solution_present':bool(sol),'missing_solution_deferred':not bool(sol)}
 if sol:
  if defined and q[':db/id'] in entry_ids:
   match=re.search(r'\$\{?([a-z])\}?_\{(\d)(\d)\}',q[':question/problem']);assert match,q[':question/problem']
   value=result[int(match[2])-1,int(match[3])-1]
   last=re.search(r'&\s*=\s*(-?\d+)\.?(?:\\end\{aligned\})',sol);assert last,(q[':db/id'],sol)
   assert int(last[1])==value,(q[':db/id'],last[1],value)
   detail['result']=str(value)
  elif defined:
   last=simple_matrix(matrices(sol)[-1]);assert result==last,(q[':db/id'],result,last)
   detail['result']=[list(map(str,row)) for row in result.tolist()]
  else:assert 'not' in sol.lower() or 'undefined' in sol.lower();detail['result']='undefined'
  detail['existing_solution_result_verified']=True
 reviews.append(detail)

(HERE/'changes.json').write_text(json.dumps(changes,indent=2)+'\n')
(HERE/'review.json').write_text(json.dumps({'identity':snap['identity'],'topic':17592186050407,'title':snap['topic'][':topic/title'],'tutorial_count':2,'canonical_example_count':3,'practice_count':34,'existing_solutions_reviewed':sum(bool(q.get(':question/worked-solution')) for q in practice)+3,'missing_solutions_deferred':sum(not bool(q.get(':question/worked-solution')) for q in practice),'answer_matrix_repairs':answer_layouts,'source_level_notation_repairs':[c['entity'] for c in changes if c['source_proof'].get('source_level_notation_correction')],'changes':len(changes),'source_cause':'Old lesson-json.py selected only first nested MathML in mixed SVG titles; pure-TeX comment lines were escaped as visible percent notation rather than omitted. Source e4407 and related practice additionally present scalar entry as equal to whole matrix product; this is corrected explicitly as source-level notation.','authored_style_adaptations':'Pure blue→RoyalBlue #4169E1; faint lightgray inactive entries→gray; green dimension cue→#2E8B57; explicit black text inside lightgray boxes. All highlight locations retained.','questions':reviews},indent=2)+'\n')
print(json.dumps({'changes':len(changes),'answer_matrix_repairs':len(answer_layouts),'questions_reviewed':len(reviews)},indent=2))
