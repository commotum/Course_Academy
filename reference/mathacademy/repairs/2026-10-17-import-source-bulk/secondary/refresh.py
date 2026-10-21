"""Rematerialize already-proven source spans after converter fixes.

No source-position rebinding and no live reads/writes. Every original bound
span and before field remains identical; only source conversion is refreshed.
"""
from pathlib import Path
import hashlib,json
import prepare as p
HERE=Path(__file__).resolve().parent
changes=json.loads((HERE/'changes.json').read_text())
for row in changes:
 for span in row['replacements']:
  result=p.conv.convert_source(p.pm.sources[span['source_occurrence_id']])
  assert not result['errors'],(span['source_occurrence_id'],result['errors'])
  assert result['source_sha256']==span['source_sha256']
  span['after']=p.wrap(result['tex'],span['before'],row['answer_type'])
  span['features']=result['features']
 after=row['before']
 for span in reversed(sorted(row['replacements'],key=lambda x:x['start'])):
  assert after[span['start']:span['end']]==span['before']
  after=after[:span['start']]+span['after']+after[span['end']:]
 row['after']=after;row['after_sha256']=p.digest(after)
(HERE/'changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
(HERE/'changes.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in changes))
bykey={(r['entity'],r['attribute']):r for r in changes}
decisions=json.loads((HERE/'decisions.json').read_text())
for d in decisions:
 c=bykey.get((d['entity'],d['attribute']))
 if c:d['after_sha256']=c['after_sha256']
(HERE/'decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n')
(HERE/'decisions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in decisions))
manifest={'changes':len(changes),'replacements':sum(len(r['replacements']) for r in changes),'files':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('convert_source.py','prepare.py','refresh.py','changes.json','decisions.json')}}
(HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest,indent=2))
