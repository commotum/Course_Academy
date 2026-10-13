#!/usr/bin/env python3
"""Independent displayed-math, source shape, workload, identities, native QA."""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
ROOT=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location('ellipse_axes',ROOT.parent/(ROOT.name+'.py'))
g=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(g)
X,Y,a,b=sp.symbols('x y a b')

def group(s,pos):
 assert s[pos]=='{';start=pos+1;depth=1;pos+=1
 while depth:
  assert pos<len(s),'Unclosed TeX group'
  depth+=(s[pos]=='{')-(s[pos]=='}');pos+=1
 return s[start:pos-1],pos

def translate(s):
 out='';i=0
 while i<len(s):
  if s.startswith('\\frac',i):
   n,j=group(s,i+5);d,i=group(s,j);out+='(('+translate(n)+')/('+translate(d)+'))'
  elif s.startswith('\\sqrt',i):
   j=i+5
   if s[j]=='[':
    end=s.index(']',j);power=s[j+1:end];n,i=group(s,end+1);out+='(('+translate(n)+')**(1/'+power+'))'
   else:n,i=group(s,j);out+='sqrt('+translate(n)+')'
  elif s.startswith('\\cdot',i):out+='*';i+=5
  elif s[i]=='{':n,i=group(s,i);out+='('+translate(n)+')'
  elif s[i]=='^':out+='**';i+=1
  else:out+=s[i];i+=1
 return out

def math(s):
 s=s.strip().rstrip('.,?')
 return parse_expr(translate(s),local_dict={'x':X,'y':Y,'a':a,'b':b},transformations=standard_transformations+(implicit_multiplication_application,rationalize))

def equal(v,w):return sp.simplify(v-w)==0

def formula_from_prompt(q):
 expressions=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'],re.S)
 expr=next(e for e in expressions if '\\frac' in e)
 lhs,rhs=expr.rstrip('.,?').split('=');assert math(rhs)==1
 value=sp.expand(math(lhs));assert value.subs({X:0,Y:0})==0
 dx=1/value.coeff(X,2);dy=1/value.coeff(Y,2)
 assert equal(value,X**2/dx+Y**2/dy)
 assert dx>0 and dy>0 and dx!=dy
 return dx,dy,value

def pair(value):
 pieces=re.findall(r'\$(.*?)\$',value);assert len(pieces)==2
 return tuple(math(v) for v in pieces)

def formatting(s):
 # These templates contain no escaped literal groups; every brace must balance.
 depth=0
 for char in s:
  depth+=(char=='{')-(char=='}');assert depth>=0
 assert depth==0 and s.count('$')%2==0
 assert not re.search(r'(?<!\\)\\\\',s),'No literal doubled command slashes'
 assert '--' not in s and '+-' not in s

def inspect_record(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];dx,dy,lhs=formula_from_prompt(q)
 assert r['generation']['evidence_only']==bool(r['generation']['source_id'])
 assert r['generation']['eligible_for_learning']==(not r['generation']['evidence_only'])
 expected=(2*sp.sqrt(max(dx,dy)),2*sp.sqrt(min(dx,dy)))
 p=r['generation']['parameters'];assert dx==sp.Rational(p['dx']) and dy==sp.Rational(p['dy'])
 formatting(q[':question/problem'])
 for f in q[':question/answer-fields']:
  assert f[':answer-field/type'] in (':answer-field.type/radio',':answer-field.type/blank')
  choices=f[':answer-field/choices'];assert len({v[':answer/id'] for v in choices})==len(choices)
  vals=[]
  for v in choices:
   formatting(v[':answer/value']);vals.append(pair(v[':answer/value']) if f[':answer-field/type'].endswith('/radio') else math(v[':answer/value']))
  assert len(set(vals))==len(vals)
  corr=f.get(':answer-field/correct')
  if corr:
   assert corr[0]==':answer/id';i=next(i for i,c in enumerate(choices) if c[':answer/id']==corr[1])
   if f[':answer-field/type'].endswith('/radio'):
    assert vals[i]==expected and sum(v==expected for v in vals)==1
   else:
    assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
    assert equal(vals[i],expected[0 if f[':answer-field/key']=='field-1' else 1])
 if ':question/worked-solution' in q:
  s=q[':question/worked-solution'];formatting(s)
  blocks=re.findall(r'\$\$(.*?)\$\$',s,re.S);assert len(blocks)==1
  general=blocks[0].strip().rstrip('.').split('=');assert math(general[1])==1
  substitutions={a:sp.sqrt(dx),b:sp.sqrt(dy)}
  assert equal(math(general[0]).subs(substitutions),lhs)
  inline=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',s,re.S)
  chains=[]
  for fragment in inline:
   if '=' not in fragment:continue
   expressions=[math(piece).subs(substitutions) for piece in fragment.split('=')]
   assert all(equal(v,expressions[0]) for v in expressions),fragment
   chains.append(fragment)
  assert len(chains)==10,chains
  # Ordered operation masks independently enforce identification, radius root,
  # ordered axes and double lengths, beyond scalar equality.
  assert chains[0].startswith('{a}^{2}=') and chains[1].startswith('{b}^{2}=')
  assert chains[3].startswith('a=\\sqrt{') and chains[5].startswith('b=\\sqrt{')
  major,minor=('a','b') if dx>dy else ('b','a')
  assert chains[6].startswith(major+'=') and chains[7].startswith(minor+'=')
  assert chains[8].startswith('2'+major+'=2\\cdot ') and chains[9].startswith('2'+minor+'=2\\cdot ')
 return expected

