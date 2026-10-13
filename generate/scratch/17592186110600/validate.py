#!/usr/bin/env python3
"""Independent displayed-expression, fidelity, scope, identity and native checks."""
import hashlib, importlib.util, json, re, subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
HERE=Path(__file__).resolve().parent
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=sp.symbols('x y')
def expr(s):
 s=s.strip().rstrip('.').replace(r'\cdot','*')
 while r'\frac' in s:
  old=s;s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
  assert old!=s,('Unparsed fraction',s)
 return parse_expr(s,local_dict={'x':x,'y':y},transformations=standard_transformations+(implicit_multiplication_application,))
def equation(s):
 lhs,rhs=s.replace('&','').split('=');return sp.expand(expr(lhs)-expr(rhs))
def norm(s):
 p=sp.Poly(equation(s),x,y);assert p.total_degree()<=1
 return tuple(str(z/p.LC()) for z in p.coeffs())+tuple(str(m) for m in p.monoms())
def line(s):
 e=equation(s);ay=e.coeff(y);assert ay!=0
 return -e.coeff(x)/ay,-e.subs({x:0,y:0})/ay
def correct_value(q):
 f=q[':question/answer-fields'][0];ref=f[':answer-field/correct'][1]
 return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ref)
def check(r):
 q=r['question'];meta=r['generation'];f=q[':question/answer-fields'][0]
 given=re.search(r'\$(.+)\?\$',q[':question/problem']).group(1)
 m,b=line(given);assert m!=0
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 assert len(f[':answer-field/choices'])==5
 vals=[a[':answer/value'] for a in f[':answer-field/choices']]
 assert len({norm(v) for v in vals})==5
 mathcorrect=[v for v in vals if line(v)[0]*m==-1]
 assert mathcorrect==[correct_value(q)]
 sol=q[':question/worked-solution'];body=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S).group(1)
 rows=body.split(r'\\');assert len(rows)==int(meta['template'][-1])
 assert all(norm(row)==norm(given) for row in rows)
 assert rows[0].strip().replace(' & ','')==given
 assert re.sub(r'\s','',rows[1].split('&')[0]) in ('y','-y',str(meta['parameters']['b'])+'y')
 if meta['template']=='standard4':
  assert r'\frac{'+str(abs(meta['parameters']['a']))+'}{'+str(abs(meta['parameters']['b']))+'}x' in rows[2]
  assert r'\frac' in rows[2]
 claimed=re.search(r'slope of the given line is \$(.+?)\.\$',sol).group(1)
 assert expr(claimed)==m
 claimed_perp=re.search(r'has a slope of \$(.+?)\.\$',sol).group(1)
 assert expr(claimed_perp)==-1/m
 product=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S)[-1];lhs,rhs=product.rstrip('.').split('=')
 assert expr(lhs)==expr(rhs)==-1
 for text in [q[':question/problem'],sol,*vals]:
  assert text.count('$')%2==0 and text.count('{')==text.count('}')
  assert 'feedback' not in text
 for ident in [q[':question/id'],f[':answer-field/id'],*[a[':answer/id'] for a in f[':answer-field/choices']]]:g.uuid.UUID(ident)
 assert meta['task_fingerprint']==g.digest({'kp':g.KP_ID,'slope':str(m)})
 assert f[':answer-field/correct'][0]==':answer/id'
 return r

