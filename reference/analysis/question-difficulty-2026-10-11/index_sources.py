"""Build slim, auditable source appearances without changing captures or EDB."""
from pathlib import Path
import json, re, collections, csv, sys
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
normalize={'E':'easy','M':'moderate','H':'hard','easy':'easy','moderate':'moderate','hard':'hard'}
rows={}; tasks={}; files=[]; problems=[]
def mid(q):
 x=q.get('math_academy_id') or q.get('id') or q.get('question_id') or q.get('dom_id')
 if not x:return None
 m=re.fullmatch(r'(?:step-)?(?:question-|q-)?(\d+)',str(x)); return 'q-'+m[1] if m else str(x)
def add_task(p,d,stream):
 tid=str(d.get('task_id') or '')
 if not tid:return
 typ=str(d.get('task_type') or d.get('kind') or '').lower()
 if typ not in ('lesson','review','assessment','multistep','diagnostic'):return
 state={}; sp=p.parent/'state.json'
 if sp.exists():
  try:state=json.loads(sp.read_text())
  except (ValueError,OSError) as e:problems.append([str(sp),str(e)])
 sq=state.get('questions') or {}; sq=sq if isinstance(sq,dict) else {}
 verification={}
 if stream=='manual-capture' and (p.parent/'verification.json').exists():verification=json.loads((p.parent/'verification.json').read_text())
 complete=bool(verification.get('score') or state.get('activity_complete') or state.get('lesson_complete') or state.get('review_complete') or state.get('assessment_complete') or state.get('multistep_complete') or state.get('diagnostic_complete') or d.get('completion'))
 # New content.json comes from its completed task history; retain that source metadata.
 qs=d.get('questions') or []
 if not isinstance(qs,list):return
 smap={mid(q):q for q in qs if isinstance(q,dict) and mid(q)}
 order=list(smap)
 order_method='content-list-order'
 if sq and set(order).issubset(set(sq)):
  order=[x for x in sq if x in smap]; order_method='capture-state-insertion-order'
 elif qs and all(q.get('sequence_position') is not None for q in qs):
  order=sorted(smap,key=lambda x:(int(smap[x]['sequence_position']),list(smap).index(x))); order_method='source-sequence-position'
 auto=stream in ('older-automated','recent-automated')
 policy=d.get('sequence_policy') or d.get('policy') or None
 task={'task_id':tid,'activity_type':typ,'stream':stream,'source_file':str(p),'complete':complete,'question_count':len(order),'course_id':d.get('course_id'),'topic_id':d.get('topic_id'),'order_method':order_method,'policy':policy,'priority':2 if stream=='recent-automated' else 1}
 if tid in tasks and tasks[tid]['activity_type']!=typ:problems.append(['task-type-conflict',tid,tasks[tid]['activity_type'],typ])
 if tid not in tasks or task['priority']>tasks[tid]['priority']: tasks[tid]=task
 kpcounts=collections.Counter()
 for i,x in enumerate(order,1):
  q=smap[x]; s=sq.get(x,{})
  kp=q.get('source_example_id') or q.get('knowledge_point_id') or q.get('kp_id') or s.get('kp_id') or q.get('knowledge_point')
  if kp is not None:kp=str(kp)
  kpcounts[kp]+=1
  position=kpcounts[kp] if typ=='lesson' and kp else i if typ!='lesson' else None
  diff=normalize.get(q.get('difficulty'))
  grade=q.get('source_grade') or q.get('grade') or q.get('result') or s.get('actual_result')
  html=q.get('raw_html') or q.get('html') or ''
  if not diff:
   m=re.search(r'questionDifficulty[^>]*difficulty(Easy|Moderate|Hard)',html)
   if m:diff=m[1].lower()
  row={'question_mid':x,'task_id':tid,'activity_type':typ,'source_difficulty':diff,'grade':grade,'kp_key':kp,'position_in_sequence':position,'task_position':i,'source_file':str(p),'source_question_file':q.get('html_path'),'complete':complete,'stream':stream,'order_method':order_method,'priority':task['priority']}
  key=(tid,x)
  if key not in rows or row['priority']>rows[key]['priority']:rows[key]=row
 files.append(str(p))