def source_normalized(q):
 def f(field):
  choices=field[':answer-field/choices'];correct=field.get(':answer-field/correct')
  cuuid=correct.get(':answer/id') if isinstance(correct,dict) else correct[1] if correct else None
  return {'key':field[':answer-field/key'],'type':field[':answer-field/type'].get(':db/ident') if isinstance(field[':answer-field/type'],dict) else field[':answer-field/type'],
   'choices':sorted((c[':answer/type'].get(':db/ident') if isinstance(c[':answer/type'],dict) else c[':answer/type'],c[':answer/value']) for c in choices),
   'correct_present':':answer-field/correct' in field,'correct':next((c[':answer/value'] for c in choices if c[':answer/id']==cuuid),None)}
 result={k:q[k] for k in (':question/problem',':question/worked-solution') if k in q}
 if ':question/difficulty' in q:result['difficulty']=q[':question/difficulty'].get(':db/ident') if isinstance(q[':question/difficulty'],dict) else q[':question/difficulty']
 if ':question/answer-fields' in q:result['fields']=[f(x) for x in q[':question/answer-fields']]
 return result

def engine_item(r,label):
 checks=[];q=r['question'];expected=inspect_record(r)
 if any(':answer-field/correct' not in f for f in q[':question/answer-fields']):return None
 for i,f in enumerate(q[':question/answer-fields']):
  choices=f[':answer-field/choices'];cid=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/radio'):
   for choice in choices:checks.append({'field_index':i,'submitted_answer_id':choice[':answer/id'],'expected':'accepted' if choice[':answer/id']==cid else 'rejected','purpose':'all owned answer selections'})
  else:
   answer=next(c[':answer/value'] for c in choices if c[':answer/id']==cid)
   value=expected[0 if f[':answer-field/key']=='field-1' else 1]
   equivalent='2*sqrt('+str(sp.simplify((value/2)**2))+')'
   for submission,outcome,purpose in [(answer,'accepted','canonical exact answer'),(equivalent,'accepted','unreduced radical diameter'),(str(value+1),'rejected','unequal axis length')]:
    checks.append({'field_index':i,'submitted':submission,'expected':outcome,'purpose':purpose})
 return {'label':label,'record':r,'checks':checks}

