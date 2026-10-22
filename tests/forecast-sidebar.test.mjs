import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { completionEstimate, withForecastGoal, courseCompletionEstimates } from '../ui/forecast.js';

process.env.TZ = 'America/Los_Angeles';
const source = (await readFile(new URL('../ui/forecast-sidebar.js', import.meta.url), 'utf8'))
  .replace(/^import .*;\n/gm, '').replaceAll('export ', '');
const origin = new Date(2026, 9, 21, 12).getTime();
function model() {
  const forecast = {
    basis: 1, capturedAt: new Date(origin).toISOString(), scope: { courses: ['255', '256', '341'],
      includeQueue: true, weekSelection: { kind: 'all' }, prerequisiteDepth: 2 },
    inventory: { remainingTopics: 60, remainingLessonBaseXp: 600, estimatedTopics: [] },
    pace: { observedThrough: new Date(2026, 9, 21).toISOString(), observedDays: 7, baseXpPerDay: 100, earnedXp: 840, dailyEarnedXpGoal: 240,
      earnedToBaseFactor: 1.2, goalBaseXpPerDay: 200, reviewBaseXp: 0, otherBaseXp: 0, reviewAttempts: 0 },
    overhead: { retryFactor: 1, quizRatio: 0, averageQuizBaseXp: 15 },
    growth: { total: { baseXpPerDay: 0, estimatedTopics: [], isLowerBound: false } },
    initialWorkBaseXp: 600, dailyDemandBaseXp: 0,
    courses: ['255', '256', '341'].map((code, i) => ({ code, remainingTopics: 10 * (i + 1),
      initialWorkBaseXp: 100 * (i + 1), dailyDemandBaseXp: 0 })),
    currentPace: completionEstimate(600, 0, 100, origin),
  };
  return withForecastGoal(forecast, 240);
}
function fixture(storage = new Map()) {
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.children = []; this.attrs = {}; }
    append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
    replaceChildren(...nodes) { this.children.forEach(node => { node.parent = null; }); this.children = []; this.text = ''; this.append(...nodes); }
    setAttribute(name, value) { this.attrs[name] = String(value); }
    get textContent() { return (this.text || '') + this.children.map(node => node.textContent).join(''); }
    set textContent(value) { this.text = String(value); this.children = []; }
    get isConnected() { for (let node = this; node; node = node.parent) if (node === document.body) return true; return false; }
  }
  const document = { createElement: tag => new Element(tag), body: new Element('body') };
  const f = { data: model(), calls: 0, workers: [], controller: new AbortController(), storage };
  let now = origin;
  f.setNow = at => { now = at; };
  f.reader = async () => structuredClone(f.data);
  class Worker {
    constructor(path, options) {
      assert.equal(path, '/ui/forecast-worker.js'); assert.equal(options.type, 'module');
      f.workers.push(this);
    }
    postMessage(scope) {
      f.calls++; f.workerScope = scope;
      Promise.resolve(f.reader()).then(forecast => {
        if (!this.terminated) this.onmessage({ data: { forecast } });
      }, error => { if (!this.terminated) this.onmessage({ data: { error: error.message } }); });
    }
    terminate() { this.terminated = true; }
  }
  const context = vm.createContext({ document, Intl, Number, AbortController,
    Date: class extends Date { constructor(...args) { super(...(args.length ? args : [now])); } static now() { return now; } },
    sessionStorage: {
      getItem(key) { if (f.blockStorage) throw new Error('Blocked'); return storage.get(key) ?? null; },
      setItem(key, value) { if (f.blockStorage) throw new Error('Full'); storage.set(key, value); },
    },
    completionEstimate, withForecastGoal, courseCompletionEstimates, Worker,
  });
  const create = vm.runInContext(`(() => { ${source}; return createForecastSidebar; })()`, context);
  f.mount = () => {
    f.controller.abort(); f.controller = new AbortController();
    f.view = create({ signal: f.controller.signal }); document.body.replaceChildren(...f.view.cards);
  };
  f.mount();
  f.text = () => f.view.cards.map(card => card.textContent).join(' ');
  f.all = (node = document.body) => [node, ...node.children.flatMap(child => f.all(child))];
  f.times = () => f.all().filter(node => node.tagName === 'time');
  f.headers = () => f.all().find(node => node.tagName === 'thead').children[0].children.map(cell => cell.textContent);
  return f;
}