roots=[('older-automated',ROOT/'reference/mathacademy/question-capture'),('older-automated',ROOT/'reference/mathacademy/question-capture-workers'),('recent-automated',ROOT/'reference/mathacademy/capture')]
for stream,root in roots:
 ps=sorted(root.rglob('content.json'))
 for n,p in enumerate(ps,1):
  try:add_task(p,json.loads(p.read_text()),stream)
  except (ValueError,TypeError,OSError) as e:problems.append([str(p),str(e)])
  if n%200==0:print(stream,n,'/',len(ps),flush=True)
# Saved human history has direct task type and source DOM grouping/order.
progress={str(r['task-id']):r for r in csv.DictReader((ROOT/'reference/progress.csv').open())}
for p in sorted((ROOT/'reference/mathacademy/progress-history-2026-10-04').glob('*.json')):
 if not p.stem.isdigit():continue
 d=json.loads(p.read_text()); tid=str(d.get('task_id') or p.stem)
 typ=(progress.get(tid,{}).get('activity-type') or (re.match(r'\s*(Lesson|Review|Assessment|Multistep|(?:Supplemental )?Diagnostic)',d.get('task_text','')) or ['',''])[1]).lower().replace('supplemental diagnostic','diagnostic')
 if typ not in ('lesson','review','assessment','multistep','diagnostic'):problems.append(['unclassified-human-task',str(p)]);continue
 qs=d.get('questions') or []; qm={mid(q):q for q in qs if mid(q)}
 soup=BeautifulSoup(d.get('raw_html',''),'html.parser')
 groupmap={}; positions={}; ordered=[]
 for gi,kp in enumerate(soup.select('.kp'),1):
  for pos,node in enumerate(kp.select('.question[id]'),1):
   x=mid({'id':node.get('id')}); groupmap[x]=f'dom-kp-{gi}'; positions[x]=pos
 for node in soup.select('.question[id]'):
  x=mid({'id':node.get('id')})
  if x in qm and x not in ordered:ordered.append(x)
 if set(ordered)!=set(qm):ordered=list(qm);problems.append(['human-dom-order-incomplete',tid])
 task={'task_id':tid,'activity_type':typ,'stream':'human-history','source_file':str(p),'complete':True,'question_count':len(ordered),'course_id':progress.get(tid,{}).get('course-code'),'topic_id':progress.get(tid,{}).get('topic-id'),'order_method':'completed-task-DOM','policy':None,'priority':3}
 if tid not in tasks or tasks[tid]['priority']<3:tasks[tid]=task
 for i,x in enumerate(ordered,1):
  q=qm[x]; kp=groupmap.get(x) or q.get('kp_href') or q.get('kp_title')
  position=positions.get(x) if typ=='lesson' else i
  row={'question_mid':x,'task_id':tid,'activity_type':typ,'source_difficulty':normalize.get(q.get('difficulty')),'grade':q.get('result'),'kp_key':kp,'position_in_sequence':position,'task_position':i,'source_file':str(p),'source_question_file':None,'complete':True,'stream':'human-history','order_method':'completed-task-DOM','priority':3}
  rows[(tid,x)]=row
 files.append(str(p))
for root in sorted((ROOT/'reference/mathacademy').glob('multistep-*'))+sorted((ROOT/'reference/mathacademy').glob('assessment-*')):
 for name in ['content-import.json','content.json']:
  p=root/name
  if p.exists():
   add_task(p,json.loads(p.read_text()),'manual-capture');break
with (OUT/'source-appearances.jsonl').open('w') as f:
 for row in sorted(rows.values(),key=lambda x:(x['task_id'],x['task_position'])):f.write(json.dumps(row,default=str)+'\n')
(OUT/'source-tasks.json').write_text(json.dumps(list(tasks.values()),indent=2,default=str)+'\n')
(OUT/'source-index-metadata.json').write_text(json.dumps({'files':files,'errors':problems,'task_count':len(tasks),'appearance_count':len(rows),'type_counts':dict(collections.Counter(x['activity_type'] for x in tasks.values()))},indent=2)+'\n')
print('DONE',len(tasks),'tasks',len(rows),'appearances','issues',len(problems),flush=True)
