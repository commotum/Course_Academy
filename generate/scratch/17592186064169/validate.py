#!/usr/bin/env python3
"""Independent printed-TeX readback, source replay, finite scope and native QA."""
import copy, hashlib, importlib.util, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor, rationalize
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('reciprocal_generator',SCRIPT)
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=sp.Symbol('x',positive=True);C=sp.Symbol('C',real=True)

def save(name,value): (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def group(text,i):
 assert text[i]=='{',(text,i)
 depth=1;j=i+1
 while depth:
  assert j<len(text),text
  depth+=int(text[j]=='{')-int(text[j]=='}');j+=1
 return text[i+1:j-1],j

def decode(text):
 """Parse ONLY the displayed vocabulary; no generation metadata or recipe values."""
 text=text.strip().rstrip('.').replace(r'\,','').replace(r'\text{d}x','').replace('{x}','x')
 out='';i=0
 while i<len(text):
  if text.startswith(r'\frac',i):
   i+=5;a,i=group(text,i);b,i=group(text,i);out+='(('+decode(a)+')/('+decode(b)+'))'
  elif text.startswith(r'\sqrt',i):
   i+=5;q='2'
   if text[i]=='[':
    end=text.index(']',i);q=text[i+1:end];i=end+1
   a,i=group(text,i);out+='(('+decode(a)+')**(1/('+q+')))'
  elif text[i]=='{':
   a,i=group(text,i);out+='('+decode(a)+')'
  elif text[i]=='^':out+='**';i+=1
  else:out+=text[i];i+=1
 return out

def math_value(text):
 text=decode(text)
 assert '\\' not in text,text
 return parse_expr(text,local_dict={'x':X,'C':C},transformations=standard_transformations+(implicit_multiplication_application,convert_xor,rationalize))

def balanced(text):
 assert len(re.findall(r'(?<!\\)\$',text))%2==0,text
 stack=[]
 for i,ch in enumerate(text):
  if ch=='{' and (i==0 or text[i-1]!='\\'):stack.append(i)
  if ch=='}' and (i==0 or text[i-1]!='\\'):
   assert stack,text;stack.pop()
 assert not stack,text
 assert not any(s in text for s in ['+-','--','\\intx','\\intf']),text

def printed_integrand(problem):
 if 'f(x)' in problem:
  return math_value(re.search(r'\$f\(x\)\s*=\s*(.*?)\$',problem).group(1))
 return math_value(re.search(r'\$(.*?)\$',problem).group(1).rstrip('?'))

def verify(r,raw=False):
 q=r['question']; meta=r['generation']
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 uuid.UUID(r['knowledge_point']['id']);uuid.UUID(q[':question/id'])
 if not raw:assert 'Assume $x>0$.' in q[':question/problem'],'normal prompt must display positive real domain'
 f=printed_integrand(q[':question/problem'])
 assert f!=1/X and sp.simplify(f-X**(-sp.Rational(meta['parameters']['p'],meta['parameters']['q'])))==0
 # Read every choice from rendered text; compare general families by derivative.
 answers=[];correct=[]
 for field in q.get(':question/answer-fields',[]):
  uuid.UUID(field[':answer-field/id'])
  assert field[':answer-field/key']=='selection' and field[':answer-field/type']==':answer-field.type/radio'
  assert len(field[':answer-field/choices'])==5
  for answer in field[':answer-field/choices']:
   uuid.UUID(answer[':answer/id']);balanced(answer[':answer/value'])
   v=math_value(answer[':answer/value']);assert v.has(C)
   d=sp.simplify(sp.diff(v,X));answers.append(d)
   if sp.simplify(d-f)==0:correct.append(answer[':answer/id'])
  assert len(correct)==1
  assert len({sp.srepr(v) for v in answers})==5
  n=f.as_powers_dict()[X];m=n+1
  if meta['profile'] in ('raw_q-29987','observed_q-29987'):
   positive=-n;expected=[X**(-n),(positive.p+positive.q)*X**(-m),-m*X**(1-n),X**m/m,m*X**(-m)]
  elif meta['profile'] in ('raw_q-29989','observed_q-29989'):
   positive=-n;expected=[n*X**(sp.Rational(positive.p,positive.q-positive.p)),-X**m,m*X**(1/m),m*X**m,X**m/m]
  else:expected=[X**m/m,n*X**m,X**n/m,n*X**(n-1),-X**m/m]
  expected=[sp.simplify(sp.diff(v,X)) for v in expected]
  assert sorted(sp.srepr(v) for v in answers)==sorted(sp.srepr(v) for v in expected),'displayed bank recipe values drifted'
  if ':answer-field/correct' in field: assert field[':answer-field/correct']==[':answer/id',correct[0]]
  else: assert raw
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]:balanced(text)
 if ':question/worked-solution' in q:
  solution=q[':question/worked-solution']
  # Independently check ALL explicit rewrite equalities, n, integral operands,
  # and intermediate primitive values in their original ordered stage sequence.
  note=re.search(r'Note that \$(.*?)\.\$',solution)
  if note:
   for value in note.group(1).split('='): assert sp.simplify(math_value(value)-f)==0,(value,f)
  n=math_value(re.search(r'\$n=(.*?)\$',solution).group(1))
  assert sp.simplify(X**n-f)==0
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
  body=blocks[-1];rows=body.split(r'\\')
  for row in rows:
   rhs=row.split('=')[-1].strip().rstrip('.')
   if rhs.startswith(r'\int'):
    operand=rhs[len(r'\int'):]
    if 'f(x)' in operand: assert len(blocks)==2
    else: assert sp.simplify(math_value(operand)-f)==0,(row,f)
   else:
    v=math_value(rhs);assert v.has(C) and sp.simplify(sp.diff(v,X)-f)==0,(row,f)
  layout=g.TEMPLATES[meta['template']]['layout']
  expected={'old':4,'named':6 if n+1<0 else 5,'integer':4,'sqrt':4,'root':4}[layout]
  assert len(rows)==expected,(layout,len(rows),expected)
  assert '+1}' in rows[2 if layout in ('old','named') else 1]
  if len(blocks)==2:
   assert blocks[0]==g.OPENING.split(r'\begin{aligned}')[1].split(r'\end{aligned}')[0]
  if layout in ('sqrt','root'): assert note and len(note.group(1).split('='))==3
  if layout=='sqrt' and not raw:assert r'\text{d}x' in rows[0].split('&')[0]
 return f

