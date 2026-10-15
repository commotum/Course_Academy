"""Actual player functions/controls, full worked solutions; local immutable assets."""
import sys;sys.dont_write_bytecode=True
import functools,http.server,json,threading,hashlib,subprocess,importlib.util
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function fieldLabel('):source.index('function announce(')],source[source.index('function escapeHTML('):source.index('function loadMath(')],source[source.index('function choiceOrder('):source.index('function collectResponses(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { inlinePrompt,mountInlineFields,richSelect,checkboxControl,freeInput,blankInput,choiceIndicator,fieldFeedback } from '/ui/question-fields.js';\nconst short=v=>String(v||'').split('/').at(-1);const typeset=n=>MathJax.typesetPromise([n]);\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields),list=el('div','field-list');document.body.append(prompt,list);
 mountInlineFields(prompt,list,fields,f=>fieldControl(f,false,q[':question/id'],q[':question/problem']));
 document.body.append(markdown(q[':question/worked-solution'],'prose solution'));
 await MathJax.typesetPromise([document.body]);
 const trigger=document.querySelector('.answer-select-trigger');trigger.click();
 const options=[...document.querySelectorAll('[role="option"]')];
 const banks=options.map(n=>n.textContent.trim());
 let selections=0;for(const option of options){option.click();selections++;trigger.click();}
 const f=q[':question/answer-fields'][0];const correct=f[':answer-field/choices'].find(a=>a[':answer/id']===f[':answer-field/correct'][1])[':answer/value'];options.find(n=>n.textContent.trim()===correct).click();
 const systems=[];for(const table of document.querySelectorAll('[data-mml-node="mtable"]')){
  const brace=[...table.parentElement.children].find(n=>n.dataset.mmlNode==='mo');
  if(!brace?.querySelector('[data-c="7B"],[data-c="23A7"],[data-c="23A8"],[data-c="23A9"]'))continue;
  const equals=[...table.children].filter(n=>n.dataset.mmlNode==='mtr').map(row=>(row.children[1]||row).querySelector('[data-c="3D"]')).filter(Boolean).map(n=>n.getBoundingClientRect().x);
  systems.push({equals,braceHeight:brace.getBoundingClientRect().height,tableHeight:table.getBoundingClientRect().height});
 }
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container,select').forEach(n=>n.remove());
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),controls:document.querySelectorAll('.answer-inline .answer-select-trigger').length,banks,selections,systems,overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1000)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:960px;margin:32px auto;background:white;color:#222;padding:20px}.prose{margin-bottom:12px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
records=[];labels=[]
for case in json.loads((D/'source-cases.json').read_text()):
 records.append(g.generate(case['authored_level'],parameters=case['parameters'],template=case['template']));labels.append('anchor-'+case['source_id'])
for level in g.LEVELS:
 seen=set()
 for seed in range(100):
  r=g.generate(level,seed=seed);branch=r['generation']['inferred_correct_value']
  if branch not in seen:
   records.append(r);labels.append(level+'-'+branch.replace(' ','-'));seen.add(branch)
  if len(seen)==3:break
for level,values in [('easy',(5,-5,12,-5,3,-12)),('moderate',(-2,5,30,-8,-10,-30)),('hard',(-3,1,30,-12,4,-30))]:
 records.append(g.generate(level,parameters=dict(zip('abcdef',values))));labels.append('boundary-'+level)
(D/'render-records.json').write_text(json.dumps([{'label':label,'record':r} for label,r in zip(labels,records)])+'\n')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:subprocess.run(['node',str(D/'render-cdp.js'),f'http://127.0.0.1:{server.server_port}',str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/learning.css',ROOT/'ui/navigation.css')};report['record_file_sha256']=hashlib.sha256((D/'render-records.json').read_bytes()).hexdigest();(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
