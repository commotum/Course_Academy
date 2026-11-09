import sys,json,hashlib,re
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from migrate_learner_history import connection,kw,loads,dumps
IDS=[17592186050032,17592186050150,17592186050895,17592186049102,17592186049370,17592186050522]
db=connection();basis=db.basis();(HERE/'basis.json').write_text(json.dumps({'basis':basis}))
base=ROOT/'reference/edb-math/audits/2026-11-08-topic-17592186048459'
tq=(base/'topic-before-query.edn').read_text();lq=(base/'lessons-before-query.edn').read_text()
for tid in IDS:
 out=HERE/str(tid);out.mkdir(exist_ok=True)
 topic=db.query(tq,[tid],out,'topic-before',basis)[0][0];lessons=db.query(lq,[tid],out,'lessons-before',basis)
 (out/'topic.json').write_text(json.dumps(topic,indent=2,default=str));(out/'lessons.json').write_text(json.dumps(lessons,indent=2,default=str))
 qs={q[':db/id']:q for kp in topic[':topic/knowledge-points'] for q in [kp[':knowledge-point/canonical-example']]+kp.get(':knowledge-point/questions',[])}
 (out/'questions.json').write_text(json.dumps(list(qs.values()),indent=2,default=str))
 fields=[]
 def walk(v):
  if isinstance(v,dict):
   for k,x in v.items():
    if isinstance(x,str) and (k in [':tutorial/content',':question/problem',':question/worked-solution',':answer/value',':answer/feedback',':knowledge-point/description']):
     f={'entity':v[':db/id'],'attribute':k,'value':x}
     if k==':question/problem':f['fields']=[{'id':str(a[':db/id']),'key':a[':answer-field/key'],'type':a[':answer-field/type'][':db/ident'].split('/')[-1]} for a in v.get(':question/answer-fields',[])]
     fields.append(f)
    else:walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 walk(topic);walk(lessons)
 fields=list({(f['entity'],f['attribute']):f for f in fields}.values());(out/'fields.json').write_text(json.dumps(fields,indent=2))
 text=[]
 for f in fields:
  text.append(f"\n=== {f['entity']} {f['attribute']} ===\n{f['value']}")
 (out/'content.txt').write_text('\n'.join(text))
 print(tid,topic[':topic/title'],topic[':topic/math-academy-id'],'KP',len(topic[':topic/knowledge-points']),'Q',len(qs),'fields',len(fields),'lessons',len(lessons),flush=True)
