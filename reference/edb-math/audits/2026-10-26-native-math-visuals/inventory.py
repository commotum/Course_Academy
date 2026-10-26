import collections,json,re,sys
from pathlib import Path
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/native-math-visual-audit-2026-10-26';sys.path.insert(0,str(R/'scripts'))
from audit_math_image_imports import IMAGE,PARENTS,META
facts=[];meta=collections.defaultdict(dict);parents=collections.defaultdict(set);uses=collections.defaultdict(list)
for line in (W/'current.jsonl').open():
 d=json.loads(line);e,a,v=d['e'],d['a'],d['v']
 if a in META:meta[e][a]=v
 if a in PARENTS:parents[v].add(e)
 if isinstance(v,str)and IMAGE.search(v):facts.append(d)
old=json.loads((R/'reference/edb-math/audits/2026-10-22-math-images/assets.json').read_text());sources=json.loads((R/'reference/edb-math/images/math-academy-map.json').read_text())['by_source_path'];reverse=collections.defaultdict(list)
for p,a in sources.items():reverse[a].append(p)
def context(e):
 seen=set();todo=[e]
 while todo:
  n=todo.pop()
  if n in seen:continue
  seen.add(n);todo.extend(parents[n])
  if 'activity/scope'in meta[n]:todo.append(meta[n]['activity/scope'])
 return [{'entity':n,**meta[n]}for n in sorted(seen)if meta[n]]
for d in facts:
 c=context(d['e']);topics=[x for x in c if 'topic/title'in x];titles='; '.join(x['topic/title']for x in topics)
 for m in IMAGE.finditer(d['v']):
  uses[m[0]].append({'entity':d['e'],'attribute':d['a'],'span':[m.start(),m.end()],'context':c,'topic_titles':titles,'nearby':d['v'][max(0,m.start()-400):m.end()+220]})
assets=[]
for path,locations in uses.items():
 info=old.get(path,{});kind=info.get('kind','new-unclassified');p=Path('/media/jake/SSD/EDB/math')/path;size=None
 if not path.endswith('.svg'):
  try:
   with Image.open(p)as im:size=list(im.size)
  except OSError:pass
 assets.append({'path':path,'kind':kind,'size':size,'source_paths':reverse[path],'uses':locations})
(W/'image-facts.json').write_text(json.dumps(facts));(W/'assets.json').write_text(json.dumps(assets));(H/'inventory-summary.json').write_text(json.dumps({'basis':json.loads((W/'current.manifest.json').read_text())['basis_t'],'image_fields':len(facts),'unique_assets':len(assets),'kinds':dict(collections.Counter(a['kind']for a in assets))},indent=2)+'\n')
print((H/'inventory-summary.json').read_text());target=re.compile(r'matri|determinant|dot product|cross product|synthetic division|long division|chain rule|product rule|quotient rule|compos|factor.*polynomial|exponent',re.I);selected=[a for a in assets if any(target.search(u['topic_titles'])for u in a['uses'])and a['size']and a['kind']not in ['generated-graphic']];(W/'priority.json').write_text(json.dumps(selected));print('priority assets',len(selected));print(collections.Counter(u['topic_titles']for a in selected for u in a['uses']).most_common(35))
