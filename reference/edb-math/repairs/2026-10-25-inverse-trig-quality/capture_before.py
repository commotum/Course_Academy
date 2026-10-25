from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sys,json
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher,jsonable,normalized_question
KPS=(17592186064218,17592186064219,17592186064250,17592186064220)
p=Publisher.from_environment(source=':agent/codex');status=p.client.status();basis=status['basis'];previous=H.with_name('2026-10-25-restore-substitution-recognition')
def capture(kp):
 d=H/str(kp);k=p.read_kp(kp,d/'capture',basis);p._source_from_kp(kp,d/'fresh-source',status,basis,k);k=jsonable(k)
 records=json.loads((previous/str(kp)/'accepted-pool.json').read_text());active={q[':question/id']:q for q in k[':knowledge-point/questions']if not q.get(':question/math-academy-id')and not q.get(':question/retired')}
 assert set(active)=={r['question'][':question/id']for r in records}
 for r in records:assert normalized_question(active[r['question'][':question/id']])==normalized_question(r['question'])
 (d/'before.json').write_text(json.dumps(k,indent=2)+'\n');(d/'records-before.json').write_text(json.dumps(records,indent=2)+'\n')
 return {'kp':kp,'title':k[':knowledge-point/title'],'registered_generator':k[':knowledge-point/question-generator'][':question-generator/script']}
with ThreadPoolExecutor(max_workers=3)as pool:rows=list(pool.map(capture,KPS))
(H/'capture.json').write_text(json.dumps({'basis':basis,'knowledge_points':rows},indent=2)+'\n');print('Captured',len(rows),'KPs at',basis)
