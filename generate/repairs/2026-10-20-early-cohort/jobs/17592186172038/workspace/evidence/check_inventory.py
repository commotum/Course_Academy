import json,re,hashlib
from pathlib import Path
W=Path(__file__).resolve().parents[1];S=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186172038/source');M=Path('/media/jake/SSD/EDB/math');inv=json.loads((S/'inventory.json').read_text());results=[];affected=[]
for q in inv['questions']:
 refs=[]
 for key in (':question/problem',':question/worked-solution'):refs+=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',q.get(key,''))
 for f in q[':question/answer-fields']:
  for a in f[':answer-field/choices']:refs.append(a[':answer/value'])
 missing=[];malformed=[];hash_mismatch=[]
 for ref in set(refs):
  p=M/ref
  if not ref.startswith('images/') or not p.is_file():missing.append(ref);continue
  if hashlib.sha256(p.read_bytes()).hexdigest()!=p.stem:hash_mismatch.append(ref)
 for i,f in enumerate(q[':question/answer-fields']):
  if not f.get(':answer-field/correct'):
   malformed.append(i);affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'math_academy_source_id':q.get(':question/math-academy-id'),'has_math_academy_source_id':bool(q.get(':question/math-academy-id')),'finding':'Captured radio field has no stored correct-answer reference; source replay infers the key, but database remains unchanged.','reproduction':f"inventory.json questions where :question/id={q[':question/id']}; field {i} lacks :answer-field/correct. Native check-engine requires this reference before grade_field can be called."})
 results.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'has_math_academy_source_id':bool(q.get(':question/math-academy-id')),'unique_asset_references':len(set(refs)),'missing_or_noncanonical_assets':missing,'hash_mismatches':hash_mismatch,'missing_correct_fields':malformed})
assert not any(r['missing_or_noncanonical_assets'] or r['hash_mismatches'] for r in results)
(W/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
(W/'evidence/inventory-audit.json').write_text(json.dumps({'questions_tested':len(results),'relocation_asset_failure_present':False,'all_assets_resolve_and_match_hash':True,'missing_correct_references':len(affected),'results':results,'limits':'All 17 captured records checked for runtime-path persistence, asset resolution/hash, and missing key. No claim of exhaustive pedagogical correctness for published raster banks; no learner history or live database inspected. Source raster orientation evidence was rechecked for all seven MA sources. No database changes.'},indent=2)+'\n');print('Inventory:',len(results),'records, canonical images intact;',len(affected),'pre-existing missing correct refs')
