"""Read-only triangular-bank and learner-use inventory at one basis."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps,Tagged,kw
HERE=Path(__file__).parent;KP=17592186119771;SOURCE=':agent/gpt-6.1-sol-high'
QUESTION_PULL='[* {:question/difficulty [:db/id :db/ident]} {[:knowledge-point/_questions :limit nil] [:db/id]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]}]'
ITEM_PULL='[* {:task-item/status [:db/id :db/ident]} {[:task-item/responses :limit nil] [*]} {[:learner-task/_items :limit nil] [* {:learner-task/status [:db/id :db/ident]} {:learner-task/activity [:db/id :activity/title :activity/scope {:activity/type [:db/ident]}]} {[:learner/_activity :limit nil] [:db/id :learner/id]}]}]'
KP_PULL='[* {:knowledge-point/question-generator [*]} {[:topic/_knowledge-points :limit nil] [:db/id :topic/title]} {[:knowledge-point/questions :limit nil] [:db/id]} {:knowledge-point/canonical-example [:db/id]}]'
def read_matrix(text):
 match=re.search(r'\\begin\{(bmatrix|aligned)\}(.*?)\\end\{\1\}',text,re.S)
 if not match:return None
 return [[int(v.strip()) for v in row.split('&')] for row in match[2].split(r'\\')]
def main():
 db=Publisher.from_environment(source=SOURCE).client;identity=db.status();basis=identity['basis'];out=HERE/f'capture-{basis}';out.mkdir(parents=True,exist_ok=True)
 def read(name,q,inputs):return db.query(q,inputs,out,name,basis)
 kp=read('kp','[:find (pull ?k '+KP_PULL+') :in $ ?k :where [?k :knowledge-point/id _]]',[KP])[0][0]
 ids=sorted(q[':db/id'] for q in kp[':knowledge-point/questions'])
 specs={'questions':('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id _]]',[ids]),'items':('[:find ?q (pull ?i '+ITEM_PULL+') :in $ [?q ...] :where [?i :task-item/content ?q]]',[ids]),'incoming':('[:find ?e ?a ?q :in $ [?q ...] :where [?e ?a ?q]]',[[Tagged('edb/ref',q) for q in ids]]),'attributes':('[:find ?a ?ident :where [?a :db/ident ?ident] [?a :db/valueType _]]',[]),'source':('[:find ?e :in $ ?ident :where [?e :db/ident ?ident]]',[kw(SOURCE)])}
 with ThreadPoolExecutor(max_workers=3) as pool:
  fs={n:pool.submit(read,n,*a) for n,a in specs.items()};data={n:f.result() for n,f in fs.items()}
 snapshot={**identity,'kp':kp,**data};(out/'snapshot.edn').write_text(dumps(snapshot)+'\n');(out/'snapshot.json').write_text(json.dumps(snapshot,indent=2,default=str)+'\n')
 rows=[]
 for [q] in data['questions']:
  matrix=read_matrix(q[':question/problem']);n=len(matrix) if matrix else 0
  diagonal=matrix and all(not matrix[i][j] for i in range(n) for j in range(n) if i!=j)
  above=sum(matrix[i][j]!=0 for i in range(n) for j in range(i+1,n)) if matrix else 0
  below=sum(matrix[i][j]!=0 for i in range(n) for j in range(i)) if matrix else 0
  row={'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'difficulty':q.get(':question/difficulty',{}).get(':db/ident'),'matrix':matrix,'family':'diagonal' if diagonal else 'upper' if above and not below else 'lower' if below and not above else 'other','nonzero_diagonal':sum(matrix[i][i]!=0 for i in range(n)) if matrix else 0,'nonzero_off_diagonal':above+below,'items':[{'item':i[':db/id'],'status':i[':task-item/status'][':db/ident'],'owners':i.get(':learner-task/_items',[])} for qid,i in data['items'] if qid==q[':db/id']]}
  rows.append(row)
 (out/'inventory.json').write_text(json.dumps(rows,indent=2,default=str)+'\n');(HERE/'capture-directory.txt').write_text(str(out.relative_to(ROOT))+'\n')
 print(json.dumps({'basis':basis,'count':len(rows),'generator':kp.get(':knowledge-point/question-generator'),'topic':kp.get(':topic/_knowledge-points'),'inventory':[dict(r,items=[{'item':i['item'],'status':i['status'],'tasks':[o[':db/id'] for o in (i['owners'] if isinstance(i['owners'],list) else [i['owners']])]} for i in r['items']]) for r in rows]},indent=2,default=str))
if __name__=='__main__':main()
