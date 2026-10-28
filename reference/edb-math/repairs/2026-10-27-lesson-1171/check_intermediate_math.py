import json
from pathlib import Path
H=Path(__file__).resolve().parent;ns={'__file__':str(H/'audit_math.py')};exec(compile((H/'audit_math.py').read_text().split('for q in Q:')[0],str(H/'audit_math.py'),'exec'),ns);mat,grids,same=ns['mat'],ns['grids'],ns['same'];S=ns['S'];D=json.loads((H/'proposed.json').read_text());issues=[];matrices=0;steps=0
for q in D['questions']:
 inputs=list(map(mat,grids(q[':question/problem'])));known=inputs[:];product=inputs[0]
 for m in inputs[1:2 if 'student claims'in q[':question/problem']else len(inputs)]:product=product*m;known.append(product)
 for m in inputs:
  if m.rows==m.cols:known.append(S.eye(m.rows))
 for g in grids(q.get(':question/worked-solution','')):
  value=mat(g);matrices+=1
  if not any(same(value,m)for m in known):issues.append({'entity':q[':db/id'],'matrix':str(value),'expected':str(product)})
from question_capture.math_format import MATH
for a in D['structure']:
 for step in a[':activity/steps']:
  c=step[':step/content']
  for span in MATH.finditer(c.get(':tutorial/content','')):
   ms=list(map(mat,grids(span[0])))
   if len(ms)<3:continue
   expected=ms[0]*ms[1]
   for m in ms[2:]:
    steps+=1
    if not same(m,expected):issues.append({'entity':c[':db/id'],'matrix':str(m),'expected':str(expected)})
report={'passed':not issues,'question_solution_matrices_verified':matrices,'tutorial_expanded_and_result_matrices_verified':steps,'issues':issues};(H/'intermediate-math-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(report);assert not issues
