"""Root checks actual geometry roles and textual derivative response eligibility."""
import importlib.util,json,re
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186064152;D=R.parents[2]/f'generate/scratch/{K}'
sp=importlib.util.spec_from_file_location('root_geometry_derivative',D.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
C=dict(instances=0,values=0,operator_direction_checks=0,source_prompts=0,source_solutions=0,source_banks=0,source_values=0,source_existing_refs=0,source_missing_refs=0)
def rate(text):
 m=re.fullmatch(r'[Tt]he rate at which (.*?) changes as (.*?) changes\.?',text)
 if not m:return None
 return tuple(z.removeprefix('the ').replace('each side of the square','each side') for z in m.groups())
def roles(prompt):
 operator=re.search(r'\$\{?([A-Za-z])\}?\^\{′\}\(([A-Za-z])\)\$',prompt);assert operator,prompt;dep,ind=operator.groups()
 explicit=re.search(r'Let \$([A-Za-z])\$ denote (.*?) and let \$([A-Za-z])\$ denote (.*?)\.',prompt)
 if explicit:
  a,out,b,inp=explicit.groups();assert (a,b)==(dep,ind);out=out.removeprefix('the ').removeprefix('length of ');inp=inp.removeprefix('the ').removeprefix('length of ')
  shape=re.search(r'^Consider (?:a|an) (\w+)\.',prompt)[1]
 else:
  binding=re.search(r'[Ii]f \$'+dep+r'\$ is the (.*?)(?:[?.]|$)',prompt);assert binding,prompt
  raw=binding[1];out='each side' if raw.startswith('length of each side') else 'radius' if raw.startswith('length of the radius') else raw.split()[0]
  shape=re.search(r'^Consider (?:a|an) (?:regular )?(\w+)',prompt)[1]
  first=prompt.split('What is',1)[0].split('If ',1)[0]
  if prompt.startswith('Consider a regular'):inp='each side';assert 'length $'+ind+'$ of each side' in first
  elif shape in ('circle','rectangle','ellipse'):inp={'circle':'radius','rectangle':'base','ellipse':'major axis'}[shape];assert inp+' $'+ind+'$' in first
  elif shape=='cube':inp='each side';assert 'each side $'+ind+'$' in first
  elif shape=='square':inp='area';assert 'area $'+ind+'$' in first
  elif shape=='sphere':inp='volume';assert 'volume $'+ind+'$' in first
  else:inp='each side';assert 'length $'+ind+'$ of each side' in first
 return dep,ind,out,inp,shape
tasks={level:set() for level in ('easy','moderate','hard')}
def check(r):
 q=r['question'];dep,ind,out,inp,shape=roles(q[':question/problem']);f=q[':question/answer-fields'][0];choices=f[':answer-field/choices'];assert len(choices)==5
 eligible=[z for z in choices if rate(z[':answer/value'])==(out,inp)];assert len(eligible)==1 and f[':answer-field/correct']==[':answer/id',eligible[0][':answer/id']],(q[':question/problem'],out,inp,[(z[':answer/value'],rate(z[':answer/value'])) for z in choices])
 # A quantity/value, fixed-input rate or reverse direction is not eligible,
 # regardless of accidental equality with a calculated derivative formula.
 worked=q[':question/worked-solution'];assert f'${dep}({ind})$' in worked
 differentials=re.findall(r'\\frac\{\\text\{d\}([A-Za-z])\}\{\\text\{d\}([A-Za-z])\}',worked);assert differentials==[(dep,ind)]
 verbal=re.findall(r'\\frac\{\\text\{[^{}]*change in[^{}]*\}([A-Za-z])\}\{\\text\{[^{}]*[Cc]hange in[^{}]*\}([A-Za-z])\}',worked,re.I);assert verbal==[(dep,ind)]
 assert rate(worked.rsplit(' is ',1)[1])==(out,inp)
 level=q[':question/difficulty'].split('/')[-1];fixed=None
 if 'is fixed' in q[':question/problem']:
  fixed=next(z for z in ('height','base','radius','major axis','minor axis') if re.search(r'(?:its |the |The )'+z+r' is fixed',q[':question/problem']))
 if r['generation']['bank_origin']=='authored':
  if level=='easy':assert shape in ('circle','sphere') and inp in ('radius','diameter') and out in ('area','circumference','volume','surface area') and fixed is None
  elif level=='moderate':assert shape in ('rectangle','triangle','parallelogram','cylinder','cone') and out in ('area','volume') and fixed!=inp and fixed is not None
  else:assert (inp in ('area','volume') and out in ('radius','diameter','each side')) or (shape=='ellipse' and out=='area' and inp in ('major axis','minor axis') and fixed!=inp)
 tasks[level].add((shape,out,inp,fixed));C['instances']+=1;C['values']+=5;C['operator_direction_checks']+=2;return q
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];q=check(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']));assert q[':question/problem']==old[':question/problem'];C['source_prompts']+=1
 if old.get(':question/worked-solution'):assert q[':question/worked-solution']==old[':question/worked-solution'];C['source_solutions']+=1
 for of,nf in zip(old[':question/answer-fields'],q[':question/answer-fields']):
  assert sorted(z[':answer/value'] for z in of[':answer-field/choices'])==sorted(z[':answer/value'] for z in nf[':answer-field/choices']);C['source_banks']+=1;C['source_values']+=len(of[':answer-field/choices'])
  actual=next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1])
  if of.get(':answer-field/correct'):assert actual==of[':answer-field/correct'][':answer/value'];C['source_existing_refs']+=1
  else:C['source_missing_refs']+=1
review=json.loads((D/'review.json').read_text())
for r in review['generated']:check(r.get('record',r))
for template,contexts in g.CONTEXTS.items():
 for n,context in enumerate(contexts):
  params={'context':n,'dep':'B','ind':'x'};record=g.generate(g.TEMPLATES[template],template=template,parameters=params);check(record)
  original=g.generate(g.TEMPLATES[template],template=template,parameters={'context':n,'dep':g.symbol_for(context[1]),'ind':g.symbol_for(context[2])});assert original['generation']['mathematical_task_fingerprint']==record['generation']['mathematical_task_fingerprint']
for shape in g.POLYGONS:check(g.generate('moderate',template='polygon',parameters={'shape':shape,'dep':'P','ind':'s'}))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
C['finite_semantic_task_counts']={level:len(keys) for level,keys in tasks.items()};C['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(C,indent=2)+'\n');print(C)
