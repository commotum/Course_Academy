"""Actual player functions and field controls; headless loopback rendering only."""
import functools,http.server,json,threading,hashlib,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2];source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function short('):source.index('function short(')+source[source.index('function short('):].index('\n')],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function loadMath(')],source[source.index('function choiceOrder('):source.index('function collectResponses(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { loadMathInputs,inlinePrompt,mountInlineFields,blankInput,checkboxControl,freeInput,choiceIndicator,fieldFeedback,richSelect } from '/ui/question-fields.js';\n"+'\n'.join(parts)+r'''
const typeset=async e=>MathJax.typesetPromise([e]);
window.renderRecord=async record=>{
 await MathJax.startup.promise; await loadMathInputs();MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question,meta=record.generation;
 const heading=el('h1','',meta.template+' · '+(q[':question/difficulty']||'missing source difficulty'));document.body.append(heading);
 const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],answerType:f[':answer-field/choices'][0][':answer/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields),fieldList=el('div','answer-fields');
 mountInlineFields(prompt,fieldList,fields,f=>fieldControl(f,false,q[':question/id'],q[':question/problem']));document.body.append(prompt,fieldList);
 document.body.append(el('h2','','Worked solution'),markdown(q[':question/worked-solution']||'Missing from source.','prose solution'));
 await MathJax.typesetPromise([document.body]);
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
 const mathFields=[...document.querySelectorAll('math-field')];for(const input of mathFields){input.value='2';if(input.value!=='2')throw Error('math control entry failed');input.value='';}
 const radios=[...document.querySelectorAll('input[type=radio]')];if(radios.length){radios[0].click();if(!radios[0].checked)throw Error('radio click failed');}
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,blanks:document.querySelectorAll('math-field,input:not([type=radio])').length,mathfields:mathFields.length,visibleControls:[...document.querySelectorAll('math-field,.choice-check')].every(n=>n.getBoundingClientRect().width>0&&n.getBoundingClientRect().height>0),radios:radios.length,fieldsets:document.querySelectorAll('fieldset').length,overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().right>1120)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:1000px;margin:24px auto;background:white;color:#222;padding:20px}.prose{margin-bottom:12px}h1{font-size:20px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
try:subprocess.run(['node',str(D/'render-cdp.js'),origin,str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/navigation.css',ROOT/'ui/learning.css')};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
