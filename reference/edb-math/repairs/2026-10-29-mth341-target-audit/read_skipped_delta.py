"""Inspect the one newly detected contract defect in a previously audited topic."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
D=H/'skipped-delta';D.mkdir(exist_ok=True);db=connection();b=json.loads((H/'inventory.json').read_text())['basis_t'];rows=db.query('[:find (pull ?q [* {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/choices [* {:answer/type [:db/ident]}]} {:answer-field/correct [:db/id]}]}]) :in $ ?q :where [?q :question/id _]]',[17592186106149],D,'question',b);q=rows[0][0];(D/'question.json').write_text(json.dumps(q,default=str,indent=2)+'\n');print(json.dumps(q,default=str,indent=2)[:12000])
