import sys,json
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
out=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic');db=connection();basis=json.loads((out/'basis.json').read_text())['basis']
qs=[q for d in out.glob('175*')for q in json.loads((d/'questions.json').read_text())if q[':question/math-academy-id']in ['q-64716','q-64811']]
ids=[a[':db/id']for q in qs for f in q[':question/answer-fields']for a in f[':answer-field/choices']]
r=db.query('[:find ?e ?v :in $ [?v ...] :where [?e :task-item/responses ?v]]',[ids],out,'duplicate-bank-incoming-refs',basis)
(out/'duplicate-bank-usage.json').write_text(json.dumps(r,indent=2,default=str));print(qs)
