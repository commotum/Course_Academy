"""Index the newer capture package's hashed HTML observations and lesson pages."""
import collections,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from source_tables import tables,H,R
from enrich_sources import fences
W=R/'.local/edb/mathml-tables-work';meta=json.loads((W/'metadata.json').read_text());wanted={r['question/math-academy-id'] for r in meta.values() if 'question/math-academy-id' in r};wanted_t={str(r['tutorial/math-academy-id']) for r in meta.values() if 'tutorial/math-academy-id' in r};paths=[Path(p) for p in (W/'new-capture-html-paths.txt').read_text().splitlines()];groups=collections.defaultdict(list);lessons=[]
for p in paths:
 m=re.match(r'^(history-solution-q-|history-q-|step-q)(\d+)-',p.name)
 if m and 'q-'+m[2] in wanted:groups['q-'+m[2]].append(({'history-solution-q-':3,'history-q-':2,'step-q':1}[m[1]],p))
 elif p.name.startswith('lesson-topic-'):lessons.append(p)
out=[];counts=collections.Counter();source_fields={}
def add_part(part,identity,attr,path,**extra):
 records=tables(str(part),identity,attr,path,**extra)
 if records:
  original=[t for t in part.find_all('mtable') if any(v not in ['none',''] for k in ['frame','rowlines','columnlines'] for v in t.get(k,'none').split())]
  for r,t in zip(records,original):r['source_fences']=fences(t);out.append(r)
 return bool(records)
for i,(identity,options) in enumerate(groups.items()):
 selected=set()
 for priority,p in sorted(options,key=lambda row:(row[0],row[1].stat().st_mtime_ns),reverse=True):
  needed={'question/problem','question/worked-solution','answer/value'}-selected
  if not needed:break
  raw=p.read_text();counts['observations_read']+=1
  if '<mtable' not in raw or not any(k in raw for k in ['rowlines','columnlines','frame']):continue
  soup=BeautifulSoup(raw,'html.parser')
  if 'question/worked-solution' in needed:
   parts=soup.find_all(class_=['questionExplanation','questionWidget-explanation','exampleExplanation'])
   if parts:
    if any(add_part(part,identity,'question/worked-solution',p) for part in parts):selected.add('question/worked-solution')
  if 'question/problem' in needed:
   parts=soup.find_all(class_=['questionWidget-text','questionText'])
   if parts:
    if any(add_part(part,identity,'question/problem',p) for part in parts):selected.add('question/problem')
  if 'answer/value' in needed:
   parts=soup.find_all(class_=['questionWidget-choiceText','choiceText','selectListOption'])
   if parts:
    found=False
    for part in parts:found=add_part(part,identity,'answer/value',p,option_dom_id=part.get('id')) or found
    if found:selected.add('answer/value')
 if i%2500==0:print('New capture questions',i,'/',len(groups),'ruled tables',len(out),flush=True)
# Latest complete lesson copies provide tutorial and canonical-example evidence.
seen=set()
for p in sorted(lessons,key=lambda p:p.stat().st_mtime_ns,reverse=True):
 raw=p.read_text();counts['lesson_pages_read']+=1
 if '<mtable' not in raw or not any(k in raw for k in ['rowlines','columnlines','frame']):continue
 soup=BeautifulSoup(raw,'html.parser')
 for step in soup.select('.step[contentid]'):
  kind=step.get('steptype');cid=step.get('contentid');identity='tutorial:'+cid if kind=='tutorial' else 'e-'+cid
  if kind=='tutorial':parts=[('tutorial/content',step)] if cid in wanted_t else []
  elif kind=='example' and identity in wanted:parts=[('question/problem',n) for n in step.find_all(class_='exampleQuestion')]+[('question/worked-solution',n) for n in step.find_all(class_='exampleExplanation')]
  else:continue
  for attr,part in parts:
   if (identity,attr) in seen:continue
   if add_part(part,identity,attr,p,step_id=step.get('stepid')):seen.add((identity,attr))
unique={}
for r in out:unique[r['identity'],r['attribute'],r['old_tex'],json.dumps(r['source_attributes'],sort_keys=True),tuple(r.get('source_fences',[]))]=r
out=list(unique.values());(H/'new-capture-tables.json').write_text(json.dumps(out,indent=2)+'\n');summary={'question_identities_examined':len(groups),'source_tables':len(out),'source_identities_with_ruled_tables':len({r['identity'] for r in out}),**counts};(H/'new-capture-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
