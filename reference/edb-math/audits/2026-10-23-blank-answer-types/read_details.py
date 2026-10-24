import json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path('reference/edb-math/audits/2026-10-23-blank-answer-types');basis=json.load(open(H/'summary.json'))['basis_t'];rows=json.load(open(H/'text-blank-fields.json'));changes=[r for r in rows if 'tex-command' in r['flags']];answers=[r['answer'] for r in changes];questions=sorted({q['entity'] for r in changes for q in r['questions']}|{17592186233932});db=connection()
q=db.query('[:find (pull ?q [* {:question/difficulty [:db/ident]} {:question/answer-fields [* {:answer-field/type [:db/ident]} {:answer-field/correct [* {:answer/type [:db/ident]}]} {:answer-field/choices [* {:answer/type [:db/ident]}]}]}]) :in $ [?q ...] :where [?q :question/id _]]',[questions],H,'question-trees-before',basis);(H/'question-trees-before.json').write_text(json.dumps(q,default=str,ensure_ascii=False,indent=2)+'\n')
r=db.query('[:find ?answer ?field ?kind :in $ [?answer ...] :where (or [?field :answer-field/choices ?answer] [?field :answer-field/correct ?answer]) [?field :answer-field/type ?t] [?t :db/ident ?kind]]',[answers],H,'answer-owners',basis);print('all owning fields',r);assert {a:{f for a2,f,k in r if a2==a} for a in answers}=={c['answer']:{c['field']} for c in changes}
for row in q:
 if row[0][':db/id']==17592186233932:
  f=next(f for f in row[0][':question/answer-fields'] if f[':db/id']==17592186232880);assert f[':answer-field/correct'][':db/id']==17592186232881 and str(f[':answer-field/correct'][':answer/type'][':db/ident'])==':answer.type/math';print('confirmed example remains fixed')
