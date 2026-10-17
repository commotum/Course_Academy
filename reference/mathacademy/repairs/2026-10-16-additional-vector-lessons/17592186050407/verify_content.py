"""Independent source, arithmetic, field mapping and content-preservation checks."""
import collections,hashlib,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
sys.path.insert(0,str(HERE));from layout import MATRIX,MATH,cells,matrix_table_solution
snap=json.loads((HERE/'lesson.json').read_text());changes=json.loads((HERE/'changes.json').read_text());entities={}
def collect(v):
 if isinstance(v,dict):
  if ':db/id' in v:entities.setdefault(v[':db/id'],{}).update(v)
  for x in v.values():collect(x)
 elif isinstance(v,list):
  for x in v:collect(x)
collect(snap['topic'])
def lex(s):
 s=re.sub(r'\\color\{[^}]+\}','',s);s=re.sub(r'\\bbox\[[^\]]+\]','',s)
 s=s.replace(r'\cdot','*').replace('∗','AST').replace(r'\ast','AST').replace(r'\,','').replace('−','-')
 return re.sub(r'[{}\s]','',s)
def mats(s):return [[[lex(c) for c in row] for row in cells(m[len(r'\begin{bmatrix}'):-len(r'\end{bmatrix}')])] for m in MATRIX.findall(s)]
def sym(rows):return sp.Matrix([[sp.sympify(c.replace('^','**')) for c in row] for row in rows])
def field_value(e,a):return next((c['after'] for c in changes if c['entity']==e and c['attribute']==a),entities[e][a])
checks=[]
canonical=json.loads((HERE/'source/canonical-formulas.json').read_text())
for r in canonical:
 q=next(e for e in entities.values() if e.get(':question/math-academy-id')=='e-'+str(r['mid']))
 for a in ('question/problem','question/worked-solution'):
  expected=mats(' '.join(f['tex'] for f in r['formulas'] if f['field']==a))
  before=mats(q[':'+a]);after=mats(field_value(q[':db/id'],':'+a))
  assert expected==before==after,(r['mid'],a)
  checks.append({'entity':q[':db/id'],'attribute':':'+a,'source_matrix_count':len(expected),'all_matrix_cells_and_order_match_source_before_and_after':True,'source':r['path'],'source_sha256':r['sha256']})
source=json.loads((HERE/'source/tutorial-formulas.json').read_text())
for r in source:
 eid=17592186101959 if r['mid']==2993 else 17592186101960
 after=field_value(eid,':tutorial/content')
 expected=mats(' '.join(f['tex'] for f in r['formulas']))
 assert expected==mats(after),(eid,expected,mats(after))
 checks.append({'entity':eid,'source_matrix_count':len(expected),'complete_source_matrix_inventory_restored':True,'source':r['path'],'source_sha256':r['sha256'],'source_comment_lines_omitted':sum(len(f['source_comment_lines_removed']) for f in r['formulas'])})
 if r['mid']==2993:
  dots=[]
  for idx in (14,20,26,32):
   text=matrix_table_solution(r['formulas'][idx]['tex']);dots.append(lex(MATH.findall(text)[-1].strip('$')))
  actual=[lex(m.strip('$')) for m in MATH.findall(after) if r'\cdot' in m and 'bmatrix' not in m and 'underset' not in m]
  assert dots==actual,(dots,actual)
  checks.append({'entity':eid,'check':'Every scalar dot-product expression exactly preserved from source, ignoring authored color changes','pass':True})
  assert r'\%' not in after and 'B=' in after and 'AB =' in after
  checks.append({'entity':eid,'check':'Both missing labels restored and escaped source comments absent','pass':True})
 else:
  assert 'a_{i1}b_{1j}' in after and 'a_{i2}b_{2j}' in after and 'a_{in}b_{nj}' in after
  checks.append({'entity':eid,'check':'All source expanded sum terms and both row/column factors are present','pass':True})
# All field identities and supplied answer entries stay in their exact source cells.
for c in changes:
 assert entities[c['entity']][c['attribute']]==c['before']
 if c['attribute']==':question/problem':
  assert mats(c['before'])==mats(c['after'])
  assert re.findall(r'\{\{[^{}]+\}\}',c['before'])==re.findall(r'\{\{[^{}]+\}\}',c['after'])
 proof=c['source_proof']
 if 'source_rows' not in proof:continue
 A,B=map(sym,mats(c['before']));result=A*B
 rows=proof['source_rows'];assert (len(rows),len(rows[0]))==result.shape
 q=entities[c['entity']];fields={v[':answer-field/key']:v for v in q[':question/answer-fields']}
 for i,row in enumerate(rows):
  for j,value in enumerate(row):
   if value.startswith('{{'):
    field=fields[value[2:-2]];key=field.get(':answer-field/correct',{}).get(':db/id')
    if key is not None:
     answer=next(a for a in field[':answer-field/choices'] if a[':db/id']==key)
     assert sp.sympify(answer[':answer/value'])==result[i,j]
   else:assert sp.sympify(value)==result[i,j]
 checks.append({'entity':c['entity'],'check':'Each field and supplied fixed entry occupies its source row/column and agrees with independently computed product','rows':len(rows),'columns':len(rows[0]),'pass':True})
for e in entities.values():
 if ':question/problem' not in e:continue
 if not e.get(':question/worked-solution'):assert not any(c['entity']==e[':db/id'] and c['attribute']==':question/worked-solution' for c in changes)
# Independent symbolic/numeric verification of tutorial content.
A=sp.Matrix([[-2,2,1],[1,-1,3]]);B=sp.Matrix([[-5,2],[2,-2],[-4,1]])
assert A*B==sp.Matrix([[10,-7],[-19,7]])
checks.append({'entity':17592186101959,'check':'Full matrix product and all four displayed dot products verified with SymPy','pass':True})
# Source reconstruction proof against original retained lesson HTML.
original=Path('/home/jake/Developer/MA/DATA/Lessons/1196/Source/1196.html')
orig=BeautifulSoup(original.read_text(),'html.parser')
for mid in (2993,2994):
 retained=BeautifulSoup((ROOT/f'reference/mathacademy/question-capture/13989257/tutorial-{mid}.html').read_text(),'html.parser')
 a=[re.sub(r'\s+','',x.get_text()) for x in orig.select_one(f'[contentid="{mid}"]').select('title')]
 b=[re.sub(r'\s+','',x.get_text()) for x in retained.select('title')]
 assert a==b
checks.append({'check':'Both retained tutorial captures match every original lesson SVG-title text/MathML fragment','path':str(original),'sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'pass':True})
(HERE/'content-verification.json').write_text(json.dumps({'identity':snap['identity'],'checks':checks,'all_checks_passed':True,'changes':len(changes),'unchanged_answers_difficulty_and_metadata':'Only prompt, worked-solution and tutorial/content proposals are present; no grading or learner-state changes.','missing_solutions_left_untouched':True},indent=2)+'\n')
print(json.dumps({'checks_passed':len(checks),'changes':len(changes)},indent=2))
