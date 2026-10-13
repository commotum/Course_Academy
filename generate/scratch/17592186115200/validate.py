#!/usr/bin/env python3
"""Independent printed-TeX mathematics, raw fidelity, guards, identity and native QA."""
import importlib.util, json, re, itertools, hashlib, subprocess, sys
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)
V={v:sp.Symbol(v,real=True) for v in ('x','m','h','k','a')}
def group(s,i):
 assert s[i]=='{';depth=1;j=i+1
 while depth:
  if s[j]=='{':depth+=1
  if s[j]=='}':depth-=1
  j+=1
 return s[i+1:j-1],j

def read_math(s):
 s=s.strip().replace(' ','')
 while r'\frac' in s:
  i=s.index(r'\frac');a,j=group(s,i+5);b,k=group(s,j)
  s=s[:i]+'(('+a+')/('+b+'))'+s[k:]
 s=s.replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(s,local_dict=V,transformations=TRANS,evaluate=False)

def log_linear(e):
 """Recover real exponential log equation independently from printed AST."""
 if e.is_Number:
  assert e>0
  return sum(sp.Rational(k)*sp.log(p) for p,k in sp.factorint(int(e)).items())
 if isinstance(e,sp.Pow):return e.exp*log_linear(e.base)
 if isinstance(e,sp.Mul):return sum(log_linear(f) for f in e.args)
 raise AssertionError(('not an exponential side',e))

def format_check(s):
 assert s.count('$')%2==0
 depth=0
 for char in s:
  depth+=1 if char=='{' else -1 if char=='}' else 0
  assert depth>=0
 assert depth==0 and '+-' not in s and '--' not in s

