import json,hashlib,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=Path('/home/jake/Developer/Course_Academy')
paths=[ROOT/p for p in (HERE/'extra-source-paths.txt').read_text().splitlines()if p.endswith('.json')]
for out in sorted(HERE.glob('175*')):
 manifest=json.loads((out/'source-manifest.json').read_text())
 for row in manifest:
  if row['prompt_sources']and row['solution_sources']:continue
  mid=row['mid']
  for p in paths:
   if mid not in p.name:continue
   try:c=json.loads(p.read_text());html=c.get('html','')
   except Exception:continue
   if not html:continue
   role='solution_sources'if 'solution'in p.name or 'questionExplanation-'in html else'prompt_sources'
   row[role].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'html':html,'role':'saved original DOM'})
 (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2))
 print(out.name,'missing prompt',[r['mid']for r in manifest if not r['prompt_sources']],'missing solution',[r['mid']for r in manifest if not r['solution_sources']],flush=True)
