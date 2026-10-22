import sys,json,pathlib,collections,hashlib,re
sys.dont_write_bytecode=True
from review_generator import E,JOB,REPO,read,signature,save,independent
rules={(x['target'],tuple(x['sorted_adjacent_gaps'])):x['choose_sorted_rank_1_based']-1 for x in json.loads((E/'shortcut-rules.json').read_text())}
def probe(rs):
 out=collections.defaultdict(lambda:[0,0]);roles=collections.Counter();shapes=collections.Counter();vals=collections.Counter()
 for r in rs:
  d=independent(r);s=signature(r);pred=sorted(d['values'])[rules[s]];out[str(s)][0]+=pred==d['c'];out[str(s)][1]+=1;roles[d['target']]+=1;shapes['square' if d['m']==d['n'] else 'tall' if d['m']>d['n'] else 'wide']+=1;vals[d['c']]+=1
 return {'correct':sum(v[0] for v in out.values()),'total':len(rs),'roles':dict(roles),'shapes':dict(shapes),'answers':dict(vals),'conditional':{k:{'correct':v[0],'total':v[1]} for k,v in out.items()},'baseline':.2}
batch=json.loads((E/'delivery-batch/accepted.json').read_text());control=json.loads((E/'delivery-control/accepted.json').read_text());save('delivery-shortcut-results.json',{'control':probe(control),'runner_batch':probe(batch),'stages':{'control':json.loads((E/'delivery-control/delivery.json').read_text()),'batch':json.loads((E/'delivery-batch/delivery.json').read_text())}})
# Native input for changed publication identities and for the actual surviving batch.
inputs=json.loads((E/'grader-input.json').read_text())
for i,r in enumerate(batch):
 d=read(r);f=r['question'][':question/answer-fields'][0];v=sorted(d['values'])[rules[signature(r)]]
 checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if int(a[':answer/value'])==d['n']-d['k'] else 'rejected','purpose':'surviving normalized batch; complete bank'} for a in f[':answer-field/choices']]
 checks.append({'submitted_answer_id':next(a[':answer/id'] for a in f[':answer-field/choices'] if int(a[':answer/value'])==v),'expected':'accepted','purpose':'delivered bank-only shortcut'})
 inputs.append({'label':'delivered-batch-'+str(i),'record':r,'checks':checks})
save('grader-input.json',inputs)
inv=json.loads((JOB/'source/inventory.json').read_text());source=json.loads((JOB/'source/source.json').read_text());source_ids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
inv_report={'basis':inv['basis'],'questions':[],'generated_questions':[],'conclusion':'All 14 captured inventory records are original source questions, with no generation metadata. There are zero captured generated questions to reproduce for the demonstrated generator weaknesses. Verified on the captured inventory, not a claim about a later live bank.'}
for q in inv['questions']:
 keys=[k for k in q if 'generat' in k];row={'id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in source_ids,'generation_keys':keys};inv_report['questions'].append(row)
 if keys or not row['original_source']:inv_report['generated_questions'].append(row)
assert not inv_report['generated_questions'];save('inventory-audit.json',inv_report);save('affected-inventory.json',{'affected_questions':[]})
# Read-only reproduction of question_selection.rs::select when all fresh candidates are easy.
# For positive easy weight (configured policy), SHA byte offset 8 draws uniformly from sorted entities.
# New database entity IDs are not yet allocated; assign monotonic hypothetical IDs, preserving records.
records={q[':db/id']:{'question':q} for q in inv['questions']};first=max(records)+1000
for i,r in enumerate(batch):records[first+i]=r

def select(ids,seed,configured=True,easy_positive=True):
 ids=sorted(set(ids))
 if not ids:return None
 if not configured:return ids[0]
 if not easy_positive:return None # explicit zero easy weight is never fallback
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();bits=int.from_bytes(digest[8:16],'big')>>11
 return ids[int(bits/(1<<53)*len(ids))]
selection=[]
for name,ids in [('fresh-captured-plus-batch',list(records)),('originals-seen-batch-only',list(range(first,first+len(batch)))),('four-batch-records-seen',[first+4])]:
 hits=collections.Counter();draws=[]
 for i in range(256):
  seed=f'independent-review/{i}';qid=select(ids,seed);hits[qid]+=1;draws.append({'seed':seed,'entity_id':qid})
 generated=[records[i] for i in hits if i>=first]
 selection.append({'case':name,'eligible_count':len(ids),'hypothetical_entity_ids':True,'draws':draws,'counts':{str(i):n for i,n in hits.items()},'generated_selected_unique':len(generated),'selected_generated_shortcut':probe(generated) if generated else None})
save('learner-selection.json',{'implementation':'engine/rust/question_selection.rs select, SHA256 domain course-academy/question-selection/v1/, sorted unique IDs, bits 8..16 >>11 for within-band draw','all_rated_easy':True,'configured_positive_easy':selection,'unconfigured_policy_first_record':select(list(records),'ignored',False),'explicit_zero_easy_weight':select(list(records),'ignored',True,False),'freshness':'seen_before_task and current prefix exclude previously served records before selection; exclusions cannot introduce a counterexample to a per-record perfect strategy.','limits':['Captured inventory has no learner history or policy-weight entities. Conditional reproduction covers positive-easy configured policy, no-policy fallback and zero-easy exclusion, with explicit exclusion scenarios; it does not predict a real learner task.','New records do not yet have database entity IDs. Hypothetical IDs make hash draws reproducible, not actual future selection predictions.','All five accepted batch records preserve the shortcut; every nonempty fresh subset also does.']})
# Minimal failures and exact complete records for adoption by repair.
minimal=next(r for r in json.loads((E/'independent-samples.json').read_text()) if r['generation']['profile']=='q-141220');save('minimal-shortcut-record.json',[minimal])
missing=[x for x in json.loads((E/'source-replay.json').read_text()) if x['status']=='failed'];save('minimal-failures.json',{'bank_shortcut':{'record_file':'minimal-shortcut-record.json','parameters':minimal['generation']['parameters'],'profile':minimal['generation']['profile'],'seed':minimal['generation']['seed'],'visible_rule':'When target is rank and choices are five consecutive integers, select the second largest.','correct':read(minimal)['c'],'choices':read(minimal)['values']},'missing_sources':missing})
(E/'session-state.md').write_text('Delivery complete: 264 controls -> 257 accepted (7 duplicates); runner batch 5 -> 5. Signature shortcut succeeds for every survivor. Native raw tests passed; combined normalized input saved for rerun. Inventory verified: all 14 records are original sources, no stored generated instances. Learner-selection conditional reproduction saved with explicit missing-policy/history limits. Actual renderer is running.\n')
print(json.dumps({'control':probe(control),'batch':probe(batch),'inventory_generated':0,'selection_scenarios':len(selection)}))
