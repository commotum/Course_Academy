import json,sys
from pathlib import Path
out=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/foundations');fs=[];bugs=[]
for d in sorted(out.glob('175*')):
 qs=json.loads((d/'questions-before.json').read_text());ls=json.loads((d/'lessons-before.json').read_text());local=[]
 for a in ls:
  for s in a[0].get(':activity/steps',[]):
   c=s[':step/content']
   if c.get(':tutorial/content'):local.append({'entity':c[':db/id'],'attribute':':tutorial/content','value':c[':tutorial/content']})
 for q in qs:
  for a in [':question/problem',':question/worked-solution']:
   if q.get(a):
    f={'entity':q[':db/id'],'attribute':a,'value':q[a]}
    if a==':question/problem':f['fields']=[{'id':str(f[':db/id']),'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1]}for f in q.get(':question/answer-fields',[])]
    local.append(f)
  for f in q.get(':question/answer-fields',[]):
   if f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox':local.append({'entity':f[':db/id'],'attribute':':answer-field/key','value':f[':answer-field/key']})
   for a in f.get(':answer-field/choices',[]):
    local.append({'entity':a[':db/id'],'attribute':':answer/value','value':a[':answer/value'],'bare_math':a[':answer/type'][':db/ident']==':answer.type/math'})
 (d/'fields-before.json').write_text(json.dumps(local,indent=2));fs+=local
(out/'fields-before.json').write_text(json.dumps(fs,indent=2));print(len(fs))