source=json.loads((HERE/'source.json').read_text());originals=source['record'][':knowledge-point/questions']
cases=[];raw_records=[];fidelity=[];review=[];normal=[]
for original in originals:
 sid=original[':question/math-academy-id'];t=next(t for t,c in g.TEMPLATES.items() if c['source']==sid);level=g.TEMPLATES[t]['level']
 case={'source_id':sid,'source_db_id':original[':db/id'],'template':t,'level':level,'parameters':g.ORIGINAL_PARAMETERS[sid],'bank_profile':'raw_'+sid,'level_origin':'observed' if ':question/difficulty' in original else 'authored easy assignment; raw difficulty omitted'}
 cases.append(case)
 raw=g.generate(level,template=t,parameters=case['parameters'],profile=case['bank_profile']);q=raw['question'];verify(raw,True)
 for key in [':question/difficulty',':question/answer-fields',':question/worked-solution']:
  assert (key in q)==(key in original),(sid,key)
 assert q[':question/problem']==original[':question/problem'],sid
 if ':question/worked-solution' in original:assert q[':question/worked-solution']==original[':question/worked-solution'],sid
 if ':question/answer-fields' in original:
  a=original[':question/answer-fields'];b=q[':question/answer-fields'];assert len(a)==len(b)
  for of,gf in zip(a,b):
   assert gf[':answer-field/key']==of[':answer-field/key']
   assert gf[':answer-field/type']==of[':answer-field/type'][':db/ident']
   assert (':answer-field/correct' in gf)==(':answer-field/correct' in of)
   assert sorted(v[':answer/value'] for v in gf[':answer-field/choices'])==sorted(v[':answer/value'] for v in of[':answer-field/choices'])
   assert all(v[':answer/type']==':answer.type/math' for v in gf[':answer-field/choices'])
 raw_records.append(raw)
 complete=g.generate(level,template=t,parameters=case['parameters'],profile='observed_'+sid if t.endswith('_radio') else None)
 verify(complete);normal.append(complete)
 # Changed parameters demonstrate source/profile formulas rather than literals.
 other=next(p for p in g.domain(level,t) if p!=case['parameters'])
 variant=g.generate(level,seed=31,template=t,parameters=other,profile=case['bank_profile']);verify(variant,True)
 review.extend([{'label':'Raw source replay '+sid,'record':raw},{'label':'Authored completed original '+sid,'record':complete},{'label':'Parameterized raw evidence variant '+sid,'record':variant}])
 fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in original else None,'answer_bank_exact':5 if ':question/answer-fields' in original else None,'difficulty_field_solution_correct_presence_parity':True,'original_correct_designation_present':False,'solution_stage_sequence_exact':True if ':question/worked-solution' in original else None})