def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
def run():
 source=json.loads((HERE/'source.json').read_text());questions=source['record'][':knowledge-point/questions'];cases=json.loads((HERE/'source-cases.json').read_text())
 assert len(cases)==len(questions)==8
 capture=HERE.parents[1]/'runs/current/sources/17592186110600.json'
 assert capture.read_bytes()==(HERE/'source.json').read_bytes()
 reviews=[];fidelity=[];native=[];reviewtext=['# Step 6 review: originals and generated variants','All originals are captured math basis 1356. Generated records are labeled; authored hard scope is a design claim.']
 byid={q[':question/math-academy-id']:q for q in questions}
 for case in cases:
  original=byid[case['source_id']];r=check(g.generate(case['level'],parameters=case['parameters'],profile=case['bank_profile'],template=case['template']))
  q=r['question'];of=original[':question/answer-fields'][0]
  assert q[':question/problem']==original[':question/problem']
  assert q[':question/worked-solution']==original[':question/worked-solution'],(case['source_id'],q[':question/worked-solution'],original[':question/worked-solution'])
  assert sorted(norm(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(norm(a[':answer/value']) for a in of[':answer-field/choices'])
  assert sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  assert norm(correct_value(q))==norm(of[':answer-field/correct'][':answer/value'])
  fidelity.append({'source_id':case['source_id'],'options':5,'distractors':4,'complete_bank':True,'exact_prompt':True,'exact_solution':True,'correct_designation':True})
  reviews.append(r);reviewtext += ['\n## Original '+case['source_id'],g.markdown(r)]
  vp=dict(case['parameters']);vp['c']+=vp['b'] if case['level']=='moderate' else 1;vp['d']=[str(sp.Rational(d)+1) for d in vp['d']]
  # Change assessed slope while retaining observed bank's explicit operations.
  if case['level']=='easy':vp['a']+=vp['b'] if sp.Rational(-vp['a'],vp['b'])<0 else -vp['b']
  elif case['template']=='standard3':vp['b']+=1;vp['c']=2*vp['b']
  else:vp['a']=6;vp['c']=2*vp['b']
  variant=check(g.generate(case['level'],seed=77,parameters=vp,profile=case['bank_profile'],template=case['template']))
  reviews.append(variant);reviewtext+=['\n## Generated observed-profile variant '+case['source_id'],g.markdown(variant)]
 tasks={};samples=0
 for level in g.TEMPLATES:
  pool=[check(g.generate(level,seed=i,template=g.TEMPLATES[level][i%len(g.TEMPLATES[level])])) for i in range(1000)]
  tasks[level]=len({r['generation']['task_fingerprint'] for r in pool});samples+=len(pool)
  assert tasks[level]>=({'easy':16,'moderate':40,'hard':50}[level])
  for r in pool[:2]:reviews.append(r);reviewtext+=['\n## Generated authored '+level,g.markdown(r)]
  base=pool[0];p=base['generation']['parameters'];template=base['generation']['template']
  r2=check(g.generate(level,seed=987,parameters=p,template=template))
  assert base['question'][':question/id']==r2['question'][':question/id']
  altered=dict(p);altered['d']=list(p['d']);altered['d'][0]=str(sp.Rational(p['d'][0])+1)
  r3=check(g.generate(level,parameters=altered,template=template))
  assert base['question'][':question/id']!=r3['question'][':question/id']
  assert base['generation']['task_fingerprint']==r3['generation']['task_fingerprint']
 # Boundary and selectable observed-profile checks exercise normal sampling.
 for profile,(level,template,_,_) in g.PROFILES.items():
  if profile!='authored':
   for seed in range(10):check(g.generate(level,seed,profile=profile))
 for level,template,p in [('easy','standard3',dict(a=-45,b=5,c=24,d=[0]*5)),('moderate','standard4',dict(a=-15,b=27,c=0,d=[0]*5)),('hard','standard4',dict(a=27,b=6,c=1,d=[0]*5)),('hard','standard4',dict(a=4,b=6,c=1,d=[0]*5))]:check(g.generate(level,template=template,parameters=p))
 scaled1=g.generate('easy',parameters=dict(a=4,b=2,c=8,d=[0]*5))
 scaled2=g.generate('easy',parameters=dict(a=8,b=4,c=16,d=[0]*5))
 assert scaled1['generation']['task_fingerprint']==scaled2['generation']['task_fingerprint']
 assert scaled1['question'][':question/id']!=scaled2['question'][':question/id']
 # Explicit scope inputs and ambiguous complete bank must fail, never resample.
 bad=[('easy',dict(a=-4,b=2,c=8,d=['1/11']*5)),('easy',dict(a=-4,b=2,c=8,d=[0]*5,u=10)),('easy',{'a':1,'b':1,'c':1,'d':[0]*5}),('hard',{'a':-60,'b':14,'c':1,'d':[0]*5}),('hard',{'a':-4,'b':6,'c':12,'d':[0]*5}),('moderate',{'a':-4,'b':2,'c':4,'d':[0]*5})]
 for l,p in bad:
  try:g.generate(l,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Explicit scope error accepted')
 badcase=dict(cases[-1]['parameters']);badcase['d']=list(badcase['d']);badcase['d'][4]=badcase['d'][0]
 try:g.generate('easy',parameters=badcase,profile=cases[-1]['bank_profile'])
 except ValueError:pass
 else:raise AssertionError('Duplicate complete bank accepted')
 for i,r in enumerate(reviews):
  f=r['question'][':question/answer-fields'][0]
  native.append({'label':str(i),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned radio selection through actual native grader'} for a in f[':answer-field/choices']]})
 write('engine-input.json',native)
 engine=HERE.parents[1]/'runs/current/check-engine'
 subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 write('review.json',reviews);(HERE/'review.md').write_text('\n\n'.join(reviewtext)+'\n')
 write('validation.json',{'passed':True,'source':g.SOURCE,'source_fidelity':{'questions':'8/8','banks':'8/8','options':'40/40','distractors':'32/32','correct_designations':'8/8','exact_prompts':'8/8','exact_solutions':'8/8','repairs':0},'fidelity_details':fidelity,'display_math_samples':samples,'task_fingerprints_by_level':tasks,'review_records':len(reviews),'native_grading':json.loads((HERE/'engine-report.json').read_text()),'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'stopped_after_step':7,'database_writes':0,'unresolved_findings':[],'interpretation_limits':'Explicit incidental candidate slopes and independent intercepts preserve observed banks; original distractor error algorithms are not inferred.','coefficient_processing_structures':['easy integer slope / unit or nonunit y coefficient','moderate unit numerator or nonunit proper rational slope; optional raw-fraction row','authored hard nonunit reduced numerator and denominator; raw-fraction row; fractional intercept']})
 print('PASS: 8/8 full source replays, 3000 displayed mathematics samples, native grader and scope/identity checks; task directions',tasks)
if __name__=='__main__':run()
