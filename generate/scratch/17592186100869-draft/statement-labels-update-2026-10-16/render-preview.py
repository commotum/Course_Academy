"""Real player functions, finite-subset UI interactions, complete screenshots."""
import sys
sys.dont_write_bytecode=True
import hashlib,html,importlib.util,json,re,shutil,subprocess,tempfile
from pathlib import Path
D=Path(__file__).resolve().parent;ROOT=D.parents[3];UI=D/'reference/ui';UI.mkdir(parents=True,exist_ok=True)
for name in ['learning.js','question-fields.js','prose-lists.js','mathjax-config.js','learning.css','activity.css','navigation.css']:
 shutil.copyfile(ROOT/'ui'/name,UI/name)
for name in ['marked','dompurify','mathjax']:
 shutil.copytree(ROOT/'ui/vendor'/name,UI/'vendor'/name,dirs_exist_ok=True)
learning=(UI/'learning.js').read_text()
def function(name):
 start=learning.index('function '+name+'(');end=learning.find('\nfunction ',start+1);assert end!=-1;return learning[start:end]
functions=['el','short','fieldLabel','escapeHTML','assetURL','markdown','answerValue','loadMath','typeset','choiceOrder','fieldControl','collectResponses']
pipeline='\n'.join(function(n) for n in functions)
script="""import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
import {loadMathInputs,inlinePrompt,mountInlineFields,richSelect,checkboxControl,freeInput,blankInput,choiceIndicator,fieldFeedback,responsesComplete} from './reference/ui/question-fields.js';
let typesetting=Promise.resolve(),mathLoader=null;
"""+pipeline+r'''
try {
 const r=JSON.parse(document.querySelector('#data').textContent),q=r.question;
 const fields=q[':question/answer-fields'].map((f,i)=>({id:20+i,key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map((a,j)=>({id:100+2*i+j,type:a[':answer/type'],value:a[':answer/value']}))}));
 const article=document.querySelector('article'),form=document.createElement('form');article.append(form);
 form.append(el('h1','',r.generation.level+' | '+r.generation.template+' | '+r.generation.profile));
 const prompt=markdown(q[':question/problem'],'prose',fields),list=el('div','field-list');form.append(prompt,list);
 mountInlineFields(prompt,list,fields,f=>fieldControl(f,false,q[':question/id'],q[':question/problem']));
 const inputs=[...form.querySelectorAll('input[type="checkbox"]')];if(inputs.length!==3)throw Error('Expected actual three checkbox controls');
 const labels=[...form.querySelectorAll('.checkbox-field')].map(n=>n.textContent);
 const subsets=[];
 for(let mask=0;mask<8;mask++){
  inputs.forEach((input,i)=>{if(input.checked!==Boolean(mask&(1<<i)))input.click();});
  const responses=collectResponses(form,fields);
  if(!responsesComplete(fields,responses))throw Error('Unchecked false responses incomplete');
  responses.forEach((response,i)=>{const wanted=mask&(1<<i)?'true':'false';if(response.choiceId!==fields[i].choices.find(a=>a.value===wanted).id)throw Error('UI finite-subset encoding mismatch');});
  subsets.push({mask,responses});
 }
 const key=q[':question/answer-fields'].map(f=>f[':answer-field/choices'].find(a=>a[':answer/id']===f[':answer-field/correct'][1])[':answer/value']==='true');
 inputs.forEach((input,i)=>{if(input.checked!==key[i])input.click();});
 form.append(el('h2','','Answer key (review only)'),markdown(key.map((v,i)=>fields[i].key+': '+v).join('; ')));
 form.append(el('h2','','Complete fixed worked solution'),markdown(q[':question/worked-solution']));
 await MathJax.startup.promise;await MathJax.typesetPromise([article]);
 const errors=[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent);
 const controls=[...article.querySelectorAll('.answer-indicator')].map(n=>{let s=getComputedStyle(n),b=n.getBoundingClientRect();return {width:b.width,height:b.height,border:s.borderWidth,borderColor:s.borderColor};});
 const labelMath=[...form.querySelectorAll('.field-list label')].map(n=>({text:n.textContent,math:n.querySelectorAll('mjx-container').length}));
 const result={passed:true,labelMath,errors,checkbox_controls:inputs.length,radio_controls:article.querySelectorAll('input[type="radio"]').length,subsets,controls,math_expressions:article.querySelectorAll('mjx-container svg').length,whole_record_visible:article.getBoundingClientRect().bottom<innerHeight,horizontal_overflow:document.documentElement.scrollWidth>innerWidth,raw_delimiters:article.textContent.includes('$$'),document_height:document.documentElement.scrollHeight,viewport:[innerWidth,innerHeight],renderer:'actual learning.js fieldControl/collectResponses/markdown + actual question-fields/marked/DOMPurify/MathJax; navigation theme tokens'};
 result.passed=!errors.length&&result.whole_record_visible&&!result.horizontal_overflow&&!result.raw_delimiters&&controls.every(c=>c.width>=20&&c.height>=20&&parseFloat(c.border)>=1&&c.borderColor!=='rgba(0, 0, 0, 0)');
 document.querySelector('#summary').textContent=JSON.stringify(result);document.title=result.passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});}
'''
(D/'preview-player.js').write_text(script)
s=importlib.util.spec_from_file_location('render00869',D.parent.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
rows=[('generated-'+r['generation']['template'],r) for r in json.loads((D/'review.json').read_text())]
reports=[]
for name,rec in rows:
 path=D/('preview-'+name+'.html');data=json.dumps(rec,ensure_ascii=False)
 page='''<!doctype html><html data-theme="light"><head><meta charset="utf-8"><title>Rendering</title><link rel="stylesheet" href="reference/ui/navigation.css"><link rel="stylesheet" href="reference/ui/learning.css"><link rel="stylesheet" href="reference/ui/activity.css"><style>body{display:block;margin:24px;font:18px system-ui;background:white;color:#172033}article{max-width:1120px;margin:auto;padding:20px;border:1px solid #ddd}h1{font-size:21px}h2{font-size:18px;margin-top:24px}#summary{font-size:10px;max-width:1120px;white-space:pre-wrap;overflow-wrap:anywhere;margin:auto}mjx-container[display="true"]{overflow-x:auto}</style><script src="reference/ui/vendor/dompurify/purify.min.js"></script><script src="reference/ui/mathjax-config.js"></script><script defer src="reference/ui/vendor/mathjax/tex-svg.js"></script></head><body><pre id="summary">pending</pre><main><article></article></main><script type="application/json" id="data">'''+data+'''</script><script type="module" src="preview-player.js"></script></body></html>'''
 path.write_text(page);profile=tempfile.mkdtemp(prefix='kp00869-browser-',dir='/tmp');shot=D/('preview-'+name+'.png')
 cmd=['/usr/bin/google-chrome','--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--user-data-dir='+profile,'--allow-file-access-from-files','--virtual-time-budget=15000','--window-size=1400,2100','--screenshot='+str(shot),'--dump-dom',path.as_uri()]
 run=subprocess.run(cmd,capture_output=True,text=True,timeout=50);(D/('preview-'+name+'.log')).write_text(run.stderr)
 found=re.search(r'<pre id="summary">(.*?)</pre>',run.stdout,re.S);assert found,(name,run.stderr[-1000:]);result=json.loads(html.unescape(found[1]));assert result['passed'],(name,result)
 assert result['checkbox_controls']==3 and result['radio_controls']==0
 reports.append({'name':name,'question_id':rec['question'][':question/id'],'exact_record':rec,'record_sha256':hashlib.sha256(json.dumps(rec,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'screenshot':shot.name,'screenshot_sha256':hashlib.sha256(shot.read_bytes()).hexdigest(),**result});print(name,'PASS',flush=True)
(D/'render-validation.json').write_text(json.dumps({'passed':True,'records':len(reports),'UI_subset_checks':len(reports)*8,'reports':reports},indent=2,ensure_ascii=False))
assets={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in UI.rglob('*') if p.is_file()}
(D/'reference/ui-capture.json').write_text(json.dumps({'files':assets,'source':'Repository UI copied unchanged','functions':functions,'answer_control_module':'ui/question-fields.js'},indent=2))
