from pathlib import Path
import subprocess, os, json, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/"scripts/question_capture"))
from edn import loads, dumps, Tagged
ROOT=Path('/home/jake/Developer/Course_Academy')
OUT=ROOT/'reference/analysis/question-difficulty-2026-10-11'
env=os.environ.copy(); env['EDB_POSTGRES_URL']="host=/tmp/edb-math port=55432 dbname=math user=edb_peer sslmode=disable options='-c search_path=public'"; env['EDB_CONNECT_TIMEOUT_MS']='5000'; env['EDB_STATEMENT_TIMEOUT_MS']='15000'
queries={
 'questions':"""[:find [?q ...] :where [?q :question/id _]]""",
'question-identifiers':"""[:find ?q ?mid :where [?q :question/math-academy-id ?mid]]""",
'question-difficulties':"""[:find ?q ?diff :where [?q :question/difficulty ?d] [?d :db/ident ?diff]]""",
'activities':"""[:find ?a ?id ?title ?type :where [?a :activity/id ?id] [?a :activity/title ?title] [?a :activity/type ?t] [?t :db/ident ?type]]""",
'activity-steps':"""[:find ?a ?step :where [?a :activity/steps ?step]]""",
'multistep-steps':"""[:find ?m ?step :where [?m :multistep/steps ?step]]""",
'step-content':"""[:find ?s ?c :where [?s :step/content ?c]]""",
'knowledge-points':"""[:find [?kp ...] :where [?kp :knowledge-point/id _]]""",
'knowledge-point-topics':"""[:find ?t ?kp :where [?t :topic/knowledge-points ?kp]]""",
 'topics':"""[:find ?t ?tid ?title :where [?t :topic/math-academy-id ?tid] [?t :topic/title ?title]]""",
'assigned-content':"""[:find ?a ?c :where [?a :assigned-problem/content ?c]]""",
'knowledge-questions':"""[:find ?kp ?q :where [?kp :knowledge-point/questions ?q]]""",
'canonical-questions':"""[:find ?kp ?q :where [?kp :knowledge-point/canonical-example ?q]]""",
'question-task-links':"""[:find ?q ?task-id ?type :where [?q :question/difficulty _] [?item :task-item/content ?q] [?task :learner-task/items ?item] [?task :learner-task/math-academy-id ?task-id] [?task :learner-task/activity ?a] [?a :activity/type ?t] [?t :db/ident ?type]]""",
'policy':"""[:find (pull ?p [:db/id :policy/id {:policy/question-selection-weights [* {:question-weights/activity-type [:db/ident]}]}]) :where [?p :policy/id _]]"""
}
for name,q in queries.items():
 result_file=OUT/(name+'.edn')
 if result_file.exists(): print(name,'reusing existing output',flush=True); continue
 p=OUT/(name+'-query.edn')
 batches=[None]
 if name in ('question-identifiers','question-difficulties','knowledge-questions'):
  var='?kp' if name=='knowledge-questions' else '?q'
  q=q.replace(':where',':in $ ['+var+' ...] :where',1)
  ids=loads((OUT/('knowledge-points.edn' if name=='knowledge-questions' else 'questions.edn')).read_text())
  batches=[ids[i:i+2000] for i in range(0,len(ids),2000)]
 p.write_text(q+'\n'); rows=[]
 for i, batch in enumerate(batches):
  cmd=[str(ROOT/'.local/edb/capture-runtime/math-edb'),'query','--database','math','--as-of','1149','--file',str(p),'--timeout-ms','60000','--max-results','100000','--max-value-bytes','268435456','--max-join-bytes','134217728']
  if batch is not None:
   inp=OUT/(name+'-inputs.edn'); inp.write_text(dumps([[Tagged('edb/ref',x) for x in batch]])); cmd+=['--inputs',str(inp)]
  result=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=90)
  if result.returncode: raise RuntimeError(name+': '+result.stderr)
  rows.extend(loads(result.stdout))
 result_file.write_text(dumps(rows)+'\n'); print(name,len(rows),'rows',flush=True)
(OUT/'snapshot.json').write_text(json.dumps({'database':'math','basis_t':1149,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'},indent=2)+'\n')
