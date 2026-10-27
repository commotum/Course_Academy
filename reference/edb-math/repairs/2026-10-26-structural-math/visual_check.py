import functools,http.server,json,threading,sys,re
from pathlib import Path
from playwright.sync_api import sync_playwright
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import MATH,ENV,environment,cells
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
first={};final={}
for name in ['fields.json','batch-02/fields.json','batch-03/fields.json']:
 for f in json.loads((H/name).read_text()):
  k=f['entity'],f['attribute'];first.setdefault(k,f['before']);final[k]=f
samples=[]
def choose(e,a,name,needle):
 k=e,a;old=list(MATH.finditer(first[k]));new=list(MATH.finditer(final[k]['after']));i=next(i for i,m in enumerate(old)if needle in m[0]);assert len(old)==len(new);samples.append({'entity':e,'name':name,'before':old[i][0],'after':new[i][0]})
choose(17592186105571,'question/worked-solution','Sign chart: source grid restored',r'\begin{aligned}x &')
choose(17592186068485,'question/worked-solution','Parallel equations: false matrix removed',r'\begin{bmatrix}')
k=17592186052582,'answer/value';samples.append({'entity':k[0],'name':'Absolute values: false determinant removed','before':'$$'+first[k]+'$$','after':'$$'+final[k]['after']+'$$'})
choose(17592186233511,'question/problem','Piecewise function: visible cases brace',r'f(x)={')
f=next(f for f in json.loads((H/'batch-02/fields.json').read_text())if f['attribute']=='question/problem'and'{lim}'in f['before']and'standalone-limit-display'in f['reasons']and f['before'].count('$')==2)
samples.append({'entity':f['entity'],'name':'Limit operator and standalone display','before':f['before'],'after':f['after']})
d=next(d for d in json.loads((H/'reviewed-edits.json').read_text())if d.get('zero_rule_stacks_recovered',0)>0);new=d['after'];m=next(ENV.finditer(new));span=environment(new,m.start());body=re.sub(r'^\{[^{}]*\}','',new[span[0]:span[1]]);g=cells(body);cell=next(c for row in g for c in row if r'\genfrac' in c);samples.append({'entity':d['e'],'name':'Zero-rule stack: source binomial notation','before':'$$'+cell.replace(r'\genfrac{}{}{0pt}{}',r'\frac')+'$$','after':'$$'+cell+'$$'})
fixture=(R/'reference/mathacademy/repairs/2026-10-14-study-backlog/renderer-fixture.html').read_text();server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(R)));threading.Thread(target=server.serve_forever,daemon=True).start();origin=f'http://127.0.0.1:{server.server_port}';report=[]
with sync_playwright()as p:
 b=p.chromium.launch(headless=True);page=b.new_page(viewport={'width':1200,'height':1900});page.route('**/*',lambda r:r.fulfill(body=fixture,content_type='text/html')if r.request.url==origin+'/fixture'else r.continue_()if r.request.url.startswith(origin+'/')else r.abort());page.goto(origin+'/fixture');page.wait_for_function('window.ready===true')
 report=page.evaluate('''async rows=>{content.style.display='grid';content.style.gridTemplateColumns='minmax(0,1fr) minmax(0,1fr)';content.style.gap='16px';const out=[];for(const row of rows){for(const side of ['before','after']){const box=document.createElement('section');box.style.padding='14px';box.style.border='1px solid #ccc';box.style.minWidth='0';const title=document.createElement('p');title.textContent=row.name+' — '+side;box.append(title,render(row[side]));content.append(box);await MathJax.typesetPromise([box]);out.push({entity:row.entity,name:row.name,side,errors:[...box.querySelectorAll('[data-mml-node="merror"]')].map(n=>n.getAttribute('data-mjx-error'))});}}return out}''',samples);page.locator('#content').screenshot(path=str(H/'structural-before-after.png'));b.close()
server.shutdown();assert all(not r['errors']for r in report if r['side']=='after');(H/'visual-verification.json').write_text(json.dumps(report,indent=2)+'\n');print('Visually reviewable comparison:',len(samples),'real repaired examples; zero after-errors.')
