#!/usr/bin/env python3
"""Render repaired question pulls with actual player code; never writes EDB.

Usage: python3 render-current.py PATH/preview-questions-after.edn
Outputs current-question-*.{html,png,log,json} and render-current-report.json
beside the supplied pull file. UI assets are loaded directly from this checkout.
"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, html, json, re, shutil, subprocess, tempfile
from pathlib import Path
ROOT = next(p for p in Path(__file__).resolve().parents if (p / 'ui/learning.js').is_file())
sys.path.insert(0, str(ROOT))
from capture.scripts.database import edn

FUNCTIONS = ['el', 'short', 'fieldLabel', 'escapeHTML', 'assetURL', 'markdown', 'answerValue', 'loadMath', 'typeset', 'choiceOrder', 'fieldControl', 'collectResponses']


def enum(value):
    return str(value[':db/ident'] if isinstance(value, dict) else value)


def normalize(question):
    """Keep persisted identities; turn Pull maps into generator/player data."""
    q = {k: question[k] for k in [':db/id', ':question/problem', ':question/worked-solution']}
    q[':question/id'] = str(question[':question/id'])
    q[':question/difficulty'] = enum(question[':question/difficulty'])
    q[':question/answer-fields'] = []
    for field in question[':question/answer-fields']:
        f = {k: field[k] for k in [':db/id', ':answer-field/key']}
        f[':answer-field/id'] = str(field[':answer-field/id'])
        f[':answer-field/type'] = enum(field[':answer-field/type'])
        f[':answer-field/choices'] = [
            {':db/id': a[':db/id'], ':answer/id': str(a[':answer/id']), ':answer/type': enum(a[':answer/type']), ':answer/value': a[':answer/value']}
            for a in field[':answer-field/choices']
        ]
        correct = field[':answer-field/correct']
        if isinstance(correct, dict):
            correct_id = str(correct[':answer/id']) if ':answer/id' in correct else next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':db/id'] == correct[':db/id'])
        elif isinstance(correct, (list, tuple)):
            correct_id = str(correct[1])
        else:
            correct_id = next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':db/id'] == correct)
        assert any(a[':answer/id'] == correct_id for a in f[':answer-field/choices']), 'Correct answer must belong to the field'
        f[':answer-field/correct'] = [':answer/id', correct_id]
        assert f[':answer-field/type'] == ':answer-field.type/checkbox'
        assert sorted(a[':answer/value'] for a in f[':answer-field/choices']) == ['false', 'true']
        assert not re.fullmatch(r'I{1,3}', f[':answer-field/key']) and len(f[':answer-field/key']) > 5
        q[':question/answer-fields'].append(f)
    assert len(q[':question/answer-fields']) in [3, 4]
    assert not re.search(r'\bI{1,3}\b', q[':question/problem'] + '\n' + q[':question/worked-solution'])
    assert not re.search(r'(?m)^\s*[-*]?\s*\*?\*?I{1,3}\.', q[':question/problem'])
    return q


def player_script():
    learning = (ROOT / 'ui/learning.js').read_text()
    def function(name):
        start = learning.index('function ' + name + '(')
        end = learning.find('\nfunction ', start + 1)
        assert end != -1
        return learning[start:end]
    ui = (ROOT / 'ui').as_uri()
    return f"""import {{marked}} from '{ui}/vendor/marked/marked.esm.js';
