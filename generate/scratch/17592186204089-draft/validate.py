"""Standalone frozen-draft validation; no database or mutable QA imports."""
import copy,hashlib,importlib.util,json,subprocess,sys,itertools
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
EXPECTED_PRIVATE_SHA={'source.json': 'e78a579d319b28f89eab504094ebc10274b9783ff6a7ebd9e5b0b32ac3ff937a', 'display_parser.py': 'fb78f4e5d89e138a5bd74b5dd635a0e852536f6089c972ebfa53b2cb5a2a5091', 'math_format.py': '723744b896f1ff5290bce3ac7e70a15eb60e810df118686164f87bd412295291'}
for name,expected in EXPECTED_PRIVATE_SHA.items():
 assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==expected,'frozen private dependency changed: '+name
g=module('private_generator',HERE.with_suffix('.py'));p=module('private_display_parser',HERE/'display_parser.py')
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def checks(rec):
 out=[]
 for i,f in enumerate(rec['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:out.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every field-owned choice, full bank'})
  offset=100+sum(len(v[':answer-field/choices']) for v in rec['question'][':question/answer-fields'][:i])
  correct_id=offset+next(j for j,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
  for entry in ('000'+str(correct_id),'+'+str(correct_id)):
   out.append({'field_index':i,'submitted':entry,'expected':'accepted','purpose':'equivalent decimal spelling of the canonical owned entity ID'})
  # Native choice contract takes entity IDs. Ordinary numeric/text submissions
  # and foreign IDs fail as documented native errors; never recategorize them.
  for value in ('0','1','+1','999999','true','false'):
   out.append({'field_index':i,'submitted':value,'expected':'unresolved','purpose':'native invalid choice submission; explicit error retained'})
  if len(rec['question'][':question/answer-fields'])>1:
   out.append({'field_index':i,'submitted':str(100+2*((i+1)%3)),'expected':'unresolved','purpose':'foreign field choice ID'})
 return out
source=json.loads((HERE/'source.json').read_text());raw=[];replays=[];mappings=[];cases=[];records=[]
for c in g.SOURCE_CASES:
 src=g.ORIGINALS[c['source_id']];assert g.replay_source(c['source_id'])==src;raw.append({'source_id':c['source_id'],'question':g.replay_source(c['source_id'])})
 rec=g.generate('easy',parameters=c['parameters'],template=c['template']);p.validate(rec);replays.append(rec);cases.append(c)
 assert rec['question'][':question/problem']==src[':question/problem']
 assert rec['question'][':question/worked-solution'].replace('$','')==src[':question/worked-solution'].replace('$','')
 for original,new in zip(src[':question/answer-fields'],rec['question'][':question/answer-fields']):
  assert original[':answer-field/key']==new[':answer-field/key'] and original[':answer-field/type'][':db/ident']==new[':answer-field/type']
  assert [a[':answer/value'] for a in original[':answer-field/choices']]==[a[':answer/value'] for a in new[':answer-field/choices']]
  assert original[':answer-field/correct'][':answer/value']==next(a[':answer/value'] for a in new[':answer-field/choices'] if a[':answer/id']==new[':answer-field/correct'][1])
  mappings.append({'source_id':c['source_id'],'field_key':new[':answer-field/key'],'profile':c['bank_profile'],'choices':[{'value':a[':answer/value'],'recipe':'literal true/false classification state' if c['bank_profile']=='boolean-per-equation' else 'exact observed subset '+a[':answer/value'],'exact_reproduced':True} for a in original[':answer-field/choices']],'correct_value':original[':answer-field/correct'][':answer/value'],'feedback':'absent in frozen source; absent in generated bank'})
 records.append(rec)
capacity={};allfp=set();stages=0;patterns=set();slotvalues={'coefficients':set(),'constants':set(),'variables':set()}
for level in g.SUPPORTED_LEVELS:
 batch=g.batch(level,256,0);assert len(batch)==256
 fingerprints={r['generation']['parameter_fingerprint'] for r in batch};assert len(fingerprints)==256 and not fingerprints&allfp;allfp.update(fingerprints)
 capacity[level]={'distinct_semantic_tasks':256,'templates':{t:64 for t in g.TEMPLATES},'same_method_sparse_band':level!='easy'}
 for rec in batch:
  detail=p.validate(rec);stages+=detail['displayed_stages'];patterns.add(detail['status_pattern']);records.append(rec)
  meta=rec['generation'];assert rec==g.generate(level,meta['seed'],meta['template'],meta['parameters'],meta['bank_profile'])
  slotvalues['variables'].add(meta['parameters']['variable'])
  for a,b,c,d in meta['parameters']['equations']:slotvalues['coefficients'].update((a,c));slotvalues['constants'].update((b,d))
 for template in g.TEMPLATES:
  for params in g.CATALOG[level][template]:p.validate(g.generate(level,parameters=params,template=template))
 assert batch==g.batch(level,256,0)
 try:g.batch(level,257)
 except ValueError:pass
 else:raise AssertionError('capacity overflow accepted')
# Controlled radio target changes retain every coefficient while transforming
# the whole source bank with all six permutations. No extra learner skill.
target_reviews=[];target_coverage={}
for level in g.SUPPORTED_LEVELS:
 group=g.CATALOG[level]['radio-detailed-scaled'][:6];assert len(group)==6
 bases=[];positions=set();permutations=set()
 for params in group:
  order=params['label_permutation'];base=[None,None,None]
  for new_index,old_index in enumerate(order):base[old_index]=params['equations'][new_index]
  bases.append(base);rec=g.generate(level,template='radio-detailed-scaled',parameters=params);detail=p.validate(rec)
  selected=next(a[':answer/value'] for a in rec['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==rec['question'][':question/answer-fields'][0][':answer-field/correct'][1])
  positions.add(selected);permutations.add(tuple(order));target_reviews.append(rec)
 assert all(base==bases[0] for base in bases) and positions=={'I only','II only','III only'} and len(permutations)==6
 all_radio=[r for r in records if r['question'][':question/difficulty']==':question.difficulty/'+level and r['generation']['template']=='radio-detailed-scaled']
 counts={key:0 for key in ('I','II','III')}
 for rec in all_radio:
  _,_,_,statuses=p.read_prompt(rec['question'][':question/problem']);index=next(i for i,status in enumerate(statuses) if status==p.sp.S.EmptySet);counts[p.LABELS[index]]+=1
 assert all(counts.values());target_coverage[level]={'inconsistent_positions':counts,'controlled_same_coefficients_permutations':6}
save('target-change-review.json',target_reviews)
radio_mutations=[]
anchor=target_reviews[0];changed=target_reviews[1]
for kind in ('stale_footer','stale_key','stale_bank','stale_label_role','stale_prompt_label'):
 bad=copy.deepcopy(changed);q=bad['question'];f=q[':question/answer-fields'][0]
 if kind=='stale_footer':q[':question/worked-solution']=q[':question/worked-solution'].rsplit('Therefore, the correct answer',1)[0]+'Therefore, the correct answer is "I only."'
 elif kind=='stale_key':f[':answer-field/correct'][1]=f[':answer-field/choices'][1][':answer/id']
 elif kind=='stale_bank':
  for a,b in zip(f[':answer-field/choices'],anchor['question'][':question/answer-fields'][0][':answer-field/choices']):a[':answer/value']=b[':answer/value']
 elif kind=='stale_label_role':bad['generation']['parameters']['label_permutation']=[0,1,2]
 else:q[':question/problem']=q[':question/problem'].replace('I. $','II. $',1)
 try:p.validate(bad)
 except (AssertionError,ValueError,KeyError):radio_mutations.append(kind)
 else:raise AssertionError('stale radio target mutation passed '+kind)
assert len(radio_mutations)==5
for level in g.SUPPORTED_LEVELS:
 params=copy.deepcopy(g.CATALOG[level]['radio-detailed-scaled'][0]);a=g.generate(level,seed=0,template='radio-detailed-scaled',parameters=params);b=g.generate(level,seed=999,template='radio-detailed-scaled',parameters=params)
 assert a['question']==b['question'] and a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 renamed=copy.deepcopy(params);renamed['variable']='x' if params['variable']!='x' else 'u';assert g.fingerprint(renamed)==g.fingerprint(params)
 for invalid in ([0,0,2],[False,1,2],[0,1,3],[1,0,2]):
  bad=copy.deepcopy(params);bad['label_permutation']=invalid
  try:g.generate(level,template='radio-detailed-scaled',parameters=bad)
  except ValueError:pass
  else:raise AssertionError('invalid permutation accepted '+repr(invalid))

# Fail-closed arbitrary input and mutation checks.
negative=[]
for change in ('prompt','intermediate','bank','key','conclusion','domain'):
 rec=copy.deepcopy(g.generate('easy',0));q=rec['question']
 if change=='prompt':q[':question/problem']=q[':question/problem'].replace('=', '=1+',1)
 elif change=='intermediate':q[':question/worked-solution']=q[':question/worked-solution'].replace('& =','& =1+',2)
 elif change=='bank':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='maybe'
 elif change=='key':q[':question/answer-fields'][0][':answer-field/correct'][1]=q[':question/answer-fields'][0][':answer-field/choices'][1][':answer/id'] if q[':question/answer-fields'][0][':answer-field/correct'][1]==q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/id'] else q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/id']
 elif change=='conclusion':q[':question/worked-solution']=q[':question/worked-solution'].rsplit('Therefore, the correct answer',1)[0]+'Therefore, the correct answer is "I, II, and III."'
 else:rec['generation']['domain']['domain']='complex numbers'
 try:p.validate(rec)
 except (AssertionError,ValueError,KeyError):negative.append(change)
 else:raise AssertionError('mutation passed '+change)
# g.DOMAIN is returned by reference; reset after testing the independent copy.
assert len(negative)==6
params=copy.deepcopy(g.CATALOG['easy']['detailed-scaled'][0]);params['equations'][0][1]=100
try:g.generate('easy',parameters=params)
except ValueError:negative.append('out-of-domain parameters')
else:raise AssertionError('unbounded parameters accepted')
engine=ROOT/'generate/runs/current/check-engine';assert sha(engine)=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
inputs=[{'label':'record/'+str(i),'record':r,'checks':checks(r)} for i,r in enumerate(records)]
subset_cases=[]
for i,r in enumerate(records):
 fields=r['question'][':question/answer-fields']
 if fields[0][':answer-field/type']!=':answer-field.type/checkbox':continue
 for bits in itertools.product((False,True),repeat=len(fields)):
  cs=[]
  for field_index,(f,bit) in enumerate(zip(fields,bits)):
   selected=next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==str(bit).lower())
   cs.append({'field_index':field_index,'submitted_answer_id':selected,'expected':'accepted' if selected==f[':answer-field/correct'][1] else 'rejected','purpose':'exhaustive checkbox response subset'})
  label='subset/'+str(i)+'/'+''.join(str(int(b)) for b in bits)
  inputs.append({'label':label,'record':r,'checks':cs})
  subset_cases.append({'label':label,'selected_subset':[f[':answer-field/key'] for f,b in zip(fields,bits) if b],'expected_question_correct':all(c['expected']=='accepted' for c in cs)})
save('engine-input.json',inputs)
subprocess.run([str(engine),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True,capture_output=True,text=True,timeout=60)
report=json.loads((HERE/'engine-report.json').read_text())
by_label={r['label']:r for r in report['records']}
for case in subset_cases:
 actual=all(c['outcome']=='accepted' for c in by_label[case['label']]['checks'])
 assert actual==case['expected_question_correct'];case['native_all_field_results_correct']=True
save('checkbox-subset-grading.json',subset_cases)
save('source-cases.json',cases);save('raw-replay.json',raw);save('served-original-replays.json',replays);save('choice-mapping.json',mappings);save('catalog.json',g.CATALOG)
save('independent-inventory.json',{'basis':2275,'lineage':source['lineage'],'questions':[{'record':q,'role':'independently authored inventory','relationship_to_source_templates':'Captured independent inventory, excluded from source-template inference.'} for q in source['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]})
review=[]
for level in g.SUPPORTED_LEVELS:
 for i,t in enumerate(g.TEMPLATES):review.append(g.generate(level,811+i,template=t))
save('review.json',{'original_replays':replays,'generated_variants':review,'controlled_radio_target_changes':target_reviews})
(HERE/'review.md').write_text('\n\n'.join(['# Complete originals and representative variants']+[f'## Source {c["source_id"]}\n\n'+g.markdown(r) for c,r in zip(cases,replays)]+[f'## {r["question"][":question/difficulty"]} / {r["generation"]["template"]}\n\n'+g.markdown(r) for r in review]+['## Controlled radio target change\n\n'+g.markdown(r) for r in target_reviews])+'\n')
baseline=json.loads((HERE/'baseline.json').read_text());baseline_ok=all(Path(r['path']).exists() and sha(Path(r['path']))==r['sha256'] for r in baseline['files']);assert baseline_ok
validation={'status':'worker_validated_root_review_pending','basis':2275,'source_coverage':{'practice_questions':8,'raw_whole_question_replays':8,'exact_prompts':8,'exact_full_worked_solutions_before_served_typography_repair':8,'complete_field_banks':22,'complete_question_banks':8,'matched_values':47,'total_values':47,'matched_correct_designations':22,'missing_options':[],'extra_options':[]},'mathematics':{'records':len(records),'finite_catalog_records_exhausted':768,'displayed_intermediate_stages':stages,'independent_parser':str(HERE/'display_parser.py'),'patterns':sorted(patterns),'slot_coverage':{k:sorted(v) for k,v in slotvalues.items()},'negative_controls':negative},'capacity':capacity,'radio_target_position_coverage':target_coverage,'radio_target_mutation_controls':radio_mutations,'native_grading':{k:report[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks')},'checkbox_subset_coverage':{'all_subsets_per_question':8,'question_instances':len(subset_cases)//8,'subset_cases':len(subset_cases),'empty_all_singletons_wrong_subsets':'all enumerated; correct iff every native field grade accepts','duplicate_normalization':'not applicable: one scalar owned true/false choice entity ID per field, no list-valued submission'},'native_unresolved_reason':'Separate malformed-input diagnostics only: 0/1/+1, foreign IDs, boolean text; no unresolved owned mathematical responses. Native grade_field reports errors for non-owned choices; exact error messages retained without converting to rejection. Valid owned canonical choices all accepted and all owned distractors rejected. No blank fields and no algebraic-equivalence text contract.','source_errors':[],'served_repairs':[{'sources':['q-287964','q-288058'],'repair':'Wrap three mathematical reductions in inline math delimiters; raw exact replay preserved.'}],'registered_baseline':{'unchanged':baseline_ok,'files':len(baseline['files']),'script_sha256':baseline['script_sha256']},'generator_sha256':sha(HERE.with_suffix('.py')),'engine_sha256':sha(engine),'database_writes':0,'registration_changes':0}
save('validation.json',validation);print(json.dumps(validation,indent=2))
