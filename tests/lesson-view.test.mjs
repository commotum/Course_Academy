import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

// Run the actual lesson renderer and visibility logic with a DOM and API stand-in.
// No live learner, attempts, or database are used.
const source = await readFile(new URL('../ui/learning.js', import.meta.url), 'utf8');
const controllers = source.slice(source.indexOf('const $'), source.indexOf("$('retryButton').addEventListener"));
const visibility = source.slice(source.indexOf('async function syncAfterVisibility()'), source.indexOf("document.addEventListener('visibilitychange'"));

function fixture(storage = new Map()) {
  const f = { storage, calls: [], scrolls: [], focused: [], cleared: [], dev: false, now: 10000 };
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.childNodes = []; this.dataset = {}; this.style = {}; this.attrs = {}; this.className = ''; }
    get children() { return this.childNodes.filter(node => node.tagName !== '#text'); }
    get childElementCount() { return this.children.length; }
    get firstChild() { return this.childNodes[0] || null; }
    get textContent() { return (this.text || '') + this.childNodes.map(node => node.textContent).join(''); }
    set textContent(value) { this.replaceChildren(); this.text = String(value); }
    get isConnected() { return document.body.contains(this); }
    append(...nodes) {
      for (let node of nodes) {
        if (typeof node === 'string') { const text = new Element('#text'); text.textContent = node; node = text; }
        node.remove(); node.parent = this; this.childNodes.push(node);
      }
    }
    insertBefore(node, before) { node.remove(); node.parent = this; const i = this.childNodes.indexOf(before); this.childNodes.splice(i < 0 ? this.childNodes.length : i, 0, node); }
    remove() { if (this.parent) this.parent.childNodes = this.parent.childNodes.filter(node => node !== this); this.parent = null; }
    replaceChildren(...nodes) { for (const child of this.childNodes) child.parent = null; this.childNodes = []; this.text = ''; this.append(...nodes); }
    contains(node) { for (; node; node = node.parent) if (node === this) return true; return false; }
    setAttribute(key, value) { this.attrs[key] = String(value); }
    getAttribute(key) { return this.attrs[key] ?? null; }
    matches(selector) {
      if (selector.startsWith('.')) return this.className.split(' ').includes(selector.slice(1));
      if (selector.startsWith('[data-')) return selector.slice(6, -1).replace(/-([a-z])/g, (_m, c) => c.toUpperCase()) in this.dataset;
      if (selector === 'input:checked') return this.tagName === 'input' && this.checked;
      return this.tagName === selector;
    }
    querySelectorAll(selector) { return this.children.flatMap(child => [...(selector.split(',').some(s => child.matches(s.trim())) ? [child] : []), ...child.querySelectorAll(selector)]); }
    querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
    focus() { document.activeElement = this; f.focused.push(this); }
    scrollIntoView(options) { f.scrolls.push({ node: this, options }); }
    click() { if (!this.disabled) this.dispatchEvent(new Event('click')); }
  }
  const document = { body: new Element('body'), hidden: false, createElement: tag => new Element(tag) };
  document.querySelectorAll = selector => document.body.querySelectorAll(selector);
  document.getElementById = id => [document.body, ...document.body.querySelectorAll('main,button,a,span,div')].find(node => node.id === id) || null;
  for (const id of ['main', 'learnerName', 'courseLink', 'errorText', 'errorBanner', 'retryButton', 'announcement']) {
    const node = new Element(id === 'main' ? 'main' : 'div'); node.id = id; document.body.append(node);
  }
  document.getElementById('errorBanner').hidden = true;
  f.document = document;
  const window = { MathJax: { typesetClear(nodes) { f.cleared.push(...nodes); } } };
  const context = vm.createContext({ document, window, MathJax: window.MathJax, crypto, URLSearchParams, AbortController, Event,
    Date: class extends Date { static now() { return f.now; } },
    isDeveloperMode: () => f.dev,
    attachStepMenu(node, id) { node.dataset.stepDbId = id; },
    sessionStorage: { getItem: key => storage.get(key) ?? null, setItem(key, value) { storage.set(key, value); } },
    history: { replaceState() {} }, location: { replace() {}, assign() {} },
    fetch: async (path, options) => {
      const body = options.body ? JSON.parse(options.body) : null;
      f.calls.push({ path, body, keepalive: options.keepalive });
      if (path === '/api/pause') { f.server.status = 'paused'; f.server.step.status = 'paused'; f.server.elapsedSeconds = f.h.clock.elapsed; }
      if (path === '/api/resume') { f.server.status = 'started'; f.server.step.status = 'started'; }
      return { ok: true, json: async () => structuredClone(f.server) };
    },
  });
  f.h = vm.runInContext(`(() => {
    ${controllers}
    ${visibility}
    markdown = (value, className = 'prose') => el('div', className, value || '');
    typeset = async () => {};
    loadMath = async () => {};
    return {
      get view() { return lessonView; }, get clock() { return clock; }, get pending() { return pendingPause; },
      setBusy, pauseWhenHidden, syncAfterVisibility, openTask, home,
      render: async data => { task = data; await renderTask(data); },
      preview: async (data, index) => { task = data; previewStepIndex = index; await renderPreview(); },
    };
  })()`, context);
  return f;
}

