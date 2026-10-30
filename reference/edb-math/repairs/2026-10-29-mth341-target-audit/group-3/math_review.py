import json,re,sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
H=Path(__file__).resolve().parent;S=json.loads((H/'current.json').read_text());qs=json.loads((H/'proposed-questions.json').read_text());owners={q:k for t,k,q in S['links']};checks=[];fail=[]
syms={n:sp.Symbol(n)for n in'xyztspabc dijk'.replace(' ','')};x,y,z=map(syms.get,'xyz');V=sp.Matrix([x,y,z])
def plain(t):
 t=re.sub(r'\\(?:hspace|bbox)\[[^\]]*\]|\\hspace\{[^{}]*\}|\\color(?:\[[^\]]*\])?\{[^{}]*\}','',t);t=re.sub(r'\\(?:mathbf|mathbb|mathrm|mathit|displaystyle|textstyle|left|right|quad|qquad)\b','',t);t=re.sub(r'(?<!\\)\\[,;!: ]','',t);return t.replace('−','-').replace(r'\langle','⟨').replace(r'\rangle','⟩').replace(r'\cdot','*').replace('$','').strip().rstrip('.,?')
def scalar(t):
 t=plain(t)
 def group(st,pos):
  while pos<len(st)and st[pos].isspace():pos+=1
  if st[pos]!='{':return st[pos],pos+1
  depth=1;j=pos+1
  while depth:depth+=(st[j]=='{')-(st[j]=='}');j+=1
  return st[pos+1:j-1],j
 while(m:=re.search(r'\\(?:dfrac|tfrac|frac|sqrt)',t)):
  a,end=group(t,m.end())
  if m[0]==r'\sqrt':replacement='sqrt('+str(scalar(a))+')'
  else:b,end=group(t,end);replacement='('+str(scalar(a))+')/('+str(scalar(b))+')'
  t=t[:m.start()]+replacement+t[end:]
 t=t.replace('^','**').replace('{','(').replace('}',')');t=re.sub(r'(?<=[0-9)])(?=[A-Za-z])','*',t);t=re.sub(r'\s+',' ',t);assert '\\'not in t,t
 return sp.simplify(parse_expr(t,local_dict=syms,transformations=standard_transformations+(implicit_multiplication_application,)))
def vecs(t):
 t=plain(t);out=[]
 for m in re.finditer(r'⟨([^⟨⟩]*)⟩|\\begin\{(?:bmatrix|array)\}(.*?)\\end\{(?:bmatrix|array)\}',t,re.S):
  if m[1]is not None:cells=m[1].split(',')
  else:
   b=m[2];b=re.sub(r'^\{[clr]+\}','',b);cells=b.split('\\\\')
  if len(cells)!=3:continue
  try:v=sp.Matrix([scalar(c)for c in cells]);out.append((m.start(),m.end(),v))
  except Exception:pass
 return out

def vector(t):
 vv=vecs(t)
 if vv:return vv[0][2]
 e=scalar(t);return sp.Matrix([e.coeff(syms[n])for n in'ijk'])
def points(t):return[sp.Matrix([scalar(c)for c in m[1].split(',')])for m in re.finditer(r'(?<![A-Za-z])(?:[A-Z])\(([^()]*)\)',t)if len(m[1].split(','))==3]
def direction(t):
 vv=vecs(t)
 if vv:return vv[-1][2]
 rows=[]
 if r'\begin{aligned}'in t:
  body=t.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];rows=[scalar(row.split('=',1)[1]).coeff(syms['t'])for row in body.split(r'\\')if '='in row]
  if len(rows)==3:return sp.Matrix(rows)
 for n in'xyz':
  m=re.search(n+r'\s*&?=([^\\$]*?)(?=\\\\|\\end|$)',t,re.S)
  if m:rows.append(scalar(m[1]).coeff(syms['t']))
 if len(rows)==3:return sp.Matrix(rows)
 fs=list(re.finditer(r'\\(?:dfrac|frac)\{([^{}]*)\}\{([^{}]*)\}',t));ds={}
 for m in fs:
  for n in'xyz':
   if n in m[1]:ds[n]=scalar(m[2])
 if len(ds)>=2:return sp.Matrix([ds.get(n,0)for n in'xyz'])
 raise ValueError('No direction '+t)
