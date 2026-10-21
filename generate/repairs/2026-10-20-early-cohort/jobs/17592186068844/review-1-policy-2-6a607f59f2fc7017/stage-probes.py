"""Choice-only attacks plus faithful read-only selection-rule reproduction.
Run after check_delivery. All paths local to this independent evidence directory.
"""
import json,collections,hashlib
from pathlib import Path
import audit as a
from importlib.util import spec_from_file_location,module_from_spec
E=Path(__file__).resolve().parent
sp=spec_from_file_location('review',E/'independent-review.py');review=module_from_spec(sp);sp.loader.exec_module(review)
save=review.save;key=review.key;bank=review.bank
probes=[];coverage={}
POLICIES={'first':lambda b:b[0],'last':lambda b:b[-1],'middle':lambda b:b[2],'shortest':lambda b:min(b,key=len),'longest':lambda b:max(b,key=len),'lexical_first':min,'lexical_last':max}
def hits(rs,fn):return sum(fn(bank(r))==key(r) for r in rs)
def inspect(name,rs):
 groups=collections.defaultdict(list)
 for r in rs:groups[r['generation']['template']].append(r)
 coverage[name]={}
 for t,sub in sorted(groups.items()):
  matched=[r for r in sub if r['generation']['seed']==661019+list(a.g.TEMPLATES).index(t)]
  # Boundaries have other seeds and batch may duplicate template; isolate the controlled quintuple.
  matched=[r for r in matched if r['generation']['parameters']['k']==3 and r['generation']['parameters']['h']==(0 if 'autonomous' in t else -2)]
  assert len(matched)==5 and len({key(r) for r in matched})==5
  assert len({tuple(bank(r)) for r in matched})==1
  row={'count':len(sub),'roles':dict(collections.Counter(str(r['generation']['parameters']['c']) for r in sub)),'positions':dict(collections.Counter(bank(r).index(key(r))+1 for r in sub)),'matched_roles_survive':len(matched),'old_attack_unique_hits':sum(a.shortcut(r)==[a.answer_id(a.field(r))] for r in sub)}
  coverage[name][t]=row
  assert row['old_attack_unique_hits']==0
  for policy,fn in POLICIES.items():
   n=hits(matched,fn);assert n==1
   probes.append({'stage':name,'template':t,'cue':policy,'correct':n,'total':5,'baseline':.2,'interpretation':'Same ordered visible bank, all five keys occur. No deterministic choice-only policy can exceed 1/5 in this matched group.'})
raw=json.load(open(E/'delivery-input.json'));post=json.load(open(E/'delivery-independent/accepted.json'));batch=json.load(open(E/'batch-records.json'));batchpost=json.load(open(E/'delivery-batch/accepted.json'))
inspect('before_delivery',raw);inspect('after_delivery',post)
batch_stats={'raw_count':len(batch),'accepted_count':len(batchpost),'positions':dict(collections.Counter(bank(r).index(key(r))+1 for r in batchpost)),'coefficients':dict(collections.Counter(str(r['generation']['parameters']['c']) for r in batchpost)),'templates':dict(collections.Counter(r['generation']['template'] for r in batchpost)),'policies':{name:{'correct':hits(batchpost,fn),'total':len(batchpost),'baseline':.2} for name,fn in POLICIES.items()},'old_attack_unique_hits':sum(a.shortcut(r)==[a.answer_id(a.field(r))] for r in batchpost),'conditional':[]}
for t in sorted({r['generation']['template'] for r in batchpost}):
 sub=[r for r in batchpost if r['generation']['template']==t]
 batch_stats['conditional'].append({'template':t,'total':len(sub),'policies':{n:hits(sub,f) for n,f in POLICIES.items()},'old_attack_unique_hits':sum(a.shortcut(r)==[a.answer_id(a.field(r))] for r in sub)})
