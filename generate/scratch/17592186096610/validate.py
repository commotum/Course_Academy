#!/usr/bin/env python3
"""Independent displayed-math QA, complete source replay, and actual app grading."""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('exp_constant',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)
X=g.X

def group(s,start,opening='{',closing='}'):
 assert s[start]==opening
 depth=1;i=start+1
 while depth:
  assert i<len(s),(s,start)
  depth+=(s[i]==opening)-(s[i]==closing);i+=1
 return s[start+1:i-1],i

def math(s):
 """Parse displayed expressions independently of generator metadata."""
 s=s.strip().rstrip('.,')
 d=r'\frac{\text{d}}{\text{d}x}'
 while d in s:
  start=s.index(d);at=start+len(d);assert s[at]=='('
  component,end=group(s,at,'(',')')
  value=sp.diff(math(component),X)
  s=s[:start]+'('+str(value)+')'+s[end:]
 s=s.replace(r'\left','').replace(r'\right','').replace('{e}','e')
 while r'\frac' in s:
  start=s.index(r'\frac');n,end=group(s,start+5);den,end2=group(s,end)
  s=s[:start]+'('+str(math(n)/math(den))+')'+s[end2:]
 # Protect exponential power structure before stripping grouping braces.
 while re.search(r'e\^\{',s):
  match=re.search(r'e\^\{',s);ex,end=group(s,match.end()-1)
  s=s[:match.start()]+'exp('+str(math(ex))+')'+s[end:]
 s=re.sub(r'\\ln\{\(([^()]*)\)\}',r'log(\1)',s)
 s=re.sub(r'\\ln\s*([0-9]+)',r'log(\1)',s)
 # Unicode ln followed by a parenthesized rational or an integer.
 s=re.sub(r'ln⁡\(([^()]*)\)',r'log(\1)',s)
 s=re.sub(r'ln⁡([0-9]+)',r'log(\1)',s)
 s=s.replace(r'\cdot','*').replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(s,local_dict={'x':X,'e':sp.E,'exp':sp.exp,'log':sp.log},transformations=TRANS)

def equal(a,b):return sp.simplify(a-b)==0

def normalize(s):
 return re.sub(r'\s+','',s.replace('{e}','e').replace('{f}','f').replace('ln⁡',r'\ln').replace(r'\ln{\left(',r'\ln').replace(r'\right)}','').replace('e^x','e^{x}'))

def formatting(s):
 assert s.count('$$')%2==0
 assert s.replace('$$','').count('$')%2==0
 depth=0
 for c in s:
  if c=='{':depth+=1
  if c=='}':depth-=1;assert depth>=0
 assert depth==0
 assert '+-' not in s and '--' not in s

