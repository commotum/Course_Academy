"""Executable retained finding regressions; no services or runtime mutations.
Run: PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python repair_check.py
"""
import sys,json,re,importlib.util
from pathlib import Path
from functools import lru_cache
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W/'evidence/deps'))
import sympy as S
from sympy.parsing.latex import parse_latex
spec=importlib.util.spec_from_file_location('generator',W/'17592186147454.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=S.symbols('x y',positive=True);C,D=S.symbols('C D',real=True)
def save(name,obj):(W/'evidence'/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def field(r):return r['question'][':question/answer-fields'][0]
def key(r):return field(r)[':answer-field/correct'][1]
def keyvalue(r):return next(a[':answer/value'] for a in field(r)[':answer-field/choices'] if a[':answer/id']==key(r))
@lru_cache(None)
def parse(v):
 v=v.replace(r'\left','').replace(r'\right','').strip().rstrip('.,').replace(r'\pm','').replace('\u2061','').replace(r'\dfrac',r'\frac')
 v=re.sub(r'\\frac\{\\(?:text|mathrm)\{d\}y\}\{\\(?:text|mathrm)\{d\}x\}|\\frac\{dy\}\{dx\}', 'D',v)
 try:a=parse_latex(v,strict=True)
 except Exception as e:raise ValueError("Cannot parse: "+v) from e
 return a.xreplace({s:{'x':x,'y':y,'C':C,'D':D,'e':S.E}.get(str(s),s) for s in a.free_symbols})
@lru_cache(None)
def ode(prompt,h):
 equations=re.findall(r'\$\$([\s\S]*?)\$\$',prompt)
 assert equations
 l,r=equations[0].strip().rstrip('.').split('=')
 F=S.expand(parse(l)-parse(r));assert S.diff(F,D)!=0
 F=S.expand(S.simplify(-F.subs(D,0)/S.diff(F,D)).subs(x,x-h))
 terms=S.Add.make_args(F)
 powers={S.simplify(y*S.diff(t,y)/t) for t in terms}
 assert len(powers)==2 and 1 in powers,powers
 n=next(n for n in powers if n!=1)
 p=S.simplify(-sum(t/y for t in terms if S.simplify(y*S.diff(t,y)/t)==1))
 q=S.simplify(sum(t/y**n for t in terms if S.simplify(y*S.diff(t,y)/t)==n))
 return p,q,n
@lru_cache(None)
def residual(z,p,q,n):return S.simplify(S.expand(S.diff(z,x)+(1-n)*p*z-(1-n)*q))
@lru_cache(None)
def bank_check(prompt,values,h):
 p,q,n=ode(prompt,h);out=[]
 for v in values:
  Y=S.simplify(parse(v.split('=',1)[1]).subs(x,x-h))
  z=S.simplify(S.powdenest(Y**(1-n),force=True))
  if n in (S.Rational(1,2),S.Rational(3,4),S.Rational(-1,2)):z=z.replace(S.Abs,lambda v:v)
  res=residual(z,p,q,n)
  witness=None
  if res!=0:
   for xx,cc in [(1,2),(2,3),(3,1)]:
    vv=res.subs({x:xx,C:cc})
    if vv.is_finite and vv!=0:witness={'x':xx,'C':cc,'value':str(vv)};break
   assert witness is not None,('no wrong-answer witness',v,str(res))
  out.append({'value':v,'valid':res==0,'residual':str(res),'witness':witness})
 return {'p':str(p),'q':str(q),'n':str(n),'choices':out}
def verify(r,stages=True):
 q=r['question'];h=r['generation']['parameters']['shift'];f=field(r)
 result=bank_check(q[':question/problem'],tuple(a[':answer/value'] for a in f[':answer-field/choices']),h)
 assert [a['valid'] for a in result['choices']]==[a[':answer/id']==key(r) for a in f[':answer-field/choices']],(r['generation'],result)
 assert len(f[':answer-field/choices'])==5
 if stages:
  solution=q[':question/worked-solution'];p,qq,n=ode(q[':question/problem'],h)
  zz=re.findall(r'\$\$z=([\s\S]*?)\$\$',solution);assert len(zz)==1
  z=parse(zz[0]).subs(x,x-h);assert residual(z,p,qq,n)==0
  given=re.search(r'\$\$p\(x\)=([\s\S]*?),\\quad q\(x\)=([\s\S]*?),\\quad n=([\s\S]*?)\$\$',solution);assert given
  assert S.simplify(parse(given[1]).subs(x,x-h)-p)==0
  assert S.simplify(parse(given[2]).subs(x,x-h)-qq)==0
  assert S.simplify(parse(given[3])-n)==0
  final=re.findall(r'\$\$y=([\s\S]*?)\$\$',solution);assert len(final)==1
  assert final[0].rstrip('.')==keyvalue(r).split('=',1)[1]
 return {'question_id':q[':question/id'],'template':r['generation']['template'],**result}
def controlled():
 records=[]
 for t in g.FAMILIES:
  level=g.SOURCES[t][':question/difficulty'][':db/ident'].split('/')[-1]
  first=2 if t=='q-109172' else 1
  # Same bank contains positive/negative forcing and multiple IF exponents.
  bank=[[first,1],[first,2],[first,-1],[first+1,1],[first+2,-2]]
  rr=[g.generate(level,98301,t,{'shift':1,'bank':bank,'target':i}) for i in range(5)]
  assert len({tuple(sorted(a[':answer/value'] for a in field(r)[':answer-field/choices'])) for r in rr})==1
  assert len({keyvalue(r) for r in rr})==5
  assert len({r['question'][':question/problem'] for r in rr})==5
  assert len({r['question'][':question/worked-solution'] for r in rr})==5
  records+=rr
 return records
def main():
 # Retain the exact old minimal call and whole shift domain, not copied outcomes.
 focused=[g.generate('moderate',98301,'q-109154',{'shift':h}) for h in g.SHIFTS]
 def old_cue(r):
  candidates=[a for a in field(r)[':answer-field/choices'] if re.search(r'C\s*-\s*2',a[':answer/value']) and ('5/2' in a[':answer/value'] or r'\frac{5}{2}' in a[':answer/value'])]
  return len(candidates)==1 and candidates[0][':answer/id']==key(r)
 assert not all(map(old_cue,focused)), 'Retained C-2u^(5/2) shortcut persists'
 # Explicit q_scale counterfactual rejected by the old implementation.
 scaled=[g.generate('moderate',98301,'q-109154',{'shift':1,'q_scale':b}) for b in [1,2]]
 assert keyvalue(scaled[0])!=keyvalue(scaled[1])
 # Retain the exact autonomous failure and check ordinary seed selection.
 autonomous=g.generate('moderate',0,'q-109029',{'shift':1})
 ordinary=[g.generate('moderate',seed) for seed in range(24)]
 assert any(r['generation']['template']=='q-109029' for r in ordinary), 'Autonomous family unavailable in normal generation'
 records=controlled()
 math=[verify(r) for r in records+scaled+[focused[0],autonomous]]
 irrelevant=g.generate('moderate',73429,'q-109154',records[25]['generation']['parameters'])
 assert irrelevant['question']==records[25]['question'], 'Seed changes fully specified instance'
 save('controlled-records.json',records);save('focused-records.json',focused);save('ordinary-records.json',ordinary);save('coefficient-counterfactual.json',scaled)
 save('regression-math.json',math)
 summary={'finding_ids':['1388ffc008aaf44c1904','0d445813c431c607edbe'],'exact_old_cue':{'successes':sum(map(old_cue,focused)),'attempts':len(focused)},'controlled_templates':len(g.FAMILIES),'fixed_banks':10,'eligible_correct_formulas_per_fixed_bank':5,'independent_math_records':len(math),'ordinary_autonomous_count':sum(r['generation']['template']=='q-109029' for r in ordinary),'irrelevant_seed_preserves_question':True,'status':'passed'}
 save('regression-results.json',summary);print(json.dumps(summary))
if __name__=='__main__':main()
