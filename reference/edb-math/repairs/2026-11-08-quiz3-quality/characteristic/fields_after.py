import json,re
from pathlib import Path
root=Path('/home/jake/Developer/Course_Academy');base=root/'reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic'
for d in base.glob('175*'):
 fields=[];seen=set()
 for q in json.loads((d/'questions-after.json').read_text()):
  fs=[{'id':str(f[':db/id']),'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':[{'id':str(a[':db/id']),'type':a[':answer/type'][':db/ident'].split('/')[-1],'value':a[':answer/value']}for a in f.get(':answer-field/choices',[])]}for f in q.get(':question/answer-fields',[])]
  for attr in [':question/problem',':question/worked-solution']:
   if attr in q:fields.append({'entity':q[':db/id'],'attribute':attr,'value':q[attr],**({'fields':fs}if attr.endswith('/problem')else {})})
  for f in q.get(':question/answer-fields',[]):
   for a in f.get(':answer-field/choices',[]):
    if a[':db/id']not in seen:fields.append({'entity':a[':db/id'],'attribute':':answer/value','value':a[':answer/value'],'bare_math':a[':answer/type'][':db/ident']==':answer.type/math'});seen.add(a[':db/id'])
 for l in json.loads((d/'lessons-after.json').read_text()):
  for s in l[0][':activity/steps']:
   c=s[':step/content']
   if ':tutorial/content'in c:fields.append({'entity':c[':db/id'],'attribute':':tutorial/content','value':c[':tutorial/content']})
 (d/'fields-after.json').write_text(json.dumps(fields,indent=2))
print(sum(len(json.loads((d/'fields-after.json').read_text()))for d in base.glob('175*')))
