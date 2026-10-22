import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';
import { completionEstimate, withForecastGoal, courseCompletionEstimates } from '../ui/forecast.js';

process.env.TZ = 'America/Los_Angeles';
const source = (await readFile(new URL('../ui/forecast-sidebar.js', import.meta.url), 'utf8'))
  .replace(/^import .*;\n/gm, '').replaceAll('export ', '');
const origin = new Date(2026, 9, 21, 12).getTime();
const formatDate = value => new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(value));
function model() {
  const forecast = {
    capturedAt: new Date(origin).toISOString(), scope: { courses: ['255', '256', '341'] },
    inventory: { remainingTopics: 60, remainingLessonBaseXp: 600, estimatedTopics: [] },
    pace: { observedDays: 7, baseXpPerDay: 100, earnedXp: 840, dailyEarnedXpGoal: 240,
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
function fixture() {
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
  const f = { data: model(), calls: 0, workers: [], controller: new AbortController() };
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
  const context = vm.createContext({ document, Intl, Number, Date, AbortController,
    completionEstimate, withForecastGoal, courseCompletionEstimates, Worker,
  });
  const create = vm.runInContext(`(() => { ${source}; return createForecastSidebar; })()`, context);
  f.view = create({ signal: f.controller.signal }); document.body.append(...f.view.cards);
  f.text = () => f.view.cards.map(card => card.textContent).join(' ');
  f.all = (node = document.body) => [node, ...node.children.flatMap(child => f.all(child))];
  f.times = () => f.all().filter(node => node.tagName === 'time');
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
  assert.deepEqual(tables[0].children[0].children[0].children.map(cell => cell.textContent), ['', '120 XP/day', '240 XP/day']);
  assert.deepEqual(tables[0].children[1].children.map(row => row.children[0].textContent), ['All', 'MTH 255', 'MTH 256', 'MTH 341']);
  assert.doesNotMatch(f.text(), /Course catch-up|7-day average|Daily goal|One third|Based on your Targets filters|Catch-up includes|excludes today/);
  const courses = courseCompletionEstimates(f.data);
  const dates = [f.data.currentPace, f.data.goalPace, ...courses.flatMap(course => [course.currentPace, course.goalPace])];
  assert.deepEqual(f.times().map(time => time.dateTime), dates.map(estimate => estimate.date));
  assert.deepEqual(f.times().map(time => time.textContent), dates.map(estimate => formatDate(estimate.date)));
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
  assert.match(f.text(), /480 XP\/day/);
  assert.doesNotMatch(f.text(), /160 XP\/day/);
  assert.equal(f.calls, 1);
});

test('a goal changed during a read survives that response, but later fresh server goals win', async () => {
  const f = fixture(); let finish;
  f.reader = () => new Promise(resolve => { finish = resolve; });
  const pending = f.view.refresh(); f.view.updateGoal(480); finish(f.data); await pending;
  assert.match(f.text(), /480 XP\/day/);
  f.reader = async () => withForecastGoal(f.data, 600);
  await f.view.refresh();
  assert.match(f.text(), /600 XP\/day/);
  assert.doesNotMatch(f.text(), /480 XP\/day/);
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
  assert.match(f.text(), /Not catching up/);
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
  assert.equal(f.workers.at(-1).terminated, true);
  finish(withForecastGoal(f.data, 800)); await pending;
  assert.equal(f.text(), before);
});
