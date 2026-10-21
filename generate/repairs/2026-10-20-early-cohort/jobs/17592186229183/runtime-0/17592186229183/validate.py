#!/usr/bin/env python3
"""Private independent source, displayed-math, scope and native grading QA."""
import importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
D=Path(__file__).parent
spec=importlib.util.spec_from_file_location('overflow',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
raw=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
cases=json.loads((D/'source-cases.json').read_text());T=s.Symbol('t',nonnegative=True)

def frac_to_expr(text):
 # Recursive parser for the actual finite LaTeX components in these masks.
 def group(z,i):
  assert z[i]=='{';depth=1;j=i+1
  while depth:
   depth+=(z[j]=='{')-(z[j]=='}');j+=1
  return z[i+1:j-1],j
 def expand(z):
  out='';i=0
  while i<len(z):
   if z.startswith(r'\frac',i):
    a,j=group(z,i+5);b,k=group(z,j);out+='(('+expand(a)+')/('+expand(b)+'))';i=k
   else:out+=z[i];i+=1
  return out
 text=text.split(r'\end{aligned}')[0].strip().rstrip('.')
 z=expand(text).replace(r'\cdot','*').replace('^{','**{').replace('^','**').replace('{','(').replace('}',')')
 z=z.replace(r'\,','').replace('⁡','')
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
 return parse_expr(z,local_dict={'t':T,'C':s.Symbol('C'),'Q':s.Symbol('Q'),'DQ':s.Symbol('DQ')},transformations=standard_transformations+(implicit_multiplication_application,rationalize))

def physical_from_prompt(prompt):
 unit=r'(?:\\,)?(?:\\text\{)?'
 # Read each complete quantity before its stated unit, including fractional c.
 number=r'(\\frac\{\d+\}\{\d+\}|\d+(?:\.\d+)?|\d+/\d+)'
 vals=re.findall(r'\$'+number+r'(?:\\,)?(?:\\text\{|\\textrm\{)?(?:gal|lb)',prompt)
 assert len(vals)==6,(vals,prompt)
 def rational(z):
  m=re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}',z)
  return s.Rational(m[1],m[2]) if m else s.Rational(z)
 return dict(zip(['H','v','q','c','rin','rout'],map(rational,vals)))

