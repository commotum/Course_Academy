import collections,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from source_tables import tables,H,R,LegacyRenderer
from enrich_sources import fences
W=R/'.local/edb/mathml-tables-work';wanted=set(json.loads((W/'choice-source-question-ids.json').read_text()));paths=[Path(s) for s in (W/'source-paths.txt').read_text().splitlines()]
selected=[];parents=set()
for p in paths:
 m=re.fullmatch(r'(q-\d+)-(?:before|after)\.json',p.name) or re.fullmatch(r'history-(q-\d+)\.json',p.name)
 if m and m[1] in wanted:selected.append((p,m[1]));parents.add(p.parent)
for p in paths:
 if p.name=='state.json' and p.parent in parents:selected.append((p,None))
out=[]
def process(html,identity,path):
 if not html or '<mtable' not in html or not any(k in html for k in ['rowlines','columnlines','frame']):return
 soup=BeautifulSoup(html,'html.parser');seen=set()
 for cls in ['questionWidget-choiceText','choiceText','selectListOption']:
  for n in soup.find_all(class_=cls):
   if id(n) in seen:continue
   seen.add(id(n));records=tables(str(n),identity,'answer/value',path,option_dom_id=n.get('id'))
   original=[t for t in n.find_all('mtable') if any(v not in ['none',''] for k in ['frame','rowlines','columnlines'] for v in t.get(k,'none').split())]
   for r,t in zip(records,original):r['source_fences']=fences(t);out.append(r)
for i,(p,identity) in enumerate(selected):
 raw=p.read_text()
 if 'mtable' not in raw or not any(k in raw for k in ['rowlines','columnlines','frame']):continue
 d=json.loads(raw)
 if identity:process(d.get('html') or d.get('raw_html'),identity,p)
 else:
  for mid,record in d.get('questions',{}).items():
   if mid not in wanted:continue
   for k in ['before','history','after']:
    if isinstance(record.get(k),dict):process(record[k].get('html') or record[k].get('raw_html'),mid,p)
 if i%2000==0:print('Choice source paths',i,'/',len(selected),'tables',len(out),flush=True)
unique={}
for r in out:unique[r['identity'],r['old_tex'],json.dumps(r['source_attributes'],sort_keys=True),tuple(r['source_fences'])]=r
out=list(unique.values());(H/'choice-tables.json').write_text(json.dumps(out,indent=2)+'\n');print('Choice source paths',len(selected),'ruled tables',len(out),'identities',len({r['identity'] for r in out}))
