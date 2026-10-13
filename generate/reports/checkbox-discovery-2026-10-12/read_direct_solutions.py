import json,importlib.util,concurrent.futures
from pathlib import Path
p=Path('generate/reports/checkbox-discovery-2026-10-12');spec=importlib.util.spec_from_file_location('scan',p/'scan.py');scan=importlib.util.module_from_spec(spec);spec.loader.exec_module(scan)
ids=[q['id']for q in json.loads((p/'direct-format-provisional.json').read_text())]
query='[:find (pull ?q [:db/id :question/worked-solution]) :in $ [?q ...] :where [?q :question/id _]]'
def read(group):return scan.DB.query(query,[group],p/'evidence','direct-solutions-'+str(group[0]),scan.BASIS)
rows=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
 for result in pool.map(read,[ids[i:i+128]for i in range(0,len(ids),128)]):rows.extend(x[0]for x in result)
assert set(ids)=={q[':db/id']for q in rows}
(p/'direct-worked-solutions.json').write_text(json.dumps(rows,indent=2)+'\n')
print('Read',len(rows),'worked solutions at basis',scan.BASIS)
