import sys
sys.dont_write_bytecode=True
from audit import *
from collections import Counter

def summary(rs):
 d={}
 for r in rs:
  i=r['generation']['instance'];t=i['template'];c=d.setdefault(t,{'count':0,'roles':Counter(),'key_positions':Counter(),'attempts':Counter(),'scalars':Counter()});c['count']+=1
  c['roles'][str(i.get('pair', [i.get('target'),i.get('donor')]))]+=1
  f=r['question'][':question/answer-fields'][0];c['key_positions'][next(n for n,x in enumerate(f[':answer-field/choices']) if x[':answer/id']==key(r['question']))+1]+=1
  c['attempts'][i.get('entry_attempts',1)]+=1
  c['scalars'][str(i.get('factor',i.get('coefficient')))]+=1
 return d

def probes(rs,refs,scope_tag=''):
 out=[]
 for t in sorted(set(r['generation']['template'] for r in rs)):
  sub=[r for r in rs if r['generation']['template']==t]
  for cue in ['first-position','largest-magnitude','smallest-magnitude']:
   hits=0
   for r in sub:
    f=r['question'][':question/answer-fields'][0];cs=f[':answer-field/choices'];mags=[sum(abs(x) for row in matrices(c[':answer/value'])[0] for x in row) for c in cs]
    pick=0 if cue=='first-position' else (max if cue=='largest-magnitude' else min)(range(5),key=lambda n:mags[n])
    hits+=cs[pick][':answer/id']==key(r['question'])
   out.append({'cue':cue,'subgroup':scope_tag+t,'scope':'within_template','strategy':'Choose '+cue+' option, with display-order tie breaking','correct':hits,'total':len(sub),'baseline':.2,'disposition':'not_predictive','conclusion':'Comparison baseline is uniform guessing among five choices. No tested cue predicts every response; finite small-batch rates are descriptive.','sample_refs':refs})
 return out

def select(candidates,weights,seed):
 # Faithful question_selection.rs::select: sorted unique IDs, band first, then uniform within band.
 bands=[sorted({id for id,band in candidates if band==b}) for b in ['easy','moderate','hard']]
 h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 uniform=lambda off:(int.from_bytes(h[off:off+8],'big')>>11)/2**53
 total=sum(w for w,p in zip(weights,bands) if p)
 if not total:return None
 draw=uniform(0)*total;chosen=None
 for j,(w,p) in enumerate(zip(weights,bands)):
  if not p or w==0:continue
  chosen=j
  if draw<w:break
  draw-=w
 p=bands[chosen];return p[int(uniform(8)*len(p))]

def main():
 raw=json.load(open(OUT/'easy-samples.json'));accepted=json.load(open(OUT/'delivery-sample/accepted.json'));batch=json.load(open(OUT/'runner-batch.json'));ab=json.load(open(OUT/'delivery-batch/accepted.json'))
 # prepare_records retains generation metadata; compare case distributions from delivered data.
 stage={'raw':summary(raw),'accepted':summary(accepted),'batch_raw':summary(batch),'batch_accepted':summary(ab)}
 save('stage-coverage.json',stage)
 # IDs assigned only for this read-only selection model; arbitrary monotonic IDs cannot change uniform within-band coverage.
 inventory=json.load(open(JOB/'source/inventory.json'));cand=[];records={};index=1
 for q in inventory['questions']:
  band=q.get(':question/difficulty',{});band=band.get(':db/ident','') if isinstance(band,dict) else band;band=band.split('/')[-1]
  if band in ['easy','moderate','hard']:cand.append((q[':db/id'],band));records[q[':db/id']]={'question':q}
 for r in ab:cand.append((index,'easy'));records[index]=r;index+=1
 tests=[]
 # No learner state supplied: exercise no history and a history excluding all captured questions.
 for fresh in [False,True]:
  cc=[c for c in cand if not fresh or c[0]<index]
  counts=Counter(select(cc,[1,0,0],f'audit-{n}') for n in range(1000))
  tests.append({'history':'captured inventory excluded as previously seen' if fresh else 'none excluded','weights':[1,0,0],'counts':dict(counts),'batch_selected':{str(k):v for k,v in counts.items() if k<index},'batch_question_ids':{str(k):r['question'][':question/id'] for k,r in records.items() if k<index}})
 save('selection-results.json',{'source':'engine/rust/question_selection.rs::select and seen_before_task','faithful_readonly_model':True,'tests':tests,'limits':['No learner/task/policy snapshot provided. Conditional tests use a positive easy-band weight; zero weight makes easy records ineligible. Unknown/unrated fallback and default no-policy first-ID behavior inspected in code, not claimed as live distribution.','No generated records were published and no actual database entity IDs were allocated. Model IDs test the uniform easy-band rule, not the exact next learner draw.']})
 ps=probes(raw,['easy-samples.json'],'sample:')+probes(ab,['delivery-batch/accepted.json'],'batch:')+probes([r for r in json.load(open(OUT/'samples.json')) if r['generation']['difficulty']!='easy'],['samples.json'],'sample:')
 save('shortcut-results.json',ps)
 print(json.dumps(stage,default=dict)[:2200]);print('perfect cues',[(p['subgroup'],p['cue']) for p in ps if p['correct']==p['total']])
if __name__=='__main__':main()
