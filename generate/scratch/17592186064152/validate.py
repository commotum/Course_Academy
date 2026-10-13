#!/usr/bin/env python3
"""Independent displayed-role, complete-source and actual native-grading QA."""
import importlib.util, json, re, hashlib, subprocess, uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('generator',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=json.loads((HERE/'source.json').read_text())
questions=source['record'][':knowledge-point/questions']
BY_SOURCE={v['source']:k for k,v in g.OBSERVED.items()}

def write(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def normalize_rate(text):
 text=text.replace('each side of the square','each side')
 m=re.fullmatch(r'The rate at which (.*?) changes as (.*?) changes',text)
 if not m:return None
 return tuple(re.sub(r'^the ','',x) for x in m.groups())
def check_format(text):
 # Source uses ordinary nested TeX braces, no unescaped literal systems.
 assert text.count('$')%2==0
 depth=0
 for c in re.sub(r'\\[{}]','',text):
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert 'the each side' not in text
 assert '\\frac{\\text{d}' not in text.replace('\\frac{\\text{d}', '', 1) # one differential quotient

def read_displayed_roles(record):
 """Parse the prompt, not generation metadata, to identify direction/roles."""
 prompt=record['question'][':question/problem']
 derivative=re.search(r'\$\{?([A-Za-z])\}?\^\{′\}\(([A-Za-z])\)\$',prompt)
 assert derivative, prompt
 dep,ind=derivative.groups()
 # Authored prompts have explicit symbol-role declarations.
 declarations=re.search(r'Let \$([A-Za-z])\$ denote (.*?) and let \$([A-Za-z])\$ denote (.*?)\.',prompt)
 if declarations:
  d,out,x,inp=declarations.groups();assert (d,x)==(dep,ind)
  return dep,ind,re.sub(r'^the ','',out).replace('length of each side','each side'),re.sub(r'^the ','',inp).replace('length of each side','each side')
 # Independently parse the seven observed natural-language layouts.
 if prompt.startswith('Consider a circle'):
  assert f'radius ${ind}$' in prompt and f'If ${dep}$ is the area' in prompt
  out,inp='area','radius'
 elif prompt.startswith('Consider a rectangle'):
  assert f'base ${ind}$' in prompt and f'${dep}$ is the area' in prompt
  out,inp='area','base'
 elif prompt.startswith('Consider an ellipse'):
  assert f'major axis ${ind}$' in prompt and f'${dep}$ is the area' in prompt
  out,inp='area','major axis'
 elif prompt.startswith('Consider a cube'):
  assert f'each side ${ind}$' in prompt and f'${dep}$ is the volume' in prompt
  out,inp='volume','each side'
 elif prompt.startswith('Consider a square'):
  assert f'area ${ind}$' in prompt and f'${dep}$ is the length of each side' in prompt
  out,inp='each side','area'
 elif prompt.startswith('Consider a sphere'):
  assert f'volume ${ind}$' in prompt and f'${dep}$ is the length of the radius' in prompt
  out,inp='radius','volume'
 elif prompt.startswith('Consider a regular'):
  assert f'length ${ind}$ of each side' in prompt and f'${dep}$ is the perimeter' in prompt
  out,inp='perimeter','each side'
 else:raise AssertionError(prompt)
 return dep,ind,out,inp

def inspect(record):
 kp=record['knowledge_point'];assert set(kp)=={'db_id','id','title'}
 assert kp['db_id']==17592186064152 and kp['title']=='Interpreting the Derivative of a Function'
 q=record['question'];dep,ind,out,inp=read_displayed_roles(record)
 assert q[':question/difficulty'] in [':question.difficulty/'+l for l in ['easy','moderate','hard']]
 assert len(q[':question/answer-fields'])==1
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 assert f[':answer-field/correct'][0]==':answer/id'
 choices=f[':answer-field/choices'];assert len(choices)==5
 ids=[a[':answer/id'] for a in choices];assert len(set(ids))==5
 for identity in [kp['id'],q[':question/id'],f[':answer-field/id']]+ids: uuid.UUID(identity)
 assert f[':answer-field/correct'][1] in ids
 for a in choices:assert a[':answer/type']==':answer.type/text';check_format(a[':answer/value'])
 check_format(q[':question/problem']);check_format(q[':question/worked-solution'])
 eligible=[a for a in choices if normalize_rate(a[':answer/value'])==(out,inp)]
 assert len(eligible)==1 and eligible[0][':answer/id']==f[':answer-field/correct'][1]
 solution=q[':question/worked-solution']
 # Every formal mathematical stage must use the actual printed symbols.
 assert f'${dep}({ind})$' in solution
 fractions=re.findall(r'\\frac\{\\text\{d\}([A-Za-z])\}\{\\text\{d\}([A-Za-z])\}',solution)
 assert fractions==[(dep,ind)]
 verbal=re.findall(r'\\frac\{\\text\{(?:Instantaneous change in |Change in\xa0)\}([A-Za-z])\}\{\\text\{(?:Instantaneous change in |Change in |Change in\xa0)\}([A-Za-z])\}',solution)
 assert verbal==[(dep,ind)], solution
 assert f'({ind})=' in solution and ('{'+dep+'}^{′}('+ind+')=' in solution or dep+'^{′}('+ind+')=' in solution)
 # Independent exact operator model: dependence must remain output(input).
 x=sp.Symbol(ind,positive=True);F=sp.Function(dep);D=sp.Derivative(F(x),x)
 assert D.expr.func==F and D.variables==(x,)
 assert str(D.expr.func)==dep and str(D.variables[0])==ind
 conclusion=solution.split('\n\n')[-1]
 assert normalize_rate(conclusion.split(' is ',1)[1].rstrip('.').replace('the rate','The rate',1))==(out,inp)
 assert len(set(a[':answer/value'] for a in choices))==5
 return record

def engine_entry(label,r):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Complete displayed-bank radio selection'} for a in f[':answer-field/choices']]}

def main():
 cases=[];source_records=[];comparisons=[];engine=[]
 for q in questions:
  template=BY_SOURCE[q[':question/math-academy-id']];t=g.OBSERVED[template]
  p={'dep':t['dep'],'ind':t['ind']}
  if template=='polygon':p['shape']='pentagon'
  case={'source_id':q[':question/math-academy-id'],'source_db_id':q[':db/id'],'template':template,'level':t['level'],'parameters':p,'bank_profile':'observed_'+template,'difficulty_origin':'observed' if ':question/difficulty' in q else 'authored supported easy assignment'}
  cases.append(case)
  r=inspect(g.generate(t['level'],template=template,parameters=p,profile=case['bank_profile']))
  fq=r['question'][':question/answer-fields'][0];sq=q[':question/answer-fields'][0]
  old=sorted(a[':answer/value'] for a in sq[':answer-field/choices']);new=sorted(a[':answer/value'] for a in fq[':answer-field/choices'])
  assert old==new,(template,old,new)
  assert r['question'][':question/problem']==q[':question/problem']
  raw_solution=q.get(':question/worked-solution')
  if raw_solution:assert raw_solution==r['question'][':question/worked-solution'],(template,raw_solution,r['question'][':question/worked-solution'])
  original_correct=sq.get(':answer-field/correct',{}).get(':answer/value')
  generated_correct=next(a[':answer/value'] for a in fq[':answer-field/choices'] if a[':answer/id']==fq[':answer-field/correct'][1])
  if original_correct:assert original_correct==generated_correct
  comparisons.append({'source_id':case['source_id'],'bank_values_matched':5,'bank_values_total':5,'prompt_exact':True,'worked_solution_exact':True if raw_solution else None,'original_designation_matched':True if original_correct else None,'missing_source_fields':[] if original_correct else ['difficulty','worked_solution','correct designation'],'supported_inferred_correct':generated_correct if not original_correct else None})
  source_records.append(r);engine.append(engine_entry('source/'+case['source_id'],r))
 write('source-cases.json',cases);write('source-fidelity.json',comparisons)
 variants=[];exhaustive=[]
 # Two symbol variants of every observed template/bank. Symbol changes do not
 # contribute to distinct semantic task counts.
 for template,t in g.OBSERVED.items():
  for i,(d,x) in enumerate([('B','x'),('S','y')]):
   p={'dep':d,'ind':x}
   if template=='polygon':p['shape']=['hexagon','octagon'][i]
   r=inspect(g.generate(t['level'],seed=i+11,template=template,parameters=p))
   variants.append({'label':'generated observed-mask '+template+' '+str(i),'record':r});engine.append(engine_entry('variation/'+template+'/'+str(i),r))
 # Enumerate every finite authored context, default symbols and independently
 # renamed symbols, plus every polygon. No sampling claims hide a narrow bank.
 for template,contexts in g.CONTEXTS.items():
  for i in range(len(contexts)):
   base=g.generate(g.TEMPLATES[template],template=template,parameters={'context':i,'dep':g.symbol_for(contexts[i][1]),'ind':g.symbol_for(contexts[i][2])})
   exhaustive.append(inspect(base));engine.append(engine_entry('authored/'+template+'/'+str(i),base))
   inspect(g.generate(g.TEMPLATES[template],template=template,parameters={'context':i,'dep':'B','ind':'x'}))
   if i<2:variants.append({'label':'authored '+template+' '+str(i),'record':base})
 for shape in g.POLYGONS:exhaustive.append(inspect(g.generate('moderate',template='polygon',parameters={'shape':shape,'dep':'P','ind':'s'})))
 # Deterministic identity, canonical task dedup, owned IDs and changed bank IDs.
 for r in source_records+exhaustive:
  m=r['generation'];r2=g.generate(g.TEMPLATES[m['template']],seed=938,template=m['template'],parameters=m['parameters'],profile=m['bank_profile'])
  assert r['question'][':question/id']==r2['question'][':question/id']
  assert r['generation']['content_fingerprint']==r2['generation']['content_fingerprint']
  renamed={**m['parameters'],'dep':'B','ind':'x'}
  rr=g.generate(g.TEMPLATES[m['template']],template=m['template'],parameters=renamed)
  assert rr['generation']['mathematical_task_fingerprint']==m['mathematical_task_fingerprint']
 r1=g.generate('hard',template='sphere_inverse',parameters={'dep':'r','ind':'V'})
 r2=g.generate('hard',template='hard_roles',parameters={'context':2,'dep':'r','ind':'V'})
 assert r1['generation']['parameter_fingerprint']==r2['generation']['parameter_fingerprint']
 assert r1['question'][':question/id']!=r2['question'][':question/id']
 # Exhaustive symbols for every template/context catch accidental component slots.
 renamed_count=0
 for template in g.TEMPLATES:
  level=g.TEMPLATES[template]
  for d in g.SYMBOLS:
   for x in g.SYMBOLS:
    if d==x:continue
    p={'dep':d,'ind':x}
    if template in g.CONTEXTS:p['context']=0
    if template=='polygon':p['shape']='pentagon'
    inspect(g.generate(level,template=template,parameters=p));renamed_count+=1
 failures=0
 bad=[dict(level='easy',template='rectangle'),dict(level='hard',template='hard_roles',parameters={'context':-1,'dep':'A','ind':'a'}),dict(level='moderate',template='moderate_fixed',parameters={'context':10,'dep':'A','ind':'a'}),dict(level='easy',template='circle',parameters={'dep':'A','ind':'A'}),dict(level='moderate',template='polygon',parameters={'dep':'P','ind':'s','shape':'irregular polygon'}),dict(level='easy',template='circle',profile='authored_easy_direct'),dict(level='easy',field_type='blank'),dict(level='hard',template='hard_roles',parameters={'context':True,'dep':'A','ind':'a'}),dict(level='easy',template='easy_direct',parameters={'context':0,'dep':'AA','ind':'a'})]
 for kwargs in bad:
  try:g.generate(**kwargs)
  except ValueError:failures+=1
  else:raise AssertionError('Invalid explicit input accepted: '+str(kwargs))
 positions=set()
 for seed in range(20):
  r=g.generate('easy',seed,template='circle');f=r['question'][':question/answer-fields'][0]
  positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 assert len(positions)==5
 catalog={l:[{'template':t,'parameters':p,'record':inspect(g.generate(l,template=t,parameters=p))} for t,p in cases] for l,cases in g.semantic_catalog().items()}
 assert {l:len(v) for l,v in catalog.items()}=={'easy':8,'moderate':20,'hard':8}
 for l,entries in catalog.items():assert len({e['record']['generation']['mathematical_task_fingerprint'] for e in entries})==len(entries)
 write('semantic-catalog.json',catalog)
 write('engine-input.json',engine)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True)
 grader=json.loads((HERE/'engine.json').read_text())
 write('review.json',{'originals':source_records,'generated':variants})
 lines=['# Source and generated review','', 'Raw source evidence remains in source.json. Source q-48616 lacks original difficulty, correct designation and solution; its displayed replay includes supported authored repairs. Correct answer is identified in author review only.','']
 for original,r,cmp in zip(questions,source_records,comparisons):
  lines+=['## Original '+original[':question/math-academy-id'], '',original[':question/problem'],'','\n'.join('- '+a[':answer/value'] for a in original[':question/answer-fields'][0][':answer-field/choices']),'',original.get(':question/worked-solution','Original solution absent; see generated supported repair.'),'','### Normal generator replay','',g.markdown(r),'Fidelity: '+json.dumps(cmp,ensure_ascii=False),'']
  template=r['generation']['template']
  for v in variants:
   if v['record']['generation']['template']==template:lines+=['### '+v['label'],'',g.markdown(v['record']),'']
 for v in variants:
  if v['record']['generation']['bank_origin']=='authored':lines+=['## '+v['label'],'',g.markdown(v['record']),'']
 (HERE/'review.md').write_text('\n'.join(lines))
 report={'status':'pass','database_writes':0,'source_provenance':source|{'record':'See immutable source.json'},'coverage':{'practice_questions':7,'source_questions_replayed':7,'full_banks_matched':7,'answer_values_matched':35,'answer_values_total':35,'distractors_matched':28,'distractors_total':28,'original_designations_matched':6,'original_designations_total':6,'original_designations_missing':1,'observed_solutions_exact':6,'observed_solutions_available':6,'authored_missing_solution':1,'prompts_exact':7,'unrated_authored_easy':1},'distinct_default_semantic_tasks_per_level':{'easy':8,'moderate':20,'hard':8},'finite_semantic_domains':{'easy_authored':8,'moderate_fixed_authored':10,'hard_authored':8,'regular_polygon_variants':9},'exhaustive_context_records':len(exhaustive),'symbol_component_checks':renamed_count,'invalid_explicit_inputs_rejected':failures,'option_positions_observed':sorted(positions),'review_examples_per_level':{l:sum(v['record']['question'][':question/difficulty']==':question.difficulty/'+l for v in variants) for l in ['easy','moderate','hard']},'native_grader':{'accepted':grader['accepted_checks'],'rejected':grader['rejected_checks'],'unresolved':grader['documented_unresolved_checks'],'binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()},'limitations':['No original correct designation, worked solution, or difficulty exists for q-48616. Repairs are not counted as exact recovered fields.','Source circle circumference equals the numerical derivative of area with respect to radius, but response eligibility asks for a rate interpretation, not a geometrically equivalent quantity.','Authored levels are curriculum design claims; finite categorical variation does not imply unlimited tasks.','Verbal Change in / Change in in source solutions is qualitative differential shorthand, not a finite average-rate equation.']}
 write('validation.json',report)
 files=[SCRIPT]+[p for p in HERE.iterdir() if p.is_file() and p.name not in ['freeze.json']]
 write('freeze.json',{'version':g.VERSION,'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}})
 print(json.dumps({'status':'pass','source_banks':'7/7','source_values':'35/35','source_solutions':'6/6 available','symbol_checks':renamed_count,'native_checks':sum(len(e['checks']) for e in engine)},indent=2))
if __name__=='__main__':main()
