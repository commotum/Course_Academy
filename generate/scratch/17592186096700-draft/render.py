"""Actual player markdown/sanitization/math/checkbox controls and loaded PNGs."""
import functools,http.server,json,threading,re,hashlib,urllib.parse,shutil
from pathlib import Path
import subprocess
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
source=(ROOT/'ui/learning.js').read_text()
parts=[source[source.index('function el('):source.index('function button(')],source[source.index('function fieldLabel('):source.index('function fieldLabel(')+source[source.index('function fieldLabel('):].index('\n}')+2],source[source.index('function escapeHTML('):source.index('function loadMath()')]]
js="import { marked } from '/ui/vendor/marked/marked.esm.js';\nimport { romanLists } from '/ui/prose-lists.js';\nimport { inlinePrompt,checkboxControl } from '/ui/question-fields.js';\nconst short=x=>String(x).replace(/^:/,'').split('/').pop();\n"+'\n'.join(parts)+r'''
window.renderRecord=async record=>{
 await MathJax.startup.promise; MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map((f,i)=>({id:20+i,key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map((a,j)=>({id:100+i*2+j,type:a[':answer/type'],value:a[':answer/value']}))}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 for(const f of fields){const control=checkboxControl(f,label=>answerValue({type:'text',value:label}),false);document.body.append(control);}
 document.body.append(markdown(q[':question/worked-solution'],'prose solution'));
 for(const image of document.querySelectorAll('img'))image.loading='eager';
 const images=await Promise.all([...document.querySelectorAll('img')].map(async img=>{await img.decode();return {source:img.src,width:img.naturalWidth,height:img.naturalHeight,loaded:img.complete&&img.naturalWidth>0}}));
 await MathJax.typesetPromise([document.body]);
 const tables=[];for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});});
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container').forEach(n=>n.remove());
 return {errors:document.querySelectorAll('[data-mml-node="merror"],.math-error,mjx-container [fill="red"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,blanks:prompt.querySelectorAll('[data-field-key]').length,checkboxes:document.querySelectorAll('input[type="checkbox"]').length,images,overflow:[...document.querySelectorAll('mjx-container,img')].some(n=>n.getBoundingClientRect().width>1050)};
};
'''
(D/'render-harness.js').write_text(js)
(D/'render-harness.html').write_text('<html data-theme="light"><head><meta charset="utf-8"><link rel="stylesheet" href="/ui/navigation.css"><link rel="stylesheet" href="/ui/learning.css"><style>body{max-width:1000px;margin:32px auto;background:white;color:#222;padding:20px}.choice{padding:4px 0}.prose{margin-bottom:12px}</style><script src="/ui/vendor/dompurify/purify.min.js"></script><script src="/ui/mathjax-config.js"></script><script src="/ui/vendor/mathjax/tex-svg.js"></script><script type="module" src="render-harness.js"></script></head><body></body></html>')
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path.startswith('/api/asset?'):
   path=urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)['path'][0];p=Path(path)
   if not p.is_absolute():p=Path('/media/jake/SSD/EDB/math')/p
   data=p.read_bytes();self.send_response(200);self.send_header('Content-Type','image/png');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
  return super().do_GET()
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}'
records=json.loads((D/'review.json').read_text())
# Each screenshot role includes current original, legacy inventory, changed targets,
# both masks, all levels, both signs and fractional factors in full visual pages.
for i,r in enumerate(records):
 gen=r['generation'];p=gen['parameters'];level=r['question'].get(':question/difficulty','unrated').split('/')[-1]
 gen['template']=('source-'+gen['bank_profile'] if gen['evidence_only'] else level+'-'+gen['template']+'-'+('targets-'+''.join(p['targets']['primary'])+'-'+''.join(p['targets']['secondary']) if 'targets' in p else 'legacy'))
for r in records:
 if r['question'][':question/id']=='8a82f548-82f9-5e2c-9cd1-94b0a2a7a9d0':r['generation']['template']+='-tex-repair'
(D/'render-records.json').write_text(json.dumps(records)+'\n')
try:subprocess.run(['node',str(D/'render-cdp.js'),origin,str(D.relative_to(ROOT))],cwd=ROOT,check=True)
finally:server.shutdown();server.server_close()
report=json.loads((D/'render-report.json').read_text());report['ui_source_hashes']={str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in (ROOT/'ui/learning.js',ROOT/'ui/question-fields.js',ROOT/'ui/mathjax-config.js',ROOT/'ui/prose-lists.js')};(D/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
