import concurrent.futures,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from migrate_learner_history import connection,loads
D=json.loads((H/'duplicate-keys.json').read_text());ids={17592186577462}
for d in D:
 for f in d['fields']:
  if ':answer-field/correct'not in f:ids.add(f[':db/id']);ids.update(a[':db/id']for a in f.get(':answer-field/choices',[]))
def read(task):
 history,e=task;name=('history-literal-'if history else'incoming-literal-')+str(e);p=H/(name+'.edn')
 query=f'[:find ?e ?a ?tx ?source ?added :where [?e ?a {e} ?tx ?source ?added]]'if history else f'[:find ?e ?a :where [?e ?a {e}]]'
 try:
  rows=loads(p.read_text())if p.exists()else connection().query(query,[],H,name,9837,history=history);return {'target':e,'history':history,'rows':rows,'error':None}
 except subprocess.CalledProcessError as ex:return {'target':e,'history':history,'rows':[],'error':ex.stderr}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 for row in pool.map(read,[(h,e)for h in[False,True]for e in sorted(ids)]):
  results.append(row);(H/'incoming-history-proof.json').write_text(json.dumps({'basis_t':9837,'targets':sorted(ids),'results':results},default=str,indent=2)+'\n');print(row['target'],row['history'],len(row['rows']),row['error'],flush=True)
