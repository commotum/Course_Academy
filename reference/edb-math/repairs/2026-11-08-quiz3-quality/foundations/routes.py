import json,re
from pathlib import Path
from bs4 import BeautifulSoup
H=Path(__file__).resolve().parent;rows=[]
for d in sorted(H.glob('175*')):
 topic=json.loads((d/'topic-before.json').read_text());mid=topic[':topic/math-academy-id'];src=Path(f'/home/jake/Developer/MA/DATA/Lessons/{mid}/Source/{mid}.html');soup=BeautifulSoup(src.read_text(),'html.parser')
 for ar in json.loads((d/'lessons-after.json').read_text()):
  activity=ar[0];steps={s[':db/id']:s for s in activity[':activity/steps']};route=[];eid=activity[':activity/first-step'][':db/id']
  while eid is not None:
   assert eid in steps and eid not in route,(d.name,eid)
   route.append(eid);eid=steps[eid].get(':step/next',{}).get(':db/id')
  assert set(route)==set(steps)
  sourceids=[str(steps[e][':step/math-academy-id'])for e in route];domids=[n.get('id').split('-')[-1]for n in soup.select('[id^="step-"]')if n.get('id').split('-')[-1]in sourceids]
  source_titles=[re.sub(r'^Example:\s*','',(n.select_one('.stepName').get_text(' ',strip=True)if n.select_one('.stepName')else n.get_text(' ',strip=True).split('?')[0]).strip())for n in soup.select('[id^="step-"]')]
  stored_titles=[steps[e][':step/content'].get(':tutorial/title',steps[e][':step/content'].get(':knowledge-point/title'))for e in route]
  tutorials=[steps[e][':step/content']for e in route if steps[e][':step/content'].get(':tutorial/content')]
  r={'topic':int(d.name),'title':topic[':topic/title'],'steps':len(route),'tutorials':len(tutorials),'knowledge_points':len(topic[':topic/knowledge-points']),'canonical_examples':sum(bool(k.get(':knowledge-point/canonical-example'))for k in topic[':topic/knowledge-points']),'complete_acyclic_route':True,'source_step_order':domids,'saved_route_source_ids':sourceids,'source_order_agrees':domids==sourceids or source_titles==stored_titles,'source_titles':source_titles,'stored_titles':stored_titles,'tutorial_source_roles':[{'entity':c[':db/id'],'title':c.get(':tutorial/title'),'source':str(src),'source_node_present':c.get(':tutorial/title')in source_titles or soup.select_one('#step-'+str(next(s[':step/math-academy-id']for s in steps.values()if s[':step/content'][':db/id']==c[':db/id'])))is not None}for c in tutorials]};rows.append(r)
(H/'routes.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
