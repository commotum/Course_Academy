import sys,json
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());db=connection();k=[v[':db/id']for v in D['kps']]
a=db.query('[:find ?kp ?g ?script :in $ [?kp ...] :where [?kp :knowledge-point/question-generator ?g] [?g :question-generator/script ?script]]',[k],H,'generators',9047)
b=db.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],H,'idents',9047)
(H/'generators.json').write_text(json.dumps(a,default=str,indent=2));(H/'idents.json').write_text(json.dumps(b,default=str,indent=2));print(len(a))
