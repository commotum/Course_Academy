"""Render actual draft records with frozen player controls and full solutions."""
import sys
sys.dont_write_bytecode=True
import functools,http.server,json,threading,hashlib,subprocess,shutil
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2];UI=D/'reference/ui';UI.parent.mkdir(exist_ok=True);shutil.copytree(ROOT/'ui',UI,dirs_exist_ok=True)
source=(UI/'learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function short('):source.index('function appendStepHeading(')],source[source.index('function fieldLabel('):source.index('function announce(')],source[source.index('function escapeHTML('):source.index('function loadMath(')],source[source.index('function choiceOrder('):source.index('function collectResponses(')]]
js="""import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
import {checkboxControl,freeInput,choiceIndicator,fieldFeedback,blankInput,richSelect,inlinePrompt,mountInlineFields,loadMathInputs} from './reference/ui/question-fields.js';
const typeset=()=>{};
"""+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;await loadMathInputs();MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],answerType:':answer.type/math',choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);const list=el('div','field-list');document.body.append(list);
 mountInlineFields(prompt,list,fields,f=>fieldControl(f,false,q[':question/id'],q[':question/problem']));
 document.body.append(markdown(q[':question/worked-solution'],'prose worked-solution'));
 await MathJax.typesetPromise([document.body]);await new Promise(r=>setTimeout(r,40));
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
 const inputs=[...document.querySelectorAll('input,math-field')];const f=fields[0];
 if(f.type.endsWith('/radio')){const target=inputs.find(n=>n.value===q[':question/answer-fields'][0][':answer-field/correct'][1]);target.click();if(!target.checked)throw Error('radio not selectable');}
 else {const target=inputs[0];target.value=f.choices[0].value;target.dispatchEvent(new Event('input',{bubbles:true}));if(!target.value)throw Error('blank not editable');}
 const math=[...document.querySelectorAll('mjx-container')];
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),blanks:prompt.querySelectorAll('[data-field-key]').length,controls:inputs.length,control_kind:inputs[0].tagName,interactive:true,rendered_math:math.length,solution_math:document.querySelector('.worked-solution').querySelectorAll('mjx-container').length,overflow:math.some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="reference/ui/learning.css"><link rel="stylesheet" href="reference/ui/navigation.css"><style>body{max-width:1000px;margin:32px auto;background:white;color:#222;padding:20px}.prose{margin-bottom:14px}</style><script src="reference/ui/vendor/dompurify/purify.min.js"></script><script src="reference/ui/mathjax-config.js"></script><script src="reference/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body class="lesson-main"></body></html>')
review=json.loads((D/'review.json').read_text());records=[]
boundary=[x['record'] for x in json.loads((D/'boundary-engine-input.json').read_text())]
for index,r in enumerate(review['generated_variants']+boundary):
 r['generation']['render_label']=r['question'][':question/difficulty'].split('/')[-1]+'-'+r['generation']['template']+'-'+r['generation']['parameters'].get('trig','source')+'-'+r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1]+('-boundary' if index>=len(review['generated_variants']) else '');records.append(r)
(D/'render-records.json').write_text(json.dumps(records)+'\n')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
try:subprocess.run(['node',str(D/'render-cdp.js'),origin,str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(UI.rglob('*')) if x.is_file()};report['normal_content_only']=True;report['generator_sha256']=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest();report['render_records_sha256']=hashlib.sha256((D/'render-records.json').read_bytes()).hexdigest();report['rendered_math']=sum(x['rendered_math'] for x in report['checks']);report['full_solution_math']=sum(x['solution_math'] for x in report['checks']);report['browser_version']=subprocess.check_output(['/home/jake/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell','--version'],text=True).strip();(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
