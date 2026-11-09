import sys,json
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');H=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection
b=json.loads((H/'basis.json').read_text())['basis'];db=connection();mids=['q-342744','q-65121','q-332547','q-343294','q-343299','q-339878']
report={}
for name,where in [('presentations','[?item :task-item/content ?q ?tx true]'),('responses','[?q :question/answer-fields ?f] [?f :answer-field/choices ?a] [?item :task-item/responses ?a ?tx true]')]:
 report[name]=db.query('[:find ?mid ?item :in $ [?mid ...] :where [?q :question/math-academy-id ?mid] '+where+']',[mids],H,'historical-'+name,b,history=True)
(H/'historical-usage.json').write_text(json.dumps(report,indent=2));print(report)
