"""Capture the affine-transformation topic for a scoped checkbox migration."""
import json, sys
from pathlib import Path
ROOT = next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists())
sys.path.insert(0, str(ROOT))
from scripts.generator_publish import Publisher
from capture.scripts.database.edn import dumps
HERE = Path(__file__).resolve().parent
QUESTION = '''[* {:question/difficulty [:db/id :db/ident]}
 {[:knowledge-point/_questions :limit nil] [:db/id :knowledge-point/title]}
 {[:knowledge-point/_canonical-example :limit nil] [:db/id :knowledge-point/title]}
 {[:question/answer-fields :limit nil] [* {:answer-field/type [:db/id :db/ident]}
 {:answer-field/correct [* {:answer/type [:db/id :db/ident]}]}
 {[:answer-field/choices :limit nil] [* {:answer/type [:db/id :db/ident]}]}]}]'''
ITEM = '''[* {:task-item/status [:db/id :db/ident]}
 {[:task-item/responses :limit nil] [* {:answer/type [:db/id :db/ident]}]}
 {[:task-item/working-periods :limit nil] [*]}]'''
KP = '''[* {:knowledge-point/question-generator [*]}
 {[:knowledge-point/questions :limit nil] [:db/id]}
 {:knowledge-point/canonical-example [:db/id]}
 {[:topic/_knowledge-points :limit nil] [:db/id :topic/title]}]'''
def save(name, value): (HERE/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
def main():
    db=Publisher.from_environment(source=':agent/codex').client
    identity=db.status();basis=identity['basis'];out=HERE/f'capture-{basis}';out.mkdir(exist_ok=True)
    def read(name,q,inputs):return db.query(q,inputs,out,name,basis)
    topics=read('topics','[:find (pull ?t [* {[:topic/knowledge-points :limit nil] [:db/id :knowledge-point/title]}]) :in $ ?k :where [?t :topic/knowledge-points ?k]]',[17592186172092])
    kids=sorted({k[':db/id'] for [t] in topics for k in t[':topic/knowledge-points']})
    kps=read('kps','[:find (pull ?k '+KP+') :in $ [?k ...] :where [?k :knowledge-point/id _]]',[kids])
    qids=sorted({q[':db/id'] for [k] in kps for q in k.get(':knowledge-point/questions',[])}|{k[':knowledge-point/canonical-example'][':db/id'] for [k] in kps if k.get(':knowledge-point/canonical-example')})
    questions=read('questions','[:find (pull ?q '+QUESTION+') :in $ [?q ...] :where [?q :question/id _]]',[qids])
    items=read('items','[:find ?q (pull ?i '+ITEM+') :in $ [?q ...] :where [?i :task-item/content ?q]]',[qids])
    attributes=read('attributes','[:find ?a ?ident ?type :where [?a :db/ident ?ident] [?a :db/valueType ?v] [?v :db/ident ?type]]',[])
    idents=read('idents','[:find ?e ?ident :where [?e :db/ident ?ident]]',[])
    data={**identity,'topics':topics,'kps':kps,'questions':questions,'items':items,'attributes':attributes,'idents':idents}
    (out/'snapshot.edn').write_text(dumps(data)+'\n');save('capture.json',{'directory':str(out),**identity})
    summary={'basis':basis,'topics':[{'id':t[':db/id'],'title':t.get(':topic/title')} for [t] in topics],
      'kps':[{'id':k[':db/id'],'title':k.get(':knowledge-point/title'),'questions':len(k.get(':knowledge-point/questions',[])),'generator':k.get(':knowledge-point/question-generator')} for [k] in kps],
      'questions':[{'id':q[':db/id'],'ma':q.get(':question/math-academy-id'),'problem':q.get(':question/problem'),'types':[f[':answer-field/type'][':db/ident'] for f in q.get(':question/answer-fields',[])],'choices':[[a[':answer/value'] for a in f.get(':answer-field/choices',[])] for f in q.get(':question/answer-fields',[])]} for [q] in questions], 'saved_items':len(items)}
    save('summary.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k!='questions'},default=str));print('Question records:',len(questions))
if __name__=='__main__':main()
