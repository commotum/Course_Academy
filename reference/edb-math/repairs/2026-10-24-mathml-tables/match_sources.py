import collections,json
from pathlib import Path
from layout import H,R,grid_key,expected_layout
W=R/'.local/edb/mathml-tables-work'
sources=json.loads((H/'archived-tables.json').read_text())+json.loads((H/'capture-tables.json').read_text())
index=collections.defaultdict(list)
for r in sources:
 if r['errors']:continue
 try:layout=expected_layout(r)
 except ValueError:continue
 if layout:index[r['identity'],r['attribute'],grid_key(r['rows'])].append(r)
rows=json.loads((W/'inventory-all.json').read_text());out=[];ambiguous=[];retained=[]
for r in rows:
 identity='tutorial:'+str(r['metadata']['tutorial/math-academy-id']) if 'tutorial/math-academy-id' in r['metadata'] else r['metadata'].get('question/math-academy-id')
 for s in r['spans']:
  found=index.get((identity,r['a'],grid_key(s['rows'])),[])
  if not found:continue
  # Different frames/rules for identical cells require individual review.
  layouts={expected_layout(f) for f in found}
  if len(layouts)!=1:ambiguous.append({'e':r['e'],'a':r['a'],'span':s,'sources':found});continue
  if s['env']=='array':
   # Candidate rule patterns are compared in preparation; retain exact layouts.
   retained.append({'e':r['e'],'a':r['a'],'span':s,'source':found[0]});continue
  out.append({'e':r['e'],'a':r['a'],'span':s,'source':found[0]})
(H/'direct-matches.json').write_text(json.dumps(out,indent=2)+'\n');(H/'retained-arrays.json').write_text(json.dumps(retained,indent=2)+'\n');(H/'ambiguous-layouts.json').write_text(json.dumps(ambiguous,indent=2)+'\n');print('Candidates',len(out),'fields',len({(r['e'],r['a']) for r in out}),'envs',collections.Counter(r['span']['env'] for r in out),'arrays',len(retained),'ambiguous',len(ambiguous),'sources',len(sources));print('Attributes',collections.Counter(r['a'] for r in out))
