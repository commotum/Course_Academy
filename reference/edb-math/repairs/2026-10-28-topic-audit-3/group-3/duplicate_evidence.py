import collections,json,sys
from pathlib import Path
sys.path.insert(0,'scripts');from migrate_learner_history import connection
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());Q={q[':db/id']:q for q in D['questions']};groups=json.loads((H/'duplicate-field-keys.json').read_text());db=connection();fids=sorted({f for g in groups for f in g['fields']});answers=sorted({a[':db/id']for g in groups for f in Q[g['question']][':question/answer-fields']if f[':db/id']in g['fields']for a in f[':answer-field/choices']});qids=sorted({g['question']for g in groups});queries={
 'field-owners':('[:find ?f ?q ?tx ?op :in $ [?f ...] :where [?q :question/answer-fields ?f ?tx _ ?op]]',fids),
 'answer-owners':('[:find ?a ?f ?tx ?op :in $ [?a ...] :where [?f :answer-field/choices ?a ?tx _ ?op]]',answers),
 'answer-responses':('[:find ?a ?item ?tx ?op :in $ [?a ...] :where [?item :task-item/responses ?a ?tx _ ?op]]',answers),
 'question-tasks':('[:find ?q ?item ?tx ?op :in $ [?q ...] :where [?item :task-item/content ?q ?tx _ ?op]]',qids)};refs={}
for hist in(False,True):
 for name,(query,ids)in queries.items():
  rows=[]
  for n,entity in enumerate(ids):
   scalar=query.replace('[?f ...]','?f').replace('[?a ...]','?a').replace('[?q ...]','?q')
   rows+=db.query(scalar,[entity],H,'duplicates-'+name+'-'+str(hist)+'-'+str(n),9837,history=hist)
  refs[name+('-history'if hist else'-current')]=rows
  print(name,hist,len(rows),flush=True)
records=[]
for g in groups:
 q=Q[g['question']];records.append({**g,'all_question_field_ids':[f[':db/id']for f in q[':question/answer-fields']],'full_fields':[f for f in q[':question/answer-fields']if f[':db/id']in g['fields']],'problem':q[':question/problem'],'worked_solution':q.get(':question/worked-solution')})
(H/'duplicate-field-records.json').write_text(json.dumps(records,indent=2));(H/'duplicate-field-reference-evidence.json').write_text(json.dumps(refs,indent=2));print('duplicate evidence ready',len(groups))
