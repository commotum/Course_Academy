import json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts/question_capture'));from edn import loads,dumps
basis=json.loads((H/'snapshot.json').read_text())['basis'];qs=json.loads((H/'questions.json').read_text());E={**os.environ,'EDB_POSTGRES_URL':'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
def cli(*args):return subprocess.check_output(['/home/jake/Developer/EDB/target/release/edb',*args],env=E,text=True,timeout=150)
pattern=H/'kp-pull.edn';entry='[* {:question/difficulty [:db/id :db/ident]} {:question/answer-fields [* {:answer-field/type [:db/id :db/ident]} {:answer-field/choices [* {:answer/type [:db/id :db/ident]}]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}]}]';pattern.write_text('[* {:knowledge-point/questions '+entry+'} {:knowledge-point/canonical-example '+entry+'}]')
for eid in sorted({k[':db/id'] for q in qs for k in q[':knowledge-point/_questions']}):
 (H/f'kp-{eid}.edn').write_text(cli('pull','--database','math','--as-of',str(basis),'--file',str(pattern),'--entity',str(eid),'--max-depth','25','--max-entities','30000'))
ids=[q[':db/id'] for q in qs];answers=sorted({a[':db/id'] for q in qs for f in q[':question/answer-fields'] for a in f[':answer-field/choices']})
for name,attr,es in [('presentation-history','task-item/content',ids),('response-history','task-item/responses',answers)]:
 query=H/(name+'-query.edn');query.write_text('[:find ?target ?item ?tx ?source ?added :in $ [?target ...] :where [?item :'+attr+' ?target ?tx ?source ?added]]');inputs=H/(name+'-inputs.edn');inputs.write_text(dumps([es]));(H/(name+'.edn')).write_text(cli('query','--database','math','--as-of',str(basis),'--history','--file',str(query),'--inputs',str(inputs)))
print('Context and retained presentation/response history read at',basis)
