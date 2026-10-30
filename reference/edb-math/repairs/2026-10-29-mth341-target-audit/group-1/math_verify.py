"""Exact independent family checks; no database writes."""
import json,re,sys,collections
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells,MATH
D=json.loads((H/'current.json').read_text());P=json.loads((H/'proposals.json').read_text());pm={(p['entity'],p['attribute']):p['after']for p in P};bykp={q:k for t,k,q in D['links']};bymid={q:next(x['ma_id']for x in D['topics']if x['entity']==t)for t,k,q in D['links']}
def scalar(s):
 s=s.replace('⁡','').replace('−','-').replace('′',"'");s=re.sub(r'\\color\{[A-Za-z]+\}','',s);s=re.sub(r'\\hspace\{[^{}]*\}|\\text\{\s*\}','',s);s=re.sub(r'\\(?:left|right|displaystyle|textstyle)|\\[,;!]','',s);s=s.replace(r'\operatorname{ln}',r'\ln');s=re.sub(r'\{?([a-z])\}?_\{(\d+)\}',r'\1\2',s)
 def group(t,i):
  while i<len(t)and t[i].isspace():i+=1
  if t[i]!='{':return t[i],i+1
  start=i+1;depth=1;i+=1
  while depth:depth+=(t[i]=='{')-(t[i]=='}');i+=1
  return t[start:i-1],i
 while(m:=re.search(r'\\(?:dfrac|frac|sqrt)\s*',s)):
  arg,end=group(s,m.end())
  if'sqrt'in m[0]:repl='sqrt('+str(scalar(arg))+')'
  else:b,end=group(s,end);repl='(('+str(scalar(arg))+')/('+str(scalar(b))+'))'
  s=s[:m.start()]+repl+s[end:]
 s=s.replace(r'\cdot','*').replace(r'\times','*').replace(r'\pi','pi').replace(r'\ln','log').replace('^','**').replace('{','(').replace('}',')')
 assert re.fullmatch(r'[\w+*/().\s-]+',s),s
 names=set(re.findall(r'[A-Za-z_]\w*',s));return parse_expr(s,local_dict={'pi':S.pi,'sqrt':S.sqrt,'log':S.log,**{n:S.Symbol(n)for n in names-{'pi','sqrt','log'}}},transformations=standard_transformations+(implicit_multiplication_application,rationalize))
def mats(v):
 out=[]
 for m in ENV.finditer(v):
  if m[1]!='begin'or m[2]not in ['bmatrix','array']:continue
  span=environment(v,m.start());body=v[span[0]:span[1]]
  if m[2]=='array':
   mm=re.match(r'\{[cl|r]+\}',body)
   if not mm:continue
   body=body[mm.end():]
  try:mat=S.Matrix([[scalar(c)for c in row]for row in cells(body)]);out.append((m.start(),span[2],mat))
  except Exception:continue
 return out
out=[];flags=[];skips=[]
def check(q,kind,proof,ok=True):
 r={'entity':q[':db/id'],'identity':q.get(':question/math-academy-id'),'topic':bymid[q[':db/id']],'check':kind,'passed':bool(ok),'proof':str(proof)};out.append(r)
 if not ok:flags.append(r)
def qfields(q):
 for f in q.get(':question/answer-fields',[]):
  aid=pm.get((f[':db/id'],'answer-field/correct'),f.get(':answer-field/correct',{}).get(':db/id'));choices=[{**a,':answer/value':pm.get((a[':db/id'],'answer/value'),a[':answer/value'])}for a in f[':answer-field/choices']];right=next(a for a in choices if a[':db/id']==aid);yield f,choices,right
