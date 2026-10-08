import sys,json,random
from pathlib import Path
sys.path.insert(0,str(Path('scripts/question_capture').resolve()))
from capture import arguments,locked
from browser import CaptureBrowser,repair_math_editor_document
from core import Pacer,atomic_json
from playwright.sync_api import sync_playwright
root=Path('reference/mathacademy/question-capture-workers/differential/14040950').resolve()
args=arguments(['run','--headless','--state-dir',str(Path('.local/question_capture-workers/differential').resolve())])
with locked(args.state_dir),sync_playwright() as pw:
 ctx=pw.chromium.launch_persistent_context(str(args.profile),headless=True,slow_mo=args.ui_delay_ms)
 ctx.route('https://mathacademy.com/**',repair_math_editor_document)
 page=ctx.pages[0]
 def keep_script(response):
  if response.url.split('?')[0].endswith(('/proof-question-widget.js','/select-list.js','/dynamic-select-question-widget.js','/student-lesson.js','/question-widget.js')):
   (root/'manual-recovery'/response.url.split('/')[-1].split('?')[0]).write_bytes(response.body())
 page.on('response',keep_script)
 b=CaptureBrowser(page,args,Pacer(args,random.Random()),None)
 b.navigate(json.loads((root/'state.json').read_text())['activity_url']);b.wait_activity_ready()
 scope=page.locator('#step-q334055');scope.wait_for(state='visible')
 item,shot=b.read(scope,root/'manual-recovery','server-next')
 info=scope.evaluate('''n=>({result:n.querySelector('.questionWidget-result')?.textContent,spinner:[...n.querySelectorAll('.questionWidget-spinner,.questionWidget-spinnerFrame')].map(e=>({html:e.outerHTML,rect:e.getBoundingClientRect().toJSON(),style:['display','visibility','opacity','width','height'].map(k=>[k,getComputedStyle(e)[k]])})),selects:[...n.querySelectorAll('.selectList')].map(e=>({id:e.id,html:e.outerHTML})),scripts:[...document.querySelectorAll('script[src]')].map(e=>e.src)})''')
 atomic_json(root/'manual-recovery/server-evidence-next.json',info)
 print(json.dumps({'step':b.current_step(),'result':item['result'],'fields':[(f['key'],f['dom_id']) for f in item['fields']],'errors':item['errors'],'scripts':info['scripts']}))
 ctx.close()
