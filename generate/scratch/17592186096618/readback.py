"""Small independent reader for the actually displayed algebra in this generator.

No generation parameters are consulted. Supports only the recorded source grammar
and authored same-KP peers; unknown tokens and unconsumed text are failures.
"""
import re
import sympy as s
X=s.Symbol('x',positive=True)
UF=s.Function('u')(X);VF=s.Function('v')(X)
def normalize(t):
 t=t.replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 t=re.sub(r'\\operatorname\{(ln|sin|cos|tan|log)\}',r'\1',t)
 t=re.sub(r'\{?log\}?_\{(\d+)\}',r'log_\1',t)
 t=re.sub(r'\{?sec\}?\^\{2\}\(x\)',r'sec(x)^2',t)
 t=re.sub(r'\{([uv])\}\^\{[′\']\}\(x\)',r"\1'",t)
 t=re.sub(r'([uv])\(x\)',r'\1',t)
 t=re.sub(r'\^\{[′\']\}',"'",t)
 t=t.replace('′',"'")
 t=re.sub(r'\\(ln|log|sin|cos|tan|sec|frac)',r'\1',t)
 return t
class Reader:
 def __init__(self,t):
  t=normalize(t);self.ts=re.findall(r'log_\d+|frac|ln|log|sin|cos|tan|sec|\d+|[xuve]|[{}()+*/^\-\']',t)
  rem=re.sub(r'log_\d+|frac|ln|log|sin|cos|tan|sec|\d+|[xuve]|[{}()+*/^\-\']|\s','',t)
  assert not rem,(t,rem);self.i=0
 def peek(self):return self.ts[self.i] if self.i<len(self.ts) else None
 def take(self):q=self.peek();self.i+=1;return q
 def atom(self):
  a=self.take();assert a is not None
  if a in ('+','-'):return self.atom()*(1 if a=='+' else -1)
  if a in ('{','('):
   out=self.expr();assert self.take()==('}' if a=='{' else ')');return out
  if a=='frac':return self.atom()/self.atom()
  if a.isdigit():return s.Integer(a)
  if a in ('x','e','u','v'):return {'x':X,'e':s.E,'u':UF,'v':VF}[a]
  arg=self.atom() if self.peek() in ('(','{') else self.power()
  if a.startswith('log_'):return s.log(arg)/s.log(int(a[4:]))
  if a=='log':return s.log(arg)/s.log(10)
  return {'ln':s.log,'sin':s.sin,'cos':s.cos,'tan':s.tan,'sec':s.sec}[a](arg)
 def power(self):
  if self.peek() in ('+','-'):
   op=self.take();return self.power()*(1 if op=='+' else -1)
  a=self.atom()
  while self.peek() in ('^',"'"):
   q=self.take();a=s.diff(a,X) if q=="'" else a**self.atom()
  return a
 def term(self):
  a=self.power()
  while self.peek() not in (None,'+','-','}',')'):
   if self.peek() in ('*','/'):
    op=self.take();b=self.power();a=a*b if op=='*' else a/b
   else:a*=self.power()
  return a
 def expr(self):
  a=self.term()
  while self.peek() in ('+','-'):
   op=self.take();b=self.term();a=a+b if op=='+' else a-b
  return a
 def read(self):
  a=self.expr();assert self.i==len(self.ts),(self.ts,self.i);return a
def read(t):return Reader(t).read()
def equal(a,b):return s.simplify(s.expand(a-b))==0
def math_rows(solution):
 body=solution.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0]
 return body.split(' & =',1)[1].split(r' \\  & =')
def check(rec):
 q=rec['question'];pr=q[':question/problem'];sol=q[':question/worked-solution'];f=q[':question/answer-fields'][0]
 product=re.search(r'f\(x\)\s*=\s*(.*?)\$',pr).group(1).rstrip(',')
 displayed=read(product)
 utext=re.search(r'\$u\(x\)\s*=\s*(.*?)\$',sol).group(1)
 vtext=re.search(r'\$v\(x\)\s*=\s*(.*?)\.\$',sol).group(1)
 u,v=read(utext),read(vtext);assert equal(displayed,u*v),('factors',product,utext,vtext)
 d=s.diff(displayed,X)
 rows=math_rows(sol)
 template=rec['generation']['template']
 generic=template.startswith(('base_log','binomial','trinomial')) or template in ('log_log_radio','power_log_radio')
 assert len(rows)==(4 if generic or template in ('linear_base_radio','power_exp_radio') else 3),('stage count',template)
 assert normalize(rows[0]).count("'")==2,('formal-rule stage',rows[0])
 if generic:assert normalize(rows[1]).count("'")==2,('actual factor operator stage',rows[1])
 for row in rows[2 if generic else 1:]:assert "'" not in normalize(row),('derivatives not evaluated',row)
 for row in rows:
  value=read(row).subs({s.diff(UF,X):s.diff(u,X),s.diff(VF,X):s.diff(v,X),UF:u,VF:v},simultaneous=True)
  assert equal(value,d),('solution row',row,value,d)
 answers=f[':answer-field/choices'];aid=f[':answer-field/correct'][1]
 parsed=[(a,read(a[':answer/value'])) for a in answers]
 assert all(not equal(a[1],b[1]) for i,a in enumerate(parsed) for b in parsed[i+1:]),'equivalent bank members'
 if f[':answer-field/type'].endswith('/radio'):
  assert [a[':answer/id'] for a,answer_value in parsed if equal(answer_value,d)]==[aid],('correct designation',product)
 else:
  a,answer_value=parsed[0];assert a[':answer/id']==aid
  response=pr.split('\n\n',1)[1].split('=',1)[1].replace('{{field-1}}','('+a[':answer/value']+')').replace('$','')
  assert equal(read(response),d),('fragment reinsertion',response)
 return {'product':s.sstr(displayed),'derivative':s.sstr(d),'u':s.sstr(u),'v':s.sstr(v),'rows':len(math_rows(sol))}
