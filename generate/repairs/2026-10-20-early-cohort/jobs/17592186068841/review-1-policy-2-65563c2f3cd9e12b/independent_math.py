"""Small independent reader for the elementary TeX actually printed by these cases.
No generator spec, mapping, bank, family-equivalence helper or metadata is used as a math oracle.
"""
import re,json,sys
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
X,Y,K,C,D=s.symbols('x y K C D',real=True)
class Tex:
 def __init__(self,t):
  t=t.replace('\u2061','').replace('′',"'")
  t=t.replace(r'\frac{\text{d}y}{\text{d}x}','D').replace(r'\dfrac{\textrm{d}y}{\textrm{d}x}','D')
  t=re.sub(r'\{y\}\^\{[\u2032\']\}', 'D',t).replace("y'",'D')
  t=re.sub(r'\\operatorname\{(sin|cos|arcsin|arctan|ln|sec)\}',lambda m:'\\'+m[1]+' ',t)
  t=t.replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace(r'\!',' ').replace(r'\cdot','*').replace(r'\times','*').replace(r'\,','')
  self.a=re.findall(r'\\[A-Za-z]+|\d+(?:\.\d+)?|[A-Za-z]|[^\s]',t);self.i=0
 def peek(self):return self.a[self.i] if self.i<len(self.a) else ''
 def take(self):v=self.peek();self.i+=1;return v
 def atom(self):
  a=self.take()
  if a in ['{','(','[']:
   v=self.expr();end={ '{':'}','(':')','[':']'}[a];assert self.take()==end,(a,self.a,self.i);return v
  if a==r'\frac' or a==r'\dfrac':return self.atom()/self.atom()
  if a==r'\sqrt':
   degree=2
   if self.peek()=='[': degree=self.atom()
   return self.atom()**(s.Integer(1)/degree)
  fun={r'\sin':s.sin,r'\cos':s.cos,r'\sec':s.sec,r'\arcsin':s.asin,r'\arctan':s.atan,r'\ln':s.log,r'\log':s.log,r'\exp':s.exp}
  if a in fun:
   if self.peek()=='^':
    self.take();power=self.signed();return fun[a](self.power())**power
   return fun[a](self.power())
  if a=='e':return s.E
  if a in 'xyKCD' and len(a)==1:return {'x':X,'y':Y,'K':K,'C':C,'D':D}[a]
  if re.fullmatch(r'\d+(?:\.\d+)?',a):return s.Rational(a)
  raise ValueError('Unknown token '+repr(a))
 def power(self):
  v=self.atom()
  if self.peek()=='^':self.take();v=v**self.signed()
  return v
 def signed(self):
  if self.peek() in ['+','-']:
   t=self.take();return self.signed()*(1 if t=='+' else -1)
  return self.power()
 def product(self):
  v=self.signed()
  while self.peek() and self.peek() not in ['+','-','}',')',']','=']:
   if self.peek()=='*':self.take();v*=self.signed()
   elif self.peek()=='/':self.take();v/=self.signed()
   else:v*=self.signed()
  return v
 def expr(self):
  v=self.product()
  while self.peek() in ['+','-']:
   op=self.take();v+=(1 if op=='+' else -1)*self.product()
  return v
 def all(self):
  v=self.expr();assert self.i==len(self.a),(self.a,self.i);return v

def parse(t):return Tex(t).all()
def value(t):return parse(t.split('=',1)[-1])
def rhs(prompt):
 ode=re.findall(r'\$([^$]+)\$',prompt)[0].rstrip('.,')
 l,r=ode.split('=');return s.solve(parse(l)-parse(r),D)[0]
def correct(r):
 f=r['question'][':question/answer-fields'][0];id=f[':answer-field/correct'][1];return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==id)
def save(n,x):(ROOT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def test():
 replay=json.loads((ROOT/'source-replay.json').read_text());source=json.loads((ROOT/'source-analysis.json').read_text())['source_cases'];report=[]
 for r in replay:
  name=r['generation']['template'];q=next(q for q in source if q['ma_id']==name);f=r['question'][':question/answer-fields'][0];sf=q['fields'][0]
  try:
   got=[value(a[':answer/value']) for a in f[':answer-field/choices']];wanted=[value(a[':answer/value']) for a in sf[':answer-field/choices']]
   bank_match=len(got)==len(wanted) and all(any(s.simplify(v-w)==0 for w in got) for v in wanted)
   key_match=s.simplify(value(correct(r))-value(sf[':answer-field/correct'][':answer/value']))==0
   report.append({'template':name,'source_id':q['id'],'bank_match':bank_match,'key_match':key_match,'got_bank':[str(v) for v in got],'source_bank':[str(v) for v in wanted]})
  except Exception as e:report.append({'template':name,'error':repr(e)})
 save('source-bank-comparison.json',report)
 records=[]
 for file in ['easy-grid.json','normal-cases.json','batch.json','leak-cases.json','fresh-render-input.json']:
  for i,r in enumerate(json.loads((ROOT/file).read_text())):
   q=r['question'];out={'file':file,'index':i,'id':q[':question/id']}
   try:
    f=q[':question/answer-fields'][0];ode=rhs(q[':question/problem']);out['printed_rhs']=str(ode);valid=[];tests=[]
    for a in f[':answer-field/choices']:
     expr=value(a[':answer/value'])
     if f[':answer-field/type'].endswith('/blank'):
      # Recover the coefficient outside the displayed blank, not metadata.
      m=re.search(r'\$y=-(\d+)\(',q[':question/problem']);expr=-int(m[1])/(expr+K) if m else s.sqrt(expr+K)
     residual=s.diff(expr,X)-ode.subs(Y,expr)
     numerical=[]
     for x,k in [(s.Rational(1,5),3),(s.Rational(1,2),7),(s.Rational(4,5),11)]:
      sub={X:x,K:k,C:k};res=complex(residual.subs(sub).evalf(30));scale=1+abs(complex(s.diff(expr,X).subs(sub).evalf(30)))+abs(complex(ode.subs(Y,expr).subs(sub).evalf(30)));numerical.append(abs(res)/scale<1e-12)
     if all(numerical) and bool(expr.free_symbols & {K,C}):valid.append(a[':answer/id'])
     tests.append({'choice':a[':answer/value'],'substituted_solution':str(expr),'residual':str(residual),'zero_at_independent_points':numerical,'has_arbitrary_constant':bool(expr.free_symbols & {K,C})})
    out.update({'valid_choices':valid,'expected_choice':f[':answer-field/correct'][1],'passed':valid==[f[':answer-field/correct'][1]],'checks':tests})
   except Exception as e:out.update({'passed':False,'error':repr(e)})
   records.append(out)
 save('math-results.json',{'method':'Independent printed-TeX parser; solve printed ODE for derivative; substitute each printed option and evaluate exact symbolic derivative residual at x=1/5,1/2,4/5 and C=K=3,7,11. Local positive branches tested; not a global domain proof.','records':records})
 print('bank',len(report),'failures',[v for v in report if not v.get('bank_match') or not v.get('key_match')]);print('math',len(records),'failures',[{k:v for k,v in r.items() if k!='checks'} for r in records if not r['passed']][:8])
if __name__=='__main__':test()
