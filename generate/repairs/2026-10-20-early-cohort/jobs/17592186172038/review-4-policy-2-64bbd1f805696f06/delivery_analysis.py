import json,pathlib,hashlib,collections,math,copy
from audit import fields,answer,save,visible_bank,mirror_probe
from fractions import Fraction as F
ROOT=pathlib.Path.cwd();load=lambda n:json.loads((ROOT/n).read_text());raw=load('delivery-input.json');batch=load('runner-batch.json');gmap={}
for r in raw+batch:
 for a in fields(r)[':answer-field/choices']:
  p=pathlib.Path(a[':answer/value']);gmap[hashlib.sha256(p.read_bytes()).hexdigest()]=json.loads(p.with_suffix('.json').read_text())['slopes']
def rows(r,folder=None):
 out=[]
 for a in fields(r)[':answer-field/choices']:
  p=(ROOT/folder/'assets'/a[':answer/value']) if folder else pathlib.Path(a[':answer/value']);out.append([F(v) for v in gmap[hashlib.sha256(p.read_bytes()).hexdigest()]])
 return out
def ci(r):return next(i for i,a in enumerate(fields(r)[':answer-field/choices']) if a[':answer/id']==fields(r)[':answer-field/correct'][1])
def sg(v):return (v>0)-(v<0)
def predictions(rr):
 signs=[[sg(v) for v in row] for row in rr];pairs=[(i,j) for i in range(5) for j in range(i) if all(a==-b for a,b in zip(rr[i],rr[j]))]
 mirror=None
 if len(pairs)==1:
  pair=pairs[0];scores={i:sum(a==b and a!=0 for j in range(5) if j not in pair for a,b in zip(signs[i],signs[j])) for i in pair};wins=[i for i in pair if scores[i]==max(scores.values())]
  if len(wins)==1:mirror=wins[0]
 score={
 'most_horizontal':[sum(v==0 for v in row) for row in rr],
 'most_positive':[sum(v>0 for v in row) for row in rr],
 'most_negative':[sum(v<0 for v in row) for row in rr],
 'greatest_total_steepness':[sum(abs(math.atan(float(v))) for v in row) for row in rr],
 'smallest_total_steepness':[-sum(abs(math.atan(float(v))) for v in row) for row in rr],
 'direction_consensus':[sum(a==b for j in range(5) if j!=i for a,b in zip(signs[i],signs[j])) for i in range(5)]}
 pred={k:max(range(5),key=lambda i:v[i]) for k,v in score.items()};pred.update(first_position=0,last_position=4,mirror_consensus=mirror);return pred
stages=[];grader=[]
for stage,recs,folder in [('fresh_independent',load('independent-samples.json'),None),('raw_independent',raw,None),('raw_runner',batch,None),('accepted_independent',load('delivery-independent/accepted.json'),'delivery-independent'),('accepted_runner',load('delivery-runner/accepted.json'),'delivery-runner'),('fixed_bank_counterfactuals',load('counterfactual-records.json')[:30],None)]:
 obs=[]
 for r in recs:
  rr=rows(r,folder);pr=predictions(rr);idx=ci(r);obs.append({'question_id':r['question'][':question/id'],'seed':r['generation']['seed'],'template':r['generation']['template'],'correct_position':idx+1,'slope_rows':[[str(v) for v in row] for row in rr],'predictions':{k:None if v is None else {'position':v+1,'correct':v==idx} for k,v in pr.items()}})
  if folder:
   f=fields(r);grader.append({'label':stage+' '+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if i==idx else 'rejected','purpose':'post-normalization complete bank; independent PNG hash/geometry match'} for i,a in enumerate(f[':answer-field/choices'])]})
 summary=[]
 for subgroup in ['overall']+sorted({r['template'] for r in obs}):
  oo=[r for r in obs if subgroup=='overall' or r['template']==subgroup]
  for k in predictions(rows(recs[0],folder)):
   pp=[r['predictions'][k] for r in oo if r['predictions'][k] is not None]
   if pp:summary.append({'subgroup':subgroup,'strategy':k,'correct':sum(p['correct'] for p in pp),'total':len(pp),'baseline':0.2})
 stages.append({'stage':stage,'count':len(recs),'templates':dict(collections.Counter(r['template'] for r in obs)),'records':obs,'strategies':summary})