def independent(r):
 q=r['question'];p=physical_from_prompt(q[':question/problem']);H,v,q0,c,ri,ro=(p[k] for k in ('H','v','q','c','rin','rout'))
 d=ri-ro;n=ro/d;a=v/d;to=(H-v)/d
 V=v+d*T;Q=c*V+(q0-c*v)*(v/V)**n
 assert d>0 and to>0 and s.simplify(V.subs(T,to)-H)==0
 assert s.simplify(s.diff(Q,T)-(c*ri-ro*Q/V))==0
 assert s.simplify(Q.subs(T,0)-q0)==0
 sol=q.get(':question/worked-solution')
 if sol is not None:
  blocks=sol.split('$$');assert len(blocks)==31
  # Read actual volume, factor, solved Q and endpoint substitution strings.
  volume=blocks[7].split('=')[-1].split(r'\,')[0]
  assert s.simplify(frac_to_expr(volume)-V)==0
  final_if=blocks[17].split('& =')[-1].strip().rstrip('.')
  assert s.simplify(frac_to_expr(final_if)-(a+T)**n)==0
  assert s.simplify(s.diff(frac_to_expr(final_if),T)/frac_to_expr(final_if)-ro/V)==0
  lastQ=blocks[25].split('& =')[-1].strip().rstrip('.')
  assert s.simplify(frac_to_expr(lastQ)-Q)==0,(lastQ,Q)
  last=blocks[29]
  initial_rhs=last.split('& =')[1].split(r'\\')[0].strip()
  assert s.simplify(frac_to_expr(initial_rhs)-Q.subs(T,to))==0
  rhs_eval=last.split('& =')[2].split(r'\\')[0].strip()
  assert s.simplify(frac_to_expr(rhs_eval)-Q.subs(T,to))==0
  end_num=re.search(r'[≈=]([\d.]+)\\,',last)[1]
  assert end_num==g.rounded(Q.subs(T,to)),(end_num,Q.subs(T,to))
  assert '**Step 1**' in sol and '**Step 2**' in sol and '**Step 3**' in sol and '**Step 4**' in sol
  # Read distributed/primitive/initial-condition stages from displayed blocks.
  actual_in=blocks[5].split('& =')[-1].split(r'\,')[0]
  assert frac_to_expr(actual_in)==c*ri
  actual_out=blocks[11].split('& =')[-1].split(r'\,')[0]
  assert s.simplify(frac_to_expr(actual_out)-ro*s.Symbol('Q')/V)==0
  distributed=blocks[19].split(r'\\')[1]
  lhs,rhs=distributed.split('& =')
  lhs=lhs.replace(r'\frac{dQ}{dt}','DQ')
  assert s.simplify(frac_to_expr(lhs).subs(s.Symbol('DQ'),c*ri-n*s.Symbol('Q')/(a+T))-frac_to_expr(rhs))==0
  actual_ode=blocks[15].strip().rstrip('.')
  assert actual_ode.endswith('='+g.fmt(c*ri))
  actual_coefficient=actual_ode.split('+',1)[1].split(r'\,Q')[0]
  assert s.simplify(frac_to_expr(actual_coefficient)-ro/V)==0
  primitive=blocks[21].split('& =')[2].split(r'\\')[0].strip()
  actual_primitive=frac_to_expr(primitive)-s.Symbol('C')
  assert s.simplify(s.diff(actual_primitive,T)-c*ri*(a+T)**n)==0
  general=blocks[21].split('& =')[-1].strip()
  Cexpected=(q0-c*v)*a**n
  assert s.simplify(frac_to_expr(general).subs(s.Symbol('C'),Cexpected)-Q)==0
  actual_C=blocks[23].split('C & =')[-1].strip()
  assert s.simplify(frac_to_expr(actual_C)-Cexpected)==0
  displayed_to=blocks[27].split('& =')[-1].split(r'\,')[0].strip()
  assert frac_to_expr(displayed_to)==to
  assert re.search(r'Q\((.*?)\)',blocks[29])[1]==g.fmt(to)
  # Independent primitive and solved integration constant checks.
  C=(q0-c*v)*a**n;k=c*d;A=c*ri
  assert s.simplify(s.diff(A/(n+1)*(a+T)**(n+1),T)-A*(a+T)**n)==0
  assert s.simplify((k*(a+T)+C/(a+T)**n)-Q)==0
 if r['generation']['eligible_for_learning']:
  f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
  assert value==g.rounded(Q.subs(T,to))+r'\,\text{lb}'
  values=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(set(values))==len(values)==5
 for text in [q[':question/problem']]+([sol] if sol else []):
  assert text.count('$')%2==0 and text.count('{')==text.count('}')
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 json.dumps(r)

