import review as v
import json,copy,hashlib,sys
from collections import Counter,defaultdict
from pathlib import Path
m=v.load_generator(v.JOB/'workspace/17592186161966.py')
# Instrument the real rejection loop without altering its results or package files.
trace=[];original=m.recipes
for rec in json.load(open(v.ROOT/'samples.json')):
 calls=[]
 def wrapper(profile,a,b):
  bank=original(profile,a,b);calls.append({'profile':profile,'pair':[a,b],'unique_choices':len(set(bank))});return bank
 m.recipes=wrapper
 got=m.generate(seed=rec['generation']['seed'],bank_profile=rec['generation']['bank_profile'])
 assert got==rec
 trace.append({'seed':rec['generation']['seed'],'profile':rec['generation']['bank_profile'],'attempts':calls[:-1],'accepted_pair':calls[-1]['pair']})
m.recipes=original
v.save('rejection-trace.json',trace)
v.save('rejection-summary.json',{'attempts':sum(len(t['attempts']) for t in trace),'outputs':len(trace),'bank_collision_rejections':sum(a['unique_choices']!=5 for t in trace for a in t['attempts']),'profiles':{p:{'attempts':sum(len(t['attempts']) for t in trace if t['profile']==p),'outputs':sum(t['profile']==p for t in trace)} for p in m.PROFILES}})
# Independent source bank check for intentionally excluded unrated profile.
src=json.load(open(v.JOB/'source/source.json'))['material']['kp']
q=next(q for q in src[':knowledge-point/questions'] if q[':question/math-academy-id']=='q-91208')
expected=sorted(tuple(o[2] for o in v.ops(a[':answer/value'])) for a in q[':question/answer-fields'][0][':answer-field/choices'])
v.save('unrated-source-bank.json',{'source_id':q[':question/id'],'original_question':q,'recipe_bank':original('q-91208',5,-3),'complete_bank_matches':sorted(original('q-91208',5,-3))==expected,'normal_generation':'Explicitly unsupported because captured difficulty absent; arithmetic/key inferred independently (+5,-3). No new rating assigned.'})
v.save('source-inputs.json',src)
# all allowed row/pivot/given assignments with bounded, deliberately unequal multipliers
boundary=[]
for r in range(4):
 for p in range(4):
  cols=[c for c in range(4) if c!=p];ks=[0]*4
  for c,k in zip(cols,[-2,3,-4]):ks[c]=k
  A=[[1+i*4+j for j in range(4)] for i in range(4)];A[r][p]=-2
  for c in cols:A[r][c]=-ks[c]*A[r][p]
  for g in cols:
   rec=m.generate(seed=7911,bank_profile='q-130619',parameters={'A':A,'row':r,'pivot':p,'given':g,'ks':ks});v.inspect(rec);boundary.append(rec)
v.save('role-boundaries.json',boundary)
v.save('role-boundary-results.json',{'passed':True,'count':len(boundary),'parameters':'All 48 row/pivot/given tuples, pivot -2, additive multipliers -2,3,-4. Matrix arithmetic and complete solution parsed from output.'})
# UI hashes choice UUIDs using field/item identity; positions in generator JSON are not UI positions.
def fnv(s):
 n=2166136261
 for c in s:n=((n^ord(c))*16777619)&0xffffffff
 return n
def first_ui(rec,item):
 f=v.field(rec);choices=sorted(f[':answer-field/choices'],key=lambda a:fnv(f"{item}:{f[':answer-field/id']}:{a[':answer/id']}"));return choices[0][':answer/id']==f[':answer-field/correct'][1]
stages=[];position=[]
for name,path in [('fresh','samples.json'),('fresh-delivered','delivery-samples/accepted.json'),('batch','batch.json'),('batch-delivered','delivery-batch/accepted.json')]:
 rs=json.load(open(v.ROOT/path));app=[r for r in rs if v.shortcut(r)!=None]
 stages.append({'stage':name,'path':path,'count':len(rs),'shortcut_applicable':len(app),'shortcut_correct':sum(v.shortcut(r)==v.correct_index(r) for r in app),'profiles':dict(Counter(r['generation']['bank_profile'] for r in rs)),'sign_pairs':dict(Counter(str(tuple(1 if x>0 else -1 for x in v.coefficients(r)[v.correct_index(r)])) for r in rs))})
 for p in sorted({r['generation']['bank_profile'] for r in rs}):
  subset=[r for r in rs if r['generation']['bank_profile']==p]
  position.append({'set':name,'profile':p,'strategy':'Select first visible UI option, actual FNV ordering, item id 1001 (explicit fixture identity)','correct':sum(first_ui(r,1001) for r in subset),'total':len(subset),'baseline':0.2})
v.save('delivery-stage-results.json',stages);v.save('ui-position-probes.json',position)
# Exact selection algorithm for eligible all-moderate candidates depends only on the second digest slice.
# Demonstrate a possible history: all captured source questions already seen, batch fresh.
rs=json.load(open(v.ROOT/'delivery-batch/accepted.json'))
selected=[]
for slot in range(100):
 seed=f'task-91023/kp-17592186161966/slot-{slot}';digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(digest[8:16],'big')>>11)/2**53;rank=int(u*len(rs));selected.append({'seed':seed,'candidate_rank':rank,'record_id':rs[rank]['question'][':question/id'],'shortcut':v.shortcut(rs[rank]) is not None})
v.save('selection-analysis.json',{'rule_sources':['engine/rust/learning.rs:151 retired questions rejected','engine/rust/learning.rs:595 candidates exclude seen and invalid practice','engine/rust/question_selection.rs:select sorts distinct entity IDs, selects weighted band, then uniform within band'], 'captured_basis':5579,'assumptions':'Read-only possible-history scenario: 13 captured originals already seen; five delivered candidates fresh and usable; moderate band has positive policy weight. Candidate rank uses batch order as an illustrative future entity ordering. No actual future entity IDs or learner history are claimed.','analytic_result':'All candidates are moderate. Positive moderate weight yields uniform probability 1/5 each; shortcut subgroup retains probability 2/5 for every entity ordering. Removing any source candidates or changing nonzero moderate weight cannot remove the weakness. If moderate weight is zero none are selected. With no configured distribution first entity wins; no coverage guarantee is asserted.','draws':selected,'shortcut_draws':sum(s['shortcut'] for s in selected),'limits':['No database queries or mutations; live policy and learner history are absent from snapshot.','Retirement/source-question eligibility does not create any eligible generated historical inventory record; none captured.']})
# Minimal delivered counterexample, including full record.
r=next(r for r in rs if v.shortcut(r)!=None)
v.save('minimal-shortcut.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce.py','record':r,'choice_coefficients':v.coefficients(r),'predicted_index':v.shortcut(r),'independent_correct_index':v.correct_index(r),'explanation':'Four choices have absolute pair (3,2); singleton has (2,3) with positive signs. Negate and swap singleton (+2,+3) to (-3,-2), without inspecting matrices.'})
print(json.dumps({'stages':[(s['stage'],s['count'],s['shortcut_correct']) for s in stages],'rejection_attempts':sum(len(t['attempts']) for t in trace),'boundary_cases':len(boundary),'selection_shortcut_draws':sum(s['shortcut'] for s in selected)}))
