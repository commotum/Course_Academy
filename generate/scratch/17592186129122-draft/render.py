"""Render actual draft records through unchanged player controls and MathJax."""
import sys;sys.dont_write_bytecode=True
import functools,http.server,json,threading,hashlib,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2];source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function loadMath()')],source[source.index('function choiceOrder('):source.index('\nasync function openPreview(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { inlinePrompt, checkboxControl, choiceIndicator, fieldFeedback, freeInput, blankInput, richSelect } from '/ui/question-fields.js';\nconst short=x=>String(x).replace(/^:/,'').split('/').pop();\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;
 const fields=(q[':question/answer-fields']||[]).map((f,i)=>({id:20+i,key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map((a,j)=>({id:100+i*10+j,type:a[':answer/type'],value:a[':answer/value']}))}));
 const form=el('form');document.body.append(form);const prompt=markdown(q[':question/problem'],'prose prompt',fields);form.append(prompt);
 for(const f of fields)form.append(fieldControl(f,false,1,q[':question/problem']));
 if(q[':question/worked-solution'])form.append(markdown(q[':question/worked-solution'],'prose solution'));
 await MathJax.typesetPromise([document.body]);
 let selections=0;for(const f of fields){for(const a of f.choices){const input=[...form.querySelectorAll('input[type="radio"]')].find(x=>x.name===String(f.id)&&x.value===String(a.id));input.click();const out=collectResponses(form,fields).find(x=>x.fieldId===f.id);if(out.choiceId!==a.id)throw Error('player response collection mismatch');selections++;}for(const x of form.querySelectorAll('input'))x.checked=false;}
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 return {errors:document.querySelectorAll('[data-mml-node="merror"],.math-error,mjx-container [fill="red"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),radios:form.querySelectorAll('input[type="radio"]').length,selections,expectedRadios:fields.reduce((n,f)=>n+f.choices.length,0),overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1000)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/navigation.css"><link rel="stylesheet" href="/ui/learning.css"><style>body{max-width:1000px;margin:32px auto;background:white;color:#222;padding:20px}.prose{margin-bottom:12px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
records=json.loads((D/'raw-replays.json').read_text())+json.loads((D/'review.json').read_text())+json.loads((D/'normal-anchors.json').read_text())+[r['record'] for r in json.loads((D/'held-slot-checks.json').read_text())]
for r in records:
 gen=r['generation'];gen['render_role']=('raw-' if gen['evidence_only'] else r['question'][':question/difficulty'].split('/')[-1]+'-')+gen['template']+'-'+gen['unit']
(D/'render-records.json').write_text(json.dumps(records)+'\n')
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:subprocess.run(['node',str(D/'render-cdp.js'),f'http://127.0.0.1:{server.server_port}',str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report.update(python_version=sys.version.split()[0],node_version=subprocess.check_output(['node','--version'],text=True).strip(),ui_source_hashes={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/prose-lists.js',ROOT/'ui/learning.css',ROOT/'ui/navigation.css',ROOT/'ui/vendor/marked/marked.esm.js',ROOT/'ui/vendor/dompurify/purify.min.js',ROOT/'ui/vendor/mathjax/tex-svg.js']});(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
