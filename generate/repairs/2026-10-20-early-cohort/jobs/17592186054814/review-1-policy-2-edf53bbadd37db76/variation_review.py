"""Compare raw/delivered decisions and simple conditional cue strategies, read-only."""
import sys,json,re,collections,hashlib,pathlib
sys.dont_write_bytecode=True
from review_checks import R,J,P,REPO,g,save,semantic,oracle,tex,family,hashes,selected
load=lambda p:json.load(open(R/p))
files={'raw_sample':'sample-records.json','delivered_sample':'delivery-sample/accepted.json','raw_batch':'batch-records.json','delivered_batch':'delivery-batch/accepted.json'}
sets={n:load(p) for n,p in files.items()}
coverage={};probes=[]
for stage,rs in sets.items():
 fams=collections.defaultdict(collections.Counter)
 for r in rs:
  assert oracle(r)==semantic(r)
  fams[family(r)][semantic(r)]+=1
 coverage[stage]={'count':len(rs),'memberships':dict(collections.Counter(semantic(r) for r in rs)),'representations':{k:dict(v) for k,v in fams.items()},'C_positions':dict(collections.Counter(next(i for i,f in enumerate(r['question'][':question/answer-fields']) if '($C$)' in f[':answer-field/key']) for r in rs)),'records':[{'id':r['question'][':question/id'],'tex':tex(r),'membership':semantic(r)} for r in rs]}
 for subgroup in ['all','integer','fraction','decimal','radical','pi','negative radical']:
  group=[r for r in rs if subgroup=='all' or (subgroup==family(r)) or (subgroup=='negative radical' and tex(r).startswith(r'\sqrt{-'))]
  if not group:continue
  strategies=[('fixed C only',lambda r:'C'),('fixed all labels',lambda r:'NZQRC'),('fixed Q,R,C',lambda r:'QRC'),('first field only',lambda r:re.search(r'\(\$([NZQRC])\$\)',r['question'][':question/answer-fields'][0][':answer-field/key'])[1])]
  for cue,fn in strategies:
   correct=sum(fn(r)==semantic(r) for r in group)
   intended=(subgroup=='negative radical' and cue=='fixed C only')
   probes.append({'cue':cue,'subgroup':stage+'/'+subgroup,'scope':'overall' if subgroup=='all' else 'other_recognizable_subgroup','strategy':cue+' as the complete membership response','correct':correct,'total':len(group),'baseline':.2,'disposition':'intended_skill' if intended else 'not_predictive','conclusion':('Uniform guess among five eligible full membership patterns gives 0.2. Negative roots being nonreal is the actual source skill; this is a necessary mathematical simplification.' if intended else 'Uniform guess among five eligible full membership patterns gives 0.2. This rule does not solve the full fresh/delivered family. Small homogeneous subgroups can reflect value classification; see within-representation class coverage and controlled changes. No universal absence claim.'),'sample_refs':[files[stage],'coverage-results.json']})
  # Answer-producing action independent of which labels: choose a fixed number of fields.
  for count in [1,2,3,4,5]:
   correct=sum(len(semantic(r))==count for r in group)
   intended=(subgroup=='negative radical' and count==1) or (subgroup=='pi' and count==2)
   probes.append({'cue':'fixed selection count '+str(count),'subgroup':stage+'/'+subgroup,'scope':'within_template' if subgroup=='all' else 'other_recognizable_subgroup','strategy':'Always select '+str(count)+' fields (only a necessary action, not full correctness)','correct':correct,'total':len(group),'baseline':.2,'disposition':'intended_skill' if intended else 'not_predictive','conclusion':'Baseline 0.2 is uniformly guessing one of five possible selection counts. Count success does not guarantee correct labels. '+('Fixed count follows the known irrational/nonreal class by definition.' if intended else 'Not a universal action for the sampled parent representation; fractions/decimals and roots have multiple counts. Small batch singleton counts are not claimed as evidence of broad coverage.'),'sample_refs':[files[stage],'coverage-results.json']})
 # Exhaust every fixed positional subset and every correct-mathematical label-mask shortcut.
 subsets=[]
 for bits in range(1,32):
  ok=0
  for r in rs:
   chosen=''.join(s for s in 'NZQRC' if any((bits>>i)&1 and ('($'+s+'$)') in f[':answer-field/key'] for i,f in enumerate(r['question'][':question/answer-fields'])))
   ok+=chosen==semantic(r)
  subsets.append({'positional_bits':bits,'correct':ok,'total':len(rs)})
 best=max(subsets,key=lambda x:x['correct']);save(stage+'-position-probes.json',subsets)
 assert best['correct']<len(rs)
 probes.append({'cue':'best fixed positional subset','subgroup':stage+'/checkbox template','scope':'within_template','strategy':'Exhaust all 31 nonempty subsets of five UI positions; best bits='+str(best['positional_bits']),'correct':best['correct'],'total':len(rs),'baseline':1/31,'disposition':'not_predictive','conclusion':'Baseline 1/31 is uniform guessing a nonempty positional subset. Reported best is selected post hoc across all subsets, and still cannot solve all records. Shuffle alone is not sufficient; class variation independently checked.','sample_refs':[stage+'-position-probes.json',files[stage]]})
 # Necessary mathematical fixed action: C always belongs.
 probes.append({'cue':'C label','subgroup':stage+'/checkbox template','scope':'within_template','strategy':'Always check C (partial action)','correct':len(rs),'total':len(rs),'baseline':.5,'disposition':'intended_skill','conclusion':'Baseline 0.5 is a random boolean on C. All scoped values are complex, explicitly established by the nested source hierarchy. Other memberships still require classification.','sample_refs':[files[stage]]})
 # Canonical source operation for pi, even though ordinary sample can deduplicate to one.
 pi=[r for r in rs if family(r)=='pi']
 if pi:probes.append({'cue':'pi symbol','subgroup':stage+'/pi','scope':'other_recognizable_subgroup','strategy':'Select R,C for signed pi','correct':sum(semantic(r)=='RC' for r in pi),'total':len(pi),'baseline':.2,'disposition':'intended_skill','conclusion':'Baseline 0.2 is uniform full-mask guessing. Knowing pi is irrational is exactly source 3c87cce5-2762-52a9-b3ea-307f7f887046, so its fixed classification is justified.','sample_refs':[files[stage]]})
