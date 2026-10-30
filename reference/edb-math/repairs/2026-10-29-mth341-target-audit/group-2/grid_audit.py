import ast,collections,json,re,sys
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path[:0]=[str(H),str(R/'scripts'),str(R/'reference/edb-math/repairs/2026-10-26-mixed-math-titles')];from algebra import matrices
from reconstruct import SourceRenderer,reconstruct
from question_capture.math_format import normalize_source_tex
sources=json.loads((H/'source-inventory.json').read_text());S=json.loads((H/'current.json').read_text());objs={q[':question/math-academy-id']:q for q in S['questions']};objs.update({'tutorial:'+str(c[':tutorial/math-academy-id']):c for c in S['contents']if ':tutorial/content'in c});index=collections.defaultdict(list)
for r in sources:index[r['identity'],r['attribute']].append(r)
def grids(html):
 s=BeautifulSoup(html,'html.parser')
 for control in s.select('.freeResponseTextbox,.matheditor-wrapper-answer,.selectList,.studentAnswer'):control.decompose()
 ns=s.select('.mjpage,mjx-container,math');ids={id(n)for n in ns};roots=[n for n in ns if not any(id(p)in ids for p in n.parents)];tex=[];errors=[]
 for n in roots:
  try:
   title=n.find('title')
   if title:value=reconstruct(title)
   else:
    math=n if n.name=='math'else n.find('math');assert math is not None;r=SourceRenderer(None);value=normalize_source_tex(r.m(math));assert not r.errors,r.errors
   tex.append(value)
  except Exception as e:errors.append(str(e))
 return[tuple(tuple(str(c)for c in row)for row in m['matrix'].tolist())for t in tex for m in matrices(t)],errors
checks=[];review=[];missing=[]
for(mid,attr),srcs in index.items():
 q=objs[mid];visible=q.get(':'+attr,'')
 if attr=='question/problem':visible+='\n'+''.join(f[':answer-field/key']for f in q.get(':question/answer-fields',[])if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox')
 if not visible:continue
 current=[tuple(tuple(str(c)for c in row)for row in m['matrix'].tolist())for m in matrices(visible)];matched=[];mismatches=[]
 for src in srcs:
  sg,errors=grids(src['html'])
  if sg==current and not errors:matched.append(src['path'])
  else:mismatches.append({'path':src['path'],'source_grids':sg,'current_grids':current,'errors':errors})
 if matched:checks.append({'entity':q[':db/id'],'identity':mid,'attribute':attr,'matched_source':matched[0],'numeric_or_symbolic_grids':len(current)})
 else:review.append({'entity':q[':db/id'],'identity':mid,'attribute':attr,'candidates':mismatches})
(H/'source-grid-audit.json').write_text(json.dumps({'checks':checks,'review':review},indent=2)+'\n');print('Matched',len(checks),'Review',len(review));print([(r['identity'],r['attribute'])for r in review])
