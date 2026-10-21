import json, re, sys, pathlib, importlib.util, collections, hashlib, shutil, subprocess
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE.parent/'evidence'
ROOT.mkdir(exist_ok=True)
JOB=BASE.parent.parent
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PY=REPO/'.venv/bin/python'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed_generator',BASE.parent/'17592186068844.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,C=s.symbols('x y C', real=True)
FUN={'sin':s.sin,'cos':s.cos,'tan':s.tan,'sec':s.sec,'arcsin':s.asin,'arctan':s.atan,'arccos':s.acos,'ln':s.log}
class Parser:
 def __init__(self,t):
  t=t.replace('\u2061',' ').replace('\\left','').replace('\\right','').replace('\\,','').replace('\\cdot','*').replace('\\!','')
  t=re.sub(r'\\(?:text|textrm)\{[^}]*\}', '',t)
  t=re.sub(r'\\operatorname\{([^}]+)\}',r'\\\1 ',t)
  for f in ['cos','sec','sin','tan']:t=t.replace('{'+f+'}', '\\'+f)
  t=t.replace('\\dfrac','\\frac').replace('\\vert','|')
  self.ts=re.findall(r'\\[A-Za-z]+|\d+|[^\s]',t);self.i=0
 def peek(self):return self.ts[self.i] if self.i<len(self.ts) else ''
 def pop(self):t=self.peek();self.i+=1;return t
 def atom(self):
  t=self.pop()
  if t in ('{','('):
   z=self.expr();end=self.pop();assert end==('}' if t=='{' else ')'),(t,end,self.ts);return z
  if t=='|':z=self.expr(stopbar=True);assert self.pop()=='|';return s.log(z) if False else s.Abs(z)
  if t=='-':return -self.term()
  if t=='+':return self.term()
  if t=='\\frac':a=self.atom();b=self.atom();return a/b
  if t=='\\sqrt':return s.sqrt(self.atom())
  if t.startswith('\\') and t[1:] in FUN:
   power=s.Integer(1)
   if self.peek()=='^':self.pop();power=self.atom()
   return FUN[t[1:]](self.atom())**power
  if t.isdigit():return s.Integer(t)
  if t in ('x','y','C','e'):return {'x':x,'y':y,'C':C,'e':s.E}[t]
  raise ValueError(('unknown',t,self.ts))
 def term(self):
  z=self.atom()
  if self.peek()=='^':self.pop();z=z**self.atom()
  return z
 def product(self,stopbar=False):
  z=self.term()
  while self.peek() and self.peek() not in ('}',')','=','+','-') and not (stopbar and self.peek()=='|'):
   p=self.peek()
   if p in ('*','/'):self.pop();a=self.term();z=z*a if p=='*' else z/a
   else:z*=self.term()
  return z
 def expr(self,stopbar=False):
  z=self.product(stopbar)
  while self.peek() in ('+','-'):
   op=self.pop();a=self.product(stopbar);z=z+a if op=='+' else z-a
  return z
def parse(t):
 p=Parser(t);z=p.expr();assert p.i==len(p.ts),(t,p.ts[p.i:]);return z
def relation(t):a,b=t.strip().rstrip('.,').split('=');return parse(a),parse(b)-C
def deriv(z,v):
 z=z.replace(lambda a:a.func==s.log and a.args[0].func==s.Abs,lambda a:s.log(a.args[0].args[0]))
 return s.diff(z,v)
def zero(z):return s.simplify(s.trigsimp(z))==0
def dump(n,o):p=ROOT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def answer_id(f):
 a=f[':answer-field/correct'];return a[1] if isinstance(a,list) else a[':answer/id']
def field(r):return r['question'][':question/answer-fields'][0]
def shortcut(r):
 # No prompt, parameters, template, solution, or correct key used. Recover the
 # repeated R, -R, 2R bank construction from the equations alone.
 f=field(r);a=[(v,*map(s.expand,relation(v[':answer/value']))) for v in f[':answer-field/choices']];picks=[]
 for v,l,rhs in a:
  same=[rr for _,ll,rr in a if ll==l]
  if -rhs in same and s.expand(2*rhs) in same:picks.append(v[':answer/id'])
 return picks
def inspect_record(r):
 q=r['question'];f=field(r)
 # Read ODE directly from displayed prompt, ignoring generation metadata.
 ode=q[':question/problem'].split('=')[1].split('$')[0].replace('\\,','').rstrip('., ')
 h=r['generation']['parameters'].get('h',0);k=r['generation']['parameters'].get('k',0)
 u,v=s.symbols('u v',positive=True)
 sub={x:u-h,y:v-k}
 rhs=parse(ode).subs(sub,simultaneous=True)
 outcomes=[]
 for a in f[':answer-field/choices']:
  l,rr=relation(a[':answer/value']);l=l.subs(sub,simultaneous=True);rr=rr.subs(sub,simultaneous=True)
  res=s.diff(l,v)*rhs-s.diff(rr,u)
  ok=zero(res)
  outcomes.append({'value':a[':answer/value'],'is_solution':bool(ok),'stored_correct':a[':answer/id']==answer_id(f)})
 final=q[':question/worked-solution'].split('$$')[-2].strip()
 l,rr=relation(final);l=l.subs(sub,simultaneous=True);rr=rr.subs(sub,simultaneous=True)
 solution_ok=zero(s.diff(l,v)*rhs-s.diff(rr,u))
 return {'id':q[':question/id'],'choices':outcomes,'solution_final_valid':bool(solution_ok),'passed':all(z['is_solution']==z['stored_correct'] for z in outcomes) and bool(solution_ok)}
