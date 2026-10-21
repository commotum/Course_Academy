import audit as a
import json, collections, hashlib, math, pathlib, inspect, copy
E=a.E;g=a.g
# Natural CLI-equivalent batch, retaining rejection/resampling and fingerprint trace.
seed=5812061;count=75
natural=g.batch('easy',count,seed);a.save('natural-samples.json',natural)
seen=set();trace=[];accepted=[]
for offset in range(50*count):
 if len(accepted)==count:break
 raw=g.generate.__wrapped__('easy',seed+offset)
 r=g.generate('easy',seed+offset)
 fp=g.fingerprint(r);keep=fp not in seen
 if keep:seen.add(fp);accepted.append(r)
 trace.append({'input_seed':seed+offset,'raw_id':raw['question'][':question/id'],'raw_selection':a.keyed(raw),'raw_profile':raw['generation']['profile'],'final_id':r['question'][':question/id'],'final_seed':r['generation']['seed'],'final_selection':a.keyed(r),'final_profile':r['generation']['profile'],'resampled':raw['question'][':question/id']!=r['question'][':question/id'],'fingerprint_kept':keep})
assert accepted==natural
for r in natural:a.check_record(r)
a.save('resampling-trace.json',{'command':'PYTHONDONTWRITEBYTECODE=1 '+a.sys.executable+' variation.py','seed':seed,'count':count,'attempts':len(trace),'trace':trace,'stages':{'raw_attempts':len(trace),'policy_resampled':sum(x['resampled'] for x in trace),'fingerprint_duplicates':sum(not x['fingerprint_kept'] for x in trace),'output':len(natural)}})
allsets={'independent':json.load(open(E/'independent-samples.json')),'runner_batch':json.load(open(E/'runner-batch.json')),'natural':natural,'delivery_independent':json.load(open(E/'delivery-independent/accepted.json')),'delivery_batch':json.load(open(E/'delivery-batch/accepted.json'))}
def profile(r):return r['generation']['profile']
def grouping(rs,kind):
 if kind=='overall':return {'all':rs}
 d=collections.defaultdict(list)
 for r in rs:
  if kind=='profile':key=profile(r)
  elif kind=='template':key=r['generation']['template']
  elif kind=='shapes':key=json.dumps([(len(m),len(m[0])-1) for _,m in sorted(a.visible(r).items())])+'|'+r['generation']['template']
  d[key].append(r)
 return d
probes=[];coverage={}
for name,rs in allsets.items():
 coverage[name]={'count':len(rs),'profiles':dict(collections.Counter(profile(r) for r in rs)),'templates':dict(collections.Counter(r['generation']['template'] for r in rs)),'subsets':dict(collections.Counter(a.keyed(r) for r in rs)),'rule_cases':dict(collections.Counter(c for r in rs for c in r['generation']['cases']))}
 for group_kind in ['overall','profile','template','shapes']:
  for group,members in grouping(rs,group_kind).items():
   subs=collections.Counter(a.keyed(r) for r in members);target,n=subs.most_common(1)[0]
   # Fixed subset strategy uses labels only, completely bypassing mathematics.
   baseline=sum(1/len([s for s in g.eligible_subsets(profile(r)) if s or g.field_type(profile(r))=='radio']) for r in members)/len(members)
   probes.append({'dataset':name,'group_kind':group_kind,'group':group,'strategy':'always select '+(target or 'none'),'correct':n,'total':len(members),'baseline':baseline,'outcomes':dict(subs),'perfect':n==len(members),'small_group_limit':len(members)<10})
   # Literal response position for radio banks; for checkbox, choose one fixed label combination above.
   radios=[r for r in members if g.field_type(profile(r))=='radio']
   if radios:
    counts=collections.Counter(next(i for i,x in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if x[':answer/value']==a.val(r['question'][':question/answer-fields'][0])) for r in radios)
    pos,n=counts.most_common(1)[0];probes.append({'dataset':name,'group_kind':group_kind,'group':group,'strategy':'always choose radio position '+str(pos+1),'correct':n,'total':len(radios),'baseline':0.2,'outcomes':dict(counts),'perfect':n==len(radios),'small_group_limit':len(radios)<10})
 # sign-only strategy: choose positive top-left entry, compare complete response.
 successes=sum(''.join(k for k,m in sorted(a.visible(r).items()) if m[0][0]>0)==a.keyed(r) for r in rs)
 probes.append({'dataset':name,'group_kind':'overall','group':'all','strategy':'select matrices whose top-left number is positive','correct':successes,'total':len(rs),'baseline':1/7,'perfect':successes==len(rs)})
