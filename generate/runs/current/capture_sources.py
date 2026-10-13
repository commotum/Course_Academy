"""Read-only, fixed-basis source capture for this generator run."""
import json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
from capture.scripts.database.edn import loads,dumps,Tagged,kw
from scripts.serve_graph_explorer import database_environment
ROOT=Path(__file__).resolve().parent
c=json.loads((ROOT/'candidates.json').read_text());basis=c['basis'];db=c['database']
question='''[:db/id :question/id :question/math-academy-id :question/problem :question/worked-solution
 {:question/difficulty [:db/ident]}
 {[:question/answer-fields :limit nil] [:db/id :answer-field/id :answer-field/key
  {:answer-field/type [:db/ident]}
  {:answer-field/correct [:db/id :answer/id :answer/value :answer/feedback {:answer/type [:db/ident]}]}
  {[:answer-field/choices :limit nil] [:db/id :answer/id :answer/value :answer/feedback {:answer/type [:db/ident]}]}]}]'''
kp='[:db/id :knowledge-point/id :knowledge-point/title {:knowledge-point/canonical-example '+question+'} {[:knowledge-point/questions :limit nil] '+question+'} {[:knowledge-point/key-prerequisites :limit nil] [:db/id :topic/math-academy-id :topic/title]}]'
queries={
 'sources':'[:find (pull ?kp '+kp+') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]',
 'topics':'''[:find (pull ?t [:db/id :topic/id :topic/math-academy-id :topic/title
 {[:topic/knowledge-points :limit nil] [:db/id :knowledge-point/title {:knowledge-point/canonical-example '''+question+'''}]}
 {[:topic/_next :limit nil] [:db/id :topic/title :topic/math-academy-id]}
 {[:topic/next :limit nil] [:db/id :topic/title :topic/math-academy-id]}])
 :in $ [?t ...] :where [?t :topic/id _]]''',
 'lessons':'''[:find ?t (pull ?a [:db/id :activity/id :activity/title :activity/first-step
 {[:activity/steps :limit nil] [:db/id :step/next {:step/content [:db/id :tutorial/title :tutorial/content :knowledge-point/title {:knowledge-point/canonical-example '''+question+'''}]}]}])
 :in $ [?t ...] :where [?a :activity/scope ?t] [?a :activity/type :activity.type/lesson]]''',
}
def plain(v):
 if isinstance(v,Tagged):return plain(v.value)
 if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
 if isinstance(v,list):return [plain(x) for x in v]
 if isinstance(v,(str,int,float,bool)) or v is None:return v
 return str(v)

def read(kind,ids,n):
 folder=ROOT/kind;folder.mkdir(exist_ok=True)
 q=ROOT/(kind+'-query.edn');q.write_text(queries[kind])
 inputs=ROOT/(kind+'-inputs-'+str(n)+'.edn')
 inputs.write_text(dumps([[Tagged('edb/ref',x) for x in ids]]))
 cmd=['/home/jake/Developer/EDB/target/release/edb','query','--database',db,'--as-of',str(basis),'--file',str(q),'--inputs',str(inputs)]
 result=subprocess.run(cmd,env=database_environment(db),text=True,capture_output=True,timeout=60,check=True)
 (folder/('batch-'+str(n)+'.edn')).write_text(result.stdout)
 return plain(loads(result.stdout))

def write(kind,eid,record):
 (ROOT/kind/(str(eid)+'.json')).write_text(json.dumps({'database':db,'basis':basis,'lineage':c['cursor']['lineage'],'record':record},indent=2,ensure_ascii=False)+'\n')

kps=sorted({k['db/id'] for t in c['topics'] for k in t['knowledge_points']})
priority=[17592186115393,17592186100890,17592186059847]
kps=[x for x in priority if x in kps]+[x for x in kps if x not in priority]
for start in range(0,len(kps),4):
 group=kps[start:start+4]
 if all((ROOT/'sources'/(str(x)+'.json')).exists() for x in group):continue
 rows=read('sources',group,start)
 assert {row[0][':db/id'] for row in rows}==set(group)
 for row in rows:write('sources',row[0][':db/id'],row[0])
 print('KP sources',min(start+4,len(kps)),'/',len(kps),flush=True)
# Capture topic narrative/routes before workers need curriculum context.
ids=[t['db/id'] for t in c['topics']]
for start in range(0,len(ids),4):
 group=ids[start:start+4]
 if all((ROOT/'topics'/(str(x)+'.json')).exists() for x in group):continue
 for row in read('topics',group,start):write('topics',row[0][':db/id'],row[0])
 lessons={x:[] for x in group}
 for row in read('lessons',group,start):lessons[row[0]].append(row[1])
 for x,ls in lessons.items():write('lessons',x,ls)
 print('Topic contexts',min(start+4,len(ids)),'/',len(ids),flush=True)
print('Captured',len(kps),'KPs and',len(ids),'topic contexts at basis',basis,flush=True)
