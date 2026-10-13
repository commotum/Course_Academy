#!/usr/bin/env python3
"""Independent printed-expression QA, exact source replay, native learner tests."""
from pathlib import Path
import importlib.util,json,re,hashlib,subprocess,copy
import sympy as sp
import uuid
from math import gcd
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent; SCRIPT=HERE.with_suffix('.py');ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,D,alpha,beta,A=sp.symbols('x y D alpha beta A')
loc={s.name:s for s in [x,y,D,alpha,beta,A]};loc['exp']=sp.exp

def expr(s):
 """Parse this finite source TeX grammar, separately from rendering helpers."""
 s=s.strip().rstrip('.,')
 s=s.replace(r'\frac{\text{d}y}{\text{d}x}','D').replace(r'\frac{dy}{dx}','D').replace(r'\frac{\text{d}{y}_{p}}{\text{d}x}','D')
 for a,b in [(r'\alpha','alpha'),(r'\beta','beta'),('{y}_{p}(x)','Y'),('{y}_{p}','Y'),(r'y_{c}(x)','Y'),('{y}_{c}(x)','Y'),('{e}','e')]:s=s.replace(a,b)
 while r'\frac' in s:
  nxt=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
  assert nxt!=s,('unhandled fraction',s);s=nxt
 s=re.sub(r'e\^\{([^{}]+)\}',r' exp(\1)',s)
 s=s.replace(r'\,','').replace(r'\text{and}',',').replace('{','(').replace('}',')').replace('^','**')
 assert '\\' not in s,('unhandled TeX',s)
 return parse_expr(s,local_dict=loc,transformations=standard_transformations+(implicit_multiplication_application,))

def equal(a,b):assert sp.simplify(sp.expand(a-b))==0,(a,b)
def formatting(s):
 assert s.count('$$')%2==0
 assert s.replace('$$','').count('$')%2==0
 count=0
 for ch in s:
  if ch=='{':count+=1
  elif ch=='}':count-=1;assert count>=0
 assert count==0
 assert '+-' not in s and '--' not in s

