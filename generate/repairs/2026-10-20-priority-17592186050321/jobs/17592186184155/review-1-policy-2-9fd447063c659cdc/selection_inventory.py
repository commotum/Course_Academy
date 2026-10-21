from audit import *
# Exact select() band draw reproduced using the captured rated, usable hard inventory
# and post-filtered generated records. Unknown/incomplete fields are explicitly excluded.
inventory=json.loads((JOB/'source/inventory.json').read_text());replays=json.loads((E/'source-replays.json').read_text())
accepted=json.loads((E/'delivery-sampled/accepted.json').read_text());rb=json.loads((E/'delivery-batch/accepted.json').read_text())
originals=[];excluded=[]
for q in inventory['questions']:
 fs=q.get(':question/answer-fields',[])
 if not fs or any(':answer-field/correct' not in f for f in fs):
  excluded.append({'id':q[':question/id'],'reason':'Captured record lacks answer fields or correct-answer reference; usability cannot be established.'});continue
 r=next(x for x in replays if x['generation']['source_id']==q[':question/id'])
 originals.append((q[':db/id'],r,'inventory'))
assert len(originals)==2
start=max(q[':db/id'] for q in inventory['questions'])+1
seeds=[f'inventory-selection-{i}' for i in range(1000)]
results=[];selection_records=[]
for label,rs in [('sampled',accepted),('runner',rb)]:
 universe=originals+[(start+i,r,'generated') for i,r in enumerate(rs)]
 for name,weights,fresh in [('hard-only',[0,0,1],'all'),('mixed',[2,3,4],'all'),('seen-inventory',[0,0,1],'generated'),('seen-half-new',[0,0,1],'half-generated'),('zero-hard',[1,1,0],'all'),('unconfigured',None,'all')]:
  pool=[x for x in universe if fresh=='all' or fresh=='generated' and x[2]=='generated' or fresh=='half-generated' and (x[2]=='inventory' or x[0]>=start+len(rs)//2)]
  pool.sort(key=lambda x:x[0]);draws=[]
  for seed in seeds:
   if weights is None:chosen=pool[0]
   elif weights[2]==0:continue
   else:
    digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);chosen=pool[int(u*len(pool))]
   draws.append(chosen)
  gen=[r for _,r,kind in draws if kind=='generated'];pc=collections.Counter(r['generation']['template'] for r in gen);positions=collections.Counter(str(qparts(r)[2]) for r in gen)
  results.append({'input':label,'case':name,'weights':weights,'available':len(pool),'draws':len(draws),'generated_draws':len(gen),'inventory_draws':len(draws)-len(gen),'distinct_generated':len({r['question'][':question/id'] for r in gen}),'generated_profiles':pc,'generated_positions':positions})
  if label=='sampled' and name=='mixed':selection_records=gen
save('inventory-selection-samples.json',selection_records)
save('inventory-selection-results.json',{'command':f'{PY} selection_inventory.py','basis':inventory['basis'],'inventory_records':len(inventory['questions']),'usable_captured_inventory_hard':len(originals),'excluded_incomplete':excluded,'seeds':seeds,'generated_entity_id_assignment':f'Synthetic ascending IDs from {start}; real publication may permute seeded selection but cannot change uniform support.','source_rules':'engine/rust/question_selection.rs: seen_before_task; select lines 135-217: sort/dedup, optional first-row fallback, band weighting, uniform within band; unknown ratings fallback only when no positively weighted rated pool.','results':results,'limitations':['No learner or active-policy snapshot; inspect configured/freshness scenarios instead of claiming live selection. Captured incomplete records cannot be treated as learner-usable.','Conclusions about support are conditional on a positive hard weight and available fresh questions. Unconfigured first-row and zero-hard behavior belong to the platform policy.']})
# Reuse the independent probe definitions without rerunning other milestones.
ns={};text=(E/'decision_tests.py').read_text();code=text[text.index('def probes('):text.index("survived=json.loads")];exec(code,globals(),ns)
save('inventory-selection-shortcuts.json',{'command':f'{PY} selection_inventory.py','results':ns['probes'](selection_records,'inventory-mixed-policy')})
print(json.dumps({'usable_inventory':len(originals),'incomplete_excluded':len(excluded),'cases':results}))