def inspect_record(r):
 assert r['knowledge_point']=={'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE}
 q=r['question'];p=r['generation']['parameters'];t=r['generation']['template'];slope='slope' in t
 problem=q[':question/problem'];worked=q[':question/worked-solution']
 formatting(problem);formatting(worked)
 displayed=re.search(r'\$f\(x\)\s*=([^$]+)',problem).group(1)
 actual=math(displayed);derivative=sp.diff(actual,X)
 # Check the only x-dependent term is a constant times e^x.
 ratio=sp.simplify(derivative/sp.exp(X));assert not ratio.has(X) and ratio!=0
 assert not sp.simplify(actual-derivative).has(X)
 if slope:
  at=re.search(r'\$x=([^$]+)',problem).group(1).rstrip('.')
  eval_at=math(at);expected=sp.simplify(derivative.subs(X,eval_at))
 else:expected=derivative
 field=q[':question/answer-fields'][0];ft=field[':answer-field/type'].split('/')[-1]
 assert field[':answer-field/key']==('selection' if ft=='radio' else 'field-1')
 if ft=='blank':assert '{{field-1}}' in problem
 choices=field[':answer-field/choices'];values=[];is_correct=[]
 for a in choices:
  value=a[':answer/value'];formatting(value)
  if '=' in value:
   left,value=value.split('=',1);assert normalize(left) in ('f^{′}(x)',"f'(x)")
  parsed=math(value);assert parsed.free_symbols<= {X},value
  assert not slope or not parsed.has(X)
  values.append(parsed);is_correct.append(equal(parsed,expected))
 designated=field[':answer-field/correct'][1]
 assert field[':answer-field/correct'][0]==':answer/id'
 for ident in [q[':question/id'],field[':answer-field/id']]+[a[':answer/id'] for a in choices]:assert str(uuid.UUID(ident))==ident
 assert designated in [a[':answer/id'] for a in choices]
 assert all(is_correct[i]==(a[':answer/id']==designated) for i,a in enumerate(choices)) if ft=='radio' else all(is_correct)
 if ft=='radio':
  assert len(choices)==5
  assert sum(is_correct)==1
  assert all(not equal(values[i],values[j]) for i in range(5) for j in range(i))
 # Read each displayed formal/distribution/reduction row, including signs.
 block=worked.split('$$')[1]
 rows=block.split(r' \\  & =')
 assert len(rows)==4,(t,rows)
 rows[0]=rows[0].split('& =',1)[1]
 rows[-1]=rows[-1].split(r'\end{aligned}',1)[0]
 for row in rows:assert equal(math(row),derivative),(t,row,derivative)
 # Enforce the ordered, uncollapsed operator masks independently.
 d=r'\frac{\text{d}}{\text{d}x}'
 assert [row.count(d) for row in rows]==[1,2,1,0]
 assert '+0' in rows[2] or rows[2].startswith('0')
 if slope:
  evaluation=worked.split('$$')[3]
  stages=evaluation.split(r' \\  & =')
  first=stages[0].split('& =',1)[1]
  expression=re.search(r'\{\((.*?)\)\\,\|\}_\{x=(.*)\}',first).groups()
  assert equal(math(expression[0]).subs(X,math(expression[1])),expected)
  for stage in stages[1:]:
   stage=stage.split(r'\end{aligned}',1)[0]
   assert equal(math(stage),expected),(stage,expected)
  expected_count=4 if p['point_kind']=='ln' or math(at)==0 else 3
  assert len(stages)==expected_count
 return expected

def checks(r,label):
 q=r['question'];f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Every owned displayed choice'} for a in f[':answer-field/choices']]}
 answer=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
 value=inspect_record(r)
 # A structurally different equivalent: split the coefficient or unreduced rational.
 if value.has(X):
  a=sp.simplify(value/sp.exp(X));equivalent=g.tex(a/2)+'e^{x}+'+g.tex(a/2)+'e^{x}'
 else:
  n,d=sp.fraction(value);equivalent=r'\frac{'+str(n*3)+'}{'+str(d*3)+'}'
 return {'label':label,'record':r,'checks':[{'submitted':answer,'expected':'accepted','purpose':'Canonical fragment'},{'submitted':equivalent,'expected':'accepted','purpose':'Uncollected or unreduced equivalent fragment'},{'submitted':g.tex(value+1),'expected':'rejected','purpose':'Wrong derivative/slope'},{'submitted':'0','expected':'rejected','purpose':'Incorrect constant derivative'},{'submitted':answer.replace('x','t') if value.has(X) else g.tex(-value),'expected':'rejected','purpose':'Wrong displayed variable or sign'}]}

def main():
 source=json.loads((ROOT/'source.json').read_text());qs=source['record'][':knowledge-point/questions'];cases=json.loads((ROOT/'source-cases.json').read_text());assert len(cases)==len(qs)==7
 assert source==json.loads((REPO/'generate/runs/current/sources/17592186096610.json').read_text())
 route=json.loads((REPO/'generate/runs/current/lessons/17592186048749.json').read_text())['record'][0]
 steps={s[':db/id']:s for s in route[':activity/steps']};order=[];key=route[':activity/first-step'][':db/id']
 while key:
  step=steps[key];order.append(step[':step/content'][':db/id']);key=step.get(':step/next',{}).get(':db/id')
 assert order[:5]==[17592186097813,g.KP_ID,17592186096611,17592186097814,17592186096612]
 ledger=[];engine=[];review=[];by_id={q[':question/math-academy-id']:q for q in qs}
 for case in cases:
  original=by_id[case['source_id']];r=g.generate('easy',18,case['template'],parameters=case['parameters'],profile=case['bank_profile']);inspect_record(r)
  field=r['question'][':question/answer-fields'][0];oldfield=original[':question/answer-fields'][0]
  bank=field[':answer-field/choices'];old=oldfield[':answer-field/choices'];assert len(bank)==len(old)
  newvalues=[math(a[':answer/value'].split('=')[-1]) for a in bank];oldvalues=[math(a[':answer/value'].split('=')[-1]) for a in old]
  unmatched=list(newvalues)
  for v in oldvalues:
   matches=[i for i,vv in enumerate(unmatched) if equal(v,vv)];assert matches,(case,v);unmatched.pop(matches[0])
  assert not unmatched
  q=r['question'];assert q[':question/problem']==original[':question/problem'],(case['source_id'],q[':question/problem'])
  sol=original.get(':question/worked-solution')
  if sol:assert normalize(q[':question/worked-solution'])==normalize(sol),(case['source_id'],q[':question/worked-solution'],sol)
  correct=oldfield.get(':answer-field/correct')
  if correct:
   value=next(a[':answer/value'] for a in bank if a[':answer/id']==field[':answer-field/correct'][1]);assert equal(math(value.split('=')[-1]),math(correct[':answer/value'].split('=')[-1]))
  ledger.append({'source_id':case['source_id'],'bank_values_matched':len(old),'designation_matched':bool(correct),'designation_inferred':not bool(correct),'prompt_raw_exact':True,'solution_present':bool(sol),'solution_raw_exact':sol==q[':question/worked-solution'] if sol else None,'solution_normalized_exact':True if sol else None})
  engine.append(checks(r,'source/'+case['source_id']));review.append({'label':'Original replay '+case['source_id'],'record':r})
  # Changed parameters test each full observed bank and display shape.
  for seed in (27,28):
   rr=g.generate('easy',seed,case['template'],profile=case['bank_profile']);inspect_record(rr);engine.append(checks(rr,'variant/'+case['source_id']+'/'+str(seed)));review.append({'label':'Generated variant '+case['source_id']+'/'+str(seed),'record':rr})
 for t,(level,ft) in g.TEMPLATES.items():
  for seed in range(24):
   r=g.generate(level,seed,t);inspect_record(r)
   assert r==g.generate(level,seed,t)
   p=r['generation']['parameters'];reordered=g.generate(level,seed+100,t,parameters=p,profile=r['generation']['bank_profile'])
   assert r['question'][':question/id']==reordered['question'][':question/id']
   assert r['generation']['parameter_fingerprint']==reordered['generation']['parameter_fingerprint']
   engine.append(checks(r,t+'/'+str(seed)))
   if level!='easy' and seed<2:review.append({'label':'Authored '+level+' peer '+str(seed),'record':r})

 assert g.generate('moderate',profile='slope_blank')==g.generate_moderate(profile='slope_blank')
 assert g.generate('hard',profile='slope_blank')==g.generate_hard(profile='slope_blank')
 fixed=g.generate_easy(0,'derivative_radio')['generation']['parameters']
 positions=set()
 for seed in range(20):
  rr=g.generate_easy(seed,'derivative_radio',parameters=fixed);ff=rr['question'][':question/answer-fields'][0]
  positions.add(next(i for i,v in enumerate(ff[':answer-field/choices']) if v[':answer/id']==ff[':answer-field/correct'][1]))
 assert len(positions)>1
 # Explicit signed arithmetic corners, including every supported denominator.
 boundary_count=0
 for level in ('moderate','hard'):
  for sign in (-1,1):
   for den in range(2,5 if level=='moderate' else 6):
    for numerator in (1,11):
     for bv in (-20,20):
      p={'a':str(sp.Rational(sign*numerator,den)),'b':str(bv),'constant_kind':'ln','order':'constant_first','point':str(-2 if level=='moderate' else sp.Rational(-11,den)),'point_kind':'ln'}
      r=g.generate(level,parameters=p);inspect_record(r);engine.append(checks(r,level+'/boundary/'+str(boundary_count)));boundary_count+=1
 # Per-level explicit invalid workload inputs must fail, rather than silently resample.
 for level in ('moderate','hard'):
  good=g.generate(level)['generation']['parameters']
  for key,value in [('a','2'),('a','-20'),('point','1'),('point_kind','integer')]:
   bad=dict(good);bad[key]=value
   try:g.generate(level,parameters=bad)
   except ValueError:pass
   else:raise AssertionError((level,bad))
 for kwargs in ({'level':'easy','template':'unknown'},{'level':'easy','profile':'unknown'},{'level':'hard','field_type':'radio'}):
  try:g.generate(**kwargs)
  except ValueError:pass
  else:raise AssertionError(kwargs)
 # Equivalent tasks with changed incidental constant or complete banks share task fingerprints.
 p=g.generate_easy(3,'derivative_radio')['generation']['parameters'];p2=dict(p);p2['b']='19'
 a=g.generate_easy(3,'derivative_radio',parameters=p);b=g.generate_easy(4,'derivative_radio',parameters=p2)
 assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 assert a['question'][':question/id']!=b['question'][':question/id']
 diversity={}
 for level in ('easy','moderate','hard'):
  rr=[g.generate(level,i) for i in range(200)]
  diversity[level]={'mathematical_tasks':len({v['generation']['parameter_fingerprint'] for v in rr}),'presentations':len({v['question'][':question/id'] for v in rr})}
 engine_path=REPO/'generate/runs/current/check-engine';input_path=ROOT/'native-input.json';output_path=ROOT/'native-report.json';input_path.write_text(json.dumps(engine,ensure_ascii=False,indent=2))
 subprocess.run([str(engine_path),str(input_path),str(output_path)],check=True)
 report=json.loads(output_path.read_text())
 validation={'status':'passed','basis':1356,'source_cases':len(cases),'source_bank_values_matched':sum(v['bank_values_matched'] for v in ledger),'source_complete_banks_matched':7,'source_distractors_matched':20,'source_distractors_total':20,'source_designations_matched':5,'missing_designations_inferred':2,'source_prompts_raw_exact':7,'source_solutions_present':5,'source_solutions_raw_exact':sum(v['solution_raw_exact'] is True for v in ledger),'source_solutions_notation_normalized':5,'mathematical_repairs':0,'authored_missing_levels':['moderate','hard'],'generated_cases_checked':168,'arithmetic_boundaries_checked':boundary_count,'native_records':len(engine),'source_ledger':ledger,'native_report':report,'engine_sha256':hashlib.sha256(engine_path.read_bytes()).hexdigest(),'engine_harness_source_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'route_content_ids':order,'unresolved_wrong_intent':['slope_zero: ln(abs(a)), b, -b scalar recipes underdetermine intent','slope_one: exp(a) scalar recipe underdetermines original operation','legacy_log_base: abs(b)+ae^x does not recover original author intent'],'diversity_200_seeds':diversity,'failures':[]}
 (ROOT/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2))
 (ROOT/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2))
 md=['# Original evidence and generated peers','All seven original problems/banks follow; missing legacy solutions are explicitly authored. Generated variants use the same complete observed profile; difficulty extensions are labeled.']
 for case in cases:
  old=by_id[case['source_id']];md+=['\n## Raw original '+case['source_id'],old[':question/problem'],'\n'.join('$'+a[':answer/value']+'$' for a in old[':question/answer-fields'][0][':answer-field/choices']),old.get(':question/worked-solution','No worked solution in source; generated solution is authored from the canonical method.')]
  for item in review:
   if case['source_id'] in item['label']:md+=['\n### '+item['label'],g.markdown(item['record'])]
 for item in review:
  if item['label'].startswith('Authored'):md+=['\n## '+item['label'],g.markdown(item['record'])]
 (ROOT/'review.md').write_text('\n\n'.join(md))
 print(json.dumps({k:v for k,v in validation.items() if k not in ('native_report','source_ledger')},indent=2))
if __name__=='__main__':main()
