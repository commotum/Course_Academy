import json,sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]
H=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps,loads,kw
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint='/tmp/edb-math/writer.sock'))
KP=17592186119743
QUESTION='''[* {:question/difficulty [:db/id :db/ident]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'''
PATTERN='''[* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '''+QUESTION+'''} {[:knowledge-point/questions :limit nil] '''+QUESTION+'''}]'''
def read(basis,name='source'):
 return DB.query('[:find (pull ?k '+PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],H/'evidence',name,basis)[0][0]
def plain(x):
 if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
 if isinstance(x,list):return [plain(v) for v in x]
 return str(x) if not isinstance(x,(str,int,float,bool)) and x is not None else x
