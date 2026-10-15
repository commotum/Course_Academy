#!/usr/bin/env python3
"""Local frozen player Markdown/DOMPurify/MathJax rendering; no network or DB."""
import importlib.util,json,re,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('preview_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
learning=(HERE/'reference/ui/learning.js').read_text();start=learning.index('function markdown(');end=learning.index('\n}\n',start)+2
pipeline=learning[start:end]
script="""import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
const el=(tag,cls)=>{let n=document.createElement(tag);n.className=cls;return n};
const inlinePrompt=value=>value;
const fieldLabel=key=>key;
const assetURL=value=>value;
const escapeHTML=text=>String(text).replace(/[&<>\"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'})[c]);
"""+pipeline+"""
try {
const rows=JSON.parse(document.querySelector('#data').textContent);let expected=0;
for(const r of rows){let article=document.createElement('article');article.id=r.question[':question/id'];let h=document.createElement('h2');h.textContent=r.generation.template+' '+JSON.stringify(r.generation.parameters);article.append(h);
let values=[r.question[':question/problem'],...r.question[':question/answer-fields'][0][':answer-field/choices'].map(a=>'$'+a[':answer/value']+'$'),r.question[':question/worked-solution']];
for(let text of values){expected+=(text.match(/\\$\\$[\\s\\S]*?\\$\\$|(?<!\\\\)\\$(?!\\$)(?:\\\\.|[^$\\\\])*?(?<!\\\\)\\$/g)||[]).length;article.append(markdown(text));}document.querySelector('main').append(article);}
await MathJax.startup.promise;await MathJax.typesetPromise();
const svgs=[...document.querySelectorAll('mjx-container svg')];
const errors=[...document.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent);
const empty=svgs.filter(n=>!n.querySelector('path,use,text,rect,line,polygon')).length;
const overflow=[...document.querySelectorAll('mjx-container')].filter(n=>n.getBoundingClientRect().right>document.documentElement.clientWidth+2).length;
const result={records:rows.length,expected_math:expected,rendered_math:svgs.length,errors,empty_svg:empty,horizontal_overflow:overflow,renderer:'player Markdown protection + marked + DOMPurify + MathJax3.2.2 frozen assets'};
result.passed=errors.length===0&&empty===0&&svgs.length===expected&&overflow===0;
document.querySelector('#summary').textContent=JSON.stringify(result);document.title=result.passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});document.title='FAIL';}
"""
(HERE/'preview-player.js').write_text(script)
reports=[]
for name,sid in g.TEMPLATES.items():
 rows=[]
 for params in g.parameters_for(name):
  rows.append(g.generate(g.DIFFICULTY[sid],template=name,parameters=params))
  if name in g.OPAQUE:rows.append(g.generate(g.DIFFICULTY[sid],template=name,parameters=params,profile='completed:'+sid))
 html='''<!doctype html><html><head><meta charset="utf-8"><title>Rendering</title><style>body{margin:25px;font:16px system-ui;max-width:1050px}article{padding:20px;border-bottom:2px solid #bbb}mjx-container[display="true"]{overflow-x:auto}#summary{white-space:pre-wrap}h2{font-size:18px}</style><script src="reference/ui/vendor/dompurify/purify.min.js"></script><script src="reference/ui/mathjax-config.js"></script><script defer src="reference/ui/vendor/mathjax/tex-svg.js"></script></head><body><pre id="summary">pending</pre><main></main><script type="application/json" id="data">'''+json.dumps(rows,ensure_ascii=False)+'''</script><script type="module" src="preview-player.js"></script></body></html>'''
 path=HERE/('preview-'+name+'.html');path.write_text(html)
 profile=tempfile.mkdtemp(prefix='kp17592186184351-chrome-',dir='/tmp')
 cmd=['/usr/bin/google-chrome','--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--user-data-dir='+profile,'--allow-file-access-from-files','--virtual-time-budget=45000','--window-size=1400,1100','--dump-dom',path.as_uri()]
 result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=60)
 (HERE/('preview-'+name+'.log')).write_text(result.stderr)
 found=re.search(r'<pre id="summary">(.*?)</pre>',result.stdout,re.S)
 assert found,('Missing render summary',name,result.stderr[-2000:])
 import html as escape
 summary=json.loads(escape.unescape(found[1]));reports.append({'template':name,**summary});print(name,summary,flush=True)
 assert summary['passed'],summary
 if name in ('positive_integer_power','natural_positive_root','derivative_ratio'):
  shot=HERE/('preview-'+name+'.png')
  subprocess.run(cmd[:-2]+['--screenshot='+str(shot),path.as_uri()],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=60,check=True)
(HERE/'render-validation.json').write_text(json.dumps({'passed':True,'records':sum(r['records'] for r in reports),'math_expressions':sum(r['rendered_math'] for r in reports),'templates':reports,'network_reads':0},indent=2)+'\n')
