"""Actual player Markdown/fieldControl/collectResponses and MathJax, local CDP."""
import sys
sys.dont_write_bytecode=True
import functools,hashlib,http.server,json,subprocess,threading
from pathlib import Path
D=Path(__file__).resolve().parent;REPO=D.parents[2]
s=(REPO/'ui/learning.js').read_text()
def between(a,b):return s[s.index(a):s.index(b)]
js="""import {marked} from '/ui/vendor/marked/marked.esm.js';
import {romanLists} from '/ui/prose-lists.js';
import {checkboxControl,freeInput,choiceIndicator,fieldFeedback,blankInput,richSelect,inlinePrompt,responsesComplete} from '/ui/question-fields.js';
const short=value=>String(value||'').split('/').at(-1);
const typeset=()=>{};
"""
js+=between('function el(','function button(')+'\n'
js+=between('function fieldLabel(','function escapeHTML(')+'\n'
js+=between('function escapeHTML(','function loadMath(')+'\n'
js+=between('function choiceOrder(','async function openPreview(')+'\n'
js+=r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const f=q[':question/answer-fields'][0];
 const field={id:20,key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map((a,i)=>({id:100+i,type:a[':answer/type'],value:a[':answer/value']}))};
 const article=el('article','lesson-content');const card=el('div','content-card');article.append(card);document.body.append(article);
 card.append(el('p','difficulty',short(q[':question/difficulty'])||'unrated original'));
 const form=el('form');form.addEventListener('submit',e=>e.preventDefault());
 form.append(markdown(q[':question/problem'],'prose prompt',[field]));form.append(fieldControl(field,false,q[':question/id']));
 const actions=el('div','answer-actions');const check=el('button','primary','Check answer');check.type='submit';
 const refresh=()=>{check.disabled=!responsesComplete([field],collectResponses(form,[field]));};
 form.addEventListener('input',refresh);form.addEventListener('change',refresh);actions.append(check);form.append(actions);card.append(form);refresh();
 const beforeDisabled=check.disabled;const inputs=[...form.querySelectorAll('input[type=radio]')];inputs[1].click();
 const response=collectResponses(form,[field]);const selected=inputs.filter(x=>x.checked).length;
 const afterEnabled=!check.disabled;const actualSubmission=response[0].choiceId;
 const solution=el('details','worked-solution');solution.open=true;solution.append(el('summary','solution-heading','Solution:'));
 if(q[':question/worked-solution'])solution.append(markdown(q[':question/worked-solution'],'prose'));else solution.append(el('p','','Original worked solution absent.'));
 card.append(solution);await MathJax.typesetPromise([article]);
 let alignRows=[];for(const item of MathJax.startup.document.math)item.root.walkTree(n=>{if(n.kind==='mtable')alignRows.push(n.childNodes.length);});
 const clone=article.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 return {mathjax:MathJax.version,errors:article.querySelectorAll('[data-mml-node=merror],.MathJax_Error').length,exposed:/\$|\\begin|\\end/.test(clone.innerText),overflow:article.scrollWidth>article.clientWidth,radios:inputs.length,visibleIndicators:[...article.querySelectorAll('.answer-indicator')].filter(n=>{let b=n.getBoundingClientRect(),c=getComputedStyle(n);return b.width>10&&b.height>10&&c.borderTopStyle==='solid'&&c.borderTopColor!=='rgba(0, 0, 0, 0)';}).length,beforeDisabled,afterEnabled,selected,actualSubmission,solutionOpen:solution.open,alignRows,svg:article.querySelectorAll('mjx-container svg').length};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/learning.css"><link rel="stylesheet" href="/ui/navigation.css"><style>body{max-width:1100px;margin:20px auto;background:white;color:#222;padding:20px}.content-card{max-width:1100px}.difficulty{font-size:14px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(REPO)));threading.Thread(target=server.serve_forever,daemon=True).start()
records=json.loads((D/'source-replays.json').read_text())
originals=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions']
originals={x[':question/math-academy-id']:x for x in originals}
for r in records:
 source=originals[r['generation']['source_id']]
 # Exact immutable source learner strings, with enum/lookup adapter only.
 r['question']=source
 q=r['question']
 if ':question/difficulty' in q:q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
records += [x['record'] for x in json.loads((D/'review.json').read_text())]
(D/'render-records.json').write_text(json.dumps(records))
try:subprocess.run(['node',str(D/'render-cdp.js'),f'http://127.0.0.1:{server.server_port}',str(D.relative_to(REPO))],cwd=REPO,check=True)
finally:server.shutdown();server.server_close()
r=json.loads((D/'render-report.json').read_text());r['ui_source_hashes']={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (REPO/'ui/learning.js',REPO/'ui/question-fields.js',REPO/'ui/mathjax-config.js',REPO/'ui/learning.css',REPO/'ui/navigation.css',REPO/'ui/vendor/mathjax/tex-svg.js')};r['runtime']={'python':sys.version.split()[0],'node':subprocess.check_output(['node','--version'],text=True).strip(),'chromium':subprocess.check_output(['/home/jake/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell','--version'],text=True).strip(),'mathjax':r['checks'][0]['mathjax']};(D/'render-report.json').write_text(json.dumps(r,indent=2)+'\n')