assert len(batchpost)==5 and not any(v['correct']==5 for v in batch_stats['policies'].values())
save('shortcut-results.json',{'matched_probes':probes,'coverage':coverage,'batch':batch_stats,'limit':'Singleton batch template groups trivially have a perfect fitted answer. These are observations, not a reproducible template-wide predictor; matched controls refute extending those constant-choice rules. No finite set proves absence of all cues.'})
# Faithful select() branch, using stored IDs and explicitly provisional IDs for prepared records.
inv=json.load(open(a.JOB/'source/inventory.json'));candidates={q[':db/id']:{'band':q[':question/difficulty'][':db/ident'].split('/')[-1],'role':'legacy/source','question_id':q[':question/id']} for q in inv['questions']}
start=max(candidates)+1000
for i,r in enumerate(post):candidates[start+i]={'band':'easy','role':r['generation']['parameters']['c'],'question_id':r['question'][':question/id'],'template':r['generation']['template']}
BANDS=('easy','moderate','hard')
def select(pool,distribution,seed):
 pool=sorted(set(pool))
 if distribution is None:return pool[0] if pool else None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 uniform=lambda offset:(int.from_bytes(digest[offset:offset+8],'big')>>11)/(1<<53)
 bands=[[q for q in pool if candidates[q]['band']==b] for b in BANDS]
 total=sum(w for b,w in zip(bands,distribution) if b)
 if total>0:
  draw=uniform(0)*total;chosen=None
  for i,w in enumerate(distribution):
   if not bands[i] or w==0:continue
   chosen=i
   if draw<w:break
   draw-=w
  pool=bands[chosen]
 else:pool=[] # Every captured/generated candidate is rated; no unrated fallback here.
 return pool[int(uniform(8)*len(pool))] if pool else None
seen={q for q,d in candidates.items() if d['band']!='easy'}
pool=sorted(set(candidates)-seen)
trials=[]
for i in range(256):
 seed='independent-review-731871-'+str(i);q=select(pool,[1,0,0],seed);assert q==select(pool,[1,0,0],seed)
 trials.append({'seed':seed,'entity_id':q,**candidates[q]})
# Selection support proof follows directly from uniform(8) within sorted easy pool;
# this numerical exercise verifies representative hashes and history exclusions.
assert all(t['band']=='easy' for t in trials)
selection={'implementation_file':str(a.REPO/'engine/rust/question_selection.rs'),'implementation_sha256':hashlib.sha256((a.REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'captured_basis':inv['basis'],'candidate_basis':'Captured inventory plus actual post-filter records; provisional IDs for unpublished records only. New real IDs would change exact hash-to-question mappings, not the uniform-within-band rule.','rules_examined':['Exclude learner previous tasks and current prefix before selection','Configured activity/phase chooses difficulty first; absent/nonpositive supply renormalizes','Deduplicate/sort IDs; hash task seed; uniform index within chosen nonempty band','Unconfigured policy chooses first candidate; rated zero-weight bands never enter fallback'],'candidate_band_counts':dict(collections.Counter(d['band'] for d in candidates.values())),'test_configuration':{'weights':[1,0,0],'excluded_ids':sorted(seen),'seeds':'independent-review-731871-0 through -255'},'trials':trials,'selected_coefficient_counts':dict(collections.Counter(str(t['role']) for t in trials)),'no_policy_candidate':select(pool,None,'x'),'all_zero_easy_supply':select(sorted(seen),[1,0,0],'x'),'conclusion':'For configured easy delivery the within-band rule does not condition on key, template, sign or coefficient, and all five new roles have selection support. Historic moderate/hard defects are reachable under policy bands that allow them, retained in affected-inventory.json.','limits':['No live policy or learner task history captured; exact live mixture cannot be asserted.','Publication absent; no real new entity IDs assigned. This is rule inspection and read-only faithful reproduction, not a native EntitySnapshot integration test.']}
save('selection-results.json',selection)
save('delivery-coverage.json',{'inventory_basis':inv['basis'],'before_count':len(raw),'accepted_count':len(post),'discarded_count':len(raw)-len(post),'matched_cases_by_stage':coverage,'batch':batch_stats,'selection_evidence':'selection-results.json','generator_rejection':'No valid-parameter rejection/resampling loop. Eight explicit invalid cases rejected and boundary cases passed in packaging-results.json.','filter_implementation':'check_delivery actual publisher prepare_records; stage counts/hashes in delivery-independent/delivery.json and delivery-batch/delivery.json'})
print(json.dumps({'before':len(raw),'after':len(post),'all_role_groups_retained':len(coverage['after_delivery']),'batch':batch_stats,'selected_roles':selection['selected_coefficient_counts']}))
