"""Read-only finite source inventory; compare only the approved brace serializer delta."""
from pathlib import Path
import json,hashlib,re
from playwright.sync_api import sync_playwright
from scripts.browser.adapter import EXTRACT
R=Path(__file__).resolve().parent
old=EXTRACT.replace("literalFence(n.textContent)","n.textContent").replace("literalFence(n.getAttribute('open') || '(')","(n.getAttribute('open') || '(')").replace("literalFence(n.getAttribute('close') || ')')","(n.getAttribute('close') || ')')").replace("[')',']','}','\\\\}']","[')',']','}']")
assert old!=EXTRACT
items=[]
candidates=json.loads((R/'later-source-candidates.json').read_text())+[{'account':'multivariable','directory':str(R.parents[1]/'capture/multivariable/14120884/repairs/source-candidates-v1')}]+json.loads((R/'later-finite-additional-candidates.json').read_text())
for row in candidates:
 d=Path(row['directory']).parents[1];c=json.loads((d/'content.json').read_text())
 for bucket in ['questions','canonical_examples']:
  for q in c.get(bucket,[]):items.append(('archive39',str(d),bucket,q))
 checkpoint=json.loads((d/'checkpoint.json').read_text())
 for presentation in checkpoint.get('presentations',{}).values():
  if presentation.get('question'):items.append(('archive39',str(d),'presentations',presentation['question']))
 for bucket in ['questions','canonical_examples']:
  for q in checkpoint.get('history',{}).get(bucket,[]):items.append(('archive39',str(d),bucket,q))
 for step in checkpoint.get('steps',[]):
  if step.get('question'):items.append(('archive39',str(d),'steps',step['question']))
for path in (R/'legacy-provenance').glob('batch-*/source-records.json'):
 for entry in json.loads(path.read_text()):items.append(('legacy',entry['directory'],'questions',entry['question']))
# q80447 independently proven source case outside original39.
d=R.parents[1]/'capture/differential/14117715';c=json.loads((d/'content.json').read_text())
for q in c['questions']:
 if q.get('math_academy_id')=='q-80447':items.append(('frozen318',str(d),'questions',q))
pattern=re.compile(r'<mo\b[^>]*>\s*[{}]\s*</mo>|<mfenced\b[^>]*(?:open|close)=["\'][{}]["\']',re.I)
out=[];seen=set();counts={}
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True);context=browser.new_context();context.route('**/*',lambda route:route.abort());page=context.new_page()
 for scope,d,bucket,q in items:
  counts[scope]=counts.get(scope,0)+1
  markup=q.get('html')
  if not markup and q.get('html_path') and Path(q['html_path']).is_file():markup=Path(q['html_path']).read_text()
  if not markup or not pattern.search(markup):continue
  sha=hashlib.sha256(markup.encode()).hexdigest();identity=(scope,d,q.get('math_academy_id'),sha)
  if identity in seen:continue
  seen.add(identity);row={'scope':scope,'directory':d,'id':q.get('math_academy_id'),'bucket':bucket,'source_html':q.get('html_path'),'source_sha256':sha}
  try:
   page.set_content(markup);node=page.locator('[id='+json.dumps(q['dom_id'])+']') if q.get('dom_id') else page.locator('body')
   before=node.evaluate(old,{'history_grade':q.get('grade') or q.get('result')} if bucket=='questions' else {});after=node.evaluate(EXTRACT,{'history_grade':q.get('grade') or q.get('result')} if bucket=='questions' else {})
   keys=['problem','worked_solution','fields','errors','answer_fields_complete'];changed=[k for k in keys if before.get(k)!=after.get(k)]
   row.update(changed_keys=changed,changed=bool(changed))
   if changed:row.update(before={k:before.get(k) for k in changed},after={k:after.get(k) for k in changed})
  except Exception as e:row.update(error=str(e))
  out.append(row)
 browser.close()
result={'extractor_sha256':hashlib.sha256(EXTRACT.encode()).hexdigest(),'isolated_delta_baseline_sha256':hashlib.sha256(old.encode()).hexdigest(),'records_scanned':counts,'candidates':len(out),'records':out,'network':'all requests aborted; no shared packages mutated'}
(R/'literal-brace-source-change-inventory.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'scanned':counts,'candidates':len(out),'actual_changed':[ {k:v for k,v in r.items() if k not in ('before','after')} for r in out if r.get('changed')],'errors':[r for r in out if r.get('error')]}))
