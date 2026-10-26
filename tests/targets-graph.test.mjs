import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

// Exercise the actual graph scope and URL code with fixtures, without a server or DB.
const html = await readFile(new URL('../ui/Math-Academy-Graph-Explorer.html', import.meta.url), 'utf8');
const weekSource = (await readFile(new URL('../ui/target-weeks.js', import.meta.url), 'utf8')).replaceAll('export ', '');
const targetScopeSource = html.slice(html.indexOf('  // Graph-owned filtering and placement;'), html.indexOf('  // End graph-owned filtering and placement.'));
const scopeSource = html.slice(html.indexOf('  function selectedCourse()'), html.indexOf('  const coursePicker ='));
const activeSource = html.slice(html.indexOf('  function buildActiveSet()'), html.indexOf('  // Keep dependency columns fixed.'));
const helperSource = html.slice(html.indexOf('  function isScoped()'), html.indexOf('  function titleWrap('));
const columnSource = html.slice(html.indexOf('  function assignScopedColumns('), html.indexOf('  function buildActiveSet()'));
const selectionSource = html.slice(html.indexOf('  function selectionSnapshot()'), html.indexOf('  let MAX_DEPTH='));
const depthSource = html.slice(html.indexOf('  function setDepth('), html.indexOf('  function handleDepthWheel('));
const resetSource = html.slice(html.indexOf('  function resetView()'), html.indexOf('  function fitToBounds('));
const geometrySource = html.slice(html.indexOf('  function titleWrap('), html.indexOf('  // An active set can contain'));
const layoutSource = html.slice(html.indexOf('  function orderColumnStacks('), html.indexOf('  function relatedNodeIds('));
const guidesSource = html.slice(html.indexOf('  function renderGuides('), html.indexOf('  function stopMarqueeLoop('));
const changeSource = html.slice(html.indexOf('    onChange: learner => {') + '    onChange: learner => {'.length, html.indexOf('\n    },\n  });'));
const queueChangeStart = html.indexOf('    onChange: learner => {', html.indexOf('  const queueControls ='));
const queueChangeSource = html.slice(queueChangeStart + '    onChange: learner => {'.length, html.indexOf('\n    },\n  });', queueChangeStart));

function fixture(targets = [1, 3], { splitSaved = null, queueSaved = null } = {}) {
  const element = () => ({
    listeners: {}, dataset: {},
    addEventListener(name, listener) { this.listeners[name] = listener; },
    attributes: {}, children: [], classList: { toggle() {} },
    setAttribute(key, value) { this.attributes[key] = value; },
    removeAttribute(key) { delete this.attributes[key]; },
    replaceChildren() { this.children = []; },
    appendChild(child) { this.children.push(child); },
    focus() { this.focused = true; }, scrollIntoView() {},
  });
  const elements = new Map();
  const $ = id => { if (!elements.has(id)) elements.set(id, element()); return elements.get(id); };
  const nodes = [1, 2, 3, 4, 5, 6].map(id => ({ id, name: `Topic ${id}`, layer: 29 + ({ 4: 0, 1: 1, 6: 1, 2: 2, 3: 2, 5: 3 })[id], order: 0 }));
  const links = [{ source: 1, target: 3 }, { source: 1, target: 2 }, { source: 4, target: 1 }, { source: 3, target: 5 }, { source: 4, target: 6 }];
  const context = vm.createContext({
    URL, $, attachGraphTopicMenu() {}, document: { createElement: element, createElementNS: element, getElementById: $, querySelector: () => $('.app'), title: '' },
    location: { href: 'http://example.test/?view=targets&course=course-a&topic=2' },
    snapshot: { learner: { targets, courseId: 'course-a' }, courses: [{ id: 'course-a', title: 'Course A', topicIds: [1, 2] }] },
    storage: new Map(),
    localStorage: { getItem(key) { return key === 'course-academy.graph-targets-split' ? splitSaved : key === 'course-academy.graph-target-queue' ? queueSaved : null; }, setItem(key, value) { context.storage.set(key, value); } },
    NODES: nodes, LINKS: links,
    dependencyOrder: [4, 1, 2, 3, 5, 6],
    inMap: new Map(nodes.map(n => [n.id, links.filter(e => e.target === n.id).map(e => e.source)])),
    outMap: new Map(nodes.map(n => [n.id, links.filter(e => e.source === n.id).map(e => e.target)])),
    nodeById: new Map(nodes.map(n => [n.id, n])),
    courseId: null, targetsView: false, courseTopics: new Set(), loading: false, targetTopicId: null,
    state: { activeIds: new Set(), selected: null }, pendingDepthFrame: 0, MAX_DEPTH: 10,
    stackOrderCache: new Map(), STARTER_TOPIC_IDS: [],
    nodeGeometryCache: new Map(), layoutCache: new Map(),
    titleReaderboards: { clear() {}, set() {} },
    redraws: [], resetDepthWheel() {}, resize() {},
    redraw(fit) { context.redraws.push(fit); }, updateUI() {},
    scheduleDepthLayout() {}, refreshTargetColors() {},
    constants: { maxNodeWidth: 320, minNodeWidth: 78, textPadX: 11, textPadY: 7, lineHeight: 14, layerGap: 160, rowGap: 12, topPad: 24, leftPad: 28 },
    measuredTitleWidth: text => text.length * 7, layerLabel: node => 'L' + String(node.layer + 1).padStart(2, '0'),
    guidesG: $('guides'),
  });
  context.history = { replaceState(_state, _title, url) { context.location.href = String(url); } };
  vm.runInContext(`${weekSource}\n${targetScopeSource}\n${helperSource}\n${geometrySource}\n${columnSource}\n${selectionSource}\n${depthSource}\n${resetSource}\n${scopeSource}\n${activeSource}\n${layoutSource}\n${guidesSource}\nfunction learnerChanged(learner) { ${changeSource} }`, context);
  vm.runInContext(`function queueChanged(learner) { ${queueChangeSource} }`, context);
  return context;
}

