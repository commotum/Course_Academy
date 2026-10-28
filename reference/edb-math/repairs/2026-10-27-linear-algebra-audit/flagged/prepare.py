import copy,json,re,shutil,sys
from pathlib import Path
import sympy as S
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));sys.path.insert(0,str(H))
from question_capture.math_format import ENV,environment,cells,matrix_answer,validate_prose
from product_highlights import product_solution

def grids(t):
 return [cells(t[span[0]:span[1]]) for m in ENV.finditer(t) if m.groups()==('begin','bmatrix') for span in [environment(t,m.start())]]
def integers(t):return [[int(c.strip()) for c in row]for row in t]
qs=json.loads((H/'kp-questions.json').read_text());changes=[];checks=[]
for q in qs:
 p=q[':question/problem'];g=grids(p);assert len(g)==2,q[':db/id'];a,b=map(integers,g);c=[list(map(int,row))for row in (S.Matrix(a)*S.Matrix(b)).tolist()];names=re.findall(r'([A-Z])\s*=\s*\\begin\{bmatrix\}',p);assert len(names)==2,(q[':db/id'],names)
 if 'matrix-answer'in p:
  rows=re.findall(r'<tr>(.*?)</tr>',p,re.S);targets=[]
  for i,row in enumerate(rows):
   for j,cell in enumerate(re.findall(r'<td>(.*?)</td>',row,re.S)):
    if '{{' in cell:targets.append([i,j])
    else:assert int(cell.strip('$ '))==c[i][j],(q[':db/id'],i,j,cell,c)
 else:targets=[[i,j]for i in range(len(c))for j in range(len(c[0]))]
 # Source q318413 retained old decorative table: two fields in a 1x2 result.
 if q[':db/id']==17592186602444:
  keys=re.findall(r'\{\{([^{}]+)\}\}',p);assert keys==['field-1','field-2'];targets=[[0,0],[0,1]]
  after=p[:p.index('<table')]+matrix_answer('AB',[['{{'+k+'}}'for k in keys]])
  changes.append({'entity':q[':db/id'],'attribute':'question/problem','before':p,'after':after,'reason':'replace decorative source HTML cells with canonical bracketed matrix input preserving both existing field keys','evidence':'legacy source HTML table has label and blank bracket spacer cells, not data; exact 1x2 product and existing correct fields independently verified','confidence':'high'})
 # Verify existing answer bank against independent product, preserving identities.
 fs=q.get(':question/answer-fields',[])
 if fs and '{{' not in p:
  f=fs[0];matches=[v for v in f[':answer-field/choices']if len(grids(v[':answer/value']))==1 and integers(grids(v[':answer/value'])[0])==c];assert len(matches)==1,(q[':db/id'],c)
  if ':answer-field/correct'in f:assert f[':answer-field/correct'][':db/id']==matches[0][':db/id']
 elif fs:
  keys=re.findall(r'\{\{([^{}]+)\}\}',p);bykey={f[':answer-field/key']:f for f in fs};assert len(targets)==len(keys)
  for pos,key in zip(targets,keys):assert int(next(v[':answer/value']for v in bykey[key][':answer-field/choices']if v[':db/id']==bykey[key][':answer-field/correct'][':db/id']))==c[pos[0]][pos[1]],(q[':db/id'],key)
 before=q.get(':question/worked-solution')
 if before:
  after=product_solution(a,b,names,targets);validate_prose(after)
  changes.append({'entity':q[':db/id'],'attribute':'question/worked-solution','before':before,'after':after,'reason':'restore instructional row/column/result focus and responsive stages using tutorial2993 convention; correct inconsistent operand/mask wherever present','evidence':'tutorial17592186101959 row blue, column red, current cell emphasized; independently calculated every target dot product, final product, and existing bank; this is an authored presentation repair, not asserted original question color recovery','confidence':'high'})
 checks.append({'entity':q[':db/id'],'names':names,'A':a,'B':b,'product':c,'targets':targets,'key_verified':True if before else 'completion delegated'})
(H/'proposals.json').write_text(json.dumps(changes,indent=2)+'\n');(H/'math-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
old=Path('/media/jake/SSD/EDB/math/generators/c6/c62b54d8ef950438382d6e06550ade42523c5f1bc54c398a1b10b760c2b35b64');manifest=json.loads((old/'generator-package.json').read_text());stage=H/'generator';stage.mkdir(exist_ok=True)
for f in manifest['files']:shutil.copyfile(old/f,stage/f)
shutil.copyfile(H/'product_highlights.py',stage/'product_highlights.py');shutil.copyfile(R/'scripts/question_capture/math_format.py',stage/'math_format.py')
p=stage/'generator.py';s=p.read_text().replace('VERSION=\'4697-matrix-product-2\'','VERSION=\'9047-matrix-product-highlights-3\'').replace('import math_format as mf','import math_format as mf\nfrom product_highlights import product_solution');needle=" if s['solution_template']:\n";assert s.count(needle)==1;s=s.replace(needle," if not raw:\n  return product_solution(a,b,s['names'],t),slots\n"+needle);p.write_text(s)
(stage/'repair-evidence.json').write_text(json.dumps({'basis_t':9047,'tutorial':17592186101959,'reason':'Authored source-tutorial teaching convention: blue active row, red active column, emphasized result, explicit accessible entry labels. Raw source replay remains unchanged. Arithmetic, banks, targets and parameter domains unchanged.','source_limit':'q129497 raw capture not found; no claim colors recovered from unavailable source.'},indent=2)+'\n')
(H/'generator-candidates.json').write_text(json.dumps([{'kp':17592186100872,'old_reference':'generators/c6/c62b54d8ef950438382d6e06550ade42523c5f1bc54c398a1b10b760c2b35b64/generator.py','directory':str(stage.resolve()),'entrypoint':'generator.py','files':sorted([*manifest['files'],'product_highlights.py','repair-evidence.json']),'dependencies':manifest['dependencies']}],indent=2)+'\n')
print('Staged',len(changes),'changes and one replacement generator; verified',len(checks),'products.')
