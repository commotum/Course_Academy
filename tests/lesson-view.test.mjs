import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

// Run the actual lesson renderer and visibility logic with a DOM and API stand-in.
// No live learner, attempts, or database are used.
const source = await readFile(new URL('../ui/learning.js', import.meta.url), 'utf8');
const controllers = source.slice(source.indexOf('const $'), source.indexOf("$('retryButton').addEventListener"));
const visibility = source.slice(source.indexOf('async function syncAfterVisibility()'), source.indexOf("document.addEventListener('visibilitychange'"));
const fieldUI = (await readFile(new URL('../ui/question-fields.js', import.meta.url), 'utf8')).replace(/^[\s\S]*?(?=\/\/ Shared presentation)/, '').replaceAll('export ', '');

function fixture(storage = new Map()) {
  const f = { storage, calls: [], scrolls: [], focused: [], cleared: [], notifications: [], dev: false, now: 10000 };
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.childNodes = []; this.dataset = {}; this.style = {}; this.attrs = {}; this.className = ''; }
    get children() { return this.childNodes.filter(node => node.tagName !== '#text'); }
    get childElementCount() { return this.children.length; }
    get firstChild() { return this.childNodes[0] || null; }
    get classList() { return { contains: name => this.className.split(' ').includes(name) }; }
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
  const document = { body: new Element('body'), hidden: false, createElement: tag => new Element(tag),
    createTextNode: text => { const node = new Element('#text'); node.textContent = text; return node; },
    addEventListener() {}, removeEventListener() {},
  };
  document.querySelectorAll = selector => document.body.querySelectorAll(selector);
  document.getElementById = id => [document.body, ...document.body.querySelectorAll('main,button,a,span,div')].find(node => node.id === id) || null;
  for (const id of ['main', 'learnerName', 'courseLink', 'errorText', 'errorBanner', 'retryButton', 'announcement']) {
    const node = new Element(id === 'main' ? 'main' : 'div'); node.id = id; document.body.append(node);
  }
  document.getElementById('errorBanner').hidden = true;
  f.document = document;
  const window = { MathJax: { typesetClear(nodes) { f.cleared.push(...nodes); } } };
  const context = vm.createContext({ document, window, MathJax: window.MathJax, crypto, URLSearchParams, AbortController, Event,
    setTimeout, clearTimeout,
    Date: class extends Date { static now() { return f.now; } },
    isDeveloperMode: () => f.dev,
    attachStepMenu(node, id, mathAcademyId, options = {}) { node.dataset.stepDbId = id; node.dataset.mathAcademyId = mathAcademyId; node.dataset.contentKind = options.kind; },
    sessionStorage: { getItem: key => storage.get(key) ?? null, setItem(key, value) { storage.set(key, value); }, removeItem(key) { storage.delete(key); } },
    localStorage: { setItem: (key, value) => f.notifications.push({ key, value }) },
    history: { replaceState() {} }, location: { replace() {}, assign() {} },
    createStudySidebar: () => new Element('aside'),
    loadMathInputs: async () => {},
    fetch: async (path, options) => {
      const body = options.body ? JSON.parse(options.body) : null;
      f.calls.push({ path, body, keepalive: options.keepalive });
      const response = await f.respond?.(path, body);
      if (response) return response;
      if (path === '/api/pause') { f.server.status = 'paused'; f.server.step.status = 'paused'; f.server.elapsedSeconds = f.h.clock.elapsed; }
      if (path === '/api/resume') { f.server.status = 'started'; f.server.step.status = 'started'; }
      if (f.delay) await f.delay;
      return { ok: true, json: async () => structuredClone(f.server) };
    },
  });
  f.h = vm.runInContext(`(() => {
    ${fieldUI}
    ${controllers}
    ${visibility}
    markdown = (value, className = 'prose', fields = []) => {
      const node = el('div', className, value || '');
      for (const match of inlinePrompt(value, fields).matchAll(/data-field-key="([^"]+)"/g)) {
        const slot = el('span', 'field-location'); slot.dataset.fieldKey = match[1]; node.append(slot);
      }
      return node;
    };
    typeset = async () => {};
    loadMath = async () => {};
    return {
      get view() { return lessonView; }, get clock() { return clock; }, get pending() { return pendingPause; },
      updateTaskTimer, mutation, setBusy, pauseWhenHidden, syncAfterVisibility, refreshPageOnReturn, openTask, studyTopic, home, toggleLessonPause, retry: () => retryOperation?.(),
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
  step: { itemId, stepId: 'step-' + itemId, contentId: 9000 + itemId, mathAcademyId: '100' + itemId, kind: 'tutorial', title: 'Introduction', markdown: 'Read this.', status: 'started', canContinue: true, fields: [] },
  ...overrides,
});
const question = (itemId, status = 'started') => ({
  itemId, stepId: 'step-' + itemId, contentId: 9000 + itemId, mathAcademyId: '200' + itemId, kind: 'question', title: 'Power rule', markdown: 'Find the derivative.', status,
  canContinue: status === 'correct', solution: status === 'correct' ? 'Apply the power rule.' : undefined,
  fields: [{ id: 30, key: 'selection', type: 'radio', response: status === 'correct' ? { choiceId: 41 } : null,
    choices: [{ id: 41, type: 'text', value: 'Correct option' }, { id: 42, type: 'text', value: 'Other option' }] }],
});

test('generic answer keys do not become visible labels above radio choices', async () => {
  for (const key of ['answer', 'selection', undefined]) {
    const f = fixture(), step = question(1);
    step.fields[0].key = key;
    await f.h.render(activity(1, 1, { step }));
    const legend = f.h.view.current.querySelector('legend');
    assert.equal(legend.className, 'sr-only');
    assert.equal(legend.textContent, 'Choose an answer');
    assert.doesNotMatch(f.h.view.current.textContent, /Answer: answer/);
    assert.equal(f.h.view.current.querySelector('.choices').querySelectorAll('input').length, 2);
  }
});

test('generic blank labels stay accessible and numbered fields retain their labels', async () => {
  for (const [key, label] of [['answer', 'Answer'], ['field-2', 'Answer 2']]) {
    const f = fixture(), step = question(1);
    step.fields = [{ id: 30, key, type: 'blank', answerType: 'text' }];
    await f.h.render(activity(1, 1, { step }));
    assert.equal(f.h.view.current.querySelector('legend').textContent, label);
    assert.equal(f.h.view.current.querySelector('.answer-input').getAttribute('aria-label'), label);
  }
});

test('preview solutions do not expose the generic answer key', async () => {
  const f = fixture(), step = question(1, 'correct');
  f.dev = true;
  step.fields[0].key = 'answer';
  step.fields[0].correctAnswer = step.fields[0].choices[0];
  await f.h.preview({ activityId: 456, steps: [step] }, 0);
  assert.equal(f.h.view.current.querySelector('.response-summary').textContent, 'Answer · correct value:');
  assert.doesNotMatch(f.h.view.current.textContent, /Answer: answer/);
});

test('lesson frame has a compact progress bar and timer, and hides the topic heading', async () => {
  const f = fixture();
  await f.h.render(activity(1));
  const main = f.document.getElementById('main');
  assert.equal(main.querySelector('h1').className, 'sr-only');
  assert.equal(main.querySelector('.lesson-heading'), null);
  assert.equal(main.querySelector('.pause-panel'), null);
  assert.equal(f.h.view.pause.textContent, 'Pause');
  assert.equal(f.h.view.pause.hidden, false);
  assert.equal(f.h.view.track.getAttribute('aria-valuenow'), '0');
  assert.equal(f.h.view.timer.textContent, '0:10');
  assert.equal(f.h.view.feed.children.length, 1);
  assert.equal(f.scrolls.length, 1);
});

test('reviews link to the topic reference outside the question card without starting an activity', async () => {
  const f = fixture();
  const data = activity(1, 1, { type: 'review', step: question(1), reviewTopic: { uuid: 'topic-uuid', title: 'Power rule' } });
  await f.h.render(data);
  const view = f.h.view;
  assert.equal(view.reference.hidden, false);
  assert.equal(view.reviewLink.textContent, 'Open topic lesson');
  assert.equal(view.reviewLink.href, '/topic?topic=topic-uuid&course=course');
  assert.equal(view.reviewLink.target, '_blank');
  assert.equal(view.reviewLink.rel, 'noopener');
  assert.equal(view.current.contains(view.reference), false);
  assert.equal(f.document.getElementById('main').querySelector('.lesson-toolbar').contains(view.reference), true);
  assert.equal(f.document.getElementById('main').contains(view.reference), true);
  assert.equal(f.calls.length, 0);
  await f.h.render({ ...data, status: 'completed' });
  assert.equal(view.reference.hidden, true);
  await f.h.render({ ...data, type: 'lesson' });
  assert.equal(view.reference.hidden, true);
  await f.h.render({ ...data, reviewTopic: null });
  assert.equal(view.reference.hidden, true);
});

test('pause controls are hidden for previews, completed lessons, and fixed-deadline assessments', async () => {
  const f = fixture();
  await f.h.render(activity(1, 1, { status: 'completed' }));
  assert.equal(f.h.view.pause.hidden, true);
  await f.h.render(activity(2, 1, { type: 'assessment', remainingSeconds: 900 }));
  assert.equal(f.h.view.pause.hidden, true);
  await f.h.toggleLessonPause();
  assert.equal(f.calls.length, 0);
  f.dev = true;
  await f.h.preview({ activityId: 500, type: 'lesson', learner: { id: 'test' }, steps: [{ ...question(1), fields: [] }] }, 0);
  assert.equal(f.h.view.pause.hidden, true);
  assert.match(f.h.view.timer.title, /Nothing recorded/);
});

test('successful lessons and reviews invalidate queue state in other tabs', async () => {
  for (const type of ['lesson', 'review', 'assessment']) for (const status of ['started', 'paused', 'failed', 'completed']) {
    const f = fixture();
    await f.h.render(activity(1, 1, { type }));
    f.server = activity(1, 1, { type, status });
    await f.h.mutation('/api/continue', { taskId: 123, itemId: 1 });
    const changed = type !== 'assessment' && status === 'completed';
    assert.equal(f.notifications.length, changed ? 1 : 0);
    if (changed) {
      assert.equal(f.notifications[0].key, 'course-academy-queue-changed');
      await f.h.mutation('/api/continue', { taskId: 123, itemId: 1 });
      assert.equal(f.notifications.length, 1, 'replaying a completion does not notify twice');
    }
  }
});

test('a zero-progress lesson returned to unstarted keeps a stopped timer and can begin again', async () => {
  const f = fixture();
  f.server = activity(1, 1, { type: 'lesson' });
  f.respond = async path => {
    if (path !== '/api/pause') return null;
    f.server.status = 'locked';
    f.server.step.status = 'paused';
    return { ok: true, json: async () => structuredClone(f.server) };
  };
  await f.h.render(structuredClone(f.server));
  await f.h.toggleLessonPause();
  assert.equal(f.h.clock.running, false);
  assert.equal(f.h.view.pause.textContent, 'Resume');
  assert.equal(f.h.view.current.querySelector('.lesson-controls').textContent, 'Resume →');
  await f.h.toggleLessonPause();
  assert.equal(f.calls.at(-1).path, '/api/resume');
  assert.equal(f.h.clock.running, true);
  assert.equal(f.h.view.timer.textContent, '0:10');
});

test('Study now starts the selected graph topic directly in the progressive lesson view', async () => {
  const f = fixture(); f.server = activity(1);
  await f.h.studyTopic('17592186050674');
  assert.equal(f.calls.length, 1);
  assert.equal(f.calls[0].path, '/api/study-topic');
  assert.equal(f.calls[0].body.topicId, 17592186050674);
  assert.ok(f.calls[0].body.requestId);
  assert.equal(f.h.view.feed.children.length, 1);
  assert.match(f.h.view.current.textContent, /Read this/);
  await f.h.studyTopic('bad-topic');
  assert.equal(f.calls.length, 1);
});

test('Study now in developer mode opens a topic preview without starting an attempt', async () => {
  const f = fixture(); f.dev = true;
  f.server = { ...activity(1), preview: true, steps: [activity(1).step, activity(2).step] };
  await f.h.studyTopic('17592186050674');
  assert.equal(f.calls.length, 1);
  assert.equal(f.calls[0].path, '/api/preview?topicId=17592186050674');
  assert.equal(f.calls[0].body, null);
  assert.equal(f.h.view.feed.children.length, 1);
  assert.equal(f.h.view.timer.textContent, 'Preview');
});

test('advancing retains the earlier DOM, disables its answers, and focuses only the new step', async () => {
  const f = fixture();
  await f.h.render(activity(1, 1, { step: question(1, 'correct') }));
  const previous = f.h.view.current;
  await f.h.render(activity(2, 2));
  assert.equal(f.h.view.feed.children[0], previous);
  assert.equal(previous.dataset.history, 'true');
  assert.equal(previous.dataset.mathAcademyId, '2001');
  assert.equal(previous.dataset.contentKind, 'question');
  assert.equal(previous.querySelector('.lesson-controls'), null);
  assert.equal(previous.querySelector('.answer-actions'), null);
  assert.equal(previous.querySelectorAll('input').every(node => node.disabled && node.dataset.readOnly === 'true'), true);
  assert.match(previous.textContent, /Apply the power rule/);
  assert.equal(previous.querySelector('.step-title'), null);
  assert.equal(previous.querySelector('.step-meta'), null);
  assert.doesNotMatch(previous.textContent, /Step 1 \/ 3/);
  assert.equal(f.h.view.history.size, 1);
  assert.equal(f.h.view.current.dataset.stepDbId, 9002);
  assert.equal(f.h.view.current.dataset.contentKind, 'tutorial');
  assert.equal(f.h.view.current.dataset.mathAcademyId, '1002');
  assert.equal(f.scrolls.at(-1).node, f.h.view.current);
  assert.equal(f.h.view.track.getAttribute('aria-valuenow'), '1');
  assert.equal(f.h.view.feed.children.filter(node => node.querySelector('.lesson-controls')).length, 1);
});

test('answer feedback updates the same presentation without duplicating history or scrolling', async () => {
  const f = fixture();
  await f.h.render(activity(1, 1, { step: question(1) }));
  assert.ok(f.h.view.current.querySelector('.answer-actions'));
  assert.equal(f.h.view.current.querySelector('.step-title'), null);
  assert.equal(f.h.view.current.querySelector('.step-meta'), null);
  assert.equal(f.h.view.current.querySelector('legend').className, 'sr-only');
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

test('resuming in a fresh session restores the database presentation chain as read-only history', async () => {
  const f = fixture();
  const first = { order: 1, number: 1, total: 3, step: question(11, 'correct') };
  const second = { order: 2, number: 1, total: 3, step: question(12, 'correct') };
  f.server = activity(13, 2, { status: 'paused', history: [first, second], progress: { stepNumber: 2, totalSteps: 3, presented: 3 } });
  await f.h.openTask('123');
  assert.equal(f.calls.some(call => call.path === '/api/resume'), true);
  assert.deepEqual(f.h.view.feed.children.map(node => node.dataset.stepDbId), [9011, 9012, 9013]);
  assert.equal(f.h.view.history.size, 2);
  for (const node of f.h.view.feed.children.slice(0, 2)) {
    assert.equal(node.dataset.history, 'true');
    assert.equal(node.querySelector('.lesson-controls'), null);
    assert.equal(node.querySelector('.answer-actions'), null);
    assert.equal(node.querySelectorAll('input').every(input => input.disabled), true);
    assert.match(node.textContent, /Apply the power rule/);
  }
  assert.equal(f.scrolls.at(-1).node, f.h.view.current);
  await f.h.render(activity(14, 3, { progress: { stepNumber: 3, totalSteps: 3, presented: 4 } }));
  assert.equal(f.h.view.feed.children.length, 4);
  assert.equal(f.calls.length, 2); // No extra history request while advancing.
});

test('a completed attempt reopens as a full read-only lesson history without restarting its timer', async () => {
  const f = fixture();
  await f.h.render(activity(2, 3, {
    status: 'completed', xp: 7, xpBase: 10,
    step: { ...activity(2).step, status: 'completed' },
    history: [{ order: 1, number: 1, total: 3, step: question(1, 'correct') }],
    progress: { stepNumber: 3, totalSteps: 3, presented: 2 },
  }));
  assert.equal(f.h.clock.running, false);
  assert.equal(f.h.view.history.size, 2);
  assert.equal(f.h.view.feed.children.length, 3);
  assert.match(f.h.view.current.textContent, /Activity complete/);
  assert.equal(f.h.view.current.querySelector('.completion-xp').textContent, '7/10 XP');
  for (const node of f.h.view.feed.children.slice(0, 2)) {
    assert.equal(node.dataset.history, 'true');
    assert.equal(node.querySelector('.answer-actions'), null);
    assert.equal(node.querySelector('.lesson-controls'), null);
  }
  assert.equal(f.calls.length, 0);
});

test('resumed instruction history has no response badges while answered questions retain feedback', async () => {
  const f = fixture();
  const tutorial = { ...activity(1).step, status: 'completed' };
  const example = { ...activity(2).step, kind: 'example', status: 'completed', solution: 'The worked solution.' };
  const response = { ...question(3, 'completed'), fields: [{ id: 30, key: 'field-1', type: 'free', response: { value: 'My answer' } }] };
  await f.h.render(activity(4, 4, {
    status: 'paused',
    history: [tutorial, example, response].map((step, i) => ({ order: i + 1, number: i + 1, total: 4, step })),
  }));
  const [tutorialCard, exampleCard, questionCard] = f.h.view.feed.children;
  assert.equal(tutorialCard.querySelector('.feedback'), null);
  assert.equal(exampleCard.querySelector('.feedback'), null);
  assert.match(exampleCard.querySelector('.worked-solution').textContent, /The worked solution/);
  assert.match(questionCard.querySelector('.feedback').textContent, /Response saved/);
  assert.equal(f.calls.length, 0);

  const preview = fixture(); preview.dev = true;
  await preview.h.preview({ activityId: 456, learner: { id: 'test' }, steps: [example, tutorial] }, 1);
  assert.equal(preview.h.view.feed.querySelector('.feedback'), null);
  assert.match(preview.h.view.feed.querySelector('.worked-solution').textContent, /The worked solution/);
});

test('database history replaces stale browser entries without revealing later steps', async () => {
  const f = fixture();
  await f.h.render(activity(99, 1));
  await f.h.render(activity(3, 2, {
    history: [{ order: 1, number: 1, total: 3, step: activity(1).step }],
    progress: { stepNumber: 2, totalSteps: 3, presented: 2 },
  }));
  assert.deepEqual(f.h.view.feed.children.map(node => node.dataset.stepDbId), [9001, 9003]);
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
  assert.equal(f.h.view.feed.children[0].dataset.mathAcademyId, '1001');
  assert.equal(f.h.view.current.dataset.mathAcademyId, '1002');
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

test('manual pause stops working time, preserves a draft, and stays paused across visibility and reload', async () => {
  const f = fixture();
  const step = { ...question(1), markdown: 'Enter {{value}}.', fields: [{ id: 30, key: 'value', type: 'blank', answerType: 'text' }] };
  f.server = activity(1, 1, { step });
  await f.h.render(structuredClone(f.server));
  f.h.view.current.querySelector('input').value = 'typed draft';
  f.h.view.current.querySelector('form').dispatchEvent(new Event('input'));
  f.now += 3000;
  await f.h.toggleLessonPause();
  assert.equal(f.h.clock.running, false);
  assert.equal(f.h.clock.elapsed, 13);
  assert.equal(f.h.view.pause.textContent, 'Resume');
  assert.equal(f.h.view.current.querySelector('input').value, 'typed draft');
  assert.equal(f.h.view.current.querySelector('input').disabled, true);
  f.now += 60000; f.h.updateTaskTimer();
  assert.equal(f.h.view.timer.textContent, '0:13');
  f.document.hidden = true; await f.h.pauseWhenHidden();
  f.document.hidden = false; await f.h.refreshPageOnReturn();
  assert.equal(f.calls.filter(call => call.path === '/api/resume').length, 0);
  const reopened = fixture(f.storage); reopened.server = structuredClone(f.server);
  await reopened.h.openTask(123);
  assert.equal(reopened.calls.some(call => call.path === '/api/resume'), false);
  assert.equal(reopened.h.view.current.querySelector('input').value, 'typed draft');
  assert.equal(reopened.h.view.pause.textContent, 'Resume');
  await reopened.h.toggleLessonPause();
  assert.equal(reopened.calls.filter(call => call.path === '/api/resume').length, 1);
  assert.equal(reopened.h.clock.running, true);
  assert.equal(reopened.h.view.current.querySelector('input').value, 'typed draft');
  assert.equal(reopened.h.view.current.querySelector('input').disabled, false);
});

test('an uncertain manual pause stops the local clock and retries the same request', async () => {
  const f = fixture(); f.server = activity(1);
  await f.h.render(structuredClone(f.server));
  let attempts = 0;
  f.respond = async path => {
    if (path === '/api/pause' && ++attempts === 1) throw new Error('Reply lost');
    return null;
  };
  f.now += 3000; await f.h.toggleLessonPause();
  assert.equal(f.h.clock.running, false);
  assert.equal(f.h.view.pause.disabled, true);
  const first = f.calls.find(call => call.path === '/api/pause').body;
  await f.h.retry();
  const requests = f.calls.filter(call => call.path === '/api/pause');
  assert.equal(requests.length, 2); assert.deepEqual(requests[1].body, first);
  assert.equal(f.h.view.pause.textContent, 'Resume');
  assert.equal(f.h.view.pause.disabled, false);
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

test('Study identifies the selected plan and distinguishes target shortages from an empty plan', async () => {
  const f = fixture();
  const main = f.document.getElementById('main');
  f.server = { learner: { selfDirected: true, queue: [6] }, activities: [activity(1, 1)] };
  await f.h.home();
  assert.equal(main.querySelector('h1').textContent, 'Your study plan');
  assert.equal(main.querySelector('h1').className, 'sr-only');
  assert.equal(main.querySelector('.page-heading'), null);
  assert.equal(main.querySelector('.subheading'), null);
  assert.equal(main.querySelector('.eyebrow'), null);
  f.server.activities = [];
  await f.h.home();
  assert.equal(main.querySelector('.empty-state').querySelector('h2').textContent, 'No ready activities yet');
  assert.match(main.querySelector('.empty-state').textContent, /selected topics/);
  f.server.learner.queue = [];
  f.server.learner.targets = [30];
  await f.h.home();
  assert.equal(main.querySelector('.empty-state').querySelector('h2').textContent, 'No ready activities yet');
  f.server.learner.targets = [];
  await f.h.home();
  assert.equal(main.querySelector('.empty-state').querySelector('h2').textContent, 'Your study plan is empty');
  f.server.learner.selfDirected = false;
  await f.h.home();
  assert.equal(main.querySelector('h1').textContent, 'Next up');
  assert.equal(main.querySelector('h1').className, 'sr-only');
  assert.equal(main.querySelector('.subheading'), null);
  f.dev = true;
  f.server.learner.selfDirected = true;
  await f.h.home();
  assert.equal(main.querySelector('h1').textContent, 'Your study plan');
  assert.equal(f.calls.at(-1).path, '/api/preview-home');
});

test('Study and developer preview prompt an unconfigured learner to choose a course through the profile', async () => {
  const f = fixture();
  await f.h.render(activity(1));
  assert.ok(f.storage.has('course-academy.study-header'));
  f.server = { learner: { name: 'New learner', selfDirected: false }, course: null, activities: [], needsCourseSelection: true };
  let profileOpened = 0;
  f.document.getElementById('learnerName').addEventListener('click', () => profileOpened++);
  for (const dev of [false, true]) {
    f.dev = dev;
    await f.h.home();
    const main = f.document.getElementById('main');
    assert.equal(main.querySelector('h1').textContent, 'Choose your first course');
    assert.equal(main.querySelector('.queue-foot'), null);
    assert.equal(f.document.getElementById('errorBanner').hidden, true);
    assert.equal(f.document.getElementById('courseLink').getAttribute('href'), '/progress');
    assert.equal(f.storage.has('course-academy.study-header'), false);
    main.querySelector('button').click();
    assert.equal(f.calls.at(-1).path, dev ? '/api/preview-home' : '/api/queue');
  }
  assert.equal(profileOpened, 2);
  assert.equal(f.calls.length, 2);
});

test('self-directed Study offers Begin for prepared locked lessons and selections without a task', async () => {
  const f = fixture();
  f.server = { learner: { selfDirected: true, queue: [6] }, activities: [
    activity(1, 1, { status: 'locked', taskId: 81, progress: null }),
    activity(2, 1, { status: 'selected', taskId: null, progress: null }),
  ] };
  await f.h.home();
  const rows = f.document.getElementById('main').querySelectorAll('.queue-card');
  assert.equal(rows.length, 2);
  assert.equal(rows.every(row => row.querySelector('button').textContent === 'Begin →'), true);
  assert.equal(rows.every(row => !row.querySelector('button').disabled), true);
  assert.equal(rows.every(row => row.querySelector('.queue-progress-track') === null), true);
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

test('inline lesson fields stay inside the submitting form and preserve saved answers and feedback', async () => {
  const f = fixture();
  const step = { itemId: 42, kind: 'question', title: 'Fill in', status: 'correct', canContinue: true,
    markdown: "$y=$ {{blank-1}}, then choose {{term}}.", fields: [
      { id: 11, key: 'blank-1', type: 'blank', response: { value: '2x' } },
      { id: 12, key: 'term', type: 'select', choices: [{ id: 91, type: 'text', value: 'derivative' }], response: { choiceId: 91 } },
    ] };
  await f.h.render(activity(42, 2, { step }));
  const current = f.h.view.current;
  assert.equal(current.querySelectorAll('.answer-inline').length, 2);
  assert.equal(current.querySelector('.answer-fields').hidden, true);
  const form = current.querySelector('form');
  assert.equal(form.querySelector('input').value, '2x');
  assert.equal(form.querySelector('select').value, '91');
  assert.equal(form.querySelector('.answer-select-value').textContent, 'derivative');
  assert.equal(form.querySelector('.answer-select-trigger').disabled, true);
  assert.equal(current.querySelector('.feedback').dataset.feedback, 'correct');
  assert.match(current.querySelector('.feedback-heading').textContent, /Correct/);
  await f.h.render(activity(43, 2, { step: { ...step, itemId: 43, status: 'incorrect' } }));
  assert.equal(f.h.view.current.querySelector('.feedback').dataset.feedback, 'incorrect');
  assert.match(f.h.view.current.querySelector('.feedback-heading').textContent, /Incorrect/);
});

test('returning to Study refreshes its queue without a Refresh button or a loading flash', async () => {
  const f = fixture(); f.server = { activities: [activity(1)] };
  await f.h.home();
  const original = f.document.getElementById('main').querySelector('.queue-card');
  assert.equal(f.document.getElementById('main').querySelectorAll('button').some(node => /Refresh/.test(node.textContent)), false);
  f.server = { activities: [activity(2, 2, { title: 'Updated lesson' })] };
  f.document.hidden = true; await f.h.refreshPageOnReturn();
  assert.equal(f.calls.length, 1);
  f.document.hidden = false;
  let release;
  f.delay = new Promise(resolve => { release = resolve; });
  const refresh = f.h.refreshPageOnReturn();
  await f.h.refreshPageOnReturn();
  assert.equal(f.calls.length, 2);
  assert.equal(f.document.getElementById('main').querySelector('.queue-card'), original);
  release(); await refresh;
  assert.match(f.document.getElementById('main').textContent, /Updated lesson/);
  f.delay = null; f.dev = true;
  await f.h.refreshPageOnReturn();
  assert.equal(f.calls.at(-1).path, '/api/preview-home');
  await f.h.preview({ activityId: 456, title: 'Preview', steps: [{ kind: 'tutorial', markdown: 'Read.' }] }, 0);
  const calls = f.calls.length;
  await f.h.refreshPageOnReturn();
  assert.equal(f.calls.length, calls);
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


test('question shortages offer continuation and deferred practice is shown without claiming completion', async () => {
  const f=fixture();
  await f.h.render(activity(1,2,{step:{...question(1,'correct'),practiceShortage:{stepId:55,title:'Skill'}}}));
  assert.match(f.h.view.current.textContent,/No fresh questions remain/);
  assert.ok(f.h.view.current.querySelectorAll('button').some(b=>b.textContent==='Continue to next skill →'));
  await f.h.render(activity(1,3,{awaitingQuestions:false,deferredSteps:[{stepId:55,title:'Skill'}],step:question(1,'correct')}));
  assert.ok(f.h.view.current.querySelectorAll('button').some(b=>b.textContent==='Next step →'));
  assert.equal(f.h.view.current.querySelector('.completion-xp'),null);
  await f.h.render(activity(1,3,{status:'paused',awaitingQuestions:true,canResumePractice:false,xp:0,xpBase:7,deferredSteps:[{stepId:55,title:'Skill'}],step:question(1,'correct')}));
  assert.match(f.h.view.current.textContent,/Practice paused/);
  assert.match(f.h.view.current.textContent,/ran out of fresh questions/);
  assert.match(f.h.view.current.textContent,/Waiting for new questions/);
  assert.match(f.h.view.current.textContent,/Lesson XP is pending/);
  assert.equal(f.h.view.current.querySelector('.completion-xp'),null);
  assert.equal(f.h.view.current.querySelector('.deferred-skills').textContent,'Skill');
  assert.ok(!f.h.view.current.textContent.includes('Activity complete'));
  assert.equal(f.h.clock.running,false);
  await f.h.render(activity(1,3,{status:'paused',awaitingQuestions:true,canResumePractice:true,deferredSteps:[{stepId:55,title:'Skill'}],step:question(1,'correct')}));
  assert.match(f.h.view.current.textContent,/New questions are available/);
  assert.ok(f.h.view.current.querySelectorAll('button').some(b=>b.textContent==='Resume unfinished practice →'));
});


test('an active Next click recovers a confirmed paused state and advances exactly once', async () => {
  const f=fixture();f.server=activity(1);
  await f.h.render(structuredClone(f.server));
  let attempts=0;
  f.respond=async(path)=>{
    if(path==='/api/continue' && ++attempts===1) return {ok:false,status:409,json:async()=>({error:'Resume the lesson before continuing',code:'lesson-paused'})};
    if(path==='/api/continue') f.server=activity(2,2);
  };
  await f.h.mutation('/api/continue',{taskId:123,itemId:1});
  assert.deepEqual(f.calls.map(call=>call.path),['/api/continue','/api/resume','/api/continue']);
  assert.notEqual(f.calls[0].body.requestId,f.calls[2].body.requestId);
  assert.equal(f.h.view.current.dataset.stepDbId,9002);
  assert.equal(f.document.getElementById('errorBanner').hidden,true);
});

test('stale Next never advances the new item after another tab has already advanced', async () => {
  const f=fixture();f.server=activity(2,2);
  await f.h.render(activity(1));
  f.respond=async(path)=>path==='/api/continue'?{ok:false,status:409,json:async()=>({error:'Resume the lesson before continuing',code:'lesson-paused'})}:null;
  await f.h.mutation('/api/continue',{taskId:123,itemId:1});
  assert.deepEqual(f.calls.map(call=>call.path),['/api/continue','/api/resume']);
  assert.equal(f.h.view.current.dataset.stepDbId,9002);
});

test('submitting an answer freezes working time while grading waits and the next item restarts it', async () => {
  const f = fixture(); f.server = activity(1, 1, { step: question(1) });
  await f.h.render(structuredClone(f.server));
  let release; f.delay = new Promise(resolve => { release = resolve; });
  f.server = activity(1, 1, { elapsedSeconds: 13, step: question(1, 'correct') });
  f.now += 3000;
  const save = f.h.mutation('/api/answer', { taskId: 123, itemId: 1, responses: [{ fieldId: 30, choiceId: 41 }] });
  assert.equal(f.h.clock.running, false); assert.equal(f.h.clock.elapsed, 13);
  f.now += 60000; f.h.updateTaskTimer(); assert.equal(f.h.view.timer.textContent, '0:13');
  release(); await save; assert.equal(f.h.view.timer.textContent, '0:13');
  assert.equal(f.calls[0].body.submissionId, f.calls[0].body.requestId);
  f.delay = null; f.server = activity(2, 2, { elapsedSeconds: 13, step: question(2) });
  await f.h.mutation('/api/continue', { taskId: 123, itemId: 1 });
  assert.equal(f.h.clock.running, true);
  f.now += 2000; f.h.updateTaskTimer(); assert.equal(f.h.view.timer.textContent, '0:15');
});

test('an answer retries a confirmed concurrent basis conflict once while preserving its submission identity', async () => {
  const f=fixture(); f.server=activity(1,1,{step:question(1,'correct')});
  await f.h.render(activity(1,1,{step:question(1)}));
  let attempts=0;
  f.respond=async()=> ++attempts===1 ? {ok:false,status:409,json:async()=>({error:'Content changed',code:'basis-conflict'})} : null;
  await f.h.mutation('/api/answer',{taskId:123,itemId:1,responses:[{fieldId:30,choiceId:41}]});
  assert.equal(f.calls.length,2);
  assert.notEqual(f.calls[0].body.requestId,f.calls[1].body.requestId);
  assert.equal(f.calls[0].body.submissionId,f.calls[1].body.submissionId);
  assert.equal(f.h.clock.running,false);
});

test('unknown save outcomes keep the original request identity and do not resume or retry automatically', async () => {
  const f=fixture();f.server=activity(1);await f.h.render(structuredClone(f.server));
  f.respond=async()=>{throw new Error('Network unavailable');};
  await f.h.mutation('/api/continue',{taskId:123,itemId:1});
  assert.equal(f.calls.length,1);
  assert.equal(f.document.getElementById('errorBanner').hidden,false);
});


test('paused answer recovery keeps the selected answer and does not recover unrelated validation errors', async () => {
  const f=fixture();f.server=activity(1,1,{step:question(1)});
  await f.h.render(activity(1,1,{step:question(1)}));
  let attempts=0;
  f.respond=async(path)=>{
    if(path==='/api/answer' && ++attempts===1) return {ok:false,status:409,json:async()=>({error:'Resume the lesson before continuing',code:'lesson-paused'})};
    if(path==='/api/answer') f.server=activity(1,1,{step:question(1,'correct')});
  };
  const responses=[{fieldId:30,choiceId:41}];
  await f.h.mutation('/api/answer',{taskId:123,itemId:1,responses});
  assert.deepEqual(f.calls.map(call=>call.path),['/api/answer','/api/resume','/api/answer']);
  assert.deepEqual(f.calls[2].body.responses,responses);
  f.calls.length=0;
  f.respond=async()=>({ok:false,status:409,json:async()=>({error:'Foreign question',code:'validation'})});
  await f.h.mutation('/api/answer',{taskId:123,itemId:1,responses});
  assert.equal(f.calls.length,1);
  assert.equal(f.document.getElementById('errorBanner').hidden,false);
});


test('assessment navigation and actions sit outside the question card and lock while saving', async () => {
  const f = fixture();
  const step = question(7);
  const data = activity(7, 7, { type: 'assessment', remainingSeconds: 900, step,
    questions: Array.from({ length: 8 }, (_, i) => ({ questionId: 9001 + i, number: i + 1, answered: i < 6, active: i === 6 })) });
  await f.h.render(data);
  const current = f.h.view.current, card = current.querySelector('.content-card');
  const controls = current.querySelector('.assessment-controls');
  const nav = controls.querySelector('.assessment-navigation'), actions = controls.querySelector('.assessment-actions');
  assert.equal(current.children[0], card);
  assert.equal(current.children[1], controls);
  assert.equal(card.contains(nav), false);
  assert.equal(card.contains(actions), false);
  assert.equal(card.contains(f.h.view.track), false);
  assert.equal(card.querySelector('form').querySelector('button'), null);
  assert.equal(nav.children.length, 8);
  assert.deepEqual(nav.children.map(button => button.textContent), ['1', '2', '3', '4', '5', '6', '7', '8']);
  assert.equal(nav.children[0].dataset.answered, 'true');
  assert.equal(nav.children[0].getAttribute('aria-label'), 'Question 1, answered');
  assert.equal(nav.children[6].dataset.answered, 'false');
  assert.equal(nav.children[6].getAttribute('aria-current'), 'step');
  assert.deepEqual(actions.children.map(button => button.textContent), ['Previous question', 'Next question', 'Submit assessment']);
  f.h.setBusy(true);
  assert.ok(controls.querySelectorAll('button').every(button => button.disabled));
  f.h.setBusy(false);
  assert.ok(controls.querySelectorAll('button').every(button => !button.disabled));
});

test('assessment submits without correctness feedback and keeps its countdown running while paused', async () => {
  const f = fixture();
  const data = activity(1, 1, { type: 'assessment', remainingSeconds: 900,
    step: { itemId: 1, kind: 'question', markdown: 'Enter two.', status: 'submitted', canContinue: true,
      fields: [{ id: 1, key: 'value', type: 'blank', answerType: 'math', response: { type: 'math', value: '3' } }] } });
  await f.h.render(data);
  assert.equal(f.h.view.timer.textContent, '15:00 left');
  assert.equal(f.h.view.current.querySelector('.feedback'), null);
  assert.equal(f.h.view.current.querySelector('.worked-solution'), null);
  assert.match(f.h.view.current.textContent, /Next step/);
  f.now += 60000;
  f.h.updateTaskTimer();
  assert.equal(f.h.view.timer.textContent, '14:00 left');
  await f.h.render({ ...data, status: 'paused', remainingSeconds: 840 });
  f.now += 60000;
  f.h.updateTaskTimer();
  assert.equal(f.h.view.timer.textContent, '13:00 left');
  assert.equal(f.h.clock.running, false);
});

test('assessment deadline rejection finalizes expiry without retrying late answers', async () => {
  const f = fixture();
  f.server = activity(1, 1, { type: 'assessment', remainingSeconds: 0, status: 'completed' });
  await f.h.render(activity(1, 1, { type: 'assessment', remainingSeconds: 1 }));
  f.respond = async path => path === '/api/answer'
    ? { ok: false, json: async () => ({ ok: false, code: 'assessment-expired', error: 'Assessment deadline has elapsed' }) }
    : null;
  await f.h.mutation('/api/answer', { taskId: 123, itemId: 1, responses: [] });
  assert.deepEqual(f.calls.map(c => c.path), ['/api/answer', '/api/expire']);
  assert.ok(f.calls[1].body.requestId);
  assert.match(f.h.view.current.textContent, /Activity complete/);
});

test('reopening an expired paused assessment expires it before any resume request', async () => {
  const f = fixture();
  f.server = activity(1, 1, { type: 'assessment', status: 'paused', expired: true });
  f.respond = async path => {
    if (path === '/api/expire') { f.server.status = 'completed'; return { ok: true, json: async () => structuredClone(f.server) }; }
    return null;
  };
  await f.h.openTask(123);
  assert.deepEqual(f.calls.map(c => c.path), ['/api/task?taskId=123', '/api/expire']);
  assert.match(f.h.view.current.textContent, /Activity complete/);
});


test('assessment completion replaces submitted archived cards with revealed server history', async () => {
  const f = fixture();
  const first = { itemId: 1, kind: 'question', markdown: 'First question', status: 'submitted', canContinue: true, fields: [] };
  const second = { ...first, itemId: 2, markdown: 'Second question' };
  await f.h.render(activity(1, 1, { type: 'assessment', step: first, remainingSeconds: 800 }));
  await f.h.render(activity(2, 2, { type: 'assessment', step: second, remainingSeconds: 700 }));
  const old = f.h.view.history.get('1');
  assert.equal(old, undefined); // Active tests render only the freely navigable current question.
  await f.h.render(activity(2, 2, { type: 'assessment', status: 'completed',
    step: { ...second, status: 'correct', solution: 'Second solution' },
    history: [{ order: 1, number: 1, total: 3, step: { ...first, status: 'incorrect', solution: 'First solution' } }] }));
  const revealed = f.h.view.history.get('1');
  assert.notEqual(revealed, old);
  assert.match(revealed.textContent, /Incorrect/);
  assert.match(revealed.textContent, /First solution/);
});