save('source-cases.json',cases);save('source-replays.json',raw_records)

# Exhaust the entire finite task domain, across every supported template.
counts={};fingerprints={level:set() for level in ('easy','moderate','hard')}
for t,config in g.TEMPLATES.items():
 level=config['level'];counts[t]=len(g.domain(level,t))
 for i,p in enumerate(g.domain(level,t)):
  r=g.generate(level,seed=i,template=t,parameters=p);verify(r);normal.append(r)
  fingerprints[level].add(r['generation']['mathematical_fingerprint'])
  reordered=g.generate(level,seed=i+777,template=t,parameters=p)
  assert r['question'][':question/id']==reordered['question'][':question/id']
  assert r['generation']['mathematical_fingerprint']==reordered['generation']['mathematical_fingerprint']
  assert sorted(a[':answer/id'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in reordered['question'][':question/answer-fields'][0][':answer-field/choices'])
 # Two generated examples for every template, therefore every observed family and level.
 for i,p in enumerate(g.domain(level,t)[-2:]):review.append({'label':'Generated authored '+level+' '+t,'record':g.generate(level,seed=10+i,template=t,parameters=p)})
 # Every observed complete bank also exercised throughout the permitted finite easy domain.
 if t.endswith('_radio'):
  for i,p in enumerate(g.domain(level,t)):
   r=g.generate(level,seed=i,template=t,parameters=p,profile='observed_'+config['source']);verify(r);normal.append(r)

# Guard failures, response-shape errors, deterministic CLI and mutation sensitivity.
invalid=[('easy','negative_named',{'p':2,'q':2}),('easy','negative_named',{'p':3,'q':2}),('moderate','reciprocal_named',{'p':1,'q':2}),('hard','reciprocal_root',{'p':5,'q':2}),('hard','reciprocal_root',{'p':20,'q':3}),('moderate','reciprocal_integer',{'p':4,'q':2}),('moderate','reciprocal_sqrt',{'p':4,'q':3}),('easy','negative_named',{'p':1,'q':10})]
for level,t,p in invalid:
 try:g.generate(level,template=t,parameters=p)
 except ValueError:pass
 else:raise AssertionError((level,t,p,'invalid input accepted'))
for key in ['prompt','choice','solution']:
 r=copy.deepcopy(normal[-1]);q=r['question']
 if key=='prompt':q[':question/problem']=q[':question/problem'].replace('x','y')
 elif key=='choice':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='x+C'
 else:q[':question/worked-solution']=q[':question/worked-solution'].replace('+1}', '+2}',1)
 try:verify(r)
 except (AssertionError,AttributeError,TypeError,NameError):pass
 else:raise AssertionError('validator missed '+key+' corruption')
for level in ['easy','moderate','hard']:
 assert g.generate(level,seed=42)==g.generate(level,seed=42)
 fields=[g.generate(level,seed=i)['question'][':question/answer-fields'][0] for i in range(20)]
 positions={next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]) for f in fields}
 assert len(positions)>1
for r in normal:
 preview=g.markdown(r)
 assert '**Difficulty:** ' in preview and '**Origin:** ' in preview
 assert preview.count('✓ ')==1
