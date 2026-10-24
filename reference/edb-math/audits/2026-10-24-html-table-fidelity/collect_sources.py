"""Collect archived source tables in exact question/tutorial content containers."""
import collections,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from tables import H,R,W,compact_dom,source_table

def main():
 inventory=json.loads((W/'inventory.json').read_text());meta=json.loads((W/'metadata.json').read_text());owners=json.loads((W/'owners.json').read_text());wanted=set()
 for r in inventory:
  if r['a']=='tutorial/content':wanted.add('tutorial:'+str(r['metadata'].get('tutorial/math-academy-id')))
  elif r['a'].startswith('question/'):wanted.add(r['metadata'].get('question/math-academy-id'))
  else:
   fields=[r['e']]if r['a']=='answer-field/key'else[p for p,a in owners.get(str(r['e']),[])if a=='answer-field/choices']
   for field in fields:
    for q,a in owners.get(str(field),[]):
     if a=='question/answer-fields':wanted.add(meta.get(str(q),{}).get('question/math-academy-id'))
 wanted.discard(None);out=[];counts=collections.Counter()
 for p in sorted(Path('/home/jake/Developer/MA/DATA/Lessons').glob('*/Source/*.html')):
  raw=p.read_text();counts['lesson_files_examined']+=1
  if not re.search(r'<table\b',raw,re.I):continue
  data=json.loads(p.with_suffix('.json').read_text());items=data.get('lesson',{}).get('items',[]);use=[]
  for i in items:
   if i['item_type']=='step':
    kind=i['step_type'];identity=('tutorial:'+str(i['content_id']))if kind=='tutorial'else'e-'+str(i['content_id'])
   else:kind='question';identity='q-'+str(i['question_id'])
   if identity in wanted:use.append((i,kind,identity))
  if not use:continue
  soup=BeautifulSoup(compact_dom(raw),'html.parser');counts['lesson_pages_with_relevant_html_tables']+=1
  for item,kind,identity in use:
   root=soup.find(id=item['dom_id'])
   if root is None:continue
   if kind=='tutorial':parts=[('tutorial/content',root)]
   else:
    parts=[('question/problem',p)for p in root.find_all(class_=['exampleQuestion','questionText','questionWidget-text'])]+[('question/worked-solution',p)for p in root.find_all(class_=['exampleExplanation','questionExplanation','questionWidget-explanation'])]+[('answer/value',p)for p in root.find_all(class_=['questionWidget-choiceText','choiceText','selectListOption'])]
   for attr,part in parts:
    for index,t in enumerate(part.find_all('table')):
     if set(t.get('class',[]))&{'questionWidget-choicesTable','choicesTable','choiceTable'}:continue
     out.append(source_table(t,identity,attr,p,topic=data['topic_id'],dom_id=item['dom_id'],table_index=index))
  if len(out)and len(out)%100==0:print('Source table records',len(out),flush=True)
 (H/'archive-source-tables.json').write_text(json.dumps(out,indent=2)+'\n');report={**counts,'source_tables':len(out),'source_identities':len({r['identity']for r in out}),'feature_counts':dict(collections.Counter(k for r in out for k,v in r['features'].items()if v))};(H/'source-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
