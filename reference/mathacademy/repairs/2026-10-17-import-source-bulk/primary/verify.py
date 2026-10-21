"""Offline mechanical verification of exact source-bound primary proposals."""
from pathlib import Path
import collections,hashlib,json,re
HERE=Path(__file__).resolve().parent
changes=json.loads((HERE/'changes.json').read_text());bound=json.loads((HERE/'bound.json').read_text());decisions=json.loads((HERE/'decisions.json').read_text())
sha=lambda s:hashlib.sha256(s.encode()).hexdigest()
seen=set();repeated=[]
for c in changes:
 assert (c['entity'],c['attribute']) not in seen;seen.add((c['entity'],c['attribute']))
 assert sha(c['before'])==c['before_sha256'] and sha(c['after'])==c['after_sha256']
 parts=sorted(c['replacements'],key=lambda x:x['start'])
 assert all(a['end']<=b['start'] for a,b in zip(parts,parts[1:]))
 after=c['before']
 for p in reversed(parts):
  assert after[p['start']:p['end']]==p['before']
  assert sha(p['source_html'])==p['source_sha256']
  raw=Path(p['source_file']).read_text()
  assert raw[p['source_offset']:p['source_offset']+len(p['source_html'])]==p['source_html']
  assert sha(raw)==p['source_file_sha256']
  assert p['source_html_sha256_verified'] and not p['conversion']['errors']
  after=after[:p['start']]+p['after']+after[p['end']:]
 assert after==c['after']
 assert re.findall(r'\{\{[^{}]+\}\}',c['before'])==re.findall(r'\{\{[^{}]+\}\}',c['after'])
 # Distinct source locations can share old fragment value and need distinct restores.
 by_old=collections.defaultdict(list)
 for p in parts:by_old[p['before']].append(p)
 for old,ps in by_old.items():
  if len(ps)>1:repeated.append({'entity':c['entity'],'attribute':c['attribute'],'source_occurrences':[p['source_occurrence_id'] for p in ps],'positions':[[p['start'],p['end']] for p in ps],'different_restored_values':len({p['after'] for p in ps})})
assert len(decisions)==312 and len(bound)==312
result={'passed':True,'fields':len(changes),'source_bound_fields':len(bound),'replacements':sum(len(c['replacements']) for c in changes),'source_binding_modes':dict(collections.Counter(s['binding'] for r in bound for s in r['spans'])),'unchanged_bytes_outside_replacements':True,'source_offset_and_sha256_verified':True,'answer_control_tokens_preserved':True,'same_value_source_groups':len(repeated),'same_value_groups_with_different_recoveries':sum(x['different_restored_values']>1 for x in repeated),'decisions':dict(collections.Counter(x['status'] for x in decisions)),'changes_sha256':hashlib.sha256((HERE/'changes.json').read_bytes()).hexdigest()}
(HERE/'verification.json').write_text(json.dumps(result,indent=2)+'\n');(HERE/'repeated-fragment-proof.json').write_text(json.dumps(repeated,indent=2)+'\n');print(json.dumps(result,indent=2))
