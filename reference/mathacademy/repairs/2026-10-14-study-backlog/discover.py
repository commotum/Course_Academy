"""Read-only snapshot of the user's deferred repair list and lesson ownership."""
import json,os,re,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from edn import loads,dumps
BIN='/home/jake/Developer/EDB/target/release/edb'
ENV={**os.environ,'EDB_POSTGRES_URL':'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
IDS=[17592186059581,17592186059582,17592186130339,17592186128995,17592186262981,17592186130380,17592186128926,17592186400415,17592186339126,17592186262997,17592186128927,17592186161758,17592186097840,17592186060941]
STACK={17592186400415,17592186339126,17592186262997}
def cli(*args):return subprocess.check_output([BIN,*args],env=ENV,text=True,timeout=120)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
assert not (HERE/'snapshot.json').exists(),'Retain the original read snapshot'
basis=int(re.search(r'basis_t=(\d+)',cli('status','--database','math'))[1])
save('snapshot.json',{'database':'math','basis':basis,'status':'PREPARATION ONLY; user has not authorized application','reported':[{'entity':i,'issue':'horizontal matrix overflow' if i in STACK else 'equation rendered as image'} for i in IDS]})
pattern=HERE/'entry-pull.edn';pattern.write_text('[* {:question/answer-fields [* {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]')
for eid in IDS:
 (HERE/f'{eid}.edn').write_text(cli('pull','--database','math','--as-of',str(basis),'--file',str(pattern),'--entity',str(eid),'--max-depth','25','--max-entities','20000'))
query=HERE/'parents-query.edn';query.write_text('[:find ?entity ?ident ?parent :in $ [?entity ...] :where [?parent ?attr ?entity] [?attr :db/ident ?ident]]')
inputs=HERE/'parents-inputs.edn';inputs.write_text(dumps([IDS]))
parents=cli('query','--database','math','--as-of',str(basis),'--file',str(query),'--inputs',str(inputs));(HERE/'parents.edn').write_text(parents)
for eid in IDS:
 x=loads((HERE/f'{eid}.edn').read_text());print(json.dumps({'id':eid,'type':[str(k) for k in x if str(k).endswith('/content') or str(k).endswith('/problem')],'ma_id':x.get(':question/math-academy-id'),'problem':x.get(':question/problem',x.get(':tutorial/content',''))[:180]},default=str))
print('parents',parents[:5000])
