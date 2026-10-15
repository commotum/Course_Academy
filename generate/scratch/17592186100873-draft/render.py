import sys;sys.dont_write_bytecode=True
import functools,http.server,json,threading,hashlib,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
s=(ROOT/'ui/learning.js').read_text();parts=[s[s.index('function el('):s.index('function button(')],s[s.index('function fieldLabel('):s.index('function announce(')],s[s.index('function escapeHTML('):s.index('function loadMath(')],s[s.index('function choiceOrder('):s.index('function collectResponses(')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { loadMathInputs,inlinePrompt,mountInlineFields,richSelect,checkboxControl,freeInput,blankInput,choiceIndicator,fieldFeedback } from '/ui/question-fields.js';\nconst short=v=>String(v||'').split('/').at(-1);const typeset=n=>MathJax.typesetPromise([n]);\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;await loadMathInputs();MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],answerType:':answer.type/math',key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const main=el('main','lesson-main'),card=el('section','lesson-content'),prompt=markdown(q[':question/problem'],'prose prompt',fields),list=el('div','answer-fields');card.append(prompt,list);main.append(card);document.body.append(main);
 mountInlineFields(prompt,list,fields,f=>fieldControl(f,false,q[':question/id'],q[':question/problem']));
 if(q[':question/worked-solution'])card.append(markdown(q[':question/worked-solution'],'prose worked-solution solution'));
 else card.append(el('p','missing','Raw source has no worked solution or correct designation.'));
 await MathJax.typesetPromise([document.body]);
 if(fields[0].type.endsWith('/blank')){await customElements.whenDefined('math-field');const input=document.querySelector('math-field');input.value='7';input.dispatchEvent(new Event('input',{bubbles:true}));}
 else {for(const input of document.querySelectorAll('input[type=radio]'))input.click();}
 const matricesPrompt=document.querySelectorAll('.prompt [data-mml-node="mtable"]').length;
 const matricesSolution=document.querySelectorAll('.solution [data-mml-node="mtable"]').length;
 const tables=[...document.querySelectorAll('.solution [data-mml-node="mtable"]')];
 const firstAlignedRow=tables[0]?[...tables[0].children].find(n=>n.dataset.mmlNode==='mtr'):null;
 const firstStageSubscripts=firstAlignedRow?firstAlignedRow.querySelectorAll('[data-mml-node="msub"]').length:0;
 const alignedRows=tables[0]?[...tables[0].children].filter(n=>n.dataset.mmlNode==='mtr').length:0;
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
 const controls=[...document.querySelectorAll('input[type=radio],math-field')];
 return {mathJaxVersion:MathJax.version,browserUserAgent:navigator.userAgent,errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),controlCount:controls.length,controlTypes:controls.map(n=>n.tagName),controlVisibility:controls.every(n=>{const r=n.getBoundingClientRect();const c=getComputedStyle(n);return r.width>0&&r.height>0&&c.display!=='none'&&c.visibility!=='hidden'}),blankValue:document.querySelector('math-field')?.value,matricesPrompt,matricesSolution,alignedRows,firstStageSubscripts,overflow:[...document.querySelectorAll('mjx-container[display="true"]')].some(n=>n.scrollWidth>n.clientWidth+2),solutionPresent:Boolean(q[':question/worked-solution']),documentHeight:document.documentElement.scrollHeight};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/navigation.css"><link rel="stylesheet" href="/ui/learning.css"><style>.answer-fields:empty{display:none}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
records=[]
for r in json.loads((D/'source-replays.json').read_text()):records.append({'label':'source-'+r['generation']['template'],'record':r})
for i,r in enumerate(json.loads((D/'review.json').read_text())):records.append({'label':r['question'][':question/difficulty'].split('/')[-1]+'-'+str(i),'record':r})
for i,r in enumerate(json.loads((D/'held-target-records.json').read_text())):records.append({'label':'held-target-'+str(i),'record':r})
for x in records:x['record_sha256']=hashlib.sha256(json.dumps(x['record'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
(D/'render-records.json').write_text(json.dumps(records,indent=2)+'\n')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:subprocess.run(['node',str(D/'render-cdp.js'),f'http://127.0.0.1:{server.server_port}',str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
r=json.loads((D/'render-report.json').read_text());r['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/learning.css',ROOT/'ui/navigation.css',ROOT/'ui/vendor/mathlive/mathlive.min.mjs',ROOT/'ui/vendor/mathjax/tex-svg.js',ROOT/'ui/vendor/marked/marked.esm.js')};r['runtime_versions']={'python':sys.version.split()[0],'mathjax':r['checks'][0]['mathJaxVersion'],'mathlive':'0.108.3','marked':'18.0.14','browser_user_agent':r['checks'][0]['browserUserAgent']};r['record_file_sha256']=hashlib.sha256((D/'render-records.json').read_bytes()).hexdigest();(D/'render-report.json').write_text(json.dumps(r,indent=2)+'\n')
