import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection
D=json.loads((H/'current.json').read_text());q=next(q for q in D['questions']if q[':db/id']==17592186106313);fields=[f[':db/id']for f in q[':question/answer-fields']];answers=[a[':db/id']for f in q[':question/answer-fields']for a in f[':answer-field/choices']];db=connection();rows=[]
for attr,ids in [('question/answer-fields',fields),('answer-field/choices',answers),('answer-field/correct',answers),('task-item/responses',answers),('task-item/content',[q[':db/id']])]:
 r=db.query('[:find ?v ?e :in $ [?v ...] :where [?e :'+attr+' ?v]]',[ids],H,'duplicate-'+attr.replace('/','-'),9047);rows.extend([v,e,attr]for v,e in r)
ents=sorted({r[1]for r in rows});records=[]
for i in range(0,len(ents),15):records +=[r[0]for r in db.query('[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]',[ents[i:i+15]],H,'duplicate-referrers-'+str(i),9047)]
(H/'duplicate-history.json').write_text(json.dumps({'basis':9047,'question':q, 'incoming':rows,'referrers':records,'limit':'All current supported field, choice, key, task-item/content and task-item/responses attributes checked at T9047. Generic unknown-attribute reverse scan exceeded EDB query budget.'},default=str,indent=2));print('incoming',rows,'referrers',len(records))
