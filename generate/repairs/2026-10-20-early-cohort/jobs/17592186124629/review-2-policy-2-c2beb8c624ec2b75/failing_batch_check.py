"""Strict delivered-batch acceptance test; intentionally fails on reviewed package.
Run: <job-python> -B failing_batch_check.py [path/to/entrypoint.py]
Regenerate rather than edit stored keys. Applicable rule: repeated observable
checkbox concept triplets in this finite batch must offer varying true subsets.
"""
import importlib.util,json,sys
from pathlib import Path
from collections import defaultdict
sys.dont_write_bytecode=True
entry=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent.parent/'workspace/17592186124629.py'
sys.path.insert(0,str(entry.parent));spec=importlib.util.spec_from_file_location('reviewed',entry);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rows=g.batch(difficulty='moderate',count=5,seed=2086806769)
groups=defaultdict(list)
for r in rows:
 fs=r['question'][':question/answer-fields']
 if len(fs)!=3 or any(f[':answer-field/type']!=':answer-field.type/checkbox' for f in fs):continue
 if not all(cue in fs[i][':answer-field/key'] for i,cue in enumerate(['det','Col','pivot'])):continue
 mask=tuple(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='true' for f in fs)
 groups['det,col,pivot'].append(mask)
print(json.dumps({'seed':2086806769,'observed':groups}))
for name,masks in groups.items():
 if len(masks)>=2:
  assert len(set(masks))>1, f'{name}: all {len(masks)} surviving questions share {masks[0]}; select-column-space-only bypasses the premise'
