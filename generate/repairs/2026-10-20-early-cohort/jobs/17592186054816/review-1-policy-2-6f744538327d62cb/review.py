import sys,os,json,pathlib,subprocess,hashlib,shutil,importlib.util,random,re,math,platform
from fractions import Fraction
from collections import Counter,defaultdict
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent; JOB=ROOT.parent; PKG=JOB/'workspace'; REPO=pathlib.Path('/home/jake/Developer/Course_Academy'); PY=REPO/'.venv/bin/python'
sys.path.insert(0,str(PKG));import generator as g
exec((ROOT/'prior-oracle.py').read_text())
# Extend the earlier independent prompt-based oracle for the newly added radio contract.
def sym(key):
 if key in ('None','None of the above'):return None
 base=re.search('[NZQRC]',key)[0]
 return base+('0' if '0' in key else '')+('+' if '+' in key else '-' if '-' in key else '')
def roman(label):return {['I','II','III','IV'].index(s) for s in re.findall(r'\b(?:IV|III|II|I)\b',label)}
def expected(r):
 q=r['question'];vs=target(q);fs=q[':question/answer-fields']
 if str(fs[0][':answer-field/type']).endswith('/radio'):
  keys=re.findall(r'^(?:[1-4]|I|II|III|IV)\.\s*\$(.*?)\$',q[':question/problem'],re.M)
  assert len(keys)==4,(q[':question/id'],keys)
  selected={i for i,k in enumerate(keys) if all(member(v,sym(k)) for v in vs)}
  return [next(a[':answer/value'] for a in fs[0][':answer-field/choices'] if roman(a[':answer/value'])==selected)]
 ordinary=[all(member(v,sym(f[':answer-field/key'])) for v in vs) for f in fs if sym(f[':answer-field/key']) is not None]
 it=iter(ordinary);return [str(not any(ordinary) if sym(f[':answer-field/key']) is None else next(it)).lower() for f in fs]
def validate(r):
 want=expected(r);actual=[truth(f) for f in r['question'][':question/answer-fields']]
 assert actual==want,(actual,want)
 q=r['question'];end=q[':question/worked-solution'].split('\n\n')[-1]
 assert 'leave every box unchecked' not in q[':question/worked-solution']
 if str(q[':question/answer-fields'][0][':answer-field/type']).endswith('/checkbox'):
  chosen=[f[':answer-field/key'] for f,w in zip(q[':question/answer-fields'],want) if w=='true']
  for k in chosen: assert k in end,(k,end)
 else: assert want[0] in end
 return want
