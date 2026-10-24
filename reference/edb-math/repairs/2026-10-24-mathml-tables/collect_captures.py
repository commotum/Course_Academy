"""Index ruled tables in retained captures, bound to observed source identities."""
import json,re,collections
from pathlib import Path
from source_tables import tables,H,R
W=R/'.local/edb/mathml-tables-work'
meta=json.loads((W/'metadata.json').read_text());wanted={v.get('question/math-academy-id') for v in meta.values() if 'question/math-academy-id' in v};wanted_t={v.get('tutorial/math-academy-id') for v in meta.values() if 'tutorial/math-academy-id' in v}
paths=[Path(s) for s in (W/'source-paths.txt').read_text().splitlines()];out=[];counts=collections.Counter();bad=[]
rule=re.compile(r'(?:columnlines|rowlines|frame)=["\'][^"\']*(?:solid|dashed)')
def add_raw(d,identity,path):
 if not isinstance(d,dict):return
 html=d.get('html') or d.get('raw_html')
 if not isinstance(html,str) or '<mtable' not in html or not rule.search(html):return
 from bs4 import BeautifulSoup
 soup=BeautifulSoup(html,'html.parser')
 canonical=identity.startswith('e-')
 pairs=[('exampleQuestion' if canonical else 'questionWidget-text','question/problem'),('exampleExplanation' if canonical else 'questionExplanation','question/worked-solution'),('questionWidget-explanation','question/worked-solution')]
 # Saved history roots are themselves the questionExplanation wrapper.
 seen=set()
 for cls,attr in pairs:
  for n in soup.find_all(class_=cls):
   if id(n) in seen:continue
   seen.add(id(n));out.extend(tables(str(n),identity,attr,path))
 # The standard before/history snapshots sometimes use the older questionText.
 for cls,attr in [('questionText','question/problem')]:
  for n in soup.find_all(class_=cls):
   if id(n) not in seen:out.extend(tables(str(n),identity,attr,path));seen.add(id(n))
for i,path in enumerate(paths):
 name=path.name
 match=re.fullmatch(r'(q-\d+)-(?:before|after)\.json',name) or re.fullmatch(r'history-(q-\d+)\.json',name)
 example=re.fullmatch(r'example-(\d+)\.json',name);tutorial=re.fullmatch(r'tutorial-(\d+)\.html',name)
 if match and match[1] not in wanted:continue
 if example and 'e-'+example[1] not in wanted:continue
 if tutorial and int(tutorial[1]) not in wanted_t:continue
 if name!='state.json' and not (match or example or tutorial):continue
 raw=path.read_text();counts['files_read']+=1
 if 'mtable' not in raw or not any(k in raw for k in ['columnlines','rowlines','frame']):continue
 try:
  if tutorial:out.extend(tables(raw,'tutorial:'+tutorial[1],'tutorial/content',path));continue
  d=json.loads(raw)
  if match:add_raw(d,match[1],path)
  elif example:add_raw(d,'e-'+example[1],path)
  else:
   for identity,r in d.get('questions',{}).items():
    if identity not in wanted or not isinstance(r,dict):continue
    for key in ['before','history','after']:add_raw(r.get(key),identity,path)
 except (ValueError,TypeError,KeyError) as e:bad.append({'path':str(path),'error':str(e)})
 if i%2000==0:print('Scanned',i,'/',len(paths),'tables',len(out),flush=True)
# Historical completed-activity exports preserve original problem/solution DOM.
p=R/'reference/mathacademy/progress-history-2026-10-04/observations.json'
d=json.loads(p.read_text())
for task in d['tasks']:
 for q in task['questions']:
  identity=q['id'].replace('question-','q-')
  if identity not in wanted:continue
  for key,attr in [('problem_html','question/problem'),('worked_solution_html','question/worked-solution')]:
   html=q.get(key,'')
   if html:out.extend(tables(html,identity,attr,p,task=task.get('task_id',task.get('id'))))
# Dedupe exact source evidence without merging different source layouts.
unique={}
for r in out:unique[r['identity'],r['attribute'],r['old_tex'],json.dumps(r['source_attributes'],sort_keys=True)]=r
out=list(unique.values());(H/'capture-tables.json').write_text(json.dumps(out,indent=2)+'\n');report={'source_paths':len(paths),'files_read':counts['files_read'],'ruled_source_tables':len(out),'identities':len({r['identity'] for r in out}),'errors':bad};(H/'capture-summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='errors'},indent=2));print('errors',len(bad))
