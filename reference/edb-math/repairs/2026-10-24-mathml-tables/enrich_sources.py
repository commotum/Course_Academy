"""Recover explicit matrix fences from each table's original containing DOM."""
import json,re,collections
from pathlib import Path
from bs4 import BeautifulSoup
from source_tables import H,R,LegacyRenderer
MATCHED={'[]':['[',']'],'()':['(',')'],'{}':[r'\{',r'\}'],'||':['|','|'],'‖‖':[r'\Vert',r'\Vert']}
def fences(t):
 node=t
 for _ in range(8):
  p=node.parent
  if p is None:return []
  if p.name=='mfenced':
   a=p.get('open','(');b=p.get('close',')');return MATCHED.get(a+b,[])
  if p.name in ['math','mrow','mstyle','mpadded','semantics','mtd']:
   tags=[n for n in p.children if getattr(n,'name',None) and n.name not in ['annotation','annotation-xml']]
   if node in tags:
    i=tags.index(node)
    if i>0 and i+1<len(tags) and tags[i-1].name=='mo' and tags[i+1].name=='mo':
     pair=tags[i-1].get_text().strip()+tags[i+1].get_text().strip()
     if pair in MATCHED:return MATCHED[pair]
    if len(tags)>1:return []
   node=p
  elif p.name=='title':
   items=list(p.children);i=items.index(node);before=''.join(str(x) for x in items[:i]).strip();after=''.join(str(x) for x in items[i+1:]).strip()
   for a,b in [('\\left[','\\right]'),('\\left(','\\right)'),('\\left|','\\right|')]:
    if before.endswith(a) and after.startswith(b):return MATCHED[a[-1]+b[-1]]
   return []
  else:return []
 return []
def htmls(value):
 if isinstance(value,dict):
  for k,v in value.items():
   if k in ['html','raw_html','problem_html','worked_solution_html'] and isinstance(v,str) and '<mtable' in v:yield v
   elif isinstance(v,(dict,list)):yield from htmls(v)
 elif isinstance(value,list):
  for v in value:yield from htmls(v)

def main():
 paths=collections.defaultdict(list)
 for file in ['archived-tables.json','capture-tables.json']:
  data=json.loads((H/file).read_text())
  for r in data:paths[r['path']].append(r)
 needed=collections.defaultdict(set)
 for file in ['direct-matches.json','retained-arrays.json','ambiguous-layouts.json']:
  for r in json.loads((H/file).read_text()):
   for s in r.get('sources',[r.get('source')]):
    if s:needed[s['path']].add(s['old_tex'])
 proof={};counts=collections.Counter()
 for name,sigs in needed.items():
  p=Path(name);p=p if p.is_absolute() else R/p;raw=p.read_text();docs=[raw] if p.suffix=='.html' else list(htmls(json.loads(raw)))
  found=collections.defaultdict(set)
  for markup in docs:
   if not any(x in markup for x in ['columnlines','rowlines','frame']):continue
   soup=BeautifulSoup(markup,'html.parser')
   for t in soup.find_all('mtable'):
    if not any(v not in ['none',''] for key in ['columnlines','rowlines','frame'] for v in t.get(key,'none').split()):continue
    tex=LegacyRenderer(None).m(t)
    if tex in sigs:found[tex].add(tuple(fences(t)))
  for s in paths[name]:
   if s['old_tex'] in found:
    options=found[s['old_tex']]
    if len(options)==1:s['source_fences']=list(next(iter(options)));counts['resolved']+=1
    else:s['fence_options']=[list(v) for v in options];counts['ambiguous']+=1
 for file in ['archived-tables.json','capture-tables.json']:
  source_paths={r['path'] for r in json.loads((H/file).read_text())};data=[r for p in source_paths for r in paths[p] if (file=='archived-tables.json')==('topic' in r)]
  # Archives are marked with topic/step metadata; captures are not.
  (H/file).write_text(json.dumps(data,indent=2)+'\n')
 print('Fence evidence',dict(counts),'source paths',len(needed))
if __name__=='__main__':main()
