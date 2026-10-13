import json,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
R=Path('reference/mathacademy/capture-audits/2026-10-11-completeness-repairs/legacy-provenance');inv=json.load(open('reference/mathacademy/capture-audits/2026-10-11-backlog-repairs/identity-omission-qc/boxed-phantom/boxed-phantom-independent-inventory.json'));old=Path('/tmp/extract-before-decorated-phantom.js').read_text();new=Path('/tmp/extract-decorated-phantom-7ec1335d.js').read_text();results=[];seen=set();fixtures=[]
from bs4 import BeautifulSoup
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True);context=browser.new_context();context.route('**/*',lambda r:r.abort());page=context.new_page()
 for mid in inv['decorated_question_ids']:
  entries=[x for x in inv['findings'] if x['id']==mid and x['kind']=='decorated'];x=entries[0];state=json.loads((Path(x['directory'])/'state.json').read_text());record=state['questions'][mid][x['original_record']];markup=record['html'];page.set_content(markup);root=page.locator('[id='+json.dumps(record['dom_id'])+']').first;a=root.evaluate(old);b=root.evaluate(new);results.append({'id':mid,'record':x['original_record'],'part':x['part'],'changed':a!=b,'old_errors':a.get('errors'),'new_errors':b.get('errors'),'new_problem':b.get('problem'),'new_solution':b.get('worked_solution'),'fields_equal':a.get('fields')==b.get('fields')});
  soup=BeautifulSoup(markup,'html.parser');maths=[]
  for e in soup.select('math'):
   if e.select('mphantom') and (e.select('menclose') or e.select('[mathbackground]') or e.select('[style]')):maths.append(str(e))
  fixtures.append({'id':mid,'part':x['part'],'original_record':x['original_record'],'source_file':str(Path(x['directory'])/'state.json'),'source_html_sha256':x['original_html_sha256'],'mathml':maths})
 for pack in ['aggregate-structural-repairs/cf270523533919134351','aggregate-controls-repairs/df8d8f660a59c278f124']:
  evidence=json.loads((R/pack/'source-evidence.json').read_text())
  for bind in evidence['bindings']:
   state=json.loads(Path(bind['state_file']).read_text());record=state['questions'][bind['id']]
   for name in ['before','history','after']:
    rec=record.get(name,{})
    if not rec.get('html') or not rec.get('dom_id'):continue
    key=(bind['id'],hashlib.sha256(rec['html'].encode()).hexdigest(),rec['dom_id'])
    if key in seen:continue
    seen.add(key);page.set_content(rec['html']);root=page.locator('[id='+json.dumps(rec['dom_id'])+']').first
    if root.count()!=1:raise AssertionError(('missingroot',key))
    a=root.evaluate(old);b=root.evaluate(new)
    if a!=b:results.append({'aggregate_changed':bind['id'],'name':name,'keys':[k for k in a.keys()|b.keys() if a.get(k)!=b.get(k)]})
 context.close();browser.close()
report={'candidate_sha256':hashlib.sha256(new.encode()).hexdigest(),'decorated_questions':results[:16],'aggregate_original_roots_compared':len(seen),'aggregate_changed':results[16:]};Path('/tmp/decorated-candidate-7ec1335d-proof.json').write_text(json.dumps(report,indent=2));Path('/tmp/decorated-phantom-fixtures.json').write_text(json.dumps(fixtures,indent=2));print(json.dumps({'decorated_questions':[{k:v for k,v in r.items() if k not in ('new_problem','new_solution')} for r in results[:16]],'aggregate_original_roots_compared':len(seen),'aggregate_changed':results[16:]},indent=2))
