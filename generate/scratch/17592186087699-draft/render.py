"""Actual player Markdown, answerValue and fieldControl, with MathJax checks."""
import sys
sys.dont_write_bytecode = True
import functools
import hashlib
import http.server
import json
import subprocess
import threading
from pathlib import Path

D = Path(__file__).resolve().parent
ROOT = D.parents[2]
source = (ROOT/'ui/learning.js').read_text()
parts = [source[source.index('function el('):source.index('function button(')],
         source[source.index('function fieldLabel('):source.index('function announce(')],
         source[source.index('function escapeHTML('):source.index('function loadMath(')],
         source[source.index('function choiceOrder('):source.index('function collectResponses(')]]
js = "import {marked} from '/ui/vendor/marked/marked.esm.js';\nimport {romanLists} from '/ui/prose-lists.js';\nimport {inlinePrompt,checkboxControl,choiceIndicator,fieldFeedback} from '/ui/question-fields.js';\nconst short=value=>String(value).split('/').at(-1);\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;
 const fields=(q[':question/answer-fields']||[]).map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 for(const f of fields)document.body.append(fieldControl(f,false,q[':question/id'],q[':question/problem']));
 document.body.append(markdown(q[':question/worked-solution'],'prose solution'));
 for(const field of fields){
  const set=[...document.querySelectorAll('fieldset.answer-field')].find(n=>n.dataset.fieldId===String(field.id));
  if(field.type.endsWith('/checkbox')){
   const input=set.querySelector('input[type="checkbox"]'),hidden=set.querySelector('.answer-choice-value');
   const yes=field.choices.find(a=>a.value==='true'),no=field.choices.find(a=>a.value==='false');
   if(!input||hidden.value!==String(no.id))throw Error('Initial unchecked field contract');
   input.checked=true;input.dispatchEvent(new Event('input'));
   if(hidden.value!==String(yes.id))throw Error('Checked entity submission contract');
   input.checked=false;input.dispatchEvent(new Event('input'));
   if(hidden.value!==String(no.id))throw Error('Explicit false entity submission contract');
  }else if(field.type.endsWith('/radio')){
   const controls=set.querySelectorAll('input[type="radio"]');
   if(controls.length!==field.choices.length)throw Error('Radio full bank contract');
   if(JSON.stringify([...controls].map(n=>n.value).sort())!==JSON.stringify(field.choices.map(a=>String(a.id)).sort()))throw Error('Radio answer ownership');
  }
 }
 await MathJax.typesetPromise([document.body]);
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 const undefinedMacros=[...document.querySelectorAll('mjx-container [data-mml-node="mtext"]')].filter(n=>n.textContent.includes('\\')||n.querySelector('[fill="red"],[stroke="red"]')).map(n=>n.textContent);
 // noUndefined renders some unknown macros as red mtext rather than merror.
 const red=[...document.querySelectorAll('mjx-container [fill],mjx-container [stroke],mjx-container [style]')].filter(n=>/red|#f00|#ff0000|rgb\(255,\s*0,\s*0\)/i.test((n.getAttribute('fill')||'')+' '+(n.getAttribute('stroke')||'')+' '+(n.getAttribute('style')||'')));
 return {errors:document.querySelectorAll('[data-mml-node="merror"],mjx-merror').length,undefinedMacros:undefinedMacros.length+red.length,exposed:/\$|\\begin|\\end|\{\{/.test(clone.textContent),tables,fieldsets:document.querySelectorAll('fieldset.answer-field').length,checkboxes:document.querySelectorAll('input[type="checkbox"]').length,radios:document.querySelectorAll('input[type="radio"]').length,overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:1000px;margin:32px auto;padding:20px}.prose{margin-bottom:12px}.answer-field{margin-bottom:12px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass


server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
    subprocess.run(['node',str(D/'render-cdp.js'),'http://127.0.0.1:'+str(server.server_port),str(D.relative_to(ROOT))],check=True,cwd=ROOT)
finally:
    server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text())
report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/prose-lists.js',ROOT/'ui/learning.css',ROOT/'ui/navigation.css')}
(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