test('indexed track placement preserves nearest clear routes and stable ties under dense skipping links', () => {
  const c = fixture();
  const routingSource = html.slice(html.indexOf('  function routeConnections('), html.indexOf('  function relatedNodeIds('));
  // Straightforward nearest-clear-track oracle, independent of the optimized
  // cached spaces and binary searches. Stable sort defines equal-distance ties.
  const referenceTrack = `function freeTrack(col, preferred) {
    const boxes=col.nodes.map(n=>pos.get(n.id)).sort((a,b)=>a.y-b.y), candidates=[];
    for(let i=0;i<boxes.length-1;i++) {
      const low=boxes[i].y+boxes[i].h+5, high=boxes[i+1].y-5;
      if(high>=low) {
        candidates.push((low+high)/2);
        if(high-low>=8)candidates.push(low+1,high-1);
      }
    }
    const taken=referenceTaken.get(col.index)||[];
    for(let i=1;i<=Math.max(24,taken.length+1);i++)
      candidates.push(boxes[0].y-6-i*5,boxes.at(-1).y+boxes.at(-1).h+6+i*5);
    candidates.sort((a,b)=>Math.abs(a-preferred)-Math.abs(b-preferred));
    const y=candidates.find(v=>taken.every(t=>Math.abs(t-v)>=3.7))??candidates[0];
    taken.push(y);referenceTaken.set(col.index,taken);return y;
  }
  `;
  const referenceSource=routingSource
    .replace('function routeConnections(', 'function referenceRouting(')
    .replace('const trackSpaces=new Map();','const referenceTaken=new Map();');
  const start=referenceSource.indexOf('    function freeTrack('), end=referenceSource.indexOf('    // Main inter-column links');
  vm.runInContext(referenceSource.slice(0,start)+referenceTrack+referenceSource.slice(end),c);
  const positions=new Map(),columns=[];
  for(let col=0;col<5;col++) {
    const nodes=[];
    for(let row=0;row<14;row++) {
      const id=col*14+row+1,h=26+row%3,y=row*51.25+col%2*5.125;
      nodes.push({id});positions.set(id,{x:col*200,y,w:80,h,col,colIndex:col});
    }
    columns.push({index:col,x:col*200,width:80,nodes});
  }
  const edges=[];
  for(let col=0;col<4;col++)for(let row=0;row<14;row++)for(let end=col+1;end<5;end++) {
    edges.push({source:col*14+row+1,target:end*14+(row*7+end*3)%14+1,index:edges.length});
  }
  for(const scoped of [true,false]) {
    assert.equal(JSON.stringify(c.routeConnections(edges,positions,columns,scoped)),
      JSON.stringify(c.referenceRouting(edges,positions,columns,scoped)));
  }
});

test('only edges beyond two displayed layers become disconnected, bidirectional continuation stubs', () => {
  const c=fixture(),positions=new Map(),columns=[];
  for(let col=0;col<5;col++) {
    const id=(col+1)*10;
    positions.set(id,{x:col*220,y:col*40,w:80,h:26,col,colIndex:col});
    columns.push({index:col,x:col*220,width:80,nodes:[{id}]});
  }
  const raw=[20,30,40,50].map((target,index)=>({source:10,target,index}));
  for(const scoped of [false,true]) {
    const routing=c.routeConnections(raw,positions,columns,scoped);
    assert.equal(routing.edges.length,raw.length);assert.equal(routing.summary.shortened,2);
    for(const edge of routing.edges) {
      assert.equal(edge.shortened,edge.span>2);
      assert.equal(edge.source,10);
      if(!edge.shortened){assert.equal(edge.stubs.length,0);assert.equal((edge.d.match(/M/g)||[]).length,1);continue;}
      assert.equal(edge.stubs.length,2);assert.equal(edge.segments.length,2);
      assert.equal((edge.d.match(/M/g)||[]).length,2); // Never connect the remote subpaths.
      assert.equal(edge.stubs[0].nodeId,edge.source);assert.equal(edge.stubs[0].peerId,edge.target);
      assert.equal(edge.stubs[1].nodeId,edge.target);assert.equal(edge.stubs[1].peerId,edge.source);
      for(const segment of edge.segments) {
        assert.equal(segment.p1[0]-segment.p0[0],54);
        assert.equal(segment.p0[1],segment.p1[1]);
        assert.equal(segment.c1[1],segment.p0[1]);assert.equal(segment.c2[1],segment.p0[1]);
      }
    }
    const bundled=c.bundleLongConnections(routing.edges);
    assert.equal(bundled.length,3); // One outgoing mark for two long edges, plus each incoming end.
    const source=bundled.find(stub=>stub.nodeId===10);
    assert.deepEqual([...source.peerIds],[40,50]);
    assert.deepEqual(Array.from(bundled.filter(stub=>stub.nodeId!==10),stub=>[stub.nodeId,[...stub.peerIds]]),[[40,[10]],[50,[10]]]);
    assert.ok(routing.edges.flatMap(edge=>edge.stubs).some(stub=>stub.nodeId===source.nodeId&&stub.y===source.y));
  }
});

// Clip each monotone cubic to the continuation's horizontal extent. Its y
// extrema occur at the clipped endpoints, so this checks the whole mark,
// including crossings farther from the rectangle than the attachment port.
function continuationCollisions(edges) {
  const collisions=[];
  const cubic=(q,t,axis)=>((1-t)**3*q.p0[axis]+3*(1-t)**2*t*q.c1[axis]+3*(1-t)*t*t*q.c2[axis]+t**3*q.p1[axis]);
  const atX=(q,x)=>{
    let low=0,high=1;
    for(let i=0;i<40;i++){
      const mid=(low+high)/2;
      if(cubic(q,mid,0)<x)low=mid;else high=mid;
    }
    return cubic(q,(low+high)/2,1);
  };
  for(const stub of edges.flatMap(edge=>edge.stubs)) {
    const tip=stub.x+stub.direction*stub.length;
    const left=Math.min(stub.x,tip),right=Math.max(stub.x,tip);
    for(const edge of edges.filter(edge=>!edge.shortened))for(const q of edge.segments){
      const lo=Math.max(left,q.p0[0]),hi=Math.min(right,q.p1[0]);
      if(hi<lo)continue;
      if(Math.min(q.p0[1],q.p1[1])-stub.y>=3.5||stub.y-Math.max(q.p0[1],q.p1[1])>=3.5)continue;
      const a=atX(q,lo),b=atX(q,hi);
      const clearance=Math.max(Math.min(a,b)-stub.y,stub.y-Math.max(a,b),0);
      if(clearance<3.5)collisions.push({node:stub.nodeId,side:stub.side,edge:[edge.source,edge.target],clearance});
    }
  }
  return collisions;
}

test('continuations stay clear of incoming, outgoing, and passing curves along their entire length', () => {
  const c=fixture();
  for(const gap of [160,80])for(const scoped of [true,false]){
    const positions=new Map(),columns=[],raw=[];
    for(let col=0;col<7;col++){
      const nodes=[];
      for(let row=0;row<12;row++){
        const id=col*12+row+1;
        nodes.push({id});positions.set(id,{x:col*(100+gap),y:row*51.25+col%2*5.125,w:100,h:26,col,colIndex:col});
      }
      columns.push({index:col,x:col*(100+gap),width:100,nodes});
    }
    for(let col=0;col<6;col++)for(let row=0;row<12;row++)for(let end=col+1;end<Math.min(7,col+5);end++){
      raw.push({source:col*12+row+1,target:end*12+(row*7+end*3)%12+1,index:raw.length});
    }
    const {edges}=c.routeConnections(raw,positions,columns,scoped);
    assert.equal(edges.length,raw.length);
    assert.ok(edges.some(edge=>edge.shortened));
    assert.deepEqual(continuationCollisions(edges),[],`gap ${gap}, scoped ${scoped}`);
    for(const stub of c.bundleLongConnections(edges)){
      assert.ok(stub.length>0&&stub.length<=54);
      if(gap===160)assert.equal(stub.length,54);
      const mixed=edges.some(edge=>!edge.shortened&&(stub.side==='right'?edge.source:edge.target)===stub.nodeId);
      if(mixed)assert.equal(stub.y,positions.get(stub.nodeId).y+3);
    }
  }
});

