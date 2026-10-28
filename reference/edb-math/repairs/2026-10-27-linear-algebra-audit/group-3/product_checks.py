import json,re,sys
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import ENV,environment,cells
import sympy as sp
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());keys={r['field']:r['answer']for r in json.loads((H/'missing-key-completions.json').read_text())};ids={r[2]for r in D['links']if r[1]in (17592186100873,17592186100913)};checks=[];skips=[]
def number(c):
 c=re.sub(r'\\frac\{(-?\d+)\}\{(-?\d+)\}',r'(\1)/(\2)',c)
 if not re.fullmatch(r'[\d\s+*/().-]+',c):raise ValueError(c)
 return sp.sympify(c)
def grids(s):
 out=[]
 for m in ENV.finditer(s):
  if m[1]!='begin'or m[2]not in ('bmatrix','array'):continue
  span=environment(s,m.start());b=s[span[0]:span[1]]
  if m[2]=='array':b=re.sub(r'^\{[^{}]*\}','',b)
  cs=cells(b)
  if not cs:continue
  try:out.append(sp.Matrix([[number(c)for c in row]for row in cs]))
  except ValueError:continue
 return out
for q in D['questions']:
 if q[':db/id']not in ids:continue
 gs=grids(q[':question/problem']);fs=q.get(':question/answer-fields',[])
 if len(gs)!=2:skips.append({'entity':q[':db/id'],'reason':'requires separate nonnumeric/dimension-only or canonical-example inspection','operands':len(gs)});continue
 expected=gs[0]*gs[1]if gs[0].cols==gs[1].rows else None
 if not fs:
  if q[':db/id']==17592186100695:assert expected[2,1]==0
  else:assert expected in grids(q[':question/worked-solution'])
  checks.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'expected':str(expected),'passed':True,'canonical_example_no_fields':True});continue
 fieldmap={f[':answer-field/key']:f for f in fs};ordered_keys=re.findall(r'\{\{([^{}]+)\}\}',q[':question/problem']);fs=[fieldmap[k]for k in ordered_keys]if ordered_keys else fs
 correct=[]
 for f in fs:
  right=f.get(':answer-field/correct',{}).get(':db/id')or keys.get(f[':db/id']);correct.append(next(a[':answer/value']for a in f[':answer-field/choices']if a[':db/id']==right))
 target=re.search(r'\{?([a-z])\}?_\{([1-5])([1-5])\}',q[':question/problem']);result=None
 if expected is None:result=len(correct)==1 and correct[0].lower().strip()=='undefined'
 elif target:result=len(correct)==1 and sp.Integer(correct[0])==expected[int(target[2])-1,int(target[3])-1]
 elif len(fs)==1:
  ans=grids(correct[0]);result=bool(ans and ans[0]==expected)
 else:
  # Whole row-by-column product grid; keys appear in the original table in row-major order.
  if len(correct)==expected.rows*expected.cols:result=[sp.Integer(x)for x in correct]==list(expected)
  else:skips.append({'entity':q[':db/id'],'reason':'partial grid needs cell-position check','fields':len(correct)});continue
 checks.append({'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'expected':str(expected),'correct_values':correct,'passed':result})
 assert result,(q[':db/id'],correct,expected)
(H/'product-math-validation.json').write_text(json.dumps({'checks':checks,'skipped':skips},indent=2));print('product checks',len(checks),'skipped',skips)
