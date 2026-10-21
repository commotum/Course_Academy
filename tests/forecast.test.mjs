import assert from 'node:assert/strict';
import test from 'node:test';
import { ForecastFacts, forecastGraph, knownPreparationTopics, calculateForecast, completionEstimate,
  forecastDayStarts, savedForecastScope, readForecast } from '../ui/forecast.js';
import { projectTargetScope } from '../ui/target-scope.js';

process.env.TZ = 'America/Los_Angeles';
const at = (day, hour = 12) => new Date(2026, 9, day, hour).getTime();
const iso = (day, hour = 12) => new Date(at(day, hour)).toISOString();
const enums = { 11: 'activity.type/lesson', 12: 'activity.type/review', 13: 'activity.type/assessment',
  14: 'activity.type/assignment', 21: 'learner-task.status/completed', 22: 'learner-task.status/failed',
  23: 'learner-task.status/paused', 24: 'learner-task.status/started' };
const changesFor = (e, fields) => Object.entries(fields).flatMap(([a, values]) =>
  (Array.isArray(values) ? values : [values]).map(value => [e, a, value, true]));
const recordsOf = facts => Object.fromEntries([...facts.records].map(([id, record]) => [id,
  Object.fromEntries([...record].map(([a, values]) => [a, [...values.values()]]))]));

function fixture({ tasks = true } = {}) {
  const f = new ForecastFacts({}, enums), history = [], finishedAt = {};
  const event = (day, changes) => {
    f.apply(changes); history.push({ t: history.length + 1, at: iso(day), changes });
  };
  const initial = [
    ...changesFor(1, { 'learner/id': 'learner', 'learner/targets': [133], 'learner/daily-xp-goal': 140 }),
    ...changesFor(2, { 'course/id': 'course-255', 'course/code': 'MTH 255', 'course/units': [5] }),
    ...changesFor(3, { 'course/id': 'course-256', 'course/code': 'MTH 256' }),
    ...changesFor(4, { 'course/id': 'course-341', 'course/code': 'MTH 341', 'course/units': [7] }),
    ...changesFor(5, { 'unit/modules': [6] }), ...changesFor(6, { 'module/topics': [133, 134, 135] }),
    ...changesFor(7, { 'unit/modules': [8] }),
  ];
  for (let id = 100; id <= 135; id++) {
    initial.push(...changesFor(id, { 'topic/id': `topic-${id}`, 'topic/title': `Topic ${id}` }));
    if (id < 135) initial.push([id, 'topic/next', id + 1, true]);
    initial.push(...changesFor(1000 + id, { 'activity/id': `lesson-${id}`, 'activity/type': 11,
      'activity/scope': id, 'activity/expected-seconds': 600 }));
  }
  initial.push(...changesFor(2000, { 'activity/id': 'review', 'activity/type': 12, 'activity/scope': 131 }),
    ...changesFor(2001, { 'activity/id': 'quiz', 'activity/type': 13 }),
    ...changesFor(2002, { 'activity/id': 'homework', 'activity/type': 14 }));
  event(1, initial);
  event(10, [[1, 'learner/targets', 135, true]]);
  if (tasks) {
    const changes = [];
    for (const [task, activity, status, base, earned] of [
      [3000, 1133, 21, 20, 25], [3001, 1134, 22, 20, -1],
      [3002, 2000, 21, 5, 7], [3003, 2001, 21, 15, 18],
    ]) {
      changes.push([1, 'learner/activity', task, true], ...changesFor(task, {
        'learner-task/activity': activity, 'learner-task/status': status,
        'learner-task/xp-base': base, 'learner-task/xp-earned': earned, 'learner-task/elapsed-seconds': 600,
      }));
      finishedAt[task] = at(18);
    }
    event(18, changes);
  }
  const starts = forecastDayStarts(new Date(at(21)));
  const inputs = () => ({ basis: history.length, learnerId: 1, capturedAt: iso(21), enums,
    records: recordsOf(f), history: structuredClone(history), lessonBases: {}, finishedAt,
    firstObservedAt: at(1), timing: { days: starts.slice(0, 7).map((start, i) => ({ start, workingSeconds: i === 4 ? 3600 : 0 })) } });
  return { f, event, inputs };
}

function close(actual, expected) { assert.ok(Math.abs(actual - expected) < 1e-8, `${actual} != ${expected}`); }

test('base throughput includes failed lessons, reviews and quizzes; the earned goal is converted by paired totals', () => {
  const x = fixture(), result = calculateForecast(x.inputs());
  assert.equal(result.pace.baseXp, 60);
  assert.equal(result.pace.earnedXp, 49);
  close(result.pace.baseXpPerDay, 60 / 7);
  close(result.pace.earnedToBaseFactor, 49 / 60);
  close(result.pace.goalBaseXpPerDay, 140 / (49 / 60));
  assert.equal(result.overhead.retryFactor, 2);
  close(result.overhead.quizRatio, 15 / 45);
  close(result.overhead.reviewOtherBaseXpPerDay, 5 / 7);
  assert.equal(result.currentPace.status, 'estimated');
  assert.ok(result.goalPace.days < result.currentPace.days);
  assert.equal(result.inventory.selectedTopics, 5);
  assert.equal(result.inventory.remainingTopics, 2);
  assert.equal(result.inventory.remainingLessonBaseXp, 20);
});

