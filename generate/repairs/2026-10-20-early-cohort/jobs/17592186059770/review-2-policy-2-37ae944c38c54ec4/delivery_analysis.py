"""Read-only delivery, conditional cue, and learner-selection analysis."""
from audit import *
from reproduce_shortcut import select

def matrix_key(m):return tuple(tuple(str(x) for x in row) for row in m)
def inspect(rs):
 groups=collections.defaultdict(list);profiles=collections.defaultdict(list)
 for r in rs:
  qcheck(r);f=r['question'][':question/answer-fields'][0]
  key=tuple(sorted(matrix_key(mat(a[':answer/value'])) for a in f[':answer-field/choices']))
  groups[key].append(r);profiles[r['generation']['bank_profile']].append(r)
 out={}
 for profile,xs in profiles.items():
  probes=collections.defaultdict(list)
  for r in xs:
   f=r['question'][':question/answer-fields'][0];vals=[mat(a[':answer/value']) for a in f[':answer-field/choices']];expected=visible(r['question']);pos=vals.index(expected)
   probes['prior_shape_sign_tree'].append(select(r)==f[':answer-field/correct'][1])
   for j in range(5):probes[f'fixed_index_{j}'].append(j==pos)
   for row in range(2):
    for col in range(3):
     for sign in [-1,0,1]:
      hits=[i for i,m in enumerate(vals) if row<len(m) and col<len(m[0]) and sp.sign(m[row][col])==sign]
      probes[f'unique_sign_{row}_{col}_{sign}'].append(hits==[pos])
   for name,score in [('most_zeros',lambda m:sum(x==0 for row in m for x in row)),('most_negatives',lambda m:sum(bool(x<0) for row in m for x in row)),('fewest_negatives',lambda m:-sum(bool(x<0) for row in m for x in row)),('largest_abs',lambda m:sum(abs(x) for row in m for x in row)),('smallest_abs',lambda m:-sum(abs(x) for row in m for x in row))]:
    scores=[score(m) for m in vals];hits=[i for i,s in enumerate(scores) if s==max(scores)];probes[name].append(hits==[pos])
  out[profile]={'count':len(xs),'target_roles':dict(collections.Counter(x['generation']['target_recipe'] for x in xs)),'positions':dict(collections.Counter(qcheck(r)['correct_index'] for r in xs)),'probes':{k:{'correct':sum(v),'total':len(v)} for k,v in probes.items()},'perfect_tested_bank_only_rules':[k for k,v in probes.items() if all(v)]}
 return {'records':len(rs),'profiles':out,'fixed_banks':[{'size':len(xs),'distinct_targets':len({matrix_key(visible(r['question'])) for r in xs}),'bank_only_upper_bound':max(collections.Counter(matrix_key(visible(r['question'])) for r in xs).values())} for xs in groups.values()]}
paths=['batch.json','delivery-batch/accepted.json','fresh-batches.json','delivery-fresh/accepted.json','controlled.json','delivery-controlled/accepted.json','sample.json','delivery-sample/accepted.json']
reports={p:inspect(load(E/p)) for p in paths}
for p in ['batch.json','delivery-batch/accepted.json','fresh-batches.json','delivery-fresh/accepted.json']:
 assert all(g['size']==g['distinct_targets'] and g['size']>=2 for g in reports[p]['fixed_banks'])
 assert not any(x['perfect_tested_bank_only_rules'] for x in reports[p]['profiles'].values())
assert reports['controlled.json']['profiles'].keys()==reports['delivery-controlled/accepted.json']['profiles'].keys()
for p,x in reports['controlled.json']['profiles'].items():assert set(x['target_roles'])==set(reports['delivery-controlled/accepted.json']['profiles'][p]['target_roles'])
save('delivery-analysis.json',reports)
# The Rust rule is implemented here only for the documented, all-fresh easy
# candidate band, using actual IDs for old records and hypothetical fresh IDs
# for not-yet-published records. It is not a live learner-state claim.
inv=load(J/'source/inventory.json');new=load(E/'delivery-batch/accepted.json')
old_easy=[q for q in inv['questions'] if q.get(':question/difficulty')=={':db/ident':':question.difficulty/easy'}]
base=max(q[':db/id'] for q in inv['questions'])+1
candidates=[(q[':db/id'],q[':question/id'],'existing-source') for q in old_easy]+[(base+i,r['question'][':question/id'],'new-batch') for i,r in enumerate(new)]
candidates.sort();draws=[]
for seed in range(180):
 digest=hashlib.sha256(f'course-academy/question-selection/v1/independent-review-{seed}'.encode()).digest()
 u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 draws.append(candidates[int(u*len(candidates))][1])
assert set(draws)=={q for _,q,_ in candidates}
save('selection-analysis.json',{'implementation':'engine/rust/question_selection.rs: seen_before_task and select; sorted unique entity IDs, difficulty band draw using uniform(0), within-band uniform(8), unconfigured policy picks candidates.first().','captured_basis':inv['basis'],'captured_counts':{'inventory_questions':len(inv['questions']),'easy_source':len(old_easy),'proposed_easy_batch':len(new),'combined_easy':len(candidates)},'simulation':{'seeds':'independent-review-0 .. independent-review-179','conditional_distribution':'easy chosen with positive policy weight; no excluded questions','hypothetical_entity_ids':{r['question'][':question/id']:base+i for i,r in enumerate(new)},'candidates':candidates,'draw_counts':dict(collections.Counter(draws)),'all_new_records_selectable':all(r['question'][':question/id'] in draws for r in new)},'post_selection_interpretation':'Uniform within-band draw preserves each bank target as a selectable item for all-fresh candidates. Neither filtering nor actual selector enforces paired delivery; arbitrary seen/reserved exclusions may remove companions. A single learner sequence is not certified. Current tested raw/delivered groups defeat the old bank-only rule; no universal all-history claim.','unconfigured_policy':'Select first eligible entity after caller freshness/usable filtering. Unknown future IDs and learner exclusions prevent predicting the exact chosen record.','limits':['No publication preparation file exists; actual read-only shared delivery filter used.','No live policy weights, learner history, reservations or future entity IDs are available.','Captured original source questions remain instructional records, not generated affected instances.','Five old moderate generated records remain in captured inventory and are separately listed for downstream remediation.']})
print(json.dumps({'datasets':len(reports),'batch_bank_sizes':[g['size'] for g in reports['delivery-batch/accepted.json']['fixed_banks']],'fresh_delivery':reports['delivery-fresh/accepted.json']['records'],'controlled_delivery':reports['delivery-controlled/accepted.json']['records'],'selection_easy_candidates':len(candidates)}))
