"""Private immutable-player renderer. No application or engine edits."""
import functools,http.server,json,threading,hashlib,subprocess,pathlib
D=pathlib.Path(__file__).resolve().parent;ROOT=D.parents[2]
source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function short('):source.index('function short(')+source[source.index('function short('):].index('\n')],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function loadMath(')],source[source.index('function choiceOrder('):source.index('function collectResponses(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport {loadMathInputs, inlinePrompt,mountInlineFields,blankInput,choiceIndicator,fieldFeedback,checkboxControl,freeInput,richSelect} from '/ui/question-fields.js';\nconst typeset=node=>MathJax.typesetPromise([node]);\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;await loadMathInputs();
 MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const card=el('main','content-card');document.body.append(card);
 const q=record.question;card.append(el('h2','',record.generation.level+' · '+record.generation.template+' · '+record.generation.profile));
 const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],answerType:f[':answer-field/choices'][0][':answer/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],value:a[':answer/value'],type:a[':answer/type']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);card.append(prompt);
 const list=el('div','answer-fields');card.append(list);
 mountInlineFields(prompt,list,fields,field=>fieldControl(field,false,q[':question/id'],q[':question/problem']));
 if(fields.some(f=>!q[':question/answer-fields'].find(x=>x[':answer-field/id']===f.id)[':answer-field/correct']))card.append(el('p','','Raw source has no correct designation. Evidence only.'));
 card.append(el('h3','','Worked solution'));
 card.append(markdown(q[':question/worked-solution']||'Raw source has no worked solution.','prose solution'));
 await customElements.whenDefined('math-field');await MathJax.typesetPromise([card]);await document.fonts.ready;
 await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=card.cloneNode(true);clone.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
 const inputs=[...card.querySelectorAll('math-field')];const borders=inputs.map(n=>({width:getComputedStyle(n).borderTopWidth,color:getComputedStyle(n).borderTopColor,shadow:!!n.shadowRoot}));
 return {errors:card.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,blanks:inputs.length,radios:card.querySelectorAll('input[type="radio"]').length,borders,overflow:[...card.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().right>innerWidth),theme:document.documentElement.dataset.theme};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<!doctype html><html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{padding:24px}main.content-card{max-width:1050px;margin:auto;padding:30px}h2{font-size:14px}.solution{margin-top:24px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
records=json.load(open(D/'review.json'))+json.load(open(D/'render-extra-records.json'));(D/'render-records.json').write_text(json.dumps(records,indent=2)+'\n')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:subprocess.run(['node',str(D/'render-cdp.js'),f'http://127.0.0.1:{server.server_port}',str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.load(open(D/'render-report.json'));report['ui_source_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/learning.css',ROOT/'ui/navigation.css']};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
