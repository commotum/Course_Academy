import audit as a
import json,hashlib,collections,re
E=a.E;save=a.save
inv=json.load(open(a.B/'source/inventory.json'));run=json.load(open(E/'delivery-runner/accepted.json'))
# Faithful pure read-only reproduction of select() on one available rated band.
# IDs for prospective records are explicit hypothetical IDs; no EDB allocation occurs.
base={int(q[':db/id']):{'question':q,'kind':'captured inventory'} for q in inv['questions']}
start=max(base)+1
new={start+i:r for i,r in enumerate(run)}
pool={**base,**new}
def select(ids,seed,configured=True,positive_moderate=True):
 ids=sorted(set(ids))
 if not ids:return None
 if not configured:return ids[0]
 if not positive_moderate:return None
 d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=(int.from_bytes(d[8:16],'big')>>11)/2**53
 return ids[int(u*len(ids))]
def stats(records):
 roles=collections.Counter();shapes=collections.Counter();profiles=collections.Counter()
 for r in records:
  if 'generation' in r:
   roles[str(r['generation']['parameters']['answer_role'])]+=1;profiles[r['generation']['template']]+=1
  shapes['vector' if 'then solve' in r['question'][':question/problem'] else 'matrix']+=1
 return {'count':len(records),'answer_roles':dict(roles),'profiles':dict(profiles),'response_shapes':dict(shapes)}
scenarios=[]
for name,seen in [('fresh learner',set()),('source practice previously seen',{q[':db/id'] for q in inv['questions'] if ':question/math-academy-id' in q}),('all captured inventory previously seen',set(base)),('runner prefix excludes first 2 new questions',set(base)|set(list(new)[:2]))]:
 ids=set(pool)-seen;draws=[]
 for trial in range(512):
  seed=f'independent-review/{name}/{trial}';qid=select(ids,seed)
  draws.append({'seed':seed,'selected_entity_id':qid,'question_id':pool[qid]['question'][':question/id']})
 counts=collections.Counter(d['selected_entity_id'] for d in draws)
 scenarios.append({'name':name,'seen_entity_ids':sorted(seen),'candidate_entity_ids':sorted(ids),'configured_weights':[6,3,1],'all_candidates_moderate':True,'draw_count':512,'selected_counts':dict(counts),'new_question_support':{r['question'][':question/id']:counts.get(i,0) for i,r in new.items() if i in ids},'unconfigured_first_question':select(ids,'any',False),'zero_moderate_weight':select(ids,'any',True,False),'draws':draws})
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs select(), seen_before_task(); candidates deduplicated/sorted, history and current prefix excluded, SHA256 stable weighted draw. Only available rated band is moderate, so a positive weight selects uniformly within that band.','captured_basis':inv['basis'],'prospective_ids':{str(i):r['question'][':question/id'] for i,r in new.items()},'scenarios':scenarios,'limitations':['Live learner histories, policy weights and not-yet-assigned database entity IDs are not in the captured inputs. Prospective IDs are explicit modeling parameters, not a claim about future database allocations.','With no configured weights select() chooses the smallest remaining entity ID; an explicit zero moderate weight yields no rated candidate. Neither case creates a bank-label shortcut; generated supply frequency remains policy-dependent.','No live database reads/writes or publication occurred.']})
stages=[]
for stem in ['independent','fresh','runner']:
 raw=json.load(open(E/({'independent':'independent-samples.json','fresh':'fresh-batch.json','runner':'runner-batch.json'}[stem])))
 accepted=json.load(open(E/f'delivery-{stem}/accepted.json'))
 stages.append({'name':stem,'before':stats(raw),'after':stats(accepted),'report':f'delivery-{stem}/delivery.json'})
# Rejection/resampling: inspect and exactly replay bounded duplicate rejection on fresh batch seeds.
seeds=[];seen=set();accepted=[];reject=[]
for i in range(42*20):
 r=a.g.generate(seed=927410+i);m=a.parse_problem(r['question'][':question/problem']);fp=str(m.tolist());seeds.append(927410+i)
 if fp in seen:reject.append({'seed':927410+i,'question_id':r['question'][':question/id']})
 else:accepted.append(r);seen.add(fp)
 if len(accepted)==42:break
save('delivery-coverage.json',{'stages':stages,'sampler':{'command':'generator.batch(count=42, seed=927410)','attempted_seeds':seeds,'rejected_duplicates':reject,'accepted':stats(accepted),'same_records_as_fresh_batch':accepted==json.load(open(E/'fresh-batch.json')),'rule':'at most count*20 attempts; reject repeated underlying augmented matrix; no sign/role rejection or additional numerical rejection; invalid explicit parameter/difficulty requests fail instead of resampling'},'selection_report':'selection-results.json','limits':'Only captured inventory basis 5370; changes after capture are outside these read-only results.'})
print(json.dumps({'stage_counts':[(x['name'],x['before']['count'],x['after']['count']) for x in stages],'sampler_attempts':len(seeds),'sampler_rejected':len(reject),'selection_new_support':[(x['name'],x['new_question_support']) for x in scenarios]}))
