import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

// Actual selection controllers and graph color callbacks with a DOM/API stand-in.
// Menu interactions use the real browser DOM in entity-menu-browser.cjs.
// These tests do not change a live learner or create study attempts.
const controlsSource = (await readFile(new URL('../ui/targets.js', import.meta.url), 'utf8'))
  .replace(/^import .*;\n/gm, '').replaceAll('export ', '');
const html = await readFile(new URL('../ui/Math-Academy-Graph-Explorer.html', import.meta.url), 'utf8');

const statusPaletteSource = html.slice(html.indexOf('  const STATUS_PALETTES ='), html.indexOf('  let snapshot ='));
const appearanceSource = html.slice(html.indexOf('  function competencyFor('), html.indexOf('  function paintNode('));
const queueStart = html.indexOf('    onChange: learner => {', html.indexOf('  const queueControls ='));
const queueChanged = html.slice(queueStart + '    onChange: learner => {'.length, html.indexOf('\n    },\n  });', queueStart));

function fixture({ selfDirected = false, queue = [], targetsView = false, nodes = [] } = {}) {
  const f = { calls: [], storage: new Map(), events: [], dev: false, fail: false, learner: { id: 'test', selfDirected, queue, targets: [30] } };
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.children = []; this.attrs = {}; this.dataset = {}; this.offsetWidth = 224; this.offsetHeight = 180; this.style = {}; }
    append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
    appendChild(node) { this.append(node); }
    replaceChildren(...nodes) { for (const node of this.children) node.parent = null; this.children = []; this.append(...nodes); }
    setAttribute(key, value) { this.attrs[key] = String(value); }
    getAttribute(key) { return this.attrs[key] ?? null; }
    removeAttribute(key) { delete this.attrs[key]; if (key === 'href') delete this.href; }
    get isConnected() { return document.body.contains(this); }
    contains(node) { for (; node; node = node.parent) if (node === this) return true; return false; }
    matches(selector) { return (selector === '.node-hit' || selector === '.menu-new-tab-indicator') ? this.className === selector.slice(1) : selector === '[role="menuitem"]' && this.attrs.role === 'menuitem'; }
    querySelectorAll(selector) { return this.children.flatMap(node => [...(node.matches(selector) ? [node] : []), ...node.querySelectorAll(selector)]); }
    querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
    closest(selector) { for (let node = this; node; node = node.parent) if (selector === '[hidden]' && node.hidden || selector === '.node, .edge-stub' && /\b(node|edge-stub)\b/.test(node.className || '')) return node; return null; }
    focus() { document.activeElement = this; }
    select() { this.selected = true; }
    setSelectionRange(start, end) { this.selection = [start, end]; }
    getBoundingClientRect() { return { left: 20, bottom: 100, width: 240 }; }
    remove() { if(this.parent) this.parent.children=this.parent.children.filter(child=>child!==this); this.parent=null; }
    click() { if(this.tagName==='a' && this.target==='_blank') f.opened.push([this.href,this.target,this.rel]); if (!this.disabled && !this.closest('[hidden]')) { const event = new Event('click', { cancelable: true }); Object.defineProperty(event, 'detail', { value: 0 }); this.dispatchEvent(event); } }
  }
  const document = new EventTarget(); document.body = new Element('body'); document.hidden = false;
  document.createElement = tag => new Element(tag);
  document.getElementById = id => { const walk = node => node.id === id ? node : node.children.map(walk).find(Boolean); return walk(document.body); };
  const menu = new Element('div'); menu.id = 'nodeContextMenu'; menu.hidden = true;
  for (const id of ['nodeQueueAction', 'nodeTargetAction', 'studyTopicLink', 'reviewTopicLink', 'goToTopicLink', 'copyNodeButton', 'copyNodeDbId', 'copyNodeMaId', 'copyCanvasDbIds']) {
    const node = new Element(id.endsWith('Link') ? 'a' : 'div'); node.id = id;
    if (id.endsWith('Link') || id.startsWith('copy')) node.setAttribute('role', 'menuitem');
    if (id === 'copyCanvasDbIds') node.hidden = true;
    if (id.endsWith('Link')) {
      const arrow = new Element('span'); arrow.className = 'menu-new-tab-indicator'; arrow.hidden = true; node.append(arrow);
    }
    menu.append(node);
  }
  document.body.append(menu);
  for (const id of ['copyNodeNotice', 'manualNodeCopy', 'manualNodeTitle', 'manualNodeText', 'manualNodeDone']) { const node = new Element('div'); node.id = id; document.body.append(node); }
  const svg = new Element('svg'); svg.id = 'svg'; document.body.append(svg);
  const opener = new Element('g'), hit = new Element('rect'); opener.className = 'node'; hit.className = 'node-hit'; opener.append(hit); svg.append(opener);
  f.opened = []; f.copied = []; f.clipboard = [];
  f.availabilityReads = []; f.availability = new Map();
  f.state = { layout: { activeNodes: nodes }, activeIds: new Set([20]), view: { x: 0, y: 0, k: 1 } };
  const window = new EventTarget(); window.open = () => { throw new Error('Navigation must use a normal link, not a new-window request'); }; window.innerWidth = 1000; window.innerHeight = 900;
  for (const name of ['queue', 'targets']) window.addEventListener(`course-academy:${name}-changed`, () => f.events.push(name));
  const context = vm.createContext({ document, window, Event, CustomEvent, crypto, setTimeout, clearTimeout,
    navigator: { clipboard: { async writeText(value) { if (f.clipboardBlocked) throw new Error('Clipboard blocked'); f.clipboard.push(value); } } },
    state: f.state,
    copyEntityId: (id, label) => f.copied.push([id, label]),
    academyEntityId: value => value == null ? null : String(value),
    snapshot: { learner: structuredClone(f.learner) }, courseId: 'course',
    targetsView, colorCodeEnabled: true, repetitions: { 20: 5 }, isLightTheme: () => false, themeColor: color => color,
    loading: false, refreshTargetColors() {},
    PALETTE: ['#000000', '#303030', '#5A5A5A', '#858585', '#AEAEAE', '#D6D6D6', '#FFFFFF'],
    topicReferenceURL: (_snapshot, node) => '/topic?topic=' + node.uuid,
    $: document.getElementById, isDeveloperMode: () => f.dev, developerModeReady: Promise.resolve(),
    localStorage: { setItem: (key, value) => f.storage.set(key, value) },
    readLearner: async () => structuredClone(f.learner),
    readTopicStudyAvailability: async id => {
      f.availabilityReads.push(id);
      if (f.availabilityHold) return f.availabilityHold(id);
      return f.availability.get(id) || { topicId: id, available: true };
    },
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
    const queueControls = createQueueControls({ readLearner, onChange: learner => {
      ${queueChanged}
    } });
    const targetControls = createTargetControls({ readLearner, onChange: learner => {
      snapshot.learner = { ...snapshot.learner, ...learner, queue:snapshot.learner.queue };
    } });
    queueControls.setLearner(snapshot.learner); targetControls.setLearner(snapshot.learner);
    ${statusPaletteSource}
    ${appearanceSource}
    // Mount the production selection controls without the retired graph menu.
    const nodeContextMenu = { open(node) {
      document.getElementById('nodeContextMenu').hidden = false;
      document.getElementById('nodeQueueAction').replaceChildren(queueControls.createToggle(node,{menuItem:true}));
      document.getElementById('nodeTargetAction').replaceChildren(targetControls.createToggle(node,{menuItem:true}));
    }};
    return { queueControls, targetControls, menu: nodeContextMenu, nodeAppearance };
  })()`, context);
  f.document = document; f.window = window; f.opener = opener; f.svg = svg;
  f.open = (shiftKey = false) => f.h.menu.open({ id: 20, uuid: 'topic-uuid', name: 'Topic twenty' }, { type: 'contextmenu', shiftKey, clientX: 50, clientY: 70, preventDefault() {}, stopPropagation() {} }, opener);
  f.queueButton = () => document.getElementById('nodeQueueAction').querySelector('[role="menuitem"]');
  return f;
}
const settle = async () => { await new Promise(resolve => setImmediate(resolve)); };

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
  assert.equal(f.h.nodeAppearance(20).fill, '#3464df');
  assert.equal(f.calls.length, 0);
});

test('target previews retain blue after queue membership was saved through the other controller', async () => {
  const f = fixture({ selfDirected: true }); f.open();
  f.queueButton().click(); await settle();
  let release;
  f.hold = new Promise(resolve => { release = resolve; });
  f.open();
  f.document.getElementById('nodeTargetAction').querySelector('[role="menuitem"]').click();
  assert.equal(f.h.nodeAppearance(20).fill, '#3464df');
  release(); await settle();
  assert.equal(f.h.nodeAppearance(20).fill, '#3464df');
});

test('queue changes paint immediately while saving and roll back failed requests with an exact retry', async () => {
  const f = fixture(); let release;
  f.hold = new Promise(resolve => { release = resolve; }); f.fail = true; f.open();
  f.queueButton().click();
  assert.equal(f.h.nodeAppearance(20).fill, '#3464df');
  assert.deepEqual(f.learner.queue, []);
  release(); await settle();
  assert.equal(f.h.nodeAppearance(20).fill, '#D6D6D6');
  assert.equal(f.queueButton().textContent, 'Retry');
  f.queueButton().click(); await settle();
  assert.equal(f.h.nodeAppearance(20).fill, '#3464df');
  assert.deepEqual(f.calls[0].body, f.calls[1].body);
  f.open(); f.hold = new Promise(resolve => { release = resolve; });
  f.queueButton().click();
  assert.equal(f.h.nodeAppearance(20).fill, '#D6D6D6');
  assert.deepEqual(f.learner.queue, [20]);
  release(); await settle(); assert.deepEqual(f.learner.queue, []);
});

test('a target response preserves a queue preview still waiting for its save response', async () => {
  const f = fixture({ selfDirected: true }); let release;
  f.hold = new Promise(resolve => { release = resolve; }); f.open(); f.queueButton().click();
  f.h.targetControls.setLearner({ ...f.learner, targets: [20, 30], queue: [] });
  assert.equal(f.h.nodeAppearance(20).fill, '#3464df');
  release(); await settle(); assert.equal(f.h.nodeAppearance(20).fill, '#3464df');
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
  assert.equal(f.h.nodeAppearance(20).fill, '#2a8851');
  assert.deepEqual(f.learner.targets, [30]);
  release(); await settle();
  assert.deepEqual(f.learner.targets, [30, 20]);
  assert.equal(f.h.nodeAppearance(20).fill, '#2a8851');
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
  assert.equal(f.h.nodeAppearance(20).fill, '#2a8851');
  assert.deepEqual(f.learner.targets, [30]); // The server has not saved yet.
  assert.equal(button.disabled, true);
  assert.equal(otherButton.getAttribute('aria-checked'), 'true');
  assert.equal(otherButton.dataset.animate, undefined);
  release(); await settle(); f.hold = null;
  assert.equal(button.disabled, false);
  assert.deepEqual(f.learner.targets, [30, 20]);
  assert.equal(f.h.nodeAppearance(20).fill, '#2a8851');
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
  assert.equal(f.h.nodeAppearance(20).fill, '#2a8851');
  assert.equal(host.children[1].textContent, '');
  assert.deepEqual(f.learner.targets, [30, 20]);
});


function dispatch(target, type, values) {
  const event = new Event(type, { cancelable: true });
  for (const [key, value] of Object.entries(values)) Object.defineProperty(event, key, { value });
  target.dispatchEvent(event);
  return event;
}

