import json, re, sys, pathlib, importlib.util, collections, hashlib, shutil, subprocess
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
BASE=pathlib.Path(__file__).resolve().parent
ROOT=BASE/'verified'
ROOT.mkdir(exist_ok=True)
JOB=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186068844')
REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
PY=REPO/'.venv/bin/python'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('reviewed_generator',JOB/'workspace/17592186068844.py')
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
def main():
 source=json.load(open(JOB/'source/source.json'))['material']['kp'];batch=json.load(open(JOB/'samples.json'));dump('batch-records.json',batch)
 records=[];replay=[];boundaries=[]
 for i,(t,(level,sid)) in enumerate(g.TEMPLATES.items()):
  if level!='easy':continue
  original=next(q for q in source[':knowledge-point/questions'] if q[':question/math-academy-id']==sid)
  r=g.generate_easy(seed=90031+i,template=t,parameters={'h':0,'k':0},profile='observed');records.append(r)
  f=field(r);sf=original[':question/answer-fields'][0]
  replay.append({'source_id':original[':question/id'],'template':t,'prompt_equal':r['question'][':question/problem']==original[':question/problem'],'solution_equal':r['question'][':question/worked-solution']==original[':question/worked-solution'],'bank_equal':sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']),'correct_equal':next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==answer_id(f))==sf[':answer-field/correct'][':answer/value']})
  for j,p in enumerate([{'h':0,'k':0},{'h':0 if 'autonomous' in t else -6,'k':-6},{'h':0 if 'autonomous' in t else 6,'k':6}]):
   rr=g.generate_easy(seed=91007+i*10+j,template=t,parameters=p);records.append(rr)
   boundaries.append({'template':t,'parameters':p,'deterministic':rr==g.generate_easy(seed=91007+i*10+j,template=t,parameters=p)})
 for seed in range(720181,720214):records.append(g.generate_easy(seed=seed))
 dump('independent-records.json',records);dump('source-replay.json',replay)
 math=[inspect_record(r) for r in records+batch];dump('math-results.json',math)
 probes=[]
 for group,rs in [('independent',records),('batch',batch)]:
  for t in sorted(set(r['generation']['template'] for r in rs)):
   sub=[r for r in rs if r['generation']['template']==t and r['generation']['bank_profile']=='standard']
   if not sub:continue
   hits=[]
   for r in sub:
    picks=shortcut(r);hits.append({'id':r['question'][':question/id'],'selected':picks,'correct':len(picks)==1 and picks[0]==answer_id(field(r))})
   probes.append({'group':group,'template':t,'total':len(sub),'correct':sum(z['correct'] for z in hits),'baseline':.2,'trials':hits})
 dump('shortcut-results.json',probes)
 invalid=[]
 for kwargs in [dict(parameters={'h':7,'k':0}),dict(parameters={'h':0,'k':True}),dict(template='arcsin_autonomous',parameters={'h':1,'k':0}),dict(profile='invalid'),dict(field_type='free'),dict(template='two_x_terms')]:
  try:g.generate_easy(**kwargs);out='unexpected acceptance'
  except (ValueError,TypeError) as e:out=type(e).__name__+': '+str(e)
  invalid.append({'arguments':kwargs,'outcome':out})
 dump('boundary-results.json',{'determinism':boundaries,'rejections':invalid})
 # Controlled relevant shift and irrelevant seed/option-order pairs.
 before=g.generate_easy(seed=101,template='exp_linear',parameters={'h':0,'k':0})
 relevant=g.generate_easy(seed=101,template='exp_linear',parameters={'h':1,'k':0})
 irrelevant=g.generate_easy(seed=102,template='exp_linear',parameters={'h':0,'k':0})
 dump('counterfactual-records.json',[before,relevant,irrelevant]);
 # Grader sees all options, all pairs and the runner batch in one invocation.
 cases=[]
 for i,r in enumerate(records+batch+[before,relevant,irrelevant]):
  f=field(r);checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==answer_id(f) else 'rejected','purpose':'independently differentiated complete equation'} for a in f[':answer-field/choices']]
  cases.append({'label':str(i)+' '+r['generation']['template'],'record':r,'checks':checks})
 # Radio submissions must be owned choices. The old equation is absent from the
 # changed bank, so assess both complete new banks rather than submit foreign IDs.
 cases.append({'label':'irrelevant option shuffle identity','record':irrelevant,'checks':[{'submitted_answer_id':answer_id(field(before)),'expected':'accepted','purpose':'same relation survives option order change'}]})
 dump('grader-input.json',cases)
 summary={'replay_total':len(replay),'replay_failures':[r for r in replay if not all(r[k] for k in ('prompt_equal','solution_equal','bank_equal','correct_equal'))],'math_total':len(math),'math_failures':[r for r in math if not r['passed']],'shortcut':[{k:v for k,v in p.items() if k!='trials'} for p in probes]}
 dump('audit-summary.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
