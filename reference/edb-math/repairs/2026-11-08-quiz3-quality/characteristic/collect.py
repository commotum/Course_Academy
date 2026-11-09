import sys,json
from pathlib import Path
sys.path.insert(0,'/home/jake/Developer/Course_Academy/scripts')
from migrate_learner_history import connection
root=Path('/home/jake/Developer/Course_Academy');out=root/'reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic';out.mkdir(parents=True,exist_ok=True)
db=connection();basis=db.basis();(out/'basis.json').write_text(json.dumps({'basis':basis}))
query=(root/'reference/edb-math/audits/2026-11-08-topic-17592186048459/topic-before-query.edn').read_text()
lessonq=(root/'reference/edb-math/audits/2026-11-08-topic-17592186048459/lessons-before-query.edn').read_text()
for i in [48391,50433,48289,49099,50557,50040]:
 eid=17592186000000+i;p=out/str(eid);p.mkdir(exist_ok=True)
 topic=db.query(query,[eid],p,'topic',basis)[0][0];lessons=db.query(lessonq,[eid],p,'lessons',basis)
 (p/'topic.json').write_text(json.dumps(topic,indent=2,default=str));(p/'lessons.json').write_text(json.dumps(lessons,indent=2,default=str))
 qs={q[':db/id']:q for kp in topic.get(':topic/knowledge-points',[]) for q in [kp.get(':knowledge-point/canonical-example',{})]+kp.get(':knowledge-point/questions',[]) if q}
 (p/'questions.json').write_text(json.dumps(list(qs.values()),indent=2,default=str))
 with (p/'inspection.txt').open('w')as f:
  for l in lessons:f.write('LESSON '+json.dumps(l,indent=2,default=str)+'\n')
  for kp in topic.get(':topic/knowledge-points',[]):
   f.write('\nKP '+str(kp[':db/id'])+' '+kp.get(':knowledge-point/title','')+'\n')
   for q in [kp.get(':knowledge-point/canonical-example',{})]+kp.get(':knowledge-point/questions',[]):
    if not q:continue
    f.write('\nQUESTION '+str(q[':db/id'])+' '+q.get(':question/math-academy-id','')+'\n'+q.get(':question/problem','')+'\nSOLUTION\n'+q.get(':question/worked-solution','MISSING')+'\n')
    for field in q.get(':question/answer-fields',[]):
     f.write('FIELD '+str(field[':db/id'])+' '+field.get(':answer-field/key','')+' '+str(field.get(':answer-field/type'))+' correct '+str(field.get(':answer-field/correct'))+'\nCHOICES '+str(field.get(':answer-field/choices'))+'\n')
 print(eid,len(qs),len(lessons))
