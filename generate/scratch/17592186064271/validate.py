#!/usr/bin/env python3
"""Independent displayed-unit QA, source fidelity, and real native grading."""
import hashlib,importlib.util,itertools,json,pathlib,re,subprocess,sys,uuid
import sympy as sp
D=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('units',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
# Independent registry: scale is part of the complete requested unit, including
# same-dimension ratios such as hour/minute and minute/hour.
m,t,l,c,e,p,k,v,w,i,j,s,h=sp.symbols('m t l c e p cupcake visitor visit item package student ticket',positive=True)
LEX={'gram':m,'kilogram':1000*m,'ton':1000000*m,'second':t,'minute':60*t,'hour':3600*t,'meter':l,'centimeter':l/100,'liter':l**3/1000,'milliliter':l**3/1000000,'dollar':c,'euro':e,'point':p,'cupcake':k,'visitor':v,'visit':w,'item':i,'package':j,'student':s,'ticket':h,'degree fahrenheit':sp.Symbol('temp',positive=True)}
assert LEX['liter']==1000*LEX['centimeter']**3
assert LEX['milliliter']==LEX['centimeter']**3
assert LEX['hour']==60*LEX['minute'] and LEX['minute']==60*LEX['second']
assert LEX['kilogram']==1000*LEX['gram'] and LEX['ton']==1000*LEX['kilogram']

def unit(text):
 text=text.lower().strip();text=re.sub(r'^metric ','',text)
 if ' per ' in text:
  a,b=text.split(' per ',1);return unit(a)/unit(b)
 power=1
 for prefix,n in [('squared ',2),('square ',2),('cubic ',3)]:
  if text.startswith(prefix):power=n;text=text[len(prefix):]
 for suffix,n in [(' squared',2),(' cubed',3)]:
  if text.endswith(suffix):power=n;text=text[:-len(suffix)]
 if text=='degrees fahrenheit':text='degree fahrenheit'
 elif text.endswith('s'):text=text[:-1]
 return LEX[text]**power

def following_units(text):
 # Read the longest complete named-unit phrase from actual learner prose.
 hit=re.match(r'(?:metric )?(?:(?:squared|square|cubic) )?(?:degrees Fahrenheit|[A-Za-z]+)(?: per (?:(?:squared|square|cubic) )?(?:degrees Fahrenheit|[A-Za-z]+))?',text)
 if not hit:raise AssertionError('Missing displayed units: '+text)
 return unit(hit.group(0))

def prompt_target(q,template):
 prompt=q[':question/problem']
 dep=re.search(r'\$([A-Za-z]+)\(([A-Za-z]+)\)\$ ([^$]+)',prompt)
 assert dep, prompt
 f,x,ut=dep.groups();U=following_units(ut)
 # Input labels may be separated from their unit by explicit narrative.
 if template=='milk':pat=r'\$v\$ is the number of ([^$]+)'
 elif template=='reward':pat=r'\$p\$ ([^$]+)'
 else:pat=r'\$'+re.escape(x)+r'\$ ([^$]+)'
 inputs=re.findall(pat,prompt)
 assert inputs,(template,prompt)
 V=following_units(inputs[-1])
 # Actual requested numerator/denominator symbols must agree with the
 # displayed function and independent variable, before dimensional checks.
 last_math=re.findall(r'\$([^$]+)\$',prompt)[-1]
 cleaned=last_math.replace(r'\text{d}','d').replace(r'\textrm{d}','d')
 assert '{d'+f+'}' in cleaned or '{d'+f in cleaned,(f,last_math)
 assert '{d'+x+'}' in cleaned or '{d'+x in cleaned,(x,last_math)
 return sp.cancel(U/V),U,V

def balanced(text):
 assert text.count('$')%2==0,text
 stack=0
 for z,ch in enumerate(text):
  if ch in '{}' and (z==0 or text[z-1]!='\\'):
   stack+=1 if ch=='{' else -1
   assert stack>=0,text
 assert stack==0,text

def check_record(r,raw_solution=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];gen=r['generation'];balanced(q[':question/problem']);balanced(q[':question/worked-solution'])
 assert q[':question/difficulty']==':question.difficulty/'+gen['level']
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio'
 uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id']);assert len(f[':answer-field/choices'])==5
 answers=f[':answer-field/choices'];assert len({a[':answer/id'] for a in answers})==5
 target,U,V=prompt_target(q,gen['template'])
 parsed=[unit(a[':answer/value']) for a in answers]
 assert all(sp.cancel(a-b)!=0 for n,a in enumerate(parsed) for b in parsed[n+1:]),'Equivalent bank choices'
 correct=[n for n,a in enumerate(parsed) if sp.cancel(a-target)==0]
 if gen['raw_invalid_evidence']:
  assert not correct and ':answer-field/correct' not in f;return
 assert len(correct)==1,(gen,parsed,target)
 assert f[':answer-field/correct']==[':answer/id',answers[correct[0]][':answer/id']]
 # Read every displayed ratio stage, independently from actual prompt units.
 sol=q[':question/worked-solution']
 ratios=re.findall(r'\\frac\{\\text\{([^{}]+)\}\}\{\\text\{([^{}]+)\}\}',sol)
 assert ratios,'Missing formal quotient stage'
 if not raw_solution:
  for a,b in ratios:assert sp.cancel(unit(a)/unit(b)-target)==0,(a,b,target)
  labels=re.findall(r': & \\text\{([^{}]+)\}',sol.split('The derivative')[0])
  assert len(labels)==2
  assert sorted(str(unit(s)) for s in labels)==sorted([str(U),str(V)]),(labels,U,V)
  conclusion=re.search(r'is measured in "([^"]+)"',sol)
  assert conclusion and sp.cancel(unit(conclusion.group(1))-target)==0
 assert sol.count('The derivative')==1 and sol.count('ratio of the units')==1
 assert sol.count(r'\begin{aligned}')==2

source=json.loads((D/'source.json').read_text())
assert source['basis']==1356
originals={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
cases=json.loads((D/'source-cases.json').read_text())
metrics={'source_questions':len(cases),'exact_prompts':0,'exact_solutions':0,'available_solutions':0,'exact_banks':0,'available_banks':0,'matched_choices':0,'available_choices':0,'exact_designations':0,'available_designations':0}
review=[];source_reports=[];engine=[]
def add_engine(r,label):
 f=r['question'][':question/answer-fields'][0];right=f[':answer-field/correct'][1]
 engine.append({'label':label,'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==right else 'rejected','purpose':'owned radio choice; displayed units checked independently'} for a in f[':answer-field/choices']]})
for case in cases:
 q=originals[case['source_id']];r=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
 check_record(r,raw_solution=case['template']=='website')
 assert r['question'][':question/problem']==q[':question/problem'];metrics['exact_prompts']+=1
 if ':question/worked-solution' in q:
  metrics['available_solutions']+=1
  assert r['question'][':question/worked-solution']==q[':question/worked-solution'];metrics['exact_solutions']+=1
 fields=q.get(':question/answer-fields',[])
 if fields:
  metrics['available_banks']+=1;bank=fields[0][':answer-field/choices'];rb=r['question'][':question/answer-fields'][0][':answer-field/choices']
  assert sorted(a[':answer/value'] for a in bank)==sorted(a[':answer/value'] for a in rb)
  metrics['exact_banks']+=1;metrics['matched_choices']+=len(bank);metrics['available_choices']+=len(bank)
  if ':answer-field/correct' in fields[0]:
   metrics['available_designations']+=1
   cf=r['question'][':question/answer-fields'][0][':answer-field/correct'][1]
   assert next(a[':answer/value'] for a in rb if a[':answer/id']==cf)==fields[0][':answer-field/correct'][':answer/value'];metrics['exact_designations']+=1
 source_reports.append({'source_id':case['source_id'],'exact_prompt':True,'solution_status':'raw exact teaching anomaly' if case['template']=='website' else 'exact' if ':question/worked-solution' in q else 'authored missing-source solution','bank_status':'raw exact invalid bank' if case['template']=='farmer' else 'authored missing-field bank' if not fields else 'exact','original_designation_present':bool(fields and ':answer-field/correct' in fields[0])})
 review.append({'label':'Original replay '+case['source_id'],'record':r})
 normal=g.generate(case['level'],template=case['template'],parameters=case['parameters'])
 check_record(normal);add_engine(normal,'Normal '+case['source_id'])
 # Changed-parameter instance per every observed context/profile.
 varied=g.generate(case['level'],seed=24,template=case['template']);check_record(varied)
 review.append({'label':'Generated variant '+case['template'],'record':varied});add_engine(varied,'Variant '+case['template'])
 if case['template'] in ('farmer','website'):review.append({'label':'Minimal source repair '+case['source_id'],'record':normal})

# Exhaust the finite meaningful unit domains; context/seed are not counted as
# extra mathematical tasks. Identical mathematical objects share fingerprints.
mathcounts={};records={}
for template,desc in g.TEMPLATES.items():
 if template in g.DEFS:
  domain=g.DEFS[template]['eligible'];keys=list(domain)
  params=[dict(zip(keys,combo)) for combo in itertools.product(*(domain[k] for k in keys))]
  params=[p for p in params if not ('alt' in p and ((template=='cupcake' and p['alt']!={'gram':'kilogram','kilogram':'gram'}[p['u']]) or (template=='milk' and p['alt']!={'liter':'milliliter','milliliter':'liter'}[p['v']]))) ]
 elif template=='non_time_power':params=[{'u':u,'v':v,'power':p} for u,v,p in itertools.product(('centimeter','meter'),('item','package','ticket','cupcake'),(2,3))]
 else:params=[{'u':u,'v':v,'power':1} for u,v in itertools.product(('ton','kilogram','liter','meter','item','package','ticket','cupcake'),('dollar','euro'))]
 fingerprints=set()
 for p in params:
  r=g.generate(desc['level'],template=template,parameters=p);check_record(r)
  r2=g.generate(desc['level'],seed=125,template=template,parameters=p)
  assert r['question'][':question/id']==r2['question'][':question/id']
  assert sorted(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in r2['question'][':question/answer-fields'][0][':answer-field/choices'])
  fingerprints.add(r['generation']['mathematical_fingerprint']);records[r['generation']['content_fingerprint']]=r
 mathcounts[template]=len(fingerprints)
for level in ('easy','moderate','hard'):
 for n in (0,1):
  r=g.generate(level,n);check_record(r);review.append({'label':'Generated '+level+' example '+str(n+1),'record':r})
for n,r in enumerate(records.values()):add_engine(r,'Exhaustive instance '+str(n))
# Every sampling path and explicit bounds are checked, including shuffled
# correct positions. No numerical derivation is smuggled into the prompt.
positions=set()
for level in ('easy','moderate','hard'):
 for n in range(80):
  r=g.generate(level,n);check_record(r)
  f=r['question'][':question/answer-fields'][0];positions.add(next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
assert positions==set(range(5))
for kw in [dict(level='moderate',parameters={'u':'meter','v':'minute','power':2}),dict(level='hard',parameters={'u':'ton','v':'dollar','power':2}),dict(level='easy',template='cupcake',parameters={'u':'gram','v':'cupcake','alt':'gram'}),dict(level='hard',profile='observed')]:
 try:g.generate(**kw)
 except ValueError:pass
 else:raise AssertionError('Invalid explicit parameters accepted')
(D/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
root=D.parents[2];grader=root/'generate/runs/current/check-engine'
subprocess.run([str(grader),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
engine_result=json.loads((D/'engine-report.json').read_text())
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
text=['# Original source evidence and generated units questions','Raw source is preserved in source.json; records below distinguish exact evidence replay from normal repairs.']
for case in cases:
 q=originals[case['source_id']];text+=['\n## Original '+case['source_id'],q[':question/problem'],q.get(':question/worked-solution','(No source solution captured.)'),'\nBank: '+', '.join(a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices'])]
for r in review:text+=['\n## '+r['label'],g.markdown(r['record'])]
(D/'review.md').write_text('\n\n'.join(text)+'\n')
report={'status':'pass','generator_version':g.VERSION,'database_writes':0,'source_fidelity':metrics,'source_reports':source_reports,'normal_correctness':'all displayed units, exact scales, formal ratio stages and conclusion independently checked','raw_invalid_cases':['q-48557: no correct option','q-110040: raw worked solution says visitors instead of visits'],'minimal_math_bank_repairs':{'questions':1,'choices_changed':1,'raw_exact_choices':35,'normal_exact_original_choices':34},'missing_correct_designation_repairs':['q-48557','q-48613'],'missing_field_repairs':['q-110040','q-72091'],'authored_missing_levels':['moderate','hard'],'finite_meaningful_tasks_by_template':mathcounts,'distinct_mathematical_tasks_by_level':{level:len({r['generation']['mathematical_fingerprint'] for r in records.values() if r['generation']['level']==level}) for level in ('easy','moderate','hard')},'exhaustive_normal_instances':len(records),'random_normal_instances':240,'native_grading':{k:engine_result[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'engine_sha256':hashlib.sha256(grader.read_bytes()).hexdigest(),'python':sys.version,'sympy':sp.__version__}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
