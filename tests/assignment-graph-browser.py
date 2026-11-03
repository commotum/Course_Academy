"""Read-only browser check against a running app; all browser API writes blocked."""
from pathlib import Path
import json
import os
import subprocess
import tempfile

origin = os.environ.get('COURSE_ACADEMY_TEST_ORIGIN', 'http://127.0.0.1:8765')
script = r'''
const assert=require('assert/strict');
const {chromium}=require('/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'/home/jake/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell',args:['--disable-dev-shm-usage']});
 try {
  const page=await browser.newPage({viewport:{width:1400,height:1000}}), errors=[], writes=[];
  page.on('pageerror',error=>errors.push(String(error)));
  await page.route('**/api/**',route=>{
   if(!['GET','HEAD'].includes(route.request().method())){writes.push(route.request().url());return route.abort();}
   return route.continue();
  });
  await page.goto(ORIGIN+'/assignments');
  await page.waitForSelector('.assignment-queue .queue-card');
  const list=await(await page.request.get(ORIGIN+'/api/assignments')).json();
  const first=page.locator('.assignment-queue .queue-card').first();
  const assignmentURL=await first.locator('h2 a').getAttribute('href');
  const id=new URL(assignmentURL,ORIGIN).searchParams.get('assignment');
  const assignment=list.assignments.find(a=>a.id===id);assert.ok(assignment);
  const graphResponse=page.waitForResponse(r=>new URL(r.url()).pathname==='/api/graph-explorer');
  await first.click({button:'right'});
  const action=page.locator('#entity-context-menu a[data-action="assignment-targets-graph"]');
  await action.waitFor({state:'visible'});
  assert.equal(new URL(await action.getAttribute('href'),ORIGIN).searchParams.get('assignment'),id);
  await action.click();
  const graph=await(await graphResponse).json();
  await page.waitForFunction(()=>window.FlowAtlas&&document.getElementById('loadState').hidden);
  assert.equal(new URL(page.url()).searchParams.get('assignment'),id);
  assert.ok((await page.title()).includes(assignment.title));
  const nodeIds=new Set(graph.nodes.map(n=>n.id));
  const expectedRoots=assignment.topics.map(t=>t.id).filter(id=>nodeIds.has(id)).sort((a,b)=>a-b);
  const state=await page.evaluate(()=>FlowAtlas.getState());
  assert.equal(state.targetsView,true);assert.equal(state.depth,'0');
  assert.deepEqual([...state.activeIds].sort((a,b)=>a-b),expectedRoots);
  assert.deepEqual(await page.evaluate(()=>FlowAtlas.getNodes().map(n=>n.id).sort((a,b)=>a-b)),expectedRoots);
  assert.equal(await page.locator('#targetWeekStrip').isVisible(),false);
  assert.equal(await page.locator('#targetCourseFilters').isVisible(),false);
  const incoming=new Map(graph.nodes.map(n=>[n.id,[]]));
  for(const edge of graph.links)incoming.get(edge.target).push(edge.source);
  function expected(depth){const seen=new Map(expectedRoots.map(id=>[id,0])),todo=[...expectedRoots];for(let i=0;i<todo.length;i++){const id=todo[i],d=seen.get(id);if(d>=depth)continue;for(const pre of incoming.get(id)){if(!seen.has(pre)){seen.set(pre,d+1);todo.push(pre);}}}return [...seen.keys()].sort((a,b)=>a-b);}
  const sizes=[];
  for(const depth of [1,2]){
   await page.locator('#viewport').dispatchEvent('wheel',{shiftKey:true,deltaY:80,deltaMode:0,bubbles:true,cancelable:true});
   await page.waitForFunction(d=>FlowAtlas.getState().depth===String(d),depth);
   await page.waitForFunction(n=>FlowAtlas.getNodes().length===n,expected(depth).length);
   assert.deepEqual(await page.evaluate(()=>FlowAtlas.getNodes().map(n=>n.id).sort((a,b)=>a-b)),expected(depth));
   sizes.push(expected(depth).length);
  }
  await page.locator('#overviewBtn').click();
  await page.waitForFunction(()=>FlowAtlas.getState().depth==='0');
  assert.equal(new URL(page.url()).searchParams.get('assignment'),id);
  await page.reload();await page.waitForFunction(()=>window.FlowAtlas&&document.getElementById('loadState').hidden);
  assert.deepEqual(await page.evaluate(()=>FlowAtlas.getNodes().map(n=>n.id).sort((a,b)=>a-b)),expectedRoots);
  // A bad ID must show an error, never silently open all personal targets.
  await page.goto(ORIGIN+'/?view=targets&assignment=missing-browser-fixture');
  await page.waitForFunction(()=>document.getElementById('retryLoad').hidden===false);
  assert.match(await page.locator('#loadMessage').textContent(),/assignment.*not available/);
  assert.equal(await page.locator('#nodes .node').count(),0);
  assert.deepEqual(errors,[]);assert.deepEqual(writes,[]);
  console.log(JSON.stringify({passed:true,readOnly:true,assignment:assignment.title,roots:expectedRoots.length,upstreamCounts:sizes,contextMenu:true,shiftScroll:true,reload:true,invalidIdSafe:true,apiWrites:writes,javascriptErrors:errors}));
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
'''
with tempfile.TemporaryDirectory(prefix='assignment-graph-browser-') as directory:
    path=Path(directory)/'test.cjs';path.write_text(script.replace('ORIGIN',json.dumps(origin)))
    subprocess.run(['/home/jake/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node',str(path)],check=True,timeout=100)
