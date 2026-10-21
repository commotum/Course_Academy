import json,pathlib,sys,importlib.util
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent;REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
load=lambda f:json.loads((R/f).read_text())
cases=load('grader-input.json')
for name,file,indexes in [('batch','delivery-batch/accepted.json',range(5)),('hard','delivery-hard/accepted.json',range(3))]:
 rs=load(file)
 for i in indexes:
  record=rs[i];correct=record['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']
  cases.append({'label':'post-normalization-'+name+'-'+str(i),'record':record,'checks':[{'submitted':correct,'expected':'accepted','purpose':'delivered normalized record accepts known independently checked solution'},{'submitted':'0','expected':'rejected','purpose':'delivered record rejects ignored forcing'}]})
(R/'grader-delivered-input.json').write_text(json.dumps(cases,indent=2)+'\n')
spec=importlib.util.spec_from_file_location('actual_renderer',REPO/'generate/pipeline/render_preview.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
# Supplement shared renderer with browser geometry and actual scroll behavior. UI remains unmodified.
renderer.BROWSER_SCRIPT=renderer.BROWSER_SCRIPT.replace('const state = await page.evaluate(() => ({','''const scrolling = await page.evaluate(() => [...document.querySelectorAll('.prose mjx-container[display="true"]')].filter(n=>n.scrollWidth>n.clientWidth+2).map(n=>{
 const before=n.scrollLeft;n.scrollLeft=n.scrollWidth;
 return {clientWidth:n.clientWidth,scrollWidth:n.scrollWidth,before,after:n.scrollLeft,overflowX:getComputedStyle(n).overflowX,text:n.textContent};
}));
      const state = await page.evaluate(() => ({''').replace('state.index=index;', 'state.scrolling=scrolling; state.index=index;')
renderer.render([load('hard-controlled-records.json')[3]],R/'render-scroll',[R])
report=load('render-scroll/rendering.json');assert report['passed']
assert report['cases'][0]['scrolling'] and all(row['after']>0 and row['overflowX']=='auto' for row in report['cases'][0]['scrolling'])
print('All oversized boundary equations have working horizontal scroll; saved right-edge screenshot.')
