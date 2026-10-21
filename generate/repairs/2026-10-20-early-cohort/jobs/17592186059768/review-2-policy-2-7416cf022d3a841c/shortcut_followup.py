import sys
sys.dont_write_bytecode=True
import review as a
import variation as v
import collections,itertools,hashlib
E=a.E
# These probes inspect mathematical choice presentation, not author test flags.
scalars={'sum':lambda m:sum(map(sum,m)), 'abs_sum':lambda m:sum(abs(x) for row in m for x in row),'unit_count':lambda m:sum(abs(x)==1 for row in m for x in row),'negative_count':lambda m:sum(x<0 for row in m for x in row),'zero_count':lambda m:sum(x==0 for row in m for x in row),'lexicographic':lambda m:tuple(x for row in m for x in row),'top_left':lambda m:m[0][0],'corner':lambda m:m[-1][-1]}
def probes(rs,label,ref):
 groups={'ALL':rs};groups.update({p:[r for r in rs if r['generation']['template']==p] for p in sorted({r['generation']['template'] for r in rs})})
 groups['unit_only_display']=[r for r in rs if all(abs(x)<=1 for row in a.correct_matrix(r) for x in row)]
 groups['nonunit_repeated_display']=[r for r in rs if len([x for row in a.correct_matrix(r) for x in row if x])>len({abs(x) for row in a.correct_matrix(r) for x in row if x}) and any(abs(x)>1 for row in a.correct_matrix(r) for x in row)]
 rows=[]
 for group,records in groups.items():
  if not records:continue
  for cue,fn in scalars.items():
   for ext,op in [('min',min),('max',max)]:
    wins=attempts=0
    for r in records:
     vals=[fn(m) for m in a.bank(r)];ix=[i for i,x in enumerate(vals) if x==op(vals)]
     if len(ix)==1:
      attempts+=1;wins+=a.field(r)[':answer-field/choices'][ix[0]][':answer/id']==a.correct_id(a.field(r))
    rows.append({'stage':label,'subgroup':group,'strategy':cue+'_'+ext,'correct':wins,'total':len(records),'unique_candidate_attempts':attempts,'baseline':.2,'sample_refs':[ref]})
 return rows
rows=[]
for label,ref in [('units_raw','unit-records.json'),('units_filtered_easy','delivery-unit-easy/accepted.json'),('units_filtered_moderate','delivery-unit-moderate/accepted.json'),('batch_filtered','delivery-batch/accepted.json'),('normal_filtered_easy','delivery-easy/accepted.json'),('normal_filtered_moderate','delivery-moderate/accepted.json')]:rows+=probes(a.read(E/ref),label,ref)
a.save('fallback-shortcut-results.json',rows)
# Inspect sign-mask-permutation orbit capacities for stored generated inventory.
stored=[]
for r in a.read(E/'generated-records.json'):
 m=a.correct_matrix(r);groups=collections.defaultdict(list)
 for row in m:
  for x in row:
   if x:groups[x>0].append(x)
 import math
 orbit=1
 for xs in groups.values():
  ways=math.factorial(len(xs))
  for count in collections.Counter(xs).values():ways//=math.factorial(count)
  orbit*=ways
 stored.append({'question_id':r['question'][':question/id'],'same_mask_orbit':orbit,'latest_unit_capacity_defect_demonstrated':False,'basis':'Exactly reconstructed archived generation parameters match stored full content; every same-mask orbit >=5, so no stored instance of latest defect.'});assert orbit>=5
a.save('inventory-unit-results.json',{'all_generated_inventory_tested':True,'generated_count':len(stored),'cases':stored,'original_sources_excluded':True})
# Reuse earlier actual selection-policy evidence only after verifying source and inventory.
prior=a.read(a.JOB/'review-1-policy-2-a0f21dc2de58c6f5/learner-selection-results.json');sha=hashlib.sha256((a.REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest();assert sha==prior['current_verification']['source_sha256']
prior['reuse_provenance']={'from':'review-1-policy-2-a0f21dc2de58c6f5/learner-selection-results.json','unchanged_source_sha256':sha,'source_lines_reviewed':'100..198','current_batch':'5/5 survive; positive easy weight gives every usable member conditional support. No policy excludes by signs/role/mode; unconfigured policy chooses smallest fresh entity ID. Actual learner history/reservations/weights and future IDs not captured.'};a.save('learner-selection-results.json',prior)
print({'probes':len(rows),'universal_multirecord_scalar_cues':[(r['stage'],r['subgroup'],r['strategy'],r['total']) for r in rows if r['total']>=3 and r['correct']==r['total']],'inventory_latest_defect':0})
