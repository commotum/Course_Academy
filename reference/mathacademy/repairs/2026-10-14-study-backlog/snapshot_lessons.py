import json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3]
sys.path.insert(0,str(R/'scripts/question_capture'));from edn import loads
s=json.loads((H/'snapshot.json').read_text());p=(R/'reference/mathacademy/repairs/2026-10-14-linear-algebra-latex/lesson-pull.edn').read_text()
p=p.replace('{:answer-field/choices [* {:answer/type [:db/ident]}]}','{:answer-field/choices [* {:answer/type [:db/ident]}]} {:answer-field/correct [* {:answer/type [:db/ident]}]}')
(H/'lesson-pull.edn').write_text(p)
env={**os.environ,'EDB_POSTGRES_URL':'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
for eid in json.loads((H/'requested-order.json').read_text()):
 out=subprocess.check_output(['/home/jake/Developer/EDB/target/release/edb','pull','--database','math','--as-of',str(s['basis']),'--file',str(H/'lesson-pull.edn'),'--entity',str(eid),'--max-depth','30','--max-entities','50000'],env=env,text=True,timeout=120)
 (H/f'{eid}.edn').write_text(out);t=loads(out);print(eid,t[':topic/title'])
