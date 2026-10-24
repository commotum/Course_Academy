import json,collections
from pathlib import Path
from bs4 import BeautifulSoup
from enrich_sources import fences
from source_tables import H,R,LegacyRenderer
cache={};soup_cache={}
def get_doc(r):
 path=Path(r['path']);path=path if path.is_absolute() else R/path
 if str(path) not in cache:cache[str(path)]=path.read_text() if path.suffix=='.html' else json.loads(path.read_text())
 d=cache[str(path)];identity=r['identity'];attr=r['attribute'];docs=[]
 if isinstance(d,str):docs=[d]
 elif path.name=='observations.json':
  for task in d['tasks']:
   for q in task['questions']:
    if q['id'].replace('question-','q-')==identity:docs.append(q.get('problem_html' if attr=='question/problem' else 'worked_solution_html',''))
 elif path.name=='state.json':
  record=d.get('questions',{}).get(identity,{})
  keys=['history','after','before'] if attr=='question/worked-solution' else ['before','history','after']
  for k in keys:
   if isinstance(record.get(k),dict):
    markup=record[k].get('html') or record[k].get('raw_html') or ''
    if markup:docs.append(markup)
    if attr=='question/worked-solution' and markup and any(cls in markup for cls in ['questionExplanation','questionWidget-explanation','exampleExplanation']):break
 else:docs=[d.get('html') or d.get('raw_html') or '']
 result=[]
 for markup in docs:
  if not markup:continue
  ck=markup
  if ck not in soup_cache:soup_cache[ck]=BeautifulSoup(markup,'html.parser')
  soup=soup_cache[ck]
  if r.get('step_id'):soup=soup.find(id='step-'+str(r['step_id'])) or soup
  if attr=='tutorial/content':parts=[soup]
  elif attr=='answer/value':
   specific=soup.find(id=r.get('option_dom_id')) if r.get('option_dom_id') else None
   parts=[specific] if specific else [p for cls in ['questionWidget-choiceText','choiceText','selectListOption'] for p in soup.find_all(class_=cls)]
  else:
   classes=['exampleQuestion','questionWidget-text','questionText'] if attr=='question/problem' else ['exampleExplanation','questionExplanation','questionWidget-explanation']
   parts=[p for cls in classes for p in soup.find_all(class_=cls)]
   if not parts:parts=[soup]
  result.extend(parts)
 return result

def main():
 matched=set()
 for f in ['direct-matches.json','retained-arrays.json','ambiguous-layouts.json']:
  for r in json.loads((H/f).read_text()):
   for source in r.get('sources',[r.get('source')]):
    if source:matched.add((source['path'],source['identity'],source['attribute']))
 counts=collections.Counter()
 for file in ['archived-tables.json','capture-tables.json']:
  data=json.loads((H/file).read_text())
  for r in data:
   if (r['path'],r['identity'],r['attribute']) not in matched:continue
   options=set()
   for soup in get_doc(r):
    for t in soup.find_all('mtable'):
     if dict(t.attrs)==r['source_attributes'] and LegacyRenderer(None).m(t)==r['old_tex']:options.add(tuple(fences(t)))
   r.pop('source_fences',None);r.pop('fence_options',None)
   if len(options)==1:r['source_fences']=list(next(iter(options)));counts['resolved']+=1
   else:r['fence_options']=[list(v) for v in options];counts['ambiguous' if options else 'not_found']+=1
  (H/file).write_text(json.dumps(data,indent=2)+'\n')
 print('Identity-bound fence evidence',dict(counts))
if __name__=='__main__':main()