test('shortening long routes preserves nodes, positions, prerequisite scope, and logical edge IDs', () => {
  const c=fixture([4,1,3,5]);
  c.LINKS.push({source:4,target:5});c.inMap.get(5).push(4);c.outMap.get(4).push(5);
  c.changeCourse(null,true,'targets');
  const shortened=c.layoutCurrent();assert.ok(shortened.routeSummary.shortened>0);
  const source=html.slice(html.indexOf('  function routeConnections('),html.indexOf('  function bundleLongConnections('));
  vm.runInContext(source.replace('function routeConnections(','function fullRouting(').replace('e.shortened=e.span>2;','e.shortened=false;'),c);
  c.routeConnections=c.fullRouting;c.layoutCache.clear();
  const full=c.layoutCurrent();
  assert.deepEqual(shortened.pos,full.pos);
  assert.deepEqual([...shortened.localColumns],[...full.localColumns]);
  assert.deepEqual(shortened.activeLinks.map(edge=>[edge.source,edge.target,edge.index]),full.activeLinks.map(edge=>[edge.source,edge.target,edge.index]));
});

test('targets overview spans courses and retains only links between saved targets', () => {
  const c = fixture([1, 3, 3, 999]);
  c.changeCourse('course-a', true, 'targets');
  const active = c.buildActiveSet();
  assert.deepEqual([...active.nodeIds], [1, 3]);
  assert.deepEqual([...active.edgeSet], [0]);
  assert.equal(c.location.href, 'http://example.test/?view=targets');
  assert.equal(c.$('targetsLink').attributes['aria-current'], 'page');
  assert.equal(c.document.title, 'Targets · Course Academy');
  assert.equal(c.isScoped(), true);
  assert.equal(c.state.mode, 'upstream');
  assert.equal(c.state.depth, '0');
  assert.deepEqual([...c.state.activeIds], [1, 3]);
  assert.equal([...active.columns.values()].every(Number.isInteger), true);
});

test('targets exclude displayed L29 and below from roots, expanded prerequisites, links, and counts', () => {
  const c = fixture([1, 3]); c.snapshot.learner.queue = [2, 4, 6];
  for (const [id, layer] of [[4, 27], [1, 28], [6, 28], [2, 29], [3, 30], [5, 31]]) c.nodeById.get(id).layer = layer;
  const saved = JSON.stringify(c.snapshot.learner);
  c.changeCourse(null, true, 'targets');
  assert.deepEqual([...c.state.activeIds], [3, 2]); // L30 is retained; L29 is excluded.
  assert.equal(c.$('targetWeekReadout').textContent, 'All weeks · 1 target · 1 queued');
  for (const depth of [0, 1, 2, 'all']) {
    c.setDepth(depth, true);
    const active = c.buildActiveSet();
    assert.deepEqual([...active.nodeIds].sort(), [2, 3]);
    assert.ok([...active.edgeSet].every(i => active.nodeIds.has(c.LINKS[i].source) && active.nodeIds.has(c.LINKS[i].target)));
  }
  c.setSelected(1); assert.deepEqual([...c.state.activeIds], [3, 2]);
  c.state.mode = 'overview'; assert.deepEqual([...c.buildActiveSet().nodeIds], [3, 2]);
  c.changeCourse('course-a');
  assert.deepEqual([...c.buildActiveSet().nodeIds], [1, 2]); // Other graph pages retain the lower layers.
  assert.equal(JSON.stringify(c.snapshot.learner), saved);
  c.learnerChanged({ ...c.snapshot.learner, targets: [1] });
  c.queueChanged({ queue: [4, 6] });
  c.changeCourse(null, true, 'targets');
  assert.equal(c.buildActiveSet().nodeIds.size, 0);
  assert.equal(c.state.selected, null);
});

function addSchoolCourses(c) {
  c.snapshot.courses.push(
    { id: 'de', code: 'MTH 256', topicIds: [], targetTopicIds: [1, 3] },
    { id: 'vc', code: 'MTH 255', topicIds: [], targetTopicIds: [2, 3] },
    { id: 'la', code: 'MTH 341', topicIds: [5], targetTopicIds: [4] },
  );
}

function addWeekSchedule(c) {
  c.installTargetCalendar([
    { due: '2026-09-30T06:59:59Z', courseId: 'de', topicIds: [1, 3] },
    { due: '2026-10-16T06:59:59Z', courseId: 'vc', topicIds: [2, 3] },
    { due: null, courseId: 'la', topicIds: [5] },
  ]);
}

test('week clicks and Shift-click ranges change target roots while retaining depth, Split, and learner selections', () => {
  const c = fixture([1, 2, 3, 5]); addSchoolCourses(c); addWeekSchedule(c);
  c.changeCourse(null, true, 'targets'); c.setDepth(1); c.setTargetSplit(true);
  const learner=JSON.stringify(c.snapshot.learner);
  const buttons=c.$('targetWeekButtons').children;
  assert.equal(buttons.length, 3);
  assert.match(buttons[0].attributes['aria-label'], /Week 1 - 9\/27-10\/03 · 2 due/);
  buttons[0].listeners.click({ shiftKey:false });
  assert.deepEqual([...c.courseFilteredTargetIds()], [1, 2, 3, 5]);
  assert.deepEqual([...c.filteredTargetIds()], [1, 3]);
  assert.deepEqual([...c.buildActiveSet().nodeIds], [1, 3, 4]); // Existing depth expansion remains.
  assert.equal(c.state.depth, '1'); assert.equal(c.$('targetSplitToggle').attributes['aria-checked'], 'true');
  assert.equal(buttons[0].attributes['aria-pressed'], 'true');
  buttons[2].listeners.click({ shiftKey:true });
  assert.deepEqual([...c.filteredTargetIds()], [1, 2, 3]);
  assert.equal(buttons[1].attributes['aria-pressed'], 'true'); // Empty intervening week is selected too.
  assert.match(c.$('targetWeekReadout').textContent, /Weeks 1–3 - 9\/27-10\/17 · 3 due · 0 queued/);
  assert.equal(JSON.stringify(c.snapshot.learner), learner);
  const saved=JSON.parse(c.storage.get('course-academy.graph-target-weeks'));
  assert.equal(saved.kind, 'range'); assert.equal(saved.end-saved.start, 14);
  c.$('targetWeeksUnscheduled').listeners.click();
  assert.deepEqual([...c.filteredTargetIds()], [5]);
  c.$('targetWeeksAll').listeners.click();
  assert.deepEqual([...c.filteredTargetIds()], [1, 2, 3, 5]);
});

test('calendar navigation is keyboard accessible and week counts react to course filters and target edits', () => {
  const c=fixture([1, 2, 3, 5]); addSchoolCourses(c); addWeekSchedule(c); c.changeCourse(null,true,'targets');
  const buttons=c.$('targetWeekButtons').children;
  let prevented=0,stopped=0;
  buttons[0].listeners.keydown({key:'ArrowRight',preventDefault(){prevented++;},stopPropagation(){stopped++;}});
  assert.equal(buttons[1].focused,true); assert.equal(buttons[1].tabIndex,0);
  assert.equal(prevented,1); assert.equal(stopped,1);
  assert.deepEqual([...c.filteredTargetIds()], [1,2,3,5]); // Moving focus does not select.
  buttons[0].listeners.click({shiftKey:false});
  buttons[2].listeners.keydown({key:'Enter',shiftKey:true,preventDefault(){},stopPropagation(){}});
  assert.deepEqual([...c.filteredTargetIds()], [1,2,3]);
  c.setTargetCourseEnabled('256',false);
  assert.deepEqual([...c.filteredTargetIds()], [2,3]);
  assert.match(buttons[0].title,/0 due/); // Shared topic 3's Week 1 assignment is in disabled MTH 256.
  c.learnerChanged({...c.snapshot.learner,targets:[1,2,5]});
  assert.match(c.$('targetWeekReadout').textContent,/1 due · 0 queued$/);
  c.changeCourse('course-a');assert.equal(c.$('targetWeekStrip').hidden,true);
});

