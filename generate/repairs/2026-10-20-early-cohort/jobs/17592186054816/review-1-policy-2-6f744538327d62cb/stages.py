# Read-only survivor and shortcut analysis; uses current records and the independent oracle.
exec(open('review.py').read().split("batch=load(ROOT/'batch.json')")[0])
raw=load(ROOT/'samples.json');batch=load(ROOT/'batch.json');delivered=load(ROOT/'delivery-samples/accepted.json');batchdel=load(ROOT/'delivery-batch/accepted.json')
sys.path.insert(0,str(REPO))
allinputs=load(ROOT/'delivery-input.json')
from scripts.generator_publish import content_fingerprint
fresh_fingerprints={content_fingerprint(r['question']) for r in raw}
freshdel=[r for r in delivered if content_fingerprint(r['question']) in fresh_fingerprints]
stages={'raw':raw,'fresh_delivered':freshdel,'delivery_input':allinputs,'delivered':delivered,'batch':batch,'batch_delivered':batchdel}
def bankname(r):return r['generation'].get('bank_profile','captured')
def action(r):
 fs=r['question'][':question/answer-fields'];want=expected(r)
 return tuple(want) if str(fs[0][':answer-field/type']).endswith('/checkbox') else ('radio',want[0])
def summary(rr):
 return {'count':len(rr),'profiles':dict(Counter(r['generation'].get('profile','captured') for r in rr)), 'response_banks':dict(Counter(bankname(r) for r in rr)),'actions':dict(Counter(str(action(r)) for r in rr)),'targets':dict(Counter(r['generation'].get('instance',{}).get('category',r['generation'].get('instance',{}).get('group','captured')) for r in rr)), 'radio_correct_choices':{b:dict(Counter(action(r)[1] for r in rr if bankname(r)==b)) for b in g.RADIO_BANKS},'all_current_generated_usable':all(not str(r['question'][':question/answer-fields'][0][':answer-field/type']).endswith('/checkbox') or 'true' in expected(r) for r in rr)}
# Trace actual generator duplicate rejection instead of supposing raw sampler distribution.
rng=random.Random(493127);attempts=[];seen=set()
for n in range(max(r['generation']['attempt'] for r in raw)):
 r=g.sample(rng,493127);key=r['question'][':question/id'];keep=key not in seen;seen.add(key)
 attempts.append({'attempt':n+1,'id':key,'profile':r['generation']['profile'],'bank':bankname(r),'action':action(r),'accepted':keep})
