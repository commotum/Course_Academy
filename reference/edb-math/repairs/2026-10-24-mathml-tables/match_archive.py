import json,re,collections
from pathlib import Path
H=Path(__file__).resolve().parent;W=H.parents[3]/'.local/edb/mathml-tables-work'
canon=lambda s:re.sub(r'\s+','',s)
sources=json.loads((H/'archived-tables.json').read_text());index=collections.defaultdict(list)
for r in sources:index[r['identity'],r['attribute'],canon(r['old_tex'])].append(r)
rows=json.loads((W/'inventory.json').read_text());matches=[];globalmatches=[]
allsig=collections.defaultdict(list)
for r in sources:allsig[canon(r['old_tex'])].append(r)
for r in rows:
 identity='tutorial:'+str(r['metadata']['tutorial/math-academy-id']) if 'tutorial/math-academy-id' in r['metadata'] else r['metadata'].get('question/math-academy-id')
 for s in r['spans']:
  found=index.get((identity,r['a'],canon(s['tex'])),[])
  if found:matches.append({'e':r['e'],'a':r['a'],'span':s,'source':found[0]})
  elif canon(s['tex']) in allsig:globalmatches.append({'e':r['e'],'a':r['a'],'span':s,'sources':[(f['identity'],f['attribute'],f['source_attributes']) for f in allsig[canon(s['tex'])]]})
(H/'archive-direct-matches.json').write_text(json.dumps(matches,indent=2)+'\n');(H/'archive-global-matches.json').write_text(json.dumps(globalmatches,indent=2)+'\n')
print('direct',len(matches),'fields',len({(r['e'],r['a']) for r in matches}),'additional exact signatures',len(globalmatches));print('direct identities',len({r['source']['identity'] for r in matches}),'attrs',collections.Counter(r['a'] for r in matches));print('row kinds',collections.Counter(r['source']['source_attributes'].get('columnalign','') for r in matches).most_common(10))