batch=load(ROOT/'batch.json')
# Small fresh regression sample, expanded only enough to test all added response-bank choices.
SEED=493127; samples=g.generate(count=90,seed=SEED);save('samples.json',samples)
source=load(JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']
replays=[g.replay_source(i) for i in range(len(source))];save('source-replays.json',replays)
source_result=[]
for r,s in zip(replays,source):
 def bank(q):return [(f[':answer-field/key'],[a[':answer/value'] for a in f[':answer-field/choices']]) for f in q[':question/answer-fields']]
 assert r['generation']['source_id']==s[':question/id']
 assert bank(r['question'])==bank(s)
 assert r['question'][':question/problem']==g.normalize_prose(s[':question/problem'])
 if ':question/worked-solution' in s:assert r['question'][':question/worked-solution']==g.normalize_prose(s[':question/worked-solution'])
 keys=expected(r);assert keys==[truth(f) for f in r['question'][':question/answer-fields']]
 for f,k in zip(s[':question/answer-fields'],keys):
  if ':answer-field/correct' in f:assert truth(f)==k
 source_result.append({'source_id':s[':question/id'],'complete_bank':True,'prompt':True,'solution':'preserved' if ':question/worked-solution' in s else 'independently reconstructed','expected':keys})
save('source-replay-results.json',{'cases':source_result,'canonical':'Canonical e8b7d098-3cda-548e-b1d3-e1f2a87b59b6 has no captured response bank; its negative-integer containment method covered by source index10 and controlled universal cases.'})
# Retained historical failing examples, unchanged explicit mathematical parameters.
spec=importlib.util.spec_from_file_location('legacy',ROOT/'legacy-generator.py');legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
from generator_policy import explicit_none_checkbox
checks=[]
def check(label,old,new):
 results={}
 for name,f in [('baseline',old),('current',new)]:
  try:f();results[name]={'passed':True}
  except Exception as e:results[name]={'passed':False,'error':type(e).__name__+': '+str(e)}
 checks.append({'label':label,**results})
def none_case(module):
 r=explicit_none_checkbox(module.make_record(module.number_instance('root',radicand=0,sign=1),['Z+','Q-','Z-','N']))
 assert expected(r)==['false']*4+['true'];validate(r)
def source_bank(module,index):
 r=module.replay_source(index);s=source[index]
 assert bank(r['question'])==bank(s),'complete captured bank required'
check('explicit None after sqrt(0)',lambda:none_case(legacy),lambda:none_case(g))
for i in [3,6,7,10]:check('complete source bank index '+str(i),lambda i=i:source_bank(legacy,i),lambda i=i:source_bank(g,i))
def decimal(module):assert 'decimal' in module.PROFILES,'terminating decimal absent from production domain'
check('production finite-decimal domain',lambda:decimal(legacy),lambda:decimal(g))
def radios(module):
 rs=module.generate(count=90,seed=SEED)
 assert any(str(r['question'][':question/answer-fields'][0][':answer-field/type']).endswith('/radio') for r in rs),'radio banks absent'
check('production radio banks',lambda:radios(legacy),lambda:radios(g))
assert all(not c['baseline']['passed'] and c['current']['passed'] for c in checks)
save('retained-regression-results.json',{'checks':checks,'baseline_limit':'Author retained legacy constructor checked by actual independent failing examples; prior source bindings unchanged.','prior_seed':827461,'parameters':'root radicand=0 sign=1 candidates=[Z+,Q-,Z-,N]; source bank indices 3,6,7,10'})
# Relevant/irrelevant controlled interventions, including new decimal and radio construction.
pairs=[];pair_specs=[]
def pair(label,a,b,cs,bank='checkbox',same=False):
 rr=[g.make_record(x,cs,bank_profile=bank) for x in [a,b]]
 wants=[validate(r) for r in rr];assert (wants[0]==wants[1])==same
 assert rr[0]['question'][':question/problem']!=rr[1]['question'][':question/problem']
 start=len(pairs);pairs.extend(rr);pair_specs.append({'label':label,'indices':[start,start+1],'kind':'irrelevant' if same else 'relevant','expected':wants,'passed':True,'bank':bank})
root=lambda n:g.number_instance('root',radicand=n,sign=1)
pair('zero boundary with explicit None',root(1),root(0),['Z+','Q-','Z-','N'])
pair('root rationality radio',root(2),root(121),['Q+','R','Q','Z'],'radio-0')
pair('root magnitude radio',root(121),root(144),['Q+','R','Q','Z'],'radio-0',True)
pair('decimal zero and positive fraction',g.number_instance('decimal',value='0.0'),g.number_instance('decimal',value='0.25'),['Z','Q+','Q-','R'],'radio-10')
pair('decimal magnitude preservation',g.number_instance('decimal',value='0.25'),g.number_instance('decimal',value='0.75'),['Z','Q+','Q-','R'],'radio-10',True)
pair('universal target sign',{'profile':'universal','group':'natural numbers'},{'profile':'universal','group':'negative integers'},['Z-','Q+','Z+','Q-'],'radio-10')
save('counterfactual-records.json',pairs);save('counterfactual-results.json',pair_specs)
# Boundary targets covering old classification rules, newly sampled finite decimals and all four bank profiles.
bounds=[]
for n in [0,1,2,144]:
 for sign in [-1,1]:bounds.append(g.make_record(g.number_instance('root',radicand=n,sign=sign),['N','N0','Z0-','Q+']))
for n,d in [(0,2),(1,2),(-1,2),(12,12),(-12,12)]:bounds.append(g.make_record(g.number_instance('fraction',numerator=n,denominator=d),['Z','Q','Q0+','R-']))
for v in ['-1.4142','0.0000','1.4142','12.0000','-12.0000']:
 bounds.append(g.make_record(g.number_instance('decimal',value=v),['N','Q0+','Z0-','R']))
save('boundary-records.json',bounds)
math_results=[];grader=[]
for group,rr in [('samples',samples),('batch',batch),('pairs',pairs),('boundary',bounds),('source',replays)]:
 for i,r in enumerate(rr):
  want=expected(r)
  if group!='source':validate(r)
  else:assert want==[truth(f) for f in r['question'][':question/answer-fields']]
  math_results.append({'group':group,'index':i,'id':r['question'][':question/id'],'expected':want,'passed':True})
  checks=[]
  for j,(f,w) in enumerate(zip(r['question'][':question/answer-fields'],want)):
   for a in f[':answer-field/choices']:
    checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/value']==w else 'rejected','purpose':'Prompt-derived exact membership/subset; includes every plausible authored wrong option.'})
  grader.append({'label':group+'-'+str(i),'record':r,'checks':checks})
save('math-results.json',{'cases':math_results,'failures':[],'oracle':'Independent Fraction/isqrt and complete sign/integrality/rationality witness partition. Reads rendered-content source strings, not generation metadata.'})
save('grader-input.json',grader)
save('delivery-input.json',samples+pairs+bounds+replays)
# Runtime files only relocation, exact dependency contract, invalid inputs, external assets.
manifest=load(PKG/'package.json');rel=ROOT/'relocated';rel.mkdir(exist_ok=True)
for name in manifest['files']:
 assert not pathlib.Path(name).is_absolute() and '..' not in pathlib.Path(name).parts
 dst=rel/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(PKG/name,dst)
version=subprocess.check_output([str(PY),'-c','import platform;print(platform.python_version())'],text=True).strip()
assert manifest['dependencies']=={'python':version,'packages':{}}
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(ROOT/'external-assets')};(ROOT/'external-assets').mkdir(exist_ok=True)
args=['--seed',str(SEED),'--count','90','--format','json'];cmd=[str(PY),str(rel/'generator.py'),*args]
p=subprocess.run(cmd,cwd=rel,env=env,capture_output=True,text=True,check=True)
assert json.loads(p.stdout)==samples==g.generate(count=90,seed=SEED)
invalid=[]
for args in [['--difficulty','hard'],['--count','-1'],['--format','xml'],['--replay-source','11']]:
 p=subprocess.run([str(PY),str(rel/'generator.py'),*args],env=env,capture_output=True,text=True);assert p.returncode!=0;invalid.append({'args':args,'returncode':p.returncode,'stderr':p.stderr[-350:]})
