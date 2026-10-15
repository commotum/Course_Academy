"""Independent reading of printed prompts, choices and every operative equation.

Does not call production displayed_set/number/choices/solution to establish truth.
Source snapshots and independently authored inventory are separate populations.
"""
import copy,hashlib,importlib.util,json,re,subprocess,sys,platform
from pathlib import Path
import sympy as sp
from functools import lru_cache
D=Path(__file__).resolve().parent;ROOT=D.parents[2];SCRIPT=D.with_suffix('.py')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('closed_interval_draft',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,v):(D/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def clean(s):
 s=s.replace('−','-').replace('∈',r'\in').replace('∞',r'\infty').strip().rstrip('.?')
 s=re.sub(r'\{\\color\{[^}]+\}\{([^{}]*)\}\}',r'\1',s)
 s=re.sub(r'\\(?:,|;|!|quad|qquad)', '',s)
 return s.replace(' ','').replace('\n','')
@lru_cache(None)
def num(s):
 s=clean(s)
 if s in (r'\infty',r'-\infty'):return sp.oo if not s.startswith('-') else -sp.oo
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 s=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',s)
 s=re.sub(r'(\d)(sqrt)',r'\1*\2',s)
 assert re.fullmatch(r'[\d+*/().\-sqrt]+',s),s
 return sp.sympify(s)
@lru_cache(None)
def _read(s):
 s=clean(s.replace('$',''))
 if 'or' in s:
  left,right=s.split('or');a,b=read(left),read(right)
  assert a['variable']==b['variable']
  return {'set':sp.Union(a['set'],b['set']),'variable':a['variable'],'form':'union','orientation':None}
 m=re.fullmatch(r'([a-z])\\in(.+)',s)
 if m:
  q=read(m[2]);assert q['form']=='interval';q.update(variable=m[1],form='membership');return q
 if s.startswith(('(','[')):
  assert s[-1] in (')',']'),s
  a,b=map(num,s[1:-1].split(','));return {'set':sp.Interval(a,b,left_open=s[0]=='(',right_open=s[-1]==')'),'variable':None,'form':'interval','orientation':None}
 terms=re.split(r'(\\le|\\ge|<|>)',s)
 assert len(terms) in (3,5),(s,terms)
 variables=[z for z in terms[::2] if re.fullmatch('[a-z]',z)];assert len(variables)==1,s
 variable=variables[0];answer=sp.S.Reals
 for i in range(0,len(terms)-2,2):
  left,op,right=terms[i:i+3]
  assert (left==variable)!=(right==variable),s
  bound=num(right if left==variable else left)
  upper=(op in ('<',r'\le')) if left==variable else (op in ('>',r'\ge'))
  strict=op in ('<','>')
  ray=sp.Interval(-sp.oo,bound,right_open=strict) if upper else sp.Interval(bound,sp.oo,left_open=strict)
  answer=sp.Intersection(answer,ray)
 return {'set':answer,'variable':variable,'form':'chain' if len(terms)==5 else 'ray','orientation':('ascending' if terms[1] in ('<',r'\le') else 'descending') if len(terms)==5 else None}
def read(s):return dict(_read(s))

def equal(a,b):
 # Exact SymPy sets canonicalize rational and algebraic endpoint expressions.
 # This is set-object comparison, never comparison of serialized expressions.
 return a==b
def inline(s):return re.findall(r'(?<!\$)\$(?!\$)([^$]+)\$(?!\$)',s)
def fingerprint(direction,target):
 return g.digest({'direction':direction,'a':sp.srepr(target.start),'b':sp.srepr(target.end),'endpoint_inclusion':'both'})
def check(r,raw=False):
 q=r['question'];fs=q[':question/answer-fields'];assert len(fs)==1
 f=fs[0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 ps=inline(q[':question/problem']);assert len(ps)==1
 prompt=read(ps[0]);target=prompt['set'];assert isinstance(target,sp.Interval) and not target.left_open and not target.right_open and target.start.is_finite and target.end.is_finite
 direction='inequality_to_interval' if prompt['form']=='chain' else 'interval_to_inequality';assert prompt['form'] in ('chain','membership')
 bank=f[':answer-field/choices'];assert len(bank)==5
 assert len({a[':answer/id'] for a in bank})==5
 parsed=[read(a[':answer/value']) for a in bank]
 assert all(not equal(a['set'],b['set']) for i,a in enumerate(parsed) for b in parsed[i+1:])
 matches=[i for i,p in enumerate(parsed) if equal(p['set'],target)];assert len(matches)==1
 for p in parsed:
  if direction=='inequality_to_interval':assert p['form']=='interval'
  else:assert p['variable']==prompt['variable'] and p['form'] in ('chain','union')
 if ':answer-field/correct' in f:
  assert bank[matches[0]][':answer/id']==f[':answer-field/correct'][1]
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];stages=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
  expected=['chain','interval','membership'] if direction=='inequality_to_interval' else ['membership','chain']
  assert len(stages)==len(expected)
  for text,form in zip(stages,expected):
   stage=read(text);assert stage['form']==form,(form,stage,text);assert equal(stage['set'],target),(stage,target)
   if stage['variable'] is not None:assert stage['variable']==prompt['variable']
   if form=='chain':
    ref=prompt if direction=='inequality_to_interval' else parsed[matches[0]]
    assert stage['orientation']==ref['orientation']
  assert 'endpoints' in sol and '*included*' in sol.replace('*are* included','*included*')
  assert 'Parentheses' in sol and 'Brackets' in sol
  # Read all informative inline endpoint claims, rather than the final key alone.
  claims=inline(sol)
  endpoint_claims=[z for z in claims if not any(t in z for t in ['color','phantom','(',')','[',']'])]
  if direction=='inequality_to_interval':assert [num(z) for z in endpoint_claims]==[target.start,target.end],endpoint_claims
  else:assert not endpoint_claims
 if not raw:
  assert r['generation']['template']==direction
  assert fingerprint(direction,target)==r['generation']['mathematical_fingerprint']
  assert r['generation']['variable']==prompt['variable']
  if direction=='inequality_to_interval':assert r['generation']['orientation']==prompt['orientation']
  g._fmt.validate_generated_record(r)
 return {'set':str(target),'variable':prompt['variable'],'direction':direction,'orientation':prompt['orientation'] or parsed[matches[0]]['orientation'],'stages':len(stages) if ':question/worked-solution' in q else 0}

def engine_item(r,label):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'native radio entity-ID contract: independently read full choice'} for a in f[':answer-field/choices']]
 value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
 # Values and equivalent mathematical expressions are deliberately NOT IDs.
 checks += [{'submitted':value,'expected':'unresolved','purpose':'radio value-expression is not an entity ID; not a mathematical false rejection'}, {'submitted':value.replace(' ','')+' ','expected':'unresolved','purpose':'equivalent display expression remains outside radio-ID contract'}, {'submitted':'99999999','expected':'unresolved','purpose':'foreign entity ID outside full field context'}]
 return {'label':label,'record':r,'checks':checks}

