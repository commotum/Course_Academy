import json,re
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/structural-math-2026-10-26';m=json.loads((W/'metadata.json').read_text());parents=json.loads((W/'parents.json').read_text());rows=json.loads((H/'table-candidates.json').read_text())+json.loads((H/'malformed-structure.json').read_text());want=set()
for d in rows:
 e=d['e'];meta=m.get(str(e),{})
 if d['a']=='answer/value':
  want|={m.get(str(q),{}).get('question/math-academy-id')for f,a in parents.get(str(e),[])if a=='answer-field/choices'for q,a in parents.get(str(f),[])if a=='question/answer-fields'}
 else:want.add(meta.get('question/math-academy-id'))
ps=[]
for line in(R/'.local/edb/mathml-tables-work/source-paths.txt').read_text().splitlines():
 p=Path(line);mt=re.search(r'(q-\d+)-(?:before|after)\.json$|history-(q-\d+)\.json$|example-(\d+)\.json$',p.name)
 if mt:
  ident=mt[1]or mt[2]or'e-'+mt[3]
  if ident in want:ps.append([line,ident])
(H/'additional-source-paths.json').write_text(json.dumps(ps,indent=2)+'\n');print('wanted identities',len(want),'capture identities',len({i for p,i in ps}),'capture files',len(ps))
