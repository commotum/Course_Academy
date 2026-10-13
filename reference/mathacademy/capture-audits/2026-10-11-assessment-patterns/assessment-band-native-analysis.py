import json,csv
from pathlib import Path
from collections import defaultdict,Counter
from datetime import datetime
O=Path(__file__).resolve().parent;R=O.parents[3];e=json.loads((O/'evidence.json').read_text());d=json.loads((O/'assessment-band-evidence.json').read_text());members={m['course_id']:{t['topic-id'] for t in csv.DictReader(Path(m['membership_source']).open())} for m in e['xp_topic_membership_metrics']}
rs=[r for r in d['rows'] if not r['retake'] and r['pre_offer_band'] and r['pre_offer_band']['band']==1 and r['pre_offer_observation_gap_seconds']<=3600 and r['topic_id'] in members.get(r['course_id'],set())];want=defaultdict(dict)
for r in rs:want[r['account']][r['topic_id']]=r
hist=defaultdict(list)
def add(a,p,cs):
 for c in cs:
  t=c.get('captured_at');t=float(t) if isinstance(t,(int,float)) else datetime.fromisoformat(t).timestamp() if t else None
  if t is None:continue
  for q in c.get('topics',[]):
   tid=str(q.get('topic_id'));r=want[a].get(tid)
   if r and t<=r['assessment_time'] and t>=r['first_observed_lesson']['age_anchor']-60:
    hist[a,tid].append({'time':t,'band':q.get('display_band'),'source':str(p.relative_to(R)),'course_id':c['course_id']})
for a in want:
 base=R/'reference/mathacademy/question-capture' if a=='foundations' else R/f'reference/mathacademy/question-capture-workers/{a}'
 for p in base.glob('*/knowledge-state/*.json'):add(a,p,json.loads(p.read_text()).get('courses',[]))
 for p in (R/f'reference/mathacademy/capture/{a}').glob('*/post-activity.json'):
  data=json.loads(p.read_text());add(a,p,data.get('observations',{}).get('courses',[]))
  for x in data.get('observation_history',[]):add(a,p,x.get('observations',{}).get('courses',[]))
for r in rs:
 h=sorted({(x['time'],x['source'],x['course_id']):x for x in hist[r['account'],r['topic_id']]}.values(),key=lambda x:x['time']);bs=[x['band'] for x in h if isinstance(x['band'],int)];r['history']=h;r['max']=max(bs) if bs else None;print(r['account'],r['topic_id'],'max',r['max'],'counts',dict(Counter(bs)))
(O/'assessment-band-native-low-histories.json').write_text(json.dumps(rs,indent=2))
