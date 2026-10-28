import collections,json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};targets={17592186152565:[(17592186307618,17592186306480,17592186307380),(17592186307826,17592186306754,17592186306402)],17592186308544:[(17592186308213,17592186306207,17592186307270),(17592186307843,17592186306654,17592186305897)]};db=connection();refs={};ans=[r[1]for rs in targets.values()for r in rs]
for hist in (False,True):
 refs['content-history'if hist else'content-current']=db.query('[:find ?q ?item ?tx ?op :in $ [?q ...] :where [?item :task-item/content ?q ?tx _ ?op]]',[list(targets)],H,'dependence-badkeys-content-'+str(hist),9122,history=hist)
 refs['responses-history'if hist else'responses-current']=db.query('[:find ?a ?item ?tx ?op :in $ [?a ...] :where [?item :task-item/responses ?a ?tx _ ?op]]',[ans],H,'dependence-badkeys-responses-'+str(hist),9122,history=hist)
assert all(v==[]for v in refs.values()),refs
keys=[];detaches=[];evidence=[];manifest=json.loads((H/'source-manifest.json').read_text())
for qid,repairs in targets.items():
 q=Q[qid];sid=q[':question/math-academy-id'];paths=manifest.get(sid,[]);source=next((p for p in paths if p.endswith('-before.json')),None)
 evidence.append({'question':qid,'source_identity':sid,'source_path':source,'worked_solution':q[':question/worked-solution'],'proof':'2*x+0*exp(x)-1*(2*x)=0 with nonzero coefficients'if sid=='q-333508'else'0*(7*sin(x))+4*(5*cos(x))+4*(-5*cos(x))=0 with nonzero coefficients','source_question':json.loads(Path(source).read_text())if source else None})
 for field,bad,good in repairs:
  f=next(f for f in q[':question/answer-fields']if f[':db/id']==field);assert f[':answer-field/correct'][':db/id']==bad
  keys.append({'question':qid,'field':field,'before':bad,'answer':good,'reason':'Restore the numeric coefficient proved by the original worked solution; current canonical member is a prose conclusion inserted into the wrong field.','evidence':{'source_identity':sid,'path':source,'algebraic_identity':evidence[-1]['proof'],'historical_question_and_bad_answer_response_refs':[]},'confidence':'high'})
  detaches.append({'operation':'db/retract','entity':field,'attribute':'answer-field/choices','value':bad,'expected_before_choice_ids':sorted(a[':db/id']for a in f[':answer-field/choices']),'reason':'Remove only the unused malformed prose member from the numeric source bank after repointing the key; retain the answer entity.','evidence':{'source_identity':sid,'path':source,'no_current_or_historical_task_or_response_refs_at_basis':9122,'answer_entity_retained':True}})
(H/'dependence-correct-link-repairs.json').write_text(json.dumps(keys,indent=2));(H/'dependence-bank-membership-proposals.json').write_text(json.dumps(detaches,indent=2));(H/'dependence-source-evidence.json').write_text(json.dumps(evidence,indent=2));(H/'dependence-reference-evidence.json').write_text(json.dumps(refs,indent=2));print('bad canonical links',len(keys),'unused malformed members',len(detaches),'all history refs empty')
