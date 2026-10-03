import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

// Exercise the actual graph scope and URL code with fixtures, without a server or DB.
const html = await readFile(new URL('../ui/Math-Academy-Graph-Explorer.html', import.meta.url), 'utf8');
const scopeSource = html.slice(html.indexOf('  function selectedCourse()'), html.indexOf('  const coursePicker ='));
const activeSource = html.slice(html.indexOf('  function buildActiveSet()'), html.indexOf('  // Keep dependency columns fixed.'));
const helperSource = html.slice(html.indexOf('  function isScoped()'), html.indexOf('  function titleWrap('));
const columnSource = html.slice(html.indexOf('  function assignScopedColumns('), html.indexOf('  function buildActiveSet()'));
const selectionSource = html.slice(html.indexOf('  function selectionSnapshot()'), html.indexOf('  let MAX_DEPTH='));
const depthSource = html.slice(html.indexOf('  function setDepth('), html.indexOf('  function handleDepthWheel('));
const resetSource = html.slice(html.indexOf('  function resetView()'), html.indexOf('  function fitToBounds('));
const changeSource = html.slice(html.indexOf('    onChange: learner => {') + '    onChange: learner => {'.length, html.indexOf('\n    },\n  });'));

function fixture(targets = [1, 3]) {
  const element = () => ({
    attributes: {}, children: [], classList: { toggle() {} },
    setAttribute(key, value) { this.attributes[key] = value; },
    removeAttribute(key) { delete this.attributes[key]; },
    replaceChildren() { this.children = []; },
    appendChild(child) { this.children.push(child); },
  });
  const elements = new Map();
  const $ = id => { if (!elements.has(id)) elements.set(id, element()); return elements.get(id); };
  const nodes = [1, 2, 3, 4, 5, 6].map(id => ({ id, name: `Topic ${id}`, layer: id, order: 0 }));
  const links = [{ source: 1, target: 3 }, { source: 1, target: 2 }, { source: 4, target: 1 }, { source: 3, target: 5 }, { source: 4, target: 6 }];
  const context = vm.createContext({
    URL, $, document: { createElement: element, getElementById: $, title: '' },
    location: { href: 'http://example.test/?view=targets&course=course-a&topic=2' },
    snapshot: { learner: { targets, courseId: 'course-a' }, courses: [{ id: 'course-a', title: 'Course A', topicIds: [1, 2] }] },
    NODES: nodes, LINKS: links,
    dependencyOrder: [4, 1, 2, 3, 5, 6],
    inMap: new Map(nodes.map(n => [n.id, links.filter(e => e.target === n.id).map(e => e.source)])),
    outMap: new Map(nodes.map(n => [n.id, links.filter(e => e.source === n.id).map(e => e.target)])),
    nodeById: new Map(nodes.map(n => [n.id, n])),
    courseId: null, targetsView: false, courseTopics: new Set(), loading: false, targetTopicId: null,
    state: { activeIds: new Set(), selected: null }, pendingDepthFrame: 0, MAX_DEPTH: 10,
    stackOrderCache: new Map(), STARTER_TOPIC_IDS: [],
    titleReaderboards: { clear() {}, set() {} },
    resetDepthWheel() {}, resize() {}, redraw() {}, scheduleDepthLayout() {},
  });
  context.history = { replaceState(_state, _title, url) { context.location.href = String(url); } };
  vm.runInContext(`${helperSource}\n${columnSource}\n${selectionSource}\n${depthSource}\n${resetSource}\n${scopeSource}\n${activeSource}\nfunction learnerChanged(learner) { ${changeSource} }`, context);
  return context;
}

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
