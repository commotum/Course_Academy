import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = (await readFile(new URL('../ui/study-stats.js', import.meta.url), 'utf8')).replace(/^import .*;\n/gm, '').replaceAll('export ', '');
const flush = () => new Promise(resolve => setImmediate(resolve));
function fixture(goal = 200, at = new Date(2026, 9, 14, 12), { storage = new Map(), holdRead = false } = {}) {
  const f = { calls: [], data: null, timers: new Map(), forecastRefreshes: 0, forecastRequests: [], goals: [] };
  const pendingRead = holdRead ? new Promise(resolve => { f.releaseRead = resolve; }) : null;
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.children = []; this.dataset = {}; this.attrs = {}; this.style = {}; }
    append(...nodes) { for (const node of nodes) { node.parent = this; this.children.push(node); } }
    replaceChildren(...nodes) { for (const node of this.children) node.parent = null; this.children = []; this.text = ''; this.append(...nodes); }
    setAttribute(name, value) { this.attrs[name] = String(value); }
    getAttribute(name) { return this.attrs[name]; }
    get textContent() { return (this.text || '') + this.children.map(node => node.textContent).join(''); }
    set textContent(value) { this.text = String(value); this.children = []; }
    get isConnected() { for (let node = this; node; node = node.parent) if (node === document.body) return true; return false; }
  }
  const document = new EventTarget(); document.body = new Element('body'); document.createElement = tag => new Element(tag);
  let now = at.getTime(), timerId = 0;
  f.setNow = date => { now = date.getTime(); };
  f.window = new EventTarget();
  const context = vm.createContext({ document, window: f.window, Intl, Number, AbortController, crypto,
    createForecastSidebar: ({ signal }) => { f.forecastSignal = signal; f.forecastCard = new Element('section'); return { cards: [f.forecastCard],
      refresh(options) { f.forecastRefreshes++; f.forecastRequests.push(options); }, updateGoal(goal) { f.goals.push(goal); } }; },
    Date: class extends Date { constructor(...args) { super(...(args.length ? args : [now])); } static now() { return now; } },
    setTimeout: (callback, delay) => { f.timers.set(++timerId, { callback, delay }); return timerId; },
    clearTimeout: id => f.timers.delete(id),
    localStorage: { setItem() {} },
    sessionStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, value) },
    readRequest: async path => {
      f.calls.push({ path });
      if (f.failRead) throw new Error('Offline');
      const days = Array.from({ length: 7 }, (_, i) => ({ earnedXp: i === 6 ? 250 : 0, workingSeconds: i === 6 ? 600 : 0 }));
      f.data ||= { basis: 1, dailyXpGoal: goal, days, earnedXp: 250, totalEarnedXp: 12400, totalXpMissing: 0,
        activityTotals: { lessons: 27, knowledgePoints: 54, reviews: 13 } };
      return { ok: true, json: async () => { if (pendingRead) await pendingRead; return structuredClone(f.data); } };
    },
    fetch: async (path, settings) => {
      const body = JSON.parse(settings.body); f.calls.push({ path, body });
      if (f.failSave) throw new Error('Reply lost');
      f.data.dailyXpGoal = body.dailyXpGoal;
      return { ok: true, json: async () => ({ learner: { dailyXpGoal: body.dailyXpGoal } }) };
    },
  });
  const api = vm.runInContext(`(() => { ${source}; return { createStudySidebar, localWeek }; })()`, context);
  f.sidebar = api.createStudySidebar(); document.body.append(f.sidebar);
  f.find = (name, node = f.sidebar) => node.className?.split(' ').includes(name) ? node : node.children.map(child => f.find(name, child)).find(Boolean);
  f.api = api; return f;
}

test('local week uses calendar midnights, including daylight-saving boundaries', () => {
  const previous = process.env.TZ; process.env.TZ = 'America/Los_Angeles';
  try {
    const f = fixture();
    const days = f.api.localWeek(new Date(2026, 10, 1, 12));
    assert.equal(days.length, 8);
    assert.equal(new Date(days[0]).getDay(), 1);
    assert.equal(new Date(days[0]).getHours(), 0);
    assert.equal(days[7] - days[6], 25 * 3_600_000);
  } finally { if (previous === undefined) delete process.env.TZ; else process.env.TZ = previous; }
});

test('refresh shows saved XP immediately and replaces it with the fresh response', async () => {
  const storage = new Map();
  fixture(200, undefined, { storage }); await flush();
  const f = fixture(200, undefined, { storage, holdRead: true });
  assert.equal(f.find('stat-xp-summary').children[0].children[1].textContent, '250');
  assert.equal(f.find('stat-week-chart').children.length, 7);
  assert.match(f.sidebar.title, /Refreshing/);
  assert.equal(f.calls.length, 1);
  assert.equal(f.forecastRefreshes, 0);
  f.data.days[6].earnedXp = 300; f.data.totalEarnedXp = 12450;
  f.releaseRead(); await flush();
  assert.equal(f.find('stat-xp-summary').children[0].children[1].textContent, '300');
  assert.equal(f.sidebar.title, '');
  assert.equal(f.forecastRefreshes, 1);
  assert.equal(JSON.parse(storage.get('course-academy.study-stats.v1')).data.totalEarnedXp, 12450);
});

