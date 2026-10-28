import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,kw
D=H/'detached-answer-history';D.mkdir(exist_ok=True);db=connection();basis=db.basis();answers=[17592186310249,17592186310565];questions=[17592186311586,17592186311625]
queries={
 'current-responses':('[:find ?answer ?item :in $ [?answer ...] :where [?item :task-item/responses ?answer]]',[answers],False),
 'historical-responses':('[:find ?answer ?item ?tx ?source ?added :in $ [?answer ...] :where [?item :task-item/responses ?answer ?tx ?source ?added]]',[answers],True),
 'current-memberships':('[:find ?answer ?field :in $ [?answer ...] :where [?field :answer-field/choices ?answer]]',[answers],False),
 'historical-memberships-positive-control':('[:find ?answer ?field ?tx ?source ?added :in $ [?answer ...] :where [?field :answer-field/choices ?answer ?tx ?source ?added]]',[answers],True),
 'current-question-task-items':('[:find ?question ?item :in $ [?question ...] :where [?item :task-item/content ?question]]',[questions],False),
 'historical-question-task-items':('[:find ?question ?item ?tx ?source ?added :in $ [?question ...] :where [?item :task-item/content ?question ?tx ?source ?added]]',[questions],True),
 'response-schema':('[:find (pull ?a [*]) :where [?a :db/ident :task-item/responses]]',[],False),
}
results={}
for name,(query,inputs,history)in queries.items():
 results[name]=db.query(query,inputs,D,name,basis,history=history);print(name,len(results[name]),flush=True)
# Also retain the original audit-basis point-in-time and full historical view.
for name in['current-responses','historical-responses']:
 query,inputs,history=queries[name];results[name+'-basis9122']=db.query(query,inputs,D,name+'-basis9122',9122,history=history)
report={'database':'math','captured_basis':basis,'audit_basis':9122,'answers':answers,'questions':questions,'results':results,'response_reference_counts':{str(a):{'current':sum(r[0]==a for r in results['current-responses']),'retained_historical_events':sum(r[0]==a for r in results['historical-responses']),'historical_assertions':sum(r[0]==a and r[-1]for r in results['historical-responses'])}for a in answers},'database_writes':0,'history_limit':'Retained history at captured basis, including assertions and retractions; does not claim recovery of excised/noHistory data.'}
report['detach_must_be_held']=bool(results['current-responses']or results['historical-responses'])
(D/'report.json').write_text(json.dumps(report,indent=2,default=str)+'\n');print(json.dumps({'basis':basis,'counts':report['response_reference_counts'],'hold':report['detach_must_be_held']},indent=2))