test('Split switch persists and retains the selected topics, depth, history, URL, and learner membership', () => {
  const c = fixture(); addSchoolCourses(c); c.changeCourse(null, true, 'targets'); c.setDepth(2);
  c.snapshot.learner.queue = [4];
  const active = [...c.state.activeIds], history = c.state.history, url = c.location.href;
  const learner = JSON.stringify(c.snapshot.learner);
  c.$('targetSplitToggle').listeners.click();
  assert.equal(c.$('targetSplitToggle').attributes['aria-checked'], 'true');
  assert.equal(c.$('targetSplitToggle').dataset.animate, 'true');
  assert.equal(c.storage.get('course-academy.graph-targets-split'), 'true');
  assert.deepEqual([...c.state.activeIds], active);
  assert.equal(c.state.depth, '2'); assert.equal(c.state.history, history);
  assert.equal(c.location.href, url); assert.equal(JSON.stringify(c.snapshot.learner), learner);
  assert.equal(c.redraws.at(-1), true);
  const restored = fixture([1, 3], { splitSaved: c.storage.get('course-academy.graph-targets-split') });
  addSchoolCourses(restored); restored.changeCourse(null, true, 'targets');
  assert.equal(restored.$('targetSplitToggle').attributes['aria-checked'], 'true');
  assert.ok(restored.layoutCurrent().courseBands.length);
  c.setTargetSplit(false); assert.equal(c.$('targetSplitToggle').attributes['aria-checked'], 'false');
  assert.equal(c.storage.get('course-academy.graph-targets-split'), 'false');
});

test('split layout vertically separates labeled courses and keeps all nodes and cross-course links exactly once', () => {
  const c = fixture([1, 2, 3, 4, 5, 6]); addSchoolCourses(c); c.changeCourse(null, true, 'targets');
  const combined = c.layoutCurrent();
  c.setTargetSplit(true); const split = c.layoutCurrent(); c.renderGuides();
  assert.deepEqual(Array.from(split.courseBands, band => band.label), ['MTH 255', 'MTH 256', 'MTH 341']);
  assert.deepEqual(Array.from(split.courseBands, band => [...band.nodeIds]), [[2], [1, 3], [4, 5, 6]]);
  assert.deepEqual(Array.from(split.activeNodes, node => node.id), Array.from(combined.activeNodes, node => node.id));
  assert.deepEqual(Array.from(split.activeLinks, edge => edge.index), Array.from(combined.activeLinks, edge => edge.index));
  assert.equal(split.pos.size, split.activeNodes.length);
  for (const [index, band] of split.courseBands.entries()) {
    if (index) assert.ok(split.courseBands[index - 1].y + split.courseBands[index - 1].height < band.y);
    for (const id of band.nodeIds) {
      const box = split.pos.get(id);
      assert.ok(box.y >= band.y + 32 && box.y + box.h <= band.y + band.height);
      assert.equal(box.x, combined.pos.get(id).x);
      assert.equal(box.col, combined.pos.get(id).col);
    }
    assert.equal(c.guidesG.children[index].children[1].textContent, band.label + ' · ' + band.nodeIds.size + ' topics');
    assert.ok(split.bounds.y1 <= band.y && split.bounds.y2 >= band.y + band.height);
  }
  for (const edge of split.activeLinks) {
    assert.ok(split.pos.get(edge.source).col < split.pos.get(edge.target).col);
    assert.ok(edge.segments.every(segment => [...segment.p0, ...segment.c1, ...segment.c2, ...segment.p1].every(Number.isFinite)));
    assert.ok(edge.segments.every(segment => segment.p0[0] <= segment.c1[0] && segment.c1[0] <= segment.c2[0] && segment.c2[0] <= segment.p1[0]));
  }
  c.setTargetSplit(false); const again = c.layoutCurrent(); c.renderGuides();
  assert.equal(again.courseBands.length, 0); assert.equal(c.guidesG.children.length, 0);
  for (const [id, box] of combined.pos) assert.deepEqual(again.pos.get(id), box);
});

function configureCourseBands(c, memberships, edges) {
  c.snapshot.courses = ['256', '255', '341'].map((code, i) => ({ id: code, code: 'MTH ' + code, topicIds: memberships[i] }));
  c.LINKS.splice(0, c.LINKS.length, ...edges.map(([source, target]) => ({ source, target })));
  for (const node of c.NODES) {
    c.inMap.set(node.id, c.LINKS.filter(edge => edge.target === node.id).map(edge => edge.source));
    c.outMap.set(node.id, c.LINKS.filter(edge => edge.source === node.id).map(edge => edge.target));
  }
}
function coursePlacements(c, ids = c.NODES.map(node => node.id)) {
  return new Map(Array.from(c.targetCourseBands(new Set(ids)), band =>
    Array.from(band.nodeIds, id => [id, band.key])).flat());
}

test('excluded low-layer targets and queue topics do not inflate track workloads', () => {
  const c = fixture([1, 2, 3, 4, 5, 6]); c.snapshot.learner.queue = [1];
  configureCourseBands(c, [[1], [2], [3]], []);
  c.nodeById.get(1).layer = 28;
  c.changeCourse(null, true, 'targets');
  const placement = coursePlacements(c, c.buildActiveSet().nodeIds);
  assert.equal(placement.has(1), false);
  assert.equal(placement.get(4), '256');
  assert.equal(placement.get(5), '255');
  assert.equal(placement.get(6), '256');
});

test('course distance crosses hidden nodes in either direction and wins over lighter workloads', () => {
  const c = fixture([1, 2, 3, 4]);
  configureCourseBands(c, [[1], [2, 3], []], [[5, 1], [5, 4], [2, 4]]);
  assert.equal(coursePlacements(c, [4]).get(4), '255'); // One hop to 255, two to 256, none to empty 341.
  configureCourseBands(c, [[1], [2, 3], []], [[5, 1], [5, 4]]);
  assert.equal(coursePlacements(c, [4]).get(4), '256'); // Reverse through hidden node 5.
});

test('shared topics choose the lighter of their equally near associated courses', () => {
  const c = fixture([1, 2, 4, 5]);
  configureCourseBands(c, [[1, 4, 5], [2, 4], [3]], [[1, 4], [2, 4], [3, 4]]);
  const placement = coursePlacements(c);
  assert.equal(placement.get(4), '255'); // 256 has two roots; 255 has one. Empty 341 is not an associated candidate.
  assert.equal(placement.get(5), '256'); // Explicit single-course membership stays anchored.
});

