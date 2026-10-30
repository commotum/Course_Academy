"""Read-only player render: actual fields, CSS, MathLive, MathJax and modes."""
import functools,http.server,json,re,sys,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[4]
source=(R/'ui/learning.js').read_text();renderers=source[source.index('function markdown('):source.index('function loadMath(')]+source[source.index('function choiceOrder('):source.index('function collectResponses(')]
s=(R/'tests/matrix-overflow-browser.cjs').read_text();fixture=re.search(r'const html=`([\s\S]+?)`;\nconst profile=',s)[1].replace('${renderers}',renderers).replace(r'\\n',r'\n')
fixture=fixture.replace("img-src 'none'","img-src data:")
fixture=fixture.replace('<script src="/ui/vendor/mathjax/tex-svg.js">','<script>MathJax.tex.packages=MathJax.tex.packages.filter(n=>n!=="noundefined");</script><script src="/ui/vendor/mathjax/tex-svg.js">')
items=json.loads(Path(sys.argv[1]).read_text())
for item in items:
 assert len({f['key']for f in item['fields']})==len(item['fields']),('Duplicate active key',item['entity'])
 item['repaired']=False
output=Path(sys.argv[2]);checks=[]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
try:
 with sync_playwright()as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page(viewport={'width':760,'height':950});page.route(origin+'/fixture',lambda r:r.fulfill(body=fixture,content_type='text/html'));page.goto(origin+'/fixture');page.wait_for_function('window.ready')
  for width in[760,390,320]:
   page.set_viewport_size({'width':width,'height':950})
   for mode in['edit','correct','incorrect']:
    for offset in range(0,len(items),15):
     batch=items[offset:offset+15];result=page.evaluate('([xs,mode])=>window.renderBatch(xs,mode)',[batch,mode]);assert not result['exceptions'],result
     geometry=page.evaluate('''()=>[...main.children].map(article=>{const tables=[...article.querySelectorAll('.matrix-answer table')];return {entity:Number(article.dataset.entity),tables:tables.map(t=>({rows:t.rows.length,columns:[...t.rows].map(r=>r.cells.length),nested:!!t.querySelector('table'),scroll:t.scrollWidth>t.clientWidth+1,borders:[...t.querySelectorAll('td')].some(c=>getComputedStyle(c).borderTopWidth!=='0px')})),fieldKeys:[...article.querySelectorAll('.answer-inline')].map(n=>n.closest('[data-field-key]')?.dataset.fieldKey),disabled:[...article.querySelectorAll('math-field')].map(n=>n.disabled),unmounted:article.querySelector('.answer-fields')?.childElementCount||0}})''')
     for item,row,g in zip(batch,result['items'],geometry):
      row.update(width=width,mode=mode,geometry=g);assert not row['mathErrors'],row
      if item.get('repaired'):
       assert not row['overflow']and not row['contentOverflow'],row
       assert row['blankEditors']==sum(f['type']=='blank'for f in item['fields']),row
       assert g['unmounted']==0,row
       assert all(not t['nested']and not t['scroll']and not t['borders']for t in g['tables']),row
       assert len(g['tables'])==item.get('expected_tables',3),row
      checks.append(row)
     if width==760 and mode=='edit'and len(items)<=2:
      for i,item in enumerate(batch):page.locator('article').nth(i).screenshot(path=str(output.parent/(str(item['entity'])+'-760.png')))
  browser.close()
finally:server.shutdown();server.server_close()
report={'passed':True,'checks':checks,'actual_player_controls':True,'database_writes':0};output.write_text(json.dumps(report,indent=2)+'\n');print('Verified',len(items),'prompts in',len(checks),'width/mode cases')
