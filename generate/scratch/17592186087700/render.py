"""Render actual draft outputs with the player's Markdown/sanitization/MathJax pipeline."""
import functools,http.server,json,threading,re,hashlib
from pathlib import Path
import subprocess
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function answerValue(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { inlinePrompt, checkboxControl } from '/ui/question-fields.js';\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise; MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],value:a[':answer/value'],type:a[':answer/type']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 for(const f of fields) document.body.append(checkboxControl(f,label=>markdown(label),false));
 document.body.append(markdown(q[':question/worked-solution'],'prose solution'));
 await MathJax.typesetPromise([document.body]);
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,red:document.querySelectorAll('mjx-merror,[data-mjx-error],.math-error,mjx-container [fill=red],mjx-container [stroke=red]').length,undefinedCommands:/Undefined control sequence|Unknown command/i.test(document.body.textContent),checkboxes:document.querySelectorAll('input[type=checkbox]').length,invisibleCheckboxes:[...document.querySelectorAll('.answer-indicator')].filter(n=>parseFloat(getComputedStyle(n).borderTopWidth)<1 || n.getBoundingClientRect().width<20).length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,blanks:prompt.querySelectorAll('[data-field-key]').length,overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:1000px;margin:32px auto;background:white;color:#222;padding:20px}.choice{padding:4px 0}.prose{margin-bottom:12px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'

try:
 subprocess.run(['node',str(D/'render-cdp.js'),origin,str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js')};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