test('disconnected and tied roots balance sequentially using unique saved targets and queue topics', () => {
  const c = fixture([1, 2, 3, 4, 5, 6]);
  c.snapshot.learner.queue = [1, 1]; // Repeated and overlapping membership adds no extra workload.
  configureCourseBands(c, [[1], [2], [3]], []);
  const expected = new Map([[2, '255'], [4, '255'], [1, '256'], [5, '256'], [3, '341'], [6, '341']]);
  assert.deepEqual(coursePlacements(c), expected);
  c.snapshot.learner.targets.reverse();
  assert.deepEqual(coursePlacements(c, [6, 5, 4, 3, 2, 1]), expected);
  configureCourseBands(c, [[1], [2], [3]], [[1, 4], [2, 4], [3, 4], [1, 5], [2, 5], [3, 5], [1, 6], [2, 6], [3, 6]]);
  assert.deepEqual(coursePlacements(c), expected); // Equal distance follows the same balancing rule.
});

test('expanded prerequisites follow placed roots even without original course anchors and do not change workload', () => {
  const c = fixture([2, 3, 5]);
  configureCourseBands(c, [[], [], []], [[4, 1], [1, 3], [6, 2]]);
  c.changeCourse(null, true, 'targets'); c.setTargetSplit(true);
  const overview = coursePlacements(c, c.buildActiveSet().nodeIds);
  assert.deepEqual(overview, new Map([[2, '255'], [3, '256'], [5, '341']]));
  c.setDepth(1, true);
  const shallow = coursePlacements(c, c.buildActiveSet().nodeIds);
  assert.equal(shallow.get(1), '256'); assert.equal(shallow.get(6), '255');
  c.setDepth(2, true);
  const deep = coursePlacements(c, c.buildActiveSet().nodeIds);
  assert.equal(deep.get(4), '256');
  for (const [id, code] of shallow) assert.equal(deep.get(id), code);
  for (const [id, code] of overview) assert.equal(deep.get(id), code);
  assert.deepEqual(Array.from(c.layoutCurrent().courseBands, band => band.key), ['255', '256', '341']);
});

test('week, course, Queue visibility, and focus changes keep placements based on the saved workload', () => {
  const c = fixture([1, 2, 3, 4, 5, 6]); addSchoolCourses(c); addWeekSchedule(c);
  c.snapshot.learner.queue = [4]; c.changeCourse(null, true, 'targets');
  const expected = coursePlacements(c);
  c.$('targetWeekButtons').children[0].listeners.click({ shiftKey: false });
  c.setTargetCourseEnabled('341', false); c.setTargetQueueEnabled(false);
  c.setDepth(2, true); c.setSelected(1);
  for (const [id, code] of coursePlacements(c, c.buildActiveSet().nodeIds)) assert.equal(code, expected.get(id));
});

test('expanded prerequisites receive course tracks without adding hidden topics and respect course filters', () => {
  const c = fixture([2, 3]); addSchoolCourses(c);
  c.snapshot.courses.find(course => course.code === 'MTH 256').targetTopicIds = [3];
  c.snapshot.courses.find(course => course.code === 'MTH 255').targetTopicIds = [2];
  c.snapshot.courses.find(course => course.code === 'MTH 341').targetTopicIds = [];
  c.snapshot.learner.queue = [4, 6]; c.changeCourse(null, true, 'targets'); c.setTargetSplit(true);
  c.setTargetQueueEnabled(false);
  assert.deepEqual(Array.from(c.layoutCurrent().activeNodes, node => node.id), [2, 3]);
  c.setDepth(2, true); let layout = c.layoutCurrent();
  assert.deepEqual([...layout.courseBands.find(band => band.key === '256').nodeIds], [3]);
  assert.deepEqual([...layout.courseBands.find(band => band.key === '255').nodeIds].sort(), [1, 2, 4]);
  assert.equal(layout.pos.has(6), false);
  c.setSelected(1); layout = c.layoutCurrent();
  assert.deepEqual(Array.from(layout.courseBands, band => band.label), ['MTH 255']);
  c.setTargetCourseEnabled('255', false); layout = c.layoutCurrent();
  assert.deepEqual(Array.from(layout.courseBands, band => band.label), ['MTH 255', 'MTH 256']);
  assert.deepEqual([...layout.courseBands[0].nodeIds].sort(), [1, 4]);
  assert.deepEqual([...layout.courseBands[1].nodeIds], [3]);
  assert.deepEqual([...c.state.activeIds], [3]);
  assert.equal(c.$('targetSplitToggle').attributes['aria-checked'], 'true');
  assert.equal(c.state.depth, '2');
});

test('empty targets and regular course views remain usable with the Split preference enabled', () => {
  const c = fixture([], { splitSaved: 'true' }); addSchoolCourses(c); c.changeCourse(null, true, 'targets');
  const empty = c.layoutCurrent(); c.renderGuides();
  assert.equal(empty.courseBands.length, 0); assert.equal(empty.activeNodes.length, 0);
  assert.ok(Object.values(empty.bounds).every(Number.isFinite));
  c.changeCourse('course-a'); const course = c.layoutCurrent();
  assert.equal(c.$('targetCourseFilters').hidden, true);
  assert.equal(course.courseBands.length, 0);
  assert.deepEqual(Array.from(course.activeNodes, node => node.id), [1, 2]);
  c.setTargetSplit(false); c.changeCourse(null, true, 'targets');
  assert.equal(c.$('targetSplitToggle').attributes['aria-checked'], 'true');
});

test('revisited layouts reuse routing and text measurements without changing selection distances or course bands', () => {
  const c=fixture([1,2,3,4,5,6]); addSchoolCourses(c); c.changeCourse(null,true,'targets');
  const combined=c.layoutCurrent();
  c.setTargetSplit(true);const split=c.layoutCurrent();
  c.setTargetSplit(false);const cached=c.layoutCurrent();
  assert.equal(cached.rowOrdering.layoutCached,true);
  assert.equal(cached.pos,combined.pos);assert.equal(cached.activeLinks,combined.activeLinks);
  c.setTargetSplit(true);assert.equal(c.layoutCurrent().pos,split.pos);
  // A changed ownership mapping requires a new split layout even if the
  // same nodes and columns remain visible.
  c.snapshot.courses.find(course=>course.code==='MTH 256').targetTopicIds=[1];
  const changed=c.layoutCurrent();
  assert.notEqual(changed.pos,split.pos);
  assert.equal(changed.courseBands.find(band=>band.key==='255').nodeIds.has(3),true);
  assert.ok(c.layoutCache.size<=12);
  const geometry=changed.pos.get(1).geometry;
  c.layoutCache.clear();c.nodeGeometryCache.clear();
  assert.notEqual(c.layoutCurrent().pos.get(1).geometry,geometry);
});