def parallel(a,b):return a!=sp.zeros(3,1)and b!=sp.zeros(3,1)and all(sp.simplify(c)==0 for c in a.cross(b))
def correct(q):
 f=q.get(':question/answer-fields',[])
 return{a[':answer-field/key']:next(b[':answer/value']for b in a[':answer-field/choices']if b[':db/id']==a[':answer-field/correct'][':db/id'])for a in f}
def response(q,vals):
 p=q[':question/problem'];idx=p.index('{{');start=p.rfind('\n\n',0,idx);body=p[start:]
 # Response prefix may be in the immediately previous inline math fragment.
 if start>=0 and body.lstrip().startswith('{{'):
  prev=p.rfind('\n\n',0,start)
  if prev>=0 and '$'in p[prev:start]:body=p[prev:]
 return re.sub(r'\s+',' ',re.sub(r'\{\{([^{}]+)\}\}',lambda m:'('+vals[m[1]]+')',body).replace('$','')).strip()
def equation(t):
 t=plain(t);left,right=t.split('=')[-2:];return scalar(left)-scalar(right)
def plane_from_answer(value):
 assert not vecs(value.rsplit('=',1)[1]),'Vector right-hand side cannot equal scalar dot product'
 vv=vecs(value)
 if len(vv)>=2 and r'\cdot'in value:return vv[-1][2],-vv[-1][2].dot(vv[-2][2])
 if len(vv)==1 and r'\cdot'in value:
  return vv[0][2],-scalar(value.rsplit('=',1)[1])
 if r'\cdot'in value and '='in value:
  left,right=value.rsplit('=',1);left=left.split(r'\cdot')[-1].strip().strip('()');return vector(left),-scalar(right)
 e=equation(value);return sp.Matrix([e.coeff(v)for v in[x,y,z]]),e.subs({x:0,y:0,z:0})
