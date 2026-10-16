import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = (await readFile(new URL('../ui/study-stats.js', import.meta.url), 'utf8')).replace(/^import .*;\n/gm, '').replaceAll('export ', '');
const flush = () => new Promise(resolve => setImmediate(resolve));
function fixture(goal = 200) {
  const f = { calls: [], data: null };
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
  const now = new Date(2026, 9, 14, 12).getTime();
  const context = vm.createContext({ document, window: new EventTarget(), Intl, Number, AbortController, crypto,
    Date: class extends Date { constructor(...args) { super(...(args.length ? args : [now])); } static now() { return now; } },
    localStorage: { setItem() {} },
    readRequest: async path => {
      f.calls.push({ path });
      if (f.failRead) throw new Error('Offline');
      const days = Array.from({ length: 7 }, (_, i) => ({ earnedXp: i === 2 ? 250 : 0, workingSeconds: i === 2 ? 600 : 0 }));
      f.data ||= { dailyXpGoal: goal, days, earnedXp: 250, totalEarnedXp: 12400, totalXpMissing: 0 };
      return { ok: true, json: async () => structuredClone(f.data) };
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
    f.data.days.forEach((day, i) => { day.earnedXp = [0, scale / 2, scale, scale * 2, 0, 0, 0][i]; });
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
  f.data.days[0].earnedXp = -50;
  f.data.days[1].earnedXp = 100;
  await flush();
  const bars = f.find('stat-week-chart').children;
  const negative = f.find('stat-day-fill', bars[0]);
  assert.equal(negative.dataset.negative, 'true');
  assert.equal(negative.style.top, '80%');
  assert.equal(negative.style.height, '20%');
  assert.equal(f.find('stat-day-fill', bars[1]).style.height, '40%');
  assert.equal(f.find('stat-day-fill', bars[2]).style.height, '80%');
});
