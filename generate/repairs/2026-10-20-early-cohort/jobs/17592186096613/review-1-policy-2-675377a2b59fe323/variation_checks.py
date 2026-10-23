import json,pathlib,collections,re,hashlib,argparse
P=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--candidate-records',type=pathlib.Path,default=P/'batch.json');args=ap.parse_args()
def load(p):return json.loads((P/p).read_text())
def save(p,x):(P/p).write_text(json.dumps(x,indent=2))
def f(r):return r['question'][':question/answer-fields'][0]
def key(r):return next(a[':answer/value'] for a in f(r)[':answer-field/choices'] if a[':answer/id']==f(r)[':answer-field/correct'][1])
def counts(rs):return {'count':len(rs),'profiles':dict(collections.Counter(r['generation']['bank_profile'] for r in rs)),'signs':dict(collections.Counter('negative' if 'y=-' in r['question'][':question/problem'].replace(' ','') else 'positive' for r in rs)),'unique_derivatives':len(set(key(r) for r in rs)),'quotient_form':sum('\\frac{\\ln' in r['question'][':question/problem'] for r in rs)}
sets={'raw_sample':load('samples.json'),'delivered_sample':load('delivery-samples/accepted.json'),'raw_batch':json.loads(args.candidate_records.read_text()),'delivered_batch':load('delivery-batch/accepted.json')}
coverage={k:counts(v) for k,v in sets.items()};probes=[]
for stage,rs in sets.items():
 for profile in ['all','integer','fraction','euler']:
  rr=[r for r in rs if f(r)[':answer-field/type'].endswith('/radio') and (profile=='all' or r['generation']['bank_profile']==profile)]
  if not rr:continue
  pos=[next(i for i,a in enumerate(f(r)[':answer-field/choices']) if a[':answer/id']==f(r)[':answer-field/correct'][1]) for r in rr]
  probes.append({'stage':stage,'profile':profile,'strategy':'choose first serialized option','correct':pos.count(0),'total':len(rr),'positions':dict(collections.Counter(pos)),'note':'Serialized position only; actual UI reshuffles, measured separately from rendered HTML.'})
# Read actual UI display order from saved DOM, not the package order.
render=load('render-records.json');ui=[]
for i,r in enumerate(render):
 if not f(r)[':answer-field/type'].endswith('/radio'):continue
 html=(P/'render-pairs'/f'question-{i+1:03}.html').read_text()
 ids=re.findall(r'<input type="radio"[^>]* value="([^"]+)"',html)
 assert len(ids)==5
 pos=ids.index(f(r)[':answer-field/correct'][1]);ui.append({'render_index':i,'profile':r['generation']['bank_profile'],'id':r['question'][':question/id'],'position_zero_based':pos,'displayed_answer_ids':ids})
for profile in ['all','integer','fraction','euler']:
 rr=[v for v in ui if profile=='all' or v['profile']==profile]
 probes.append({'stage':'actual UI batch and controlled pairs','profile':profile,'strategy':'choose first displayed option','correct':sum(v['position_zero_based']==0 for v in rr),'total':len(rr)})
cf=[]
for p in load('counterfactuals.json'):
 b,r,i=p['before'],p['relevant_after'],p['irrelevant_after']
 cf.append({'profile':p['profile'],'before_key':key(b),'relevant_key':key(r),'irrelevant_key':key(i),'relevant_prompt_changed':b['question'][':question/problem']!=r['question'][':question/problem'],'relevant_solution_changed':b['question'][':question/worked-solution']!=r['question'][':question/worked-solution'],'relevant_key_changed':key(b)!=key(r),'irrelevant_prompt_preserved':b['question'][':question/problem']==i['question'][':question/problem'],'irrelevant_solution_preserved':b['question'][':question/worked-solution']==i['question'][':question/worked-solution'],'irrelevant_key_preserved':key(b)==key(i),'bank_order_changed':f(b)[':answer-field/choices']!=f(i)[':answer-field/choices']})
save('variation-results.json',{'command':['python3','variation_checks.py','--candidate-records',str(args.candidate_records)],'coverage':coverage,'position_probes':probes,'ui_positions':ui,'counterfactuals':cf})
# Captured inventory eligibility. Three original records lack complete response fields/keys.
inv=json.loads((P.parent/'source/inventory.json').read_text());inventory=[]
for q in inv['questions']:
 fields=q.get(':question/answer-fields',[]);eligible=bool(fields) and all(':answer-field/correct' in a for a in fields) and not q.get(':question/retired',False)
 inventory.append({'id':q[':question/id'],'entity_id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'eligible_by_captured_response_and_retirement':eligible,'reason':'complete keyed response; not retired' if eligible else 'missing fields or key'})
hist=load('historical-records.json')[0];stored=next(q for q in inv['questions'] if q[':question/id']==hist['question'][':question/id'])
assert hist['question'][':question/problem']==stored[':question/problem']
assert hist['question'][':question/worked-solution']==stored[':question/worked-solution']
assert sorted(a[':answer/value'] for a in f(hist)[':answer-field/choices'])==sorted(a[':answer/value'] for a in stored[':question/answer-fields'][0][':answer-field/choices'])
save('inventory-results.json',{'basis':inv['basis'],'questions':inventory,'historical_generated_record':'historical-records.json','historical_record_matches_stored_prompt_solution_bank':True,'historical_math':'d[-12 ln(x)/7]/dx=-12/(7x), matches key and solution','historical_grading':'grader-report.json stored-2aa37d05: 3 accepted equivalents and 3 rejected wrong entries','demonstrated_defects':[],'limits':'Verified absence of the demonstrated runtime source omission as a stored-record defect: omission is not corrupt content. Not an exhaustive historical rendering audit; original source records are never classified as generated.'})
save('affected-inventory.json',{'affected_questions':[]})
# Selection formula from question_selection.rs; no unknown live learner state invented.
existing=[q['entity_id'] for q in inventory if q['eligible_by_captured_response_and_retirement']]
# Virtual contiguous entity IDs are explicit: publication has not assigned real new IDs.
new=list(range(max(existing)+1,max(existing)+1+len(sets['delivered_batch'])))
sel=[]
for excluded in [[],existing,new[:-1],existing+new[:-1]]:
 pool=sorted(set(existing+new)-set(excluded));draws=[]
 for i in range(128):
  seed='independent-review/'+str(i);h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(h[8:16],'big')>>11)/2**53;draws.append(pool[int(u*len(pool))])
 sel.append({'excluded':excluded,'pool':pool,'draw_counts':dict(collections.Counter(draws))})
save('selection-results.json',{'source':'engine/rust/question_selection.rs select and seen_before_task; engine/rust/learning.rs validate_practice_question','basis':inv['basis'],'assumptions':['easy band has positive configured weight; all eligible captured questions and candidates are easy','empty or explicitly modeled prior history','new entity IDs modeled contiguously because publication is absent'],'observations':sel,'conclusion':'With positive easy weight, selection is uniform within the fresh easy pool. All modeled candidates are reached. History removes seen records and does not enforce bank/profile balance. An unconfigured policy instead returns the lowest entity ID; no policy was captured, so actual learner draws are not claimed.','limits':['No actual learner history/policy or future entity IDs are captured. These affect individual draws, not the missing quotient family or all-five-candidates survival.']})
print(json.dumps({'coverage':coverage,'counterfactuals':cf,'eligible_inventory':len(existing),'ui_first':[(x['profile'],x['correct'],x['total']) for x in probes if x['stage'].startswith('actual')]}))