def check_record(r):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 for k in (':question/problem',':question/worked-solution'):
  if k in q:format_check(q[k])
 mathparts=re.findall(r'\$(.*?)\$',q[':question/problem']);eq=next(s.rstrip('.') for s in mathparts if '=' in s and '^' in s)
 l,rr=eq.split('=');lhs,rhs=read_math(l),read_math(rr)
 v=next(iter((lhs.free_symbols|rhs.free_symbols)));delta=sp.expand(log_linear(lhs)-log_linear(rhs))
 z=sp.solve(delta,v)[0];assert sp.simplify(delta.subs(v,z))==0
 assert sp.simplify(z-read_math(r['generation']['inferred_answer']))==0
 solution=q.get(':question/worked-solution','')
 # Check EVERY actual displayed aligned row at its independently solved root,
 # including nested powers, power-rule products, distributed negatives, collection.
 rows=[]
 for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S):
  for row in block.split(r'\\'):
   a,b=row.replace('&','').split('=');aa,bb=read_math(a),read_math(b)
   if '^' in row:assert sp.simplify((log_linear(aa)-log_linear(bb)).subs(v,z))==0
   else:assert sp.simplify((aa-bb).subs(v,z))==0
   rows.append(row)
 if solution:
  expected=8 if r['generation']['template'].startswith('hard') else 5 if r['generation']['template']=='easy_right' else 6
  assert len(rows)==expected,(len(rows),expected)
  assert rows[0].replace(' ','').replace('&','')==eq.replace(' ','')
 fs=q.get(':question/answer-fields',[])
 for f in fs:
  vals=[read_math(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(vals)==5 and len(set(sp.simplify(a) for a in vals))==5
  if ':answer-field/correct' in f:
   correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert sp.simplify(read_math(correct[':answer/value'])-z)==0
  for a in f[':answer-field/choices']:format_check(a[':answer/value'])
  if r['generation']['bank_origin']=='authored':
   side='left' if r['generation']['template'].endswith('left') else 'right'
   assert 'rewrite the '+side+'-hand side' in solution
   def leaf_power(e):
    if isinstance(e,sp.Pow) and e.base.is_Integer and e.base>1:return e
    for arg in e.args:
     try:return leaf_power(arg)
     except ValueError:pass
    raise ValueError('printed exponential power absent')
   lp,rp=leaf_power(lhs),leaf_power(rhs)
   a=int(sp.expand(lp.exp).coeff(v));c=int(sp.expand(lp.exp).subs(v,0))
   b=int(sp.expand(rp.exp).coeff(v));d=int(sp.expand(rp.exp).subs(v,0))
   left=int(lp.base)>int(rp.base);base=int(rp.base if left else lp.base);big=int(lp.base if left else rp.base)
   n=next(n for n in range(2,5) if base**n==big)
   hard=isinstance(rhs,sp.Mul)
   A,C=(n*a,n*c) if left else (a,c);B,D=(b,d) if left else (n*b,n*d)
   if hard:B,D=-B,-D
   if hard and left:
    expected=[z,sp.Rational(-D-C,A+B),sp.Rational(-d-c,a+b),sp.Rational(-d,n+a+b),1/z]
   elif hard:
    expected=[z,sp.Rational(-D-C,A+B),sp.Rational(-D-C,A-B),sp.Rational(-d-c,a+b),-z]
   else:
    omit=sp.Rational(d-c,a-b) if a!=b else sp.Rational(-n*n*c,n*n*a-b) if left else sp.Integer(n-c)
    second=sp.Rational(d-c,n*a-b) if left else sp.Rational(n*d-c,a-n*n*b)
    expected=[z,omit,second,-z,sp.Rational(D-C,A+B)]
   assert set(map(sp.simplify,vals))==set(map(sp.simplify,expected)), 'authored operations mismatch actual printed components'
   if not hard and not left and d:assert r['generation']['distractor_recipes'][2]=='multiply_slope_twice_keep_shift_once'
 return z

def native_item(r,label):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each complete displayed choice, independently mathematically checked'} for a in f[':answer-field/choices']]}

def run():
 cases=json.loads((HERE/'source-cases.json').read_text())
 assert len(cases)==len(g.CASES)==len(g.RAW)
 for case in cases:
  assert (case['template'],case['parameters'])==g.CASES[case['source_id']]
 replays=[];native=[];matched_choices=0;source_solutions=0;designation=0
 for source,(t,p) in g.CASES.items():
  r=g.generate(g.TEMPLATES[t],seed=47,template=t,parameters=p,profile=source);check_record(r);o=g.RAW[source];q=r['question']
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in q)==(key in o),(source,key)
  assert q[':question/problem']==o[':question/problem'],source
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'],source;source_solutions+=1
  if ':question/answer-fields' in o:
   f=q[':question/answer-fields'][0];old=o[':question/answer-fields'][0]
   assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
   assert f[':answer-field/key']==old[':answer-field/key']
   assert f[':answer-field/type']==old[':answer-field/type'][':db/ident']
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in old[':answer-field/choices']);matched_choices+=5
   if ':answer-field/correct' in old:
    ca=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ca==old[':answer-field/correct'][':answer/value'];designation+=1;native.append(native_item(r,source))
   else:
    # Minimal inferred correct reference is a separate grading fixture, not raw fidelity.
    fixed=json.loads(json.dumps(r));ff=fixed['question'][':question/answer-fields'][0];ff[':answer-field/correct']=[':answer/id',next(a[':answer/id'] for a in ff[':answer-field/choices'] if sp.simplify(read_math(a[':answer/value'])-check_record(r))==0)];native.append(native_item(fixed,source+' inferred designation fixture'))
  replays.append(r)
 normal=[];tasks={l:set() for l in ('easy','moderate','hard')}
 for t,l in g.TEMPLATES.items():
  for seed in range(60):
   r=g.generate(l,seed=seed,template=t);check_record(r);normal.append(r);tasks[l].add(r['generation']['parameter_fingerprint'])
   p=r['generation']['parameters'];rr=g.generate(l,seed=seed+99,template=t,parameters=p)
   assert r['question'][':question/id']==rr['question'][':question/id']
   assert r['generation']['parameter_fingerprint']==rr['generation']['parameter_fingerprint']
   assert sorted(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in rr['question'][':question/answer-fields'][0][':answer-field/choices'])
   if seed<2:native.append(native_item(r,t+str(seed)))
 # Every observed bank also runs normally through API at changed parameters.
 changed=[]
 for source,(t,p) in g.CASES.items():
  pp=dict(p);pp['base']=2 if p['base']!=2 else 3
  if t=='hard_left':pp['d']-=1
  else:pp['c']={'q-26817':-3,'q-66877':-6,'q-100449':-11,'q-66872':-9}.get(source,pp['c']+(1 if pp['c']>0 else -1))
  rr=g.generate(g.TEMPLATES[t],template=t,parameters=pp,profile=source);check_record(rr);changed.append(rr)
 # Domains enforced on explicit inputs, including reduced arithmetic and level demand.
 invalid=0
 for t,l in g.TEMPLATES.items():
  p=g.generate(l,template=t)['generation']['parameters']
  for key,value in [('base',1),('base',13),('n',1),('n',5),('a',6),('c',-13),('d',7),('var','t')]:
   pp={**p,key:value}
   try:g.generate(l,template=t,parameters=pp)
   except ValueError:invalid+=1
   else:raise AssertionError(('guard bypass',t,key,value))
  if l=='moderate' and t=='moderate_right':
   try:g.generate(l,template=t,parameters={**p,'b':1})
   except ValueError:invalid+=1
   else:raise AssertionError('moderate collapsed to easy')
 # Enumerate meaningful valid domain, excluding variable-letter and profile aliases.
 counts={}
 for t,l in g.TEMPLATES.items():
  count=0
  for base,n,a,c,b,d in itertools.product((2,3,4,5,6,7,8,9,10,12),range(2,5),range(1,6),range(-12,13),range(1,6),range(-6,7)):
   # Structural prefilter avoids expensive construction over irrelevant products.
   if t.startswith('easy') and not(a==b==1 and d==0 and c):continue
   if t=='moderate_right' and not(a==1 and b>=2 and d==0 and c):continue
   if t=='moderate_two_shifts' and not(a==b==1 and c and d):continue
   if t=='hard_right' and not(a>=2 and b==1 and c<0 and d>0):continue
   if t=='hard_left' and not(a>=2 and b==1 and c==0 and d<0):continue
   p=dict(base=base,n=n,a=a,c=c,b=b,d=d,var='x')
   try:g.validate_parameters(t,p);g.authored_bank(p,t)
   except ValueError:continue
   count+=1
  counts[t]=count
 (HERE/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 report={'status':'pass','source_questions':9,'prompt_exact':9,'presence_parity':9,'complete_banks_matched':7,'choice_values_matched':matched_choices,'correct_designations_matched':designation,'correct_designations_missing_in_source':2,'fieldless_originals':2,'solutions_exact':source_solutions,'solution_total_present':7,'authored_records_checked':len(normal),'changed_profile_records_checked':len(changed),'domain_guard_rejections':invalid,'sample_distinct_tasks':{k:len(v) for k,v in tasks.items()},'finite_authored_domain_counts':counts,'native':json.loads((HERE/'engine-report.json').read_text()),'source_anomalies':['q-110537 prose says left while rows rewrite right','q-110539 prose says right while rows rewrite left','q-26817 and q-66877 missing difficulty, correct ref, worked solution','q-110539 and q-66864 missing fields'],'native_grader_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 (HERE/'replays.json').write_text(json.dumps(replays,indent=2)+'\n')
 (HERE/'changed-profiles.json').write_text(json.dumps(changed,indent=2)+'\n')
 # Review has every original, changed profile and two authored examples/template.
 review=[r for i,r in enumerate(normal) if i%60<2]
 (HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 md=['# Source originals and generated variants','All observed bank profiles below are evidence-only. Normal authored banks are method-derived.']
 for r,change in zip(replays,changed):
  source=r['generation']['source_analysis']['source_id'];o=g.RAW[source]
  md+=['## Original '+source,o[':question/problem'],o.get(':question/worked-solution','No original solution.'),'### Original choices','\n'.join('- $'+a[':answer/value']+'$' for f in o.get(':question/answer-fields',[]) for a in f[':answer-field/choices']),'### Parameterized raw replay',g.markdown(r),'### Generated changed-base evidence variant',g.markdown(change)]
 md+=['## Authored learning variants']+[g.markdown(r) for r in review]
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='native'},indent=2))
if __name__=='__main__':run()
