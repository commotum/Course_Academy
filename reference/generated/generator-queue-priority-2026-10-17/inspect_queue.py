"""Read saved queue metadata only. No database access and no job mutations."""
import collections,json,sys,time
from pathlib import Path
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'scripts'))
from inventory_jobs import InventoryJobs,priority_key
HERE=ROOT/'reference/generated/generator-queue-priority-2026-10-17'
queue=ROOT/'.local/learning/inventory/math/59d5cf13-351c-4114-be19-4c3bb64ee051'
readiness=json.loads((ROOT/'reference/generated/selected-topics-readiness-2026-10-17/result.json').read_text())
targets={t['topic']:t for t in readiness['topics'] if not t['content_ready_for_fresh_lesson']}
deficient={k['kp'] for t in targets.values() for k in t['knowledge_points'] if k['needed']}
now=time.time();cursor=json.loads((queue/'cursor.json').read_text());jobs=[]
for path in queue.glob('*.json'):
 if path.name=='cursor.json':continue
 j=json.loads(path.read_text());r=j.get('request')
 if not r:continue
 j['_path']=path
 jobs.append(j)
builds=[j for j in jobs if j['request'].get('jobKind','build')=='build']
for j in builds:j['_recoverable']=InventoryJobs.recoverable(j['_path'],j)
score_sorted=sorted([j for j in builds if j['state'] in ('pending','running')],key=lambda j:(*priority_key(j['request']),j['key']))
eligible=sorted([j for j in score_sorted if j.get('retryAt',0)<=now],key=lambda j:(not j['_recoverable'],*priority_key(j['request']),j['key']))
score_ranks={j['key']:i for i,j in enumerate(score_sorted,1)};worker_ranks={j['key']:i for i,j in enumerate(eligible,1)}
def compact(j):
 r=j['request'];return {**{k:r.get(k) for k in ('topic','knowledgePoint','score','purpose','shortage','urgency_value','waiting_since','next_activity','difficulty','stage','jobKind','basis')},'state':j['state'],'score_rank':score_ranks.get(j['key']),'worker_order':worker_ranks.get(j['key']),'recoverable':j.get('_recoverable',False),'in_backoff':j.get('retryAt',0)>now,'deficient_in_audit':r['knowledgePoint'] in deficient,'path':str(j['_path'].relative_to(ROOT))}
selected=[compact(j) for j in jobs if j['request']['topic'] in targets]
selected.sort(key=lambda j:(j['topic'],j['knowledgePoint'],j['jobKind'] or '',j['difficulty'] or ''))
result={'captured_at_unix':now,'cursor':cursor,'database_reads':0,'queue_writes':0,'metadata_files':len(jobs),'build_states':dict(collections.Counter(j['state'] for j in builds)),'pending_running_builds':len(score_sorted),'ready_to_run_builds':len(eligible),'top_10':list(map(compact,eligible[:10])),'selected_jobs':selected,'deficient_kps':sorted(deficient)}
(HERE/'queue-snapshot.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('cursor','build_states','pending_running_builds','ready_to_run_builds','top_10')},indent=2))
for topic,t in targets.items():
 rows=[r for r in selected if r['topic']==topic and r['deficient_in_audit']]
 print(json.dumps({'topic':topic,'title':t['title'],'jobs':rows}))
