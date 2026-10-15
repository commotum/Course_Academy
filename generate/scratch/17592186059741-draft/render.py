"""Render actual draft outputs with the player's Markdown/sanitization/MathJax pipeline."""
import functools,http.server,json,threading,re,hashlib
from pathlib import Path
import subprocess
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function loadMath(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { loadMathInputs, inlinePrompt, mountInlineFields, richSelect, blankInput, checkboxControl, freeInput, choiceIndicator, fieldFeedback } from '/ui/question-fields.js';\n"+'\n'.join(parts)+"\nconst short=value=>String(value||'').split('/').at(-1);\n"+source[source.index('function choiceOrder('):source.index('function collectResponses(')]+r'''
window.renderRecord=async record=>{
 await loadMathInputs(); await MathJax.startup.promise; MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],answerType:'math',choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 const fieldList=el('div','answer-fields');mountInlineFields(prompt,fieldList,fields,field=>fieldControl(field,false,q[':question/id'],q[':question/problem']));document.body.append(fieldList);
 document.body.append(markdown(q[':question/worked-solution']||'Source omits worked solution.','prose solution'));
 await MathJax.typesetPromise([document.body]);
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 return {errors:document.querySelectorAll('[data-mml-node="merror"],.math-error,mjx-merror').length,undefined:/Undefined|NaN/.test(document.body.textContent),literal_markup:/<span|data-field-key=/.test(document.body.textContent),red_error:[...document.querySelectorAll('mjx-container *')].some(n=>/rgb\(255, 0, 0\)|red/.test(n.getAttribute('fill')||'')),controls:document.querySelectorAll('input[type=radio],math-field').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,blanks:prompt.querySelectorAll('[data-field-key]').length,overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/navigation.css"><link rel="stylesheet" href="/ui/learning.css"><style>body{max-width:1000px;margin:32px auto;background:white;color:#222;padding:20px}.choice{padding:4px 0}.prose{margin-bottom:12px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
records=[]
for index,row in enumerate(json.loads((D/'review.json').read_text())):
 r=row['record'];r['generation']['template']=str(index)+'-'+row['label'].replace(' ','-').replace(',','_');records.append(r)
(D/'render-records.json').write_text(json.dumps(records)+'\n')
try:
 subprocess.run(['node',str(D/'render-cdp.js'),origin,str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js')};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
