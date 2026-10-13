#!/usr/bin/env python3
"""Independent printed-math, complete-bank, prose/sequence and native checks."""
import hashlib,importlib.util,itertools,json,pathlib,re,subprocess,sys,uuid
import sympy as s
B=pathlib.Path(__file__).parent
ROOT=B.parents[2]
def module(name,p):
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
m=module('jacobian3',B.with_suffix('.py'));r=module('jacobian3_readback',B/'readback.py')

def scalar(x):return r.scalar(x)
def eq(x,y):return s.trigsimp(s.expand(x-y))==0
def displays(x):return re.findall(r'\$\$(.*?)\$\$',x,re.S)
def prose(x):return re.sub(r'\$\$.*?\$\$','<DISPLAY>',x,flags=re.S)
def matrix(body):
 rows=[z.split('&') for z in body.split(r'\\')]
 assert len(set(map(len,rows)))==1,body
 return s.Matrix([[scalar(cell) for cell in row] for row in rows])
def arrays(x):
 return [matrix(z) for z in re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',x,re.S)]
def determinant_rows(x):
 # Independently substitute each actual displayed matrix's determinant, then
 # parse all cofactor and arithmetic rows from the actual rendered strings.
 def replace(z):return '('+s.sstr(matrix(z[1]).det()).replace('**','^')+')'
 text=re.sub(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',replace,x,flags=re.S)
 text=text.strip()[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
 return [scalar(row.split('& =',1)[1]) for row in text.split(r'\\')]
def derivative_rows(x):
 text=x.strip()[len(r'\begin{aligned}'):-len(r'\end{aligned}')]
 found=re.findall(r'\\frac\{∂([xyz])\}\{∂([uvw])\}\s*&\s*=\s*(.*?)(?=\s*&\s*\\(?:,)?\\?frac|\s*\\\\|$)',text,re.S)
 # More robust split: each pair consists of a derivative and its complete value.
 found=[]
 for row in text.split(r'\\'):
  cells=row.split('&');assert len(cells)==6,(row,cells)
  for k in range(0,6,2):
   label=re.search(r'∂([xyz])\}\{∂([uvw])',cells[k]);assert label,cells[k]
   found.append((label[1],label[2],scalar(cells[k+1].strip().lstrip('=').replace(r'\,',''))))
 assert [(x,y) for x,y,_ in found]==list(itertools.product('xyz','uvw'))
 return s.Matrix(3,3,[z for _,_,z in found])
def coordinates(problem):
 math=displays(problem)[0].strip().rstrip('.')
 if '⟶' in math:
  parts=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',math,re.S)
  assert len(parts)==2 and [x.strip() for x in parts[0].split(r'\\')]==list('uvw')
  return s.Matrix([scalar(z) for z in parts[1].split(r'\\')])
 fields=math.split(r'\, ')
 if len(fields)!=3:fields=math.split(r'\,')
 assert len(fields)==3,fields
 return s.Matrix([scalar(z.split('=',1)[1]) for z in fields])
def braces(text):
 depth=0
 for i,c in enumerate(text):
  if c=='{' and (i==0 or text[i-1]!='\\'):depth+=1
  if c=='}' and (i==0 or text[i-1]!='\\'):depth-=1
  assert depth>=0,text
 assert depth==0,text
 assert text.count('$$')%2==0
 assert re.sub(r'\$\$.*?\$\$','',text,flags=re.S).count('$')%2==0
 assert not re.search(r'\+\s*-|--',text),text

def check(record,identity=True):
 q,g=record['question'],record['generation'];f=q[':question/answer-fields'][0]
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 assert record['knowledge_point']['db_id']==m.KP_ID
 for obj,key in [(q,':question/id'),(f,':answer-field/id')]:uuid.UUID(obj[key])
 assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 assert len(f[':answer-field/choices'])==5
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in f[':answer-field/choices']]:braces(text)
 F=coordinates(q[':question/problem']);J=F.jacobian((r.u,r.v,r.w));D=s.trigsimp(s.expand(J.det()))
 blocks=displays(q[':question/worked-solution']);pi=3 if 'Here, we have' in q[':question/worked-solution'] else 2
 # Formal operator/transform blocks must retain the exact source coordinate convention.
 sid=m.TEMPLATES[g['template']][1] or 'q-39710'
 assert blocks[:2]==displays(m.ORIGINALS[sid][':question/worked-solution'])[:2]
 if pi==3:
  supplied=re.split(r',?\\,\s*(?=[xyz]\(u,v,w\)=)',blocks[2].strip().rstrip('.'))
  for z,correct in zip(supplied,F):assert eq(scalar(z.split('=',1)[1]),correct)
 printed=derivative_rows(blocks[pi]);assert printed.shape==(3,3)
 for x,y in zip(printed,J):assert eq(x,y),(g['template'],x,y)
 determinants=arrays(blocks[-1]);assert len(determinants)>=2
 for x,y in zip(determinants[0],J):assert eq(x,y)
 rows=determinant_rows(blocks[-1])
 for row in rows:assert eq(row,D),(g['template'],row,D)
 expected={'polynomial_column':3,'spherical':6}.get(g['template'],4)
 assert len(rows)==expected,(g['template'],len(rows))
 # Every printed 2x2 minor is precisely the appropriate submatrix of the prompt Jacobian.
 rc={'sparse_trig':('row',0),'sparse_exp':('col',1),'sparse_square':('row',2),'log_product':('col',2),'rotation':('row',2),'polynomial_column':('col',2),'polynomial_mixed':('col',0),'linear_offdiag':('row',0),'symbolic_diagonal':('row',0),'spherical':('row',2)}[g['template']]
 expected_minors=[]
 for n in range(3):
  i,j=(rc[1],n) if rc[0]=='row' else (n,rc[1])
  if J[i,j]!=0:expected_minors.append(J.minor_submatrix(i,j))
 assert len(determinants)-1==len(expected_minors),(g['template'],len(determinants),len(expected_minors))
 for actual,expected in zip(determinants[1:],expected_minors):
  for x,y in zip(actual,expected):assert eq(x,y)
 if g['template']=='spherical':
  assert blocks[-1].count(r'\cos^2 w+\sin^2 w')==2
  assert blocks[-1].count(r'\cos^2 v+\sin^2 v')==1
 choices=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 assert all(not eq(x,y) for i,x in enumerate(choices) for y in choices[i+1:])
 hits=[a[':answer/id'] for a,x in zip(f[':answer-field/choices'],choices) if eq(x,D)]
 assert hits==[f[':answer-field/correct'][1]]
 assert g['parameter_fingerprint']==m.digest([s.srepr(s.expand(z)) for z in J])
 if identity:
  displayed=sorted(a[':answer/value'] for a in f[':answer-field/choices'])
  correct_string=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  content=m.digest([m.VERSION,q[':question/difficulty'].split('/')[-1],q[':question/problem'],q[':question/worked-solution'],displayed,correct_string,'radio','selection'])
  assert g['content_fingerprint']==content and q[':question/id']==m.uid(content)
  assert f[':answer-field/id']==m.uid(content+':selection')
  for z in f[':answer-field/choices']:assert z[':answer/id']==m.uid(f[':answer-field/id']+':'+z[':answer/value'])
  assert g['evidence_only']==g['bank_profile'].endswith('-observed')
  assert g['eligible_for_learning']==(not g['evidence_only'])
 assert 'inverse' not in q[':question/problem'].lower() and 'critical' not in q[':question/problem'].lower()
 return D

def native(record,label):
 f=record['question'][':question/answer-fields'][0]
 return {'label':label,'record':record,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every displayed owned radio option'} for a in f[':answer-field/choices']]}

cases=[];source_results=[];grading=[];reviews=[];review_md=['# Direct 3D Jacobian review','All generated records are labeled. Raw source strings remain in source.json. Source math notation is normalized; prose and ordered teaching stages are retained.']
for name,(level,sid,p) in m.TEMPLATES.items():
 if sid:
  case={'source_id':sid,'template':name,'level':level,'parameters':p,'bank_profile':name+'-observed'};cases.append(case)
  rec=m.generate(level,template=name,parameters=p,profile=case['bank_profile']);check(rec)
  q=m.ORIGINALS[sid];f=q[':question/answer-fields'][0];g=rec['question'][':question/answer-fields'][0]
  generated=[scalar(a[':answer/value']) for a in g[':answer-field/choices']]
  matched=[]
  for a in f[':answer-field/choices']:
   hits=[i for i,z in enumerate(generated) if eq(scalar(a[':answer/value']),z)];assert len(hits)==1;matched.append(hits[0])
  assert len(set(matched))==5
  original_correct=scalar(f[':answer-field/correct'][':answer/value'])
  generated_correct=scalar(next(a[':answer/value'] for a in g[':answer-field/choices'] if a[':answer/id']==g[':answer-field/correct'][1]))
  assert eq(original_correct,generated_correct)
  assert prose(q[':question/problem'])==prose(rec['question'][':question/problem'])
  assert prose(q[':question/worked-solution'])==prose(rec['question'][':question/worked-solution'])
  assert eq(coordinates(q[':question/problem'])[0],coordinates(rec['question'][':question/problem'])[0])
  for x,y in zip(coordinates(q[':question/problem']),coordinates(rec['question'][':question/problem'])):assert eq(x,y)
  ob=displays(q[':question/worked-solution']);gb=displays(rec['question'][':question/worked-solution'])
  assert len(ob)==len(gb)
  assert len(determinant_rows(ob[-1]))==len(determinant_rows(gb[-1]))
  # Full original stages and derivatives independently checked as well.
  original_fixture={'knowledge_point':rec['knowledge_point'],'question':{**rec['question'],':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution']},'generation':rec['generation']}
  check(original_fixture,identity=False)
  source_results.append({'source_id':sid,'choices_matched':5,'wrong_choices_matched':4,'correct_designation_matched':True,'presence_parity':set(k for k in q if k.startswith(':question/') and k not in (':question/id',':question/math-academy-id'))==set(k for k in rec['question'] if k!=':question/id'),'prompt_prose_exact':True,'solution_prose_exact':True,'complete_stage_sequence':True,'raw_prompt_exact':q[':question/problem']==rec['question'][':question/problem'],'raw_solution_exact':q[':question/worked-solution']==rec['question'][':question/worked-solution'],'presentation_normalization':'math notation and grouped signed factors; no mathematical correction'})
  assert source_results[-1]['presence_parity']
  grading.append(native(rec,sid+'-replay'));reviews.append(rec)
  review_md+=['','## Original — '+sid+' ('+level+')',q[':question/problem'],'']
  review_md += ['- $'+a[':answer/value']+'$'+(' **Correct**' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else '') for a in f[':answer-field/choices']]
  review_md+=['','**Original worked solution**','',q[':question/worked-solution'],'',m.markdown(rec)]
  # Also show a changed-parameter public observed-bank replay per observed bank.
  changed=m.generate(level,seed=71,template=name,profile=name+'-observed');check(changed);reviews.append(changed);grading.append(native(changed,sid+'-changed-observed'));review_md+=['',m.markdown(changed)]
 for seed in (17,39):
  rec=m.generate(level,seed=seed,template=name);check(rec);reviews.append(rec);grading.append(native(rec,name+'-method-'+str(seed)));review_md+=['',m.markdown(rec)]

# Sample each complete profile: varying signs, arithmetic and option positions.
sampled=0;unique={};positions=set()
for name,(level,sid,p) in m.TEMPLATES.items():
 fps=set()
 for seed in range(24):
  rec=m.generate(level,seed=seed,template=name);check(rec);sampled+=1;fps.add(rec['generation']['parameter_fingerprint'])
  f=rec['question'][':question/answer-fields'][0];positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
 unique[name]=len(fps);assert len(fps)>=20,(name,len(fps))
assert positions==set(range(5))
# Exercise the explicit observed profiles with changed signs and all coefficient boundaries.
profile_samples=0
for name,(level,sid,p) in m.TEMPLATES.items():
 if not sid:continue
 for seed in range(8):
  rec=m.generate(level,seed=seed,template=name,profile=name+'-observed');check(rec);profile_samples+=1
 for coefficient in (-4,-1,1,4):
  pp={k:coefficient for k in p}
  if 'k' in pp:pp['k']=0
  for profile in (name+'-observed',name+'-method'):
   try:rec=m.generate(level,template=name,parameters=pp,profile=profile)
   except ValueError:continue
   check(rec);profile_samples+=1
# Explicit invalid parameters fail without mutation/resampling.
rejected=0
for name,(level,sid,p) in m.TEMPLATES.items():
 for bad in [dict(p,a=0),dict(p,a=5),dict(p,a=True),dict(p,unknown=1)]:
  try:m.generate(level,template=name,parameters=bad)
  except ValueError:rejected+=1
  else:raise AssertionError(('invalid accepted',name,bad))
 for profile in [name+'-method']+([name+'-observed'] if sid else []):
  rec=m.generate(level,seed=11,template=name,profile=profile);pp=rec['generation']['parameters']
  other=m.generate(level,seed=203,template=name,parameters=pp,profile=profile)
  assert other['question'][':question/id']==rec['question'][':question/id']
  assert other['generation']['content_fingerprint']==rec['generation']['content_fingerprint']
  assert sorted(a[':answer/id'] for a in other['question'][':question/answer-fields'][0][':answer-field/choices'])==sorted(a[':answer/id'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices'])
# Whole bank invalidity: no first-valid replacement; incidental offsets don't
# inflate mathematical identity but do change actual displayed content.
x=m.generate('moderate',template='polynomial_mixed',parameters={'a':1,'b':1,'c':1,'d':1,'k':0})
y=m.generate('moderate',template='polynomial_mixed',parameters={'a':1,'b':1,'c':1,'d':1,'k':3})
assert x['generation']['parameter_fingerprint']==y['generation']['parameter_fingerprint']
assert x['question'][':question/id']!=y['question'][':question/id']
for name in ('sparse_trig','sparse_exp','sparse_square'):
 p=dict(m.TEMPLATES[name][2]);p['a' if name=='sparse_trig' else 'd']=1
 try:m.generate(m.TEMPLATES[name][0],template=name,parameters=p)
 except ValueError:rejected+=1
 else:raise AssertionError('method workload guard bypassed')
# Exact hard domain enumeration without repeating identical bank algebra 512 times.
hardfps={m.digest([s.srepr(z) for z in s.Matrix(m.components('spherical',dict(zip('abc',p)))).jacobian(m.VARS)]) for p in itertools.product([-4,-3,-2,-1,1,2,3,4],repeat=3)}
assert len(hardfps)==512
(B/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
(B/'review.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n')
(B/'review.md').write_text('\n'.join(review_md)+'\n')
(B/'engine-input.json').write_text(json.dumps(grading,ensure_ascii=False,indent=2)+'\n')
engine=ROOT/'generate/runs/current/check-engine'
subprocess.run([str(engine),str(B/'engine-input.json'),str(B/'engine-report.json')],check=True)
engine_report=json.loads((B/'engine-report.json').read_text())
freeze_paths=[B/'README.md',B/'classification.md',B/'template-extraction.md',B/'curriculum-route.json',B/'source-byte-inspection.json',B/'formula-inspection.json',B/'source-cases.json',B/'review.json',B/'review.md',B.with_suffix('.py'),B/'source.json',B/'topic.json',B/'lesson.json',B/'readback.py',B/'validate.py',engine,ROOT/'generate/runs/current/check-engine.rs']
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in freeze_paths}
report={'status':'passed','source':m.SOURCE,'source_questions':9,'source_complete_banks':9,'source_choices_matched':45,'source_wrong_choices_matched':36,'source_correct_designations_matched':9,'source_prose_and_sequence_matches':9,'raw_exact_prompt_count':sum(z['raw_prompt_exact'] for z in source_results),'raw_exact_solution_count':sum(z['raw_solution_exact'] for z in source_results),'mathematical_repairs':0,'source_errors':[],'source_details':source_results,'sampled_printed_math_records':sampled,'additional_profile_boundary_checks':profile_samples,'unique_sampled_tasks_by_template':unique,'authored_hard_domain_tasks':512,'explicit_invalid_rejections':rejected,'correct_positions':sorted(positions),'native_grading':{k:v for k,v in engine_report.items() if k!='records'},'dependency_versions':{'sympy':s.__version__,'python':sys.version},'freeze_hashes':hashes,'limits':['Observed opaque bank profiles are evidence-only. Their expression patterns reproduce values but causal error intent is unresolved.','Hard is an authored level from the introductory spherical computation, not an observed label.','All source math displays use normalized notation; raw exact math typography is not claimed.']}
(B/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('status','source_questions','source_complete_banks','source_choices_matched','sampled_printed_math_records','native_grading')}))
