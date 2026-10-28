import json,sys,concurrent.futures
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'))
from migrate_learner_history import connection,loads
D=json.loads((H/'current.json').read_text());duplicates=json.loads((H/'duplicate-keys.json').read_text());targets=set([17592186577462])
for d in duplicates:
 for f in d['fields']:
  if ':answer-field/correct'not in f:targets.add(f[':db/id']);targets.update(a[':db/id']for a in f.get(':answer-field/choices',[]))
def read(task):
 history,batch,offset=task;name=('history-scalar-'if history else'incoming-scalar-')+str(batch[0]);p=H/(name+'.edn');db=connection()
 query='[:find ?v ?e ?a ?tx ?source ?added :in $ ?v :where [?e ?a ?v ?tx ?source ?added]]'if history else'[:find ?v ?e ?a :in $ ?v :where [?e ?a ?v]]'
 rows=loads(p.read_text())if p.exists()else db.query(query,[batch[0]],H,name,9837,history=history)
 return history,rows
out={False:[],True:[]};ids=sorted(targets)
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for hist,rows in pool.map(read,[(h,ids[o:o+1],o)for h in[False,True]for o in range(0,len(ids),1)]):out[hist].extend(rows)
report={'basis_t':9837,'targets':ids,'current':out[False],'history':out[True],'history_scope':'All retained datoms available at captured basis; forward incoming-reference facts, including response/history ownership, not inferred from absence in current questions.'}
(H/'incoming-history-proof.json').write_text(json.dumps(report,default=str,indent=2)+'\n');print('targets',len(ids),'currentrefs',len(out[False]),'historyrefs',len(out[True]))
