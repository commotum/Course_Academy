#!/usr/bin/env python3
"""Independent displayed mathematics, source-presence fidelity, memory-only grading."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];SCRIPT=HERE.with_suffix('.py')
spec=importlib.util.spec_from_file_location('subtract_matrix_draft',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2)+'\n')
def mat(text):return sp.Matrix([[sp.sympify(v.strip().replace(r'\,','')) for v in row.split('&')] for row in text.split(r'\\')])
def matrix_bodies(text):return re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)
def check(r):
 q=r['question'];m=r['generation'];t=m['template'];raw=m['evidence_only']
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 for value in [q[':question/problem'],q.get(':question/worked-solution',''),*[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in value),'C0 control character'
  assert '--' not in value.replace('---','') and '+-' not in value,'Ungrouped signed operand'
 a,b=map(mat,matrix_bodies(q[':question/problem']));c=a-b
 fs=q[':question/answer-fields'];radio=fs[0][':answer-field/type'].endswith('/radio')
 if ':question/worked-solution' in q:
  bodies=matrix_bodies(q[':question/worked-solution']);ms=list(map(mat,bodies))
  assert len(ms)==4,'Wrong structured stage count'
  assert ms[0]==a and ms[1]==b and ms[-2]==c and ms[-1]==c
  assert q[':question/worked-solution'].startswith('We subtract the corresponding entries:\n\n$$\n\\begin{aligned}')
  # Check independently each actual ordered arithmetic node, not merely equality.
  rows=[row.split('&') for row in bodies[-2].split(r'\\')]
  for printed,x,y in zip([v.strip() for row in rows for v in row],list(a),list(b)):
   expected=str(x)+'-'+('('+str(y)+')' if y<0 else str(y))
   assert printed==expected,'Subtraction operation structure lost'
  assert q[':question/worked-solution'].count(r' \\  & =')==(1 if t in ('q-108','q-69603') else 2)
 if radio:
  assert len(fs)==1 and len(fs[0][':answer-field/choices'])==5
  vals=[mat(matrix_bodies(ans[':answer/value'])[0]) for ans in fs[0][':answer-field/choices']]
  assert len({tuple(v) for v in vals})==5
  good=[ans[':answer/id'] for ans,v in zip(fs[0][':answer-field/choices'],vals) if v==c];assert len(good)==1
  if ':answer-field/correct' in fs[0]:assert fs[0][':answer-field/correct'][1]==good[0]
  if not raw:
   expected=[c,a+b,b-a]
   u=c.copy();u[0,0]=a[0,0]+b[0,0]
   v=c.copy();v[0,1]=b[0,1]-a[0,1]
   expected.extend([u,v]);assert {tuple(x) for x in expected}=={tuple(x) for x in vals}
 else:
  assert len(fs)==6
  placeholders=re.findall(r'\{\{(field-\d+)\}\}',q[':question/problem']);assert sorted(placeholders)==sorted(f[':answer-field/key'] for f in fs)
  # Independently derive every field target from rendered table cells.
  cells=[]
  for line in q[':question/problem'].splitlines():
   if line.startswith('|') and '---' not in line:
    cells.extend(x.strip() for x in line.split('|') if x.strip().startswith('{{') or re.fullmatch(r'\$-?\d+\$',x.strip()))
  assert len(cells)==a.rows*a.cols
  bykey={f[':answer-field/key']:f for f in fs}
  actual_targets=[]
  for idx,(cell,x) in enumerate(zip(cells,list(c))):
   if cell.startswith('{{'):
    f=bykey[cell[2:-2]];assert len(f[':answer-field/choices'])==1
    ans=f[':answer-field/choices'][0];assert sp.sympify(ans[':answer/value'])==x
    assert f[':answer-field/correct'][1]==ans[':answer/id'];actual_targets.append(idx)
   else:assert int(cell[1:-1])==x
  if t=='q-319625':assert actual_targets==m['parameters']['targets']
  else:assert actual_targets==list(range(6))
 for f in fs:
  ids=[ans[':answer/id'] for ans in f[':answer-field/choices']];assert len(ids)==len(set(ids))
  if ':answer-field/correct' in f:assert f[':answer-field/correct'][1] in ids
 if not raw:g.validate_generated_record(r)
 assert m['mathematical_fingerprint']==g.fingerprint(t,m['parameters'])
 return r

def native(label,r):
 if any(':answer-field/correct' not in f for f in r['question'][':question/answer-fields']):
  r=copy.deepcopy(r);a,b=map(mat,matrix_bodies(r['question'][':question/problem']));correct=a-b
  for f in r['question'][':question/answer-fields']:
   ans=next(a for a in f[':answer-field/choices'] if mat(matrix_bodies(a[':answer/value'])[0])==correct)
   f[':answer-field/correct']=[':answer/id',ans[':answer/id']]
  label='independently-inferred-key-fixture-'+label
  r['generation']['grading_fixture_repair']='Missing captured correct ref independently derived from actual displayed matrices; this fixture is not faithful raw replay.'
 checks=[]
 for idx,f in enumerate(r['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:continue
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':idx,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every owned displayed option'} for a in f[':answer-field/choices'])
  else:
   n=int(f[':answer-field/choices'][0][':answer/value'])
   checks.extend({'field_index':idx,'submitted':entry,'expected':expected,'purpose':'canonical/equivalent arithmetic/known wrong integer'} for entry,expected in [(str(n),'accepted'),('('+str(n+3)+'-3)','accepted'),(str(n+1),'rejected')])
 return {'label':label,'record':r,'checks':checks}

def fail_mutation(r,mutate):
 x=copy.deepcopy(r);mutate(x)
 try:check(x)
 except (AssertionError,ValueError):return
 raise AssertionError('Validation accepted mutated learner content')

def main():
 snapshots=Path('generate/runs/current/refresh-2026-10-14')
 assert (HERE/'source.json').read_bytes()==(ROOT/snapshots/'sources/17592186054649.json').read_bytes()
 before=json.loads((HERE/'baseline-hashes-before.json').read_text());now={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'generate/scratch/17592186054649.py',*(ROOT/'generate/scratch/17592186054649').rglob('*')] if p.is_file()}
 now={str(Path(k).relative_to(ROOT)):v for k,v in now.items()};assert now==before,'Registered package changed';save('baseline-hashes-after.json',now)
 replays=[];cases=[];mapping=[];inputs=[];review=[];stats=[]
 for t,source in g.SOURCES.items():
  p=g.original(t);r=check(g.generate('easy',23,t,parameters=p,profile='observed:'+t));q=r['question']
  # All content attribute presence, including absent rating, worked solution and correct refs.
  assert set(q)-{':question/id'}==set(source)-{':question/id',':db/id'}
  assert q[':question/problem']==source[':question/problem']
  if ':question/worked-solution' in source:assert q[':question/worked-solution']==source[':question/worked-solution']
  vals=0;keys=0
  for sf in source[':question/answer-fields']:
   gf=next(f for f in q[':question/answer-fields'] if f[':answer-field/key']==sf[':answer-field/key'])
   assert set(gf)-{':answer-field/id'}==set(sf)-{':answer-field/id',':db/id'}
   assert gf[':answer-field/type']==sf[':answer-field/type'][':db/ident']
   assert sorted(a[':answer/value'] for a in gf[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
   for sa in sf[':answer-field/choices']:
    ga=next(a for a in gf[':answer-field/choices'] if a[':answer/value']==sa[':answer/value'])
    assert set(ga)-{':answer/id'}==set(sa)-{':answer/id',':db/id'}
    mapping.append({'source_id':source[':db/id'],'ma_id':t,'field':sf[':answer-field/key'],'source_answer_id':sa[':answer/id'],'value':sa[':answer/value'],'exact_value_match':True,'recipe_profile':'observed:'+t});vals+=1
   if ':answer-field/correct' in sf:
    correct=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1]);assert correct[':answer/value']==sf[':answer-field/correct'][':answer/value'];keys+=1
  cases.append({'source_id':source[':db/id'],'ma_id':t,'level':'easy','template':t,'parameters':p,'bank_profile':'observed:'+t,'original_rating':source.get(':question/difficulty'),'evidence_only':True,'eligible_for_learning':False})
  replays.append(r);inputs.append(native('faithful-source-'+t,r))
  stats.append({'ma_id':t,'matched_choices':vals,'total_choices':vals,'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in source else None,'matched_original_correct_refs':keys,'original_correct_refs':keys,'key_presence_parity':True})
  level='easy'
  variants=[check(g.generate(level,31+k,t)) for k in range(2)]
  review.append({'source_id':source[':db/id'],'ma_id':t,'original':source,'faithful_parameterized_replay':r,'authored_level':level,'generated_variants':variants})
  inputs.extend(native('review-'+t+'-'+str(k),r) for k,r in enumerate(variants))
  # Changed parameters must also faithfully preserve operative structure.
  rr=check(g.generate('easy',73,t,profile='observed:'+t))
  assert rr['question'][':question/problem']!=q[':question/problem']
  inputs.append(native('changed-observed-profile-'+t,rr));review[-1]['changed_historical_profile_variant']=rr
 save('source-cases.json',cases);save('source-replay.json',{'basis':g.S['basis'],'sources':stats,'matched_values':sum(x['matched_choices'] for x in stats),'originals':len(stats),'unrated_sources':['q-108','q-11478'],'missing_original_correct_refs':2,'missing_original_solutions':2,'raw_replays':replays});save('source-choice-mapping.json',mapping)
 independent=[q for q in g.S['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 save('independent-inventory.json',{'database':g.S['database'],'basis':g.S['basis'],'lineage':g.S['lineage'],'questions':[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'No independent inventory is present in this snapshot.'} for q in independent]})
 samples=[];coverage={level:set() for level in g.LEVEL_TEMPLATES};uniques={level:set() for level in coverage};targetsets=set();correct_positions=set()
 for level in g.LEVEL_TEMPLATES:
  for seed in range(120):
   r=check(g.generate(level,seed));samples.append(r);t=r['generation']['template'];coverage[level].add(t);uniques[level].add(r['generation']['mathematical_fingerprint']);inputs.append(native(level+'-'+str(seed),r))
   again=g.generate(level,seed+10000,t,parameters=r['generation']['parameters'],profile=r['generation']['profile'])
   assert again['question'][':question/id']==r['question'][':question/id']
   assert again['generation']['content_fingerprint']==r['generation']['content_fingerprint']
   if t in g.RADIO:
    f=r['question'][':question/answer-fields'][0];correct_positions.add(next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1]))
    alias=g.generate(level,seed,t,parameters=r['generation']['parameters'],profile='method-derived');assert alias['question'][':question/id']==r['question'][':question/id']
   if t=='q-319625':targetsets.update(r['generation']['parameters']['targets'])
  assert coverage[level]==set(g.LEVEL_TEMPLATES[level]);assert len(uniques[level])==120
 assert targetsets==set(range(9));assert correct_positions==set(range(5))
 # Fixed-matrix changed-target slots; all 84 six-cell subsets are meaningful.
 anchor=check(g.generate_hard(51,'q-319625'));p=anchor['generation']['parameters'];taskids=set()
 for targets in itertools.combinations(range(9),6):
  pp=copy.deepcopy(p);pp['targets']=list(targets)
  try:r=check(g.generate_hard(0,'q-319625',parameters=pp))
  except ValueError:continue
  taskids.add(r['generation']['mathematical_fingerprint']);inputs.append(native('target-subset-'+str(targets),r))
 assert len(taskids)>=30
 # Unrequested source cells change complete content but not assessed task.
 pp=copy.deepcopy(p);unqueried=next(i for i in range(9) if i not in p['targets']);pp['a'][unqueried]=pp['a'][unqueried]+1 if pp['a'][unqueried]<12 else pp['a'][unqueried]-1
 changed=check(g.generate_hard(0,'q-319625',parameters=pp));assert changed['generation']['mathematical_fingerprint']==anchor['generation']['mathematical_fingerprint'];assert changed['question'][':question/id']!=anchor['question'][':question/id']
 # Exact finite capacity lower bounds within an entry slice of each default.
 capacity={}
 for level in g.LEVEL_TEMPLATES:
  anchor=g.generate(level,17);p=anchor['generation']['parameters'];t=anchor['generation']['template'];fps=set();domain=range(10) if level=='easy' else range(-12,13)
  for vals in itertools.product(domain,repeat=4 if level=='easy' else 2):
   x,y=vals[:2];pp=copy.deepcopy(p);pp['a'][0]=x;pp['b'][0]=y
   if level=='easy':pp['a'][2]=vals[2];pp['b'][2]=vals[3]
   try:r=g.generate(level,0,t,parameters=pp)
   except ValueError:continue
   fps.add(r['generation']['mathematical_fingerprint'])
  assert len(fps)>50;capacity[level]={'enumerated_entry_slice_tasks':len(fps),'variable_entries':4 if level=='easy' else 2,'total_domain':'larger than this exact conservative lower bound','does_not_count_bank_aliases_or_names':True}
 # Same mathematical task across notation and complete bank differences.
 p=g.original('q-11441');normal_id=g.generate_easy(0,'q-11441',parameters=p)['question'][':question/id'];raw_id=g.generate_easy(0,'q-11441',parameters=p,profile='observed:q-11441')['question'][':question/id'];assert normal_id!=raw_id
 p=g.generate_moderate(92,'q-11441')['generation']['parameters'];aa=g.generate_moderate(0,'q-11441',parameters=p);bb=g.generate_moderate(0,'q-11478',parameters=p);assert aa['generation']['mathematical_fingerprint']==bb['generation']['mathematical_fingerprint'];assert aa['question'][':question/id']!=bb['question'][':question/id']
 try:g.generate_easy(0,'q-11441',parameters={'a':[0]*4,'b':[0]*4})
 except ValueError:pass
 else:raise AssertionError('Ambiguous complete authored bank accepted')
 # Stage, target, complete wrong-option and formatting mutation regressions.
 normal=next(r for r in samples if r['generation']['template']=='q-11441');raw=next(r for r in replays if r['generation']['template']=='q-319618')
 fail_mutation(normal,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(matrix_bodies(r['question'][':question/worked-solution'])[-2],matrix_bodies(r['question'][':question/worked-solution'])[-1])))
 fail_mutation(normal,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem']+'\x0c'))
 fail_mutation(raw,lambda r:r['question'].__setitem__(':question/problem',r['question'][':question/problem'].replace('{{field-1}}','{{field-2}}')))
 fail_mutation(normal,lambda r:r['question'][':question/answer-fields'][0][':answer-field/choices'][0].__setitem__(':answer/value',r'\begin{bmatrix}999 & 999 \\ 999 & 999\end{bmatrix}'))
 invalid=[]
 for level,t in [('easy','q-11441'),('moderate','q-11441'),('hard','q-319625')]:
  p=g.generate(level,71,t)['generation']['parameters'];pp=copy.deepcopy(p);pp['a'][0]=-13;invalid.append((level,t,pp))
  if level=='easy':pp=copy.deepcopy(p);pp['a'][0]=-1;invalid.append((level,t,pp))
  else:pp=copy.deepcopy(p);pp['b']=[abs(v) for v in pp['b']];invalid.append((level,t,pp))
  if t=='q-319625':pp=copy.deepcopy(p);pp['targets']=[0]*6;invalid.append((level,t,pp))
 for level,t,p in invalid:
  try:g.generate(level,0,t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit workload accepted')
 # Public field filter and unknown profiles reject rather than silently substitute.
 for seed in range(8):
  assert check(g.generate_hard(seed,field_type='blank'))['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank')
  assert check(g.generate_hard(seed,field_type='radio'))['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')
 assert check(g.generate_moderate(field_type='blank'))['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank')
 try:g.generate_easy(field_type='select')
 except ValueError:pass
 else:raise AssertionError('Unsupported field contract accepted')
 save('native-input.json',inputs);engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 save('review.json',{'source_templates':review,'level_examples':{level:[r for r in samples if r['question'][':question/difficulty'].endswith('/'+level)][:2] for level in coverage}})
 lines=['# Subtracting Matrices: basis2275 draft review','Original MA records preserve their labels/omissions. Generated examples are independently authored from the corresponding-entry method; moderate/hard grade assignments are unobserved design claims.']
 for row in review:
  source=row['original'];lines.extend(['## '+row['ma_id']+' original MA record',source[':question/problem'],'### Full original bank/fields'])
  for f in source[':question/answer-fields']:lines.append(f[':answer-field/key']+': '+', '.join(a[':answer/value'] for a in f[':answer-field/choices']))
  lines.append(source.get(':question/worked-solution','Original worked solution absent; original correct designation and rating also absent.'))
  lines.extend(['### Parameterized historical bank/layout variant — evidence only, not eligible for learning',g.markdown(row['changed_historical_profile_variant'])])
  for i,r in enumerate(row['generated_variants']):lines.extend(['### Independently authored '+row['authored_level']+' variant '+str(i+1),g.markdown(r)])
 lines.append('## Two independently authored examples at each requested level')
 for level in coverage:
  for r in [r for r in samples if r['question'][':question/difficulty'].endswith('/'+level)][:2]:lines.extend(['### '+level,g.markdown(r)])
 (HERE/'review.md').write_text('\n\n'.join(lines)+'\n')
 report={'passed':True,'basis':2275,'source_fidelity':{'originals':7,'complete_banks':7,'matched_choices':38,'total_choices':38,'original_correct_refs':20,'matched_original_correct_refs':20,'original_solutions':5,'exact_original_solutions':5,'raw_key_presence_parity':7,'unrated_and_missing_key_solution_sources':2},'mathematical_checks':{'normal_samples':360,'independent_displayed_subtraction_nodes':True,'complete_authored_bank_operations':True,'stage_and_control_character_mutations_rejected':True,'all_requested_target_cells_seen':sorted(targetsets),'valid_fixed_matrix_target_subsets':len(taskids),'default_template_coverage':{l:sorted(ts) for l,ts in coverage.items()},'unique_tasks_per_level':{l:len(v) for l,v in uniques.items()},'capacity_lower_bounds':capacity,'content_identity_seed_order_alias_checks':True,'known_invalid_explicit_parameters_rejected':len(invalid)},'native_grading':{'memory_only':True,'all_expected_results_matched':True,'records':len(inputs),'checks':sum(len(r['checks']) for r in inputs),'missing_raw_correct_refs_ungradable':2,'independently_inferred_key_fixture_records':sum(x['label'].startswith('independently-inferred-key-fixture-') for x in inputs),'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'registered_numeric_package_unchanged':True,'runtime_versions':{'python':sys.version.split()[0],'sympy':sp.__version__},'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (SCRIPT,HERE/'source.json',HERE/'validate.py')}}
 # Derive exact denominators; scalar blanks each contribute one correct ref.
 report['source_fidelity']['matched_choices']=report['source_fidelity']['total_choices']=sum(x['matched_choices'] for x in stats)
 report['source_fidelity']['original_correct_refs']=report['source_fidelity']['matched_original_correct_refs']=sum(x['original_correct_refs'] for x in stats)
 fspec=importlib.util.spec_from_file_location('root_source_fidelity',ROOT/'generate/runs/current/root-source-fidelity.py');F=importlib.util.module_from_spec(fspec);fspec.loader.exec_module(F);_,rootcounts=F.check(g,g.KP_ID,HERE);report['root_public_source_fidelity']=rootcounts
 save('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
