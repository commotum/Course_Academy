from review_lib import *
import collections
import legacy_shortcut_lib as legacy

def information(r):
 q=r['question'];f=q[':question/answer-fields'][0];bank=[vec(c[':answer/value']) for c in f[':answer-field/choices']];cid=f[':answer-field/correct'];cid=cid[1] if isinstance(cid,list) else cid[':answer/id'];key=next(i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==cid)
 return bank,key

def unique_extreme(bank,j,maximum):
 value=(max if maximum else min)(v[j] for v in bank);ix=[i for i,v in enumerate(bank) if v[j]==value];return ix[0] if len(ix)==1 else None

def old_strategy(r):
 if r['generation']['profile']=='q-20450':return unique_extreme(information(r)[0],1,True)
 try:
  v=legacy.predict(r['question']);f=r['question'][':question/answer-fields'][0];return next(i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==v['predicted_id'])
 except (AssertionError,ValueError):return None

def probe(rs):
 out=[]
 strategies={'old conditional bank rule':old_strategy}
 for j in range(3):
  for maximum in [True,False]:
   strategies[('largest' if maximum else 'smallest')+f' coordinate {j+1}']=lambda r,j=j,maximum=maximum:unique_extreme(information(r)[0],j,maximum)
 for pos in range(5):strategies[f'authored bank position {pos+1}']=lambda r,pos=pos:pos
 for subgroup in ['overall',*sorted({r['generation']['profile'] for r in rs})]:
  group=rs if subgroup=='overall' else [r for r in rs if r['generation']['profile']==subgroup]
  for name,fn in strategies.items():
   predicted=[fn(r) for r in group];keys=[information(r)[1] for r in group]
   out.append({'subgroup':subgroup,'strategy':name,'correct':sum(p==k for p,k in zip(predicted,keys)),'total':len(group),'abstentions':predicted.count(None),'predictions':predicted,'keys':keys})
 return out
sets={n:load(ROOT/f) for n,f in [('samples','samples.json'),('controlled','controlled.json'),('batch','batch.json'),('delivered_samples','delivery-samples/accepted.json'),('delivered_controlled','delivery-controlled/accepted.json'),('delivered_batch','delivery-batch/accepted.json')]}
res={n:probe(rs) for n,rs in sets.items()};save('shortcut-results.json',res)
coverage={}
for n,rs in sets.items():
 coverage[n]={p:{'count':len(group),'keys':dict(collections.Counter(information(r)[1] for r in group)),'solution_signs':[list(v) for v in sorted({tuple(int(sp.sign(v)) for v in information(r)[0][information(r)[1]]) for r in group})]} for p in sorted({r['generation']['profile'] for r in rs}) for group in [[r for r in rs if r['generation']['profile']==p]]}
save('coverage-results.json',coverage)
# Verify fixed-bank role variations before/after true publisher filtering.
for stage in ['controlled','delivered_controlled']:
 for p,c in coverage[stage].items():
  assert len(c['keys'])>=4,(stage,p,c)
  for row in res[stage]:
   if row['subgroup']==p:assert row['correct']<=1,(stage,p,row)
# Batch-specific rules assessed separately; no perfect common strategy.
assert not any(row['correct']==row['total'] for row in res['batch'] if row['subgroup']=='overall')
# Reproduce actual selector's hash index for positive easy weight: all candidates here are easy.
rs=sets['delivered_batch'];selection=[]
for mask in range(1<<len(rs)):
 eligible=[i for i in range(len(rs)) if not (mask>>i&1)];draws=[]
 for seed in range(82067,82167):
  if not eligible:break
  digest=hashlib.sha256(f'course-academy/question-selection/v1/{seed}'.encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53);draws.append(eligible[int(u*len(eligible))])
 selection.append({'excluded_indices':[i for i in range(len(rs)) if mask>>i&1],'eligible_indices':eligible,'draws':dict(collections.Counter(draws)),'keys_remaining':sorted({information(rs[i])[1] for i in eligible})})
prev=load(JOB/'review-0-policy-2-8b996ed7d80a08a9/selection-analysis.json')
save('selection-analysis.json',{'implementation':'engine/rust/question_selection.rs::seen_before_task/select','basis':5578,'facts':prev['facts'][:4], 'method':'Read actual rules again. Conditional easy-only pool: reproduce hash draw for 100 seed strings and every one of 32 history subsets. Candidate indexes stand in for future entity IDs; order affects mapping but not reachability.','subsets':selection,'limits':['No live learner history, future database IDs, or active policy weights supplied. With positive easy weight all eligible easy records are reachable. Zero easy weight excludes this package. Unconfigured policy selects smallest entity ID; no claim of random variety then. Single remaining candidate naturally has no within-pool diversity; this is not evidence of a structural key cue.','Stored original sources are separate instructional evidence. No generated historical records exist in captured inventory.']})
# CLI rejection/resampling data from actual executable.
rj=load(ROOT/'rejection-records.json')
save('rejection-analysis.json',{'command':rj['command'],'raw_profile_target_counts':dict(collections.Counter(str(r['generation']['parameters']['target']) for r in rj['raw'])),'cli_profile_target_counts':dict(collections.Counter(str(r['generation']['parameters']['target']) for r in rj['cli'])),'raw_count':len(rj['raw']),'raw_unique':len({r['generation']['mathematical_fingerprint'] for r in rj['raw']}),'cli_count':len(rj['cli']),'construction':'Normal generator selects one of 12 profiles, target 0..4, independent signs and shifts, with scale 1. CLI retries up to max(100,count*100), rejecting repeated mathematical fingerprints. No correctness-based rejection. Replay exhaustion and inconsistent template/profile are rejected rather than silently returning fewer records.','limitations':'Focused finite stream exercises duplicate rejection only when duplicates occur; code inspected for rejection predicate.'})
print(json.dumps({'batch_overall':[{k:v for k,v in row.items() if k not in ['predictions','keys']} for row in res['batch'] if row['subgroup']=='overall'],'controlled_after':{p:v['keys'] for p,v in coverage['delivered_controlled'].items()}},indent=2))
