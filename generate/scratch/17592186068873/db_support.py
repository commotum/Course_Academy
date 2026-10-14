import json,sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[3]
H=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
from edn import dumps,loads,kw
DB=Database(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',endpoint='/tmp/edb-math/writer.sock'))
KP=17592186068873
QUESTION='''[* {:question/difficulty [:db/id :db/ident]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]'''
PATTERN='''[* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '''+QUESTION+'''} {[:knowledge-point/questions :limit nil] '''+QUESTION+'''}]'''
def read(basis,name='source'):
 return DB.query('[:find (pull ?k '+PATTERN+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP],H/'evidence',name,basis)[0][0]
def plain(x):
 if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
 if isinstance(x,list):return [plain(v) for v in x]
 return str(x) if not isinstance(x,(str,int,float,bool)) and x is not None else x
if __name__=='__main__':
 basis=DB.basis();raw=read(basis)
 (H/'current-source.edn').write_text(dumps(raw)+'\n')
 (H/'current-source.json').write_text(json.dumps({'database':'math','basis':basis,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','record':plain(raw)},indent=2)+'\n')
 print('basis',basis,'generator',raw.get(':knowledge-point/question-generator'))
