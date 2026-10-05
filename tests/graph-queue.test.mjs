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

function fixture({ selfDirected = false, queue = [] } = {}) {
  const f = { calls: [], storage: new Map(), events: [], dev: false, fail: false, learner: { id: 'test', selfDirected, queue, targets: [30] } };
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.children = []; this.attrs = {}; this.offsetWidth = 224; this.offsetHeight = 180; this.style = {}; }
    append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
    replaceChildren(...nodes) { for (const node of this.children) node.parent = null; this.children = []; this.append(...nodes); }
    setAttribute(key, value) { this.attrs[key] = String(value); }
    getAttribute(key) { return this.attrs[key] ?? null; }
    removeAttribute(key) { delete this.attrs[key]; }
    get isConnected() { return document.body.contains(this); }
    contains(node) { for (; node; node = node.parent) if (node === this) return true; return false; }
    matches(selector) { return selector === '.node-hit' ? this.className === 'node-hit' : selector === '[role="menuitem"]' && this.attrs.role === 'menuitem'; }
    querySelectorAll(selector) { return this.children.flatMap(node => [...(node.matches(selector) ? [node] : []), ...node.querySelectorAll(selector)]); }
    querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
    closest(selector) { for (let node = this; node; node = node.parent) if (selector === '[hidden]' && node.hidden) return node; return null; }
    focus() { document.activeElement = this; }
    getBoundingClientRect() { return { left: 20, bottom: 100, width: 240 }; }
    click() { if (!this.disabled && !this.closest('[hidden]')) this.dispatchEvent(new Event('click')); }
  }
  const document = new EventTarget(); document.body = new Element('body'); document.hidden = false;
  document.createElement = tag => new Element(tag);
  document.getElementById = id => { const walk = node => node.id === id ? node : node.children.map(walk).find(Boolean); return walk(document.body); };
  const menu = new Element('div'); menu.id = 'nodeContextMenu'; menu.hidden = true;
  for (const id of ['nodeQueueAction', 'nodeTargetAction', 'goToTopicLink', 'copyNodeButton']) {
    const node = new Element(id === 'goToTopicLink' ? 'a' : 'div'); node.id = id;
    if (id === 'goToTopicLink' || id === 'copyNodeButton') node.setAttribute('role', 'menuitem');
    menu.append(node);
  }
  document.body.append(menu);
  for (const id of ['copyNodeNotice', 'manualNodeCopy', 'manualNodeText', 'manualNodeDone']) { const node = new Element('div'); node.id = id; document.body.append(node); }
  const opener = new Element('g'), hit = new Element('rect'); hit.className = 'node-hit'; opener.append(hit); document.body.append(opener);
  const window = new EventTarget(); window.innerWidth = 1000; window.innerHeight = 900;
  for (const name of ['queue', 'targets']) window.addEventListener(`course-academy:${name}-changed`, () => f.events.push(name));
  const context = vm.createContext({ document, window, Event, CustomEvent, crypto, setTimeout, clearTimeout, navigator: {},
    snapshot: { learner: f.learner }, courseId: 'course',
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
    const targetControls = createTargetControls({ readLearner });
    queueControls.setLearner(snapshot.learner); targetControls.setLearner(snapshot.learner);
    ${menuSource}
    return { queueControls, targetControls, menu: nodeContextMenu };
  })()`, context);
  f.document = document; f.window = window; f.opener = opener;
  f.open = () => f.h.menu.open({ id: 20, uuid: 'topic-uuid', name: 'Topic twenty' }, { type: 'contextmenu', clientX: 50, clientY: 70, preventDefault() {}, stopPropagation() {} }, opener);
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
