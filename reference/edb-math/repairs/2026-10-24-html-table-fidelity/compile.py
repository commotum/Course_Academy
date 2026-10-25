"""Compile safe source table HTML using current cell values and the real Markdown parser."""
import functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
def main():
 rows=json.loads((H/'matches.json').read_text());server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
 with sync_playwright()as p:
  browser=p.chromium.launch(headless=True);page=browser.new_page();page.goto(origin+'/');page.evaluate("async()=>window.sourceTable=(await import('/reference/edb-math/repairs/2026-10-24-html-table-fidelity/build-table.js')).sourceTable")
  for start in range(0,len(rows),100):
   chunk=rows[start:start+100];values=page.evaluate('rows=>rows.map(r=>{try{return sourceTable(r.source,r.prototype_rows)}catch(e){throw Error(r.entity+" "+r.attribute+" "+r.span+" "+e.message)}})',chunk)
   for r,v in zip(chunk,values):r['proposed_html']=v
  browser.close()
 server.shutdown();(H/'compiled.json').write_text(json.dumps(rows,indent=2)+'\n');print('Compiled source-backed tables',len(rows))
if __name__=='__main__':main()
