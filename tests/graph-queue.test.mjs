import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

// Actual selection controller and graph menu, with a DOM/API stand-in.
// These tests do not change a live learner or create study attempts.
const controlsSource = (await readFile(new URL('../ui/targets.js', import.meta.url), 'utf8'))
  .replace(/^import .*;\n/m, '').replaceAll('export ', '');
const html = await readFile(new URL('../ui/Math-Academy-Graph-Explorer.html', import.meta.url), 'utf8');
const menuSource = html.slice(html.indexOf('  const nodeContextMenu ='), html.indexOf('\n  function renderNodes()'));
const appearanceSource = html.slice(html.indexOf('  function competencyFor('), html.indexOf('  function paintNode('));

function fixture({ selfDirected = false, queue = [] } = {}) {
  const f = { calls: [], storage: new Map(), events: [], dev: false, fail: false, learner: { id: 'test', selfDirected, queue, targets: [30] } };
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.children = []; this.attrs = {}; this.dataset = {}; this.offsetWidth = 224; this.offsetHeight = 180; this.style = {}; }
    append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
    replaceChildren(...nodes) { for (const node of this.children) node.parent = null; this.children = []; this.append(...nodes); }
    setAttribute(key, value) { this.attrs[key] = String(value); }
    getAttribute(key) { return this.attrs[key] ?? null; }
    removeAttribute(key) { delete this.attrs[key]; }
    get isConnected() { return document.body.contains(this); }
    contains(node) { for (; node; node = node.parent) if (node === this) return true; return false; }
    matches(selector) { return (selector === '.node-hit' || selector === '.menu-new-tab-indicator') ? this.className === selector.slice(1) : selector === '[role="menuitem"]' && this.attrs.role === 'menuitem'; }
    querySelectorAll(selector) { return this.children.flatMap(node => [...(node.matches(selector) ? [node] : []), ...node.querySelectorAll(selector)]); }
    querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
    closest(selector) { for (let node = this; node; node = node.parent) if (selector === '[hidden]' && node.hidden) return node; return null; }
    focus() { document.activeElement = this; }
    getBoundingClientRect() { return { left: 20, bottom: 100, width: 240 }; }
    remove() { if(this.parent) this.parent.children=this.parent.children.filter(child=>child!==this); this.parent=null; }
    click() { if(this.tagName==='a' && this.target==='_blank') f.opened.push([this.href,this.target,this.rel]); if (!this.disabled && !this.closest('[hidden]')) { const event = new Event('click', { cancelable: true }); Object.defineProperty(event, 'detail', { value: 0 }); this.dispatchEvent(event); } }
  }
  const document = new EventTarget(); document.body = new Element('body'); document.hidden = false;
  document.createElement = tag => new Element(tag);
  document.getElementById = id => { const walk = node => node.id === id ? node : node.children.map(walk).find(Boolean); return walk(document.body); };
  const menu = new Element('div'); menu.id = 'nodeContextMenu'; menu.hidden = true;
  for (const id of ['nodeQueueAction', 'nodeTargetAction', 'studyTopicLink', 'goToTopicLink', 'copyNodeButton']) {
    const node = new Element(id.endsWith('Link') ? 'a' : 'div'); node.id = id;
    if (id.endsWith('Link') || id === 'copyNodeButton') node.setAttribute('role', 'menuitem');
    if (id.endsWith('Link')) {
      const arrow = new Element('span'); arrow.className = 'menu-new-tab-indicator'; arrow.hidden = true; node.append(arrow);
    }
    menu.append(node);
  }
  document.body.append(menu);
  for (const id of ['copyNodeNotice', 'manualNodeCopy', 'manualNodeText', 'manualNodeDone']) { const node = new Element('div'); node.id = id; document.body.append(node); }
  const opener = new Element('g'), hit = new Element('rect'); hit.className = 'node-hit'; opener.append(hit); document.body.append(opener);
  f.opened = [];
  const window = new EventTarget(); window.open = () => { throw new Error('Navigation must use a normal link, not a new-window request'); }; window.innerWidth = 1000; window.innerHeight = 900;
  for (const name of ['queue', 'targets']) window.addEventListener(`course-academy:${name}-changed`, () => f.events.push(name));
  const context = vm.createContext({ document, window, Event, CustomEvent, crypto, setTimeout, clearTimeout, navigator: {},
    snapshot: { learner: structuredClone(f.learner) }, courseId: 'course',
    targetsView: false, targetsInRed: true, repetitions: { 20: 5 }, isLightTheme: () => false, themeColor: color => color,
    PALETTE: ['#000000', '#303030', '#5A5A5A', '#858585', '#AEAEAE', '#D6D6D6', '#FFFFFF'],
    topicReferenceURL: (_snapshot, node) => '/topic?topic=' + node.uuid,
    $: document.getElementById, isDeveloperMode: () => f.dev, developerModeReady: Promise.resolve(),
    localStorage: { setItem: (key, value) => f.storage.set(key, value) },
    readLearner: async () => structuredClone(f.learner),
    fetch: async (path, options) => {
      const body = JSON.parse(options.body); f.calls.push({ path, body });
      if (f.hold) await f.hold;
      const collection = path === '/api/queue-topic' ? 'queue' : 'targets';
      const selected = new Set(f.learner[collection]);
      if (body.selected) selected.add(body.topicId); else selected.delete(body.topicId);
      f.learner[collection] = [...selected];
      if (f.fail) { f.fail = false; throw new Error('Reply lost after commit'); }
      return { ok: true, json: async () => ({ learner: structuredClone(f.learner) }) };
    },
  });
  f.h = vm.runInContext(`(() => {
    ${controlsSource}
    const queueControls = createQueueControls({ readLearner });
    const targetControls = createTargetControls({ readLearner, onChange: learner => {
      snapshot.learner = { ...snapshot.learner, ...learner };
    } });
    queueControls.setLearner(snapshot.learner); targetControls.setLearner(snapshot.learner);
    ${appearanceSource}
    ${menuSource}
    return { queueControls, targetControls, menu: nodeContextMenu, nodeAppearance };
  })()`, context);
  f.document = document; f.window = window; f.opener = opener;
  f.open = (shiftKey = false) => f.h.menu.open({ id: 20, uuid: 'topic-uuid', name: 'Topic twenty' }, { type: 'contextmenu', shiftKey, clientX: 50, clientY: 70, preventDefault() {}, stopPropagation() {} }, opener);
  f.queueButton = () => document.getElementById('nodeQueueAction').querySelector('[role="menuitem"]');
  return f;
}
const settle = async () => { await new Promise(resolve => setImmediate(resolve)); };

