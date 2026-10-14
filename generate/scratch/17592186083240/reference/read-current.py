import sys,json,uuid
from pathlib import Path
from types import SimpleNamespace
R=Path.cwd();sys.path.insert(0,str(R/'scripts/question_capture'))
from database import Database,QUESTION_PULL
from edn import dumps
D=R/'generate/scratch/17592186083240/reference/replenishment/initial';D.mkdir(parents=True,exist_ok=True)
db=Database(SimpleNamespace(edb_bin=str(R/'.local/edb/capture-runtime/math-edb'),database='math'))
b=db.basis();query='[:find (pull ?kp [* {:knowledge-point/question-generator [*]} {:knowledge-point/canonical-example '+QUESTION_PULL+'} {[:knowledge-point/questions :limit nil] '+QUESTION_PULL+'}]) :in $ ?kp :where [?kp :knowledge-point/id _]]'
k=db.query(query,[17592186083240],D,'kp',b)[0][0]
(D/'source-query.edn').write_text(query);(D/'before.edn').write_text(dumps(k))
print('basis',b,'generator',k.get(':knowledge-point/question-generator'),'questions',len(k.get(':knowledge-point/questions',[])))
print([(q.get(':question/math-academy-id'),str(q.get(':question/difficulty')),len(q.get(':question/answer-fields',[]))) for q in k[':knowledge-point/questions']])
x=json.load(open(R/'generate/scratch/17592186083240/validation.json'));import hashlib
print('validation integrity',[(p,hashlib.sha256((R/'generate/scratch'/p).read_bytes()).hexdigest()==h) for p,h in x['file_hashes'].items()])
