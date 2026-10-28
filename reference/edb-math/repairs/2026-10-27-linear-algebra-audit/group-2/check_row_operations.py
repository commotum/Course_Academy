import json,re,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import ENV,environment,cells
s=(H/'check_row_math.py').read_text();exec(s[s.index('s=(R/'):s.index('P=json.loads')]);P=json.loads((H/'proposals.json').read_text());pm={(p['entity'],p['attribute']):p['after']for p in P};F=json.loads((H/'fields.json').read_text());RM=json.loads((H/'row-math.json').read_text());fm={(f[0],f[1]):f[2]for f in F};checks=[];bad=[];skip=[]
def mat(tex):
 span=environment(tex,0);body=tex[span[0]:span[1]];body=body[re.match(r'\{[^{}]*\}',body).end():];return S.Matrix([[scalar(c)for c in row]for row in cells(body)])
for item in RM:
 e=item['entity'];a=item['attribute'];text=pm.get((e,a),fm[e,a]);ms=item['matrices']
 for x,y in zip(ms,ms[1:]):
  if x['shape']!=y['shape']:continue
  between=text[x['start']+len(x['tex']):y['start']];bs=between.replace('&','').replace('∼','').strip();bs=re.sub(r'\\color\{[^{}]*\}','',bs);bs=re.sub(r'\{?R\}?_\{?(\d+)\}?',r'R\1',bs)
  swap=re.search(r'R(\d+)\s*(?:↔|\\leftrightarrow)\s*R(\d+)',bs)
  assign=re.search(r'R(\d+)\s*(?::=|\\leftarrow)\s*([\s\S]*?)\s*(?:\\\\|$)',bs)
  A=mat(x['tex']);B=mat(y['tex']);after=A.copy();kind=None
  try:
   if swap:after.row_swap(int(swap[1])-1,int(swap[2])-1);kind='swap'
   elif assign:
    target=int(assign[1])-1;expr=assign[2].strip();v=scalar(expr);symbols=[S.Symbol('R'+str(i+1))for i in range(A.rows)];rhs=S.zeros(1,A.cols)
    for i,sym in enumerate(symbols):rhs+=v.coeff(sym)*A[i,:]
    assert S.simplify(v-sum(v.coeff(sym)*sym for sym in symbols))==0,(expr,v)
    after[target,:]=rhs;kind='replacement'
   else:skip.append({'entity':e,'between':between});continue
  except Exception as ex:skip.append({'entity':e,'between':between,'error':str(ex)});continue
  ok=after==B;entry={'entity':e,'attribute':a,'identity':item['identity'],'operation':bs,'kind':kind,'matches_next_matrix':ok};checks.append(entry)
  if not ok:bad.append({**entry,'before':str(A),'after_expected_from_annotation':str(after),'after_shown':str(B),'between_original':between})
(H/'row-operation-verification.json').write_text(json.dumps(checks,indent=2)+'\n');(H/'row-operation-candidates.json').write_text(json.dumps(bad,indent=2)+'\n');(H/'row-operation-skips.json').write_text(json.dumps(skip,indent=2)+'\n');print('operations checked',len(checks),'mismatches',len(bad),'skipped',len(skip));print(json.dumps(bad,indent=2))
