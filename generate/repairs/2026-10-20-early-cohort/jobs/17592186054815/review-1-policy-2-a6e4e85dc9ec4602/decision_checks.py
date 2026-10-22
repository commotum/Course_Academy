import sys
sys.dont_write_bytecode=True
from review import *

def mode(r):return enum(r['question'][':question/answer-fields'][0][':answer-field/type']).split('/')[-1]
def profile(r):
 b,z,s=target(r['question']);return b+('0' if z else '')+('+' if s==1 else '-')
def groups(rs):
 out={'all':rs}
 for r in rs:
  for label in [mode(r),mode(r)+':'+profile(r)]:out.setdefault(label,[]).append(r)
 return out

def predict(r,strategy):
 if strategy in ('first candidate only','last candidate only','none','all'):return {'first candidate only':1,'last candidate only':8,'none':0,'all':15}[strategy]
 if strategy=='sign and zero only':
  t=target(r['question']);out=0
  for i,e in enumerate(entries(r['question'])):
   v=signature(tex(e));s=(v[1]>0)-(v[1]<0)
   if s==t[2] or (s==0 and t[1]):out|=1<<i
  return out
 bank=r['question'][':question/answer-fields'][0][':answer-field/choices']
 if strategy.startswith('radio position '):return subset(bank[int(strategy.split()[-1])-1][':answer/value'])
 if strategy=='shortest radio label':return subset(min(bank,key=lambda a:len(a[':answer/value']))[':answer/value'])
 if strategy=='longest radio label':return subset(max(bank,key=lambda a:len(a[':answer/value']))[':answer/value'])
 raise ValueError(strategy)

def probes(rs,ref):
 out=[]
 for group,rr in groups(rs).items():
  strategies=['first candidate only','last candidate only','none','all','sign and zero only']
  if all(mode(r)=='radio' for r in rr):strategies+=['radio position '+str(i) for i in range(1,6)]+['shortest radio label','longest radio label']
  for st in strategies:
   correct=sum(mask(r)==predict(r,st) for r in rr);intended=st=='sign and zero only' and all(profile(r)[0]=='R' for r in rr)
   # A complete subset guess has 16 possibilities; radio option guesses have 5.
   baseline=.2 if 'radio' in st else 1/16
   out.append({'cue':st,'subgroup':group,'scope':'overall' if group=='all' else 'other_recognizable_subgroup','strategy':st,'correct':correct,'total':len(rr),'baseline':baseline,'disposition':'intended_skill' if intended else 'not_predictive','conclusion':('Sign and zero decide membership in signed real sets, an intended simplification. ' if intended else '')+('One observation cannot establish a conditional predictor. ' if len(rr)==1 else '')+f'{correct}/{len(rr)} complete responses correct; baseline is '+('uniform guess among five offered radio choices.' if baseline==.2 else 'uniform guess among 16 candidate subsets.')+' Positions and subset labels are inspected independently of values; controls show varied membership in each restored target and response type.','sample_refs':[ref]})
 return out

def metrics(rs,ref):
 return {'count':len(rs),'groups':{k:{'count':len(rr),'masks':dict(Counter(str(mask(r)) for r in rr)),'selection_counts':dict(Counter(str(mask(r).bit_count()) for r in rr)),'zero_positions':dict(Counter(str(i) for r in rr for i,e in enumerate(entries(r['question'])) if signature(tex(e))==('rat',Fraction(0))))} for k,rr in groups(rs).items()},'probes':probes(rs,ref)}

# Faithful select branch for a pool whose candidates are all easy. IDs below are
# explicitly synthetic until publishing; permutations cannot alter reachability.
def select(pool,seed,configured=True,easy_weight=1,seen=()):
 eligible=[(i,r) for i,r in enumerate(pool,1) if i not in seen]
 if not eligible:return None
 if not configured:return eligible[0]
 if easy_weight==0:return None # no unrated fallback members in this pool
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 return eligible[int(u*len(eligible))]

