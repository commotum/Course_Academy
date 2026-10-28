import collections,json,re,sys
from pathlib import Path
import sympy as sp
sys.path.insert(0,'scripts');from question_capture.math_format import MATH,ENV,environment,cells
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());tids={t['entity']for t in D['topics']if t['ma_id']in (1733,1374)};qids={r[2]for r in D['links']if r[0]in tids};out=[];skips=[];bad=[]
def scalar(t):
 t=re.sub(r'\\color\{[^{}]*\}|\\(?:displaystyle|,|;|!|quad|qquad)','',t);t=t.replace(r'\cdot','*').replace(r'\times','*').replace('−','-')
 for _ in range(10):
  n=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
  if n==t:break
  t=n
 t=re.sub(r'\\bbox\[[^\]]*\]\{([^{}]*)\}',r'\1',t);t=t.replace('{','(').replace('}',')').replace('^','**')
 if not re.fullmatch(r'[\d\s+*/().-]+',t):raise ValueError(t)
 return sp.sympify(t)
for q in D['questions']:
 if q[':db/id']not in qids:continue
 v=q.get(':question/worked-solution','');grids=[]
 for m in ENV.finditer(v):
  if m[1]!='begin'or m[2]not in ('bmatrix','array'):continue
  span=environment(v,m.start());body=v[span[0]:span[1]]
  if m[2]=='array':body=re.sub(r'^\{[^{}]*\}','',body)
  cs=cells(body)
  if not cs or len({len(row)for row in cs})!=1 or len(cs[0])!=4:continue
  try:mat=sp.Matrix([[scalar(c)for c in row]for row in cs])
  except Exception as ex:skips.append({'entity':q[':db/id'],'matrix':v[m.start():span[2]],'reason':'symbolic or decorated entries','detail':str(ex)});continue
  grids.append({'span':[m.start(),span[2]],'rows':mat.rows,'matrix':[[str(x)for x in row]for row in mat.tolist()],'rref':str(mat.rref()[0]),'tex':v[m.start():span[2]]})
 byshape=collections.defaultdict(list)
 for g in grids:byshape[g['rows'],4].append(g)
 for shape,gs in byshape.items():
  if len(gs)<2:continue
  r={'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'shape':shape,'matrices':gs,'row_equivalent':len({g['rref']for g in gs})==1};out.append(r)
  if not r['row_equivalent']:bad.append(r)
(H/'intermediate-matrix-validation.json').write_text(json.dumps({'questions_in_scope':len(qids),'chains':len(out),'matrices':sum(len(r['matrices'])for r in out),'chains_with_mismatch':bad,'skipped_matrices':skips,'checks':out},indent=2));print('scope',len(qids),'chains',len(out),'matrices',sum(len(r['matrices'])for r in out),'bad',len(bad),'skipped',len(skips));print([(r['entity'],r['source'],r['shape'])for r in bad])
