import sys
sys.dont_write_bytecode=True
import json,pathlib,re,collections,hashlib,ast,copy
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parent;JOB=ROOT.parent
# Reuse this review's independent parsing and shortcut functions, without rerunning sampling.
text=(ROOT/'review_checks.py').read_text();tree=ast.parse(text)
for node in tree.body:
 if isinstance(node,(ast.FunctionDef,ast.Assign)) and ((isinstance(node,ast.FunctionDef) and node.name in ['key','pars','ex','shortcut','measure']) or (isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EX' for t in node.targets))):
  exec(compile(ast.Module(body=[node],type_ignores=[]),str(ROOT/'review_checks.py'),'exec'))
def read(name):return json.load(open(ROOT/name))
def write(name,data):(ROOT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
stage=[];grade=[]
for group in ['sample','batch']:
 records=read('delivery-'+group+'/accepted.json'); raw=read('easy-samples.json' if group=='sample' else 'batch.json')
 def metrics(rs):
  signs=collections.Counter();positions=collections.Counter()
  for r in rs:
   q=r['question'];V,q0,c,flow,t=pars(q);signs['increasing' if q0<c*V else 'decreasing']+=1
   positions[next(i+1 for i,o in enumerate(q[':question/answer-fields'][0][':answer-field/choices']) if o[':answer/id']==key(q))]+=1
  return {'cases':dict(signs),'positions':dict(positions),'shortcut':measure(rs,group)}
 stage.append({'group':group,'before':metrics(raw),'after':metrics(records),'captured_basis':5397})
 for i,r in enumerate(records):
  q=r['question'];pick=shortcut(q)
  grade.append({'label':f'delivered-{group}-{i}','record':r,'checks':[{'submitted_answer_id':o[':answer/id'],'expected':'accepted' if o[':answer/id']==key(q) else 'rejected','purpose':'key independently checked against ODE in math-results; verify shared normalization preserved real learner behavior'} for o in q[':question/answer-fields'][0][':answer-field/choices']]+[{'submitted_answer_id':pick,'expected':'accepted','purpose':'bank-only shortcut after actual shared delivery filtering'}]})
# Independent current-source mathematical check. Compare replay banks mathematically, not formatting.
s=json.load(open(JOB/'source/source.json'));source_cases=[];source_records=[]
for orig in s['material']['kp'][':knowledge-point/questions']:
 q=copy.deepcopy(orig);V,q0,c,r,time=pars(q);f=c*V+(q0-c*V)*sp.exp(-r*sp.Symbol('t',real=True)/V)
 truths=[]
 for a in q[':question/answer-fields'][0][':answer-field/choices']:
  val=a[':answer/value']
  if time is None:
   e,A,k=ex(re.sub(r'\s+','',val));good=e==c*V and A==q0-c*V and k==r/V
  else:
   n=sp.Rational(re.match(r'([0-9.]+)',val)[1]);good=abs(float(n)-float(f.subs(sp.Symbol('t',real=True),time)))<.005
  if good:truths.append(a[':answer/id'])
 source_cases.append({'id':q[':question/id'],'entity_id':q[':db/id'],'correct_candidates':truths,'captured_correct':key(q),'unique_valid':len(truths)==1,'captured_key_agrees':None if key(q) is None else truths==[key(q)],'expected_function':str(f),'rounded_amount':None if time is None else f'{float(f.subs(sp.Symbol("t",real=True),time)):.2f}'})
 if key(q) is None:continue
 field=q[':question/answer-fields'][0];field[':answer-field/type']=field[':answer-field/type'][':db/ident'];field[':answer-field/correct']=[':answer/id',key(q)]
 for a in field[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
 rec={'knowledge_point':{'title':s['material']['kp'][':knowledge-point/title']},'question':q,'generation':{'template':'captured-source-interface-normalization','source_id':q[':question/id']}}
 source_records.append(rec)
 grade.append({'label':'current-source-'+q[':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id'] in truths else 'rejected','purpose':'independent math oracle for captured original; enum and lookup interface conversion only'} for a in field[':answer-field/choices']]})
write('source-math.json',{'cases':source_cases,'note':'No original is classified as generated. One missing source key is retained as missing, not supplied to native harness.'});write('source-original-records.json',source_records)
write('grader-delivery-input.json',grade)
# Direct counterfactual relationship checks, including same visible expression switching correctness.
cfs=read('counterfactual-records.json')
def correct_value(q):return next(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==key(q))
cv=[correct_value(r['question']) for r in cfs];cross=[]
for start,end in [(0,1),(1,0)]:
 other=next(a for a in cfs[end]['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/value']==cv[start]);cross.append({'from_case':start,'to_case':end,'expression':cv[start],'after_is_wrong':other[':answer/id']!=key(cfs[end]['question']),'native_case':f'counterfactual-{end}','submission_uuid':other[':answer/id'],'native_expected':'rejected'})
write('counterfactual-results.json',{'correct_values':cv,'initial_mass_changes_correct_sign':cv[0]!=cv[1],'flow_changes_exponential_time':cv[0]!=cv[2],'context_preserves_answer':cv[0]==cv[3],'cross_role_checks':cross,'native_report':'grader-report.json','render_records':'render-counterfactual-input.json','render_report':'render-counterfactual/rendering.json','observations':'All five choices in each pair tested against prompt-derived independent ODE. The initial-mass pair swaps the same 10±3e^{-t/20} visible expressions between correct and incorrect; context changes preserve expression. Correct final functions separately verified from worked solutions in math-results.json.'})
# Faithful database-free reproduction of question_selection.rs::select, on explicit local fixtures.
def select(candidates,weights,seed):
 bands=[sorted(set(candidates.get(b,[]))) for b in ['easy','moderate','hard']];digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 uniform=lambda off:(int.from_bytes(digest[off:off+8],'big')>>11)/2**53
 total=sum(w for w,b in zip(weights,bands) if b)
 draw=uniform(0)*total;pool=None
 for w,b in zip(weights,bands):
  if not b or not w:continue
  pool=b
  if draw<w:break
  draw-=w
 return pool[int(uniform(8)*len(pool))] if pool else None
# New records have no database entity IDs before publication; explicit local IDs test selection support, never claim future exact IDs.
rows=[];batch=read('delivery-batch/accepted.json');mapping={1000000+i:r for i,r in enumerate(batch)}
for history in [[],[1000000,1000001],[1000000,1000001,1000002,1000003]]:
 candidates={'easy':[i for i in mapping if i not in history]};chosen=[select(candidates,[1,0,0],f'independent-review-{i}') for i in range(100)]
 rows.append({'local_seen_history':history,'weights':[1,0,0],'selected_counts':dict(collections.Counter(chosen)),'shortcut_success':sum(shortcut(mapping[x]['question'])==key(mapping[x]['question']) for x in chosen),'draws':len(chosen)})
write('delivery-analysis.json',{'shared_filter_results':stage,'learner_selection':{'implementation':'engine/rust/question_selection.rs select: deduplicate/sort IDs; weight nonempty bands; SHA256 seeded uniform within chosen band. seen_before_task excludes history; caller separately excludes current prefix.','fixture_local_id_map':{i:r['question'][':question/id'] for i,r in mapping.items()},'tests':rows,'conditional_support':'All accepted new records are easy and all carry the defect, so any nonempty history-filtered subset retains it. Band weighting cannot distinguish bank profiles. Captured easy originals do not exhibit the same perfect strategy, so this is a recognizable generated-bank conditional defect, not a claim every question in the merged inventory is answerable by the cue.','limitations':['Actual policy weights and learner histories are not in captured inventory. Fixture weights are explicitly conditional on easy selection.','New database IDs do not exist before publication; local IDs test algorithmic support, not exact future task draws.','Captured inventory basis 5397; concurrent inventory updates can affect later deduplication.']},'raw_sampler':'sample() calls check_params(); generate() retries up to 2000 whole candidates on ValueError. No bank slots are replaced independently; every successful easy candidate uses the same five-model recipe. Rejection cannot break the algebraic bank fingerprint.','publication_file':'No preparation.json present; shared filter was reproduced read-only on captured inventory, rather than publication.','database_writes':0})
# Source replay mathematical normalization of the first current profile: same bank, missing repaired source attributes.
replay=read('source-replay-records.json')[0]['question'];orig=s['material']['kp'][':knowledge-point/questions'][0]
normalize=lambda x:re.sub(r'\s+','',x).replace('{e}','e')
write('source-replay-detail.json',{'source_id':orig[':question/id'],'entity_id':orig[':db/id'],'profile':'source_17592186229724','level':'easy','seed':61829,'bank_mathematically_same':sorted(normalize(a[':answer/value']) for a in orig[':question/answer-fields'][0][':answer-field/choices'])==sorted(normalize(a[':answer/value']) for a in replay[':question/answer-fields'][0][':answer-field/choices']),'source_has_solution':':question/worked-solution' in orig,'replay_has_solution':':question/worked-solution' in replay,'source_has_correct':key(orig) is not None,'replay_has_correct':key(replay) is not None,'source_difficulty':orig.get(':question/difficulty'),'replay_difficulty':replay.get(':question/difficulty'),'note':'Do not treat whitespace, unit typography or e bracing as a mathematical bank mismatch; the substantive mismatch is missing current attributes and unavailable three other captured profiles.'})
# Minimal standalone counterexample retained for adoption by repair.
r=read('easy-samples.json')[0];q=r['question'];write('minimal-failure.json',{'command':f'{sys.executable} {ROOT.parent}/workspace/17592186229181.py --difficulty easy --seed 81031 --count 1 --format json','record':r,'predicted_choice_uuid_without_prompt':shortcut(q),'stored_correct_uuid':key(q),'bank_only_rule':'Find leading constant duplicated exactly twice. Find constant plus signed exponential coefficient occurring four times. Select their unique intersection.','proof':'For models (E,A,k),(E/2,q0-E/2,2k),(2E,q0-2E,k/2),(rc,q0-rc,k),(E,-A,k), the only repeated constant is E (since k=r/V<=1/10), while four initial values equal q0. A≠0 by guard; their intersection is always the correct model. No prompt parameters needed.'})
print(json.dumps({'delivered':[(x['group'],x['after']['shortcut']['correct'],x['after']['shortcut']['total']) for x in stage],'source_math_unique':[x['unique_valid'] for x in source_cases],'counterfactual_correct':cv,'grader_cases':len(grade)},indent=2))
