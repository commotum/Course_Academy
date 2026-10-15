"""Snapshot actual player code/dependencies and make complete local visual fixture."""
from pathlib import Path
import hashlib,json,shutil
D=Path(__file__).resolve().parent;repo=D.parents[2];ref=D/'reference/ui';ref.mkdir(parents=True,exist_ok=True)
for p in (repo/'ui').iterdir():
 if p.is_file():shutil.copy2(p,ref/p.name)
shutil.copytree(repo/'ui/vendor',ref/'vendor',dirs_exist_ok=True)
source=(ref/'learning.js').read_text()
def fn(name):
 start=source.index('function '+name+'(')
 if name=='escapeHTML':return source[start:source.index('\n',start)]
 return source[start:source.index('\n}\n',start)+2]
header="""import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
import {loadMathInputs,checkboxControl,freeInput,choiceIndicator,fieldFeedback,blankInput,richSelect,inlinePrompt} from './reference/ui/question-fields.js';
const short=v=>String(v||'').split('/').at(-1); const typeset=()=>{};
"""
script=header+'\n'.join(fn(n) for n in ['el','fieldLabel','escapeHTML','assetURL','markdown','answerValue','choiceOrder','fieldControl'])+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise;await loadMathInputs();
 const main=document.querySelector('main');MathJax.typesetClear([main]);main.replaceChildren();
 const q=record.question;const outer=el('section','lesson-content');const card=el('div','content-card');outer.append(card);main.append(outer);
 const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 card.append(markdown(q[':question/problem'],'prose prompt',fields));const fs=el('div','answer-fields');for(const f of fields)fs.append(fieldControl(f,false,q[':question/id']));card.append(fs);
 const actions=el('div','answer-actions');const check=el('button','primary','Check answer');check.type='button';actions.append(check);card.append(actions);
 const solution=el('div','worked-solution');solution.append(el('h3','solution-heading','Solution:'),markdown(q[':question/worked-solution'],'prose solution'));card.append(solution);
 const controls=el('div','lesson-controls');controls.append(el('button','secondary','Previous'),el('button','primary','Continue'));outer.append(controls);
 await MathJax.typesetPromise([main]);
 const clone=main.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 const promptmath=(q[':question/problem'].match(/\$\$[\s\S]*?\$\$|\$(?!\$).*?\$/g)||[]).length;
 const solutionmath=(q[':question/worked-solution'].match(/\$\$[\s\S]*?\$\$|\$(?!\$).*?\$/g)||[]).length;
 return {errors:main.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error').length,exposed:/\$|\\begin|\\end|\{\{/.test(clone.textContent),expected_math:promptmath+solutionmath+5,rendered_math:main.querySelectorAll('mjx-container').length,radios:main.querySelectorAll('input[type="radio"]').length,visible_radio_indicators:[...main.querySelectorAll('.answer-indicator')].every(n=>n.getBoundingClientRect().width>5),overflow_details:[...main.querySelectorAll('mjx-container')].filter(n=>n.scrollWidth>n.clientWidth+2).map(n=>({tex:[...MathJax.startup.document.math][[...main.querySelectorAll('mjx-container')].indexOf(n)]?.math,scroll:n.scrollWidth,client:n.clientWidth,svg_width:n.querySelector('svg')?.getBoundingClientRect().width,display:n.getAttribute('display'),text:n.outerHTML.slice(0,150)})),overflow:[...main.querySelectorAll('mjx-container')].some(n=>n.scrollWidth>n.clientWidth+2),mathlive_loaded:Boolean(customElements.get('math-field')),tone_token:getComputedStyle(document.documentElement).getPropertyValue('--tone-06').trim(),complete_solution:main.querySelector('.solution').textContent.length>200};
};
'''
(D/'render-harness.js').write_text(script)
html='''<!doctype html><html data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Trig parts review</title><link rel="stylesheet" href="reference/ui/learning.css"><link rel="stylesheet" href="reference/ui/navigation.css"><script src="reference/ui/vendor/dompurify/purify.min.js"></script><script src="reference/ui/mathjax-config.js"></script><script src="reference/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body><header class="topbar site-header"><a class="brand" href="#">Course Academy</a><nav><a aria-current="page" href="#">Study</a><a href="#">Activity</a><a href="#">Assignments</a></nav><button class="learner-name">Profile</button></header><main class="lesson-main lesson-feed"></main></body></html>'''
# Theme tokens are imported by the same actual navigation CSS dependency chain.
assert '--tone-06:' in (ref/'navigation.css').read_text()
(D/'render-harness.html').write_text(html)
files={str(p.relative_to(D)):hashlib.sha256(p.read_bytes()).hexdigest() for p in ref.rglob('*') if p.is_file()};(D/'reference/ui-snapshot.json').write_text(json.dumps(files,indent=2)+'\n')
print('Saved exact player functions and',len(files),'frozen UI assets')
