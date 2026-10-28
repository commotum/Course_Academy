import json,re,sys,collections
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import ENV,environment,cells
s=(H/'check_row_math.py').read_text();exec(s[s.index('s=(R/'):s.index('P=json.loads')]);D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());pm={(p['entity'],p['attribute']):p['after']for p in P};src=collections.defaultdict(list)
for r in json.loads((H/'sources.json').read_text()):
 if r['attribute']=='question/problem':src[r['identity']].append(r)
def matrices(text):
 out=[]
 for m in ENV.finditer(text):
  if m[1]!='begin'or m[2]not in ['bmatrix','vmatrix','array']:continue
  span=environment(text,m.start());body=text[span[0]:span[1]]
  if m[2]=='array':
   col=re.match(r'\{[clr]+\}',body)
   if not col:continue
   body=body[col.end():]
  try:M=S.Matrix([[scalar(c)for c in row]for row in cells(body)])
  except Exception:continue
  if any(x.free_symbols for x in M):continue
  out.append(M)
 return out
proof=[];bad=[]
for q in D['questions']:
 ident=q.get(':question/math-academy-id')
 if not src[ident]:continue
 text=pm.get((q[':db/id'],'question/problem'),q[':question/problem'])+'\n'+'\n'.join(pm.get((f[':db/id'],'answer-field/key'),f[':answer-field/key'])for f in q.get(':question/answer-fields',[])if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox');want=matrices(text);options=[]
 for s in src[ident]:
  if not all(isinstance(t,str)for t in s['formulas']):continue
  actual=matrices('\n'.join(s['formulas']));same=len(want)==len(actual)and all(a.shape==b.shape and all(S.simplify(x)==0 for x in a-b)for a,b in zip(want,actual));options.append({'source':s['path'],'source_matrices':[str(x)for x in actual],'matches':same})
 good=next((o for o in options if o['matches']),None);o={'entity':q[':db/id'],'identity':ident,'numeric_matrices':[str(x)for x in want],'count':len(want),'matching_source':good,'source_options':len(options)};proof.append(o)
 if not good:bad.append({**o,'attempts':options})
(H/'given-matrix-source-verification.json').write_text(json.dumps(proof,indent=2)+'\n');(H/'given-matrix-source-candidates.json').write_text(json.dumps(bad,indent=2)+'\n');print('source question comparisons',len(proof),'numeric matrices',sum(o['count']for o in proof),'direct matches',sum(bool(o['matching_source'])for o in proof),'unmatched',len(bad));print([(b['entity'],b['identity'],b['count'],[len(o['source_matrices'])for o in b['attempts']])for b in bad])