test('one completion table shows overall and course dates beneath dynamic full-pace headers', async () => {
  const f = fixture();
  assert.match(f.text(), /Calculating/);
  await f.view.refresh();
  assert.equal(f.view.cards.length, 1);
  assert.deepEqual(f.all().filter(node => node.tagName === 'h2').map(node => node.textContent), ['Estimated completion']);
  const tables = f.all().filter(node => node.tagName === 'table');
  assert.equal(tables.length, 1);
  assert.deepEqual(f.headers(), ['XP/day', '120', '240']);
  assert.deepEqual(tables[0].children[1].children.map(row => row.children[0].textContent), ['All Courses', 'MTH 255', 'MTH 256', 'MTH 341']);
  assert.doesNotMatch(f.text(), /Course catch-up|7-day average|Daily goal|One third|Based on your Targets filters|Catch-up includes|excludes today/);
  const courses = courseCompletionEstimates(f.data);
  const dates = [f.data.currentPace, f.data.goalPace, ...courses.flatMap(course => [course.currentPace, course.goalPace])];
  assert.deepEqual(f.times().map(time => time.dateTime), dates.map(estimate => estimate.date));
  assert.deepEqual(f.times().map(time => time.textContent), ['10/27/26', '10/24/26', '10/24/26', '10/23/26', '10/27/26', '10/24/26', '10/30/26', '10/26/26']);
  assert.equal(f.calls, 1);
  assert.deepEqual(Object.keys(f.workerScope), []);
  assert.equal(f.workers[0].terminated, true);
});

test('changing a goal updates all goal dates without fetching and preserves current dates', async () => {
  const f = fixture(); await f.view.refresh();
  const before = f.times().map(time => time.dateTime);
  f.view.updateGoal(480);
  const after = f.times().map(time => time.dateTime);
  for (let i = 0; i < 8; i++) {
    if (i % 2 === 0) assert.equal(after[i], before[i]);
    else assert.ok(Date.parse(after[i]) < Date.parse(before[i]));
  }
  assert.deepEqual(f.headers(), ['XP/day', '120', '480']);
  assert.equal(f.calls, 1);
});

test('a goal changed during a read survives that response, but later fresh server goals win', async () => {
  const f = fixture(); let finish;
  f.reader = () => new Promise(resolve => { finish = resolve; });
  const pending = f.view.refresh(); f.view.updateGoal(480); finish(f.data); await pending;
  assert.deepEqual(f.headers(), ['XP/day', '120', '480']);
  f.reader = async () => withForecastGoal(f.data, 600);
  await f.view.refresh();
  assert.deepEqual(f.headers(), ['XP/day', '120', '600']);
});

test('missing goal, insufficient pace and caught-up tracks have clear states', async () => {
  const f = fixture();
  f.data = withForecastGoal(f.data, null);
  f.data.currentPace = { status: 'not-catching-up' };
  f.data.courses[0].remainingTopics = 0;
  f.data.courses[1].dailyDemandBaseXp = 100;
  f.data.courses[2].initialWorkBaseXp = null;
  await f.view.refresh();
  assert.match(f.text(), /No goal set/);
  assert.match(f.text(), /∞/);
  assert.doesNotMatch(f.text(), /Not catching up/);
  assert.equal(f.all().find(node => node.tagName === 'span' && node.textContent === '∞').attrs['aria-label'], 'Not catching up at this pace');
  assert.match(f.text(), /Caught up/);
  assert.match(f.text(), /Unavailable/);
  assert.equal(f.times().length, 0);
});

test('failed forecast loads can be retried and disposed responses cannot alter the sidebar', async () => {
  const f = fixture(); f.reader = async () => { throw new Error('Offline'); };
  await f.view.refresh(); assert.match(f.text(), /Estimates unavailable/);
  f.reader = async () => f.data;
  f.all().find(node => node.tagName === 'button').dispatchEvent(new Event('click'));
  await new Promise(resolve => setImmediate(resolve));
  assert.equal(f.times().length, 8);
  let finish; f.reader = () => new Promise(resolve => { finish = resolve; });
  const pending = f.view.refresh(), before = f.text(); f.controller.abort();
  assert.equal(f.workers.at(-1).terminated, undefined); // Finish once and cache, even after unmount.
  finish(withForecastGoal(f.data, 800)); await pending;
  assert.equal(f.text(), before);
  assert.equal(f.workers.at(-1).terminated, true);
});

