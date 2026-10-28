import json,re,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import ENV,environment,cells
s=(H/'check_row_math.py').read_text();exec(s[s.index('s=(R/'):s.index('P=json.loads')]);D=json.loads((H/'generator-samples.json').read_text());checks=[]
def matrices(text):
 out=[]
 for m in ENV.finditer(text):
  if m.groups()!=('begin','bmatrix'):continue
  span=environment(text,m.start());out.append(S.Matrix([[scalar(c)for c in row]for row in cells(text[span[0]:span[1]])]))
 return out
for r in D:
 k0=r['knowledge_point'];kp=k0 if isinstance(k0,int)else(k0.get('db_id')or k0.get(':db/id')or {k[':knowledge-point/id']:k[':db/id']for k in json.loads((H/'current.json').read_text())['kps']}.get(k0.get('id')));q=r['question'];p=q[':question/problem'];sol=q[':question/worked-solution'];features=[]
 if kp==17592186119808:
  assert all(x in p and x in sol for x in [r'\mathbf{a}',r'\mathbf{b}',r'\operatorname{Span}\{']);assert not re.search(r'(?<![A-Za-z])b\\(?:notin|in)',p+sol);features+=['bold input/output vectors','visible span braces']
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:
    if'notin'in a[':answer/value']:assert r'\mathbf{b}'in a[':answer/value']and r'\mathbf{a}'in a[':answer/value']
 if kp==17592186119809:
  assert all(r'\mathbf{'+v+'}'in p for v in 'bcu');assert r'\mathbb{R}'in p;features+=['bold plane vectors','real domain']
 if kp==17592186119856:
  assert all(r'\mathbf{'+v+'}'in p for v in 'ab');assert r'\operatorname{Span}\{'in p;features+=['bold span vectors','visible span braces']
 if kp==17592186119932:
  assert all(r'\mathbf{'+v+'}'in p for v in 'abcd');features+=['bold volume-generating vectors']
 if kp in [17592186124511,17592186124629,17592186124630]:
  assert r'\mathbb'in sol;features+=['real-number domain']
 if kp in [17592186115226,17592186115227,17592186115229]:
  ms=matrices(p)
  if kp==17592186115229:expected=ms[0]**r['generation']['power']
  else:
   expr=re.search(r'Calculate \$([ABC+\-]+)\$',p)[1];env=dict(zip('ABC',ms[:3]));parts=re.findall(r'([+-]?)([ABC])([ABC])',expr);expected=S.zeros(ms[0].rows,ms[-1].cols)if len(parts)>1 else None
   values=[(-1 if op=='-' else 1)*(env[a]*env[b])for op,a,b in parts];expected=sum(values[1:],values[0])if len(parts)>1 else env['A']*env['B']*env['C']
  fs=q[':question/answer-fields'];typ=fs[0][':answer-field/type'];typ=typ[':db/ident']if isinstance(typ,dict)else typ
  if typ==':answer-field.type/blank':
   assert'matrix-answer-brackets'in p
   rows=[[re.sub(r'<[^>]+>','',c).strip()for c in re.findall(r'<td>(.*?)</td>',row)]for row in re.findall(r'<tr>(.*?)</tr>',p,re.S)];assert len(rows)==expected.rows and all(len(row)==expected.cols for row in rows)
   bykey={f[':answer-field/key']:f for f in fs};observed=[]
   for i,row in enumerate(rows):
    for j,c in enumerate(row):
     m=re.fullmatch(r'\{\{([^{}]+)\}\}',c)
     if m:
      observed.append(m[1]);f=bykey[m[1]];correct=f[':answer-field/correct'][1];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==correct);assert S.simplify(scalar(a[':answer/value'])-expected[i,j])==0
     elif r'\ast'not in c:assert S.simplify(scalar(c.strip('$'))-expected[i,j])==0
   assert set(observed)==set(bykey);features+=['all displayed blank and supplied entries match exact product/power','field keys unique and mapped to cells']
  else:
   f=fs[0];correct=f[':answer-field/correct'][1];a=next(a for a in f[':answer-field/choices']if a[':answer/id']==correct);m=matrices(a[':answer/value']);assert len(m)==1 and m[0]==expected;features+=['whole correct matrix choice matches exact product/power']
 checks.append({'question':q[':question/id'],'kp':kp,'features':features,'passed':True})
(H/'generator-semantic-verification.json').write_text(json.dumps(checks,indent=2)+'\n');print('semantic checks',len(checks),'matrix products/powers',sum(any('matrix'in f or'entries'in f for f in c['features'])for c in checks),'source notation checks',sum(any('bold'in f or'domain'in f for f in c['features'])for c in checks))
