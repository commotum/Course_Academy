"""Fail-closed independent reader of printed operands, differentials and stages."""
from pathlib import Path
import importlib.util,re
import sympy as s
spec=importlib.util.spec_from_file_location('kp68916_scalar',Path(__file__).parent/'reference/scalar_parser.py');P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
x,u,C=P.x,P.u,P.v

def scalar(t):
 t=t.strip().rstrip('.,').replace(r'\displaystyle','').replace(r'\dfrac',r'\frac').replace(r'\big','').replace(r'\left','').replace(r'\right','')
 t=re.sub(r'(?<![a-zA-Z])C(?![a-zA-Z])','v',t)
 return P.scalar(t)
def group(t,i):
 while i<len(t) and t[i].isspace():i+=1
 if t[i]=='{':
  d=1;j=i+1
  while d:d+=(t[j]=='{')-(t[j]=='}');j+=1
  return t[i+1:j-1],j
 m=re.match(r'(?:-?\d+|[a-z])',t[i:]);assert m,(t,i);return m[0],i+len(m[0])
def clean(t):
 t=t.strip().rstrip('.,').replace(r'\displaystyle','').replace(r'{\int }',r'\int').replace(r'\dfrac',r'\frac').replace(r'\big','').replace('{|}','|').replace(r'\,','').replace('⁡','')
 return t
DIFF=re.compile(r'(?:\\(?:text|textrm|mathrm)\{d\}\s*([xu])|d([xu]))')
def read_integral(t):
 t=clean(t);start=t.index(r'\int');i=start+4
 while i<len(t) and t[i].isspace():i+=1
 bounds=None
 if i<len(t) and t[i]=='_':
  lo,i=group(t,i+1);assert t[i]=='^';hi,i=group(t,i+1);bounds=(scalar(lo),scalar(hi))
 m=DIFF.search(t,i);assert m,('missing differential',t)
 body=scalar(t[i:m.start()]);v=scalar(m[1] or m[2]);assert v in (x,u)
 return {'body':body,'variable':v,'bounds':bounds,'start':start,'end':m.end(),'raw':t[start:m.end()]}
def primitive(body,v):
 if body.is_polynomial(v):return s.integrate(body,v)
 args={f.args[0] for f in body.atoms(s.Function)}
 for arg in args:
  if s.diff(arg,v)==0:continue
  for base,F in ((s.sec(arg)*s.tan(arg),s.sec(arg)),(s.csc(arg)*s.cot(arg),-s.csc(arg)),(s.sec(arg)**2,s.tan(arg)),(s.csc(arg)**2,-s.cot(arg))):
   ratio=s.cancel(body/base)
   if v not in ratio.free_symbols and v not in s.diff(arg,v).free_symbols:return ratio*F/s.diff(arg,v)
  # Source exception: polynomial in sec(x) times its derivative.
  z=s.Symbol('z');q=s.cancel(body/(s.sec(arg)*s.tan(arg)*s.diff(arg,v)));poly=q.subs(s.sec(arg),z)
  if poly.is_polynomial(z) and not poly.has(v):return s.integrate(poly,z).subs(z,s.sec(arg))
 raise AssertionError(('unsupported printed integrand',body,v))
def zero(z):
 z=s.expand(z)
 if z==0:return True
 if z.has(x):
  for val in (s.Rational(2,7),s.Rational(3,11)):
   n=s.N(z.subs(x,val),24)
   if n.is_real and n.is_finite and abs(n)>s.Float('1e-18'):return False
 z=s.expand_trig(z)
 return s.trigsimp(z)==0

def expression(t):
 t=clean(t);formal=[]
 while r'\int' in t:
  r=read_integral(t);F=primitive(r['body'],r['variable'])
  if r['bounds']:F=s.simplify(F.subs(r['variable'],r['bounds'][1])-F.subs(r['variable'],r['bounds'][0]))
  formal.append((r['body'],r['variable'],r['bounds']))
  t=t[:r['start']]+'('+s.latex(F)+')'+t[r['end']:]
 if '|' in t:
  t=t.replace(r'\,','');a,limits=t.split('|');assert limits.startswith('_');lo,i=group(limits,1);assert limits[i]=='^';hi,j=group(limits,i+1);assert not limits[j:].strip()
  F=scalar(a);value=s.simplify(F.subs(u,scalar(hi))-F.subs(u,scalar(lo)))
 else:value=scalar(t)
 return value,formal

