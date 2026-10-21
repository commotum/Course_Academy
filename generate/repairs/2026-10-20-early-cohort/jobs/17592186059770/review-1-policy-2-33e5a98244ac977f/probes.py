import sys
sys.dont_write_bytecode=True
from audit import *

def options(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return [(i,mat(a[':answer/value']),a[':answer/id']==f[':answer-field/correct'][1]) for i,a in enumerate(f[':answer-field/choices'])]
def minority(r):
 # Two-by-three matrices only. Find the coefficient cell with a 1:3 sign split.
 # This uses only choices, never the equations or generation metadata.
 cs=[x for x in options(r) if len(x[1])==2 and len(x[1][0])==3]
 if len(cs)!=4:return None
 votes=[]
 for row,col in itertools.product(range(2),repeat=2):
  signs=[sp.sign(x[1][row][col]) for x in cs];cnt=collections.Counter(signs)
  unique=[i for i,s in enumerate(signs) if cnt[s]==1]
  if len(unique)==1 and sorted(cnt.values())==[1,3]:votes.append(cs[unique[0]][0])
 return votes[0] if votes and len(set(votes))==1 else None

def precursor(r):
 cs=options(r);extras=[x for x in cs if len(x[1])==3 and len(x[1][0])==3 and x[1][-1]==[0,0,0]]
 if len(extras)!=1:return None
 hits=[i for i,m,_ in cs if m==extras[0][1][:2]]
 return hits[0] if len(hits)==1 else None

def shortcut(r):
 p=precursor(r)
 if p is not None:return p
 cs=[x for x in options(r) if len(x[1])==2 and len(x[1][0])==3]
 if len(cs)!=4:return None
 for row in range(2):
  signs=[sp.sign(x[1][row][0]) for x in cs];cnt=collections.Counter(signs)
  if sorted(cnt.values())==[1,3]:
   return next(x[0] for x,s in zip(cs,signs) if cnt[s]==1)
 return None

def measure(rs,name):
 out=[]
 for subgroup in ['all','q-129137','q-71731','q-71733','q-71734']:
  subset=[r for r in rs if subgroup=='all' or r['generation']['bank_profile']==subgroup]
  if not subset:continue
  for label,fn in [('shape then first-column sign singleton',shortcut),('choose first option',lambda r:0),('minority coefficient sign among 2x3 options',minority),('delete last zero row from extra-row option',precursor)]:
   trials=[]
   for r in subset:
    selected=fn(r)
    if selected is None:continue
    opts=options(r);trials.append({'id':r['question'][':question/id'],'selected_index':selected,'success':opts[selected][2]})
   if trials:out.append({'dataset':name,'subgroup':subgroup,'strategy':label,'correct':sum(t['success'] for t in trials),'total':len(trials),'trials':trials})
 return out

allrows=[];coverage={}
for n in ['sample.json','delivery-sample/accepted.json','batch.json','delivery-batch/accepted.json']:
 rs=load(E/n);allrows+=measure(rs,n);coverage[n]={'count':len(rs),'profile_targets':dict(collections.Counter(r['generation']['bank_profile']+'/'+r['generation']['target_recipe'] for r in rs)),'positions':dict(collections.Counter(qcheck(r)['correct_index'] for r in rs))}
save('shortcut-results.json',allrows);save('coverage.json',coverage)
# Independent read-only reproduction of Rust select: distinct sorted candidates,
# difficulty filtering and SHA256 draw; conditional easy-only pool follows same uniform item draw.
batch=load(E/'delivery-batch/accepted.json');ordered=sorted(batch,key=lambda r:r['question'][':question/id']);selected=[]
for seed in range(200):
 d=hashlib.sha256(f'course-academy/question-selection/v1/review-{seed}'.encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);selected.append(ordered[int(u*len(ordered))])
save('selection.json',{'basis':5346,'implementation':'engine/rust/question_selection.rs select, sort+dedup and uniform(8) in selected easy band','captured_limits':'inventory lacks learner history, policy weights and new database entity IDs. Synthetic entity ordering tests index-position selection under positive easy weight; no configured policy instead returns first eligible item. No live delivery claim.','all_fresh_counts':dict(collections.Counter(r['question'][':question/id'] for r in selected)),'no_policy':'candidates.first() with ascending entity IDs; any singleton remains selectable','shortcut_results':measure(selected,'200 synthetic easy draws')})
print(json.dumps([{k:x[k] for k in ['dataset','subgroup','strategy','correct','total']} for x in allrows if x['dataset'] in ['batch.json','delivery-batch/accepted.json']],indent=2))
