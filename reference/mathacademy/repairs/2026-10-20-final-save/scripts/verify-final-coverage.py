from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import threading
from scripts.config import Config
from scripts.database.client import EDBClient
from scripts.storage import read_json,atomic_json
root=Path('reference/mathacademy/repairs/2026-10-20-final-save');out=root/'coverage';out.mkdir(exist_ok=True)
ids=read_json(root/'source-inventory.json')['unique_source_ids'];c=EDBClient(Config(),threading.Event());basis=c.basis()
groups=[ids[i:i+1000]for i in range(0,len(ids),1000)]
def query(pair):
 i,group=pair
 return c.query('[:find ?id :in $ [?id ...] :where [?q :question/math-academy-id ?id]]',[group],out,'source-ids-'+str(i),basis)
with ThreadPoolExecutor(max_workers=4)as pool:results=list(pool.map(query,enumerate(groups)))
found={r[0]for rows in results for r in rows};missing=sorted(set(ids)-found)
proof={'basis':basis,'captured_unique_ids':len(ids),'present_source_ids':len(found),'missing_source_ids':missing,'bounded_queries':len(groups),'status':'pass'if not missing else'needs_identity_review'}
atomic_json(out/'verification.json',proof);print(proof)