def stages(q):
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==1
 rows=blocks[0].split(r'\\');out=[]
 for i,row in enumerate(rows):
  if i==0:
   lhs,rhs=row.split('&');out.append(('given',*expression(lhs)));row=rhs
  row=row.strip();assert row.startswith(('=','&')),(i,row)
  out.append(('stage',*expression(re.sub(r'^[&=\s]+','',row))))
 return out

def validate(q):
 given=read_integral(q[':question/problem']);v=given['variable'];assert v==x
 expected=primitive(given['body'],x)
 if given['bounds']:expected=s.simplify(expected.subs(x,given['bounds'][1])-expected.subs(x,given['bounds'][0]))
 sol=q[':question/worked-solution'];m=re.search(r'If we let \$u=(.*?),\$',sol);assert m
 subst=scalar(m[1]);assert subst.has(x)
 # Validate actual initial derivative and the displayed solved differential.
 block=re.search(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)[1]
 left,right=block.split('⟹');assert left.split('=',1)[0].strip()==r'\frac{\text{d}u}{\text{d}x}','wrong formal derivative operands';dr=scalar(left.split('=',1)[1]);assert zero(dr-s.diff(subst,x))
 lhs,rhs=right.split('=');d=DIFF.search(lhs);e=DIFF.search(rhs);assert d and e
 lv=scalar(d[1] or d[2]);rv=scalar(e[1] or e[2]);lc=scalar(lhs[:d.start()].strip().strip('\\,') or '1');rc=scalar(rhs[:e.start()].strip().strip('\\,') or '1')
 assert zero(lc*(1 if lv==x else dr)-rc*(1 if rv==x else dr)),'incorrect differential'
 if given['bounds']:
  lines=[z for z in sol.splitlines() if z.startswith('| $')];assert len(lines)==2
  xx=[scalar(z) for z in re.findall(r'\$([^$]+)\$',lines[0])[1:]];uu=[scalar(z) for z in re.findall(r'\$([^$]+)\$',lines[1])[1:]]
  assert tuple(xx)==given['bounds'];assert all(zero(subst.subs(x,a)-b) for a,b in zip(xx,uu))
 checked=stages(q)
 for label,value,formal in checked:
  for body,dv,bounds in formal:
   if label=='given':assert dv==x and zero(body-given['body']) and bounds==given['bounds']
   elif dv==u:
    # Actual substitution operand must contain no stale x and correct dx/du.
    assert not body.has(x)
    ratio=s.cancel(body.subs(u,subst)*s.diff(subst,x)/given['body']);assert not ratio.has(x) and ratio!=0,('wrong formal substituted body',body,given)
    if bounds:assert given['bounds'] and all(zero(subst.subs(x,a)-b) for a,b in zip(given['bounds'],bounds))
   else:raise AssertionError(('unexpected formal operand variable',dv))
  if given['bounds']:assert zero(value-expected),('definite stage',value,expected)
  else:
   value=value.subs(u,subst)
   assert zero(s.diff(value,x)-given['body']),('primitive stage',value,given)
 fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];bank=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 def eq(a,b):return zero(a-b) if given['bounds'] else zero(s.diff(a-b,x))
 for i,a in enumerate(bank):
  for b in bank[:i]:assert not eq(a,b),'duplicate bank modulo constant'
 good=[a[':answer/id'] for a,z in zip(f[':answer-field/choices'],bank) if eq(z,expected)]
 assert good==[f[':answer-field/correct'][1]],('wrong key',good,f)
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 return given,checked

def prose(t):
 t=re.sub(r'\$\$.*?\$\$|\$[^$]*\$',' MATH ',t,flags=re.S)
 return re.sub(r'[^a-zA-Z]+',' ',t).strip()
def fidelity(src,dst):
 si,di=read_integral(src[':question/problem']),read_integral(dst[':question/problem'])
 assert zero(si['body']-di['body']) and si['variable']==di['variable'] and si['bounds']==di['bounds']
 assert prose(src[':question/problem'])==prose(dst[':question/problem'])
 sf,df=src[':question/answer-fields'][0],dst[':question/answer-fields'][0];assert sf[':answer-field/type'][':db/ident']==df[':answer-field/type']
 sb=[scalar(a[':answer/value']) for a in sf[':answer-field/choices']];db=[scalar(a[':answer/value']) for a in df[':answer-field/choices']]
 def eq(a,b):return zero(a-b) if si['bounds'] else zero(s.diff(a-b,x))
 assert len(sb)==len(db) and all(sum(eq(a,b) for b in db)==1 for a in sb)
 if ':answer-field/correct'in sf:
  cv=scalar(sf[':answer-field/correct'][':answer/value']);dv=next(scalar(a[':answer/value']) for a in df[':answer-field/choices'] if a[':answer/id']==df[':answer-field/correct'][1]);assert eq(cv,dv)
 if ':question/worked-solution'in src:
  assert prose(src[':question/worked-solution'])==prose(dst[':question/worked-solution'])
  ss,ds=stages(src),stages(dst);assert len(ss)==len(ds)
  for (sl,sv,sf),(dl,dv,df) in zip(ss,ds):
   assert sl==dl and zero(sv-dv),('source stage differs',sv,dv)
   assert len(sf)==len(df)
   for (a,v,b),(c,w,d) in zip(sf,df):assert v==w and b==d and zero(a-c),'formal operands differ'
 return len(sb),len(sb)-1