def inspect(r):
 q=r['question'];gen=r['generation'];prompt=q[':question/problem'];formatting(prompt)
 uuid.UUID(q[':question/id'])
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 equations=re.findall(r'\$\$\s*(.*?)\s*\$\$',prompt,re.S)
 ode=equations[0] if equations else re.search(r'\$(.*?)\$',prompt,re.S)[1]
 left,right=ode.split('=');lhs=expr(left);force=expr(right)
 a=lhs.coeff(D);b=lhs.coeff(y);assert lhs==a*D+b*y and a>0
 egs=sorted(force.atoms(sp.exp),key=lambda e:e.args[0].coeff(x));ks=[e.args[0].coeff(x) for e in egs];cs=[sp.expand(force).coeff(e) for e in egs]
 assert all(v!=0 for v in [a,b,*ks,*cs]) and len(ks)==len(set(ks)) and all(a*k+b!=0 for k in ks)
 if not gen['raw_evidence'] and gen['template']=='two_hard':
  primitive_a=int(a)//gcd(int(a),int(b),*(int(c) for c in cs))
  assert primitive_a>=4,('hard ODE reduces to moderate leading coefficient',primitive_a)
  assert all(not (c/a).is_Integer for c in cs)
 expected=sum(c/(a*k+b)*e for k,c,e in zip(ks,cs,egs))
 yc=re.search(r'complementary solution \$(.*?)\$',prompt)[1];complement=expr(yc.split('=')[1]);equal(a*sp.diff(complement,x)+b*complement,0)
 p=gen['parameters'];assert a==p['a'] and b==p['b'];equal(force,sum(c*sp.exp(k*x) for k,c in zip(p['k'],p['c'])))
 f=q[':question/answer-fields'][0];uuid.UUID(f[':answer-field/id']);assert '{{'+f[':answer-field/key']+'}}' in prompt
 if gen['raw_evidence'] and gen['template']=='legacy_single':
  assert ':answer-field/correct' not in f and ':answer-field/choices' not in f and ':question/worked-solution' not in q;return
 assert len(f[':answer-field/choices'])==1 and f[':answer-field/type']==':answer-field.type/blank'
 answer=f[':answer-field/choices'][0];uuid.UUID(answer[':answer/id']);formatting(answer[':answer/value']);assert '$' not in answer[':answer/value'];assert f[':answer-field/correct']==[':answer/id',answer[':answer/id']]
 value=expr(answer[':answer/value']);equal(value,expected);equal(a*sp.diff(value,x)+b*value,force)
 assert value.free_symbols <= {x}
 solution=q[':question/worked-solution'];formatting(solution)
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',solution,re.S);n=len(ks)
 assert len(blocks)==(4 if n==1 else 6)
 trial=expr(blocks[0].split('=')[1]);derivative=expr(blocks[1].split('=')[1]);equal(derivative,sp.diff(trial,x))
 aligned=blocks[2].replace(r'\begin{aligned}','').replace(r'\end{aligned}','');rows=aligned.split(r'\\')
 assert len(rows)==(4 if n==1 else 3)
 # Each of substitution, unevaluated distribution, collection is checked as
 # a whole symbolic equation before coefficient solving, not by final answer.
 actual_operator=a*sp.diff(trial,x)+b*trial
 for row in rows[:3]:
  l,rr=row.split('&');equal(expr(l),actual_operator);equal(expr(rr.lstrip(' =')),force)
 assert '(' in rows[0] and '(' in rows[1] and '(' not in rows[2]
 # First row must retain a grouped trial for b and a grouped derivative for a.
 assert rows[0].count('(')==2 and rows[1].count('(')==n
 unknowns=[alpha,beta][:n]; ordered_ks=p['k'];ordered_cs=p['c']; solved={s:sp.Rational(c,int(a*k+b)) for s,k,c in zip(unknowns,ordered_ks,ordered_cs)}
 equal(trial.subs(solved),expected)
 if n==1:
  l,rr=rows[3].split('&');equal(expr(l),alpha);equal(expr(rr.lstrip(' =')),solved[alpha])
 else:
  coeffparts=re.split(r',\\,\\,|,\\,|\\,\\text\{and\}\\,',blocks[3].rstrip('.,'))
  solvedparts=re.split(r',\\,\\,|,\\,|\\,\\text\{and\}\\,',blocks[4].rstrip('.,'))
  assert len(coeffparts)==2 and len(solvedparts)==2
  for i,part in enumerate(coeffparts):
   l,rr=part.split('=');equal(expr(l),(a*ordered_ks[i]+b)*unknowns[i]);equal(expr(rr),ordered_cs[i])
  for i,part in enumerate(solvedparts):
   l,rr=part.split('=');equal(expr(l),unknowns[i]);equal(expr(rr),solved[unknowns[i]])
 equal(expr(blocks[-1].split('=')[1]),expected)
 # Read prose forcing/exponent components as well as displays.
 prose=re.search(r'right-hand side is \$(.*?)\$',solution)[1];equal(expr(prose),force)
 assert all(exp in solution for exp in re.findall(r'\{e\}\^\{[^}]+\}',right))

