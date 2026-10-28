import json,re,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells
s=(H/'check_row_math.py').read_text();exec(s[s.index('s=(R/'):s.index('P=json.loads')]);D=json.loads((H/'current.json').read_text());inv=json.loads((H.parent/'inventory.json').read_text());topics={t['entity']:t['ma_id']for t in D['topics']};links={q:topics[t]for t,k,q in inv['links']if t in topics};rows={o['entity']:o for o in json.loads((H/'row-math.json').read_text())if o['attribute']=='question/worked-solution'};P=json.loads((H/'proposals.json').read_text());pm={(p['entity'],p['attribute']):p['after']for p in P};out=[];flags=[]
def matrices(v):
 out=[]
 for m in ENV.finditer(v):
  if m[1]!='begin'or m[2]not in ['bmatrix','array']:continue
  span=environment(v,m.start());body=v[span[0]:span[1]]
  if m[2]=='array':
   c=re.match(r'\{[clr]+\}',body)
   if not c:continue
   body=body[c.end():]
  try:M=S.Matrix([[scalar(c)for c in row]for row in cells(body)])
  except Exception:continue
  if any(re.search(r'^[x]_?\d',str(s))for x in M for s in x.free_symbols):continue
  out.append(M)
 return out
for q in D['questions']:
 if links[q[':db/id']]not in [1852,1850,1864,1732]:continue
 r=rows.get(q[':db/id'])
 if not r or not r['matrices']:continue
 ms=matrices(pm.get((q[':db/id'],'question/problem'),q[':question/problem']))
 if not ms:continue
 if links[q[':db/id']]==1732:
  if len(ms)!=1 or ms[0].shape!=(3,3):continue
  expected=ms[0].row_join(S.eye(3))
 else:
  try:expected=S.Matrix.hstack(*ms)
  except Exception:continue
 tex=r['matrices'][0]['tex'];span=environment(tex,0);body=tex[span[0]:span[1]];body=body[re.match(r'\{[^{}]*\}',body).end():];actual=S.Matrix([[scalar(c)for c in row]for row in cells(body)]);same=expected.shape==actual.shape and expected==actual
 o={'entity':q[':db/id'],'identity':q.get(':question/math-academy-id'),'expected_initial':str(expected),'actual_initial':str(actual),'matches':same};out.append(o)
 if not same:flags.append(o)
(H/'initial-matrix-verification.json').write_text(json.dumps(out,indent=2)+'\n');print('initial matrices',len(out),'mismatch',len(flags));print(json.dumps(flags,indent=2))
