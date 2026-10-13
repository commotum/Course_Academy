#!/usr/bin/env python3
"""Independent QA reads displayed vector definitions, operation, rows and choices.
Run from repository root: .venv/bin/python generate/scratch/17592186059713/validate.py
Writes evidence only in this folder; real native grader uses memory fixtures.
"""
import copy, hashlib, importlib.util, importlib.metadata, json, os, re, subprocess, sys
from pathlib import Path
from collections import Counter
import sympy as sp
D=Path(__file__).resolve().parent;REPO=D.parents[2]
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,data): (D/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def normalize(text):
 text=re.sub(r'\\overset\{\\to \}\{([uUvVwW])\}',r'\1',text)
 text=re.sub(r'([uvwUVW])\^\(→\)',r'\1',text)
 return text.replace(r'\cdot','*').replace('−','-')
def evaluate(text,env):
 text=normalize(text).strip().replace('&','')
 text=re.sub(r'⟨([^,⟩]+),([^⟩]+)⟩',lambda m:'Matrix(['+m[1]+','+m[2]+'])',text)
 text=re.sub(r'(\d)([uvwUVW])',r'\1*\2',text)
 return sp.sympify(text,locals={'Matrix':sp.Matrix,**env})
def read_prompt(q):
 prompt=q[':question/problem'];fragments=re.findall(r'\$([^$]+)\$',prompt);env={}
 for f in fragments[:-1]:
  left,right=normalize(f).split('=',1)
  assert left.strip() in ('u','v','w','U','V','W'),left
  env[left.strip()]=evaluate(right,{})
 assert fragments[-1].rstrip().endswith('=')
 request=normalize(fragments[-1]).strip()[:-1].strip()
 return env,request,evaluate(request,env)
def check_format(s):
 assert s.count('$')%2==0,'math delimiter'
 depth=0
 for char in s:
  if char=='{':depth+=1
  if char=='}':depth-=1
  assert depth>=0,'brace'
 assert depth==0,'brace'
 assert not re.search(r'(?<!\\)\\(?!\\|[A-Za-z ])',s),'unexpected single slash'
 assert '--' not in s and '+-' not in s,'bare signed operation'
def rows(q):
 solution=q.get(':question/worked-solution')
 if solution is None:return []
 match=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert match
 return [s.strip() for s in match[1].split('\\\\')]
def independent_bank(r,env,request,z):
 t=r['generation']['template'];profile=r['generation']['profile']; letters=('U','V') if t=='sum_upper' else ('u','v');a=env.get(letters[0],env.get('v'));b=env.get(letters[1],sp.zeros(2,1))
 if t.startswith('sum'):return [z,a-b,b-a,sp.Matrix([a[0]+b[0],a[1]-b[1]]),sp.Matrix([a[0]-b[0],a[1]+b[1]])]
 if t=='subtract' and profile=='raw-q-1323':return [z,sp.Matrix([a[0],b[1]]),sp.Matrix([-z[0],a[1]+b[1]]),sp.Matrix([z[0],-z[1]]),sp.Matrix([b[0],a[0]-b[0]])]
 if t=='subtract':return [z,a+b,b-a,sp.Matrix([a[0]-b[0],a[1]+b[1]]),sp.Matrix([a[0]+b[0],a[1]-b[1]])]
 if t=='scalar':
  a=env['v'];n=int(re.match(r'(-?\d+)v',request)[1]);return [z,-z,a+sp.ones(2,1)*n,sp.Matrix([-z[0],z[1]]),-a-sp.ones(2,1)*n]
 if t=='linear_combination':
  m=re.fullmatch(r'(\d+)u([+-])(\d+)v',request);assert m;n,q,s=int(m[1]),int(m[3]),1 if m[2]=='+' else -1
  return [z,n*a-s*q*b,a+s*q*b,n*a+s*b,sp.Matrix([n*a[0]+s*q*b[0],a[1]+s*b[1]])]
 m=re.fullmatch(r'(\d+)u-\((\d+)v([+-])(\d+)w\)',request);assert m;n,q,s,c=int(m[1]),int(m[2]),1 if m[3]=='+' else -1,int(m[4]);w=env['w']
 return [z,n*a-q*b+s*c*w,n*a+q*b+s*c*w,a-(q*b+s*c*w),n*a-(b+s*w)]
def check_record(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];env,request,z=read_prompt(q);check_format(q[':question/problem'])
 rs=rows(q)
 if rs:
  check_format(q[':question/worked-solution']);assert q[':question/worked-solution'].startswith(g.OPENING)
  expected_count=6 if r['generation']['template']=='nested_combination' else 4 if r['generation']['template']=='linear_combination' else 3
  assert len(rs)==expected_count,('stage count',rs)
  left=rs[0].split('=',1)[0].replace('&','').strip();assert evaluate(left,env)==z,'solution formal operation'
  for row in rs:
   value=evaluate(row.split('=',1)[1],env);assert value==z,('solution stage',row,value,z)
  assert re.fullmatch(r'\s*&?\s*=\s*⟨\s*-?\d+\s*,\s*-?\d+\s*⟩',rs[-1]),'collected conclusion'
  t=r['generation']['template']
  if t=='scalar': assert rs[1].count(r'\cdot')==2,'two distributed products'
  if t=='linear_combination': assert rs[1].count(r'\cdot')==4 and rs[2].count(r'\cdot')==0,'four distributed products then evaluation'
  if t=='nested_combination':
   assert rs[1].count(r'\cdot')==6,'six distributed products'
   assert len(re.findall('⟨',rs[2]))==3 and len(re.findall('⟨',rs[3]))==2,'individually evaluated vectors before inner reduction'
   assert rs[4].count('⟨')==1 and rs[4].count('-')>=2,'component subtraction before collection'
  # Verify each substituted/evaluated vector independently: correlated errors must fail.
  def vector_nodes(row): return [evaluate(v,{}) for v in re.findall(r'⟨[^⟩]+⟩',row)]
  def component_operands(row,first,second,sign):
   pair=re.search(r'⟨([^,]+),([^⟩]+)⟩',row);assert pair
   for i,part in enumerate(pair.groups()):
    token=re.fullmatch(r'\s*(-?\d+)\s*([+-])\s*(\(?-?\d+\)?)\s*',part);assert token,('component operand structure',part)
    assert int(token[1])==int(first[i]) and int(token[3].strip('()'))==int(second[i]) and token[2]==sign,('individual evaluated operands',part,first,second,sign)
  initial=vector_nodes(rs[0])
  if t.startswith('sum') or t=='subtract':
   a,b=(env['U'],env['V']) if t=='sum_upper' else (env['u'],env['v'])
   assert initial==[a,b],'individual substituted vectors'
   component_operands(rs[1],a,b,'+' if t.startswith('sum') else '-')
  elif t=='scalar':
   assert initial==[env['v']],'individual substituted scalar vector'
  elif t=='linear_combination':
   m=re.fullmatch(r'(\d+)u([+-])(\d+)v',request)
   assert initial==[env['u'],env['v']],'individual substituted linear vectors'
   component_operands(rs[2],int(m[1])*env['u'],int(m[3])*env['v'],m[2])
  else:
   m=re.fullmatch(r'(\d+)u-\((\d+)v([+-])(\d+)w\)',request)
   p,qq,c=int(m[1]),int(m[2]),int(m[4]);sgn=1 if m[3]=='+' else -1
   assert initial==[env['u'],env['v'],env['w']],'individual substituted nested vectors'
   assert vector_nodes(rs[2])==[p*env['u'],qq*env['v'],c*env['w']],'individual evaluated vector terms'
   inner=qq*env['v']+sgn*c*env['w']
   assert vector_nodes(rs[3])==[p*env['u'],inner],'individual inner reduction'
   component_operands(rs[4],p*env['u'],inner,'-')

  # Individually distributed/evaluated terms are read and checked, not only final vectors.
  # At product rows compare complete component token trees to prompt-derived product values.
  if t in ('scalar','linear_combination','nested_combination'):
   productrow=rs[1]
   observed=[(int(a) if t=='scalar' else abs(int(a)))*int(b) for a,b in re.findall(r'(\(?-?\d+\)?)\\cdot\s*(\(?-?\d+\)?)',productrow) for a,b in [(a.strip('()'),b.strip('()'))]]
   if t=='scalar':n=int(re.match(r'(-?\d+)v',request)[1]);expected=[n*int(x) for x in env['v']]
   elif t=='linear_combination':
    m=re.fullmatch(r'(\d+)u([+-])(\d+)v',request);expected=[int(m[1])*int(env['u'][0]),int(m[3])*int(env['v'][0]),int(m[1])*int(env['u'][1]),int(m[3])*int(env['v'][1])]
   else:
    m=re.fullmatch(r'(\d+)u-\((\d+)v([+-])(\d+)w\)',request);expected=[int(m[k])*int(env[v][i]) for i in range(2) for k,v in [(1,'u'),(2,'v'),(4,'w')]]
   assert observed==expected,('individual component products',observed,expected)
 fields=q.get(':question/answer-fields',[])
 for f in fields:
  assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
  values=[evaluate(a[':answer/value'],{}) for a in f[':answer-field/choices']]
  assert len(values)==5 and len({tuple(v) for v in values})==5,'bank collisions'
  assert Counter(tuple(v) for v in values)==Counter(tuple(v) for v in independent_bank(r,env,request,z)),'complete displayed operation bank'
  assert sum(v==z for v in values)==1,'unique correct value'
  if ':answer-field/correct' in f:
   correct=f[':answer-field/correct'];assert correct[0]==':answer/id'
   a=next(x for x in f[':answer-field/choices'] if x[':answer/id']==correct[1]);assert evaluate(a[':answer/value'],{})==z
  assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
  for a in f[':answer-field/choices']:check_format(a[':answer/value'])
 return len(rs)
def fidelity(r,source):
 q=r['question'];assert set(q)==set(source),'raw question key-presence parity'
 for key in (':question/problem',':question/worked-solution'):
  assert q.get(key)==source.get(key),(key,q.get(key),source.get(key))
 assert q.get(':question/difficulty')==(source.get(':question/difficulty') or {}).get(':db/ident')
 for f,sf in zip(q.get(':question/answer-fields',[]),source.get(':question/answer-fields',[])):
  assert set(f)==set(sf),'raw field presence parity'
  assert f[':answer-field/key']==sf[':answer-field/key']
  assert f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  vals=sorted(a[':answer/value'] for a in f[':answer-field/choices']);sv=sorted(a[':answer/value'] for a in sf[':answer-field/choices']);assert vals==sv
  for a in f[':answer-field/choices']:
   sa=next(sa for sa in sf[':answer-field/choices'] if a[':answer/value']==sa[':answer/value']);assert set(a)==set(sa),'raw answer presence parity'
   assert a[':answer/type']==sa[':answer/type'][':db/ident']

cases=[{'source_id':sid,'template':g.SOURCE_TEMPLATE[sid],'parameters':p,'bank_profile':'raw-'+sid,'level':'easy','level_assignment':'observed easy' if ':question/difficulty' in g.QS[sid] else 'authored single-operation easy; raw difficulty remains absent'} for sid,p in g.SOURCE_PARAMS.items()]
write('source-cases.json',cases)
raws=[];completed=[]
for case in cases:
 r=g.generate('easy',template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);check_record(r);fidelity(r,g.QS[case['source_id']]);raws.append(r)
 n=g.generate('easy',template=case['template'],parameters=case['parameters']);check_record(n);completed.append(n)
write('raw-replay.json',raws)
records=[];counts=Counter();stages=0;tasks={level:set() for level in ('easy','moderate','hard')}
for t,level in g.TEMPLATES.items():
 for seed in range(200):
  r=g.generate(level,seed,template=t);stages+=check_record(r);counts[t]+=1;tasks[level].add(r['generation']['mathematical_fingerprint']);records.append(r)
  other=g.generate(level,seed+1,template=t,parameters=r['generation']['parameters'],profile=r['generation']['profile'])
  assert other['question'][':question/id']==r['question'][':question/id'],'seed must not affect identity'
  assert other['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
assert set(g.generate('easy',s)['generation']['template'] for s in range(200))==set(t for t,l in g.TEMPLATES.items() if l=='easy'),'default family coverage'
# Explicit boundaries and failed whole banks; no silently resampled parameters.
invalid=[('moderate','linear_combination',{'a':[1,1],'b':[1,2],'p':1,'q':2,'s':1}),('moderate','linear_combination',{'a':[0,1],'b':[1,2],'p':2,'q':2,'s':1}),('hard','nested_combination',{'a':[1,1],'b':[1,2],'c':[2,3],'p':5,'q':2,'r':2,'s':1}),('easy','sum_lower',{'a':[0,0],'b':[0,0]}),('easy','scalar',{'a':[1,0],'p':3}),('easy','subtract',{'a':[10,1],'b':[1,1]})]
for l,t,p in invalid:
 try:g.generate(l,template=t,parameters=p)
 except ValueError:pass
 else:raise AssertionError(('invalid accepted',l,t,p))
valid_boundaries=[('easy','scalar',{'a':[-9,8],'p':-6}),('moderate','linear_combination',{'a':[6,-5],'b':[-4,6],'p':6,'q':5,'s':-1}),('hard','nested_combination',{'a':[6,-5],'b':[-4,6],'c':[5,-6],'p':4,'q':3,'r':4,'s':1})]
for l,t,p in valid_boundaries:check_record(g.generate(l,template=t,parameters=p))
# Raw evidence remains public but never enters default sampling.
for sid in ('q-1323','q-1386'):
 for seed in range(50):
  rr=g.generate('easy',seed,template=g.SOURCE_TEMPLATE[sid],profile='raw-'+sid);check_record(rr);assert rr['generation']['evidence_only'] and not rr['generation']['eligible_for_learning']
  assert set(rr['question'])==set(g.QS[sid])
  f=rr['question'][':question/answer-fields'][0];sf=g.QS[sid][':question/answer-fields'][0];assert set(f)==set(sf)
  assert all(set(a)==set(sf[':answer-field/choices'][0]) for a in f[':answer-field/choices'])
# Mutations prove independent reads detect failures in printed stages/choices/definitions.
mutation_base=g.generate('hard',template='nested_combination',parameters={'a':[2,-3],'b':[4,5],'c':[-2,3],'p':2,'q':3,'r':4,'s':-1})
mutations=[]
bad=copy.deepcopy(mutation_base);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('⟨2,-3⟩','⟨3,-3⟩');mutations.append(bad)
bad=copy.deepcopy(mutation_base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('3\\cdot 4-4\\cdot (-2)','3\\cdot 4+4\\cdot (-2)');mutations.append(bad)
bad=copy.deepcopy(mutation_base);f=bad['question'][':question/answer-fields'][0];f[':answer-field/choices'][0][':answer/value']=f[':answer-field/choices'][1][':answer/value'];mutations.append(bad)
bad=copy.deepcopy(mutation_base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('⟨-16,-9⟩','⟨-15,-9⟩');mutations.append(bad)
bad=copy.deepcopy(mutation_base);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('⟨4,-6⟩-(⟨12,15⟩','⟨5,-6⟩-(⟨13,15⟩');mutations.append(bad)
for bad in mutations:
 try:check_record(bad)
 except AssertionError:pass
 else:raise AssertionError('mutation survived independent check')
# Real engine: every displayed choice of 1200 generated + four complete originals.
fixtures=[]
for i,r in enumerate(completed+records):
 f=r['question'][':question/answer-fields'][0]
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'correct choice' if a[':answer/id']==f[':answer-field/correct'][1] else 'displayed wrong choice'} for a in f[':answer-field/choices']]
 fixtures.append({'label':str(i),'record':r,'checks':checks})
write('native-input.json',fixtures)
engine=REPO/'generate/runs/current/check-engine';subprocess.run([str(engine),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
native=json.loads((D/'native-report.json').read_text())
reviews=[]
for t,l in g.TEMPLATES.items():
 for seed in (27,83):reviews.append(g.generate(l,seed,template=t))
# Changed parameters for both observed banks, including raw opaque evidence.
for sid in ('q-1323','q-1386'):
 reviews.append(g.generate('easy',91,template=g.SOURCE_TEMPLATE[sid],profile='raw-'+sid))
write('review.json',reviews)
review=['# Original evidence and generated variants','', 'All raw omissions are intentional. Complete originals below infer fields/correct refs and solutions; no captured designation exists.']
for case,r,n in zip(cases,raws,completed):
 review.extend(['\n## Original '+case['source_id']+' — raw evidence',g.markdown(r),'\n### Completed original — authored assessment repair',g.markdown(n)])
for r in reviews:
 review.extend(['\n## Generated '+r['generation']['level']+' / '+r['generation']['template']+' / '+r['generation']['profile'],g.markdown(r)])
(D/'review.md').write_text('\n'.join(review)+'\n')
result={'status':'pass','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':importlib.metadata.version('matplotlib')},'source_provenance':{k:g.SOURCE[k] for k in ('database','basis','lineage')},'source_fidelity':{'practice_sources':4,'prompt_exact':4,'raw_attribute_presence':4,'complete_banks':{'matched':2,'total':2},'displayed_choices':{'matched':10,'total':10},'captured_correct_designations':{'matched':0,'total':0,'missing':2},'worked_solution_exact':{'matched':2,'total':2,'missing':2},'fieldless_sources':2,'completed_originals':4,'raw_gradeable_records':0},'generated_records':1200,'per_template':dict(counts),'independently_verified_solution_stages':stages,'sampled_unique_mathematical_tasks':{k:len(v) for k,v in tasks.items()},'valid_explicit_boundaries':len(valid_boundaries),'invalid_explicit_rejections':len(invalid),'mutation_rejections':len(mutations),'raw_changed_parameter_checks':100,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'evidence_limits':['Two raw radio records lack captured correct refs and worked solutions. Correct values are independently inferred only in completed originals.','Two raw easy sums are fieldless; authored radio completion uses the observed five-choice layout.','q-1323 complete wrong bank is opaque except final-y sign flip; parameterized evidence-only formulas reproduce all values without claiming author intent.','No observed moderate/hard label; bounds and workload are authored within the lesson method.','Canonical raster is contextual evidence, not a practice template; no assessed generated plot.']}
write('validation.json',result)
print(json.dumps(result,indent=2))