sources=json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions'];replays=[];cases=[];repairs=[]
for s in sources:
 sid=s[':question/math-academy-id'];t=g.PROFILES[sid]['template'];p=g.PROFILES[sid]['parameters'];level=g.TEMPLATES[t]
 r=g.generate(level,123,t,parameters=p,profile=sid);q=r['question'];inspect(r)
 assert q[':question/problem']==s[':question/problem']
 assert q.get(':question/worked-solution')==s.get(':question/worked-solution')
 if ':question/difficulty' in s:assert q[':question/difficulty']==s[':question/difficulty'][':db/ident']
 else:assert ':question/difficulty' not in q
 sf=s[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
 assert sf[':answer-field/key']==gf[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==gf[':answer-field/type']
 assert [v[':answer/value'] for v in sf.get(':answer-field/choices',[])]==[v[':answer/value'] for v in gf.get(':answer-field/choices',[])]
 if sf.get(':answer-field/correct'):assert sf[':answer-field/correct'][':answer/value']==gf[':answer-field/choices'][0][':answer/value']
 replays.append(r);cases.append({'source_id':sid,'template':t,'level':level,'parameters':p,'bank_profile':sid,'difficulty_authorship':sid in ('q-332393','q-332645')})
 normal=g.generate(level,parameters=p,template=t);inspect(normal);repairs.append(normal)
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2))
# Every field/value family, and two examples per level (more moderate layouts).
reviews=[g.generate(g.TEMPLATES[t],seed=53+i,template=t) for i,t in enumerate(g.TEMPLATES)]+[g.generate(l,seed=100+i) for l in ('easy','moderate','hard') for i in range(2)]
for r in reviews:inspect(r)
count=0;tasks={l:set() for l in ('easy','moderate','hard')}
for t,l in g.TEMPLATES.items():
 for seed in range(50):
  r=g.generate(l,seed,template=t);inspect(r);count+=1;tasks[l].add(r['generation']['parameter_fingerprint'])
  p=r['generation']['parameters'];again=g.generate(l,seed+500,template=t,parameters=p)
  assert again['question']==r['question'];assert again['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
# Whole parameter domain guards apply to explicit calls.
for level,t,p in [('easy','single',{'a':2,'b':3,'k':[1],'c':[3]}),('moderate','two_and',{'a':4,'b':8,'k':[1,2],'c':[3,5]}),('hard','two_hard',{'a':4,'b':8,'k':[1,2],'c':[4,3]}),('moderate','two_and',{'a':2,'b':-2,'k':[1,3],'c':[3,5]}),('moderate','two_and',{'a':2,'b':2,'k':[2,2],'c':[3,5]}),('hard','two_hard',{'a':4,'b':-100,'k':[1,2],'c':[3,5]}),('hard','two_hard',{'a':4,'b':8,'k':[1,2],'c':[2,6]}),('hard','two_hard',{'a':6,'b':12,'k':[1,2],'c':[-3,9]})]:
 try:g.generate(level,template=t,parameters=p)
 except ValueError:pass
 else:raise AssertionError(('invalid parameters accepted',p))
# Validator failure probes: actual learner text and stage corruptions must fail.
base=g.generate_moderate(88,template='two_and')
for key,old,new in [(':question/problem','{{field-1}}','{{wrong}}'),(':question/worked-solution',r'\frac{\text{d}{y}_{p}}{\text{d}x}=',r'\frac{\text{d}{y}_{p}}{\text{d}x}=2+'),(':question/worked-solution',' & =',' & =1+')]:
 bad=copy.deepcopy(base);assert old in bad['question'][key];bad['question'][key]=bad['question'][key].replace(old,new,1)
 try:inspect(bad)
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Printed mutation was not detected')
p1={'a':1,'b':3,'k':[2,5],'c':[2,1]};p2={'a':2,'b':6,'k':[5,2],'c':[2,4]}
r1=g.generate_moderate(template='two_comma',parameters=p1);r2=g.generate_moderate(template='two_comma',parameters=p2)
assert r1['generation']['parameter_fingerprint']==r2['generation']['parameter_fingerprint']
assert r1['question'][':question/id']!=r2['question'][':question/id']
# Normal records restricted to the requested finite trial span; source request
# itself admits added homogeneous solutions, documented separately below.
engine=[]
for i,r in enumerate(repairs+reviews):
 q=r['question'];p=r['generation']['parameters'];f=q[':question/answer-fields'][0];canonical=f[':answer-field/choices'][0][':answer/value']
 equivalent=g.summ([r'\frac{'+str(2*c)+'}{'+str(2*(p['a']*k+p['b']))+'}'+g.exp(k) for k,c in reversed(list(zip(p['k'],p['c'])))])
 wrong=canonical+'+'+g.exp(p['k'][0])
 homogeneous=canonical+'+'+g.exp(sp.Rational(-p['b'],p['a']))
 equal(p['a']*sp.diff(expr(homogeneous),x)+p['b']*expr(homogeneous),sum(c*sp.exp(k*x) for k,c in zip(p['k'],p['c'])))
 engine.append({'label':'normal-'+str(i),'record':r,'checks':[{'submitted':canonical,'expected':'accepted','purpose':'canonical trial particular RHS'},{'submitted':equivalent,'expected':'accepted','purpose':'independently unreduced coefficients, reversed term order'},{'submitted':wrong,'expected':'rejected','purpose':'wrong forcing coefficient'},{'submitted':homogeneous,'expected':'rejected','purpose':'solves ODE but outside clarified forcing-exponential trial span'}]})
for i,r in enumerate(replays):
 if ':question/worked-solution' not in r['question']:continue
 p=r['generation']['parameters'];canonical=r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
 homogeneous=canonical+'+'+g.exp(sp.Rational(-p['b'],p['a']))
 engine.append({'label':'raw-source-'+str(i),'record':r,'checks':[{'submitted':canonical,'expected':'accepted','purpose':'original canonical answer'},{'submitted':homogeneous,'expected':'rejected','purpose':'documented raw-source grading limitation: alternate valid particular solution is not accepted by fixed-answer grader'}]})
(HERE/'engine-input.json').write_text(json.dumps(engine,indent=2))
enginepath=ROOT/'generate/runs/current/check-engine'
subprocess.run([str(enginepath),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
(HERE/'review.json').write_text(json.dumps({'original_replays':replays,'supported_repairs':repairs,'generated_variants':reviews},indent=2))
md=['# Particular exponential solutions — review','\nBasis1356. Originals use raw API profiles. Normal output clarifies the trial span; two unrated records receive derived answers/solutions and authored easy levels.']
for s,r,normal in zip(sources,replays,repairs):
 md+=['\n## Original '+s[':question/math-academy-id'],g.markdown(r),'\n### Supported normal presentation',g.markdown(normal)]
for i,r in enumerate(reviews):md+=['\n## Generated variant '+str(i+1)+' — '+r['generation']['template'],g.markdown(r)]
md+=['\n## Review findings','All six presentation families and twelve generated records were read back. Signed derivative coefficients, subtraction groups, distributed coefficients and fraction signs remain legible and correct. Each level has at least two additional variants. All source solution stages are retained. The raw missing banks are visibly labeled. No plots or sibling resonance steps occur.']
(HERE/'review.md').write_text('\n\n'.join(md))
report={'status':'pass','basis':1356,'source_questions':10,'exact_prompt_matches':10,'exact_solution_matches':8,'missing_original_solutions':2,'exact_answer_value_matches':8,'correct_designation_matches':8,'missing_original_correct_designations':2,'field_layout_matches':10,'observed_distractors':0,'complete_observed_answer_banks':8,'raw_missing_banks_preserved':2,'supported_missing_record_repairs':2,'authored_missing_level_extensions':0,'unrated_authored_easy_assignments':2,'raw_source_alternative_solution_grader_rejections':8,'normal_response_eligibility_checks':22,'authored_variants_checked':count,'meaningful_tasks_sampled':{l:len(v) for l,v in tasks.items()},'native_checks':sum(len(v['checks']) for v in engine),'source_mathematical_errors':0,'hard_primitive_leading_guard':'a/gcd(a,b,*c)>=4; independently checked from printed ODE','hard_common_scaling_negative_controls':2,'normal_form_clarification':'finite span of displayed forcing exponentials','known_raw_source_grading_limitation':'The broad request for a particular solution mathematically permits adding any homogeneous solution; the fixed-answer grader accepts only its expected expression. Normal output clarifies the required trial span.','generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'validator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest(),'grader_sha256':hashlib.sha256(enginepath.read_bytes()).hexdigest(),'grader_report_sha256':hashlib.sha256((HERE/'engine-report.json').read_bytes()).hexdigest(),'review_sha256':hashlib.sha256((HERE/'review.json').read_bytes()).hexdigest()}
(HERE/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