# Explicitly inspect replay-only radio banks, which are never sampled/delivered by generate().
radios=[r for r in load('source-replay-records.json') if r['question'][':question/answer-fields'][0][':answer-field/type']==':answer-field.type/radio']
for longest in [True,False]:
 correct=0
 for r in radios:
  vals=[a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  counts=[sum(s in v for s in 'NZQRC') for v in vals];idx=counts.index((max if longest else min)(counts));correct+=vals[idx]==selected(r['question'][':question/answer-fields'][0])
 probes.append({'cue':'longest set list' if longest else 'shortest set list','subgroup':'archival source radio banks','scope':'within_template','strategy':'Choose option with most set labels' if longest else 'Choose option with fewest set labels','correct':correct,'total':len(radios),'baseline':.2,'disposition':'not_predictive','conclusion':'Baseline 0.2 is a random choice from five. These are three fixed archival source records rather than a sampled radio family; neither list-length rule solves all three. No radio sampling coverage is claimed.','sample_refs':['source-replay-records.json']})
save('coverage-results.json',coverage);save('shortcut-results.json',probes)
# Stage transformation must preserve exact semantic responses and visible math.
transforms=[]
for stage,raw in [('delivered_sample','raw_sample'),('delivered_batch','raw_batch')]:
 by_prompt={r['question'][':question/problem']:r for r in sets[raw]}
 for r in sets[stage]:
  old=by_prompt[r['question'][':question/problem']]
  assert semantic(r)==semantic(old)==oracle(r)
  # Asset path normalization may change only the image path; no math changes.
  strip=lambda s:re.sub(r'!\[.*?\]\(.*?\)','IMAGE',s)
  assert strip(r['question'][':question/worked-solution'])==strip(old['question'][':question/worked-solution'])
  transforms.append({'stage':stage,'before':old['question'][':question/id'],'after':r['question'][':question/id'],'membership':semantic(r),'prompt_preserved':True,'solution_math_preserved':True})
save('delivery-transformation-results.json',transforms)
# Selection: actual weighted-band function, faithfully reproduced for single easy band,
# with explicit histories (none, leave-one, prefix) and seed draw. No DB access.
inv=json.load(open(J/'source/inventory.json'));save('inventory-records.json',inv['questions'])
candidates=[]
for q in inv['questions']:
 d=q.get(':question/difficulty');d=d.get(':db/ident') if isinstance(d,dict) else d
 if d==':question.difficulty/easy':candidates.append({'entity':q[':db/id'],'id':q[':question/id'],'problem':q[':question/problem'],'origin':'captured inventory'})
next_id=max(q[':db/id'] for q in inv['questions'])+1
for i,r in enumerate(sets['delivered_batch']):candidates.append({'entity':next_id+i,'id':r['question'][':question/id'],'problem':r['question'][':question/problem'],'origin':'hypothetical accepted batch'})
candidates.sort(key=lambda q:q['entity'])
def choose(pool,seed):
 if not pool:return None
 digest=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 return pool[int(u*len(pool))]['id']
selected_ids=[choose(candidates,f'task-review/kp-17592186054814/slot-{i}') for i in range(64)]
sole=[{'seen_entities':[q['entity'] for q in candidates if q!=keep],'remaining':keep['id'],'selected':choose([keep],'task-review/slot-0')} for keep in candidates]
assert all(x['remaining']==x['selected'] for x in sole)
seq=[];pool=candidates[:]
while pool:
 chosen=choose(pool,f'task-review/kp-17592186054814/slot-{len(seq)}');seq.append(chosen);pool=[q for q in pool if q['id']!=chosen]
assert len(set(seq))==len(candidates)
save('selection-results.json',{'command':'python3 -B variation_review.py','implementation_sha256':hashlib.sha256((REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'learning_caller_sha256':hashlib.sha256((REPO/'engine/rust/learning.rs').read_bytes()).hexdigest(),'basis':inv['basis'],'rules':'BTreeSet sorted unique entity IDs. Caller removes seen questions and invalid practice questions. Weighted band drawn first, then uniform within-band by SHA256 seed. All rated candidates here are easy: positive easy weight gives uniform easy support. Unrated archival sqrt(121) is fallback only if no weighted rated candidate. Without configured weights minimum entity is chosen; seen history then excludes it.','conditions':'No publication or live learner policy/history. These explicit no-history, leave-one and prefix-history scenarios examine support under any positive easy weight. Synthetic appended IDs preserve ordinal order; exact future draw IDs cannot be claimed.','candidates':candidates,'seed_pattern':'task-review/kp-17592186054814/slot-{0..63}','no_history_selected_ids':selected_ids,'prefix_history_sequence':seq,'sole_fresh_cases':sole,'no_policy_sequence':[q['id'] for q in candidates],'zero_easy_weight':'Only unrated archival fallback can survive; no claim such weights are configured.'})
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-analysis.json',{'basis':inv['basis'],'total_questions':len(inv['questions']),'original_source_questions':sum(bool(q.get(':question/math-academy-id')) for q in inv['questions']),'other_records':[{ 'id':q[':question/id'],'entity_id':q[':db/id'],'problem':q[':question/problem']} for q in inv['questions'] if not q.get(':question/math-academy-id')],'assessment':'All captured prompts/provenance inspected. Retained defects were missing source replay/family support, not wrong stored keys. No stored instance of either coverage defect demonstrated. All eight source questions remain originals. Five other records are fractions 56/7 and 34/3, decimals -6.20 and -12.00, and pi. None is a negative nonsquare or omitted radio replay generated record.','limits':'Captured inventory has no generation metadata, so no historical generation-seed claims. Empty affected list is verified only for the specific retained defects, not a full inventory audit of all possible weaknesses.'})
# Counterfactual results are tied to actual grader and UI outputs, not only metadata.
grader=load('grader-results.json');by_label={x['label']:x for x in grader['records']}
cf=[]
for p in load('counterfactual-results.json'):
 gr=by_label[p['cross_submission_grader_label']];got=collections.Counter(c['outcome'] for c in gr['checks'])
 expected_changed=len(set(p['expected_before'])^set(p['expected_after']));assert got['rejected']==expected_changed and got['accepted']==5-expected_changed
 cf.append({'kind':p['kind'],'change':p['change'],'expected':p['expected_before']+' -> '+p['expected_after'],'observed':p['observed_before']+' -> '+p['observed_after']+'; prior response cross-submission: '+json.dumps(dict(got))+'; actual UI displays changed values, checked memberships and exact worked equalities.','status':'passed','justification':'Source negative nonsquare and square roots demonstrate nonzero imaginary classification; positive roots depend on perfect-square status. Sign of noninteger rationals and magnitude within nonreal roots preserve membership; exact imaginary coefficients must still change.','sample_refs':['controlled-records.json','counterfactual-results.json','grader-input.json','grader-results.json','render-records.json','render/rendering.json']})
a={'learner_operation':'Classify the displayed number by mathematical value, after at most one elementary fraction/root simplification, then determine every containing set in N subset Z subset Q subset R subset C; N excludes zero.',
 'fixed_features':[{'feature':'Five basic containing sets and their definitions','justification':'Introduction tutorial 2d61ed1f-938f-51f3-8f72-19f2a9db35ea defines the sets and excludes zero from N; all supplied questions classify one given value.'},{'feature':'C always qualifies','justification':'All real and nonreal numbers in the lesson are complex. Necessary mathematical inclusion; no source assignment permits excluding C.'},{'feature':'One number and elementary simplification, easy difficulty','justification':'Canonical 3.25 and source -27/3, sqrt(121), sqrt(-2) establish recognition or one short simplification.'},{'feature':'Ordinary generation uses five checkbox fields; radio banks archival','justification':'Five Boolean choices directly express the original select-all contract. Previously reviewed presentation remains; all three complete source radio banks are now faithfully replayed. No random radio-family coverage claim.'}],
 'answer_roles':[{'role':'Smallest containing set and consequent selection count','eligible_variation':'N, Z, Q, R or C may be the smallest containing set. Assignments derive from the value, never bank position or label arrangement.','observed':'All five masks survive in fresh delivered sample. Exact delivered batch contains N twice, R once, C once; no tested complete-answer positional or label-mask cue solves the batch.'},{'role':'Representation and answer-bearing value properties','eligible_variation':'Integers may be positive/nonpositive; fractions and decimals integral/nonintegral; radicals zero, positive square/nonsquare or negative. Negative radicands need not have square magnitude.','observed':'144/144 changed negative values construct and sample correctly; visible coefficients squared independently. Fresh multi-family regression and controlled roots show relevant class changes. Pi/negative roots have necessary fixed classifications.'},{'role':'Field order and complete radio choice identity','eligible_variation':'Checkbox order may change independently of value. Archival radio key follows complete containing-set list instead of longest option or fixed index.','observed':'Exhausted 31 fixed positional subsets across each raw/delivered set; none solves a set. Source-index replay and reordered source traversal preserve complete banks, keys and solutions.'}],
 'coverage':[{'case':stage,'sample_refs':[files[stage],'coverage-results.json'],'result':json.dumps({k:v for k,v in x.items() if k!='records'})} for stage,x in coverage.items()]+[{'case':'negative radical bounded domain','sample_refs':['negative-records.json','negative-domain-results.json'],'result':'All -144..-1 supported in construction and forced sampler; exact visible imaginary coefficient witnesses pass; ordinary fresh sample also exercises negative nonsquares.'},{'case':'all source radio banks and inferred legacy gap','sample_refs':['source-replay-records.json','source-replay-results.json'],'result':'All eight supplied sources replay. Complete banks, response types, available keys and available solutions match. Missing sqrt(121) key/solution are inferred and documented, not claimed as captured.'}],
 'counterfactuals':cf,'shortcut_probes':probes,
 'delivery':{'stages_examined':['generator class-first sampling, unique-TeX rejection/resampling and nonempty-checkbox wrapper','actual shared prepare_records normalization and validation','captured inventory and within-batch deduplication','requested easy difficulty filtering','learner selection weighted bands, sorted candidate IDs, seen/history exclusion and unrated fallback; conditional read-only reproduction'], 'sample_refs':['packaging-results.json','delivery-sample/delivery.json','delivery-batch/delivery.json','delivery-transformation-results.json','coverage-results.json','selection-results.json','inventory-analysis.json'], 'result':'Fresh sample 40->38 retains all five masks. Actual runner batch 5->4 removes stored -5, leaving C=1, NZQRC=2, RC=1; labels/positions/counts do not provide a complete-answer bypass. Semantic answers and solution math preserved by normalization. Every accepted batch candidate has support in positive-easy-weight no-history and leave-one/prefix scenarios. Exact future policy/history distribution is not claimed.'},
 'limitations':['Finite independent sample and enumerated simple cue strategies do not prove absence of every possible shortcut.','Captured inventory basis 5455 may later change. No publication preparation exists; actual read-only delivery adapter used instead.','Live learner policy/history are absent. Selection examined conditionally with explicit histories and weights; exact future entity IDs are unknown.','Source sqrt(121) has no captured key/solution/difficulty; canonical example has no answer fields. Their mathematical implications were checked independently.']}
save('pedagogical-variation.json',a)
save('scope-results.json',{'result':'Easy single-value membership classification preserved. Changed negative nonsquare roots directly source-supported; exact sqrt(m)i is sufficient without extra factor extraction. All five basic sets retain their source definitions. No new operators, target sets, prerequisites or multi-step workload observed.','source_refs':['5356b463-f0e3-5b2b-9ffc-35df47ad119b','Introduction 2d61ed1f-938f-51f3-8f72-19f2a9db35ea'],'sample_files':['sample-records.json','controlled-records.json','negative-records.json']})
(R/'session-state.md').write_text('All mathematical, source, runtime, grader and actual renderer checks pass. Source fidelity regression fixes verified against earlier failing package. Fresh sample 40->38 retains five masks; exact batch 5->4 retains C,N,R; positional/label/count probes and five counterfactual pairs saved. Conditional learner selection and captured inventory analyzed; no affected stored instance of retained defects. Screenshots inspected for changed negative roots, controlled changes and all radio banks. Remaining: evidence schema/path validation, package unchanged confirmation and final report.\n')
print(json.dumps({'coverage':{k:{'count':v['count'],'memberships':v['memberships'],'representations':v['representations']} for k,v in coverage.items()},'probes':len(probes),'conditional_selection_candidates':len(candidates),'pairs':len(cf)},indent=2))