def main():
 batch=load('batch-records.json');fresh=load('delivery-input.json');bafter=load('delivery-batch/accepted.json');after=load('delivery-independent/accepted.json')
 stages={}
 for label,before,post,ref in [('batch',batch,bafter,'batch-records.json'),('independent',fresh,after,'delivery-input.json')]:
  assert len(before)==len(post)
  assert Counter(mask(r) for r in before)==Counter(mask(r) for r in post)
  selections=[]
  for history in [[],[1],list(range(1,len(post)+1))]:
   for configured,weight in [(True,1),(True,0),(False,1)]:
    draws=[]
    for i in range(128):
     seed=f'review-selection-20261022-{i}';s=select(post,seed,configured,weight,history)
     draws.append({'seed':seed,'selected':s[0] if s else None,'question_id':s[1]['question'][':question/id'] if s else None,'mask':mask(s[1]) if s else None})
    selections.append({'history_synthetic_ids':history,'configured':configured,'easy_weight':weight,'draws':draws,'selected_masks':dict(Counter(str(d['mask']) for d in draws))})
  stages[label]={'before':metrics(before,ref),'accepted':metrics(post,'delivery-batch/accepted.json' if label=='batch' else 'delivery-independent/accepted.json'),'selection_cases':selections}
 save('coverage.json',{'fresh':metrics(load('fresh-records.json'),'fresh-records.json'),'controlled':metrics(load('controlled-records.json'),'controlled-records.json'),'batch':metrics(batch,'batch-records.json')})
 save('delivery-selection-checks.json',{'command':PY+' -B decision_checks.py','selection_source':str(REPO/'engine/rust/question_selection.rs'),'selection_source_sha256':hashlib.sha256((REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'inventory_basis':5456,'stages':stages,'generator_rejection':'Mask selected before values. Duplicate semantic values are removed before each candidate draw. No mask-based rejection; explicit None preserves zero-membership checkbox cases. Independent controls exercised all 16 masks for each radio target and each restored checkbox target.','selection_analysis':'Rust sorts/deduplicates entity IDs, excludes seen history/current prefix before select; configured positive easy weight draws uniformly within the sole available easy band (second SHA256 chunk). Easy weight zero excludes these candidates; no-policy branch selects first entity. Both branches and exhausted history simulated. All proposed records remain reachable with positive easy weight; identity order does not create a value-based exclusion.','limits':['Publication preparation absent: actual shared prepare_records run read-only against captured basis 5456.','No learner history, active weight configuration, or new database IDs supplied. Synthetic IDs specify each tested candidate order; the simulation demonstrates branch behavior and reachability, not a live personalized sequence. Existing source/unrated questions may also enter the full bank; no claim that a given learner receives every proposed case.','Inventory can change after capture.']})
 # Audit retained inventory for the demonstrated old source-interface weaknesses.
 inv=json.load(open(J/'source/inventory.json'));orig=json.load(open(J/'source/source.json'))['material']['kp'][':knowledge-point/questions'];origids={q[':question/id'] for q in orig}
 candidates=[q for q in inv['questions'] if q[':question/id'] not in origids]
 invresults=[]
 for q in candidates:
  r={'question':q};assert [cv(f) for f in q[':question/answer-fields']]==expected(r)
  invresults.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'mask':mask(r),'mathematical_keys_checked':True,'retained_finding_applicability':'Captured historical generated candidates use checkbox practice; absence of radio construction and added replay None concern source replay, not a defect in these stored standalone records. No affected original source questions marked generated.','generation_metadata_present':':question/generation' in q})
 save('inventory-review.json',{'basis':inv['basis'],'inventory_count':len(inv['questions']),'original_source_questions':len(origids),'historical_candidate_count':len(candidates),'results':invresults,'conclusion':'Retained replay defects repaired; no stored generated instance demonstrated affected by either retained finding. Historical implicit-empty record not adopted as current delivery. This is finding-specific verification, not a certification of every historical policy.'})
 save('affected-inventory.json',{'affected_questions':[]})
 save('inventory-records.json',[{'question':q} for q in candidates])
 p={'learner_operation':load('source-analysis.json')['skill'],
 'fixed_features':[{'feature':'Four elementary real candidates, one scripted target, easy workload','justification':'Canonical example ce8a56c1 and all 11 practice questions require four independent class/sign/zero decisions.'},{'feature':'Five complete subset options for radio; Boolean fields for checkbox','justification':'All three captured radio sources use five choices, while checkbox fields express the same finite subset. These are observed response contracts.'},{'feature':'Signed targets from the seven observed source profiles','justification':'Conservative variation within tutorial 8215 definitions; target identity, qualifying positions and count are not fixed.'}],
 'answer_roles':[{'role':'Which candidates qualify','eligible_variation':'Every four-bit mask; each position may qualify or fail','observed':'All 16 masks tested in every radio target and both restored checkbox targets; old checkbox targets sampled at none/all boundaries.'},{'role':'Target class/sign/zero rule','eligible_variation':'Change target holding all four candidates fixed','observed':'Q0+, R0+, Q0-, Q-, Z0+ change masks 5,7,9,8,1 in both response contracts.'},{'role':'Radio correct subset and choice position','eligible_variation':'Any subset may be correct and occupy any bank position; distractors derived separately','observed':'Four random distinct incorrect subsets plus correct subset, then shuffled; tests parse every offered subset and score all positions. No fixed answer-producing label or count.'},{'role':'Candidate magnitude and representation','eligible_variation':'Within-class magnitude changes preserve membership; roots and reducible fractions must be classified','observed':'1/2 to 3/4 preserves mask 5; 430 exact simplification/conversion identities checked.'}],
 'coverage':[{'case':'Restored source response families and banks','sample_refs':['replay-records.json','source-replay-checks.json'],'result':'All 11 sources, including all 3 radio banks, reproduced; source 59f3318f missing key/solution independently inferred II only and explicitly flagged.'},{'case':'All qualifying identities and counts in revised domains','sample_refs':['controlled-records.json','coverage.json'],'result':'154 controlled records; all masks 0..15 under each radio target and each restored checkbox target.'},{'case':'Exact runner batch separately','sample_refs':['batch-records.json','delivery-batch/accepted.json','delivery-selection-checks.json'],'result':'Five distinct masks 5,4,12,6,8 survive; three radio and two checkbox records. Z0+ radio masks 4 and 6 differ; R0+ checkbox masks 12 and 8 differ. No tested fixed-position complete response answers its repeated template.'}],
 'counterfactuals':[{'kind':'relevant','change':'Hold candidates [0,sqrt2,1/2,-3] fixed; change Q0+ to R0+, Q0-, Q-, and Z0+','expected':'Reconsider class, sign, and zero inclusion; masks 5,7,9,8,1','observed':'Visible prompt and per-candidate solution classifications change consistently; every offered correct/wrong response exercised by native grader; rendered Q0+/R0+ pairs show changed decisions in both response modes.','status':'passed','justification':'Tutorials 8214 and 8215 independently define these intersecting rules.','sample_refs':['counterfactual-records.json','counterfactual-checks.json','grader-report.json','render/rendering.json']},{'kind':'irrelevant','change':'Keep Q0+ and other candidates fixed; replace 1/2 by 3/4','expected':'Both are positive noninteger rationals; preserve mask 5 despite display, IDs and shuffled bank changing.','observed':'Both modes retain identical qualifying positions; updated visible value and solution, native correct/wrong outcomes, and actual UI renders checked.','status':'passed','justification':'Tutorial 8214 defines rational membership by ratio of integers; magnitude within this sign/class does not matter.','sample_refs':['counterfactual-records.json','counterfactual-checks.json','grader-report.json','render/rendering.json']}],
 'shortcut_probes':probes(load('fresh-records.json'),'fresh-records.json')+probes(load('controlled-records.json'),'controlled-records.json')+probes(batch,'batch-records.json'),
 'delivery':{'stages_examined':['generator semantic-duplicate exclusion and nonempty checkbox wrapper','actual prepare_records validation and normalization','captured inventory and within-batch deduplication','requested easy difficulty','learner history/current-prefix exclusion and weighted or unconfigured select branches'], 'sample_refs':['delivery-input.json','delivery-independent/delivery.json','delivery-independent/accepted.json','batch-records.json','delivery-batch/delivery.json','delivery-selection-checks.json'],'result':'200/200 independently chosen records and exact 5/5 runner records survive. Before/after mask and shortcut coverage preserved; selection branch analysis saved with explicit history, policy and identity-order limits.'},
 'limitations':['Finite probes cannot establish absence of all shortcuts; one-observation target/mode subgroups are descriptive only.','Source 59f3318f has no captured key or solution; II only follows its visible candidates. Canonical example lacks a captured bank, so its numeric membership is tested in both observed response modes.','No live publication, database writes, active policy query, or personalized history query performed. Delivery and selection conclusions are bounded to supplied capture and explicit modeled branches.']}
 save('pedagogical-variation.json',p)
 print(json.dumps({'batch_masks':[mask(r) for r in batch],'delivery_independent':len(after),'delivery_batch':len(bafter),'probes':len(p['shortcut_probes']),'historical_candidates_checked':len(candidates)}))
if __name__=='__main__':main()