test('goal equal to observed earned average gives the same date; adjusting the goal changes only goal pace', () => {
  const inputs = fixture().inputs();
  const a = calculateForecast(inputs, { dailyXpGoal: 49 / 7 });
  close(a.currentPace.days, a.goalPace.days);
  const b = calculateForecast(inputs, { dailyXpGoal: 200 });
  assert.deepEqual(a.currentPace, b.currentPace);
  assert.deepEqual(a.inventory, b.inventory);
  assert.deepEqual(a.growth, b.growth);
  assert.ok(b.goalPace.days < a.goalPace.days);
});

test('historical growth excludes opening inventory and counts the marginal depth-two closure through now', () => {
  const result = calculateForecast(fixture().inputs());
  assert.equal(result.growth.total.topics, 2);
  assert.equal(result.growth.total.baseXp, 20);
  assert.equal(result.growth.observedDays, 20);
  assert.equal(result.growth.total.baseXpPerWeek, 7);
  assert.equal(result.growth.total.categories.target.topics, 1);
  assert.equal(result.growth.total.categories.prerequisite.topics, 1);
  assert.equal(result.growth.total.categories.queue.topics, 0);
});

test('queue/target overlap and prerequisite promotion add no work; course transfers do not create arrivals', () => {
  const x = fixture();
  x.event(19, [[1, 'learner/queue', 135, true], [1, 'learner/targets', 134, true]]);
  x.event(20, [[6, 'module/topics', 135, false], [8, 'module/topics', 135, true]]);
  const result = calculateForecast(x.inputs());
  assert.equal(result.growth.total.topics, 2);
  assert.equal(result.growth.total.baseXp, 20);
  assert.equal(result.inventory.selectedTopics, 5);
  assert.equal(result.courses.find(c => c.code === '341').remainingTopics, 1);
  close(result.courses.reduce((sum, c) => sum + c.initialWorkBaseXp, 0), result.initialWorkBaseXp);
  close(result.courses.reduce((sum, c) => sum + c.dailyDemandBaseXp, 0), result.dailyDemandBaseXp);
});

test('the final graph handles layer cutoff, course filters, Queue independence and unassigned targets', () => {
  const x = fixture({ tasks: false });
  x.event(19, [[1, 'learner/queue', 129, true], [1, 'learner/targets', 120, true], [1, 'learner/queue', 135, true]]);
  const graph = forecastGraph(x.f, 1);
  const selected = projectTargetScope(graph, { courses: [], includeQueue: true });
  assert.ok(selected.nodeIds.has(129)); // L30 is retained.
  assert.ok(!selected.nodeIds.has(128));
  assert.ok(!selected.nodeIds.has(120));
  assert.ok(selected.nodeIds.has(135)); // Queue bypasses course switches.
  assert.equal(projectTargetScope(graph, { courses: [], includeQueue: false }).nodeIds.size, 0);
});

test('a completed queued lesson remains modeled work when completion removes its root in the same transaction', () => {
  const x = fixture({ tasks: false });
  x.event(14, [[1, 'learner/queue', 134, true]]);
  x.event(18, [[1, 'learner/queue', 134, false], [1, 'learner/activity', 3000, true], ...changesFor(3000, {
    'learner-task/activity': 1134, 'learner-task/status': 21, 'learner-task/xp-base': 20,
    'learner-task/xp-earned': 25, 'learner-task/elapsed-seconds': 1200,
  })]);
  const inputs = x.inputs(); inputs.finishedAt[3000] = at(18);
  assert.equal(calculateForecast(inputs).pace.otherBaseXp, 0);
});

test('active lessons use frozen bases, and missing lesson estimates remain outstanding', () => {
  const x = fixture();
  x.event(19, [[1, 'learner/activity', 4000, true], ...changesFor(4000, {
    'learner-task/activity': 1135, 'learner-task/status': 23, 'learner-task/xp-base': 37,
  })]);
  assert.equal(calculateForecast(x.inputs()).inventory.remainingLessonBaseXp, 47);
  x.event(20, [[1134, 'activity/expected-seconds', 600, false]]);
  const result = calculateForecast(x.inputs());
  assert.equal(result.inventory.unknownCosts.length, 1);
  assert.equal(result.inventory.remainingTopics, 2);
  assert.equal(result.currentPace.status, 'unavailable');
});

