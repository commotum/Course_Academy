"""Render actual player Markdown and radio controls locally, without database APIs."""
from pathlib import Path
import json,re,subprocess,tempfile,html,shutil,hashlib
HERE=Path(__file__).resolve().parent;root=HERE.parents[2];ui=HERE/'reference/ui';ui.mkdir(exist_ok=True)
files=['learning.js','learning.css','question-fields.js','prose-lists.js','mathjax-config.js','vendor/marked/marked.esm.js','vendor/dompurify/purify.min.js','vendor/mathjax/tex-svg.js']
for f in files:
 dest=ui/f;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(root/'ui'/f,dest)
shutil.copytree(root/'ui/vendor/mathjax',ui/'vendor/mathjax',dirs_exist_ok=True)
source=(ui/'learning.js').read_text()
def function(name):
 start=source.index('function '+name+'(');line=source[start:].split('\n',1)[0]
 if line.endswith('}'):return line
 end=source.index('\n}\n',start)+2;return source[start:end]
script="""import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
import {checkboxControl,freeInput,choiceIndicator,fieldFeedback,blankInput,richSelect,inlinePrompt} from './reference/ui/question-fields.js';
const typeset=()=>{};
const fieldLabel=key=>key, assetURL=value=>value.startsWith('/')?'file://'+value:'file:///media/jake/SSD/EDB/math/'+value;
"""+'\n'.join(function(n) for n in ['el','short','escapeHTML','markdown','answerValue','choiceOrder','fieldControl','collectResponses'])+r"""
try {
await MathJax.startup.promise;const rows=JSON.parse(document.querySelector('#data').textContent);let reports=[];
for(let {label,record} of rows){let q=record.question,a=document.createElement('article');a.dataset.label=label;let h=document.createElement('h2');h.textContent=label;a.append(h);
a.append(markdown(q[':question/problem']));let f=q[':question/answer-fields'][0];
let field={id:20,key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map((c,i)=>({id:100+i,type:c[':answer/type'],value:c[':answer/value']}))};
const form=document.createElement('form');form.append(fieldControl(field,false,q[':question/id']));a.append(form);
const solution=document.createElement('details');solution.open=true;let sh=document.createElement('summary');sh.textContent='Solution:';solution.append(sh,markdown(q[':question/worked-solution']||'Source solution absent.'));a.append(solution);
document.querySelector('main').append(a);for(let im of a.querySelectorAll('img'))im.loading='eager';
let controlChecks=[];for(let input of form.querySelectorAll('input[type=radio]')){input.click();input.dispatchEvent(new Event('change',{bubbles:true}));let response=collectResponses(form,[field]);controlChecks.push(response[0].choiceId===Number(input.value)&&form.querySelectorAll('input:checked').length===1);}
let before=[...MathJax.startup.document.math].length;await MathJax.typesetPromise([a]);let items=[...MathJax.startup.document.math].slice(before);
let errors=[...a.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent),svgs=[...a.querySelectorAll('mjx-container svg')];
reports.push({label,rendered_math:svgs.length,items:items.map(i=>({tex:i.math,tree:i.root.toString()})),errors,literal_dollars:a.innerText.includes('$'),empty_svg:svgs.filter(n=>!n.querySelector('path,use,text,rect,line,polygon')).length,horizontal_overflow:a.scrollWidth>a.clientWidth,control_checks:controlChecks,controls:a.querySelectorAll('input[type=radio]').length});
}
await new Promise(resolve=>setTimeout(resolve,1500));for(let report of reports){let article=[...document.querySelectorAll('article')].find(a=>a.dataset.label===report.label);report.images=[...article.querySelectorAll('img')].map(im=>({src:im.src,width:im.naturalWidth,height:im.naturalHeight}));report.horizontal_overflow=article.scrollWidth>article.clientWidth;}
let passed=reports.every(r=>r.rendered_math>0&&!r.errors.length&&!r.literal_dollars&&!r.empty_svg&&!r.horizontal_overflow&&r.images.length>0&&r.images.every(im=>im.width>0)&&r.controls===5&&r.control_checks.every(Boolean));
document.querySelector('#summary').textContent=JSON.stringify({passed,records:reports});document.title=passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});document.title='FAIL';}
"""
(HERE/'browser-player.js').write_text(script)
rows=json.loads((HERE/'review.json').read_text())
# Include changed normal semicircle canonical formatting explicitly.
import importlib.util
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rows.append({'label':'Canonical normal semicircle','record':g.generate('easy',template='semicircle',parameters={'r':5})})
(HERE/'visual-records.json').write_text(json.dumps(rows,indent=2)+'\n')
prefix='''<!doctype html><html><head><meta charset="utf-8"><title>Rendering</title><link rel="stylesheet" href="reference/ui/learning.css"><style>body{margin:20px;font:16px system-ui;color:#182537;background:white}article{max-width:820px;padding:18px;border:1px solid #ddd;margin:20px auto}h2{font-size:16px}img{max-width:100%;height:auto}#summary{display:none}.choices{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.choice{display:flex;align-items:center;border:1px solid #ddd}.choice .prose{flex:1}</style><script src="reference/ui/vendor/dompurify/purify.min.js"></script><script src="reference/ui/mathjax-config.js"></script><script defer src="reference/ui/vendor/mathjax/tex-svg.js"></script></head><body><pre id="summary">pending</pre><main></main><script type="application/json" id="data">'''
def page(rows):return prefix+json.dumps(rows,ensure_ascii=False)+'''</script><script type="module" src="browser-player.js"></script></body></html>'''
p=HERE/'browser-preview.html';p.write_text(page(rows));profile=tempfile.mkdtemp(prefix='kp62081-browser-',dir='/tmp');cmd=['/usr/bin/google-chrome','--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--user-data-dir='+profile,'--allow-file-access-from-files','--virtual-time-budget=15000','--window-size=1100,1800'];r=subprocess.run(cmd+['--dump-dom',p.as_uri()],capture_output=True,text=True,timeout=60);(HERE/'browser.log').write_text(r.stderr);(HERE/'browser-dom.html').write_text(r.stdout);m=re.search(r'<pre id="summary">(.*?)</pre>',r.stdout,re.S);assert m,r.stderr[-2000:];report=json.loads(html.unescape(m[1]));assert report['passed'],str(report)[:2500]
report['pipeline']='Exact current ui/learning.js Markdown, answerValue, choiceOrder, fieldControl, collectResponses; actual question-fields.js, marked, DOMPurify, MathJax; local fixture, no API calls.';report['source_hashes']={f:hashlib.sha256((ui/f).read_bytes()).hexdigest() for f in files};(HERE/'browser-rendering.json').write_text(json.dumps(report,indent=2)+'\n')
for i in [15,16,17]:
 p=HERE/f'visual-{i}.html';p.write_text(page([rows[i]]));subprocess.run(cmd+['--screenshot='+str(HERE/f'visual-{i}.png'),p.as_uri()],capture_output=True,timeout=60,check=True)
print(json.dumps({'passed':True,'records':len(rows),'radio_interactions':sum(len(r['control_checks']) for r in report['records']),'math':sum(r['rendered_math'] for r in report['records'])}))