test('saved statistics from another day or malformed storage do not render', async () => {
  const storage = new Map();
  fixture(200, new Date(2026, 9, 13, 12), { storage }); await flush();
  const f = fixture(200, new Date(2026, 9, 14, 12), { storage, holdRead: true });
  assert.equal(f.find('stat-xp-summary'), undefined);
  f.releaseRead(); await flush();
  assert.ok(f.find('stat-xp-summary'));
  storage.set('course-academy.study-stats.v1', '{bad json');
  const broken = fixture(200, undefined, { storage, holdRead: true });
  assert.equal(broken.find('stat-xp-summary'), undefined);
  broken.releaseRead(); await flush();
  assert.ok(broken.find('stat-xp-summary'));
});

test('a failed refresh retains same-day XP and storage failures do not prevent fresh reads', async () => {
  const storage = new Map();
  const f = fixture(200, undefined, { storage }); await flush();
  f.failRead = true;
  f.window.dispatchEvent(new Event('pageshow')); await flush();
  assert.equal(f.find('stat-xp-summary').children[0].children[1].textContent, '250');
  assert.match(f.sidebar.title, /refresh unavailable/);
  const unavailable = { get() { throw new Error('Storage blocked'); }, set() { throw new Error('Storage blocked'); } };
  const fresh = fixture(200, undefined, { storage: unavailable }); await flush();
  assert.ok(fresh.find('stat-xp-summary'));
});

test('the XP row shows today, week, and compact lifetime totals with exact details', async () => {
  const f = fixture(); await flush();
  const metrics = f.find('stat-xp-summary').children;
  assert.deepEqual(metrics.map(metric => metric.children[0].textContent), ['Today', 'This week', 'Total']);
  assert.deepEqual(metrics.map(metric => metric.children[1].textContent), ['250', '250', '12.4k']);
  const total = metrics[2].children[1].children[0];
  assert.equal(total.getAttribute('aria-label'), 'Total: 12,400 XP');
  total.dispatchEvent(new Event('click'));
  assert.equal(f.find('stat-xp-details').hidden, false);
  assert.equal(f.find('stat-xp-details').textContent, 'Total: 12,400 XP');
  assert.equal(f.find('stat-progress'), undefined);
  assert.match(f.sidebar.textContent, /Daily goal reached/);
  assert.match(f.sidebar.textContent, /10 min working time/);
  const chart = f.find('stat-week-chart'); assert.equal(chart.children.length, 7);
  chart.children[2].dispatchEvent(new Event('click'));
  assert.equal(chart.children[2].getAttribute('aria-pressed'), 'true');
  assert.equal(f.calls.length, 1); // Chart details need no extra request.
  assert.match(f.calls[0].path, /^\/api\/study-stats\?/);
  assert.equal(f.forecastRequests[0].basis, 1);
  assert.equal(f.forecastRequests[0].dailyXpGoal, 200);
});

test('Activities follows estimated completion and uses the XP card layout with exact completion totals', async () => {
  const f = fixture(); await flush();
  const card = f.find('stat-activities');
  assert.equal(f.sidebar.children.indexOf(card), f.sidebar.children.indexOf(f.forecastCard) + 1);
  assert.equal(card.children[0].textContent, 'Activities');
  const metrics = f.find('stat-xp-summary', card).children;
  assert.deepEqual(metrics.map(metric => metric.children[0].textContent), ['Lessons', 'KPs', 'Reviews']);
  assert.deepEqual(metrics.map(metric => metric.children[1].textContent), ['27', '54', '13']);
  metrics[1].children[1].children[0].dispatchEvent(new Event('click'));
  assert.equal(f.find('stat-xp-details', card).textContent, '54 distinct knowledge points in completed lessons');
  assert.equal(f.calls.length, 1);
});

test('the sidebar only displays statistics and has no goal editor or activity link', async () => {
  const f = fixture(null); await flush();
  assert.equal(f.find('stat-xp-summary').children[0].children[1].textContent, '250');
  assert.equal(f.find('stat-goal-reached'), undefined);
  assert.equal(f.find('stat-progress'), undefined);
  assert.equal(f.find('stat-goal-form'), undefined);
  assert.equal(f.find('stat-history-link'), undefined);
  const all = node => [node, ...node.children.flatMap(all)];
  assert.equal(all(f.sidebar).some(node => ['form', 'input', 'a'].includes(node.tagName)), false);
  assert.equal(f.calls.filter(call => call.body).length, 0);
});