test('known preparation uses explicit learned, legacy and completed evidence plus prerequisite ancestry', () => {
  const x = fixture({ tasks: false });
  x.event(19, [[1, 'learner/knowledge-profile', 4000, true], ...changesFor(4000, {
    'progress/topic': 134, 'progress/repetitions': .5,
  })]);
  let known = knownPreparationTopics(x.f, 1);
  assert.ok(known.has(134)); assert.ok(known.has(100)); assert.ok(!known.has(135));
  x.event(20, [[4000, 'progress/learned', false, true]]);
  known = knownPreparationTopics(x.f, 1);
  assert.ok(!known.has(134));
});

test('unpriced homework contributes time without suppressing base throughput; undated imports are excluded', () => {
  const x = fixture();
  x.event(19, [[1, 'learner/activity', 4000, true], ...changesFor(4000, {
    'learner-task/activity': 2002, 'learner-task/status': 21, 'learner-task/elapsed-seconds': 1800,
  }), [1, 'learner/activity', 4001, true], ...changesFor(4001, {
    'learner-task/activity': 1135, 'learner-task/status': 21, 'learner-task/xp-base': 9999,
  })]);
  const inputs = x.inputs(); inputs.finishedAt[4000] = at(19);
  const result = calculateForecast(inputs);
  assert.equal(result.pace.baseXp, 60);
  assert.equal(result.pace.unpricedActivities, 1);
  assert.equal(result.pace.undatedAttempts, 1);
  assert.equal(result.pace.missingBases, 0);
});

test('unknown timing suppresses minutes conversion, not XP/day; no goal or nonpositive conversion has no goal date', () => {
  const inputs = fixture().inputs(); inputs.timingUnknownTasks = [3000];
  const result = calculateForecast(inputs);
  assert.equal(result.pace.baseXpPerActiveMinute, null);
  assert.equal(result.currentPace.status, 'estimated');
  for (const task of [3000, 3001, 3002, 3003]) inputs.records[task]['learner-task/xp-earned'] = [-1];
  const negative = calculateForecast(inputs);
  assert.equal(negative.pace.earnedToBaseFactor, null);
  assert.equal(negative.goalPace.status, 'unavailable');
  delete inputs.records[1]['learner/daily-xp-goal'];
  assert.equal(calculateForecast(inputs).goalPace.status, 'unavailable');
});

test('completion handles zero backlog, insufficient capacity and missing values without invented dates', () => {
  assert.equal(completionEstimate(null, null, null, at(21), 0).status, 'complete');
  assert.equal(completionEstimate(100, 10, 10, at(21)).status, 'not-catching-up');
  assert.equal(completionEstimate(100, 10, 0, at(21)).status, 'not-catching-up');
  assert.equal(completionEstimate(100, null, 20, at(21)).status, 'unavailable');
  close(completionEstimate(100, 10, 20, at(21)).days, 10);
});

test('growth never observes future changes and incomplete history is reported', () => {
  const x = fixture();
  const inputs = x.inputs();
  inputs.history.push({ t: 100, at: iso(22), changes: [[1, 'learner/targets', 130, true]] });
  assert.equal(calculateForecast(inputs).growth.total.baseXp, 20);
  inputs.history = [];
  const result = calculateForecast(inputs);
  assert.equal(result.growth.total.baseXpPerDay, null);
  assert.equal(result.currentPace.status, 'unavailable');
  assert.match(result.growth.reason, /opening inventory/);
});

test('calendar windows use seven completed dates across DST and reuse the saved Targets filters', () => {
  const boundaries = forecastDayStarts(new Date(2026, 10, 3, 12));
  assert.equal(boundaries.length, 8);
  assert.equal(new Date(boundaries[7]).getHours(), 0);
  assert.equal(boundaries[7] - boundaries[0], 7 * 86400000 + 3600000);
  const prefs = new Map([['course-academy.graph-target-courses', '["255","341"]'],
    ['course-academy.graph-target-queue', 'false'], ['course-academy.graph-target-weeks', '{"kind":"unscheduled"}']]);
  assert.deepEqual(savedForecastScope({ getItem: key => prefs.get(key) }),
    { courses: ['255', '341'], includeQueue: false, weekSelection: { kind: 'unscheduled' } });
});

test('readForecast calls the read-only input endpoint and returns calculated results without rendering', async () => {
  const original = globalThis.fetch;
  const inputs = fixture().inputs();
  inputs.capturedAt = new Date().toISOString();
  inputs.timing.days = forecastDayStarts().slice(0, 7).map(start => ({ start, workingSeconds: 0 }));
  let requested;
  globalThis.fetch = async (path, options) => {
    requested = { path, options };
    return new Response(JSON.stringify(inputs), { headers: { 'Content-Type': 'application/json' } });
  };
  try {
    const result = await readForecast();
    assert.match(requested.path, /^\/api\/forecast-inputs\?dayStarts=/);
    assert.equal(requested.options.method, undefined);
    assert.equal(result.inventory.selectedTopics, 5);
    assert.ok(result.currentPace);
    assert.ok(result.goalPace);
  } finally { globalThis.fetch = original; }
});
