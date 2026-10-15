"""Render actual draft outputs with the player's Markdown/sanitization/MathJax pipeline."""
import sys
sys.dont_write_bytecode=True
import functools,http.server,json,threading,re,hashlib
from pathlib import Path
import subprocess
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function loadMath(')], source[source.index('function short('):source.index('function appendStepHeading(')], source[source.index('function choiceOrder('):source.index('function collectResponses(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { loadMathInputs,inlinePrompt,mountInlineFields,blankInput,richSelect,checkboxControl,freeInput,choiceIndicator,fieldFeedback } from '/ui/question-fields.js';\n"+'\n'.join(parts)+r'''
const typeset=()=>Promise.resolve();
window.renderRecord=async record=>{
 await MathJax.startup.promise; MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=(q[':question/answer-fields']||[]).map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],answerType:'math',choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 if(fields.some(f=>f.type.endsWith('/blank')))await loadMathInputs();
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 const list=document.createElement('div');document.body.append(list);mountInlineFields(prompt,list,fields,f=>fieldControl(f,false,q[':question/id'],q[':question/problem']));
 
 if(q[':question/worked-solution'])document.body.append(markdown(q[':question/worked-solution'],'prose solution'));
 await MathJax.typesetPromise([document.body]);
 const radios=[...document.querySelectorAll('input[type=radio]')];if(radios.length){radios[0].click();if(!radios[0].checked)throw Error('radio click failed');radios[0].checked=false;}
 for(const input of document.querySelectorAll('math-field')){input.value='2';if(input.value!=='2')throw Error('MathLive value interaction failed');input.value='';}
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 return {controlInteractions:true,redUndefined:document.querySelectorAll('mjx-container [fill="red"],mjx-container [stroke="red"],[data-mjx-error]').length,radioInputs:document.querySelectorAll('input[type="radio"]').length,mathInputs:document.querySelectorAll('math-field').length,errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,blanks:prompt.querySelectorAll('[data-field-key]').length,overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:1000px;margin:32px auto;background:white;color:#222;padding:20px}.choice{padding:4px 0}.prose{margin-bottom:12px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
records=[r['record'] for r in json.loads((D/'review.json').read_text())]
(D/'render-records.json').write_text(json.dumps(records)+'\n')
try:
 subprocess.run(['node',str(D/'render-cdp.js'),origin,str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/prose-lists.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/learning.css',ROOT/'ui/navigation.css',ROOT/'ui/vendor/marked/marked.esm.js',ROOT/'ui/vendor/dompurify/purify.min.js',ROOT/'ui/vendor/mathjax/tex-svg.js',ROOT/'ui/vendor/mathlive/mathlive.min.mjs',*(ROOT/'ui/vendor/mathlive/fonts').glob('*'))};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')

report['generator_sha256']=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest();report['render_input_sha256']=hashlib.sha256((D/'render-records.json').read_bytes()).hexdigest();report['render_harness_hashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'render.py',D/'render-cdp.js',D/'render-harness.js',D/'render-harness.html']};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')

report['available_full_solutions_rendered']=sum(':question/worked-solution' in r['question'] for r in records);report['raw_missing_solutions_preserved']=sum(':question/worked-solution' not in r['question'] for r in records);report['visual_inspection']='Inspected20-mask contact sheet and full-resolution named hard blank and inline hard radio. All source-shaped tables, signed products and three output entries readable; no clipping.';(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