test('daily bars use the goal scale instead of the highest earning day', async () => {
  for (const goal of [null, 200, 100]) {
    const f = fixture(goal);
    const scale = goal || 200;
    f.data.days.forEach((day, i) => { day.earnedXp = [scale * 2, 0, 0, 0, 0, scale / 2, scale][i]; });
    await flush();
    const chart = f.find('stat-week-chart');
    const fills = chart.children.map(bar => f.find('stat-day-fill', bar));
    assert.deepEqual(fills.map(fill => fill.style.height), ['0%', '50%', '100%', '100%', '0%', '0%', '0%']);
    assert.match(chart.getAttribute('aria-label'), new RegExp(`out of ${scale} XP per day`));
    assert.match(chart.children[3].title, new RegExp(`${scale * 2} / ${scale} XP.*goal reached`));
    assert.equal(chart.children[3].dataset.goalReached, 'true');
  }
});

test('negative daily XP stays below zero while positive bars remain capped at the goal', async () => {
  const f = fixture();
  f.data.days[4].earnedXp = -50;
  f.data.days[5].earnedXp = 100;
  await flush();
  const bars = f.find('stat-week-chart').children;
  const negative = f.find('stat-day-fill', bars[0]);
  assert.equal(negative.dataset.negative, 'true');
  assert.equal(negative.style.top, '80%');
  assert.equal(negative.style.height, '20%');
  assert.equal(f.find('stat-day-fill', bars[1]).style.height, '40%');
  assert.equal(f.find('stat-day-fill', bars[2]).style.height, '80%');
});

test('fixed weekdays retain last week until their own day, without changing the weekly total or markup', async () => {
  for (let weekday = 0; weekday < 7; weekday++) {
    const at = new Date(2026, 9, 12 + weekday, 12);
    const f = fixture(200, at);
    f.data.days.forEach((day, i) => { day.earnedXp = i === 6 ? 0 : (i + 1) * 10; });
    await flush();
    const starts = f.calls[0].path.split('dayStarts=')[1].split(',').map(Number);
    const bars = f.find('stat-week-chart').children;
    assert.deepEqual(bars.map(bar => f.find('stat-day-label', bar).textContent), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']);
    bars.forEach((bar, slot) => {
      const date = new Date(at); date.setDate(date.getDate() - (weekday - slot + 7) % 7);
      const source = starts.indexOf(new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime());
      assert.ok(source >= 0);
      const xp = source === 6 ? 0 : (source + 1) * 10;
      assert.match(bar.title, new RegExp(`: ${xp} / 200 XP`));
      assert.ok(bar.title.startsWith(new Intl.DateTimeFormat(undefined, { weekday: 'long', month: 'short', day: 'numeric' }).format(date)));
      assert.equal(bar.children.length, 2);
      assert.equal(bar.getAttribute('aria-current'), slot === weekday ? 'date' : undefined);
      assert.equal(bar.dataset.future, String(slot > weekday));
    });
    const metrics = f.find('stat-xp-summary').children;
    assert.deepEqual(metrics.map(metric => metric.children[0].textContent), ['Today', 'This week', 'Total']);
    assert.equal(metrics[0].children[1].textContent, '0');
    assert.equal(metrics[1].children[1].textContent, String(f.data.days.slice(6 - weekday).reduce((sum, day) => sum + day.earnedXp, 0)));
    assert.equal(f.find('stat-day-marker'), undefined);
    assert.equal(f.find('stat-day-date'), undefined);
  }
});

test('Sunday to Monday resets only Monday and refreshes an open sidebar at midnight', async () => {
  const f = fixture(200, new Date(2026, 9, 18, 23, 59)); await flush();
  const timer = [...f.timers.values()][0];
  assert.equal(timer.delay, 60_050);
  f.setNow(new Date(2026, 9, 19, 0, 0, 1));
  f.data.days.forEach((day, i) => { day.earnedXp = i === 6 ? 0 : 120; });
  timer.callback(); await flush();
  const bars = f.find('stat-week-chart').children;
  assert.equal(bars[0].getAttribute('aria-current'), 'date');
  assert.match(bars[0].title, /Monday, Oct 19: 0 \/ 200 XP/);
  assert.match(bars[6].title, /Sunday, Oct 18: 120 \/ 200 XP/);
  assert.equal(f.find('stat-xp-summary').children[1].children[1].textContent, '0');
  assert.equal(f.calls.length, 2);
  assert.equal(f.timers.size, 1);
  assert.equal(f.forecastRefreshes, 2);
});

test('saving the goal updates forecast dates immediately and sidebar replacement disposes its reads', async () => {
  const f = fixture(); await flush();
  assert.equal(f.forecastRefreshes, 1);
  const event = new Event('course-academy:daily-xp-goal-changed'); event.detail = { dailyXpGoal: 400 };
  f.window.dispatchEvent(event); await flush();
  assert.deepEqual(f.goals, [400]);
  assert.equal(f.forecastRefreshes, 1);
  const previous = f.forecastSignal;
  f.api.createStudySidebar();
  assert.equal(previous.aborted, true);
});

test('graph view toggles do not affect the independent forecast', async () => {
  const f = fixture(); await flush();
  for (const key of ['course-academy.graph-target-courses', 'course-academy.graph-target-queue', 'course-academy.graph-target-weeks']) {
    const event = new Event('storage'); event.key = key;
    f.window.dispatchEvent(event);
  }
  await flush();
  assert.equal(f.forecastRefreshes, 1);
  assert.equal(f.calls.length, 1);
});
