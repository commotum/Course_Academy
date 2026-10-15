"""Render real player radio controls, full prompts and full fixed solutions.

Uses exact extracted learning.js presentation/control functions and the real
question-fields.js, marked/DOMPurify/MathJax dependencies, served read-only.
"""
import sys
sys.dont_write_bytecode=True
import functools,hashlib,http.server,json,re,subprocess,threading
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function short('):source.index('\n}',source.index('function short('))+2] if False else source[source.index('function short('):source.index('\n',source.index('function short('))],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function loadMath(')],source[source.index('function choiceOrder('):source.index('async function openPreview(')]]
js="""import { marked } from '/ui/vendor/marked/marked.esm.js';
import { romanLists } from '/ui/prose-lists.js';
import { inlinePrompt, checkboxControl, choiceIndicator, fieldFeedback, freeInput, blankInput, richSelect } from '/ui/question-fields.js';
const typeset=async node=>MathJax.typesetPromise([node]);
"""+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;
 const fields=q[':question/answer-fields'].map((f,i)=>({id:20+i,key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map((a,j)=>({id:100+i*10+j,type:a[':answer/type'],value:a[':answer/value']}))}));
 document.body.append(markdown(q[':question/problem'],'prose prompt',fields));
 const form=el('form','answers');for(const field of fields)form.append(fieldControl(field,false,q[':question/id'],q[':question/problem']));document.body.append(form);
 if(q[':question/worked-solution'])document.body.append(markdown(q[':question/worked-solution'],'prose solution'));
 await MathJax.typesetPromise([document.body]);
 const inputs=[...form.querySelectorAll('input[type=radio]')];
 const indicators=[...form.querySelectorAll('.answer-indicator')];
 if(indicators.some(n=>parseFloat(getComputedStyle(n).borderTopWidth)<1||getComputedStyle(n).borderTopColor==='rgba(0, 0, 0, 0)'))throw Error('radio indicator is not visibly styled');
 if(inputs.length!==5)throw Error('expected five actual radio controls');
 const selected=[];
 for(const input of inputs){input.click();const responses=collectResponses(form,fields);if(responses[0].choiceId!==Number(input.value)||form.querySelectorAll('input:checked').length!==1)throw Error('radio selection/response collection mismatch');selected.push(responses[0].choiceId);}
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 const unexpected=[...document.querySelectorAll('mjx-container')].filter(n=>n.getBoundingClientRect().width>1050);
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,radio_controls:inputs.length,radio_selection_round_trips:selected.length,full_solution:!!q[':question/worked-solution'],overflow:unexpected.length};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<!doctype html><html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:1000px;margin:24px auto;background:white;color:#222;padding:20px}.prose{margin-bottom:16px}fieldset{margin:12px 0 24px}.choices{max-width:100%}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
records=json.loads((D/'source-replays.json').read_text())+[r['record'] for r in json.loads((D/'review.json').read_text())]
for i,r in enumerate(records):r['generation']['render_label']=('source-' if i<12 else 'generated-')+str(i)+'-'+r['generation']['template']
(D/'render-records.json').write_text(json.dumps(records,ensure_ascii=False)+'\n')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
try:subprocess.run(['node',str(D/'render-cdp.js'),origin,str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
r=json.loads((D/'render-report.json').read_text());r['ui_source_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/learning.css',ROOT/'ui/navigation.css']};(D/'render-report.json').write_text(json.dumps(r,indent=2)+'\n')