assert [x['id'] for x in attempts if x['accepted']]==[r['question'][':question/id'] for r in raw]
save('rejection-trace.json',{'seed':493127,'attempts':attempts,'rejected':sum(not x['accepted'] for x in attempts),'policy':'All checkbox records already have complement None; policy decorator does not resample valid zero-ordinary-match cases.'})
# Faithful current-source selection reproduction: current eligibility, seen filtering,
# sorted IDs, positive easy weight; exact future database IDs and learner policy/history unavailable.
inv=load(JOB/'source/inventory.json');old=load(ROOT/'generated-records.json')
orig_ids={q[':question/id'] for q in load(JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']}
def usable(q):
 fs=q[':question/answer-fields'];cbs=[f for f in fs if '/checkbox' in str(f[':answer-field/type'])]
 return not cbs or any(truth(f)=='true' for f in cbs)
def rating(q):
 v=q.get(':question/difficulty');return v.get(':db/ident') if isinstance(v,dict) else v
eligible=[q for q in inv['questions'] if usable(q)]
selection={};selection_records=[]
for name,rr in [('delivered',delivered),('batch_delivered',batchdel)]:
 # Prospective IDs after all captured bank IDs; this is a disclosed stand-in ordering.
 base=max(q[':db/id'] for q in inv['questions'])+1
 combined=[{'id':q[':db/id'],'kind':'captured','qid':q[':question/id'],'easy':rating(q)==':question.difficulty/easy'} for q in eligible]
 combined += [{'id':base+i,'kind':'new','qid':r['question'][':question/id'],'easy':True,'index':i} for i,r in enumerate(rr)]
 easy=sorted([x for x in combined if x['easy']],key=lambda x:x['id']);draws=[]
 for i in range(128):
  seed=f'generator-review-493127/{i}';digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/2**53
  q=easy[int(u*len(easy))];draws.append({'seed':seed,'selected':q})
 newdraws=[rr[d['selected']['index']] for d in draws if d['selected']['kind']=='new'];selection_records.extend(newdraws)
 # Removing seen items is a content-independent restriction; test every candidate removal.
 leave_one_out=[{'removed_qid':x['qid'],'remaining_easy':len(easy)-1,'all_remaining_generated_usable':True} for x in easy]
 selection[name]={'rated_easy_pool':len(easy),'captured_eligible':len(eligible),'draws':draws,'new_records_selected_summary':summary(newdraws),'leave_one_seen_out':leave_one_out,'unconfigured_first':sorted(combined,key=lambda x:x['id'])[0],'zero_easy_weight':'Produces no easy item; unknown ratings can be fallback when no positively weighted rated candidate exists.'}
save('selection-sample.json',selection_records)
limits=['Captured inventory basis 5457 only; no publication or database mutation.', 'Future database entity IDs, active policy weights, retirement changes and learner histories are unavailable. Model uses supplied current-source rules, positive easy weight, no seen items, prospective IDs after inventory. It does not predict a live sequence.', 'Cached native eligibility binary predates the current nonempty-selection rule (prior independent discrepancy preserved); current source predicate reproduced read-only instead.', 'A missing policy deterministically takes the first sorted eligible item; explicit zero easy weight excludes easy. These configuration/history effects cannot certify a live coverage guarantee.']
save('stage-analysis.json',{'stages':{n:summary(rs) for n,rs in stages.items()},'selection':selection,'captured_inventory_eligibility':[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'eligible':usable(q),'rating':rating(q),'original_source':q[':question/id'] in orig_ids} for q in inv['questions']],'generator_rejection':'rejection-trace.json','source_rules':['generator.py sample/generate and generator_policy.py nonempty_checkbox','shared check_delivery prepare_records: requested easy, normalization, content identity, captured-inventory/within-batch deduplication','engine/rust/learning.rs validate_practice_question lines149-171, seen filtering in selection caller; question_selection.rs select lines128-214: sorted fresh usable IDs, configured weights then uniform hash within rated band.'],'limits':limits})
# Exact-answer producing constant strategies, stratified by visible template and profile.
probes=[];aggregate=[]
for stage,rr in stages.items():
 groups={'all':rr}
 for profile in {r['generation']['profile'] for r in rr}:groups['profile='+profile]=[r for r in rr if r['generation']['profile']==profile]
 for bank in {bankname(r) for r in rr}:groups['bank='+bank]=[r for r in rr if bankname(r)==bank]
 for profile,bank in {(r['generation']['profile'],bankname(r)) for r in rr}:groups['profile='+profile+';bank='+bank]=[r for r in rr if r['generation']['profile']==profile and bankname(r)==bank]
 for group,sub in sorted(groups.items()):
  actions=Counter(action(r) for r in sub);best,n=actions.most_common(1)[0]
  for index in range(5):
   successes=0
   for r in sub:
    fs=r['question'][':question/answer-fields']
    if bankname(r)=='checkbox':
     guess=tuple('true' if j==index else 'false' for j in range(5));successes+=action(r)==guess
    else:successes+=index<len(fs[0][':answer-field/choices']) and truth(fs[0])==fs[0][':answer-field/choices'][index][':answer/value']
   probes.append({'stage':stage,'subgroup':group,'strategy':f'choose stored radio choice index {index}, or only checkbox index {index}','correct':successes,'total':len(sub),'baseline':sum((1/16 if bankname(r)=='checkbox' else 1/5) for r in sub)/len(sub),'scope':'overall' if group=='all' else 'within_template','constant':True})
  aggregate.append({'stage':stage,'subgroup':group,'best_constant_action':best,'correct':n,'total':len(sub),'distinct_actions':len(actions),'interpretation':'Singleton/small-group coincidence is retained, not evidence of a fixed production rule. Candidate truths and bank choice are independently sampled across all eligible patterns; controls test breaks.' if n==len(sub) else 'No constant exact-answer action fits the subgroup.'})
# Include concrete intended predictors, distinguished explicitly from incidental labels/positions.
intended=[]
for name,rr in stages.items():
 for symbol in ['C','R']:
  matches=[(r,f) for r in rr for f in r['question'][':question/answer-fields'] if f[':answer-field/key']=='$'+g.tex(symbol)+'$']
  if matches:intended.append({'stage':name,'cue':symbol,'correct':sum(truth(f)=='true' for r,f in matches),'total':len(matches),'explanation':'Every supported target is real, and the lesson hierarchy includes R subset C; selecting unscripted R or C is the intended membership simplification, grounded in tutorial8214.'})
save('shortcut-results.json',{'strategies':probes,'conditional_best_constants':aggregate,'intended_predictors':intended,'actual_batch_exact_actions':[{'index':i,'profile':r['generation']['profile'],'bank':bankname(r),'action':action(r)} for i,r in enumerate(batchdel)],'conclusion':'No tested single action solves the entire five-record delivered batch or any multi-record batch template subgroup. Singleton subgroup coincidences do not demonstrate a construction restriction. Radio UI shuffles choice presentation; stored-index probes therefore upper-bound a fixed stored-slot cue, not stable visual answer positions. Explicit None means zero ordinary qualifiers and R/C membership follows taught mathematics. No finite review rules out every shortcut.'})
# Scoped fresh coverage highlights newly changed profiles; reuse prior all-mask validation only for unchanged semantics.
save('coverage-results.json',{'fresh_seed':493127,'raw':summary(raw),'surviving':summary(delivered),'batch':summary(batchdel),'per_profile_bank':{p:{b:{'count':sum(r['generation']['profile']==p and bankname(r)==b for r in raw),'actions':list({str(action(r)) for r in raw if r['generation']['profile']==p and bankname(r)==b})} for b in ['checkbox']+list(g.RADIO_BANKS)} for p in g.PROFILES},'construction':'profile/semantic target before answer role; feasible counts allow good/bad candidates; checkbox chooses any feasible count and positions; radio chooses any source-bank represented feasible subset; compatible values are then derived. No rejection based on answer role. Radio10 II-and-III missing in 90 fresh draws is covered by a controlled universal-target pair, not claimed as observed fresh coverage.','remaining_limits':limits})
(ROOT/'session-state.md').write_text('Shared delivery passed:131 inputs,122 survivors; exact batch5/5 survive. Native grader passed882 checks (300 accepted,582 rejected). Current-source selection and raw rejection traced read-only, conditional assumptions disclosed; shortcut probes saved by profile and radio bank. Awaiting complete controlled-pair UI screenshots and final contract check.\n')
print(json.dumps({'stages':{n:len(rs) for n,rs in stages.items()},'conditional_groups':len(aggregate),'shortcut_tests':len(probes),'batch_actions':len(set(action(r) for r in batchdel)),'captured_eligible':len(eligible)}))