for q in qs:
 eid=q[':db/id'];kp=owners[eid];p=q[':question/problem'];vals=correct(q)if q.get(':question/answer-fields')else{};sol=q.get(':question/worked-solution','');result={'entity':eid,'kp':kp}
 if kp not in[17592186119829,17592186119830,17592186119831,17592186119933,17592186119934,17592186119935,17592186119936,17592186119832,17592186119833,17592186119834,17592186119835]:continue
 try:
  if kp==17592186119830:
   vv=vecs(p);a,n=vv[0][2],vv[1][2];ratio=re.search(r'\\(?:dfrac|frac)\{([abc])\}\{([abc])\}',p);assert ratio
   u,w=map(syms.get,ratio.groups());ans=sp.solve(sp.Eq(a.dot(n),0),u)[0]/w;expected=sp.simplify(ans);actual=scalar(vals['selection'])if vals else expected;assert sp.simplify(actual-expected)==0
   result.update(expected=str(expected),proof='Parallel direction is orthogonal to normal; solve the one linear relation.')
  elif kp==17592186119934:
   vv=vecs(p);d1,d2=vv[-2][2],vv[-1][2];n=d1.cross(d2);assert n!=sp.zeros(3,1)
   actual=vector(vals['selection'])if vals else n;assert parallel(actual,n);result.update(normal=list(n),proof='Chosen nonzero normal perpendicular to both independent directions.')
  elif kp in[17592186119933,17592186119935,17592186119936]:
   pts=points(p);vv=vecs(p);base=pts[0]
   if kp==17592186119935 or eid==17592186304926:
    d1,d2=vv[1][2],vv[3][2]
    if eid==17592186304926:d2=vv[2][2]-vv[0][2]
   elif kp==17592186119933:d1,d2=vv[0][2],vv[1][2]
   elif len(pts)==3:d1,d2=pts[1]-pts[0],pts[2]-pts[0]
   else:d1,d2=vv[0][2],pts[1]-pts[0]
   n=d1.cross(d2);assert n!=sp.zeros(3,1)
   if vals:
    ans=vecs(vals['selection']);assert len(ans)==3
    ap,ad1,ad2=[a[2]for a in ans];assert ad1.cross(ad2)!=sp.zeros(3,1);assert n.dot(ad1)==0 and n.dot(ad2)==0 and sp.simplify(n.dot(ap-base))==0
   result.update(point=list(base),directions=[list(d1),list(d2)],normal=list(n),proof='Rank-two direction span, base-point incidence, and answer-plane equivalence.')
  elif kp==17592186119834:
   match=re.search(r'\$([^$]*=[^$]*)\$',p);e=equation(match[1]);n=sp.Matrix([e.coeff(v)for v in[x,y,z]]);constant=e.subs({x:0,y:0,z:0})
   value=vals['selection']if 'selection'in vals else response(q,vals)if vals else None
   if value:
    an,ac=plane_from_answer(value);assert parallel(n,an);idx=next(i for i in range(3)if n[i]!=0);assert sp.simplify(ac/ an[idx]-constant/n[idx])==0
   result.update(normal=list(n),constant=constant,proof='Point-normal answer expands to a nonzero scalar multiple of the given Cartesian equation.')
  else:
   pts=points(p);base=pts[0]
   if 'perpendicular to the vector'in p:
    st=p.index('perpendicular to the vector');sub=p[st:];vv=vecs(sub)
    n=vv[0][2]if vv else vector(re.search(r'=([^$]*)\$',sub)[1])
   elif 'perpendicular to the line'in p:
    if len(pts)==3:n=pts[2]-pts[1]
    else:n=direction(p[p.index('perpendicular to the line'):])
   elif len(pts)==3:n=(pts[1]-pts[0]).cross(pts[2]-pts[0])
   else:vv=vecs(p);n=vv[-2][2].cross(vv[-1][2])
   assert n!=sp.zeros(3,1);constant=-n.dot(base)
   if vals:
    value=vals['selection']if'selection'in vals else response(q,vals);an,ac=plane_from_answer(value);assert parallel(n,an),(n,an,value);assert sp.simplify(an.dot(base)+ac)==0
   result.update(point=list(base),normal=list(n),constant=constant,proof='Correct nonzero normal from given vector/line or cross product; answer contains the required point.')
  choice_checks=[]
  for f in q.get(':question/answer-fields',[]):
   if f[':answer-field/type'][':db/ident']not in[':answer-field.type/radio',':answer-field.type/select']:continue
   qualified=[]
   for a in f[':answer-field/choices']:
    value=a[':answer/value'];ok=False
    try:
     if kp==17592186119830:ok=sp.simplify(scalar(value)-expected)==0
     elif kp==17592186119934:ok=parallel(vector(value),n)
     elif kp in[17592186119933,17592186119935,17592186119936]:
      av=vecs(value);assert len(av)==3;ap,ad1,ad2=[r[2]for r in av];ok=ad1.cross(ad2)!=sp.zeros(3,1)and n.dot(ad1)==0 and n.dot(ad2)==0 and sp.simplify(n.dot(ap-base))==0
     else:
      an,ac=plane_from_answer(value);ok=parallel(an,n)
      if ok:
       idx=next(i for i in range(3)if n[i]!=0);ok=sp.simplify(ac/an[idx]-constant/n[idx])==0
    except Exception:pass
    if ok:qualified.append(a[':db/id'])
   right=f.get(':answer-field/correct',{}).get(':db/id');assert qualified==[right],('Nonunique or wrong key',f[':db/id'],qualified,right)
   choice_checks.append({'field':f[':db/id'],'all_options_checked':len(f[':answer-field/choices']),'unique_mathematically_correct_choice':right})
  result['choice_checks']=choice_checks
  checks.append(result)
 except Exception as e:fail.append({**result,'error':repr(e),'prompt':p,'answers':vals})
(H/'plane-math-verification.json').write_text(json.dumps({'passed':not fail,'checks':checks,'failures':fail,'database_writes':0},default=str,indent=2)+'\n');print('Plane checks',len(checks),'failures',len(fail));print([(x['entity'],x['error'])for x in fail])
