import collections,sys
from review import E,save,load,module,field,key,correct,kind,matrices,optext
sys.dont_write_bytecode=True
g=module(E/'runtime/17592186059773.py','domain_generator')
sample=load(E/'delivery/accepted.json');domains={}
for sid in g.CASES:
 d=g.domain(sid);rs=[r for r in sample if r['generation']['template']==sid]
 domains[sid]={'domain_points':len(d),'single_entry_slots':sorted({(p[1],p[2]) for p in d}),'deltas':sorted({p[3] for p in d}),'permutations':[list(p) for p in sorted({tuple(p[4]) for p in d})],'eligible_keys':g.eligible_keys(sid),'observed_keys':sorted({key(r) for r in rs}),'observed_permutations':[list(p) for p in sorted({tuple(r['generation']['parameters'][4]) for r in rs})],'numeric_restriction':'One nonzero A entry changes by nonzero -3..3 without crossing zero or sign. Scalar bank stays fixed. This conservatively bounds arithmetic; fixed sign/zero pattern is not treated as the assessed rule. Eligible operation roles change within every bank.'}
 assert domains[sid]['eligible_keys']==domains[sid]['observed_keys']
save('sampling-domain.json',domains)
# Real UI choice order is FNV-1a over itemId:fieldUUID:answerUUID, not authored slot.
def ui_order(r,item):
 f=field(r)
 def fnv(c):
  h=2166136261
  for ch in f"{item}:{f[':answer-field/id']}:{c[':answer/id']}":h=((h^ord(ch))*16777619)&0xffffffff
  return h
 cs=sorted(f[':answer-field/choices'],key=fnv)
 return next(i for i,c in enumerate(cs) if c[':answer/id']==f[':answer-field/correct'][1])
batch=load(E/'batch-delivery/accepted.json');ui=[]
for item in (1,2,3,4,5,42,1000):
 ui.append({'item_id':item,'correct_positions':[ui_order(r,item)+1 for r in batch]})
# More conditional actions using observable bank signatures, not metadata as a cue.
probes=[]
for sid in g.CASES:
 rs=[r for r in load(E/'controlled-records.json') if r['generation']['template']==sid]
 # Limit to the shared-A target panel; duplicates from irrelevant pairs do not distort baseline.
 rs=rs[:len(g.eligible_keys(sid))]
 counts=collections.Counter(kind(correct(r)) for r in rs)
 best=max(counts,key=counts.get)
 probes.append({'cue':'Recognizable complete operation bank','subgroup':sid,'scope':'within_template','strategy':f'Choose an operation of type {best} without examining the matrices','correct':counts[best],'total':len(rs),'baseline':max(collections.Counter(kind(c[':answer/value']) for c in field(rs[0])[':answer-field/choices']).values())/5,'disposition':'not_predictive' if counts[best]<len(rs) else 'intended_skill','conclusion':('Baseline is the proportion of five offered choices belonging to the bank’s most common operation type. This is a generous type-only success bound; it still does not identify a choice. The swap-only q-72850 bank has three distinct elementary swap targets; matching the pair of changed rows is the lesson operation, and a bank-only fixed action succeeds only 1/3.' if counts[best]==len(rs) else 'Baseline is the proportion of five offered choices belonging to the bank’s most common operation type. Type prediction is a generous answer-producing-action upper bound; it does not identify the correct choice. Distinct eligible types occur while A and bank are held fixed.'),'sample_refs':['controlled-records.json']})
save('action-shortcut-results.json',{'conditional_action_probes':probes,'batch_actual_ui_order_scenarios':ui,'ui_order_source':'ui/learning.js lines 690-701. Existing renderer uses contentId; live activity uses itemId. These are scenario item IDs, not a claim of a live task.','actual_batch_repetition':'3 additions and 2 scales; no swap in this five-record draw. All five have different matrix/operation evidence; no universal authored position or type answers all five.','limitations':['No finite probe proves absence of every conceivable cue.','Live task IDs, learner history and policy were not supplied.']})
print({'eligible_roles':sum(len(x['eligible_keys']) for x in domains.values()),'bank_profiles':len(domains),'batch_ui_positions':ui})
