"""Root actual IVP family/condition, full-bank and all-isolation-stage audit."""
import importlib.util,json,sys,hashlib
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186100951'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'initial-value-readback.py','p');g=load(D.with_suffix('.py'),'g')
n=dict(records=0,choices=0,whole_banks=0,printed_stages=0,source_prompts=0,source_values=0,source_solutions=0,source_designations=0,domain_guard_rejections=0)
def check(r):
 q=r['question'];m=r['generation'];assert m['eligible_for_learning']==(not m['evidence_only']);prob=p.read_problem(q[':question/problem']);ans=prob[-1];f=q[':question/answer-fields'][0];vs=[p.scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert all(not p.equal(a,b) for i,a in enumerate(vs) for b in vs[:i]);good=[i for i,v in enumerate(vs) if p.equal(v,ans)];assert len(good)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][good[0]][':answer/id']==f[':answer-field/correct'][1]
 if m['profile']=='authored':
  if not f[':answer-field/type'].endswith('/radio'):expected=[ans]
  else:
   _,u,b,family,_=prob;ratio=s.simplify(family/p.A)
   if family.has(s.log):name='log';expected=[s.exp(b)-u,s.exp(b)+u,b-u,s.exp(b-u),s.exp(-b)-u]
   elif not s.diff(1/family,p.x).has(p.x,p.A):
    c=s.diff(1/family,p.x)*u;name='recip';expected=[1/b-c,1/b+c,b-c,1/(b-c),-1/b-c]
   elif ratio.func==s.exp:
    F=ratio.subs(p.x,u);name='exp';expected=[b/F,b*F,b,F/b,1/(b*F)]
   elif ratio.func in (s.sin,s.cos):
    F=ratio.subs(p.x,u);G=(s.cos(ratio.args[0]) if ratio.func==s.sin else s.sin(ratio.args[0])).subs(p.x,u);name='sin' if ratio.func==s.sin else 'cos';expected=[b/F,b*F,b,b/G,F/b]
   else:
    exponent=ratio.as_powers_dict().get(p.x);assert exponent and exponent.is_Integer and s.simplify(ratio-p.x**exponent)==0
    degree=abs(exponent);name=('power' if exponent>0 else 'invpower')+('_unary' if degree==1 else '_nonunit')
    if exponent>0:expected=[b/u,b*u,b,u/b,1/(b*u)] if degree==1 else [b/u**degree,b*u**degree,b/u,b/(degree*u),b/(u+degree)]
    else:expected=[b*u,b/u,b,u/b,1/(b*u)] if degree==1 else [b*u**degree,b/u**degree,b*u,b*degree*u,b*(u+degree)]
   assert m['authored_bank']==name
  assert len(vs)==len(expected) and all(sum(p.equal(v,z) for v in vs)==1 for z in expected),'Full bank differs from actual supplied-family isolation operations'
 if ':question/worked-solution' in q:n['printed_stages']+=p.check_solution(q[':question/worked-solution'],prob)
 n['records']+=1;n['choices']+=len(vs);n['whole_banks']+=1
if __name__=='__main__':
 assert json.load(open(D/'source.json'))==json.load(open(R/'sources/17592186100951.json'))
 old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);o=old[c['source_id']];q=r['question']
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:
   a=next(a[':answer/value'] for a in of[':answer-field/choices'] if a[':answer/id']==of[':answer-field/correct'][':answer/id']);b=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert a==b;n['source_designations']+=1
  n['source_prompts']+=1;n['source_values']+=len(f[':answer-field/choices']);n['source_solutions']+=int(':question/worked-solution' in o)
 for template,entry in g.TEMPLATES.items():
  for seed in range(7):
   r=g.generate(entry['level'],template=template,seed=41000+seed);check(r);z=g.generate(entry['level'],template=template,seed=42000+seed,parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id'];check(g.generate(entry['level'],template=template,seed=41000+seed,parameters=r['generation']['parameters'],field_type=entry['kind']))
 for r in json.load(open(D/'review.json')):check(r.get('record',r))
 for template in ('q-141107','q-141108'):
  for profile in (None,'observed:'+template,'completed:'+template):
   try:g.generate('easy',template=template,profile=profile,parameters={'k':2 if template=='q-141107' else 1,'u':1,'b':'1/1000003'})
   except ValueError:n['domain_guard_rejections']+=1
   else:raise AssertionError('Huge-denominator workload bypass')
 for template,params in [('q-141108',{'k':1,'u':0,'b':2}),('q-141114',{'k':1,'u':1,'b':2}),('q-141112',{'k':1,'u':-1,'b':2}),('q-141111',{'k':2,'u':'pi/8','b':'sqrt(3)'}),('q-141116',{'k':1,'u':0,'b':'1/2'}),('q-141115',{'k':1,'u':0,'b':1})]:
  try:g.generate('easy',template=template,parameters=params)
  except ValueError:n['domain_guard_rejections']+=1
  else:raise AssertionError('Whole method-bank collision admitted')
 (R/'qa/17592186100951-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
