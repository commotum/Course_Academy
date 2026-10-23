import review as v
import json,hashlib
from collections import Counter
from pathlib import Path
R=v.ROOT

def load(f):return json.load(open(R/f))
def fnv(s):
 n=2166136261
 for c in s:n=((n^ord(c))*16777619)&0xffffffff
 return n

def predicted(rec,kind):
 pairs=v.coefficients(rec)
 if kind=='negative-swapped-singleton':return v.shortcut(rec)
 if kind=='first-authored':return 0
 if kind=='first-ui':
  f=v.field(rec);ids=[a[':answer/id'] for a in f[':answer-field/choices']]
  return min(range(5),key=lambda i:fnv(f"1001:{f[':answer-field/id']}:{ids[i]}"))
 if kind=='shortest-coefficients':return min(range(5),key=lambda i:(sum(map(abs,pairs[i])),pairs[i]))
 if kind=='mixed-signs':
  candidates=[i for i,p in enumerate(pairs) if p[0]*p[1]<0]
  return min(candidates,key=lambda i:pairs[i]) if candidates else None

stages=[];probes=[]
for stage,path in [('fresh','samples.json'),('fresh-delivered','delivery-samples/accepted.json'),('batch','batch.json'),('batch-delivered','delivery-batch/accepted.json'),('controlled-banks','role-records.json')]:
 rs=load(path)
 for x in rs:v.inspect(x)
 stages.append({'stage':stage,'sample_ref':path,'count':len(rs),'profiles':dict(Counter(x['generation']['bank_profile'] for x in rs)),'sign_pairs':dict(Counter(str(tuple(1 if a>0 else -1 for a in v.coefficients(x)[v.correct_index(x)])) for x in rs)),'correct_positions':dict(Counter(v.correct_index(x) for x in rs))})
 for p in [None]+sorted({x['generation']['bank_profile'] for x in rs}):
  subset=[x for x in rs if p is None or x['generation']['bank_profile']==p]
  for kind in ['negative-swapped-singleton','first-authored','first-ui','shortest-coefficients','mixed-signs']:
   selected=[(x,predicted(x,kind)) for x in subset if predicted(x,kind) is not None]
   if not selected:continue
   probes.append({'stage':stage,'profile':p or 'all','strategy':kind,'correct':sum(i==v.correct_index(x) for x,i in selected),'total':len(selected),'baseline':0.2,'sample_refs':[path]})
v.save('delivery-stage-results.json',stages);v.save('choice-probes.json',probes)
# All-moderate selection reproduces uniform-within-band ranking from Rust, no DB required.
rs=load('delivery-batch/accepted.json');draws=[]
for slot in range(25):
 seed=f'review-20261022/slot-{slot}';digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/2**53;i=int(u*len(rs));rec=rs[i]
 draws.append({'seed':seed,'rank':i,'record_id':rec['question'][':question/id'],'profile':rec['generation']['bank_profile'],'old_shortcut_correct':v.shortcut(rec)==v.correct_index(rec)})
v.save('selection-analysis.json',{'captured_basis':5579,'sources':['engine/rust/question_selection.rs:select','engine/rust/learning.rs:151,600'],'eligibility':'Retired/invalid and seen questions excluded before select. All current records valid moderate. Captured originals are not generated records.','scenario':'All captured originals seen; five batch candidates fresh. Positive moderate weight. Future entity ordering represented by batch rank; no actual entity IDs claimed.','draws':draws,'counts':dict(Counter(x['rank'] for x in draws)),'conclusion':'Uniform 1/5 per eligible moderate candidate under positive weight; no role-dependent weighting. Old shortcut answers zero matching batch members. Seen history may reduce available variation; zero moderate weight selects none; unconfigured policy takes first entity. No guarantee about unknown histories.','limits':['Read-only captured inventory, not live publication or learner state.','Future deduplication can change if inventory changes.'],'publication_preparation_exists':(v.JOB/'publication/preparation.json').exists()})
# Audit whole stored inventory; never classify source IDs as generated.
inv=load('inventory-audit.json');assert all(q['source_question'] and not q['generation_keys'] for q in inv['questions'])
# Batch sign cue narrows options but does not identify a unique choice.
v.save('batch-cue-analysis.json',{'records':[{'question_id':r['question'][':question/id'],'profile':r['generation']['bank_profile'],'pairs':v.coefficients(r),'correct_index':v.correct_index(r),'mixed_sign_choice_count':sum(a*b<0 for a,b in v.coefficients(r))} for r in rs],'judgment':'All five correct pairs have opposite signs, but each bank contains two or three such choices. Opposite signs alone does not produce an answer. These are different matrices and target roles, not sign-only repeats. Tested lexicographic mixed-sign, shortest-coefficient, fixed-position and negative-swap actions do not solve all five. Controlled identical-bank tests show signs are eligible, not fixed. Small batch does not establish broad sign coverage.'})
print(json.dumps({'stages':stages,'batch_probes':[x for x in probes if x['stage']=='batch' and x['profile']=='all']}))
