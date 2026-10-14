"""Independently parse displayed polynomials, equations and mathematical banks."""
import re
import sympy as sp
x=sp.Symbol('x',real=True)
def scalar(s):
 s=s.strip().rstrip('.').replace('−','-').replace(r'\,','').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*')
 s=re.sub(r'\\(?:d?frac)\s*\{([^{}]+)\}\s*\{([^{}]+)\}',r'(\1)/(\2)',s)
 s=s.replace('{','(').replace('}',')').replace('^','**').replace(' ','')
 s=re.sub(r'(\d|\))(?=x)',r'\1*',s)
 s=re.sub(r'([0-9x]|\))(?=\()',r'\1*',s)
 assert re.fullmatch(r'[x0-9+*/().-]+',s),s
 return sp.sympify(s,locals={'x':x},rational=True)
def values(s):
 s=re.sub(r'^\s*x\s*=','',s).replace(r'\,','')
 return tuple(sorted(scalar(z) for z in s.split(',') if z.strip()))
def task(q):
 text=q[':question/problem'];f=scalar(re.search(r'\$y\s*=\s*([^$]+)\$',text)[1]);m=scalar(re.search(r'slope of \$([^$]+)\$',text)[1])
 roots=tuple(sorted(sp.solve(sp.diff(f,x)-m,x)))
 family='positive' if ('positive' in text) else 'all' if '$x$-coordinates' in text else 'quadratic' if sp.degree(f,x)==2 else 'repeated'
 ans=(max(roots),) if family=='positive' else roots
 assert roots and all(r.is_Rational for r in roots)
 if family=='positive':assert sum(bool(r>0) for r in roots)==1 and min(roots)<0
 if family=='repeated':assert len(roots)==1
 return f,m,roots,ans,family

def fingerprint(q):
 import hashlib,json
 f,m,roots,ans,family=task(q)
 data={'slope_equation':list(map(str,sp.Poly(sp.diff(f,x)-m,x).monic().all_coeffs())),'requested_branch':family}
 return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def check(rec):
 q=rec['question'];meta=rec['generation'];f,m,roots,ans,family=task(q);df=sp.diff(f,x)
 assert fingerprint(q)==meta['mathematical_fingerprint']
 # All intermediate evaluated rows are read from their actual TeX.
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
 dr=[r.strip() for r in blocks[0].split(r'\\') if r.strip()]
 initial=re.search(r'\\left\((.*?)\\right\)',dr[0]);assert initial and scalar(initial[1])==f
 assert len(dr)==3
 assert all(sp.expand(scalar(r.split('&=')[1])-df)==0 for r in dr[1:])
 rows=[r.strip() for r in blocks[1].split(r'\\') if r.strip()]
 for row in rows:
  left,right=row.split('&=');left=left.strip();right=right.strip()
  if left=='x':assert values(right)==roots
  else:
   equation=scalar(left)-scalar(right)
   assert tuple(sorted(sp.solve(equation,x)))==roots,(row,roots)
 if family=='positive':assert f'x={sp.latex(ans[0])}' in sol.split('Since $x>0$')[1]
 else:
  final=re.search(r'equal to \$([^$]+)\$ at .*?where \$x=([^$]+)\$',sol)
  assert final and scalar(final[1])==m and values(final[2])==ans
 fields=q[':question/answer-fields'];assert len(fields)==1
 field=fields[0];assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
 opts=field[':answer-field/choices'];bank=[values(a[':answer/value']) for a in opts]
 assert len(bank)==len(set(bank)) and bank.count(ans)==1
 correct=next(a for a,v in zip(opts,bank) if v==ans)
 assert field[':answer-field/correct']==[':answer/id',correct[':answer/id']]
 assert len({a[':answer/id'] for a in opts})==len(opts)
 if field[':answer-field/type'].endswith('/blank'):
  assert len(opts)==1 and not opts[0][':answer/value'].startswith('x=')
  expected=[ans]
 else:
  assert len(opts)==5
  profile=meta['bank_profile'];r=ans[0]
  if profile in ('quadratic_radio','cubic_repeated'):expected=[(r,),(-r,),(-2*r,),(2*r,),(sp.Integer(0),)]
  elif profile=='positive_offsets':expected=[(r,),(r-1,),(r+1,),(r-2,),(r-3,)]
  elif profile=='positive_multiples':expected=[(r,),(12*r,),(2*r,),(3*r,),(4*r,)]
  else:
   u,v=roots;expected=[(u,v),(v,),(-v,),(-u,),tuple(sorted((-v,-u)))]
 assert set(bank)==set(expected)
 assert q[':question/difficulty']==':question.difficulty/moderate'
 return ans

def check_source(q):
 """Validate the evaluated derivative, every slope equation and conclusion.
 Original derivative-operator expansions are retained as evidence; the evaluated
 derivative is independently checked against differentiation of printed f.
 """
 f,m,roots,ans,family=task(q)
 field=q[':question/answer-fields'][0];bank=[values(a[':answer/value']) for a in field[':answer-field/choices']]
 assert len(bank)==len(set(bank)) and bank.count(ans)==1
 assert values(field[':answer-field/correct'][':answer/value'])==ans
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)>=2
 dr=[r.strip() for r in blocks[0].split(r'\\') if r.strip()]
 assert sp.expand(scalar(re.split(r'&\s*=',dr[-1])[1])-sp.diff(f,x))==0
 for row in [r.strip() for r in blocks[1].split(r'\\') if r.strip()]:
  left,right=re.split(r'&\s*=',row);left=left.strip();right=right.strip()
  if left=='x':assert values(right)==roots
  else:assert tuple(sorted(sp.solve(scalar(left)-scalar(right),x)))==roots
 # Conclusions containing a stated slope must agree with the prompt.
 for stated in re.findall(r'(?:slope of|equal to) \$([^$]+)\$',sol):
  assert scalar(stated.rstrip(' ,'))==m, 'Source conclusion has inconsistent slope'
 return ans
