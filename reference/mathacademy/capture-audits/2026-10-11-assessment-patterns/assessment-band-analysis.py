import json,bisect
from pathlib import Path
from datetime import datetime
from collections import defaultdict,Counter
O=Path(__file__).resolve().parent
R=O.parents[3]
rows=json.loads((O/'topic-age-evidence.json').read_text())['rows']
want=defaultdict(set)
for r in rows:want[r['account']].add(r['topic_id'])
def epoch(t):
 if not t:return None
 return float(t) if isinstance(t,(float,int)) else datetime.fromisoformat(t).timestamp()
obs=defaultdict(list); count=Counter()
def add(account,p,courses,fallback=None):
 for c in courses:
  t=epoch(c.get('captured_at') or fallback)
  if not t:continue
  for q in c.get('topics',[]):
   tid=str(q.get('topic_id'))
   if tid not in want[account]:continue
   obs[account,tid].append({'time':t,'band':q.get('display_band'),'color':q.get('color'),'course_id':str(c.get('course_id')),'title':q.get('title'),'source':str(p.relative_to(R)),'html_path':c.get('html_path')})
for a,base in [('foundations',R/'reference/mathacademy/question-capture')]+[(a,R/f'reference/mathacademy/question-capture-workers/{a}') for a in ['linear','differential','multivariable']]:
 for p in base.glob('*/knowledge-state/*.json'):
  d=json.loads(p.read_text()); add(a,p,d.get('courses',[]),d.get('finished_at'));count[a]+=1
for p in (R/'reference/mathacademy/capture').glob('*/*/post-activity.json'):
 a=p.parts[-3];d=json.loads(p.read_text()); entries=[d.get('observations',{})]+[h.get('observations',{}) for h in d.get('observation_history',[])]
 for e in entries:add(a,p,e.get('courses',[]),e.get('observed_at'))
 count[a]+=1
for k,v in obs.items():
 dd={(r['time'],r['source'],r['course_id']):r for r in v};obs[k]=sorted(dd.values(),key=lambda r:r['time'])
out=[]
for r in rows:
 l=obs[r['account'],r['topic_id']];ts=[o['time'] for o in l];n=bisect.bisect_right(ts,r['assessment_time']);before=l[n-1] if n else None
 # strictly at or before first observed offer; the nearest later snapshot is reported separately, never used as pre-offer evidence.
 after=l[n] if n<len(l) else None
 out.append({**r,'pre_offer_band':before,'pre_offer_observation_gap_seconds':r['assessment_time']-before['time'] if before else None,'first_later_band':after,'first_later_gap_seconds':after['time']-r['assessment_time'] if after else None})
first_topics=json.loads((O/'fire-timing-followup.json').read_text())['first_quiz_topics']
no_review=[]
for f in first_topics:
 if f['recorded_prior_reviews']: continue
 r=next(r for r in out if r['account']==f['account'] and r['quiz_id']==f['quiz_id'] and r['topic_id']==f['topic_id'])
 lesson=r['first_observed_lesson']; prefix=str(Path(lesson['source']).parent)+'/'
 own=[o for o in obs[r['account'],r['topic_id']] if o['source'].startswith(prefix) and o['time']<=r['assessment_time']]
 initial=own[0] if own else None
 history=[o for o in obs[r['account'],r['topic_id']] if initial and initial['time']<=o['time']<=r['assessment_time']]
 bands=[o['band'] for o in history if isinstance(o['band'],int)]
 no_review.append({'account':r['account'],'quiz_id':r['quiz_id'],'topic_id':r['topic_id'],'age_hours':r['age_hours'],'lesson_id':lesson['task_id'],'initial_lesson_band':initial,'pre_offer_band':r['pre_offer_band'],'pre_offer_observation_gap_seconds':r['pre_offer_observation_gap_seconds'],'observed_numeric_bands':dict(Counter(bands)),'highest_observed_band':max(bands) if bands else None,'history':history})
(O/'assessment-band-no-review-histories.json').write_text(json.dumps(no_review,indent=2)+'\n')
ordinary=[r for r in out if not r['retake']]
known=[r for r in ordinary if r['pre_offer_band']]
recent=[r for r in known if r['pre_offer_observation_gap_seconds']<=3600]
summary={'input_snapshot_files':dict(count),'ordinary_question_appearances':len(ordinary),'known_preoffer_appearances':len(known),'numeric_known_count':sum(isinstance(r['pre_offer_band']['band'],int) for r in known),'recent_numeric_known_count':sum(isinstance(r['pre_offer_band']['band'],int) for r in recent),'all_band_distribution':dict(Counter(str(r['pre_offer_band']['band']) for r in known)),'recent_within_1h_appearances':len(recent),'recent_within_1h_band_distribution':dict(Counter(str(r['pre_offer_band']['band']) for r in recent))}
(O/'assessment-band-evidence.json').write_text(json.dumps({'summary':summary,'rows':out},indent=2)+'\n')
print(json.dumps(summary,indent=2))
print('No-review initial/final/history band1:')
for r in no_review:
 if r['highest_observed_band']==1: print({k:v for k,v in r.items() if k!='history'})