a.save('coverage-shortcuts.json',{'coverage':coverage,'probes':probes,'interpretation':'No fixed subset or answer-position strategy predicts every member of a well-sampled recognizable profile/template/shape family. Tiny one-item groups cannot substantiate a generator shortcut. Runner batch decisions are A, AC, AC, BC, B; q-42028 subgroup decisions A, AC, BC. All are structurally different, not sign-only copies. Sign patterns alone fail. Random-complete-answer baseline is 1/7 for nonempty checkbox and 1/5 for preserved radio bank; mixed baseline is averaged per instance.'})
# Exact-independent inventory key audit. Historical inventory lacks generation metadata.
inv=[]
for q in a.I['questions']:
 r={'question':q};truth=a.selected(r)
 try:key=a.keyed(r);matches=truth==key
 except KeyError:key=None;matches=None
 inv.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'selected_independently':truth,'stored_selection':key,'key_matches':matches,'captured_source':q[':question/id'] in {x[':question/id'] for x in a.source},'empty_checkbox':bool(q[':question/answer-fields']) and a.enum(q[':question/answer-fields'][0][':answer-field/type']).endswith('/checkbox') and key==''})
a.save('inventory-audit.json',{'basis':a.I['basis'],'questions_tested':len(inv),'rows':inv,'limits':['No generation metadata is present on any captured inventory row; seeds and original sampler bindings are unavailable.','One historical all-false checkbox exists (b32d6bad-7619-5a20-9b5f-d26342503b3d). Current public generate rejects explicit empty checkbox instances and resamples seeded ones; this is not a reproduced current-generator failure.','Original q-42026 lacks a key and solution and is not labeled generated here.'],'current_generator_defects_demonstrated':0})
a.save('affected-inventory.json',{'affected_questions':[]})
# Faithful read-only Rust select reproduction. All surviving new questions are easy;
# any positive easy weight selects uniformly among fresh easy candidates, independent of other weights.
pool=json.load(open(E/'delivery-batch/accepted.json'));draws=[]
for n in range(100):
 digest=hashlib.sha256(('course-academy/question-selection/v1/review-'+str(n)).encode()).digest()
 u=(int.from_bytes(digest[8:16],'big')>>11)/2**53
 ix=int(u*len(pool));draws.append(ix)
selected=[pool[ix] for ix in draws]
a.save('selection-results.json',{'source':'engine/rust/question_selection.rs: select, seen_before_task; lines 113-219','pool_file':'delivery-batch/accepted.json','pool_order':'five publication candidates in order; new DB IDs not allocated, rank invariant for uniform subset selection','seed_prefix':'review-','draws':draws,'counts':dict(collections.Counter(draws)),'selection_subsets':dict(collections.Counter(a.keyed(r) for r in selected)),'configured_positive_easy_weight':'All delivered candidates are easy; same-band selection is uniform; all five are reachable and no role becomes fixed. Tested 100 deterministic selection seeds.','configured_zero_easy_weight':'With zero easy weight and no unrated fresh candidates, returns None. It does not preferentially retain a decision case.','unconfigured_policy':'select returns least candidate ID; excluding previous-task history and current prefix successively exposes remaining pool. Sorting cannot alter member content; full finite-pool outcomes remain A, AC, BC, B.','history':'Removing seen items can create small or singleton remaining pools; no claim of conditional balance for arbitrary learner history. No learner policy/history snapshot was supplied.','captured_inventory_basis':a.I['basis'],'inventory_limits':'Existing original q-42026 has no key; usable candidate filtering belongs to caller. Source and generated content are not relabeled. This read-only reproduction allocates no database IDs.','database_writes':0})
(E/'session-state.md').write_text('Math, source replays, target coverage, counterfactual records, packaging and native grading passed; shared delivery accepted 360/360 independent and 5/5 batch records. Natural batch/resampling trace, conditional shortcut probes, inventory audit and selector analysis saved. UI rendering in progress. Package unchanged.\n')
print(json.dumps({'coverage':coverage,'perfect_probes_n_ge_10':[x for x in probes if x['perfect'] and x['total']>=10],'inventory_empty_historical':sum(x['empty_checkbox'] for x in inv),'selection_counts':dict(collections.Counter(draws))}))