def additive_components(t):
 """Read the two signed terms before arithmetic collection, without CAS collapse."""
 t=clean(t);i=t.find('(');assert i>=0 and t.endswith(')'),('missing outer arithmetic group',t)
 prefix=t[:i].strip();factor=scalar(prefix+'1' if prefix in ('','-','+') else prefix)
 inner=t[i+1:-1];depth=0;cuts=[]
 for j,c in enumerate(inner):
  if c in '({':depth+=1
  elif c in ')}':depth-=1
  elif c in '+-' and depth==0 and j>0:cuts.append(j)
 assert len(cuts)==1,('expected two individually evaluated endpoint components',t,cuts)
 j=cuts[0];return factor*scalar(inner[:j]),factor*scalar(inner[j:])
def structure(q,sid):
 """Source operation masks independently checked at originals and variants."""
 counts={'q-10143':4,'q-10157':4,'q-113983':3,'q-2203':4,'q-13663':6,'q-355818':6,'q-346368':6,'q-350060':4,'q-350071':6,'q-10578':4}
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)[1]
 raw=block.split(r'\\');rhs=[re.sub(r'^[&=\s]+','',z.split('&',1)[1] if i==0 else z).strip() for i,z in enumerate(raw)]
 assert len(rhs)==counts[sid],('operative row missing or extra',sid,len(rhs))
 chain=stages(q);formal=[len(z[2]) for z in chain]
 signature=[1,1,0,0] if sid=='q-113983' else [1,1,0,0,0] if sid in ('q-350060','q-10578') else [1,1,1,0,0] if sid in ('q-10143','q-10157','q-2203') else [1,1,1,0,0,0,0]
 assert formal==signature,('source formal-operator sequence changed',sid,formal)
 given=read_integral(q[':question/problem'])
 if not given['bounds']:return
 m=re.search(r'If we let \$u=(.*?),\$',q[':question/worked-solution']);sub=scalar(m[1]);a=s.diff(sub,x);b=sub.subs(x,0)
 lo,hi=[s.simplify(sub.subs(x,z)) for z in given['bounds']]
 F=s.simplify(primitive(given['body'],x).subs(x,(u-b)/a));expected=(s.simplify(F.subs(u,hi)),-s.simplify(F.subs(u,lo)))
 bar_index=1 if sid in ('q-350060','q-10578') else 2
 bar=clean(rhs[bar_index]);left,limits=bar.split('|');L,i=group(limits,1);assert limits[i]=='^';H,j=group(limits,i+1)
 assert scalar(L)==lo and scalar(H)==hi and vzero(scalar(left)-F),'incorrect primitive evaluation operands'
 # Explicit substituted-function stage and individually evaluated numeric stage.
 endpoint_index=None if sid=='q-350060' else bar_index+1
 numeric_index=None if sid=='q-10578' else bar_index+1 if sid=='q-350060' else bar_index+2
 for index in (endpoint_index,numeric_index):
  if index is None:continue
  parts=additive_components(rhs[index]);assert all(vzero(z-w) for z,w in zip(parts,expected)),('wrong individual endpoint component',sid,index,parts,expected)
  if index==endpoint_index:
   arguments=[]
   for match in re.finditer(r'\\(?:sec|csc|tan|cot)\(',rhs[index]):
    start=match.end()-1;depth=1;end=start+1
    while depth:depth+=(rhs[index][end]=='(')-(rhs[index][end]==')');end+=1
    arguments.append(scalar(rhs[index][start+1:end-1]))
   assert arguments and set(arguments)=={lo,hi},('stale endpoint function arguments',arguments,lo,hi)
  elif index==numeric_index:
   assert not scalar(rhs[index]).has(u,x) and not any(f.func in (s.sec,s.csc,s.tan,s.cot,s.sin,s.cos) for f in scalar(rhs[index]).atoms(s.Function)),'endpoint evaluation stage collapsed or unevaluated'

def vzero(z):return zero(z)