const activity = (itemId, number = 1, overrides = {}) => ({
  taskId: 123, activityId: 456, learner: { id: 'test', name: 'Learner' }, course: { id: 'course' },
  title: 'The lesson title', status: 'started', elapsedSeconds: 10,
  progress: { stepNumber: number, totalSteps: 3, presented: number },
  step: { itemId, stepId: 'step-' + itemId, kind: 'tutorial', title: 'Introduction', markdown: 'Read this.', status: 'started', canContinue: true, fields: [] },
  ...overrides,
});
const question = (itemId, status = 'started') => ({
  itemId, stepId: 'step-' + itemId, kind: 'question', title: 'Power rule', markdown: 'Find the derivative.', status,
  canContinue: status === 'correct', solution: status === 'correct' ? 'Apply the power rule.' : undefined,
  fields: [{ id: 30, key: 'selection', type: 'radio', response: status === 'correct' ? { choiceId: 41 } : null,
    choices: [{ id: 41, type: 'text', value: 'Correct option' }, { id: 42, type: 'text', value: 'Other option' }] }],
});

test('lesson frame has a compact progress bar and timer, and hides the topic heading', async () => {
  const f = fixture();
  await f.h.render(activity(1));
  const main = f.document.getElementById('main');
  assert.equal(main.querySelector('h1').className, 'sr-only');
  assert.equal(main.querySelector('.lesson-heading'), null);
  assert.equal(main.querySelector('.pause-panel'), null);
  assert.equal(main.querySelectorAll('button').some(node => node.textContent === 'Pause'), false);
  assert.equal(f.h.view.track.getAttribute('aria-valuenow'), '0');
  assert.equal(f.h.view.timer.textContent, '0:10');
  assert.equal(f.h.view.feed.children.length, 1);
  assert.equal(f.scrolls.length, 1);
});

test('advancing retains the earlier DOM, disables its answers, and focuses only the new step', async () => {
  const f = fixture();
  await f.h.render(activity(1, 1, { step: question(1, 'correct') }));
  const previous = f.h.view.current;
  await f.h.render(activity(2, 2));
  assert.equal(f.h.view.feed.children[0], previous);
  assert.equal(previous.dataset.history, 'true');
  assert.equal(previous.querySelector('.lesson-controls'), null);
  assert.equal(previous.querySelector('.answer-actions'), null);
  assert.equal(previous.querySelectorAll('input').every(node => node.disabled && node.dataset.readOnly === 'true'), true);
  assert.match(previous.textContent, /Apply the power rule/);
  assert.match(previous.textContent, /Step 1 \/ 3/);
  assert.equal(f.h.view.history.size, 1);
  assert.equal(f.h.view.current.dataset.stepDbId, 'step-2');
  assert.equal(f.scrolls.at(-1).node, f.h.view.current);
  assert.equal(f.h.view.track.getAttribute('aria-valuenow'), '1');
  assert.equal(f.h.view.feed.children.filter(node => node.querySelector('.lesson-controls')).length, 1);
});

test('answer feedback updates the same presentation without duplicating history or scrolling', async () => {
  const f = fixture();
  await f.h.render(activity(1, 1, { step: question(1) }));
  assert.ok(f.h.view.current.querySelector('.answer-actions'));
  assert.equal(f.h.view.current.querySelector('.lesson-controls'), null);
  await f.h.render(activity(1, 1, { step: question(1, 'correct') }));
  assert.equal(f.h.view.feed.children.length, 1);
  assert.equal(f.h.view.history.size, 0);
  assert.equal(f.scrolls.length, 1);
  assert.match(f.h.view.current.textContent, /Correct/);
  assert.ok(f.h.view.current.querySelector('.lesson-controls'));
});

test('reload restores previously revealed steps as read-only and separates task histories', async () => {
  const storage = new Map(), f = fixture(storage);
  await f.h.render(activity(1, 1, { step: question(1, 'correct') }));
  await f.h.render(activity(2, 2));
  const restored = fixture(storage);
  await restored.h.render(activity(2, 2));
  assert.equal(restored.h.view.feed.children.length, 2);
  assert.equal(restored.h.view.feed.children[0].querySelectorAll('input').every(node => node.disabled), true);
  assert.match(restored.h.view.feed.children[0].textContent, /Apply the power rule/);
  await restored.h.render(activity(9, 1, { taskId: 999 }));
  assert.equal(restored.h.view.feed.children.length, 1);
});

