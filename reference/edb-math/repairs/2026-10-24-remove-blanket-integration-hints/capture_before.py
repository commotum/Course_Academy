"""Capture all affected live KPs at one basis before changing hint policy."""
from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT/'scripts'))
from generator_publish import Publisher,KP_PULL,jsonable
TRIG=(17592186068915,17592186068916,17592186068917,17592186068918)
OTHER=(17592186064218,17592186064219,17592186064250,17592186064220,17592186184349,17592186184350,17592186184351,17592186184352)
p=Publisher.from_environment(source=':agent/codex');basis=p.client.status()['basis']
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3)as pool:rows=[[k]for k in pool.map(lambda kp:p.read_kp(kp,H/str(kp)/'capture',basis),TRIG+OTHER)]
summary=[]
for[k]in rows:
 k=jsonable(k);kp=k[':db/id'];old=ROOT/'reference/edb-math/repairs'/('2026-10-24-trig-scaffolding'if kp in TRIG else'2026-10-24-two-topic-pedagogy')/str(kp)
 proof=json.loads((old/'verification.json').read_text());active=[q for q in k[':knowledge-point/questions']if not q.get(':question/math-academy-id')and not q.get(':question/retired')]
 assert{q[':db/id']for q in active}=={q['entity']for q in proof['new_questions']},('Pool changed',kp,len(active))
 records=json.loads((old/('publication/preparation.json'if kp in TRIG else'accepted-pool.json')).read_text());records=records['records']if isinstance(records,dict)else records
 assert{r['question'][':question/id']for r in records}=={q[':question/id']for q in active}
 d=H/str(kp);d.mkdir(exist_ok=True);(d/'before.json').write_text(json.dumps(k,indent=2)+'\n');(d/'records-before.json').write_text(json.dumps(records,indent=2)+'\n');(d/'source.json').write_text((old/'source/source.json').read_text())
 n=sum('You may use $'in q[':question/problem']or'Endpoint values:'in q[':question/problem']for q in active)
 summary.append({'kp':kp,'title':k[':knowledge-point/title'],'active_generated':len(active),'with_blanket_hints':n,'registered_generator':k[':knowledge-point/question-generator'][':question-generator/script'],'prior_evidence':str(old)})
(H/'capture.json').write_text(json.dumps({'basis':basis,'knowledge_points':summary},indent=2)+'\n');print(json.dumps({'basis':basis,'kps':len(summary),'active_generated':sum(r['active_generated']for r in summary),'hinted':sum(r['with_blanket_hints']for r in summary)}))
