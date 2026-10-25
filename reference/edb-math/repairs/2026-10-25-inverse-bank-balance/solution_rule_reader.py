def equal(a,b):return s.simplify(s.expand_log(a-b,force=True))==0
def check(row):
 q=row['question'];problem=q[':question/problem'];sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
 body,var,lo,hi=integral(re.findall(r'\$\$\s*(.*?)\s*\$\$',problem,re.S)[0]);assert var==X
 inner=scalar(re.search(r'Let \$u=(.*?)\$',sol)[1]);du=scalar(re.search(r'\\mathrm\{d\}u=\((.*?)\)\\,',sol)[1]);assert equal(s.diff(inner,X),du)
 substitution=next(b for b in blocks if b.count(r'\int')==2).replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace(r'\\','').replace('&','')
 left,right=substitution.split('=',1);leftbody,_,ll,lh=integral(left);trans,uv,u0,u1=integral(right.rstrip('.'))
 assert equal(leftbody,body)and lo==ll and hi==lh and uv==U
 assert equal(trans.subs(U,inner)*du,body),(body,trans,inner,du)
 if lo is not None:
  assert lo<hi and equal(inner.subs(X,lo),u0)and equal(inner.subs(X,hi),u1)
 f=q[':question/answer-fields'][0];key=next(a[':answer/value']for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1])
 easy=row['question'][':question/difficulty'].endswith('/easy')
 if easy:
  vals=[];matches=[]
  for a in f[':answer-field/choices']:
   t,v,l,h=integral(a[':answer/value']);assert v==U and l==u0 and h==u1
   # All banks differ only by scalar on this nonzero integrand.
   ratio=s.simplify(t/trans);assert ratio.is_number and ratio!=0
   assert all(not equal(ratio,z)for z in vals);vals.append(ratio)
   if ratio==1:matches.append(a[':answer/id'])
  assert matches==[f[':answer-field/correct'][1]]
  answer=None
 else:
  formula=next(b for b in blocks if b.lstrip().startswith(r'\int') and b.count(r'\int')==1 and b.strip().rstrip('.').endswith('+C')).strip().rstrip('.');lhs,rhs=formula.rsplit('=',1);tf,tv,_,_=integral(lhs);primitive=scalar(rhs.removesuffix('+C'))
  derivative=s.diff(primitive,U)
  # SymPy differentiates asec with sqrt(1-1/u²); verify on both real components.
  if derivative.has(s.Abs)or tf.has(s.Abs):
   for sign in(1,-1):
    z=s.Symbol('v',positive=True);assert equal((derivative-tf).subs(U,sign*(z+1)),0),(derivative,tf)
  else:assert equal(derivative,tf),(derivative,tf)
  factor=s.simplify(trans/tf);assert not factor.has(U)
  if lo is None:
   value=scalar(key.removesuffix('+C'));expected=factor*primitive.subs(U,inner)
   assert equal(value,expected),(key,expected)
   answer=value
   if f[':answer-field/type']==':answer-field.type/radio':
    values=[scalar(a[':answer/value'].removesuffix('+C'))for a in f[':answer-field/choices']]
    assert len({str(s.simplify(v/expected))for v in values})==5
    assert sum(equal(v,expected)for v in values)==1
  else:
   answer=factor*(primitive.subs(U,u1)-primitive.subs(U,u0));assert equal(scalar(key),answer),(key,answer)
 assert blocks[-1].strip().rstrip('.')==key+('+C'if not easy and lo is None and f[':answer-field/type']==':answer-field.type/blank'else '')
 return key,lo,answer

