"""Render recovery candidates with the application's MathJax and match SVG trees."""
import functools,http.server,json,threading,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];RAW=ROOT/'.local/edb/math-image-import-audit-2026-10-22'
def save(path,v):path.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
JS=r'''html=>{
 const doc=new DOMParser().parseFromString(html,'text/html');
 const math=doc.querySelector('svg [data-mml-node="math"]');
 if(!math)return null;
 const roles=new Set(['mfrac','msup','msub','msubsup','munder','mover','munderover','msqrt','mroot','mtable','mtr','mtd','menclose']);
 const leaves=new Set(['mi','mn','mo','mtext','ms','text']);
 const stretchy={'239B':'28','239C':'28','239D':'28','239E':'29','239F':'29','23A0':'29','23A1':'5B','23A2':'5B','23A3':'5B','23A4':'5D','23A5':'5D','23A6':'5D','23A7':'7B','23A8':'7B','23A9':'7B','23AA':'7B','23AB':'7D','23AC':'7D','23AD':'7D','23B7':'221A','E001':'221A'};
 function color(n){while(n&&n!==math.parentElement){let c=n.getAttribute('fill')||n.getAttribute('color')||n.getAttribute('stroke');if(c&&!['currentColor','none','black','#000','#000000','inherit'].includes(c))return c.toLowerCase();n=n.parentElement}return ''}
 function go(n){
  const k=n.getAttribute('data-mml-node');
  if(leaves.has(k)){
   // A clipped minus path extends one arrow operator. Preserve that fact
   // instead of accepting an overset containing two separate operators.
   const pieces=[...n.querySelectorAll('path[data-c],use[data-c]')];
   if(k==='mo'&&pieces.length===2&&pieces[0].getAttribute('data-c')==='2192'&&pieces[1].getAttribute('data-c')==='2212'&&
      pieces[0].parentElement===n&&pieces[1].parentElement.localName==='svg'&&pieces[1].parentElement.parentElement===n&&pieces[1].parentElement.hasAttribute('viewBox'))
     return ['2192:'+color(n)];
   const vals=[...n.querySelectorAll('path[data-c],use[data-c]')].filter(x=>!x.closest('defs')).map(x=>[(stretchy[x.getAttribute('data-c')]||x.getAttribute('data-c')).toUpperCase(),color(x)]);
   if(!vals.length){for(const t of n.querySelectorAll('text'))for(const c of t.textContent)vals.push([c.codePointAt(0).toString(16).toUpperCase(),color(t)])}
   if(vals.length&&vals.every(([c])=>parseInt(c,16)>=0xE150&&parseInt(c,16)<=0xE156))return [(n.parentElement.getAttribute('data-mml-node')==='munder'?'23DF':'23DE')+':'+color(n)];
   const out=[];for(let [c,col] of vals){if(['20','A0','200B','2061','2062','2063','2064'].includes(c))continue;const v=c+':'+col;out.push(v)}
   // Stretchy delimiters consist of repeated pieces of the same fence.
   if(out.length>1&&out.every(x=>x===out[0])&&['28','29','5B','5D','7B','7D','7C','2016'].includes(out[0].split(':')[0]))return [out[0]];
   return out;
  }
  let kids=[...n.children].filter(x=>!['defs','title'].includes(x.localName));
  if(k==='munderover'&&kids.length===3){const y=n=>+(n.getAttribute('transform')?.match(/translate\([^, )]+[, ]+([-\d.]+)/)?.[1]||0);kids=[kids[0],...kids.slice(1).sort((a,b)=>y(a)-y(b))]}
  const bg=kids.find(x=>x.hasAttribute('data-bgcolor'));
  if(bg)return [{k:'background',color:bg.getAttribute('fill').toLowerCase(),c:kids.filter(x=>x!==bg).flatMap(go)}];
  if(roles.has(k))return [{k,c:kids.filter(x=>x.localName==='g'||x.hasAttribute('data-mml-node')).map(x=>go(x)),
     rules:k==='menclose'?[...n.querySelectorAll('line')].map(x=>Math.sign((+x.getAttribute('x2')- +x.getAttribute('x1'))*(+x.getAttribute('y2')- +x.getAttribute('y1')))):undefined}];
  return kids.flatMap(go);
 }
 return JSON.stringify(go(math));
}'''
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass

def main():
 source=json.loads((RAW/'repair-source-svgs.json').read_text());candidates=json.loads((RAW/'repair-candidates.json').read_text())
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
 fixture=(ROOT/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text()
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,timeout=15000);page=browser.new_page()
  page.route('**/*',lambda route:route.fulfill(body=fixture,content_type='text/html') if route.request.url==origin+'/fixture' else route.continue_() if route.request.url.startswith(origin+'/') else route.abort())
  page.goto(origin+'/fixture');page.wait_for_function('window.ready === true',timeout=20000);page.evaluate('() => {window.fingerprint='+JS+';}')
  targets={}
  for i in range(0,len(source),100):
   targets.update(page.evaluate('rows=>Object.fromEntries(rows.map(([p,s])=>[p,fingerprint(s)]))',list(source.items())[i:i+100]))
  save(RAW/'repair-target-fingerprints.json',targets)
  existing=RAW/'repair-rendered-candidates.jsonl';done=[]
  if existing.exists():done=list(map(json.loads,existing.open()))
  assert all(r['tex']==candidates[i]['tex'] for i,r in enumerate(done))
  with existing.open('a') as stream:
   for i in range(len(done),len(candidates),100):
    batch=candidates[i:i+100]
    results=page.evaluate('''async rows=>{const out=[];for(const r of rows){try{const n=await MathJax.tex2svgPromise(r.tex,{display:true});out.push({tex:r.tex,fp:fingerprint(n.outerHTML),errors:[...n.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.textContent)})}catch(e){out.push({tex:r.tex,error:String(e)})}}return out}''',batch)
    for r in results:stream.write(json.dumps(r,ensure_ascii=False)+'\n')
    stream.flush();done.extend(results)
    if i%1000==0:print('rendered',len(done),'/',len(candidates),flush=True)
  matches={};index={}
  for i,r in enumerate(done):
   if r.get('fp') and not r.get('errors') and not r.get('error'):index.setdefault(r['fp'],[]).append(i)
  for path,fp in targets.items():
   if fp and fp in index:
    ids=index[fp];best=min(ids,key=lambda i:len(candidates[i]['tex']));matches[path]={'tex':candidates[best]['tex'],'method':'rendered-structure-match','evidence':candidates[best]['evidence'],'matching_candidates':len(ids)}
  save(HERE/'matched-recoveries.json',matches);save(HERE/'unmatched-assets.json',[p for p in targets if p not in matches])
  print(json.dumps({'targets':len(targets),'matched':len(matches),'unmatched':len(targets)-len(matches),'render_errors':sum(bool(r.get('errors') or r.get('error')) for r in done)}))
  browser.close()
 server.shutdown()
if __name__=='__main__':main()