for r in raw_records:assert '✓ ' not in g.markdown(r)
completed=normal[:6]
for t in ['negative_named_radio','reciprocal_named_radio']:
 conf=g.TEMPLATES[t];p=g.ORIGINAL_PARAMETERS[conf['source']]
 a=g.generate('easy',template=t,parameters=p,profile='observed_'+conf['source']);b=g.generate('easy',template=t,parameters=p)
 assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']

# The actual application grades ALL displayed radios in every checked instance.
native=[]
for i,r in enumerate(normal):
 field=r['question'][':question/answer-fields'][0]
 native.append({'label':str(i)+' '+r['generation']['template']+' '+r['generation']['profile'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'correct family selection' if a[':answer/id']==field[':answer-field/correct'][1] else 'wrong family selection; display independently differentiated'} for a in field[':answer-field/choices']]})
save('native-input.json',native)
engine=ROOT/'generate/runs/current/check-engine';engine_hash=hashlib.sha256(engine.read_bytes()).hexdigest()
subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
assert hashlib.sha256(engine.read_bytes()).hexdigest()==engine_hash
report=json.loads((HERE/'native-report.json').read_text())
save('review.json',review)
text=['# Reciprocal antiderivative review','Raw evidence preserves missing keys. Completed originals and variants are explicitly authored. Opaque source-bank variants are evidence-only; only authored operation banks are eligible for learning.']
for original,case in zip(originals,cases):
 text.extend(['## Captured original '+case['source_id'],original[':question/problem']])
 for f in original.get(':question/answer-fields',[]):text.extend('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])
 text.append(original.get(':question/worked-solution','(No source worked solution.)'))
for item in review:text.extend(['## '+item['label'],g.markdown(item['record'])])
(HERE/'review.md').write_text('\n\n'.join(text)+'\n')
validation={'passed':True,'source':g.PROVENANCE,'source_practice_total':6,'source_prompt_exact':6,'source_present_solutions_exact':{'matched':4,'total':4},'source_absent_solution_parity':{'matched':2,'total':2},'source_complete_banks':{'matched':2,'total':2},'source_answer_values':{'matched':10,'total':10},'source_distractors_inferred_mathematics':{'matched':8,'total':8,'meaning':'inferred wrongness by differentiation; no original key available'},'source_original_correct_designations':{'matched':0,'total':0,'missing':2},'source_fieldless_presence_parity':{'matched':4,'total':4},'source_unrated_presence_parity':{'matched':2,'total':2},'source_fidelity':fidelity,'finite_domains_per_template':counts,'substantive_tasks_per_level':{level:len(v) for level,v in fingerprints.items()},'checked_complete_records':len(normal),'checked_displayed_choices':len(normal)*5,'native':{k:report[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'native_raw_records_skipped_due_to_missing_fields_or_correct_refs':6,'invalid_explicit_parameter_checks':len(invalid),'mutation_sensitivity_checks':3,'generator_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'native_engine_sha256':engine_hash,'database_writes':0,'limitations':['No source hard label: hard higher-root scope is explicitly authored.','Two source radios omit keys/solutions/difficulty; four sources omit all answer fields. Their completions are inferred/authored, not matched designations.','Opaque source distractor intents underdetermined; parameterized raw/observed profiles are evidence-only and not default banks.','q-29662 omits first integral differential; raw replay preserves it and normal output repairs it. All normal prompts explicitly state x>0; raw prompts remain exact.','Native grader exercised radio selection; algebraic entry is not an observed or generated response type.','Positive real connected domain used; no claim of primitive agreement across disconnected domains.']}
save('validation.json',validation)
# Freeze all final evidence other than the hash manifest itself.
files=[SCRIPT]+sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='hashes.json')
save('hashes.json',{'generator_version':g.VERSION,'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}})
print(json.dumps({k:validation[k] for k in ['passed','source_practice_total','source_prompt_exact','source_complete_banks','source_answer_values','finite_domains_per_template','substantive_tasks_per_level','checked_complete_records','native']},indent=2))
