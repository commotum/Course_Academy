"""Read-only fixed-basis MTH 341 lesson snapshot. Does not transact."""
import json,os,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BIN='/home/jake/Developer/EDB/target/release/edb'
env={**os.environ,'EDB_POSTGRES_URL':'host=/tmp/edb-math port=55432 dbname=math user=edb_peer'}
pattern=ROOT/'reference/mathacademy/repairs/2026-10-14-linear-algebra-latex/lesson-pull.edn'
for eid in json.loads((HERE/'topic-ids.json').read_text()):
 p=HERE/f'{eid}.edn'
 if p.exists() and p.stat().st_size:continue
 result=subprocess.run([BIN,'pull','--database','math','--as-of','3078','--file',str(pattern),'--entity',str(eid),'--max-depth','40','--max-entities','50000'],env=env,text=True,capture_output=True,timeout=120)
 if result.returncode:raise RuntimeError(result.stderr)
 p.write_text(result.stdout)
 print(eid,flush=True)
(HERE/'snapshot.json').write_text(json.dumps({'database':'math','basis':3078,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','mode':'read-only'},indent=2))
