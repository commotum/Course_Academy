import json,sys
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');H=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection
rows=json.loads((H/'detached-memberships.json').read_text());ids=sorted({r.get('answer',r.get('field'))for r in rows});db=connection();basis=json.loads((H/'basis.json').read_text())['basis'];q='[:find (pull ?e [*]) :in $ [?e ...] :where [?e ?a ?v]]'
before=db.query(q,[ids],H,'detached-before',basis);after=db.query(q,[ids],H,'detached-after',13542)
a={r[0][':db/id']:r[0]for r in before};b={r[0][':db/id']:r[0]for r in after};report={'entities':ids,'before_basis':basis,'after_basis':13542,'all_original_records_unchanged':a==b,'retained_count':len(b)};(H/'retention-verification.json').write_text(json.dumps(report,indent=2));print(report);assert a==b
# Repair duplicate Pull copies in the planned JSON representation; the EDN request is immutable.
for d in H.glob('175*'):
 qs=json.loads((d/'questions-after.json').read_text())
 for qq in qs:
  for f in qq.get(':question/answer-fields',[]):
   if f.get(':answer-field/correct'):f[':answer-field/correct']=next(a for a in f.get(':answer-field/choices',[])if a[':db/id']==f[':answer-field/correct'][':db/id'])
 (d/'questions-after.json').write_text(json.dumps(qs,indent=2))