test('rates round upward only for display and fallback lesson XP adds no footer', async () => {
  const f = fixture(); f.data.pace.earnedXp = 809;
  f.data.inventory.estimatedTopics = [{ topicId: 12 }];
  await f.view.refresh();
  assert.deepEqual(f.headers(), ['XP/day', '116', '240']);
  assert.doesNotMatch(f.text(), /Includes estimated lesson XP/);
  assert.equal(f.data.pace.earnedXp, 809);
});

test('navigation and page reload render cached results immediately and unchanged basis skips the worker', async () => {
  const f = fixture(); await f.view.refresh({ basis: 1 });
  const dates = f.times().map(time => time.dateTime);
  f.mount();
  assert.equal(f.times().length, 8);
  await f.view.refresh({ basis: 1 });
  assert.equal(f.calls, 1);
  const reloaded = fixture(f.storage);
  assert.deepEqual(reloaded.times().map(time => time.dateTime), dates);
  assert.equal(reloaded.calls, 0);
  await reloaded.view.refresh({ basis: 1 });
  assert.equal(reloaded.calls, 0);
});

test('changed database basis refreshes in background while retaining the cached table on failure', async () => {
  const f = fixture(); await f.view.refresh({ basis: 1 });
  const before = f.text();
  f.reader = async () => { throw new Error('Offline'); };
  await f.view.refresh({ basis: 2 });
  assert.equal(f.calls, 2); assert.equal(f.text(), before);
  f.data.basis = 2; f.reader = async () => f.data;
  await f.view.refresh({ basis: 2 });
  assert.equal(f.calls, 3);
  await f.view.refresh({ basis: 2 });
  assert.equal(f.calls, 3);
});

test('replacing a sidebar reuses its in-flight forecast and caches the result', async () => {
  const f = fixture(); let finish;
  f.reader = () => new Promise(resolve => { finish = resolve; });
  const first = f.view.refresh({ basis: 1 });
  f.mount();
  const second = f.view.refresh({ basis: 1 });
  assert.equal(f.calls, 1);
  finish(f.data); await Promise.all([first, second]);
  assert.equal(f.times().length, 8);
  assert.equal(f.calls, 1);
});

test('cache expires at local midnight and corrupt storage falls back to a fresh calculation', async () => {
  const f = fixture(); await f.view.refresh({ basis: 1 });
  f.setNow(new Date(2026, 9, 22, 0, 1).getTime()); f.mount();
  assert.match(f.text(), /Calculating/);
  f.data.pace.observedThrough = new Date(2026, 9, 22).toISOString();
  await f.view.refresh({ basis: 1 });
  assert.equal(f.calls, 2);
  const bad = fixture(new Map([['course-academy.forecast.v1', '{invalid']]));
  await bad.view.refresh({ basis: 1 });
  assert.equal(bad.times().length, 8);
});

test('goal changes persist immediately in cache without altering its measured pace', async () => {
  const f = fixture(); await f.view.refresh({ basis: 1 });
  f.view.updateGoal(450);
  const next = fixture(f.storage);
  assert.deepEqual(next.headers(), ['XP/day', '120', '450']);
  assert.equal(next.calls, 0);
});

test('an older in-flight snapshot is refreshed when a newer database basis is already known', async () => {
  const f = fixture(); let finish;
  f.reader = () => new Promise(resolve => { finish = resolve; });
  const oldRead = f.view.refresh({ basis: 1 });
  const newerRead = f.view.refresh({ basis: 2 });
  f.reader = async () => ({ ...f.data, basis: 2 });
  finish(f.data); await Promise.all([oldRead, newerRead]);
  assert.equal(f.calls, 2);
  const next = fixture(f.storage);
  await next.view.refresh({ basis: 2 });
  assert.equal(next.calls, 0);
});

test('unavailable storage preserves memory caching and restricted old scopes are rejected', async () => {
  const f = fixture(); f.blockStorage = true;
  await f.view.refresh({ basis: 1 }); f.mount();
  assert.equal(f.times().length, 8);
  await f.view.refresh({ basis: 1 });
  assert.equal(f.calls, 1);
  const restricted = model(); restricted.scope.includeQueue = false;
  const old = fixture(new Map([['course-academy.forecast.v1', JSON.stringify(restricted)]]));
  assert.match(old.text(), /Calculating/);
  await old.view.refresh({ basis: 1 });
  assert.equal(old.calls, 1);
  assert.equal(old.times().length, 8);
});