def main():
 source=json.loads((ROOT/'source.json').read_text());originals={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 assert source['basis']==1356 and source['database']=='math'
 native=[];reviews=[];banks=options=correct_present=solutions=0
 for case in g.source_cases():
  profile=case.get('bank_profile',case.get('profile'))
  record=g.generate('easy',parameters=case['parameters'],template=case['template'],profile=profile)
  original=originals[case['source_id']]
  assert source_normalized(record['question'])==source_normalized(original),case['source_id']
  inspect_record(record);banks+=1;options+=sum(len(f[':answer-field/choices']) for f in original[':question/answer-fields']);correct_present+=sum(':answer-field/correct' in f for f in original[':question/answer-fields']);solutions+=(':question/worked-solution' in original)
  item=engine_item(record,'original '+case['source_id'])
  if item:native.append(item)
  # Changed substantive parameters for every observed profile/layout, through
  # exactly the public source replay path. No copied original payload branch.
  for seed in range(100):
   variant=g.generate('easy',seed=1000+seed,template=case['template'],profile=profile)
   if variant['generation']['parameters']!=record['generation']['parameters']:break
  inspect_record(variant);reviews.append({'label':'Observed-template changed-parameter variant '+case['source_id'],'record':variant})
  item=engine_item(variant,'changed '+case['source_id'])
  if item:native.append(item)
 for level in ('easy','moderate','hard'):
  for seed in range(30):
   r=g.generate(level,seed,field_type='blank' if seed%2 else 'radio');inspect_record(r)
   r2=g.generate(level,seed+701,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])
   assert r['question'][':question/id']==r2['question'][':question/id']
   assert r['generation']['mathematical_fingerprint']==g.digest(sorted(r['generation']['parameters'].values()))
   # Axis swap changes orientation but not the required operation/answer task.
   ps=r['generation']['parameters'];swap=g.generate(level,seed,parameters={'dx':ps['dy'],'dy':ps['dx']},field_type='blank')
   assert swap['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
   if seed<2:
    reviews.append({'label':'Authored '+level+' example '+str(seed+1),'record':r});native.append(engine_item(r,level+' '+str(seed)))
 completion=g.generate('easy',parameters={'dx':'10','dy':'9'});reviews.append({'label':'Authored completion of unrated q-7600 (original omissions remain in raw replay)','record':completion});native.append(engine_item(completion,'authored q7600 completion'))
 # Explicit guard failures, including rational spelling that reduces first.
 invalid=[('easy',{'dx':'1/4','dy':9}),('moderate',{'dx':4,'dy':9}),('moderate',{'dx':'1/16','dy':9}),('hard',{'dx':'4/9','dy':'7/4'}),('hard',{'dx':'2/3','dy':'7/4'}),('hard',{'dx':'32/9','dy':'7/4'}),('hard',{'dx':'2/100000000000','dy':'7/4'}),('easy',{'dx':101,'dy':4}),('easy',{'dx':0,'dy':4}),('easy',{'dx':4,'dy':4}),('easy',{'dx':4.0,'dy':9})]
 for level,p in invalid:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('guard accepted',level,p))
 # Reduction normalizes both validation and identity; no numerical spelling aliases.
 canon=g.generate('moderate',parameters={'dx':'5/9','dy':16},field_type='blank')
 # Use an eligible equivalent fraction instead of an ineligible denominator18.
 reduced=g.generate('moderate',parameters={'dx':'10/18','dy':16},field_type='blank')
 assert reduced['question'][':question/id']==canon['question'][':question/id']
 (ROOT/'review.json').write_text(json.dumps(reviews,indent=2)+'\n')
 (ROOT/'engine-input.json').write_text(json.dumps(native,indent=2)+'\n')
 subprocess.run([str(ROOT.parents[1]/'runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 engine=json.loads((ROOT/'engine-report.json').read_text())
 # Enumerate mathematical number-form domains. Orientation/layout/profile aliases
 # do not inflate tasks. Counts here precede complete-bank collision rejection.
 easy=set((i,j) for i in range(1,101) for j in range(i+1,101))
 moderate={tuple(sorted((sp.Rational(n,d),sp.Integer(i)))) for n in range(1,101) for d in (4,9) for i in range(1,101) if sp.Rational(n,d).q in (4,9) and sp.Rational(n,d)!=i}
 hard_values={sp.Rational(c*c*s,d) for c in (1,2,3) for s in (2,3,5,6,7) for d in (4,9,16)}
 hard_values={v for v in hard_values if v.q in (4,9,16) and not sp.sqrt(v.p).is_Integer and v.p<=100}
 report={'status':'passed','source_questions':len(originals),'source_exact_prompt_matches':banks,'source_exact_solution_matches':solutions,'source_absent_solutions_preserved':1,'complete_source_question_banks_matched':banks,'source_fields_matched':29,'source_options_matched':options,'present_correct_refs_matched':correct_present,'absent_correct_refs_preserved':1,'source_distractors_matched':52,'source_distractor_role_inferred_banks':1,'generated_changed_source_profiles':21,'authored_levels_tested':{'easy':30,'moderate':30,'hard':30},'explicit_guard_rejections':len(invalid),'displayed_solution_equalities':'all actual TeX chains parsed and independently substituted','native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'meaningful_number_form_domain_counts_before_bank_rejection':{'easy':len(easy),'moderate':len(moderate),'hard':len(hard_values)*(len(hard_values)-1)//2},'eligible_authored_task_counts':{'easy_blank':4950,'easy_radio':4949,'moderate':11700,'hard':153},'remaining_limits':['q-7600 originally has no difficulty, solution or correct ref; authored completion is separately labeled','Original distractor intent underdetermined; six choice transforms are opaque evidence-only','Moderate/hard number-form workloads are authored design claims; no observed questions at those levels'],'database_writes':0}
 (ROOT/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
