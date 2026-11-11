"""Read, CAS-plan and speculate the prompt-only repair; never submit."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'scripts')]
from generator_publish import Publisher,GeneratorCommitter,StaleBasis,jsonable,digest,dumps,kw
from inventory_jobs import save
p=Publisher.from_environment(source=':agent/codex');ledger=json.loads((H/'case-ledger.json').read_text());original={r['entity']:r for r in ledger}
for attempt in range(3):
 status=p.client.status();basis=status['basis'];D=H/'question-publication'/('basis-'+str(basis));D.mkdir(parents=True,exist_ok=True)
 kp=p.read_kp(17592186092240,D,basis);questions=kp[':knowledge-point/questions'];byid={q[':db/id']:q for q in questions}
 assert set(byid)==set(original),'Sibling membership changed: review new inventory before apply'
 assertions=[];retractions=[];forms=[]
 for eid,row in original.items():
  q=byid[eid];assert q[':question/problem']==row['before'],'Prompt changed since audit'
  if row['changed']:
   assert not q.get(':question/math-academy-id')
   assertions.append([eid,kw('question/problem'),row['after']]);retractions.append([eid,kw('question/problem'),row['before']])
   forms += [[kw('db/cas'),eid,kw('question/problem'),row['before'],row['after']],[kw('db/ensure'),eid,kw('question/validate')]]
 forms.append([kw('db/ensure'),17592186092240,kw('knowledge-point/validate')])
 attrs=p.client.query('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[],D,'attributes',basis)
 idents=p.client.query('[:find ?e ?ident :where [?e :db/ident ?ident]]',[],D,'idents',basis)
 items=p.client.query('[:find (pull ?i [*]) :in $ [?q ...] :where [?i :task-item/content ?q]]',[list(byid)],D,'items-before',basis)
 snapshot=dict(basis=basis,lineage=status['lineage'],attributes=attrs,idents=idents)
 batch=dict(source=':agent/codex',assertions=assertions,retractions=retractions,forms=forms)
 committer=GeneratorCommitter(p.config,p.client,D)
 try:preview=committer.preview(batch,snapshot)
 except StaleBasis:continue
 save(D/'siblings-before.json',jsonable(questions));save(D/'task-items-before.json',jsonable(items));save(D/'batch.json',jsonable(batch));(D/'batch.edn').write_text(dumps(batch));(D/'snapshot.edn').write_text(dumps(snapshot))
 expected=jsonable(questions)
 for q in expected:q[':question/problem']=original[q[':db/id']]['after']
 save(D/'expected-siblings.json',expected)
 save(H/'question-preparation.json',dict(passed=True,basis=basis,directory=str(D),prompts=len(assertions),source=':agent/codex',batch_digest=digest(batch),committed=False))
 print(json.dumps(dict(basis=basis,prompts=len(assertions),preview_datoms=len(preview[':edb/tx-data']),directory=str(D))));break
else:raise RuntimeError('Preparation repeatedly raced database updates')