def main():
 baseline=json.loads((D/'registered-baseline.json').read_text())
 actual_paths=[D.parent/'17592186059829.py']+list((D.parent/'17592186059829').rglob('*'))+list((D.parent/'__pycache__').glob('17592186059829.*.pyc'))
 actual={str(p.relative_to(ROOT)):sha(p) for p in sorted(actual_paths) if p.is_file()};assert actual==baseline,'registered tree/pathset changed'
 frozen=ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186059829.json';assert (D/'source.json').read_bytes()==frozen.read_bytes()
 sources=json.loads((D/'source-cases.json').read_text());inventory=json.loads((D/'independent-inventory.json').read_text())
 s=json.loads(frozen.read_text());assert [z['record'] for z in sources]==[q for q in s['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q]
 assert [z['record'] for z in inventory['questions']]==[q for q in s['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 native=[];replays=[];samples=[];math_count=0;stage_count=0;coverage={}
 for z in sources:
  sid=z['source_id'];original=z['record'];r=g.replay_source(sid);check(r,True);math_count+=1
  if sid=='q-59295':
   assert ':question/difficulty' not in original and ':question/worked-solution' not in original and ':answer-field/correct' not in original[':question/answer-fields'][0]
   repair=g.generate('easy',19,parameters={'a':'-2','b':'1'},profile='observed_inequality',variable='x',orientation='ascending');check(repair);samples.append(repair);native.append(engine_item(repair,'supported-repair-q-59295'))
   replay=repair
  else:
   level,profile,p=('easy','captured_interval',{'a':'-10','b':'3'}) if sid=='q-102200' else ('moderate','captured_inequality',{'a':'-7','b':'0'})
   replay=g.generate(level,19,parameters=p,profile=profile,variable='x',orientation='ascending');check(replay);samples.append(replay)
   assert replay['question'][':question/problem']==original[':question/problem'].replace(']?$',']$?')
   assert replay['question'][':question/worked-solution']==original[':question/worked-solution']
   native.append(engine_item(replay,'source-replay-'+sid))
  of=original[':question/answer-fields'][0];rf=replay['question'][':question/answer-fields'][0]
  # Full source bank + answer type matched bijectively via mathematical sets.
  for a in of[':answer-field/choices']:
   assert sum(a[':answer/type'][':db/ident']==b[':answer/type'] and equal(read(a[':answer/value'])['set'],read(b[':answer/value'])['set']) for b in rf[':answer-field/choices'])==1
  replays.append({'source_id':sid,'original_choices':5,'matched_choices':5,'matched_distractors':4,'complete_bank':True,'correct_key':'absent original; separate supported repair' if sid=='q-59295' else 'matched','source_eligible':sid!='q-59295','solution': 'authored repair based on canonical stages' if sid=='q-59295' else 'exact source prose and operative stages','punctuation_fix':sid=='q-154728'})
 # Exact captured independent inventory is retained, never counted as MA evidence.
 for item in inventory['questions']:
  r={'knowledge_point':{'title':g.TITLE},'question':g.normalize_raw(item['record']),'generation':{'template':'inequality_to_interval' if 'The inequality' in item['record'][':question/problem'] else 'interval_to_inequality'}}
  result=check(r,True);math_count+=1;stage_count+=result['stages'];native.append(engine_item(r,'captured-independent-'+r['question'][':question/id']))
 # Exhaust all endpoint sets under each complete bank at base variable/orientation.
 # For hard surds, SymPy ordering is exact; native representative checks follow.
 for level in ['easy','moderate','hard']:
  profiles=['observed_interval','observed_inequality']+(['captured_interval'] if level=='easy' else ['captured_inequality'] if level=='moderate' else [])
  coverage[level]={}
  for profile in profiles:
   catalog=g.parameter_catalog('easy' if profile.startswith('captured_') else level)
   for i,p in enumerate(catalog):
    if i%500==0:print('checking',level,profile,i,'/',len(catalog),flush=True)
    r=g.generate(level,37,profile=profile,parameters=p,variable='x',orientation='ascending');got=check(r);math_count+=1;stage_count+=got['stages']
   coverage[level][profile]={'endpoint_pairs':len(catalog),'entire_banks_checked':len(catalog),'all_options_checked':5*len(catalog)}
  # Hold numerical set fixed, exercise ALL variable and orientation slots under
  # every profile. Aliases are not additional mathematical task capacity.
  for profile in profiles:
   catalog=g.parameter_catalog('easy' if profile.startswith('captured_') else level)
   for p in [catalog[0],catalog[len(catalog)//2],catalog[-1]]:
    base=None
    for variable in g.VARIABLES:
     for orientation in g.ORIENTATIONS:
      r=g.generate(level,17,profile=profile,parameters=p,variable=variable,orientation=orientation);got=check(r);math_count+=1;stage_count+=got['stages']
      fp=r['generation']['mathematical_fingerprint'];base=base or fp;assert base==fp
      native.append(engine_item(r,level+'-'+profile+'-'+variable+'-'+orientation+'-'+str(p)))
      if p==catalog[len(catalog)//2]:samples.append(r)
  # Sampling must actually exercise every declared presentation slot/profile.
  draws=[g.generate(level,i) for i in range(60)]
  assert {r['generation']['variable'] for r in draws}==set(g.VARIABLES)
  assert {r['generation']['orientation'] for r in draws}==set(g.ORIENTATIONS)
  assert {r['generation']['bank_profile'] for r in draws}==set(profiles)
 # Truth-preserving final answer with corrupted earlier work MUST fail.
 controls=[]
 for template in g.TEMPLATES:
  r=g.generate('easy',1,template=template,parameters={'a':'-2','b':'1'},profile='observed_interval' if template==g.TEMPLATES[0] else 'observed_inequality',variable='y',orientation='descending')
  for defect in ['endpoint','variable','closure','stage-order']:
   bad=copy.deepcopy(r);sol=bad['question'][':question/worked-solution'];stages=list(re.finditer(r'\$\$\s*(.*?)\s*\$\$',sol,re.S));idx=0;stage=stages[idx];text=stage[1]
   replacement=text.replace('-2','-3',1) if defect=='endpoint' else text.replace('y','z',1) if defect=='variable' else text.replace(r'\ge','>',1).replace('[','(',1) if defect=='closure' else stages[-1][1]
   bad['question'][':question/worked-solution']=sol[:stage.start(1)]+replacement+sol[stage.end(1):]
   try:check(bad)
   except (AssertionError,ValueError):controls.append({'direction':template,'defect':defect,'rejected':True,'final_key_unchanged':True})
   else:raise AssertionError('negative control survived '+defect)
 # strict input boundaries, deterministic repeat, unique mathematical batches.
 for bad in [True,False,'1',1.5,sp.Rational(1,2)]:
  for kw in [{'seed':bad},{'count':bad}]:
   try:g.generate_batch('easy',**kw)
   except ValueError:pass
   else:raise AssertionError(('invalid API',kw))
 try:g.generate_batch('easy',count=g.capacity('easy')+1)
 except ValueError:pass
 else:raise AssertionError('capacity guard')
 batches={l:g.generate_batch(l,seed=91,count=30) for l in ['easy','moderate','hard']}
 for level,rs in batches.items():
  assert rs==g.generate_batch(level,seed=91,count=30)
  assert len({r['generation']['mathematical_fingerprint'] for r in rs})==30
  for r in rs:check(r);math_count+=1
 cli=json.loads(subprocess.check_output([sys.executable,str(SCRIPT),'--difficulty','all','--count','1','--format','json'],text=True));assert len(cli)==3
 md=subprocess.check_output([sys.executable,str(SCRIPT),'--difficulty','all','--count','1','--format','markdown'],text=True);assert md.count('Correct:')==3
 for option in ['--seed','--count']:
  for value in ['true','1.5','1/2']:
   result=subprocess.run([sys.executable,str(SCRIPT),option,value],capture_output=True);assert result.returncode!=0
 write('samples.json',samples);write('source-replay.json',replays);write('negative-controls.json',controls);write('engine-input.json',native)
 subprocess.run([str(D/'check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
 engine=json.loads((D/'engine-report.json').read_text())
 build=json.loads((D/'reused-grader-build.json').read_text())
 for category in ['engine_sources','dependencies']:
  for path,expected in build[category].items():assert sha(ROOT/path)==expected,path
 assert sha(D/'check-engine')==build['binary_sha256']
 assert sha(ROOT/build['library'])==build['library_sha256']
 assert sha(ROOT/build['source'])==build['source_sha256']
 provenance={'binary':str(D/'check-engine'),'binary_sha256':sha(D/'check-engine'),'helper_source_sha256':sha(ROOT/'generate/runs/current/check-engine.rs'),'current_learning_source_sha256':sha(ROOT/'engine/rust/learning.rs'),'Cargo_lock_sha256':sha(ROOT/'Cargo.lock'),'binary_build_correspondence':'Verified copied binary against retained direct-current-source compilation provenance; all 28 engine source and 11 dependency hashes, compiled library hash and helper source hash match. See reused-grader-build.json.','entry_point':engine['entry_point']}
 write('engine-provenance.json',provenance)
 report={'worker_ready':True,'basis':2275,'generator_sha256':sha(SCRIPT),'source_original_practice_records':3,'source_original_keyed':2,'source_raw_ineligible':['q-59295: missing difficulty/correct key/worked solution'],'source_choices_matched':15,'source_distractors_matched':12,'complete_source_banks':3,'source_solution_exact':2,'canonical_example_counted_as_practice':False,'independent_inventory_records':len(inventory['questions']),'mathematical_records_checked':math_count,'operative_equations_checked':stage_count,'negative_controls_rejected':len(controls),'coverage':coverage,'capacity':{l:g.capacity(l) for l in ['easy','moderate','hard']},'native_records':len(native),'native':{k:engine[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'registered_immutable_files':len(baseline),'registered_pathset_hashes_unchanged':True,'python':platform.python_version(),'sympy':sp.__version__,'limitations':['Hard endpoint forms and rational moderate variants are independently authored reading extensions, not original observed higher-level practice.','Only bounded finite closed target intervals; other closures occur solely in source distractors.','Radio entity selection is graded natively; expression equivalence is a separate mathematical validator contract.','Current-source native radio grading reuses a hash-verified current-source build; preserved generic frozen runner was not treated as current-source proof.'],'independent_root_qa':'pending'}
 write('validation.json',report);print(json.dumps(report))
if __name__=='__main__':main()