# Fixed bank has unchanged pixels/order and each of five diagrams is correct once: any equation-free deterministic strategy must score 1/5 when it makes a prediction.
fixed=next(s for s in stages if s['stage']=='fixed_bank_counterfactuals')
for s in fixed['strategies']:
 assert s['correct']*5==s['total'],s
save('delivered-shortcuts.json',stages);save('delivered-grader-input.json',grader)
# Ensure every controlled answer role remains after real normalization/dedup; compare content/geometry rather than prepublication UUIDs.
accepted=load('delivery-independent/accepted.json')+load('delivery-runner/accepted.json');present={r['generation']['content_fingerprint'] for r in accepted};control=load('counterfactual-records.json')[:30];assert all(r['generation']['content_fingerprint'] in present for r in control)
# Faithful selection reproduction from reviewed Rust selector, with actual captured records and explicitly virtual IDs for unpublished accepted records.
inv=load('../source/inventory.json');pool={q[':db/id']:{'question_id':q[':question/id'],'band':q.get(':question/difficulty',{}).get(':db/ident','').rsplit('/',1)[-1],'origin':'captured','template':'source' if q.get(':question/math-academy-id') else 'historical_generated'} for q in inv['questions'] if q.get(':question/answer-fields',[{}])[0].get(':answer-field/correct')}
for i,r in enumerate(accepted):pool[17592187000000+i]={'question_id':r['question'][':question/id'],'band':'easy','origin':'hypothetical_accepted','template':r['generation']['template'],'fingerprint':r['generation']['content_fingerprint']}
def select(weights,seed,seen=()):
 ids=sorted(e for e in pool if e not in seen)
 if weights is None:return ids[0] if ids else None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=lambda off:(int.from_bytes(digest[off:off+8],'big')>>11)/(1<<53)
 bands=[[e for e in ids if pool[e]['band']==b] for b in ['easy','moderate','hard']];unrated=[e for e in ids if not pool[e]['band']];total=sum(w for w,b in zip(weights,bands) if b)
 if total:
  draw=u(0)*total
  for j,w in enumerate(weights):
   if not bands[j] or not w:continue
   chosen=j
   if draw<w:break
   draw-=w
  candidates=bands[chosen]
 else:candidates=unrated
 return candidates[int(u(8)*len(candidates))] if candidates else None
selection=[]
for weights in [[1,0,0],[6,3,1],None]:
 for hist in [[],[min(pool),max(pool)]]:
  draws=[select(weights,'review4/'+str(i),hist) for i in range(256)];assert not set(draws)&set(hist)
  selection.append({'weights':weights,'seen':hist,'draws':draws,'templates':dict(collections.Counter(pool[e]['template'] for e in draws)),'bands':dict(collections.Counter(pool[e]['band'] for e in draws))})
# Algebraic reachability under positive easy weight: uniform on complete easy candidate pool; all 30 role records represented with identical per-candidate probability.
counts=collections.Counter(v['band'] for v in pool.values());save('selection-results.json',{'basis':inv['basis'],'implementation':'question_selection.rs select + seen_before_task; weighted band SHA256 uniform(0), sorted unique pool uniform(8); None chooses first.','candidate_records':pool,'fresh_counts':dict(counts),'fixtures':selection,'controlled_role_reachability':{'roles':len(control),'all_present_after_dedup':True,'easy_only_probability_each':1/counts['easy']},'limits':['Candidate IDs for unpublished accepted records are explicit fixtures; no database writes.','Actual learner history, active policy weights and concurrent inventory are unavailable; fixtures test the supplied selection rule, not a live user sequence.','Unrated source records with missing keys are unusable and excluded.']})
save('delivery-summary.json',{'raw':len(raw),'accepted':len(load('delivery-independent/accepted.json')),'runner_raw':len(batch),'runner_accepted':len(load('delivery-runner/accepted.json')),'controlled_roles':30,'roles_preserved':True,'post_delivery_strategy_results':[{k:s[k] for k in ['stage','count','templates','strategies']} for s in stages if 'accepted' in s['stage']],'fixed_bank_strategy_results':fixed['strategies']})
print('delivery',len(raw),'->',len(load('delivery-independent/accepted.json')),'runner',len(batch),'->',len(load('delivery-runner/accepted.json')),'all30 roles retained; fixed-bank equation-free probes each at 1/5')
