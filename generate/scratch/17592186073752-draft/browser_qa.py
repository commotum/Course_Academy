"""Frozen real player Markdown + DOMPurify + MathJax, file-local browser QA."""
from pathlib import Path
import json,re,subprocess,tempfile,html
HERE=Path(__file__).resolve().parent
source=(HERE/'reference/ui/learning.js').read_text();start=source.index('function markdown(');end=source.index('\n}\n',start)+2;pipeline=source[start:end]
script="""import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
const el=(tag,cls,text)=>{let n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n};
const short=value=>String(value||'').split('/').at(-1);
import {checkboxControl,freeInput,choiceIndicator,fieldFeedback,blankInput,richSelect,inlinePrompt,mountInlineFields} from './reference/ui/question-fields.js';
import {MathfieldElement} from './reference/ui/vendor/mathlive/mathlive.min.mjs';
MathfieldElement.fontsDirectory=new URL('./reference/ui/vendor/mathlive/fonts',import.meta.url).href;MathfieldElement.soundsDirectory=null;
const typeset=()=>{};
const fieldLabel=key=>key, assetURL=value=>value.startsWith('generate/')?'file:///home/jake/Developer/Course_Academy/'+value:value.startsWith('/')?'file://'+value:'file:///media/jake/SSD/EDB/math/'+value;
const escapeHTML=text=>String(text).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'})[c]);
"""+pipeline+"\n"+source[source.index("function answerValue("):source.index("function loadMath(")]+"\n"+source[source.index("function choiceOrder("):source.index("function collectResponses(")]+r"""
try {
await MathJax.startup.promise;const rows=JSON.parse(document.querySelector('#data').textContent);let reports=[];
for(let {label,record} of rows){let q=record.question,a=document.createElement('article');a.dataset.label=label;let h=document.createElement('h2');h.textContent=label;a.append(h);
const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],answerType:':answer.type/math',choices:f[':answer-field/choices'].map(c=>({id:c[':answer/id'],type:c[':answer/type'],value:c[':answer/value']}))}));
const inputs=[q[':question/problem'],q[':question/worked-solution']||'No solution captured.'];
let expected=inputs.reduce((n,text)=>n+(text.match(/\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g)||[]).length,0);
let problem=markdown(inputs[0],'prose',fields);a.append(problem);let fieldList=document.createElement('div');a.append(fieldList);mountInlineFields(problem,fieldList,fields,f=>fieldControl(f,false,q[':question/id']));
for(let f of fields){if(f.type.endsWith('/radio'))expected+=f.choices.length;else {let key=document.createElement('div');key.append(document.createTextNode('Review key '+f.key+': '),answerValue(f.choices[0]));a.append(key);expected++;}}a.append(markdown(inputs[1]));
document.querySelector('main').append(a);for(let im of a.querySelectorAll('img'))im.loading='eager';let before=[...MathJax.startup.document.math].length;await MathJax.typesetPromise([a]);let items=[...MathJax.startup.document.math].slice(before);
let errors=[...a.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error,mjx-container [fill="red"],mjx-container [stroke="red"],mjx-container [data-mjx-error]')].map(n=>n.textContent),svgs=[...a.querySelectorAll('mjx-container svg')];
reports.push({label,expected_math:expected,rendered_math:svgs.length,items:items.map(i=>({tex:i.math,tree:i.root.toString()})),errors,literal_dollars:a.innerText.includes('$'),spacing_only_svg:items.filter(i=>/^(?:\\[,;! ]|\s)*$/.test(i.math)).length,empty_svg:svgs.filter((n,i)=>!n.querySelector('path,use,text,rect,line,polygon')&&!/^(?:\\[,;! ]|\s)*$/.test(items[i]?.math||'')).length,horizontal_overflow:a.scrollWidth>a.clientWidth,images:[...a.querySelectorAll('img')].map(im=>({src:im.src,width:im.naturalWidth,height:im.naturalHeight,display_width:im.getBoundingClientRect().width,display_height:im.getBoundingClientRect().height,role:im.closest('.choice')?'choice':'prose',content_width:im.getBoundingClientRect().width-parseFloat(getComputedStyle(im).borderLeftWidth)-parseFloat(getComputedStyle(im).borderRightWidth),content_height:im.getBoundingClientRect().height-parseFloat(getComputedStyle(im).borderTopWidth)-parseFloat(getComputedStyle(im).borderBottomWidth)}))});
}
await new Promise(resolve=>setTimeout(resolve,5000));for(let report of reports){let article=[...document.querySelectorAll('article')].find(a=>a.dataset.label===report.label);report.images=[...article.querySelectorAll('img')].map(im=>({src:im.src,width:im.naturalWidth,height:im.naturalHeight,display_width:im.getBoundingClientRect().width,display_height:im.getBoundingClientRect().height,role:im.closest('.choice')?'choice':'prose',content_width:im.getBoundingClientRect().width-parseFloat(getComputedStyle(im).borderLeftWidth)-parseFloat(getComputedStyle(im).borderRightWidth),content_height:im.getBoundingClientRect().height-parseFloat(getComputedStyle(im).borderTopWidth)-parseFloat(getComputedStyle(im).borderBottomWidth)}));report.horizontal_overflow=article.scrollWidth>article.clientWidth;}let passed=reports.every(r=>r.expected_math===r.rendered_math&&!r.errors.length&&!r.literal_dollars&&!r.empty_svg&&!r.horizontal_overflow&&r.images.every(im=>im.width>0));document.querySelector('#summary').textContent=JSON.stringify({passed,records:reports});document.title=passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});document.title='FAIL';}
"""
(HERE/'browser-player.js').write_text(script)
rows=json.loads((HERE/'visual-records.json').read_text())
htmlprefix='''<!doctype html><html><head><meta charset="utf-8"><title>Rendering</title><link rel="stylesheet" href="reference/ui/navigation.css"><link rel="stylesheet" href="reference/ui/learning.css"><style>body{margin:20px;font:16px system-ui;color:#182537;background:white}article{max-width:820px;padding:18px;border:1px solid #ddd;margin:20px auto}h2{font-size:16px}math-field.answer-math{background:#f7f9fc;color:#182537;border:1px solid #b7c3d1;color-scheme:light}img{max-width:100%;height:auto}#summary{display:none}</style><script src="reference/ui/vendor/dompurify/purify.min.js"></script><script src="reference/ui/mathjax-config.js"></script><script defer src="reference/ui/vendor/mathjax/tex-svg.js"></script></head><body><pre id="summary">pending</pre><main></main><script type="application/json" id="data">'''
path=HERE/'browser-preview.html';path.write_text(htmlprefix+json.dumps(rows,ensure_ascii=False)+'''</script><script type="module" src="browser-player.js"></script></body></html>''')
profile=tempfile.mkdtemp(prefix='kp73752-browser-',dir='/tmp')
cmd=['/usr/bin/google-chrome','--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--user-data-dir='+profile,'--allow-file-access-from-files','--virtual-time-budget=45000','--window-size=1100,1800']
r=subprocess.run(cmd+['--dump-dom',path.as_uri()],capture_output=True,text=True,timeout=60);(HERE/'browser.log').write_text(r.stderr)
(HERE/'browser-dom.html').write_text(r.stdout)
m=re.search(r'<pre id="summary">(.*?)</pre>',r.stdout,re.S);assert m, r.stderr[-2000:]
report=json.loads(html.unescape(m[1]));assert report['passed'],str(report)[:2000]
report['pipeline']='frozen actual ui/learning.js Markdown, marked, DOMPurify, MathJax3 tex-svg';report['network_reads']=0
(HERE/'browser-rendering.json').write_text(json.dumps(report,indent=2)+'\n')
# Source-template and generated-variant screenshots include every operative chain.
for index in (0,1,2,3,5,6,7,8,9,10,12,14,16,18,20,22,24,26,28):
 selected=[rows[index]];shot=HERE/('review-'+str(index)+'.png');page=HERE/('visual-'+str(index)+'.html');page.write_text(htmlprefix+json.dumps(selected,ensure_ascii=False)+'''</script><script type="module" src="browser-player.js"></script></body></html>''')
 subprocess.run(cmd+['--screenshot='+str(shot),page.as_uri()],capture_output=True,timeout=60,check=True)
print('Rendered',len(rows),'complete records;',sum(r['rendered_math'] for r in report['records']),'math expressions; no errors or overflow.')
