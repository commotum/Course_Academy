"""Current schema/content-contract check across the entire requested set."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection,loads
inv=json.loads((H/'inventory.json').read_text());b=inv['basis_t'];db=connection();ids=sorted({q for t,k,q in inv['links']});specs={
'empty-solutions':('[:find ?q :in $ [?q ...] ?empty :where [?q :question/worked-solution ?empty]]',[ids,'']),
'unowned-correct-links':('[:find ?q ?f ?a :in $ [?q ...] :where [?q :question/answer-fields ?f] [?f :answer-field/correct ?a] (not-join [?f ?a] [?f :answer-field/choices ?a])]',[ids]),
'field-keys':('[:find ?q ?f ?key :in $ [?q ...] :where [?q :question/answer-fields ?f] [?f :answer-field/key ?key]]',[ids]),
'blank-text-candidates':('[:find ?q ?f ?a ?value :in $ [?q ...] :where [?q :question/answer-fields ?f] [?f :answer-field/type :answer-field.type/blank] [?f :answer-field/correct ?a] [?a :answer/type :answer.type/text] [?a :answer/value ?value]]',[ids])}
out={}
for label,(query,inputs)in specs.items():
 saved=H/('integrity-'+label+'.edn');out[label]=loads(saved.read_text())if saved.exists()and saved.stat().st_size else db.query(query,inputs,H,'integrity-'+label,b);print(label,len(out[label]),flush=True)
from collections import defaultdict
keys=defaultdict(list)
for q,f,key in out.pop('field-keys'):keys[q,key].append(f)
out['duplicate-field-keys']=[{'question':q,'key':key,'fields':fs}for(q,key),fs in keys.items()if len(fs)>1]

(H/'full-scope-integrity.json').write_text(json.dumps({'basis_t':b,'question_records':len(ids),'results':out,'database_writes':0},default=str,indent=2)+'\n');print(out)
