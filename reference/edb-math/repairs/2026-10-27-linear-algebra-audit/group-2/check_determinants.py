import json,re,sys,collections
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells,MATH
s=(H/'check_row_math.py').read_text();exec(s[s.index('s=(R/'):s.index('P=json.loads')]);D=json.loads((H/'current.json').read_text());I=json.loads((H.parent/'inventory.json').read_text());qids={q for t,k,q in I['links']if t==17592186049159};P=json.loads((H/'proposals.json').read_text());pm={(p['entity'],p['attribute']):p['after']for p in P};proof=[];flags=[];skips=[]
def determinant_rhs(text):
 text=text.strip();edits=[];has=False
 for m in ENV.finditer(text):
  if m.groups()!=('begin','vmatrix'):continue
  span=environment(text,m.start());gs=cells(text[span[0]:span[1]]);M=S.Matrix([[scalar(c)for c in row]for row in gs]);val=M.det();edits.append((m.start(),span[2],'('+str(val)+')'));has=True
 for a,b,v in reversed(edits):text=text[:a]+v+text[b:]
 text=re.sub(r'\\left|\\right','',text).replace(r'\cdot','*').replace(r'\times','*');text=text.rstrip('.,');text=text.replace('^','**')
 if any(x in text for x in ['=','\\begin','\\end']):raise ValueError('not scalar')
 val=scalar(text)
 if val.free_symbols:raise ValueError('symbolic expression')
 return val,has
for q in D['questions']:
 if q[':db/id']not in qids:continue
 sol=pm.get((q[':db/id'],'question/worked-solution'),q.get(':question/worked-solution',''));values=[]
 for m in MATH.finditer(sol):
  v=m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1];chain=[];expected=None
  if r'\begin{aligned}'in v:
   span=environment(v,v.index(r'\begin{aligned}'));rows=cells(v[span[0]:span[1]])
   for row in rows or[]:
    joined=''.join(row)
    if '='not in joined:continue
    lhs,rhs=joined.split('=',1)
    if lhs.strip():
     expected=None
     try:expected=determinant_rhs(lhs)[0]
     except Exception:pass
    try:
     value,has=determinant_rhs(rhs);o={'value':str(value),'has_determinant':has,'tex':rhs};values.append(o)
     if expected is not None and S.simplify(value-expected)!=0:flags.append({'entity':q[':db/id'],'identity':q.get(':question/math-academy-id'),'expected':str(expected),'actual':o,'full_formula':v})
     expected=value
    except Exception:skips.append({'entity':q[':db/id'],'tex':rhs})
  elif '='in v:
   expected=None
   for part in v.split('='):
    try:
     value,has=determinant_rhs(part);o={'value':str(value),'has_determinant':has,'tex':part};values.append(o)
     if expected is not None and S.simplify(value-expected)!=0:flags.append({'entity':q[':db/id'],'identity':q.get(':question/math-academy-id'),'expected':str(expected),'actual':o,'full_formula':v})
     expected=value
    except Exception:skips.append({'entity':q[':db/id'],'tex':part});expected=None
 if values:proof.append({'entity':q[':db/id'],'identity':q.get(':question/math-academy-id'),'evaluated_rows':values})
(H/'determinant-verification.json').write_text(json.dumps(proof,indent=2)+'\n');(H/'determinant-candidates.json').write_text(json.dumps(flags,indent=2)+'\n');(H/'determinant-skips.json').write_text(json.dumps(skips,indent=2)+'\n');print('questions',len(proof),'evaluated rows',sum(len(p['evaluated_rows'])for p in proof),'skipped nonscalar rows',len(skips),'unequal rows',len(flags));print(json.dumps(flags,indent=2))
