import json
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
repo=Path('/home/jake/Developer/Course_Academy');vendor=repo/'ui/vendor/mathjax';results=[];requests=[]
expressions=[r'\bbox[2pt,lightgray]{\color{blue}{\phantom{D^{-1}}}}',r'\bbox[3pt,border:1pt solid black]{\phantom{AAAAAA}}',r'\boxed{\phantom{AAAAAA}}',r'\colorbox{lightgray}{$\phantom{D^{-1}}$}']
with sync_playwright() as pw:
 browser=pw.chromium.launch(headless=True)
 for tex in expressions:
  context=browser.new_context()
  def route(r):
   path=urlparse(r.request.url).path
   if r.request.url=='http://offline.local/':r.fulfill(body='<html><body></body></html>',content_type='text/html');return
   relative=path.removeprefix('/ui/vendor/mathjax/');local=vendor/relative
   if path.startswith('/ui/vendor/mathjax/') and local.is_file():requests.append({'path':path,'local':True});r.fulfill(path=str(local),content_type='application/javascript')
   else:requests.append({'path':path,'local':False});r.fulfill(status=404,body='Unavailable local asset')
  context.route('**/*',route);page=context.new_page();page.goto('http://offline.local/');page.evaluate('window.MathJax={startup:{typeset:false}}');page.add_script_tag(url='http://offline.local/ui/vendor/mathjax/tex-svg.js')
  try:
   data=page.evaluate('''async tex=>{await MathJax.startup.promise;const node=await MathJax.tex2svgPromise(tex);document.body.append(node);return{errors:node.querySelectorAll('[data-mml-node="merror"]').length,svg:node.querySelector('svg')?.outerHTML,backgroundRects:[...node.querySelectorAll('rect')].map(n=>({fill:n.getAttribute('fill'),stroke:n.getAttribute('stroke'),width:n.getAttribute('width'),height:n.getAttribute('height')})),phantoms:node.querySelectorAll('[data-mml-node="mphantom"]').length,visibleGlyphs:node.querySelectorAll('use').length};}''',tex)
   results.append({'tex':tex,**data})
  except Exception as error:results.append({'tex':tex,'exception':str(error)})
  context.close()
 browser.close()
report={'results':results,'requests':requests,'ui_files_changed':False,'network':'Only exact local repo vendor bytes; all other requests answered404 offline'};Path('/tmp/boxed-phantom-ui-design-proof-origin.json').write_text(json.dumps(report,indent=2));print(json.dumps({'results':[{k:v for k,v in r.items() if k!='svg'} for r in results],'requests':requests},indent=2))
