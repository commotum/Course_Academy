import json,re
from pathlib import Path
base=Path('reference/edb-math/repairs/2026-11-08-quiz3-quality/characteristic')
for d in base.glob('175*'):
 rows=json.loads((d/'source-manifest.json').read_text())
 for r in rows:
  r['sources']=[s for s in r['sources']if s['kind']=='original lesson HTML' or re.search(re.escape(r['mid'])+r'(?![0-9])',Path(s['path']).name) or (r['mid'].startswith('e-')and Path(s['path']).name=='example-'+r['mid'][2:]+'.json')]
 (d/'source-manifest.json').write_text(json.dumps(rows,indent=2));print(d.name,'missing',[r['mid']for r in rows if not r['sources']])
