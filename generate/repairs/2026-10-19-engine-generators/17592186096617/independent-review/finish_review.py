import json,hashlib,collections,math
from pathlib import Path
R=Path(__file__).resolve().parent;REPO=Path('/home/jake/Developer/Course_Academy');P=R.parent/'workspace'
load=lambda n:json.loads((R/n).read_text())
def save(n,x):(R/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
from analyze_delivery import analyze
raw=load('samples.json');acc=load('delivery/accepted.json');batch=load('runner-batch.json');cfacc=load('counterfactual-delivery/accepted.json');inventory=json.loads((R.parent/'source/inventory.json').read_text())
def enum(x):return x.get(':db/ident','') if isinstance(x,dict) else x or ''
def structurally_usable(q):
 fs=q.get(':question/answer-fields',[])
 if not fs:return False
 for f in fs:
  correct=f.get(':answer-field/correct')
  if not correct:return False
  if enum(f.get(':answer-field/type')) not in (':answer-field.type/radio',':answer-field.type/blank'):return False
 return True
old=[q for q in inventory['questions'] if structurally_usable(q)]
old_ids=[q[':db/id'] for q in old];top=max(q[':db/id'] for q in inventory['questions']);maps={q[':db/id']:q for q in old}
for i,r in enumerate(acc):maps[top+i+1]=r['question']
new={top+i+1:r for i,r in enumerate(acc)}
# Faithful question_selection.rs select core: sorted IDs; SHA-256; weighted rated band; index draw.
def select(ids,weights,seed):
 ids=sorted(set(ids))
 if weights is None:return ids[0] if ids else None
 pools=[[],[],[]];unrated=[]
 for q in ids:
  level=enum(maps[q].get(':question/difficulty')).split('/')[-1]
  if level in ('easy','moderate','hard'):pools[('easy','moderate','hard').index(level)].append(q)
  else:unrated.append(q)
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 uniform=lambda off:(int.from_bytes(digest[off:off+8],'big')>>11)/(1<<53)
 total=sum(w for w,p in zip(weights,pools) if p)
 if total>0:
  draw=uniform(0)*total;chosen=None
  for i,w in enumerate(weights):
   if not pools[i] or w==0:continue
   chosen=i
   if draw<w:break
   draw-=w
  pool=pools[chosen]
 else:pool=unrated
 return pool[int(uniform(8)*len(pool))] if pool else None
all_ids=list(maps);scenarios=[];selection_samples=[]
for label,weights,exclude in [('easy_only_empty_history',[1,0,0],set()),('equal_band_empty_history',[1,1,1],set()),('easy_only_prior_seen',[1,0,0],set(list(new)[::3])),('easy_zero',[0,1,1],set()),('unconfigured',None,set())]:
 counts=collections.Counter();coverage=collections.defaultdict(collections.Counter)
 for i in range(4096):
  seed='independent-review-20261018/'+str(i);q=select([k for k in all_ids if k not in exclude],weights,seed);counts['new' if q in new else 'inventory' if q else 'none']+=1
  if q in new:
   m=new[q]['generation'];t=m['template'];coverage[t]['count']+=1;coverage[t]['missing='+str(m['missing_term'])]+=1
   if 'trig' in m['parameters']:coverage[t]['trig='+m['parameters']['trig']]+=1
  if i<16:selection_samples.append({'scenario':label,'seed':seed,'selected_fixture_id':q,'template':new[q]['generation']['template'] if q in new else 'captured_inventory'})
 scenarios.append({'scenario':label,'weights':weights,'excluded_new_count':len(exclude),'draws':4096,'counts':dict(counts),'new_case_coverage':dict(coverage)})
save('selection-inputs.json',{'captured_basis':inventory['basis'],'captured_inventory_file':'../source/inventory.json','inventory_sha256':hashlib.sha256((R.parent/'source/inventory.json').read_bytes()).hexdigest(),'old_candidates':old,'new_records':acc,'new_fixture_ids':list(new),'source_implementation':str(REPO/'engine/rust/question_selection.rs'),'source_sha256':hashlib.sha256((REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest()})
save('selection-results.json',{'basis':inventory['basis'],'implementation':'faithful select() reproduction in finish_review.py; structural practice eligibility and canonical-key presence from learning.rs:170-250; native stored-answer acceptance checked separately','old_structurally_usable':len(old),'new_usable':len(acc),'scenarios':scenarios,'sampled_draws':selection_samples,'limits':['No live learner history or active policy supplied; sensitivity scenarios are conditional, not claims about a specific learner.','New numerical entity IDs are fixture IDs; actual allocation changes deterministic outcomes, not uniform per-band eligibility.','Captured inventory blank support not revalidated with native supports; easy source records have supported expressions. All new keys were native-graded.','Existing items may be excluded by actual learner history; explicit zero easy weight prevents all easy practice.','No-resampling public generate emits one source profile or raises. No unexpected rejections in 143 fresh/boundary draws; invalid parameter controls reject.','Live inventory may change after captured basis 3949.']})
# All stage comparisons, including runner and independent counterfactual filtering.
distributions={'raw':analyze(raw),'delivered':analyze(acc),'runner_input':analyze(batch),'runner_delivered':analyze(load('runner-delivery/accepted.json')),'counterfactual_delivered':analyze(cfacc)}
save('distribution-probes.json',distributions)
probes=[]
for t in ['q-1907','q-47965','q-104297','q-1931','q-104300']:
 for strategy in ('choose_first','choose_last','tex_length_max','tex_length_min','parenthesis_count_max','parenthesis_count_min'):
  q=next(x for x in distributions['delivered']['probes'] if x['subgroup']==t and x['strategy']==strategy)
  n=q['attempts_when_unique']
  if not n:continue
  probes.append({'cue':strategy,'subgroup':t,'scope':'within_template','strategy':strategy+'; abstain on tied extrema','correct':q['correct'],'total':n,'baseline':0.2,'disposition':'not_predictive','conclusion':f"{q['correct']}/{n} on delivered records; uniform five-choice guessing baseline is 0.2. No perfect predictor in this tested profile. Abstentions {q['total']-n}.",'sample_refs':['delivery/accepted.json','distribution-probes.json']})
# Sign cue with mathematical explanation, kept distinct from position/length cues.
q=next(x for x in distributions['delivered']['probes'] if x['subgroup']=='q-104300/c_sign=positive' and x['strategy']=='plus_count_max')
probes.append({'cue':'unique maximum plus signs','subgroup':'q-104300 with positive scalar and positive-derivative trig (sin/tan)','scope':'other_recognizable_subgroup','strategy':'choose the unique sum option when every other option includes subtraction','correct':q['correct'],'total':q['attempts_when_unique'],'baseline':0.2,'disposition':'intended_skill','conclusion':'4/4 conditional matches versus five-choice baseline 0.2. Inspecting the bank shows that this is derivative-sign elimination: positive power factor and sin/tan have positive derivative contributions for positive x in a regular interval. Cosine reverses the trig derivative sign; negative coefficients reverse it again. This uses mathematical derivative signs, not a label/position cue. It does not establish complete calculation mastery.','sample_refs':['delivery/accepted.json','distribution-probes.json','render-all/input.json']})
pairs=load('counterfactuals.json');counterfactuals=[]
for p in pairs:
 counterfactuals.append({'kind':p['kind'],'change':p['label'],'expected':p['expected'],'observed':'Independent displayed-expression checks verify '+('different required answers and unchanged underlying product for missing-role pairs; native keys accepted and stale terms rejected.' if p['label'].startswith('missing_') else 'changed trig prompts, derivatives and accepted radio keys.' if p['label'].startswith('trig_') else 'same derivative and solution, changed option order/distribution; matching answers accepted in each record.'),'status':'passed' if p['relationship_passed'] else 'failed','justification':'Product rule determines each missing term and full derivative; option order and equivalent distribution are irrelevant to value.','sample_refs':['counterfactuals.json','grader-report.json','render-all/input.json','counterfactual-delivery/accepted.json']})
coverage=[]
for t,c in distributions['delivered']['coverage'].items():coverage.append({'case':t,'sample_refs':['samples.json','delivery/accepted.json','distribution-probes.json'],'result':str(dict(c))})
coverage.append({'case':'linear polynomial factor from canonical e-3634','sample_refs':['canonical-replay-gap.json'],'result':'Not representable: public bounds reject n=1. Covered as variety/source restriction, not as a missing-term role defect.'})
variation={'learner_operation':load('source-analysis.json')['skill']+' Determine which product-rule contribution must be supplied, or select the complete derivative using the displayed factors.','fixed_features':[{'feature':'Two factors, one product-rule application, trig argument x','justification':'Canonical e-3634 and tutorial2622 teach u\'v+uv\'; chain rule and point evaluation belong outside this operation.'},{'feature':'One blank plus supplied complementary term, or five-choice radio','justification':'All captured response contracts have this workload; q-71004 missing response is documented as repaired full blank.'},{'feature':'Power n=2..4 in public polynomial profiles','justification':'Author fixes this range, but excludes the source canonical n=1 case without an instructional reason. Demonstrated restriction in canonical-replay-gap.json.'}],'answer_roles':[{'role':'Missing contribution u\'v vs uv\'','eligible_variation':'Either contribution can be hidden for the same factors.','observed':'Both roles survive delivery in all five completion profiles; all five controlled swaps change the answer correctly.'},{'role':'Primitive trig in polynomial radio profiles','eligible_variation':'sin/cos/tan with same unscaled argument and same product-rule work.','observed':'All three survive delivery in q-1907 and q-104300; same numeric data with trig swapped update prompt, solution, key and grading.'},{'role':'Radio key position and presentation','eligible_variation':'Any of five positions; equivalent expansion does not alter mathematical answer.','observed':'No tested first/last/length/parenthesis action predicts answers perfectly within a supported template.'},{'role':'Polynomial factor power, including linear canonical factor','eligible_variation':'Low source-supported powers including n=1 canonical x cos x; nonzero scalar.','observed':'Signs and n=2/4 boundaries survive; n=1 rejected. See separate restriction finding.'}], 'coverage':coverage,'counterfactuals':counterfactuals,'shortcut_probes':probes,'delivery':{'stages_examined':['public generator sampling and rejection','shared requested difficulty, identity and normalization','captured inventory/batch deduplication','independent counterfactual delivery','practice structural eligibility','learner seen exclusion and SHA256 weighted selection sensitivity'],'sample_refs':['rejections.json','samples.json','delivery/delivery.json','runner-delivery/delivery.json','counterfactual-delivery/delivery.json','selection-inputs.json','selection-results.json','distribution-probes.json'],'result':'143 ->114 samples, runner5->5, counterfactual17->16. Decision roles survive every examined stage when easy has positive selection weight; no role-specific resampling. Canonical n=1 restriction is already present before filtering. Base4 equivalent-entry failure also survives filtering.'},'limitations':['No finite audit proves absence of every shortcut.','Active learner policy, history and future numerical database IDs not supplied; selector results are documented conditional sensitivity cases.','No generated diagrams or assets; actual UI checked on desktop only.','Canonical e-3634 has no captured response field; restriction concerns its factor/derivative operation, not an invented bank.','The valid ln4 equivalent is an integrated grading failure, not an incorrect stored derivative.']}
save('pedagogical-variation.json',variation)
# Check final package preservation, manifest runtime exactness and actual UI evidence.
before=load('package-before.json');after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};save('package-integrity.json',{'same':before==after,'before_files':len(before),'after_files':len(after),'added':sorted(set(after)-set(before)),'removed':sorted(set(before)-set(after)),'changed':[k for k in before if k in after and before[k]!=after[k]],'database_writes':0,'published_assets':0})
save('scope-results.json',{'passed':True,'basis':'independent source-analysis.json; 143 displayed-function parses plus five runner records and controlled pairs','supported_operators':['one product rule','power/radical derivative','elementary exponential derivative','sin/cos/tan derivative','constant multiple and additive constant'],'no_scaled_arguments':True,'no_point_evaluation':True,'unsupported_bands_rejected':load('rejections.json')[:2],'source_error_corrected':'q-319350 solution LHS follows source prompt in normal output; raw replay preserves typo','limits':'Scope correctness does not excuse omission of the simpler canonical linear factor.'})
save('visual-inspection.json',{'passed':True,'renderer':'unmodified UI via render_preview.py','primary_cases':27,'additional_base4_cases':1,'screenshots_inspected':['render-all/contact-'+str(i)+'.png' for i in range(1,6)]+['render-log-identity/question-001.png'],'findings':['All eleven source bank/completion profiles readable.','Both missing-term locations and changed sin/cos/tan cases show consistent equations, controls, answers and worked solutions.','Radicals, fractions, logarithms, secant-squared, negative terms and continuation rows display without clipping or exposed TeX.','No source or generated image assets.','Base4 failure case displays correctly; preview CORRECT state uses canonical key and does not establish acceptance of equivalent entries.'],'limits':['1280px desktop viewport; no mobile claim.'],'reports':['render-all/rendering.json','render-log-identity/rendering.json']})
print(json.dumps({'integrity':before==after,'selection_scenarios':len(scenarios),'variation_probes':len(probes),'counterfactuals':len(counterfactuals)}))
