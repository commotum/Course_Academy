"""Database-wide read-only checkbox discovery at one captured EDB basis."""
import concurrent.futures,json,subprocess,sys
from pathlib import Path
from types import SimpleNamespace
ROOT=Path.cwd();OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from database import Database
BASIS=1534
LINEAGE='01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'
class Reader(Database):
 def command(self,command,*options):
  if command=='query':options=(*options,'--max-value-bytes',str(64*1024*1024))
  try:return super().command(command,*options)
  except subprocess.CalledProcessError as e:raise RuntimeError(e.stderr)from e
DB=Reader(SimpleNamespace(edb_bin=str(ROOT/'.local/edb/capture-runtime/math-edb'),database='math',capture_only=True))
QUESTION='''[:db/id :question/math-academy-id :question/problem
 {[:question/answer-fields :limit nil] [:db/id :answer-field/key
  {:answer-field/type [:db/ident]}
  {:answer-field/correct [:db/id :answer/value {:answer/type [:db/ident]}]}
  {[:answer-field/choices :limit nil] [:db/id :answer/value {:answer/type [:db/ident]}]}]}]'''
KP='''[:db/id :knowledge-point/title
 {[:topic/_knowledge-points :limit nil] [:db/id :topic/title :topic/math-academy-id]}
 {[:knowledge-point/questions :limit nil] '''+QUESTION+'''}]'''
QUERY='[:find (pull ?kp '+KP+') :in $ [?kp ...] :where [?kp :knowledge-point/id _]]'
def read(group):
 rows=DB.query(QUERY,[group],OUT/'evidence','batch-'+str(group[0]),BASIS)
 assert {r[0][':db/id']for r in rows}==set(group)
 for row in rows:
  kp=row[0];(OUT/'sources'/str(kp[':db/id'])).with_suffix('.json').write_text(json.dumps(kp,indent=2)+'\n')
 return len(group)
def main():
 ids=sorted(r[0]for r in DB.query('[:find ?kp :where [?kp :knowledge-point/id _]]',[],OUT/'evidence','kp-ids',BASIS))
 print('Knowledge points:',len(ids),flush=True)
 (OUT/'sources').mkdir(exist_ok=True)
 groups=[ids[i:i+16]for i in range(0,len(ids),16)if not all((OUT/'sources'/str(e)).with_suffix('.json').exists()for e in ids[i:i+16])]
 done=len(ids)-sum(map(len,groups))
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
  for n in pool.map(read,groups):
   done+=n
   if done%128==0 or done==len(ids):print('Captured',done,'/',len(ids),'KPs',flush=True)
 records=[json.loads((OUT/'sources'/str(e)).with_suffix('.json').read_text())for e in ids]
 qs={q[':db/id']:q for kp in records for q in kp.get(':knowledge-point/questions',[])}
 report={'database':'math','basis':BASIS,'lineage':LINEAGE,'knowledge_point_ids':ids,'knowledge_points':len(ids),'practice_questions':len(qs),'database_writes':0,'canonical_only_examples_excluded':True}
 (OUT/'inventory.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='knowledge_point_ids'}),flush=True)
if __name__=='__main__':main()