test('graph right-click queues the clicked topic in course mode and restores focus after saving', async () => {
  const f = fixture(); f.open();
  const button = f.queueButton();
  assert.equal(button.textContent, 'Add to queue');
  assert.equal(button.disabled, false);
  assert.equal(f.document.activeElement, button);
  assert.equal(f.document.getElementById('nodeTargetAction').children[0].hidden, true);
  button.click(); await settle();
  assert.equal(f.calls[0].path, '/api/queue-topic');
  assert.equal(f.calls[0].body.action, 'queue-topic');
  assert.equal(f.calls[0].body.topicId, 20);
  assert.equal(f.calls[0].body.selected, true);
  assert.deepEqual(f.learner.targets, [30]);
  assert.deepEqual(f.learner.queue, [20]);
  assert.equal(f.learner.selfDirected, false);
  assert.ok(f.storage.has('course-academy-queue-changed'));
  assert.deepEqual(f.events, ['queue']);
  assert.equal(f.document.getElementById('nodeContextMenu').hidden, true);
  assert.equal(f.document.activeElement, f.opener);
  f.open(); assert.equal(f.queueButton().textContent, 'Remove from queue');
});

test('already queued topics can be removed without changing targets', async () => {
  const f = fixture({ queue: [20], selfDirected: true }); f.open();
  f.queueButton().click(); await settle();
  assert.equal(f.calls[0].body.selected, false);
  assert.deepEqual(f.learner.queue, []);
  assert.deepEqual(f.learner.targets, [30]);
  f.open(); assert.equal(f.queueButton().textContent, 'Add to queue');
});

test('Study now links to the right-clicked topic without changing graph or learner selections', async () => {
  const f = fixture(); f.open();
  const link = f.document.getElementById('studyTopicLink');
  assert.equal(link.href, '/learn?topicId=20');
  const event = new Event('keydown', { cancelable: true });
  Object.defineProperty(event, 'key', { value: 'ArrowDown' });
  f.document.getElementById('nodeContextMenu').dispatchEvent(event);
  assert.equal(f.document.activeElement, link);
  f.h.menu.open({ id: 25, uuid: 'another-topic', name: 'Another topic' }, { type: 'contextmenu', clientX: 50, clientY: 70, preventDefault() {}, stopPropagation() {} }, f.opener);
  assert.equal(link.href, '/learn?topicId=25');
  assert.equal(f.calls.length, 0);
  assert.deepEqual(f.learner.queue, []);
  assert.deepEqual(f.learner.targets, [30]);
  f.dev = true; f.open();
  assert.equal(link.href, '/learn?topicId=20');
});

