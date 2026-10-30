import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
D=H/'readback';D.mkdir(exist_ok=True);db=connection();basis=json.loads((H/'inventory.json').read_text())['basis_t'];ids=sorted({x['entity']for x in json.loads((H/'proposals.json').read_text())}|{17592186551286})
q='[:find (pull ?q [* {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/choices [* {:answer/type [:db/ident]}]} {:answer-field/correct [:db/id]}]}]) :in $ [?q ...] :where [?q :question/id _]]'
rows=db.query(q,[ids],D,'questions',basis);assert len(rows)==len(ids);(H/'questions.json').write_text(json.dumps([r[0]for r in rows],default=str,indent=2)+'\n');print('Read',len(rows),'completequestions at',basis)