test('course switches filter assignment targets, preserve shared targets and leave saved membership intact', () => {
  const c = fixture([1, 2, 3, 4, 5, 6]); addSchoolCourses(c);
  const saved = [...c.snapshot.learner.targets];
  c.changeCourse(null, true, 'targets');
  assert.equal(c.$('targetCourseFilters').hidden, false);
  // Exercise the actual click handler and switch accessibility state.
  c.$('targetCourseToggle256').listeners.click();
  assert.equal(c.$('targetCourseToggle256').attributes['aria-checked'], 'false');
  assert.deepEqual([...c.buildActiveSet().nodeIds], [2, 3, 4, 5, 6]);
  assert.equal(c.$('targetCourseToggle256').dataset.animate, 'true');
  c.setTargetCourseEnabled('341', false);
  assert.deepEqual([...c.buildActiveSet().nodeIds], [2, 3, 6]);
  c.setTargetCourseEnabled('255', false);
  assert.deepEqual([...c.buildActiveSet().nodeIds], [6]);
  assert.equal(c.buildActiveSet().edgeSet.size, 0);
  assert.equal(c.state.selected, 6);
  assert.deepEqual([...c.snapshot.learner.targets], saved);
  assert.equal(c.storage.get('course-academy.graph-target-courses'), '[]');
  for (const code of ['256', '255', '341']) c.setTargetCourseEnabled(code, true);
  assert.deepEqual([...c.buildActiveSet().nodeIds], saved);
});

test('unassigned targets remain across every course and week filter independently of Queue', () => {
  const c = fixture([1, 2, 3, 5, 6]); addSchoolCourses(c); addWeekSchedule(c);
  c.snapshot.learner.queue = [6];
  const saved = JSON.stringify(c.snapshot.learner);
  c.changeCourse(null, true, 'targets'); c.setTargetSplit(true);
  c.setTargetQueueEnabled(false);
  const buttons = c.$('targetWeekButtons').children;
  buttons[0].listeners.click({ shiftKey: false });
  assert.deepEqual([...c.courseTopics], [1, 3, 6]);
  assert.match(c.$('targetWeekReadout').textContent, /2 due$/);
  assert.match(buttons[1].title, /0 due/); // Standing targets do not inflate due counts.
  buttons[1].listeners.click({ shiftKey: false });
  assert.deepEqual([...c.courseTopics], [6]);
  buttons[2].listeners.click({ shiftKey: true });
  assert.deepEqual([...c.courseTopics], [2, 3, 6]);
  for (const code of ['256', '255', '341']) c.setTargetCourseEnabled(code, false);
  for (const button of buttons) {
    button.listeners.click({ shiftKey: false });
    assert.deepEqual([...c.state.activeIds], [6]);
  }
  c.$('targetWeeksUnscheduled').listeners.click();
  assert.deepEqual([...c.courseTopics], [6]);
  c.$('targetWeeksAll').listeners.click();
  assert.deepEqual([...c.courseTopics], [6]);
  assert.deepEqual(Array.from(c.layoutCurrent().courseBands, band => band.label), ['MTH 341']);
  c.setTargetQueueEnabled(true);
  assert.deepEqual([...c.courseTopics], [6]); // Target/queue overlap is drawn once.
  assert.equal(JSON.stringify(c.snapshot.learner), saved);
  c.setTargetQueueEnabled(false);
  c.learnerChanged({ ...c.snapshot.learner, targets: [1, 2, 3, 5] });
  assert.deepEqual([...c.courseTopics], []); // Removing the target removes its standing visibility.
});

test('membership in any curriculum or assignment keeps a target subject to filters', () => {
  const c = fixture([1, 2, 3, 4, 5, 6]); addSchoolCourses(c);
  c.snapshot.courses.find(course => course.code === 'MTH 341').targetTopicIds = [];
  c.installTargetCalendar([
    { due: '2026-09-30T06:59:59Z', courseId: 'de', topicIds: [3] },
    { due: null, courseId: null, topicIds: [4] },
  ]);
  c.changeCourse(null, true, 'targets'); c.setTargetQueueEnabled(false);
  for (const code of ['256', '255', '341']) c.setTargetCourseEnabled(code, false);
  assert.deepEqual([...c.courseTopics], [6]); // Curriculum-only 1/2/5 and undated assignment-only 4 stay filtered.
  c.$('targetWeekButtons').children[0].listeners.click({ shiftKey: false });
  assert.deepEqual([...c.courseTopics], [6]);
  // A newly assigned target stops being a standing target on the next refresh.
  c.installTargetCalendar([
    { due: '2026-09-30T06:59:59Z', courseId: 'de', topicIds: [3, 6] },
    { due: null, courseId: null, topicIds: [4] },
  ]);
  c.refreshTargetScope();
  assert.deepEqual([...c.courseTopics], []);
});

test('Queue switch independently adds queued roots, deduplicates overlaps and persists without requests or membership changes', () => {
  const c = fixture([1, 3]); addSchoolCourses(c);
  c.snapshot.learner.queue = [3, 6, 6, 999];
  const learner = JSON.stringify(c.snapshot.learner);
  c.changeCourse(null, true, 'targets');
  assert.deepEqual([...c.courseTopics], [1, 3, 6]);
  for (const code of ['256', '255', '341']) c.setTargetCourseEnabled(code, false);
  assert.deepEqual([...c.courseTopics], [3, 6]);
  assert.equal(c.$('targetQueueToggle').attributes['aria-checked'], 'true');
  c.setDepth(2); c.exploreTopic({ id: 6 });
  c.$('targetQueueToggle').listeners.click();
  assert.equal(c.$('targetQueueToggle').attributes['aria-checked'], 'false');
  assert.equal(c.$('targetQueueToggle').dataset.animate, 'true');
  assert.equal(c.buildActiveSet().nodeIds.size, 0);
  assert.equal(c.state.depth, '2');
  assert.equal(c.state.history.length, 1);
  assert.equal(c.location.href, 'http://example.test/?view=targets');
  assert.equal(c.storage.get('course-academy.graph-target-queue'), 'false');
  assert.equal(JSON.stringify(c.snapshot.learner), learner);
  c.setTargetCourseEnabled('256', true);
  assert.deepEqual([...c.courseTopics], [1, 3]); // Shared target survives Queue being off.
  c.setTargetQueueEnabled(true);
  assert.deepEqual([...c.courseTopics], [1, 3, 6]);
  const restored = fixture([1], { queueSaved: 'false' });
  restored.snapshot.learner.queue = [6]; restored.changeCourse(null, true, 'targets');
  assert.deepEqual([...restored.courseTopics], [1]);
  assert.equal(restored.$('targetQueueToggle').attributes['aria-checked'], 'false');
  restored.changeCourse('course-a'); restored.setTargetQueueEnabled(true);
  assert.equal(restored.$('targetCourseFilters').hidden, true);
  assert.deepEqual([...restored.courseTopics], [1, 2]);
});

test('queue-only views remain visible across every week and refresh roots on queue edits and rollbacks', () => {
  const c = fixture([]); addSchoolCourses(c); addWeekSchedule(c);
  c.snapshot.learner.queue = [2, 6]; c.changeCourse(null, true, 'targets');
  for (const code of ['256', '255', '341']) c.setTargetCourseEnabled(code, false);
  assert.deepEqual([...c.courseTopics], [2, 6]);
  assert.equal(c.$('targetWeekReadout').textContent, 'All weeks · 0 targets · 2 queued');
  const buttons = c.$('targetWeekButtons').children;
  for (const button of buttons) {
    assert.match(button.attributes['aria-label'], /0 due/);
    button.listeners.click({ shiftKey: false });
    assert.deepEqual([...c.courseTopics], [2, 6]);
    assert.match(c.$('targetWeekReadout').textContent, /0 due · 2 queued$/);
  }
  c.$('targetWeeksUnscheduled').listeners.click();
  assert.deepEqual([...c.courseTopics], [2, 6]);
  assert.equal(c.$('targetWeekReadout').textContent, 'Unscheduled · 0 targets · 2 queued');
  c.queueChanged({ queue: [2] });
  assert.deepEqual([...c.state.activeIds], [2]);
  assert.match(c.$('targetWeekReadout').textContent, /1 queued$/);
  c.queueChanged({ queue: [2, 6] });
  assert.deepEqual([...c.state.activeIds], [2, 6]);
  assert.deepEqual([...c.snapshot.learner.targets], []);
});

