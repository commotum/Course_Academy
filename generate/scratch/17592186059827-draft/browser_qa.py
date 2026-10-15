"""Frozen real player Markdown + DOMPurify + MathJax, file-local browser QA."""
from pathlib import Path
import json,re,subprocess,tempfile,html
HERE=Path(__file__).resolve().parent
source=(HERE/'reference/ui/learning.js').read_text();start=source.index('function markdown(');end=source.index('\n}\n',start)+2;pipeline=source[start:end]
script="""import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
const el=(tag,cls)=>{let n=document.createElement(tag);n.className=cls;return n};
const inlinePrompt=value=>value, fieldLabel=key=>key, assetURL=value=>value;
const escapeHTML=text=>String(text).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'})[c]);
"""+pipeline+r"""
try {
await MathJax.startup.promise;const rows=JSON.parse(document.querySelector('#data').textContent);let reports=[];
for(let {label,record} of rows){let q=record.question,a=document.createElement('article');a.dataset.label=label;let h=document.createElement('h2');h.textContent=label;a.append(h);
const inputs=[q[':question/problem'],...q[':question/answer-fields'][0][':answer-field/choices'].map(x=>'$'+x[':answer/value']+'$'),q[':question/worked-solution']||'No solution captured.'];
let expected=0;for(let text of inputs){expected+=(text.match(/\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g)||[]).length;a.append(markdown(text));}
document.querySelector('main').append(a);let before=[...MathJax.startup.document.math].length;await MathJax.typesetPromise([a]);let items=[...MathJax.startup.document.math].slice(before);
let errors=[...a.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent),svgs=[...a.querySelectorAll('mjx-container svg')];
reports.push({label,expected_math:expected,rendered_math:svgs.length,items:items.map(i=>({tex:i.math,tree:i.root.toString()})),errors,literal_dollars:a.innerText.includes('$'),empty_svg:svgs.filter(n=>!n.querySelector('path,use,text,rect,line,polygon')).length,horizontal_overflow:a.scrollWidth>a.clientWidth});
}
let passed=reports.every(r=>r.expected_math===r.rendered_math&&!r.errors.length&&!r.literal_dollars&&!r.empty_svg&&!r.horizontal_overflow);document.querySelector('#summary').textContent=JSON.stringify({passed,records:reports});document.title=passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});document.title='FAIL';}
"""
(HERE/'browser-player.js').write_text(script)
fixtures=json.loads((HERE/'source-cases.json').read_text());review=json.loads((HERE/'review.json').read_text());variants=json.loads((HERE/'variants.json').read_text())
rows=[{'label':'original-'+f['source_id'],'record':f['record']} for f in fixtures]+[{'label':'review-'+str(i),'record':r} for i,r in enumerate(review['variants'])]+[{'label':'role-'+str(i),'record':r} for i,r in enumerate(variants['same_endpoint_roles'])]
htmlprefix='''<!doctype html><html><head><meta charset="utf-8"><title>Rendering</title><style>body{margin:20px;font:16px system-ui;color:#182537;background:white}article{max-width:820px;padding:18px;border:1px solid #ddd;margin:20px auto}h2{font-size:16px}#summary{display:none}</style><script src="reference/ui/vendor/dompurify/purify.min.js"></script><script src="reference/ui/mathjax-config.js"></script><script defer src="reference/ui/vendor/mathjax/tex-svg.js"></script></head><body><pre id="summary">pending</pre><main></main><script type="application/json" id="data">'''
path=HERE/'browser-preview.html';path.write_text(htmlprefix+json.dumps(rows,ensure_ascii=False)+'''</script><script type="module" src="browser-player.js"></script></body></html>''')
profile=tempfile.mkdtemp(prefix='kp59827-browser-',dir='/tmp')
cmd=['/usr/bin/google-chrome','--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--user-data-dir='+profile,'--allow-file-access-from-files','--virtual-time-budget=45000','--window-size=1100,1800']
r=subprocess.run(cmd+['--dump-dom',path.as_uri()],capture_output=True,text=True,timeout=60);(HERE/'browser.log').write_text(r.stderr)
m=re.search(r'<pre id="summary">(.*?)</pre>',r.stdout,re.S);assert m, r.stderr[-2000:]
report=json.loads(html.unescape(m[1]));assert report['passed'],str(report)[:2000]
report['pipeline']='frozen actual ui/learning.js Markdown, marked, DOMPurify, MathJax3 tex-svg';report['network_reads']=0
(HERE/'browser-rendering.json').write_text(json.dumps(report,indent=2)+'\n')
# First three review records are easy two directions and moderate first direction.
# Screenshot signed-rational and signed-surd examples on separate isolated pages.
for index in (2,5):
 selected=[{'label':'review-'+str(index),'record':review['variants'][index]}];shot=HERE/('review-'+str(index)+'.png');page=HERE/('visual-'+str(index)+'.html');page.write_text(htmlprefix+json.dumps(selected,ensure_ascii=False)+'''</script><script type="module" src="browser-player.js"></script></body></html>''')
 subprocess.run(cmd+['--screenshot='+str(shot),page.as_uri()],capture_output=True,timeout=60,check=True)
print('Rendered',len(rows),'complete records;',sum(r['rendered_math'] for r in report['records']),'math expressions; no errors or overflow.')
