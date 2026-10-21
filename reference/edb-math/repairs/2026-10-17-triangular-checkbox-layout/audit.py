"""Capture current selection layout, ownership and saved uses at one basis."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0,str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps,Tagged,kw
HERE=Path(__file__).resolve().parent
SOURCE=':agent/gpt-6.1-sol-high'
TARGETS=[17592186262617,17592186120421,17592186119585]
QUESTION_PULL='[* {:question/difficulty [:db/id :db/ident]} {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/title]} {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/title]} {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]} {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]}]'
KP_PULL='[* {:knowledge-point/question-generator [*]} {[:knowledge-point/questions :limit nil] [:db/id]} {:knowledge-point/canonical-example [:db/id]} {[:topic/_knowledge-points :limit nil] [:db/id :topic/title]}]'
ITEM_PULL='[* {:task-item/status [:db/id :db/ident]} {[:task-item/responses :limit nil] [*]} {[:learner-task/_items :limit nil] [:db/id :learner-task/id {:learner-task/status [:db/id :db/ident]} {:learner-task/activity [:db/id :activity/title]}]}]'
def main():
 db=Publisher.from_environment(source=SOURCE).client;identity=db.status();basis=identity['basis'];out=HERE/f'capture-{basis}';out.mkdir(parents=True,exist_ok=True)
 def read(name,q,inputs):return db.query(q,inputs,out,name,basis)
 targets=read('targets','[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id _]]',[TARGETS])
 kids=sorted({k[':db/id'] for [q] in targets for attr in [':knowledge-point/_questions',':knowledge-point/_canonical-example'] for k in q.get(attr,[])})
 kps=read('kps','[:find (pull ?k '+KP_PULL+') :in $ [?k ...] :where [?k :knowledge-point/id _]]',[kids])
 ids=sorted(set(TARGETS)|{q[':db/id'] for [k] in kps for q in k.get(':knowledge-point/questions',[])})
 specs={'questions':('[:find (pull ?q '+QUESTION_PULL+') :in $ [?q ...] :where [?q :question/id _]]',[ids]),'items':('[:find ?q (pull ?i '+ITEM_PULL+') :in $ [?q ...] :where [?i :task-item/content ?q]]',[ids]),'incoming':('[:find ?e ?a ?q :in $ [?q ...] :where [?e ?a ?q]]',[[Tagged('edb/ref',q) for q in ids]]),'attributes':('[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[]),'idents':('[:find ?e ?ident :where [?e :db/ident ?ident]]',[])}
 with ThreadPoolExecutor(max_workers=3) as pool:
  fs={n:pool.submit(read,n,*a) for n,a in specs.items()};data={n:f.result() for n,f in fs.items()}
 snapshot={**identity,'targets':targets,'kps':kps,**data}
 (out/'snapshot.edn').write_text(dumps(snapshot)+'\n');(out/'snapshot.json').write_text(json.dumps(snapshot,indent=2,default=str)+'\n');(HERE/'capture-directory.txt').write_text(str(out.relative_to(ROOT))+'\n')
 print(json.dumps({'basis':basis,'question_count':len(ids),'kps':[{'id':k[':db/id'],'title':k[':knowledge-point/title'],'generator':k.get(':knowledge-point/question-generator')} for [k] in kps],'targets':[q for [q] in targets]},indent=2,default=str))
if __name__=='__main__':main()
