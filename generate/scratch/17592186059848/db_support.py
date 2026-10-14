"""Requested knowledge point reads through the existing application EDB client."""
import sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]
H=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'scripts'),str(ROOT/'scripts/question_capture')]
from database import Database
from edn import dumps,loads,kw
from serve_graph_explorer import database_environment
ENV=database_environment('math')
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint=ENV['EDB_ENDPOINT'],postgres_url=ENV['EDB_POSTGRES_URL']))
KP=17592186059848
QUESTION='''[* {:question/difficulty [:db/id :db/ident]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'''
PATTERN='''[* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '''+QUESTION+'''} {[:knowledge-point/questions :limit nil] '''+QUESTION+'''}]'''
def read(basis,path):
 return DB.query('[:find (pull ?k '+PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],path,'kp',basis)[0][0]
def plain(x):
 if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [plain(v) for v in x]
 return str(x) if not isinstance(x,(str,int,float,bool)) and x is not None else x
if __name__=='__main__':
 import json
 out=H/'reference/replenishment';out.mkdir(parents=True,exist_ok=True)
 b=DB.basis();kp=read(b,out/'initial')
 (out/'current-source.json').write_text(json.dumps({'basis':b,'record':plain(kp)},indent=2))
 print(json.dumps({'basis':b,'title':kp.get(':knowledge-point/title'),'generator':plain(kp.get(':knowledge-point/question-generator')),'questions':len(kp[':knowledge-point/questions']),'levels':{level:sum(str(q.get(':question/difficulty',{}).get(':db/ident','')).endswith('/'+level) for q in kp[':knowledge-point/questions']) for level in ['easy','moderate','hard']}}))
