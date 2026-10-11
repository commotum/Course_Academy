import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from scripts.browser.adapter import EXTRACT
from scripts.activity.capture import ActivityCapture
root=Path('/home/jake/Developer/Course_Academy/reference/mathacademy/capture')
checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True);context=browser.new_context();context.route('**/*',lambda route:route.abort());page=context.new_page()
 for account,task,mid in [('foundations','14116310','q-181457'),('linear','14114805','q-221691'),('linear','14114805','q-221707'),('linear','14114643','q-363823')]:
  cp=json.loads((root/account/task/'checkpoint.json').read_text());hist=next(h for h in cp['history']['questions'] if h['math_academy_id']==mid)
  live=next(r['question'] for r in cp['presentations'].values() if r['question'].get('math_academy_id')==mid or str(r['question'].get('dom_id','')).endswith(mid.removeprefix('q-')))
  page.set_content(hist['html']);item=page.locator('.question').evaluate(EXTRACT)
  checks.append({'account':account,'task_id':task,'id':mid,'current_history_problem':item['problem'],'live_problem':live['problem'],
    'current_history_field_count':len(item['fields']),'history_grade':hist.get('grade'),'current_history_fields_complete':item.get('answer_fields_complete'),
    'live_fields_complete':live.get('answer_fields_complete'),'binding_matches_with_current_extractor':ActivityCapture._source_binding_matches(live,item),
    'extraction_errors':item['errors']})
 context.close();browser.close()
Path('/tmp/capture-history-dom-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
for row in checks: print(row['id'],'matches',row['binding_matches_with_current_extractor'],'complete',row['current_history_fields_complete'],'fields',row['current_history_field_count'],'grade',row['history_grade'])