reports=[];bank_count=choice_count=correct_count=0;engine=[];reviews=[];md=['# Overflow onset generator review\n\nSource replay retains observed difficulty/omissions. Generated records use explicitly authored workload policies. Raw/opaque records are evidence-only.']
for c,q in zip(cases,raw):
 r=g.generate(c['level'],0,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);rq=r['question']
 for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
  assert (key in rq)==(key in q),(c['source_id'],key)
 assert rq[':question/problem']==q[':question/problem']
 if ':question/worked-solution'in q:assert rq[':question/worked-solution']==q[':question/worked-solution']
 for sf,rf in zip(q[':question/answer-fields'],rq[':question/answer-fields']):
  assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in rf[':answer-field/choices'])
  assert (':answer-field/correct'in sf)==(':answer-field/correct'in rf)
  if ':answer-field/correct'in sf:
   val=next(a[':answer/value'] for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert val==sf[':answer-field/correct'][':answer/value'];correct_count+=1
  bank_count+=1;choice_count+=len(sf[':answer-field/choices'])
 independent(r);md.append(g.markdown(r));reviews.append(r)
 supplied=[f for f in rq[':question/answer-fields'] if ':answer-field/correct' in f]
 if supplied:
  fixture=json.loads(json.dumps(r));fixture['question'][':question/answer-fields']=supplied
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'original supplied radio field; malformed legacy field excluded only from grader fixture'} for f in supplied for a in f[':answer-field/choices']]
  engine.append({'label':'raw supplied '+c['source_id'],'record':fixture,'checks':checks})
 # Native grading tests use complete repaired supported layout; raw missing refs
 # remain public evidence and do not pretend to be gradeable observations.
 repaired=g.generate('easy',profile='repaired:'+c['source_id'],parameters=c['parameters']);independent(repaired)
 f=repaired['question'][':question/answer-fields'][0]
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'repaired evidence radio ID designation'} for a in f[':answer-field/choices']]
 engine.append({'label':'repaired '+c['source_id'],'record':repaired,'checks':checks})
 # Every observed mask/profile represented by a changed-parameter variant.
 changed=g.generate('easy',seed=71,template=c['template']);independent(changed);reviews.append(changed);md.append(g.markdown(changed))
 changed_raw=g.generate('easy',seed=72,template=c['template'],parameters=changed['generation']['parameters'],profile=c['bank_profile']);independent(changed_raw);reviews.append(changed_raw);md.append(g.markdown(changed_raw))
 reports.append({'source_id':c['source_id'],'exact_prompt':True,'solution_exact_or_absent':True,'key_presence_parity':True,'bank_values_exact':True,'raw_eligible':False})
positions=set();fingerprints={};coverage={}
for level in g.LEVELS:
 seen=set();templates=set()
 for seed in range(100):
  r=g.generate(level,seed);independent(r);seen.add(r['generation']['mathematical_fingerprint']);templates.add(r['generation']['template'])
  f=r['question'][':question/answer-fields'][0];position=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]);positions.add(position)
  if seed<2:
   reviews.append(r);md.append(g.markdown(r));engine.append({'label':level+str(seed),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'authored normal radio ID grading'} for a in f[':answer-field/choices']]})
  other=g.generate(level,999,template=r['generation']['template'],parameters=r['generation']['parameters']);assert other['question'][':question/id']==r['question'][':question/id']
 fingerprints[level]=len(seen);coverage[level]=sorted(templates);assert len(seen)>90 and len(templates)==7
assert positions==set(range(5))
# Public explicit bounds must reject cross-level and invalid physical instances.
for level in g.LEVELS:
 p=g.generate(level,seed=4)['generation']['parameters']
 for wrong in [l for l in g.LEVELS if l!=level]:
  try:g.generate(wrong,parameters=p)
  except ValueError:pass
  else:raise AssertionError('difficulty guard bypass')
(D/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
(D/'review.json').write_text(json.dumps(reviews,indent=2)+'\n');(D/'review.md').write_text('\n\n'.join(md)+'\n')
result={'status':'pass','stage':'7 frozen draft for root QA','source_questions':7,'source_banks':{'matched':bank_count,'total':8},'source_choices':{'matched':choice_count,'total':40},'supplied_correct_designations':{'matched':correct_count,'total':6},'missing_correct_designations':2,'exact_solutions':{'matched':6,'total':6},'missing_solution':1,'source_reports':reports,'source_repair_findings':['q-336451 duplicate legacy field removed in completed evidence; minerals/kg corrected to salt/lb in normal output','q-336499 unrated and missing worked solution/correct ref; raw omissions preserved; independently inferred rounded key 95.2 lb only in completed evidence','decoded source choices have no adjacent backslash pairs; empty decoded-byte-evidence.json records that no escape repair is needed'],'native':json.loads((D/'engine-report.json').read_text()),'sampled_math_checks':300,'sampled_unique_tasks':fingerprints,'default_mask_coverage':coverage,'answer_positions':sorted(positions),'plots':'none','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__}}
(D/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k in ('status','source_questions','source_banks','source_choices','sampled_unique_tasks')},indent=2))
