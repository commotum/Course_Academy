import json,hashlib
from pathlib import Path
from scripts.legacy_recovery import current_supported_reviews,source_record
from scripts.database.evidence import authoritative_question
root=Path('reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/legacy-provenance')
reviewed=current_supported_reviews(root);sha=lambda x:hashlib.sha256(x).hexdigest();report=[]
for relative in ['aggregate-structural-repairs/cf270523533919134351','aggregate-controls-repairs/df8d8f660a59c278f124']:
 directory=root/relative;content=json.loads((directory/'content.json').read_text());evidence=json.loads((directory/'source-evidence.json').read_text());issues=[]
 actual_sha=sha(json.dumps(content,sort_keys=True,ensure_ascii=False).encode())
 if actual_sha!=evidence['content_sha256']:issues.append('content SHA mismatch')
 for q in content['questions']:
  mid=q['math_academy_id'];binding=next(b for b in evidence['bindings'] if b['id']==mid)
  if q!=authoritative_question(reviewed[mid]['question']):issues.append(mid+' authoritative reviewed content mismatch')
  if reviewed[mid]['source_hash']!=binding['source_hash']:issues.append(mid+' review source generation mismatch')
  fresh=source_record(Path(binding['directory']),mid)
  if sha(json.dumps(fresh,sort_keys=True,ensure_ascii=False).encode())!=binding['source_hash']:issues.append(mid+' original bound source mismatch')
  if sha(Path(binding['state_file']).read_bytes())!=binding['state_sha256']:issues.append(mid+' immutable owning state mismatch')
 report.append({'directory':str(directory),'scope':evidence['scope'],'questions':len(content['questions']),'content_sha_matches':actual_sha==evidence['content_sha256'],'issues':issues})
print(json.dumps(report,indent=2));Path('/tmp/legacy-final-335-aggregates-independent-qc.json').write_text(json.dumps(report,indent=2))
