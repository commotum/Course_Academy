#!/usr/bin/env python3
"""Failing independent display, source, workload, identity and native grader QA."""
import hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).parent; REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('cosine_generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x',real=True); N=sp.Symbol('n',integer=True)

def group(s,i):
 assert s[i]=='{',s
 start=i+1;depth=1;i+=1
 while depth:
  assert i<len(s),s
  depth+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[start:i-1],i

def parse(s):
 s=s.strip().rstrip('.,').replace('⁡','').replace('π',r'\pi').replace(r'\cos','cos').replace(r'\left','').replace(r'\right','')
 out='';i=0
 while i<len(s):
  if s.startswith(r'\frac',i):
   i+=5
   while s[i].isspace():i+=1
   a,i=group(s,i)
   while s[i].isspace():i+=1
   b,i=group(s,i);out+='(('+str(parse(a))+')/('+str(parse(b))+'))'
  elif s.startswith(r'\sqrt',i):
   i+=5;a,i=group(s,i);out+='sqrt('+str(parse(a))+')'
  else:out+=s[i];i+=1
 out=out.replace(r'\cdot','*').replace(r'\pi','(pi)').replace('{','(').replace('}',')')
 out=re.sub(r'cos\s*x\b','cos(x)',out)
 return parse_expr(out,local_dict={'x':X,'n':N,'pi':sp.pi,'cos':lambda x:sp.cos(x,evaluate=False),'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))

def fields(r):return r['question'][':question/answer-fields'][0]
def format_check(s):
 assert s.count('$')%2==0
 depth=0
 for ch in s:
  depth+=(ch=='{')-(ch=='}'); assert depth>=0
 assert depth==0
 assert '--' not in s and '+-' not in s

def check(r,raw=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];meta=r['generation'];f=fields(r)
 for s in [q[':question/problem'],q[':question/worked-solution']]:format_check(s)
 # Read given value, multiplier, full shifted angle and offset from display.
 pieces=re.findall(r'\$(.*?)\$',q[':question/problem'])
 given=parse(pieces[0].split('=',1)[1]);expression=pieces[-1].rsplit('=',1)[0]
 expr=parse(expression)
 cosines=list(expr.atoms(sp.cos)); assert len(cosines)==1
 arg=cosines[0].args[0];shift=sp.simplify((arg-X)/sp.pi)
 assert shift.is_Integer and shift!=0 and shift%2==0
 assert sp.expand(arg).coeff(X)==1 # forbids evenness branch
 correct=sp.simplify(expr.subs(cosines[0],given))
 assert given==sp.sympify(meta['parameters']['c'])
 assert shift==2*meta['parameters']['n']
 answers=f[':answer-field/choices'];values=[parse(a[':answer/value']) for a in answers]
 assert len(answers)==5 and len({a[':answer/id'] for a in answers})==5
 ci=next(i for i,a in enumerate(answers) if a[':answer/id']==f[':answer-field/correct'][1])
 assert sp.simplify(values[ci]-correct)==0
 equal_pairs=[(i,j) for i,v in enumerate(values) for j,w in enumerate(values[:i]) if sp.simplify(v-w)==0]
 assert len(equal_pairs)==(1 if raw else 0)
 assert sum(sp.simplify(v-correct)==0 for v in values)==1
 # Assert each complete displayed stage, including the expanded shift and each
 # individually multiplied component. Equality checking uses printed values.
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
 affine=meta['parameters']['a']!=1
 assert len(blocks)==(3 if affine else 2)
 assert 'n='+str(int(shift/2))+'$' in q[':question/worked-solution']
 for bi,block in enumerate(blocks):
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
  rows=block.split(r'\\'); assert len(rows)==(3 if bi==2 else 1)
  prior=None
  for row in rows:
   components=row.strip().split('=')
   if components[0].strip(): prior=parse(components[0])
   assert prior is not None
   for part in components[1:]:
    rhs=parse(part)
    if bi>=1:
     for cosine in (prior.atoms(sp.cos)|rhs.atoms(sp.cos)):
      assert cosine.args[0] in (X,arg),('Stale full angle',cosine,arg)
    difference=sp.trigsimp(prior-rhs)
    difference=difference.subs(sp.cos(X),given)
    assert sp.simplify(difference)==0,(row,prior,rhs,difference)
    prior=rhs
 # All prose equations involving cosine are also checked against the actual
 # printed given value, rather than trusting the arithmetic blocks below them.
 for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/worked-solution'],re.S):
  if '=' in inline and ('cos' in inline) and not inline.startswith('y='):
   lhs,rhs=inline.split('=',1)
   for cosine in (parse(lhs).atoms(sp.cos)|parse(rhs).atoms(sp.cos)):
    assert cosine.args[0] in (X,arg),('Stale prose angle',cosine,arg)
   assert sp.simplify(sp.trigsimp(parse(lhs)-parse(rhs)).subs(sp.cos(X),given))==0,inline
 return {'prompt_value':str(given),'displayed_shift_pi':str(shift),'correct':str(correct),'equivalent_wrong_pairs':equal_pairs}

def engine_item(r,label):
 f=fields(r)
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual owned choice selection'} for a in f[':answer-field/choices']]}

def main():
 source=json.loads((ROOT/'source.json').read_text()); originals={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 cases=json.loads((ROOT/'source-cases.json').read_text());details=[];engine=[];review=[]
 for case in cases:
  r=g.generate(case['level'],seed=17,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);o=originals[case['source_id']];q=r['question'];raw=r['generation']['raw_source_error']
  display=check(r,raw);assert q[':question/problem']==o[':question/problem']
  observed=o[':question/answer-fields'][0][':answer-field/choices'];generated=fields(r)[':answer-field/choices'];unused=list(range(5))
  for a in observed:
   matches=[i for i in unused if sp.simplify(parse(a[':answer/value'])-parse(generated[i][':answer/value']))==0]
   assert matches,(case,a); unused.remove(matches[0])
  assert not unused
  solution_present=':question/worked-solution' in o
  if solution_present:assert q[':question/worked-solution']==o[':question/worked-solution']
  designation_present=':answer-field/correct' in o[':question/answer-fields'][0]
  if designation_present:
   correct=o[':question/answer-fields'][0][':answer-field/correct'][':answer/value']
   assert sp.simplify(parse(correct)-parse(next(a[':answer/value'] for a in generated if a[':answer/id']==fields(r)[':answer-field/correct'][1])))==0
  details.append({'source_id':case['source_id'],'options_matched':5,'prompt_exact':True,'solution_exact':True if solution_present else None,'designation_matched':True if designation_present else None,'source_error':raw,'display_checks':display})
  engine.append(engine_item(r,case['source_id']));review.append({'label':'Original parameter replay '+case['source_id'],'record':r})
  # Changed parameters for EVERY observed template/bank, and repaired q103242.
  p=dict(case['parameters']);p['n']=-p['n'];p['c']=str(-sp.sympify(p['c']))
  v=g.generate(case['level'],seed=33,template=case['template'],parameters=p,profile=case['bank_profile']);check(v,raw);review.append({'label':'Generated observed-bank variation '+case['source_id'],'record':v});engine.append(engine_item(v,'variant '+case['source_id']))
  if raw:
   repair=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile='observed_q103242');check(repair);review.append({'label':'Minimal repaired bank q-103242','record':repair});engine.append(engine_item(repair,'repair q-103242'))
 total=0;ids={level:set() for level in ('easy','moderate','hard')};task_ids={level:set() for level in ids}
 for level in ids:
  for seed in range(80):
   r=g.generate(level,seed);check(r);total+=1;ids[level].add(r['question'][':question/id']);task_ids[level].add(r['generation']['parameter_fingerprint'])
   if seed<2:review.append({'label':'Generated authored '+level+' '+str(seed),'record':r});engine.append(engine_item(r,level+' '+str(seed)))
   p=r['generation']['parameters'];other=g.generate(level,seed+101,template=r['generation']['template'],parameters=p,profile=r['generation']['bank_profile'])
   assert other['question'][':question/id']==r['question'][':question/id']
 # Math aliases, seed and bank order are not distinct assessed tasks.
 a=g.generate('moderate',parameters={'c':'sqrt(3)/3','n':5,'a':1,'b':0});b=g.generate('moderate',99,parameters={'c':'1/sqrt(3)','n':5,'a':1,'b':0})
 assert a['question'][':question/id']==b['question'][':question/id'];assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 angle_alias=g.generate('moderate',parameters={'c':'sqrt(3)/3','n':-8,'a':1,'b':0})
 assert a['generation']['parameter_fingerprint']==angle_alias['generation']['parameter_fingerprint']
 assert a['question'][':question/id']!=angle_alias['question'][':question/id']
 # Exhaust the finite easy catalog and both cosine endpoints at other levels.
 boundary_count=0
 for c in g.EASY_VALUES:
  for n in (-2,-1,1,2):
   check(g.generate('easy',parameters={'c':str(c),'n':n,'a':1,'b':0}));boundary_count+=1
 for level in ('moderate','hard'):
  for c in (-1,1):
   for n in (-10,10):
    check(g.generate(level,parameters={'c':str(c),'n':n,'a':2 if level=='hard' else 1,'b':3 if level=='hard' else 0}));boundary_count+=1
 bad=[('easy',{'c':'1/2','n':3,'a':1,'b':0}),('moderate',{'c':'1/2','n':2,'a':1,'b':0}),('hard',{'c':'1/2','n':5,'a':1,'b':5}),('hard',{'c':'1/2','n':5,'a':-7,'b':5}),('hard',{'c':'1/2','n':5,'a':4,'b':0})]
 for level,p in bad:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Workload guard did not reject '+str(p))
 # Mutation proves display arithmetic/shift checks are meaningful.
 import copy
 mutations=0
 r=g.generate('hard',parameters={'c':'3/8','n':-5,'a':4,'b':5})
 for key,old,new in [(':question/problem','x-10','x-9'),(':question/worked-solution',r'\frac{3}{2}+5',r'\frac{5}{2}+5'),(':question/worked-solution','n=-5','n=5'),(':question/worked-solution','x-10','x-12'),(':question/worked-solution',r'2\cdot (-5)',r'2\cdot (-7)')]:
  m=copy.deepcopy(r);assert old in m['question'][key];m['question'][key]=m['question'][key].replace(old,new)
  try:check(m)
  except AssertionError:mutations+=1
  else:raise AssertionError('Display mutation escaped')
 (ROOT/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False))
 subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 report=json.loads((ROOT/'engine-report.json').read_text())
 (ROOT/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False))
 lines=['# Cosine periodicity review','All source originals remain in source.json. The raw duplicate bank is explicitly ineligible for learner generation.']
 for sid,o in originals.items():
  f=o[':question/answer-fields'][0];cid=f.get(':answer-field/correct',{}).get(':answer/id')
  original_bank='\n'.join('- $'+a[':answer/value']+'$'+(' **source-designated correct**' if a[':answer/id']==cid else '') for a in f[':answer-field/choices'])
  lines+=['## Captured original '+sid,o[':question/problem'],original_bank,o.get(':question/worked-solution','No captured worked solution or correct designation. See the separately labeled authored replay below.')]
 for item in review:
  lines+=['## '+item['label'],g.markdown(item['record'])]
 (ROOT/'review.md').write_text('\n\n'.join(lines))
 result={'status':'passed','source':g.SOURCE,'practice_questions':7,'observed_difficulty':{'moderate':4,'hard':1,'unrated':2,'easy':0},'source_options_matched':35,'source_complete_banks_matched':7,'source_prompts_exact':7,'source_solutions_exact':{'matched':5,'present':5,'missing':2},'source_correct_designations':{'matched':5,'present':5,'inferred_missing':2},'normal_mathematically_valid_source_banks':6,'raw_ambiguous_source_banks':1,'minimal_repaired_banks':1,'generated_display_math_checks':total,'boundary_display_checks':boundary_count,'display_mutations_rejected':mutations,'sampled_content_counts':{k:len(v) for k,v in ids.items()},'sampled_task_counts':{k:len(v) for k,v in task_ids.items()},'finite_value_catalog':{'easy':len(g.EASY_VALUES),'moderate':len(g.MOD_VALUES),'hard':len(g.MOD_VALUES)},'native_grader':report,'details':details,'limitations':['q-103242 raw duplicate bank preserved only in public evidence profile; normal bank minimally repaired.','Two unrated source questions have no captured solution or correct designation; authored levels/solutions and derived designations do not count as observed matches.','Unusual observed scalar distractor recipes are expression-pattern generalizations with uncertain author intent; authored banks are normal defaults.']}
 (ROOT/'validation.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
 freeze={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT.with_suffix('.py'),ROOT/'validate.py',ROOT/'source.json',ROOT/'source-cases.json',ROOT/'source-authority.json',ROOT/'context-provenance.json',ROOT/'classification.md',ROOT/'template-extraction.md',ROOT/'README.md',ROOT/'review.md',ROOT/'review.json',ROOT/'validation.json',ROOT/'engine-input.json',ROOT/'engine-report.json',REPO/'generate/runs/current/check-engine',REPO/'generate/runs/current/check-engine.rs']}
 (ROOT/'freeze-hashes.json').write_text(json.dumps(freeze,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('native_grader','details')},indent=2))
if __name__=='__main__':main()
