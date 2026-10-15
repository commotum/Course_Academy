"""Actual player Markdown, radio field controls and MathJax (no MathLive fields)."""
import functools,http.server,json,threading,hashlib,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function loadMath(')],source[source.index('function choiceOrder('):source.index('function collectResponses(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { inlinePrompt, checkboxControl, choiceIndicator,fieldFeedback,freeInput,blankInput,richSelect } from '/ui/question-fields.js';\nconst short=value=>String(value||'').split('/').at(-1);const typeset=()=>{};\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=(q[':question/answer-fields']||[]).map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 fields.forEach(f=>document.body.append(fieldControl(f,false,q[':question/id'],q[':question/problem'])));
 if(q[':question/worked-solution'])document.body.append(markdown(q[':question/worked-solution'],'prose solution'));
 await MathJax.typesetPromise([document.body]);
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 const redUndefined=document.querySelectorAll('[data-mml-node="mtext"][fill="red"],mtext[mathcolor="red"]');
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,redUndefined:redUndefined.length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,blanks:prompt.querySelectorAll('[data-field-key]').length,radioControls:document.querySelectorAll('input[type=radio]').length,overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:1000px;margin:32px auto;background:white;color:#222;padding:20px}.prose{margin-bottom:12px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
records=json.loads((D/'review.json').read_text())+json.loads((D/'source-replays.json').read_text())+json.loads((D/'source-completions.json').read_text())+[json.loads((D/'canonical-normal.json').read_text())]
(D/'render-records.json').write_text(json.dumps(records)+'\n')
try:subprocess.run(['node',str(D/'render-cdp.js'),origin,str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js')};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
