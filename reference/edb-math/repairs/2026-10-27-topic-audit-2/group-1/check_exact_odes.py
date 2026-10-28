import collections,json,re,sys
from pathlib import Path
import sympy as S
from texmath import parse
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import MATH
D=json.loads((H/'current.json').read_text());ts={t['entity']for t in D['topics']if t['ma_id']==2521};ids={q for t,k,q in D['links']if t in ts};out=[]
def maths(text):return [m[0][2:-2]if m[0].startswith('$$')else m[0][1:-1]for m in MATH.finditer(text)]
def eq(a,b):return S.simplify(S.trigsimp(a-b))==0
def parts(tex):
 pattern=r'(?:\\(?:text|textrm|mathrm)\{d\}|d)([xyuvrs])';variables=list(dict.fromkeys(re.findall(pattern,tex)));assert len(variables)==2,(tex,variables);variables=sorted(variables);v1,v2=variables;ds={v1:'D',v2:'E'};tex=tex.split('=')[0];tex=re.sub(r'[PQ]\([^)]*\)',lambda m:m[0][0],tex);tex=re.sub(pattern,lambda m:ds[m[1]],tex);expression=S.expand(parse(tex));A,B=[S.Symbol(v,positive=True)for v in variables];dd,ee=S.symbols('D E',positive=True);return expression.coeff(dd),expression.coeff(ee),A,B
for q in D['questions']:
 if q[':db/id']not in ids:continue
 ms=maths(q[':question/problem']);fs=q.get(':question/answer-fields',[]);r={'question':q[':db/id'],'identity':q.get(':question/math-academy-id'),'checks':[]}
 try:
  ode=next((m for m in ms if re.match(r"\s*\{?y\}?(?:\^\{[′']\}|[′'])\s*=",m)),None)
  difftex=next((m for m in ms if len(re.findall(r'(?:\\(?:text|textrm|mathrm)\{d\}|d)[xyuvrs]',m))>=2),None)
  if ode:
   rhs=parse(ode.split('=',1)[1].rstrip('.,'));P,Q=S.fraction(S.cancel(rhs));Q=-Q;A,B=[S.Symbol(v,positive=True)for v in'xy']
  elif difftex:P,Q,A,B=parts(difftex)
  else:P=Q=None;A,B=[S.Symbol(v,positive=True)for v in'xy']
  unknown='P'if P is not None and S.Symbol('P',positive=True)in P.free_symbols else'Q'if Q is not None and S.Symbol('Q',positive=True)in Q.free_symbols else None
  if unknown:
   compare=S.diff(Q,A)if unknown=='P'else S.diff(P,B);candidate_derivative=B if unknown=='P'else A
   if fs and fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox':
    for f in fs:
     candidate=parse(maths(f[':answer-field/key'])[0]);truth=eq(S.diff(candidate,candidate_derivative),compare);r['checks'].append({'field':f[':db/id'],'candidate':str(candidate),'required_partial':str(compare),'derived_truth':truth,'pass':f[':answer-field/correct'][':answer/value']==('true'if truth else'false')})
   else:
    candidates=[]
    for tex in ms[ms.index(difftex)+1:]:
     if '='in tex or'P('in tex or'Q('in tex:continue
     try:candidates.append(parse(tex))
     except Exception:pass
    truths=[eq(S.diff(c,candidate_derivative),compare)for c in candidates];r.update(candidate_expressions=list(map(str,candidates)),truth_vector=truths)
    if fs:
     roman=['I','II','III'];chosen=[roman[i]for i,v in enumerate(truths)if v];expected=', '.join(chosen[:-1])+', and '+chosen[-1]if len(chosen)==3 else' and '.join(chosen)+' only';observed=fs[0][':answer-field/correct'][':answer/value']if fs[0].get(':answer-field/correct')else None;r['checks'].append({'field':fs[0][':db/id'],'expected':expected,'observed':observed,'pass':observed is None or observed.replace('Í','I')==expected,'typographic_error':observed is not None and'Í'in observed})
  elif fs and fs[0][':answer-field/type'][':db/ident']==':answer-field.type/checkbox'and P is None:
   for f in fs:
    p0,q0,a,b=parts(maths(f[':answer-field/key'])[0]);res=S.simplify(S.diff(p0,b)-S.diff(q0,a));truth=res==0;r['checks'].append({'field':f[':db/id'],'partial_residual':str(res),'derived_truth':truth,'pass':f[':answer-field/correct'][':answer/value']==('true'if truth else'false')})
  elif P is not None:
   Py,Qx=S.diff(P,B),S.diff(Q,A);exact=eq(Py,Qx);r.update(P=str(P),Q=str(Q),P_y=str(Py),Q_x=str(Qx),exact=exact)
   for f in fs:
    if ':answer-field/correct'not in f:continue
    av=f[':answer-field/correct'][':answer/value'];key=f[':answer-field/key'];passed=None;proof={}
    if f[':answer-field/type'][':db/ident']==':answer-field.type/select':
     if key in['field-2','field-3','field-4','field-5']:target={'field-2':P,'field-3':Q,'field-4':Py,'field-5':Qx}[key];passed=eq(parse(av),target);proof={'expected':str(target)}
     elif key=='field-7':passed=('not'in av)!=exact;proof={'expected_exact':exact}
     elif key in['field-1','field-6']:
      derivative_condition=r'\frac{∂P}{∂'+str(B)+r'}'+('='if key=='field-1'or exact else r'\ne ')+r'\frac{∂Q}{∂'+str(A)+'}';passed=re.sub(r'\s+','',av)==re.sub(r'\s+','',derivative_condition);proof={'expected':derivative_condition}
    elif '='in av:
     left,right=av.split('=',1);potential=parse(left)-parse(right);res=S.simplify(S.diff(potential,A)*Q-S.diff(potential,B)*P);passed=res==0;proof={'potential_residual':str(res)};ic=re.search(r'y\(([^)]+)\)\s*=\s*([^$.,]+)',q[':question/problem'])
     if ic:icres=S.simplify(potential.subs({A:parse(ic[1]),B:parse(ic[2])}));passed=passed and icres==0;proof['initial_condition_residual']=str(icres)
    if passed is not None:r['checks'].append({'field':f[':db/id'],'key':key,'canonical':av,'pass':bool(passed),**proof})
  else:r['limit']='Canonical candidate-equation example: first and third exact by(2x,2x),(2y,y),(−1,−1) partial pairs; no answer fields.'
  r['status']='review'if any(c.get('pass')is False for c in r['checks'])else'checked'
 except Exception as ex:r['status']='unresolved';r['reason']=str(ex)
 out.append(r)
(H/'exact-ode-validation.json').write_text(json.dumps(out,indent=2));print(collections.Counter(r['status']for r in out));print([r for r in out if r['status']!='checked'])