test('developer preview reveals only visited steps and keeps them available for review', async () => {
  const f = fixture(); f.dev = true;
  const data = { ...activity(1), steps: [activity(1).step, activity(2).step, activity(3).step] };
  await f.h.preview(data, 0);
  assert.equal(f.h.view.feed.children.length, 1);
  await f.h.preview(data, 1);
  assert.equal(f.h.view.feed.children.length, 2);
  assert.equal(f.h.view.history.size, 1);
  assert.equal(f.h.view.feed.children[0].querySelector('.lesson-controls'), null);
  assert.equal(f.h.view.timer.textContent, 'Preview');
  assert.equal(f.calls.length, 0);
});

test('a step revealed while hidden moves into focus when returning, with history kept in memory if storage fails', async () => {
  const f = fixture({ get() { throw new Error('Storage unavailable'); }, set() { throw new Error('Storage unavailable'); } });
  await f.h.render(activity(1));
  f.document.hidden = true;
  await f.h.render(activity(2, 2));
  assert.equal(f.scrolls.length, 1);
  assert.equal(f.h.view.history.size, 1);
  f.document.hidden = false;
  await f.h.render(activity(2, 2));
  assert.equal(f.scrolls.length, 2);
  assert.equal(f.scrolls.at(-1).node, f.h.view.current);
});

test('hidden lessons pause after an in-flight save and automatically resume when reopened', async () => {
  const f = fixture(); f.server = activity(1);
  await f.h.render(structuredClone(f.server));
  f.now += 3000; f.document.hidden = true; f.h.setBusy(true);
  f.h.pauseWhenHidden();
  assert.equal(f.h.clock.running, false);
  assert.equal(f.h.clock.elapsed, 13);
  assert.equal(f.calls.length, 0);
  f.h.setBusy(false); await f.h.syncAfterVisibility(); await f.h.pending;
  assert.equal(f.calls[0].path, '/api/pause');
  assert.equal(f.calls[0].keepalive, true);
  f.now += 50000;
  assert.equal(f.h.clock.elapsed, 13);
  f.document.hidden = false;
  await f.h.openTask('123');
  const resume = f.calls.find(call => call.path === '/api/resume');
  assert.equal(resume.body.taskId, 123);
  assert.equal(f.h.clock.running, true);
  assert.equal(f.h.view.timer.textContent, '0:13');
});

test('Study shows saved lesson progress with the same fraction as the player', async () => {
  const f = fixture();
  const saved = activity(7, 4, { status: 'paused', progress: { stepNumber: 4, totalSteps: 6, presented: 12 } });
  f.server = { activities: [saved] };
  await f.h.home();
  const row = f.document.getElementById('main').querySelector('.queue-card');
  const bar = row.querySelector('.queue-progress-track');
  assert.equal(row.querySelector('.queue-progress-value').textContent, '50%');
  assert.equal(bar.getAttribute('aria-valuemax'), '6');
  assert.equal(bar.getAttribute('aria-valuenow'), '3');
  assert.equal(bar.getAttribute('aria-valuetext'), '50% complete');
  assert.equal(row.querySelector('.queue-progress-fill').style.width, '50%');
  assert.match(row.textContent, /Resume →/);
  await f.h.render(saved);
  assert.equal(f.h.view.fill.style.width, '50%');
  assert.equal(f.calls.length, 1);
  assert.equal(f.calls[0].path, '/api/queue');
});

test('Study progress is only shown for real started or paused lessons with valid saved positions', async () => {
  const f = fixture();
  f.server = { activities: [
    activity(1, 1),
    activity(2, 2, { status: 'unlocked' }),
    activity(3, 2, { status: 'paused', progress: null }),
    activity(4, 2, { status: 'paused', progress: { stepNumber: 2, totalSteps: 0 } }),
    activity(5, 2, { status: 'paused', taskId: null }),
  ] };
  await f.h.home();
  const bars = f.document.getElementById('main').querySelectorAll('.queue-progress-track');
  assert.equal(bars.length, 1);
  assert.equal(bars[0].getAttribute('aria-valuenow'), '0');
  assert.equal(f.document.getElementById('main').querySelector('.queue-progress-value').textContent, '0%');
  f.dev = true;
  await f.h.home();
  assert.equal(f.document.getElementById('main').querySelectorAll('.queue-progress-track').length, 0);
  assert.equal(f.calls.at(-1).path, '/api/preview-home');
});

test('leaving the document sends a keepalive pause even when a save is busy', async () => {
  const f = fixture(); f.server = activity(1);
  await f.h.render(structuredClone(f.server));
  f.document.hidden = true; f.h.setBusy(true);
  await f.h.pauseWhenHidden({ unloading: true });
  assert.equal(f.calls.length, 1);
  assert.equal(f.calls[0].path, '/api/pause');
  assert.equal(f.calls[0].keepalive, true);
  assert.equal(f.h.clock.running, false);
});
