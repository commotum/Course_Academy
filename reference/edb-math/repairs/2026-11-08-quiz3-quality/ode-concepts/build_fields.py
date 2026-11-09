import json
from pathlib import Path
H=Path(__file__).resolve().parent
fields=[];cards=[]
for d in sorted(H.glob('175*')):
 qs=json.loads((d/'questions-after.json').read_text());lessons=json.loads((d/'lessons-after.json').read_text())
 for q in qs:
  card={'entity':q[':db/id'],'mid':q[':question/math-academy-id'],'topic':int(d.name),'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution',''),'fields':[]}
  for f in q.get(':question/answer-fields',[]):
   ff={'id':str(f[':db/id']),'key':f[':answer-field/key'],'type':f[':answer-field/type'][':db/ident'].split('/')[-1],'choices':[]}
   for a in f.get(':answer-field/choices',[]):
    typ=a[':answer/type'][':db/ident'].split('/')[-1];ff['choices'].append({'id':str(a[':db/id']),'type':typ,'value':a[':answer/value']});fields.append({'entity':a[':db/id'],'attribute':':answer/value','value':a[':answer/value'],'bare_math':typ=='math'})
   if ff['type']=='checkbox':fields.append({'entity':f[':db/id'],'attribute':':answer-field/key','value':f[':answer-field/key']})
   card['fields'].append(ff)
  for k,v in [('problem',card['prompt']),('worked-solution',card['solution'])]:
   if v:fields.append({'entity':q[':db/id'],'attribute':':question/'+k,'value':v,'fields':card['fields']if k=='problem'else[]})
  cards.append(card)
 for a in lessons:
  for s in a[0][':activity/steps']:
   c=s[':step/content']
   if ':tutorial/content'in c:
    fields.append({'entity':c[':db/id'],'attribute':':tutorial/content','value':c[':tutorial/content']});cards.append({'entity':c[':db/id'],'topic':int(d.name),'mid':'tutorial-'+str(c[':tutorial/math-academy-id']),'prompt':c[':tutorial/content'],'solution':'','fields':[]})
fields=list({(f['entity'],f['attribute']):f for f in fields}.values());(H/'fields-after.json').write_text(json.dumps(fields,indent=2));(H/'cards-after.json').write_text(json.dumps(cards,indent=2));print('fields',len(fields),'cards',len(cards))
