"""Actual frozen player Markdown/DOMPurify/MathJax pipeline, local browser QA."""
import functools,http.server,json,os,subprocess,sys,threading
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
try:from playwright.sync_api import sync_playwright
except ImportError:
 runtime=Path('/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10')
 if sys.version_info[:2]!=(3,10):subprocess.run([str(runtime),'-B',str(Path(__file__))],check=True);sys.exit(0)
 cache=Path('/home/jake/.cache/uv/wheels-v5/pypi')
 for package in('playwright','pyee','greenlet'):
  paths=[p for p in(cache/package).iterdir()if p.is_dir()and('cp310'in p.name and'manylinux'in p.name or'none-any'in p.name or package=='playwright'and'manylinux'in p.name)]
  sys.path.insert(0,str(sorted(paths)[-1]))
 from playwright.sync_api import sync_playwright
refs=json.loads((HERE/'reference/assets.json').read_text());assets={a['reference']:Path(a['local'])for a in refs}
records=[{'label':'source-'+str(i),'record':z['record']}for i,z in enumerate(json.loads((HERE/'source-cases.json').read_text()))]+json.loads((HERE/'review-cases.json').read_text())
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def translate_path(self,path):
  if path.startswith('/ui/'):return str(HERE/'reference/ui'/path[len('/ui/'):].split('?')[0])
  return super().translate_path(path)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin='http://127.0.0.1:'+str(server.server_port)
html=r'''<!doctype html><link rel="stylesheet" href="/ui/learning.css"><style>body{background:white;color:#182537;padding:18px}article{max-width:800px;margin:20px auto;padding:18px;border:1px solid #ddd}.bank{padding:8px 20px;border:1px solid #ddd}.prose img{max-width:520px;max-height:440px}h2{font:16px system-ui}</style><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script src="/ui/vendor/dompurify/purify.min.js"></script><div id="content"></div><script type="module">
import {marked}from'/ui/vendor/marked/marked.esm.js';import{romanLists}from'/ui/prose-lists.js';import{inlinePrompt}from'/ui/question-fields.js';function el(tag,className,text){let e=document.createElement(tag);if(className)e.className=className;if(text)e.textContent=text;return e;}const source=await(await fetch('/ui/learning.js')).text();const renderer=source.slice(source.indexOf('function escapeHTML('),source.indexOf('function answerValue('));const labels=source.slice(source.indexOf('function fieldLabel('),source.indexOf('\n}',source.indexOf('function fieldLabel('))+2);window.render=new Function('el','marked','romanLists','inlinePrompt',labels+';'+renderer+';return markdown;')(el,marked,romanLists,inlinePrompt);await MathJax.startup.promise;window.ready=true;</script>'''
def route(request):
 url=request.request.url
 if url==origin+'/fixture':return request.fulfill(body=html,content_type='text/html')
 if url.startswith(origin+'/api/asset?'):
  from urllib.parse import urlparse,parse_qs
  key=parse_qs(urlparse(url).query)['path'][0];path=assets.get(key,Path(key));assert path.is_relative_to(HERE)or str(path).startswith(str(HERE)),key
  return request.fulfill(body=path.read_bytes(),content_type='image/png')
 if url.startswith(origin+'/'):return request.continue_()
 return request.abort()
try:
 with sync_playwright()as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':1100,'height':1100});errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.route('**/*',route);page.goto(origin+'/fixture');page.wait_for_function('window.ready === true',timeout=20000)
  results=page.evaluate(r'''async records=>{let result=[];for(let{label,record}of records){let q=record.question,a=document.createElement('article');a.dataset.label=label;let h=document.createElement('h2');h.textContent=label;a.append(h);let prompt=render(q[':question/problem']);a.append(prompt);for(let f of q[':question/answer-fields']){let bank=document.createElement('div');bank.className='bank';for(let ans of f[':answer-field/choices']){bank.append(render(ans[':answer/value']));}a.append(bank);}let sol=render(q[':question/worked-solution']);a.append(sol);content.append(a);let before=[...MathJax.startup.document.math].length;await MathJax.typesetPromise([a]);let items=[...MathJax.startup.document.math].slice(before);let rows=[];for(let item of items)item.root.walkTree(n=>{if(n.kind==='mtable')rows.push({rows:n.childNodes.length,columns:n.childNodes[0].childNodes.length});});for(let im of a.querySelectorAll('img')){im.loading='eager';await im.decode();}result.push({label,math_items:items.map(i=>({tex:i.math,tree:i.root.toString()})),solution_tables:rows,image_sizes:[...a.querySelectorAll('img')].map(im=>[im.naturalWidth,im.naturalHeight]),errors:[...a.querySelectorAll('[data-mml-node="merror"],mjx-merror,.math-error')].map(e=>e.textContent),literal_dollars:a.innerText.includes('$'),horizontal_overflow:a.scrollWidth>a.clientWidth});}return result;}''',records)
  assert not errors,errors
  for row,src in zip(results,records):
   assert not row['errors']and not row['literal_dollars']and not row['horizontal_overflow'],row
   assert len(row['image_sizes'])==1 and min(row['image_sizes'][0])>0,row
   fields=src['record']['question'][':question/answer-fields']
   if fields[0][':answer-field/type'].endswith('/radio'):assert row['solution_tables']==[{'rows':3,'columns':2}]*3,row
   else:assert row['solution_tables']==[],row
  shots=HERE/'screenshots';shots.mkdir(exist_ok=True)
  for label in('source-2','source-3','easy-0','moderate-26','hard-52','controlled-easy-ABC','controlled-easy-BAC','controlled-moderate-BCA','controlled-hard-ACB'):
   article=page.locator('article[data-label="'+label+'"]')
   if article.count():article.screenshot(path=str(shots/(label+'.png')))
  (HERE/'browser-rendering.json').write_text(json.dumps({'pipeline':'frozen actual ui/learning.js markdown + marked + DOMPurify + mathjax-config.js + MathJax tex-svg','browser_version':browser.version,'records':results,'page_errors':errors,'screenshots':[str(p.relative_to(HERE))for p in shots.glob('*.png')]},indent=2)+'\n');browser.close();print('Browser rendered',len(results),'complete question/solution/bank records')
finally:server.shutdown();server.server_close()
