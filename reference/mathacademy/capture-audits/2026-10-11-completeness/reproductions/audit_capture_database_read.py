import json,threading,time,subprocess
from pathlib import Path
from scripts.config import Config
from scripts.database.client import EDBClient
c=EDBClient(Config(),threading.Event());identity=c.status();print('STATUS',json.dumps(identity),flush=True)
d=Path('/tmp/capture-audit-database');report=json.loads(Path('/tmp/new-capture-completeness-extended.json').read_text());suspect=sorted({r['question'] for r in report['prompt_body_gaps']}|{'q-103560','q-20359','q-105187','q-181457','q-72785'}); rows=[]
try:
 for start in range(0,len(suspect),10):
  rows+=c.query('[:find (pull ?q [:db/id :question/math-academy-id :question/problem]) :in $ [?id ...] :where [?q :question/math-academy-id ?id]]',[suspect[start:start+10]],d,'suspect-prompts-'+str(start),identity['basis'])
except subprocess.CalledProcessError as error: print('QUERY FAILURE',error.stderr);raise
result={'identity':identity,'read_at':time.time(),'requested_question_ids':suspect,'suspect_prompts':[r[0] for r in rows]}
(d/'questions.json').write_text(json.dumps(result,indent=2)+'\n');print('READ',len(rows),'suspect prompts',flush=True)