import {{romanLists}} from '{ui}/prose-lists.js';
import {{loadMathInputs,inlinePrompt,mountInlineFields,richSelect,checkboxControl,freeInput,blankInput,choiceIndicator,fieldFeedback,responsesComplete}} from '{ui}/question-fields.js';
let typesetting=Promise.resolve(),mathLoader=null;
""" + '\n'.join(function(n) for n in FUNCTIONS) + r'''
try {
 const q=JSON.parse(document.querySelector('#data').textContent);
 const fields=q[':question/answer-fields'].map(f=>({id:f[':db/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':db/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const article=document.querySelector('article'),form=document.createElement('form');article.append(form);
 form.append(el('h1','','Question '+q[':db/id']+' | '+q[':question/difficulty'].split('/').pop()));
 const prompt=markdown(q[':question/problem'],'prose',fields),list=el('div','field-list');form.append(prompt,list);
 mountInlineFields(prompt,list,fields,f=>fieldControl(f,false,q[':question/id'],q[':question/problem']));
 const inputs=[...form.querySelectorAll('input[type="checkbox"]')];
 if(inputs.length!==fields.length||![3,4].includes(inputs.length))throw Error('Expected three or four actual checkbox controls');
 const subsets=[];
 for(let mask=0;mask<(1<<fields.length);mask++){
  inputs.forEach((input,i)=>{if(input.checked!==Boolean(mask&(1<<i)))input.click();});
  const responses=collectResponses(form,fields);
  if(!responsesComplete(fields,responses))throw Error('Unchecked false responses incomplete');
  responses.forEach((response,i)=>{const wanted=mask&(1<<i)?'true':'false';if(response.fieldId!==fields[i].id||response.choiceId!==fields[i].choices.find(a=>a.value===wanted).id)throw Error('UI subset encoding mismatch');});
  subsets.push({mask,responses});
 }
 const key=q[':question/answer-fields'].map(f=>f[':answer-field/choices'].find(a=>a[':answer/id']===f[':answer-field/correct'][1])[':answer/value']==='true');
 if(!key.some(Boolean))throw Error('No visibly selectable correct answer');
 inputs.forEach((input,i)=>{if(input.checked!==key[i])input.click();});
 form.append(el('h2','','Answer key (review only)'),markdown(key.map((v,i)=>fields[i].key+': '+v).join('; ')));
 form.append(el('h2','','Complete worked solution'),markdown(q[':question/worked-solution']));
 await MathJax.startup.promise;await MathJax.typesetPromise([article]);
 const errors=[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent);
 const controls=[...article.querySelectorAll('.answer-indicator')].map(n=>{let s=getComputedStyle(n),b=n.getBoundingClientRect();return {width:b.width,height:b.height,border:s.borderWidth,borderColor:s.borderColor};});
 const labelMath=[...form.querySelectorAll('.field-list label')].map((n,i)=>({text:n.textContent,math:n.querySelectorAll('mjx-container').length,expectedMath:(fields[i].key.match(/\$/g)||[]).length/2}));
 if(labelMath.length!==fields.length||!labelMath.every(l=>l.math===l.expectedMath))throw Error('Checkbox label math failed to render');
 const result={passed:true,labelMath,errors,checkbox_controls:inputs.length,radio_controls:article.querySelectorAll('input[type="radio"]').length,correct_selection:key,subsets,controls,math_expressions:article.querySelectorAll('mjx-container svg').length,whole_record_visible:article.getBoundingClientRect().bottom<innerHeight,horizontal_overflow:document.documentElement.scrollWidth>innerWidth,raw_delimiters:article.textContent.includes('$$'),document_height:document.documentElement.scrollHeight,viewport:[innerWidth,innerHeight],renderer:'actual learning.js fieldControl/collectResponses/markdown + actual question-fields/marked/DOMPurify/MathJax; navigation theme tokens'};
 result.passed=!errors.length&&result.whole_record_visible&&!result.horizontal_overflow&&!result.raw_delimiters&&controls.every(c=>c.width>=20&&c.height>=20&&parseFloat(c.border)>=1&&c.borderColor!=='rgba(0, 0, 0, 0)');
 document.querySelector('#summary').textContent=JSON.stringify(result);document.title=result.passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});}
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pull_file', type=Path)
    ap.add_argument('--question-id', type=int, action='append')
    args = ap.parse_args()
    source = args.pull_file.resolve(); out = source.parent
    wanted = args.question_id or [17592186562914, 17592186562881]
    pulls = edn.loads(source.read_text())
    pulls = [row[0] if isinstance(row, list) and len(row) == 1 else row for row in pulls]
    by_id = {q[':db/id']: q for q in pulls}
    script = out / 'current-player.js'; script.write_text(player_script())
    ui = (ROOT / 'ui').as_uri()
    reports = []
    for eid in wanted:
        q = normalize(by_id[eid]); name = 'current-question-' + str(eid)
        data = json.dumps(q, ensure_ascii=False)
        (out / (name + '.json')).write_text(data + '\n')
        page = f'''<!doctype html><html data-theme="light"><head><meta charset="utf-8"><title>Rendering</title><link rel="stylesheet" href="{ui}/navigation.css"><link rel="stylesheet" href="{ui}/learning.css"><link rel="stylesheet" href="{ui}/activity.css"><style>body{{display:block;margin:24px;font:18px system-ui;background:white;color:#172033}}article{{max-width:1120px;margin:auto;padding:20px;border:1px solid #ddd}}h1{{font-size:21px}}h2{{font-size:18px;margin-top:24px}}#summary{{font-size:10px;max-width:1120px;white-space:pre-wrap;overflow-wrap:anywhere;margin:auto}}mjx-container[display="true"]{{overflow-x:auto}}</style><script src="{ui}/vendor/dompurify/purify.min.js"></script><script src="{ui}/mathjax-config.js"></script><script defer src="{ui}/vendor/mathjax/tex-svg.js"></script></head><body><pre id="summary">pending</pre><main><article></article></main><script type="application/json" id="data">''' + data.replace('</', '<\\/') + '''</script><script type="module" src="current-player.js"></script></body></html>'''
        path = out / (name + '.html'); path.write_text(page)
        shot = out / (name + '.png'); profile = tempfile.mkdtemp(prefix='checkbox-current-render-', dir='/tmp')
        try:
            run = subprocess.run(['/usr/bin/google-chrome','--headless','--no-sandbox','--disable-gpu','--disable-background-networking','--user-data-dir='+profile,'--allow-file-access-from-files','--virtual-time-budget=15000','--window-size=1400,2300','--screenshot='+str(shot),'--dump-dom',path.as_uri()], capture_output=True, text=True, timeout=50)
        finally:
            shutil.rmtree(profile, ignore_errors=True)
        (out / (name + '.log')).write_text(run.stderr)
        found = re.search(r'<pre id="summary">(.*?)</pre>', run.stdout, re.S)
        assert found, (eid, run.stderr[-1000:])
        result = json.loads(html.unescape(found[1])); assert result['passed'], (eid, result)
        assert result['checkbox_controls'] == len(q[':question/answer-fields']) and result['radio_controls'] == 0
        reports.append({'question_eid':eid,'question_uuid':q[':question/id'],'record_sha256':hashlib.sha256(data.encode()).hexdigest(),'screenshot':shot.name,'screenshot_sha256':hashlib.sha256(shot.read_bytes()).hexdigest(),**result})
        print(eid, 'PASS', flush=True)
    assets = ['learning.js','question-fields.js','prose-lists.js','mathjax-config.js','learning.css','activity.css','navigation.css','vendor/marked/marked.esm.js','vendor/dompurify/purify.min.js','vendor/mathjax/tex-svg.js']
    report = {'passed':True,'input':str(source),'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'records':len(reports),'UI_subset_checks':sum(len(r['subsets']) for r in reports),'UI_files':{name:hashlib.sha256((ROOT/'ui'/name).read_bytes()).hexdigest() for name in assets},'functions':FUNCTIONS,'reports':reports}
    (out / 'render-current-report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    main()