test('week filters apply to course targets while Queue stays visible, counts separately and deduplicates overlaps', () => {
  const c = fixture([1, 2, 3, 5]); addSchoolCourses(c); addWeekSchedule(c);
  c.snapshot.learner.queue = [3, 6, 6, 999];
  c.changeCourse(null, true, 'targets');
  const saved = JSON.stringify(c.snapshot.learner);
  const buttons = c.$('targetWeekButtons').children;
  buttons[0].listeners.click({ shiftKey: false });
  assert.deepEqual([...c.courseTopics], [1, 3, 6]);
  assert.match(c.$('targetWeekReadout').textContent, /2 due · 2 queued$/);
  assert.match(buttons[0].title, /2 due/);
  assert.match(buttons[1].title, /0 due/);
  buttons[1].listeners.click({ shiftKey: false });
  assert.deepEqual([...c.courseTopics], [3, 6]);
  assert.match(c.$('targetWeekReadout').textContent, /0 due · 2 queued$/);
  buttons[2].listeners.click({ shiftKey: true });
  assert.deepEqual([...c.courseTopics], [2, 3, 6]);
  assert.match(c.$('targetWeekReadout').textContent, /2 due · 2 queued$/);
  c.$('targetWeeksUnscheduled').listeners.click();
  assert.deepEqual([...c.courseTopics], [5, 3, 6]);
  assert.match(c.$('targetWeekReadout').textContent, /1 target · 2 queued$/);
  c.setTargetQueueEnabled(false);
  assert.deepEqual([...c.courseTopics], [5]);
  assert.equal(c.$('targetWeekReadout').textContent, 'Unscheduled · 1 target');
  buttons[0].listeners.click({ shiftKey: false });
  assert.deepEqual([...c.courseTopics], [1, 3]);
  assert.match(c.$('targetWeekReadout').textContent, /2 due$/);
  c.setTargetQueueEnabled(true);
  assert.deepEqual([...c.courseTopics], [1, 3, 6]);
  assert.equal(JSON.stringify(c.snapshot.learner), saved);
});

test('removing a queued topic keeps focused exploration while updating overview membership', () => {
  const c = fixture([3]);
  c.snapshot.learner.queue = [6]; c.changeCourse(null, true, 'targets');
  c.exploreTopic({ id: 6 }); c.setDepth(2);
  const history = c.state.history, url = c.location.href;
  c.queueChanged({ queue: [] });
  assert.deepEqual([...c.courseTopics], [3]);
  assert.deepEqual([...c.state.activeIds], [6]);
  assert.equal(c.state.depth, '2');
  assert.equal(c.state.history, history);
  assert.equal(c.location.href, url);
  c.resetView();
  assert.deepEqual([...c.state.activeIds], [3]);
});

test('filtering clears excluded focus/history while retaining prerequisite depth and cross-course dependencies', () => {
  const c = fixture([2, 3, 4]); addSchoolCourses(c);
  c.changeCourse(null, true, 'targets'); c.exploreTopic({ id: 4 }); c.setDepth(2);
  c.setTargetCourseEnabled('341', false);
  assert.equal(c.state.depth, '2');
  assert.deepEqual([...c.state.activeIds], [2, 3]);
  assert.equal(c.state.followTargets, true);
  assert.equal(c.state.history.length, 1);
  assert.equal(c.location.href, 'http://example.test/?view=targets');
  // Topic 4 is no longer a target root but is still a required prerequisite.
  assert.equal(c.buildActiveSet().nodeIds.has(4), true);
  c.setDepth(0, true);
  assert.deepEqual([...c.buildActiveSet().nodeIds], [2, 3]);
  c.learnerChanged({ targets: [1, 4, 5] });
  assert.deepEqual([...c.buildActiveSet().nodeIds], [1]);
  c.resetView();
  assert.deepEqual([...c.buildActiveSet().nodeIds], [1]);
  c.changeCourse('course-a');
  assert.equal(c.$('targetCourseFilters').hidden, true);
  assert.deepEqual([...c.buildActiveSet().nodeIds], [1, 2]);
});

test('target depth expands only through prerequisites, excluding dependents and siblings', () => {
  const c = fixture([3]);
  c.changeCourse(null, true, 'targets');
  c.setDepth(1, true);
  assert.deepEqual([...c.buildActiveSet().nodeIds], [3, 1]);
  c.setDepth(2, true);
  const active = c.buildActiveSet();
  assert.deepEqual([...active.nodeIds], [3, 1, 4]);
  assert.equal(active.downstream.size, 0);
  assert.equal(active.columns.get(4) < active.columns.get(1), true);
  assert.equal(active.columns.get(1) < active.columns.get(3), true);
  c.setDepth(0, true);
  assert.deepEqual([...c.buildActiveSet().nodeIds], [3]);
});

test('multiple targets anchor at the right edge when a prerequisite lies between them', () => {
  const c = fixture([1, 5]);
  c.changeCourse(null, true, 'targets');
  c.setDepth(2, true);
  const active = c.buildActiveSet();
  // 1 -> 3 -> 5: topic 3 is a prerequisite of target 5, and a dependent of target 1.
  assert.deepEqual([...active.nodeIds], [1, 5, 4, 3]);
  assert.equal(active.downstream.size, 0);
  assert.equal(active.columns.get(5), 0);
  assert.equal([...active.columns.values()].every(column => column <= 0), true);
  assert.equal(active.columns.get(4) < active.columns.get(1), true);
  assert.equal(active.columns.get(1) < active.columns.get(3), true);
  assert.equal(active.columns.get(3) < active.columns.get(5), true);
});

test('focused stacks retain global layer order while collapsing layers without visible dependencies', () => {
  for (const targeted of [false, true]) {
    const c = fixture(); c.targetsView = targeted;
    const columns = c.assignScopedColumns(new Set([4, 5, 6]), new Map(), new Map(), 5);
    // 4 -> 6 needs two stacks; later-layer topic 5 shares the second stack
    // instead of moving back into the first because its prerequisites are hidden.
    assert.equal(columns.get(6), columns.get(4) + 1);
    assert.equal(columns.get(5), columns.get(6));
    assert.equal(new Set(columns.values()).size, 2);
    assert.equal(c.nodeById.get(5).layer, 32);
  }
});

