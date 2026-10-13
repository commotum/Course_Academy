"""Read all finder KPs at the finder's fixed database basis; no transactions."""
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from capture.scripts.database.edn import loads, dumps, Tagged
from scripts.serve_graph_explorer import database_environment

CANDIDATES = json.loads((OUT/'candidates.json').read_text())
QUESTION = '''[:db/id :question/id :question/math-academy-id :question/problem :question/worked-solution
 {:question/difficulty [:db/ident]}
 {[:question/answer-fields :limit nil] [:db/id :answer-field/id :answer-field/key
  {:answer-field/type [:db/ident]}
  {:answer-field/correct [:db/id :answer/id :answer/value :answer/feedback {:answer/type [:db/ident]}]}
  {[:answer-field/choices :limit nil] [:db/id :answer/id :answer/value :answer/feedback {:answer/type [:db/ident]}]}]}]'''
KP = '''[:db/id :knowledge-point/id :knowledge-point/title
 {:knowledge-point/canonical-example '''+QUESTION+'''}
 {[:knowledge-point/questions :limit nil] '''+QUESTION+'''}]'''
QUERY = '[:find (pull ?kp '+KP+') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]'
(OUT/'sources').mkdir(exist_ok=True)
(OUT/'source-query.edn').write_text(QUERY)

def plain(v):
    if isinstance(v,Tagged): return plain(v.value)
    if isinstance(v,dict): return {str(k):plain(x) for k,x in v.items()}
    if isinstance(v,list): return [plain(x) for x in v]
    if isinstance(v,(str,int,float,bool)) or v is None: return v
    return str(v)

def read(group):
    label=str(group[0])
    inputs=OUT/'sources'/('inputs-'+label+'.edn')
    inputs.write_text(dumps([[Tagged('edb/ref',x) for x in group]]))
    result=subprocess.run([str(ROOT.parent/'EDB/target/release/edb'),'query',
      '--database',CANDIDATES['database'],'--as-of',str(CANDIDATES['basis']),
      '--file',str(OUT/'source-query.edn'),'--inputs',str(inputs),
      '--max-value-bytes',str(64*1024*1024)],
      env=database_environment(CANDIDATES['database']),text=True,capture_output=True,timeout=60)
    if result.returncode: raise RuntimeError(result.stderr)
    (OUT/'sources'/('batch-'+label+'.edn')).write_text(result.stdout)
    rows=plain(loads(result.stdout))
    assert {r[0][':db/id'] for r in rows}==set(group)
    for row in rows:
        q=row[0]
        (OUT/'sources'/(str(q[':db/id'])+'.json')).write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    return len(group)

ids=sorted({kp['db/id'] for topic in CANDIDATES['topics'] for kp in topic['knowledge_points']})
groups=[ids[i:i+8] for i in range(0,len(ids),8)
  if not all((OUT/'sources'/(str(e)+'.json')).exists() for e in ids[i:i+8])]
done=len(ids)-sum(map(len,groups))
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    for future in concurrent.futures.as_completed([pool.submit(read,g) for g in groups]):
        done+=future.result()
        if done%32==0 or done==len(ids): print(f'Captured {done}/{len(ids)} KPs',flush=True)
records=[json.loads((OUT/'sources'/(str(e)+'.json')).read_text()) for e in ids]
questions={q[':db/id'] for r in records for q in r.get(':knowledge-point/questions',[])}
print(json.dumps({'basis':CANDIDATES['basis'],'knowledge_points':len(ids),
  'unique_practice_questions':len(questions),'empty_kps':sum(not r.get(':knowledge-point/questions') for r in records)}))
