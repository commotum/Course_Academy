from pathlib import Path
import json,hashlib
from playwright.sync_api import sync_playwright
from scripts.recovery import reextract_record
from scripts.browser.adapter import EXTRACT
R=Path(__file__).resolve().parent;D=R.parents[1]/'capture/multivariable/14111253';state=json.loads((D/'checkpoint.json').read_text());records=[]
for k in ['diagnostic-12','diagnostic-58']:records.append(('presentation',k,state['presentations'][k]['question']))
for q in state['history']['questions']:
 if q.get('math_academy_id') in ['q-343408','q-331821','q-37456']:records.append(('history',q['math_academy_id'],q))
out=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(headless=True);cx=b.new_context();cx.route('**/*',lambda rt:rt.abort());p=cx.new_page()
 for bucket,key,q in records:
  n=reextract_record(q,p,R/'quiz7-source-gap-extraction',history=bucket=='history');selector='[id='+json.dumps(q['dom_id'])+']'
  dom=p.locator(selector).evaluate('''e=>({proofSections:[...e.querySelectorAll('.proofSection')].map(n=>({id:n.id,style:n.getAttribute('style'),visible:!n.hidden&&getComputedStyle(n).display!=='none'&&getComputedStyle(n).visibility!=='hidden',parent:n.parentElement.id,parentStyle:n.parentElement.getAttribute('style')})),frames:[...e.querySelectorAll('.selectList')].map(n=>({id:n.id,frame:[...n.children].filter(x=>/selectListFrame/.test(x.className)).map(x=>({id:x.id,class:x.className})),choices:n.querySelectorAll('.selectListOption').length})),tables:[...e.querySelectorAll('table')].map(n=>({class:n.className,rows:n.querySelectorAll('tr').length,circles:n.querySelectorAll('.choiceLetterCircle').length})),historyResult:e.querySelector('.answerResult')?.textContent,questionHeader:e.querySelector('.questionHeader')?.textContent})''')
  out.append({'bucket':bucket,'key':key,'source_sha256':hashlib.sha256(Path(q['html_path']).read_bytes()).hexdigest(),'source_html':q['html_path'],'grade':q.get('grade'),'result':q.get('result'),'problem':n.get('problem'),'answer_fields_complete':n.get('answer_fields_complete'),'fields':n.get('answer_fields',n.get('fields')),'errors':n.get('errors'),'dom':dom})
 b.close()
(R/'quiz7-source-gap-current-extraction.json').write_text(json.dumps({'extractor_sha256':hashlib.sha256(EXTRACT.encode()).hexdigest(),'records':out},indent=2)+'\n')
print([{k:v for k,v in x.items() if k not in ('problem','fields')} for x in out])