test('an uncertain queue response retries the same request and intent without duplicates', async () => {
  const f = fixture(); f.fail = true; f.open();
  f.queueButton().click(); await settle();
  assert.equal(f.queueButton().textContent, 'Retry');
  f.queueButton().click(); await settle();
  assert.deepEqual(f.calls[0].body, f.calls[1].body);
  assert.deepEqual(f.learner.queue, [20]);
  assert.deepEqual(f.events, ['queue']);
});

test('developer mode and preference changes disable queue writes', async () => {
  const f = fixture(); f.dev = true; f.open();
  assert.equal(f.queueButton().disabled, true);
  f.queueButton().click(); await settle(); assert.equal(f.calls.length, 0);
  f.dev = false; f.window.dispatchEvent(new Event('course-academy:developer-mode-changed'));
  f.window.dispatchEvent(new Event('course-academy:profile-changing'));
  assert.equal(f.queueButton().disabled, true);
  f.window.dispatchEvent(new CustomEvent('course-academy:profile-changed', { detail: { learner: f.learner, course: { id: 'course' } } }));
  assert.equal(f.queueButton().disabled, false);
});

test('queue changes in another tab refresh the menu from server membership', async () => {
  const f = fixture(); f.open();
  f.learner.queue = [20];
  const event = new Event('storage'); event.key = 'course-academy-queue-changed';
  f.window.dispatchEvent(event); await settle();
  assert.equal(f.queueButton().textContent, 'Remove from queue');
  assert.equal(f.calls.length, 0);
});

test('target actions preserve their endpoint, membership, and mode gating', async () => {
  const f = fixture({ selfDirected: true }); f.open();
  f.document.getElementById('nodeTargetAction').querySelector('[role="menuitem"]').click(); await settle();
  assert.equal(f.calls[0].path, '/api/target');
  assert.equal(f.calls[0].body.action, 'target');
  assert.deepEqual(f.learner.queue, []);
  assert.deepEqual(f.learner.targets, [30, 20]);
  assert.deepEqual(f.events, ['targets']);
});

test('right-click target actions update node color before their background save finishes', async () => {
  const f = fixture({ selfDirected: true }); f.open();
  let release; f.hold = new Promise(resolve => { release = resolve; });
  f.document.getElementById('nodeTargetAction').querySelector('[role="menuitem"]').click();
  assert.equal(f.h.nodeAppearance(20).fill, '#b52b34');
  assert.deepEqual(f.learner.targets, [30]);
  release(); await settle();
  assert.deepEqual(f.learner.targets, [30, 20]);
  assert.equal(f.h.nodeAppearance(20).fill, '#b52b34');
});

test('navigator target switch flips immediately with explicit add and remove labels', async () => {
  const f = fixture({ selfDirected: true });
  const host = f.h.targetControls.createToggle({ id: 20, name: 'Topic twenty' }, { switchControl: true });
  const other = f.h.targetControls.createToggle({ id: 30, name: 'Another target' }, { switchControl: true });
  f.document.body.append(host, other);
  const [label, button] = host.children[0].children;
  const otherButton = other.children[0].children[1];
  assert.equal(button.getAttribute('role'), 'switch');
  assert.equal(button.getAttribute('aria-checked'), 'false');
  assert.equal(button.getAttribute('aria-pressed'), null);
  assert.equal(label.textContent, 'Add to Targets');
  let release; f.hold = new Promise(resolve => { release = resolve; });
  button.click();
  assert.equal(button.getAttribute('aria-checked'), 'true');
  assert.equal(label.textContent, 'Remove from Targets');
  assert.equal(f.h.nodeAppearance(20).fill, '#b52b34');
  assert.deepEqual(f.learner.targets, [30]); // The server has not saved yet.
  assert.equal(button.disabled, true);
  assert.equal(otherButton.getAttribute('aria-checked'), 'true');
  assert.equal(otherButton.dataset.animate, undefined);
  release(); await settle(); f.hold = null;
  assert.equal(button.disabled, false);
  assert.deepEqual(f.learner.targets, [30, 20]);
  assert.equal(f.h.nodeAppearance(20).fill, '#b52b34');
  assert.deepEqual(f.learner.queue, []);
  let removeRelease; f.hold = new Promise(resolve => { removeRelease = resolve; });
  button.click();
  assert.equal(f.h.nodeAppearance(20).fill, '#D6D6D6');
  assert.deepEqual(f.learner.targets, [30, 20]);
  removeRelease(); await settle(); f.hold = null;
  assert.equal(f.calls[1].body.selected, false);
  assert.equal(button.getAttribute('aria-checked'), 'false');
  assert.equal(label.textContent, 'Add to Targets');
  assert.equal(f.h.nodeAppearance(20).fill, '#D6D6D6');
  f.dev = true; f.window.dispatchEvent(new Event('course-academy:developer-mode-changed'));
  assert.equal(button.disabled, true);
});

