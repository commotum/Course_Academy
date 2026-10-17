"""Exercise all changed template/difficulty examples in the unchanged learner UI."""
import importlib.util,json
from pathlib import Path
ROOT=Path('/home/jake/Developer/Course_Academy');HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('render_preview',ROOT/'generate/pipeline/render_preview.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
records=json.loads((HERE/'examples.json').read_text())
r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('mathContainers:document.querySelectorAll',r'''systems:(()=>{const systems=[];for(const item of MathJax.startup.document.math){if(!item.math.includes('\\left\\{'))continue;const tables=[];item.root.walkTree(node=>{if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes.map(row=>row.childNodes.length),alignment:node.attributes.get('columnalign')});});systems.push({tex:item.math,tables});}return systems;})(),
        undefinedMacros:[...document.querySelectorAll('[data-mjx-error], [data-mml-node="mtext"][fill="red"]')].map(n=>n.textContent),
        overflow:[...document.querySelectorAll('mjx-container')].map(n=>({left:n.getBoundingClientRect().left,right:n.getBoundingClientRect().right})).filter(b=>b.left<0||b.right>innerWidth+2),
        controls:document.querySelectorAll('input,select').length,
        mathContainers:document.querySelectorAll''')
r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('state.passed=!errors.length',"state.passed=state.systems.every(s=>s.tables.length && s.tables[0].rows===2 && !s.tex.includes(';')) && !state.undefinedMacros.length && !errors.length")
r.render(records,HERE/'desktop',[],browser='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
selected=[]
for record in records:
 if record['knowledge_point']['db_id'] not in [r['knowledge_point']['db_id'] for r in selected]:selected.append(record)
r.BROWSER_SCRIPT=r.BROWSER_SCRIPT.replace('width:1280,height:1000','width:390,height:844')
r.render(selected,HERE/'mobile',[],browser='/home/jake/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome')
summaries=[]
for view in ['desktop','mobile']:
 data=json.loads((HERE/view/'rendering.json').read_text())
 summaries.append({'viewport':view,'passed':data['passed'],'cases':len(data['cases']),'systems':sum(len(c['systems']) for c in data['cases']),'math_errors':sum(len(c['mathErrors']) for c in data['cases']),'undefined_macros':sum(len(c['undefinedMacros']) for c in data['cases']),'overflow_math_containers':sum(len(c['overflow']) for c in data['cases'])})
(HERE/'rendering-summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
print(json.dumps(summaries,indent=2))
