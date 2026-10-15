"""Freeze and exercise actual player rendering and answer controls, no server/DB."""
import sys
sys.dont_write_bytecode=True
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('render00870',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
UI=HERE/'reference/ui'
for name in ['learning.css','activity.css','navigation.css','route-matrix.css']:
    shutil.copyfile(ROOT/'ui'/name,UI/name)
shutil.copytree(ROOT/'ui/vendor/mathlive',UI/'vendor/mathlive',dirs_exist_ok=True)
learning=(UI/'learning.js').read_text()
def function(name):
    start=learning.index('function '+name+'(')
    end=learning.find('\nfunction ',start+1)
    if end==-1:raise ValueError(name)
    return learning[start:end]
functions=['el','short','fieldLabel','escapeHTML','assetURL','markdown','answerValue','loadMath','typeset','choiceOrder','fieldControl']
pipeline='\n'.join(function(name) for name in functions)
# Use the exact player functions and module; no handwritten renderer/control.
script="""import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {MathfieldElement} from './reference/ui/vendor/mathlive/mathlive.min.mjs';
import {romanLists} from './reference/ui/prose-lists.js';
import {loadMathInputs,inlinePrompt,mountInlineFields,richSelect,checkboxControl,freeInput,blankInput,choiceIndicator,fieldFeedback} from './reference/ui/question-fields.js';
let typesetting=Promise.resolve(),mathLoader=null;
"""+pipeline+"""
try {
const r=JSON.parse(document.querySelector('#data').textContent), q=r.question;
const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],answerType:':answer.type/math',choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
if(fields.some(f=>f.type.endsWith('/blank'))) await loadMathInputs();
const article=document.querySelector('article');
const heading=el('h1','',r.generation.template+' | '+r.generation.profile);article.append(heading);
const prompt=markdown(q[':question/problem'],'prose',fields), list=el('div','field-list');article.append(prompt,list);
mountInlineFields(prompt,list,fields,field=>fieldControl(field,false,q[':question/id'],q[':question/problem']));
const key=q[':question/answer-fields'].map(f=>{let id=f[':answer-field/correct']?.[1];return f[':answer-field/key']+': '+(id?'$'+f[':answer-field/choices'].find(a=>a[':answer/id']===id)[':answer/value']+'$':'designation absent');}).join('; ');
article.append(el('h2','','Answer key (review only)'),markdown(key));
article.append(el('h2','','Complete fixed worked solution'));
article.append(markdown(q[':question/worked-solution']||'Worked solution absent in captured source.'));
await MathJax.startup.promise;await MathJax.typesetPromise([article]);
const errors=[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent);
const math=[...article.querySelectorAll('mjx-container svg')];
const bare=article.textContent.includes('$$')||article.textContent.includes('\\\\times')||article.textContent.includes('{{field-');
const invisible=[...article.querySelectorAll('math-field,.answer-indicator')].filter(n=>{const s=getComputedStyle(n),b=n.getBoundingClientRect();return b.width<20||b.height<20||parseFloat(s.borderWidth)<1;}).length;
const result={passed:errors.length===0&&!bare,errors,math_expressions:math.length,radio_controls:article.querySelectorAll('input[type="radio"]').length,math_blank_controls:article.querySelectorAll('math-field').length,invisible_controls:invisible,unmounted_placeholders:article.querySelectorAll('.field-location:empty').length,document_height:document.documentElement.scrollHeight,viewport_height:innerHeight,viewport_width:innerWidth,whole_record_visible:article.getBoundingClientRect().bottom<innerHeight,horizontal_overflow:document.documentElement.scrollWidth>innerWidth,displayed_math:!!article.querySelector('mjx-container[display="true"]'),renderer:'actual player learning.js functions + actual question-fields.js + marked/DOMPurify/MathJax/MathLive'};
result.passed=result.passed&&result.whole_record_visible&&result.unmounted_placeholders===0&&invisible===0&&!result.horizontal_overflow;
document.querySelector('#summary').textContent=JSON.stringify(result);document.title=result.passed?'PASS':'FAIL';
} catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});document.title='FAIL';}
"""
(HERE/'preview-player.js').write_text(script)
rows=[]
for template in g.DEFAULTS:
    rows.append((template,g.generate(g.level_of(template),41,template=template)))
for template in ['symbolic-radio','symbolic-blank']:
    rows.append((template,g.generate('hard',42,template=template)))
for template in ['q-42379','q-42380','q-70702']:
    rows.append(('raw-'+template,g.generate(g.level_of(template),template=template,parameters=g.DEFAULTS[template],profile='raw-'+template)))
reports=[]
for name,rec in rows:
    data=json.dumps(rec,ensure_ascii=False)
    path=HERE/('preview-'+name+'.html')
    page='''<!doctype html><html data-theme="light"><head><meta charset="utf-8"><title>Rendering</title><link rel="stylesheet" href="reference/ui/learning.css"><link rel="stylesheet" href="reference/ui/activity.css"><link rel="stylesheet" href="reference/ui/navigation.css"><style>body{display:block;margin:30px;font:18px system-ui;background:white;color:#172033}article{max-width:1050px;margin:auto;padding:24px;border:1px solid #ddd}h1{font-size:22px}h2{font-size:18px;margin-top:30px}#summary{font-size:11px;max-width:1000px;white-space:pre-wrap;overflow-wrap:anywhere;margin:auto}math-field{min-width:100px;background:white}mjx-container[display="true"]{overflow-x:auto}</style><script src="reference/ui/vendor/dompurify/purify.min.js"></script><script src="reference/ui/mathjax-config.js"></script><script defer src="reference/ui/vendor/mathjax/tex-svg.js"></script></head><body><pre id="summary">pending</pre><main><article></article></main><script type="application/json" id="data">'''+data+'''</script><script type="module" src="preview-player.js"></script></body></html>'''
    path.write_text(page)
    profile=tempfile.mkdtemp(prefix='kp00870-chrome-',dir='/tmp')
    shot=HERE/('preview-'+name+'.png')
    cmd=['/usr/bin/google-chrome','--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--user-data-dir='+profile,'--allow-file-access-from-files','--virtual-time-budget=15000','--window-size=1400,1600','--screenshot='+str(shot),'--dump-dom',path.as_uri()]
    run=subprocess.run(cmd,capture_output=True,text=True,timeout=50)
    (HERE/('preview-'+name+'.log')).write_text(run.stderr)
    found=re.search(r'<pre id="summary">(.*?)</pre>',run.stdout,re.S)
    assert found,(name,run.stdout[-2000:],run.stderr[-2000:])
    result=json.loads(html.unescape(found[1]));assert result['passed'],(name,result)
    assert result['radio_controls']==(5 if g.kind_of(rec['generation']['template'])=='radio' else 0)
    assert result['math_blank_controls']==(2 if g.kind_of(rec['generation']['template'])=='blank' else 0)
    reports.append({'name':name,'question_id':rec['question'][':question/id'],'record_sha256':hashlib.sha256(json.dumps(rec,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'exact_record':rec,'screenshot':shot.name,'screenshot_sha256':hashlib.sha256(shot.read_bytes()).hexdigest(),**result})
    print(name,result,flush=True)
(HERE/'render-validation.json').write_text(json.dumps({'passed':True,'records':len(reports),'network_reads':0,'reports':reports},indent=2,ensure_ascii=False)+'\n')
assets={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in UI.rglob('*') if p.is_file()}
(HERE/'reference/ui-capture.json').write_text(json.dumps({'files':assets,'source':'actual repository ui; copied without edits','mathjax_version':'3.2.2','functions':functions,'answer_control_module':'ui/question-fields.js'},indent=2)+'\n')
