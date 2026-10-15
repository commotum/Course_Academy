import sys
sys.dont_write_bytecode=True
import functools,http.server,json,threading,re,hashlib,importlib.util,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('singularity_render_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=(ROOT/'ui/learning.js').read_text()
def function(name,next_name):return source[source.index('function '+name+'('):source.index('function '+next_name+'(')]
parts=[function('el','button'),'',function('escapeHTML','answerValue'),function('answerValue','loadMath'),function('choiceOrder','collectResponses')]
# fieldLabel ends before its next declaration; find its exact closing brace.
parts[1]=source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { inlinePrompt, checkboxControl, freeInput, blankInput, choiceIndicator, fieldFeedback, richSelect } from '/ui/question-fields.js';\nconst short=v=>String(v||'').split('/').at(-1);\nconst typeset=()=>{};\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 for(const f of fields)document.body.append(fieldControl(f,false,q[':question/id'],q[':question/problem']));
 const controls=[...document.querySelectorAll('input[type=checkbox]')];
 if(controls.length!==3)throw Error('Expected three actual checkbox controls');
 for(let i=0;i<3;i++){
  const hidden=controls[i].closest('label').querySelector('input[type=hidden]');const no=fields[i].choices.find(a=>a.value==='false').id;const yes=fields[i].choices.find(a=>a.value==='true').id;
  if(hidden.value!==no)throw Error('Unchecked field must encode false');controls[i].checked=true;controls[i].dispatchEvent(new Event('change'));if(hidden.value!==yes)throw Error('Checked field must encode true');controls[i].checked=false;controls[i].dispatchEvent(new Event('change'));
 }
 document.body.append(markdown(q[':question/worked-solution'],'prose solution'));await MathJax.typesetPromise([document.body]);
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,controls:controls.length,unchecked_false_and_checked_true:true,overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:1000px;margin:32px auto;background:white;color:#222;padding:20px}.prose{margin-bottom:12px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
records=[]
for c in json.loads((D/'source-cases.json').read_text()):
 records.append(g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
 for seed in (132,265):records.append(g.generate(c['level'],template=c['template'],seed=seed))
records += [g.generate('hard',seed=n)for n in (0,1)]
(D/'render-records.json').write_text(json.dumps(records)+'\n')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
try:subprocess.run(['node',str(D/'render-cdp.js'),origin,str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js')};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
