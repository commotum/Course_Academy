import json,collections,re
from pathlib import Path
H=Path(__file__).resolve().parent;s=json.loads((H/'current.json').read_text());qs={q[':db/id']:q for q in s['questions']};ks={k[':db/id']:k for k in s['knowledge_points']}
for t in s['topics']:
 lines=[]
 for kid in t['kp_ids']:
  k=ks[kid];lines+=['# '+k[':knowledge-point/title']]
  ids=[k[':knowledge-point/canonical-example'][':db/id']]+[x[':db/id']for x in k.get(':knowledge-point/questions',[])]
  for eid in ids:
   q=qs[eid];lines += ['\n## '+str(eid)+' '+q.get(':question/math-academy-id',''),q[':question/problem'],'SOLUTION: '+q.get(':question/worked-solution','MISSING')]
   for f in q.get(':question/answer-fields',[]):
    lines+=['FIELD '+str(f[':db/id'])+' '+f[':answer-field/key']+' '+f[':answer-field/type'][':db/ident']]
    for a in f[':answer-field/choices']:lines+=['  '+('* 'if a[':db/id']==f.get(':answer-field/correct',{}).get(':db/id')else'  ')+str(a[':db/id'])+' '+a[':answer/type'][':db/ident']+' '+a[':answer/value']]
 (H/(str(t['ma_id'])+'-review.txt')).write_text('\n'.join(lines))
print([(t['ma_id'],len((H/(str(t['ma_id'])+'-review.txt')).read_text()))for t in s['topics']])
