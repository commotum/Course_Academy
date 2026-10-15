"""Real player radio controls and full worked solutions in local Chromium.

Uses exact function bodies from ui/learning.js and imported question-field UI;
all fixtures are in memory, with no application API or EDB writes.
"""
import sys;sys.dont_write_bytecode=True
import functools,hashlib,http.server,json,subprocess,threading
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
source=(ROOT/'ui/learning.js').read_text()
def block(start,end):return source[source.index(start):source.index(end,source.index(start))]
parts=[block('function el(','function button('),block('function short(','function appendStepHeading('),block('function fieldLabel(','function announce('),block('function escapeHTML(','function loadMath('),block('function choiceOrder(','async function openPreview(')]
imports="import {marked} from '/ui/vendor/marked/marked.esm.js';\nimport {romanLists} from '/ui/prose-lists.js';\nimport {inlinePrompt,checkboxControl,choiceIndicator,fieldFeedback,blankInput,freeInput,richSelect} from '/ui/question-fields.js';\n"
js=imports+'\n'.join(parts)+r'''
const typeset=async node=>MathJax.typesetPromise([node]);
window.renderRecord=async record=>{
 await MathJax.startup.promise;MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question,heading=el('h2','',q[':question/difficulty'].split('/').at(-1)+' — '+record.generation.template);document.body.append(heading);
 const fields=q[':question/answer-fields'].map((f,i)=>({id:20+i,key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map((a,j)=>({id:100+j,type:a[':answer/type'],value:a[':answer/value'],uuid:a[':answer/id']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 const form=el('form');for(const f of fields)form.append(fieldControl(f,false,q[':question/id'],q[':question/problem']));document.body.append(form);
 const submit=el('button','','Check answer');submit.type='button';const result=el('p','result');const solution=markdown(q[':question/worked-solution'],'prose solution');solution.hidden=true;
 submit.addEventListener('click',()=>{const response=collectResponses(form,fields)[0];const selected=fields[0].choices.find(a=>String(a.id)===String(response.choiceId));const ok=selected?.uuid===q[':question/answer-fields'][0][':answer-field/correct'][1];result.textContent=ok?'Correct':'Incorrect';fields[0].response={choiceId:response.choiceId};fields[0].correctAnswer={id:fields[0].choices.find(a=>a.uuid===q[':question/answer-fields'][0][':answer-field/correct'][1]).id};fieldFeedback(form.querySelector('fieldset'),fields[0],ok?'correct':'incorrect');solution.hidden=false;});
 document.body.append(submit,result,solution);
 await MathJax.typesetPromise([document.body]);
 const correct=q[':question/answer-fields'][0][':answer-field/correct'][1];const choice=fields[0].choices.find(a=>a.uuid===correct);
 const wrong=fields[0].choices.find(a=>a.uuid!==correct);form.querySelector('input[value="'+wrong.id+'"]').click();submit.click();const wrongInteraction=result.textContent==='Incorrect';const input=form.querySelector('input[value="'+choice.id+'"]');input.click();submit.click();
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 return {wrongInteraction,mathjaxVersion:MathJax.version,errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),visibleIndicators:[...form.querySelectorAll('.answer-indicator')].filter(n=>{const s=getComputedStyle(n);return n.getBoundingClientRect().width>=20&&s.borderStyle!=='none'&&s.borderColor!=='rgba(0, 0, 0, 0)'}).length,controls:form.querySelectorAll('input[type=radio]').length,selected:form.querySelectorAll('input:checked').length,correctInteraction:result.textContent==='Correct',fullSolutionVisible:!solution.hidden,overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:1000px;margin:25px auto;background:white;color:#222;padding:20px}.prose{margin-bottom:12px}.solution{border-top:1px solid #aaa;padding-top:15px}.result{font-weight:bold}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
records=json.loads((D/'review.json').read_text());(D/'render-records.json').write_text(json.dumps(records)+'\n')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:subprocess.run(['node',str(D/'render-cdp.js'),'http://127.0.0.1:'+str(server.server_port),str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
r=json.loads((D/'render-report.json').read_text());r['ui_source_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/learning.css',ROOT/'ui/navigation.css']};(D/'render-report.json').write_text(json.dumps(r,indent=2)+'\n')
