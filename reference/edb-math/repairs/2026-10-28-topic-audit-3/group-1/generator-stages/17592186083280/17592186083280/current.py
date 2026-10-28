"""Read-only current inventory and KP evidence through application integrations."""
import json, subprocess, sys
from pathlib import Path
from types import SimpleNamespace
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path[:0]=[str(ROOT),str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps
from inventory_jobs import save
from serve_graph_explorer import database_environment
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT']))
KP=17592186083280
LEARNER='59d5cf13-351c-4114-be19-4c3bb64ee051'
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
Q='''[* {:question/difficulty [:db/id :db/ident]}
 {:knowledge-point/_canonical-example [:db/id]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/ident]}
 {:answer-field/correct [* {:answer/type [:db/ident]}]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/ident]}]}]}]'''
QUERY='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+Q+'} {[:knowledge-point/questions :limit nil] '+Q+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
def inventory(path):
    executable=ROOT/'.local/graph-explorer/learning-0ee7e7bd24d378f7'
    r=subprocess.run([str(executable),'math',LEARNER,DB.args.endpoint],input='{"action":"inventory"}',env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['ok'] and x['data']['lineage']==LINEAGE
    save(path,x['data']);return x['data']
def discovery(path):
    request={'database':'math','learner':LEARNER,'topics':[17592186050162],'activity_type':'lesson','after_basis':None,'lineage':None,'at':None}
    r=subprocess.run([str(ROOT/'.local/generate/find-candidates-b13a7928a9573a2f')],input=json.dumps(request),env=ENV,capture_output=True,text=True,check=True,timeout=90)
    x=json.loads(r.stdout);assert x['cursor']['lineage']==LINEAGE
    save(path,x);return x
def read_kp(path,basis):return DB.query(QUERY,[KP],path,'kp',basis)[0][0]
if __name__=='__main__':
    out=HERE/'reference/initial';out.mkdir(parents=True,exist_ok=True)
    inv=inventory(out/'inventory.json');disc=discovery(out/'discovery.json');b=DB.basis()
    kp=read_kp(out,b);(out/'kp.edn').write_text(dumps(kp)+'\n')
    print(json.dumps({'basis':b,'inventory_basis':inv['basis'],'discovery_basis':disc['basis'],'questions':len(kp[':knowledge-point/questions']),'generator':kp.get(':knowledge-point/question-generator'),'inventory':[k['inventory'] for t in disc['topics'] for k in t['knowledge_points'] if k['db/id']==KP]},default=str))
