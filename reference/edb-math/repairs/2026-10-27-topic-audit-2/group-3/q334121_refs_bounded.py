import json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;db=connection();q=17592186308563;ans=[17592186306650,17592186307410,17592186305867,17592186306796];out={}
for hist in (False,True):
 for name,query,inputs in [('content','[:find ?item ?tx ?op :in $ ?q :where [?item :task-item/content ?q ?tx _ ?op]]',[q]),('responses','[:find ?a ?item ?tx ?op :in $ [?a ...] :where [?item :task-item/responses ?a ?tx _ ?op]]',[ans])]:
  try:out[name+('-history'if hist else'-current')]=db.query(query,inputs,H,'q334121-'+name+('-history'if hist else'-current'),9122,history=hist)
  except Exception as ex:out[name+('-history'if hist else'-current')]={'error':getattr(ex,'stderr',str(ex))}
(H/'q334121-reference-evidence.json').write_text(json.dumps(out,indent=2,default=str));print(out)