test('target switch failures restore confirmed membership and replay the same request', async () => {
  const f = fixture({ selfDirected: true });
  const host = f.h.targetControls.createToggle({ id: 20, name: 'Topic twenty' }, { switchControl: true });
  f.document.body.append(host);
  const [label, button] = host.children[0].children;
  f.fail = true; button.click(); await settle();
  assert.equal(button.getAttribute('aria-checked'), 'false');
  assert.equal(label.textContent, 'Add to Targets');
  assert.equal(f.h.nodeAppearance(20).fill, '#D6D6D6');
  assert.match(host.children[1].textContent, /Reply lost/);
  button.click(); await settle();
  assert.deepEqual(f.calls[0].body, f.calls[1].body);
  assert.equal(button.getAttribute('aria-checked'), 'true');
  assert.equal(label.textContent, 'Remove from Targets');
  assert.equal(f.h.nodeAppearance(20).fill, '#b52b34');
  assert.equal(host.children[1].textContent, '');
  assert.deepEqual(f.learner.targets, [30, 20]);
});


function dispatch(target, type, values) {
  const event = new Event(type, { cancelable: true });
  for (const [key, value] of Object.entries(values)) Object.defineProperty(event, key, { value });
  target.dispatchEvent(event);
  return event;
}

test('Shift pressed after opening the graph menu shows navigation arrows only while held', () => {
  const f = fixture(); f.open();
  const links = ['studyTopicLink', 'goToTopicLink'].map(id => f.document.getElementById(id));
  const arrows = links.map(link => link.querySelector('.menu-new-tab-indicator'));
  assert.equal(arrows.every(arrow => arrow.hidden), true);
  dispatch(f.document, 'keydown', { key: 'Shift', shiftKey: true });
  assert.equal(arrows.every(arrow => !arrow.hidden), true);
  assert.equal(links.every(link => /Opens in a new tab/.test(link.getAttribute('aria-label'))), true);
  dispatch(f.document, 'keyup', { key: 'Shift', shiftKey: false });
  assert.equal(arrows.every(arrow => arrow.hidden), true);
  assert.equal(links.some(link => /Opens in a new tab/.test(link.getAttribute('aria-label'))), false);
  assert.equal(f.document.getElementById('nodeContextMenu').hidden, false);
});

test('Shift-click opens either navigation action in a new tab without same-tab navigation or learner writes', () => {
  for (const [id, href] of [['studyTopicLink', '/learn?topicId=20'], ['goToTopicLink', '/topic?topic=topic-uuid']]) {
    const f = fixture(); f.open();
    dispatch(f.document, 'keydown', { key: 'Shift', shiftKey: true });
    const event = dispatch(f.document.getElementById(id), 'click', { shiftKey: true, detail: 1, button: 0 });
    assert.equal(event.defaultPrevented, true);
    assert.deepEqual(f.opened, [[href, '_blank', 'noopener noreferrer']]);
    assert.equal(f.document.getElementById('nodeContextMenu').hidden, true);
    assert.equal(f.calls.length, 0);
    assert.equal(f.document.activeElement, f.opener);
  }
});

test('releasing Shift restores ordinary link navigation; menu reopening and blur clear its state', () => {
  const f = fixture(); f.open(true);
  const link = f.document.getElementById('studyTopicLink'), arrow = link.querySelector('.menu-new-tab-indicator');
  assert.equal(arrow.hidden, false);
  dispatch(f.document, 'keyup', { key: 'Shift', shiftKey: false });
  const event = dispatch(link, 'click', { shiftKey: false, detail: 1, button: 0 });
  assert.equal(event.defaultPrevented, false);
  assert.deepEqual(f.opened, []);
  f.open(true); f.window.dispatchEvent(new Event('blur'));
  assert.equal(arrow.hidden, true);
  f.open(); assert.equal(arrow.hidden, true);
});

test('keyboard activation retains the held Shift modifier and preserves native Control and Meta clicks', () => {
  const f = fixture(); f.open();
  const link = f.document.getElementById('studyTopicLink');
  dispatch(f.document, 'keydown', { key: 'Shift', shiftKey: true });
  dispatch(f.document.getElementById('nodeContextMenu'), 'keydown', { key: ' ', shiftKey: true, target: link });
  assert.deepEqual(f.opened, [['/learn?topicId=20', '_blank', 'noopener noreferrer']]);
  for (const modifier of ['ctrlKey', 'metaKey']) {
    f.open();
    const event = dispatch(link, 'click', { [modifier]: true, shiftKey: false, detail: 1, button: 0 });
    assert.equal(event.defaultPrevented, false);
  }
  assert.equal(f.opened.length, 1);
});
