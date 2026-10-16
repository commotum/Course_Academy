import json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'))
from edn import loads,dumps
B='/home/jake/Developer/EDB/target/release/edb';E={**os.environ,'EDB_POSTGRES_URL':'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
snap=json.loads((H/'snapshot.json').read_text());basis=snap['basis'];ids=[i['entity'] for i in snap['reported']]
def cli(*args):return subprocess.check_output([B,*args],env=E,text=True,timeout=120)
def query(name,attr,es):
 q=H/(name+'-query.edn');q.write_text('[:find ?entity ?parent :in $ [?entity ...] :where [?parent '+attr+' ?entity]]')
 i=H/(name+'-inputs.edn');i.write_text(dumps([es]));out=cli('query','--database','math','--as-of',str(basis),'--file',str(q),'--inputs',str(i));(H/(name+'.edn')).write_text(out);return loads(out)
parents=[]
for attr in [':knowledge-point/questions',':knowledge-point/canonical-example',':step/content']:
 for eid,parent in query('owners-'+attr[1:].replace('/','-'),attr,ids):parents.append([eid,attr,parent])
steps=[p for _,a,p in parents if a==':step/content']
acts=query('step-activities',':activity/steps',steps) if steps else []
kpids=sorted({p for _,a,p in parents if a.startswith(':knowledge-point/')})
ktopics=query('kp-topics',':topic/knowledge-points',kpids)
(H/'activity-pull.edn').write_text('[* {:activity/scope [:db/id :topic/title]}]')
aids=sorted({a for _,a in acts});activity={}
for a in aids:
 out=cli('pull','--database','math','--as-of',str(basis),'--file',str(H/'activity-pull.edn'),'--entity',str(a));(H/f'activity-{a}.edn').write_text(out);activity[a]=loads(out)
result=[];topics=set()
for e,a,p in parents:
 if a.startswith(':knowledge-point/'):
  ts=[t for kp,t in ktopics if kp==p]
 else:
  ts=[activity[act][':activity/scope'][':db/id'] for step,act in acts if step==p]
 topics.update(ts);result.append({'entry':e,'via':a,'parent':p,'topics':ts})
(H/'ownership.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
(H/'requested-order.json').write_text(json.dumps(sorted(topics),indent=2)+'\n')
print(json.dumps({'owners':result,'topics':sorted(topics)}))
