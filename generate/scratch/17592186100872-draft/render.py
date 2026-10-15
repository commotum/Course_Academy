"""Actual player Markdown/field controls/MathLive/MathJax, private loopback only."""
import functools,http.server,json,threading,hashlib,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[2];s=(ROOT/'ui/learning.js').read_text()
def part(a,b):return s[s.index(a):s.index(b)]
imports="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { loadMathInputs, inlinePrompt, mountInlineFields, richSelect, questionFeedback, feedbackHeading, blankInput, responsesComplete, checkboxControl, freeInput, choiceIndicator, fieldFeedback } from '/ui/question-fields.js';\n"
js=imports+part('function el(','function button(')+part('function short(','function appendStepHeading(')+part('function fieldLabel(','function announce(')+part('function escapeHTML(','function loadMath(')+part('function choiceOrder(','function collectResponses(')+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;await loadMathInputs();MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],answerType:'math',choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],value:a[':answer/value'],type:a[':answer/type']}))}));
 const main=el('main','lesson-main');const feed=el('div','lesson-feed');const content=el('section','lesson-content');const card=el('div','content-card');
 document.body.append(main);main.append(feed);feed.append(content);content.append(card);
 const title=el('div','step-meta',record.generation.level+' • '+record.generation.template+' • '+record.generation.profile);card.append(title);
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);const list=el('div','answer-fields');card.append(prompt,list);
 mountInlineFields(prompt,list,fields,field=>fieldControl(field,false,q[':question/id'],q[':question/problem'],''));
 const solution=el('div','worked-solution');solution.append(el('h2','solution-heading','Worked solution'),markdown(q[':question/worked-solution']||'[Source worked solution absent]'));card.append(solution);
 await MathJax.typesetPromise([main]);await document.fonts.ready;await new Promise(r=>setTimeout(r,40));
 const controls=[...document.querySelectorAll('math-field,input[type=radio]')];
 const overflow=[...document.querySelectorAll('mjx-container,table')].filter(n=>n.scrollWidth>n.clientWidth+2).map(n=>({tag:n.tagName,width:n.clientWidth,scrollWidth:n.scrollWidth}));
 const clone=main.cloneNode(true);clone.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),blank_controls:document.querySelectorAll('math-field').length,radio_controls:document.querySelectorAll('input[type=radio]').length,controls_visible:controls.every(n=>{const b=n.getBoundingClientRect();return b.width>0&&b.height>0;}),overflow,documentOverflow:document.documentElement.scrollWidth>window.innerWidth+2,solution_present:Boolean(q[':question/worked-solution'])};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/navigation.css"><link rel="stylesheet" href="/ui/learning.css"><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:subprocess.run(['node',str(D/'render-cdp.js'),f'http://127.0.0.1:{server.server_port}',str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
r=json.loads((D/'render-report.json').read_text());r['ui_source_hashes']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['ui/learning.js','ui/question-fields.js','ui/mathjax-config.js','ui/learning.css','ui/navigation.css','ui/vendor/marked/marked.esm.js','ui/vendor/mathlive/mathlive.min.mjs','ui/vendor/mathjax/tex-svg.js']};(D/'render-report.json').write_text(json.dumps(r,indent=2)+'\n')