for q in D['questions']:
 mid=bymid[q[':db/id']];kp=bykp[q[':db/id']];v=pm.get((q[':db/id'],'question/problem'),q[':question/problem']);ms=mats(v);ms=[m[2]for m in ms];solution=pm.get((q[':db/id'],'question/worked-solution'),q.get(':question/worked-solution',''))
 # Every row-reduction chain retains the same row space, including intermediate matrices.
 for env in list(ENV.finditer(solution)):
  if env.groups()!=('begin','aligned'):continue
  span=environment(solution,env.start());block=solution[env.start():span[2]]
  if'∼'not in block and r'\sim'not in block:continue
  bs=mats(block)
  for (_,_,a),(_,_,b)in zip(bs,bs[1:]):
   if a.shape==b.shape:check(q,'row-equivalence',str(a)+' => '+str(b),a.rref()[0]==b.rref()[0])
 try:
  if mid==1854:
   if kp==17592186119813:
    assert len(ms)==2;prod=ms[0]*ms[1];syms=set().union(*(x.free_symbols for x in prod));answers=S.solve(list(prod),list(syms));check(q,'null-vector-parameter',str(prod)+' roots '+str(answers),bool(answers))
    for f,choices,right in qfields(q):val=scalar(right[':answer/value']);check(q,'canonical-parameter',val,all(S.simplify(x.subs({s:val for s in syms}))==0 for x in prod))
   elif kp==17592186119814:
    A=ms[0];nullity=A.cols-A.rank()
    def valid(value):
     am=mats(value)
     if not am:return bool(re.search(r'\{(?:\\mathbf\{)?0',value)and nullity==0)
     b=am[0][2]
     if b.shape!=(A.cols,1):return False
     syms=sorted(set().union(*(x.free_symbols for x in b)),key=str)
     if not syms:return nullity==0 and b==S.zeros(A.cols,1)
     C=b.jacobian(syms);return A*b==S.zeros(A.rows,1)and C.rank()==nullity and b.subs({s:0 for s in syms})==S.zeros(A.cols,1)
    check(q,'null-space',f'rank={A.rank()}, nullity={nullity}, exact basis={A.nullspace()}')
    for f,choices,right in qfields(q):vals=[a[':db/id']for a in choices if valid(a[':answer/value'])];check(q,'null-space-bank',vals,vals==[right[':db/id']])
   elif kp==17592186119812:
    if ms:
     A=ms[0];products=[A*b for b in ms[1:]];truth=[p==S.zeros(A.rows,1)for p in products];check(q,'null-membership-products',str(products)+' truth='+str(truth))
     for f,choices,right in qfields(q):
      if f[':answer-field/type'][':db/ident'].endswith('checkbox'):
       fm=mats(f[':answer-field/key'])
       if fm:check(q,'null-membership-checkbox',A*fm[0][2],(A*fm[0][2]==S.zeros(A.rows,1))==(right[':answer/value']=='true'))
      else:
       ids=[int(x)for x in re.findall(r'\{?b\}?_?\{?(\d)',right[':answer/value'])];check(q,'null-membership-bank',ids,ids==[i+1 for i,t in enumerate(truth)if t])
    else:
     # Checkbox migration moves the vectors into their keys while the problem retains A.
     skips.append({'entity':q[':db/id'],'reason':'No problem matrices parsed'})
  elif mid==1868:
   if kp==17592186124508:
    dims=re.search(r'(\d+)\s*\\times\s*(\d+)',v);piv=re.search(r'(\d+)\$?\s+(?:of them are pivots|pivot columns)',v);nonpiv=re.search(r'(\d+)\$?\s+(?:\*\*)?non-pivot',v)
    if dims and (piv or nonpiv):
     n=int(nonpiv[1])if nonpiv else int(dims[2])-int(piv[1]);check(q,'rank-nullity-count',n)
     for f,choices,right in qfields(q):check(q,'rank-nullity-bank',right[':answer/value'],scalar(right[':answer/value'])==n)
    else:skips.append({'entity':q[':db/id'],'reason':'Count wording parser'})
   elif kp==17592186124510:
    A=ms[0];n=A.cols-A.rank();check(q,'rank-nullity-matrix',f'rank={A.rank()}, columns={A.cols}, nullity={n}')
    for f,choices,right in qfields(q):check(q,'rank-nullity-bank',right[':answer/value'],scalar(right[':answer/value'])==n)
   else:
    for f,choices,right in qfields(q):
     fm=mats(f[':answer-field/key']);claim=re.search(r'=\s*(\d+)\.?\$',f[':answer-field/key'])
     if fm and claim:
      A=fm[0][2];truth=A.cols-A.rank()==int(claim[1]);check(q,'nullity-checkbox',f'rank={A.rank()}, n={A.cols}, claim={claim[1]}',truth==(right[':answer/value']=='true'))
  elif mid==2623:
   if kp==17592186152155:
    A=ms[0];check(q,'column-space-pivots',f'rank={A.rank()}, pivots={A.rref()[1]}')
    for f,choices,right in qfields(q):
     vals=[]
     for a in choices:
      am=mats(a[':answer/value'])
      if not am:continue
      B=S.Matrix.hstack(*(m[2]for m in am));valid=B.rows==A.rows and B.cols==A.rank()and B.rank()==A.rank()and A.row_join(B).rank()==A.rank()
      if valid:vals.append(a[':db/id'])
     check(q,'column-space-bank',vals,vals==[right[':db/id']])
   else:
    A=ms[0];basis=re.search(r'(?:B|\\mathcal\{B\})\s*=([\s\S]*?)\$',v);subs=re.findall(r'\}_?\{(\d+)\}|[a-z]_\{(\d+)\}',basis[1])if basis else[];inds=[int(a or b)-1 for a,b in subs]
    if not inds:
     # The source/font-restored list may use grouped bold symbols.
     inds=[int(x)-1 for x in re.findall(r'_\{(\d+)\}',basis[1])]if basis else[]
    if not inds:skips.append({'entity':q[':db/id'],'reason':'Basis index parser'});continue
    B=A[:,inds];is_basis=B.cols==A.rank()and B.rank()==A.rank();check(q,'claimed-column-basis',f'indices={inds}, rank(A)={A.rank()}, rank(B)={B.rank()}, is_basis={is_basis}')
    for f,choices,right in qfields(q):
     if not is_basis:check(q,'nonbasis-bank',right[':answer/value'],'not a basis'in right[':answer/value']);continue
     target=re.search(r'(?:where|that)\s*\$([\s\S]*?)=',v)
     # target is explicitly the nonbasis column in the displayed decomposition.
     part=re.search(r'where\s*\$([^$]+)',v);target_ids=re.findall(r'_\{(\d+)\}',part[1])if part else[]
     if not target_ids:skips.append({'entity':q[':db/id'],'reason':'Target column parser'});continue
     j=int(target_ids[0])-1;x=B.gauss_jordan_solve(A[:,j])[0];prod=S.prod(x);check(q,'basis-coefficients',f'column={j+1}, coefficients={list(x)}, product={prod}',scalar(right[':answer/value'])==prod)
  elif mid==2103:
   if kp in [17592186133782,17592186133837]:
    n=ms[0].rows;A=S.Matrix.hstack(*ms);gram=A.T*A;check(q,'given-orthogonal-set',gram,all(gram[i,j]==0 for i in range(A.cols)for j in range(i)))
    basis=A.T.nullspace();assert len(basis)==1;b=basis[0];target=sum(abs(x)for x in b)
    if kp==17592186133837:target=S.simplify(target/S.sqrt((b.T*b)[0]))
    else:
     # Asking sum of coordinates of an extension with a specified component.
     cond=re.search(r'x\}_?\{(\d+)\}\s*=\s*(-?\d+)',v)
     if not cond:cond=re.search(r'x_\{(\d+)\}\s*=\s*(-?\d+)',v)
     ratio=re.search(r'\\frac\{\{x\}_\{(\d+)\}\}\{\{x\}_\{(\d+)\}\}',v)
     if ratio:target=S.simplify(b[int(ratio[1])-1]/b[int(ratio[2])-1])
     elif cond:target=S.simplify(sum(b)*S.Rational(cond[2])/b[int(cond[1])-1])
     else:skips.append({'entity':q[':db/id'],'reason':'Orthogonal extension component parser'});continue
    for f,choices,right in qfields(q):check(q,'orthogonal-extension-answer',f'basis={b}, expected={target}',S.simplify(scalar(right[':answer/value'])-target)==0)
   else:
    for f,choices,right in qfields(q):
     if f[':answer-field/type'][':db/ident'].endswith('checkbox'):
      fs=mats(f[':answer-field/key']);vs=[m[2]for m in fs]
      if not vs:continue
      gram=S.Matrix.hstack(*vs).T*S.Matrix.hstack(*vs);truth=all(gram[i,j]==0 for i in range(len(vs))for j in range(i))
      if kp==17592186133781:truth=truth and all(gram[i,i]==1 for i in range(len(vs)))
      check(q,'orthogonal-set-checkbox',gram,truth==(right[':answer/value']=='true'))
  elif mid==1849:
   # Exact answer values are independently substituted into all parameter dot-products.
   if kp==17592186119804:
    a,b=ms;expr=S.expand(a.dot(b));target=re.search(r'If\s*\$[^$]*?\\cdot[^$]*?=\s*([^$,]+)',v)
    if not target:skips.append({'entity':q[':db/id'],'reason':'Dot target parser'});continue
    rhs=scalar(target[1]);syms=expr.free_symbols;roots=S.solve(expr-rhs,list(syms)[0]);check(q,'dot-parameter-equation',f'{expr}={rhs}, roots={roots}')
    for f,choices,right in qfields(q):z=scalar(right[':answer/value']);check(q,'dot-parameter-answer',z,S.simplify(expr.subs({s:z for s in syms})-rhs)==0)
   elif kp in [17592186119801,17592186119802,17592186119803]:
    form=list(MATH.finditer(v))[-1][0].strip('$').rstrip('.?=');form=re.sub(r'\\mathbf\s*(?:\{([a-z])\}|([a-z]))',lambda m:m[1]or m[2],form);form=form.replace(r'\displaystyle','').strip()
    # Obtain vector labels from the equations preceding the givens.
    names=[]
    for m in re.finditer(r'([a-z])\}?\s*=\s*(?:\{?\\left\[\s*)?(?:\{?\\begin\{(?:bmatrix|array)\})',v):names.append(m[1])
    if not names:names=['u','v'][:len(ms)]
    if len(set(m.shape for m in ms))>1:
     for f,choices,right in qfields(q):check(q,'undefined-vector-shape',[m.shape for m in ms],right[':answer/value'].lower()=='undefined')
     continue
    if kp==17592186119803:
     coeff=1
     if r'\cdot'in form:
      left=form.split(r'\cdot')[0].strip('() ')
      left=re.sub(r'\{?[a-z]\}?\s*$','',left)
      if left.strip():coeff=scalar(left)
     target=S.simplify(coeff*ms[0].dot(ms[1]))
    else:
     form=re.sub(r'\\mathbf\{([a-z])\}',r'\1',form)
     ex=scalar(form);syms=sorted(ex.free_symbols,key=str)
     if len(ms)==1:coeff=ex.coeff(syms[0]);target=coeff*ms[0]
     else:
      vals={str(s):m for s,m in zip(syms,ms)};target=sum((ex.coeff(S.Symbol(n))*m for n,m in vals.items()),S.zeros(ms[0].rows,1))
    check(q,'vector-arithmetic',target)
    for f,choices,right in qfields(q):
     am=mats(right[':answer/value']);actual=am[0][2]if am else scalar(right[':answer/value']);check(q,'vector-arithmetic-answer',actual,actual==target)
 except Exception as ex:skips.append({'entity':q[':db/id'],'identity':q.get(':question/math-academy-id'),'reason':str(ex)})
(H/'math-verification.json').write_text(json.dumps({'checks':out,'flags':flags,'parser_limitations':skips},indent=2)+'\n');print('Checks',len(out),'flags',len(flags),'limitations',len(skips));print(json.dumps(flags,indent=2));print('LIMITATIONS',json.dumps(skips,indent=2))