test('a dependency between merged layers separates the entire next global layer', () => {
  const c = fixture();
  c.nodeById.get(4).layer = 0;
  c.nodeById.get(6).layer = 10;
  c.nodeById.get(1).layer = 20;
  c.nodeById.get(2).layer = 20;
  c.nodeById.get(3).layer = 30;
  c.nodeById.get(5).layer = 40;
  // The first two layers can merge. The edge 4 -> 1 starts the next stack,
  // even though it originates two global layers earlier. Topic 2 stays with 1.
  c.inMap.set(6, []); c.outMap.set(4, [1]);
  c.inMap.set(2, []); c.outMap.set(1, [3]);
  const columns = c.assignScopedColumns(new Set([4, 6, 1, 2, 3, 5]), new Map(), new Map(), 4);
  assert.equal(columns.get(4), 0);
  assert.equal(columns.get(6), 0);
  assert.equal(columns.get(1), 1);
  assert.equal(columns.get(2), 1);
  assert.equal(columns.get(3), 2);
  assert.equal(columns.get(5), 3);
});

test('unrelated layers and empty layer gaps collapse to one stack deterministically', () => {
  const c = fixture();
  c.inMap.set(1, []); c.outMap.set(1, []); c.outMap.set(3, []); c.inMap.set(5, []);
  c.nodeById.get(1).layer = 5; c.nodeById.get(3).layer = 25; c.nodeById.get(5).layer = 90;
  c.inMap.set(3, []);
  for (const ids of [new Set([1, 3, 5]), new Set([5, 3, 1])]) {
    const columns = c.assignScopedColumns(ids, new Map(), new Map(), 3);
    assert.equal(new Set(columns.values()).size, 1);
    assert.equal(columns.get(1), 0);
    assert.equal(columns.get(5), 0);
  }
});

test('shortcut edges may span columns when another visible prerequisite chain requires it', () => {
  const c = fixture();
  c.inMap.get(5).push(1); c.outMap.get(1).push(5);
  const ids = new Set([1, 3, 5]);
  c.state.activeIds = new Set(ids);
  const columns = c.assignScopedColumns(ids, new Map(), new Map(), 1);
  assert.equal(columns.get(1), 0);
  assert.equal(columns.get(3), 1);
  assert.equal(columns.get(5), 2);
});

test('topic selection, history, and reset retain prerequisite-only targets behavior', () => {
  const c = fixture();
  c.changeCourse(null, true, 'targets');
  c.setSelected(3);
  c.setDepth(2, true);
  assert.equal(c.state.mode, 'upstream');
  assert.deepEqual([...c.buildActiveSet().nodeIds], [3, 1, 4]);
  c.jumpHistory(0);
  assert.equal(c.state.mode, 'upstream');
  assert.deepEqual([...c.state.activeIds], [1, 3]);
  c.resetView();
  assert.equal(c.state.depth, '0');
  assert.deepEqual([...c.buildActiveSet().nodeIds], [1, 3]);
});

test('course topic exploration still expands in both directions', () => {
  const c = fixture();
  c.changeCourse('course-a');
  c.setSelected(1);
  assert.equal(c.state.mode, 'both');
  const active = c.buildActiveSet();
  assert.deepEqual([...active.nodeIds], [1, 4, 3, 2]);
  assert.equal(active.downstream.has(2), true);
  c.setDepth(0, true);
  assert.equal(c.state.depth, '1');
});

test('empty or absent targets never fall back to the current course or full graph', () => {
  for (const targets of [[], null]) {
    const c = fixture(targets);
    c.changeCourse('course-a', false, 'targets');
    assert.equal(c.buildActiveSet().nodeIds.size, 0);
    assert.equal(c.buildActiveSet().edgeSet.size, 0);
    c.exploreTopic({ id: 2 });
    assert.equal(c.state.selected, null);
    assert.equal(c.targetsView, true);
  }
});

test('learner target changes update the overview, including removing the last target', () => {
  const c = fixture();
  c.changeCourse(null, true, 'targets');
  c.learnerChanged({ targets: [2] });
  assert.deepEqual([...c.buildActiveSet().nodeIds], [2]);
  c.learnerChanged({ targets: [] });
  assert.equal(c.buildActiveSet().nodeIds.size, 0);
});

test('target edits retain overview depth, camera, history, URL, and row ordering', () => {
  const c = fixture(); c.changeCourse(null, true, 'targets'); c.setDepth(2);
  c.state.view = { x: 135, y: -82, k: .75 };
  const view = c.state.view, history = c.state.history, url = c.location.href;
  c.stackOrderCache.set('existing-row-order', [1, 3]);
  c.learnerChanged({ targets: [1, 3, 4] });
  assert.deepEqual([...c.state.activeIds], [1, 3, 4]);
  assert.equal(c.state.depth, '2'); assert.equal(c.state.view, view);
  assert.deepEqual(c.state.view, { x: 135, y: -82, k: .75 });
  assert.equal(c.state.history, history); assert.equal(c.location.href, url);
  assert.deepEqual(c.stackOrderCache.get('existing-row-order'), [1, 3]);
  assert.equal(c.redraws.at(-1), false);
  // Confirmation and a failed-save rollback do not refit the camera either.
  const redraws = c.redraws.length;
  c.learnerChanged({ targets: [1, 3, 4] });
  assert.equal(c.redraws.length, redraws);
  c.learnerChanged({ targets: [1, 3] });
  assert.equal(c.state.depth, '2'); assert.equal(c.state.view, view);
  assert.equal(c.state.selected, 1);
});

test('editing targets during focused exploration repaints without rebuilding or changing selection', () => {
  const c = fixture(); c.changeCourse(null, true, 'targets'); c.setSelected(3); c.setDepth(2);
  c.state.view = { x: 47, y: 62, k: .9 };
  const history = c.state.history, view = c.state.view, redraws = c.redraws.length;
  c.learnerChanged({ targets: [1, 2] });
  assert.deepEqual([...c.courseTopics], [1, 2]);
  assert.deepEqual([...c.state.activeIds], [3]);
  assert.equal(c.state.selected, 3); assert.equal(c.state.depth, '2');
  assert.equal(c.state.mode, 'upstream');
  assert.equal(c.state.history, history); assert.equal(c.state.view, view);
  assert.equal(c.redraws.length, redraws);
  assert.deepEqual([...c.buildActiveSet().nodeIds], [3, 1, 4]);
});

test('a single-target exploration stays focused when another target is added', () => {
  const c = fixture([3]); c.changeCourse(null, true, 'targets'); c.setSelected(3); c.setDepth(2);
  const redraws = c.redraws.length;
  c.learnerChanged({ targets: [3, 1] });
  assert.deepEqual([...c.state.activeIds], [3]);
  assert.equal(c.state.selected, 3); assert.equal(c.state.depth, '2');
  assert.equal(c.redraws.length, redraws);
  c.jumpHistory(0);
  assert.deepEqual([...c.state.activeIds], [3, 1]);
});

test('target deep links preserve scope and switching to a course clears targets mode', () => {
  const c = fixture();
  c.changeCourse(null, true, 'targets');
  c.exploreTopic({ id: 3 });
  assert.equal(c.state.selected, 3);
  assert.equal(c.location.href, 'http://example.test/?view=targets&topic=3');
  c.changeCourse('course-a');
  assert.deepEqual([...c.buildActiveSet().nodeIds], [1, 2]);
  assert.equal(c.location.href, 'http://example.test/?course=course-a');
  assert.equal(c.$('targetsLink').attributes['aria-current'], undefined);
});
