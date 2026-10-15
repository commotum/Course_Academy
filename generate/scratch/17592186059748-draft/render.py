import functools,http.server,json,threading,re,hashlib,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function answerValue(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { inlinePrompt,loadMathInputs,blankInput,choiceIndicator } from '/ui/question-fields.js';\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;await loadMathInputs();MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({key:f[':answer-field/key'],type:f[':answer-field/type'],id:f[':answer-field/id'],answerType:'answer.type/math'}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 let blanks=0,radios=0;
 for(let i=0;i<fields.length;i++){
  const f=fields[i],raw=q[':question/answer-fields'][i];
  if(f.type.endsWith('/blank')){
   const slot=prompt.querySelector('[data-field-key="'+f.key+'"]');if(!slot)throw Error('Missing slot '+f.key);
   const control=blankInput(f,fieldLabel(f.key),f.id);slot.replaceChildren(control);control.value=raw[':answer-field/choices'][0][':answer/value'];
   if(!control.shadowRoot||!control.value)throw Error('MathLive failed '+f.key);blanks++;
  }else{
   for(const a of raw[':answer-field/choices']){
    const row=document.createElement('label');row.className='choice';const input=document.createElement('input');input.type='radio';input.name=f.id;input.value=a[':answer/id'];
    row.append(choiceIndicator(input),markdown('$'+a[':answer/value']+'$','prose'));document.body.append(row);if(a[':answer/id']===raw[':answer-field/correct']?.[1]){input.click();if(!input.checked)throw Error('Radio interaction failed');}radios++;
   }
  }
 }
 document.body.append(markdown(q[':question/worked-solution']||'','prose solution'));
 await MathJax.typesetPromise([document.body]);
 const tables=[],undefinedCommands=[];
 for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{
  if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});
  if(node.kind==='merror'||/Undefined command|\\[a-zA-Z]+/.test(node.getText?.()||''))undefinedCommands.push(node.getText?.()||node.kind);
 });
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,redNodes:document.querySelectorAll('[fill="red"],[stroke="red"],[data-mjx-error]').length,undefinedCommands,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,blanks,radios,checkedRadios:document.querySelectorAll('input[type=radio]:checked').length,mathLiveValues:[...document.querySelectorAll('math-field')].map(e=>({value:e.value,shadow:Boolean(e.shadowRoot)})),overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/navigation.css"><link rel="stylesheet" href="/ui/learning.css"><style>body{max-width:1000px;margin:32px auto;background:white;color:#222;padding:20px}.choice{display:flex;gap:10px;align-items:center;padding:4px 0}.choice .prose{margin:0}.prose{margin-bottom:12px}math-field{min-width:80px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
records=[z['record'] for z in json.loads((D/'review.json').read_text())]
for r in records:r['generation']['render_name']=r['question'].get(':question/difficulty','unrated').split('/')[-1]+'-'+r['generation']['template']
(D/'render-records.json').write_text(json.dumps(records)+'\n')
try:subprocess.run(['node',str(D/'render-cdp.js'),f'http://127.0.0.1:{server.server_port}',str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/navigation.css',ROOT/'ui/learning.css')};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
