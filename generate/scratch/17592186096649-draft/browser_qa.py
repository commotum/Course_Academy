"""Frozen real player Markdown + DOMPurify + MathJax, file-local browser QA."""
from pathlib import Path
import json,re,subprocess,tempfile,html
HERE=Path(__file__).resolve().parent
source=(HERE/'reference/ui/learning.js').read_text();start=source.index('function markdown(');end=source.index('\n}\n',start)+2;pipeline=source[start:end]
script="""import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
const el=(tag,cls,text)=>{let n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n};
const short=value=>String(value||'').split('/').at(-1);
import {checkboxControl,freeInput,choiceIndicator,fieldFeedback,blankInput,richSelect,inlinePrompt} from './reference/ui/question-fields.js';
const typeset=()=>{};
const fieldLabel=key=>key, assetURL=value=>value.startsWith('generate/')?'file:///home/jake/Developer/Course_Academy/'+value:value.startsWith('/')?'file://'+value:'file:///media/jake/SSD/EDB/math/'+value;
const escapeHTML=text=>String(text).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'})[c]);
"""+pipeline+"\n"+source[source.index("function answerValue("):source.index("function loadMath(")]+"\n"+source[source.index("function choiceOrder("):source.index("function collectResponses(")]+r"""
try {
await MathJax.startup.promise;const rows=JSON.parse(document.querySelector('#data').textContent);let reports=[];
for(let {label,record} of rows){let q=record.question,a=document.createElement('article');a.dataset.label=label;let h=document.createElement('h2');h.textContent=label;a.append(h);
const inputs=[q[':question/problem'],q[':question/worked-solution']||'No solution captured.'];
let expected=0;for(let text of inputs){expected+=(text.match(/\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g)||[]).length;if(text===inputs[0])a.append(markdown(text));}
let f=q[':question/answer-fields'][0];if(f)a.append(fieldControl({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(c=>({id:c[':answer/id'],type:c[':answer/type'],value:c[':answer/value']}))},false,q[':question/id']));a.append(markdown(inputs[1],'prose worked-solution'));document.querySelector('main').append(a);for(let im of a.querySelectorAll('img'))im.loading='eager';let before=[...MathJax.startup.document.math].length;await MathJax.typesetPromise([a]);let items=[...MathJax.startup.document.math].slice(before);
let errors=[...a.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent),svgs=[...a.querySelectorAll('mjx-container svg')];
reports.push({label,expected_math:expected,rendered_math:svgs.length,items:items.map(i=>({tex:i.math,tree:i.root.toString()})),errors,literal_dollars:a.innerText.includes('$'),empty_svg:svgs.filter(n=>!n.querySelector('path,use,text,rect,line,polygon')).length,horizontal_overflow:a.scrollWidth>a.clientWidth,images:[...a.querySelectorAll('img')].map(im=>({src:im.src,width:im.naturalWidth,height:im.naturalHeight,display_width:im.getBoundingClientRect().width,display_height:im.getBoundingClientRect().height,role:im.closest('.choice')?'choice':'prose',content_width:im.getBoundingClientRect().width-parseFloat(getComputedStyle(im).borderLeftWidth)-parseFloat(getComputedStyle(im).borderRightWidth),content_height:im.getBoundingClientRect().height-parseFloat(getComputedStyle(im).borderTopWidth)-parseFloat(getComputedStyle(im).borderBottomWidth)}))});
}
await new Promise(resolve=>setTimeout(resolve,5000));for(let report of reports){let article=[...document.querySelectorAll('article')].find(a=>a.dataset.label===report.label);report.images=[...article.querySelectorAll('img')].map(im=>({src:im.src,width:im.naturalWidth,height:im.naturalHeight,display_width:im.getBoundingClientRect().width,display_height:im.getBoundingClientRect().height,role:im.closest('.choice')?'choice':'prose',content_width:im.getBoundingClientRect().width-parseFloat(getComputedStyle(im).borderLeftWidth)-parseFloat(getComputedStyle(im).borderRightWidth),content_height:im.getBoundingClientRect().height-parseFloat(getComputedStyle(im).borderTopWidth)-parseFloat(getComputedStyle(im).borderBottomWidth)}));report.horizontal_overflow=article.scrollWidth>article.clientWidth;}let passed=reports.every(r=>r.expected_math===r.rendered_math&&!r.errors.length&&!r.literal_dollars&&!r.empty_svg&&!r.horizontal_overflow&&r.images.every(im=>im.width>0));document.querySelector('#summary').textContent=JSON.stringify({passed,records:reports});document.title=passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});document.title='FAIL';}
"""
(HERE/'browser-player.js').write_text(script)
rows=json.loads((HERE/'visual-records.json').read_text())
htmlprefix='''<!doctype html><html><head><meta charset="utf-8"><title>Rendering</title><link rel="stylesheet" href="reference/ui/navigation.css"><link rel="stylesheet" href="reference/ui/learning.css"><style>body{margin:20px;font:16px system-ui;color:#182537;background:white}article{max-width:820px;padding:18px;border:1px solid #ddd;margin:20px auto}h2{font-size:16px}img{max-width:100%;height:auto}#summary{display:none}</style><script src="reference/ui/vendor/dompurify/purify.min.js"></script><script src="reference/ui/mathjax-config.js"></script><script defer src="reference/ui/vendor/mathjax/tex-svg.js"></script></head><body><pre id="summary">pending</pre><main></main><script type="application/json" id="data">'''
path=HERE/'browser-preview.html';path.write_text(htmlprefix+json.dumps(rows,ensure_ascii=False)+'''</script><script type="module" src="browser-player.js"></script></body></html>''')
profile=tempfile.mkdtemp(prefix='kp96649-browser-',dir='/tmp')
cmd=['/usr/bin/google-chrome','--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--user-data-dir='+profile,'--allow-file-access-from-files','--virtual-time-budget=45000','--window-size=1100,1800']
r=subprocess.run(cmd+['--dump-dom',path.as_uri()],capture_output=True,text=True,timeout=60);(HERE/'browser.log').write_text(r.stderr)
(HERE/'browser-dom.html').write_text(r.stdout)
m=re.search(r'<pre id="summary">(.*?)</pre>',r.stdout,re.S);assert m, r.stderr[-2000:]
report=json.loads(html.unescape(m[1]));assert report['passed'],str(report)[:2000]
report['pipeline']='frozen actual ui/learning.js Markdown, marked, DOMPurify, MathJax3 tex-svg';report['network_reads']=0
scalechecks=[]
for record in report['records']:
 if not (record['label'].startswith('authored ') or record['label'].startswith('repaired existing ')):continue
 units=[]
 for im in record['images']:
  assert im['width']==im['height']==180 and abs(im['content_width']-180)<1e-6 and abs(im['content_height']-180)<1e-6, im
  from urllib.parse import urlparse,unquote
  imagepath=Path(unquote(urlparse(im['src']).path));spec=json.loads(imagepath.with_suffix('.json').read_text())['spec'];units.append(180*.94/(spec['bounds'][0][1]-spec['bounds'][0][0]))
 assert max(units)-min(units)<1e-8,(record['label'],units)
 scalechecks.append({'label':record['label'],'prompt_and_all_options_natural_180px':True,'all_actual_content_sizes_px':[im['content_width'] for im in record['images']],'shared_actual_pixels_per_unit':units[0]})
assert len(scalechecks)==21
report['uniform_display_scale_checks']=scalechecks
(HERE/'browser-rendering.json').write_text(json.dumps(report,indent=2)+'\n')
# First three review records are easy two directions and moderate first direction.
# Screenshot signed-rational and signed-surd examples on separate isolated pages.
for index in (0,2,4,5):
 selected=[rows[index]];shot=HERE/('review-'+str(index)+'.png');page=HERE/('visual-'+str(index)+'.html');page.write_text(htmlprefix+json.dumps(selected,ensure_ascii=False)+'''</script><script type="module" src="browser-player.js"></script></body></html>''')
 subprocess.run(cmd+['--screenshot='+str(shot),page.as_uri()],capture_output=True,timeout=60,check=True)
print('Rendered',len(rows),'complete records;',sum(r['rendered_math'] for r in report['records']),'math expressions; no errors or overflow.')