assert g.generate(count=0)==[]
for kw in [{'radicand':-1,'sign':1},{'radicand':1,'sign':0}]:
 try:g.number_instance('root',**kw);raise AssertionError('invalid accepted')
 except ValueError:pass
try:g.number_instance('fraction',numerator=1,denominator=0);raise AssertionError('zero denominator accepted')
except ValueError:pass
assert not list((ROOT/'external-assets').iterdir())
save('packaging-results.json',{'manifest':manifest,'actual_python':version,'deterministic':True,'relocation_command':cmd,'invalid_inputs':invalid,'empty_count':True,'external_output_files':[],'third_party_imports':[],'runtime_files_only':True})
# Current captured bank weakness: independently recheck all five reproduced stored generated records.
sys.path.insert(0,str(REPO));from scripts.generator_publish import content_fingerprint,normalized_question
inventory=load(JOB/'source/inventory.json');byid={q[':question/id']:q for q in inventory['questions']}
oldrecords=load(ROOT/'prior-generated-records.json');affected=[];inspected=[]
for r in oldrecords:
 q=byid[r['question'][':question/id']];assert content_fingerprint(q)==content_fingerprint(r['question'])
 inst=r['generation']['instance'];cs=r['generation']['candidates'];raw=legacy.make_record(inst,cs)
 assert content_fingerprint(raw['question'])==content_fingerprint(q)
 import uuid
 assert str(uuid.uuid5(uuid.UUID(g.KP['id']),'generated-question:'+content_fingerprint(q)))==q[':question/id']
 assert [truth(f) for f in r['question'][':question/answer-fields']]==expected(r)
 bad=not any(truth(f)=='true' for f in r['question'][':question/answer-fields'])
 inspected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'fingerprint_reproduced':True,'missing_nonempty_selection':bad})
 if bad:affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':'Historical generated all-false checkbox bank lacks explicit None and is ineligible under current fresh-practice source rule; current constructor fixes this instance.','reproduction':f'{PY} review.py; legacy explicit parameters '+json.dumps(inst,sort_keys=True)+' candidates '+json.dumps(cs),'evidence_path':'generated-records.json'})
save('generated-records.json',oldrecords);save('affected-inventory.json',{'affected_questions':affected});save('inventory-results.json',{'basis':inventory['basis'],'captured_count':len(inventory['questions']),'generated_reproduced':inspected,'original_source_not_generated':len(source),'limit':'Captured basis only. Historical seeds absent; exact parameter/fingerprint/UUID reproduction verified. Retained bank issue remains in database; no database write authorized.'})
# Representative renderer input: exact batch, all interventions, two source controls and decimal boundary.
save('render-records.json',batch+pairs+[replays[3],replays[6],bounds[-1]])
(ROOT/'session-state.md').write_text('Completed fresh 90-record sample seed493127, exact five batch records, all eleven source banks, eighteen boundaries and six controlled pairs; math and retained independent regressions passed. Legacy failing examples confirmed. Relocation/runtime checked. Historical inventory UUID reproduced. Next: actual delivery/grading/rendering and survivor decision analysis.\n')
print(json.dumps({'source_replays':len(replays),'math_cases':len(math_results),'fresh_sample':len(samples),'retained_regressions':len(checks),'counterfactual_pairs':len(pair_specs),'historical_affected':len(affected),'banks':dict(Counter(r['generation']['bank_profile'] for r in samples))}))
