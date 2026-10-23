import assert from 'node:assert/strict';
import test from 'node:test';
import { ForecastFacts, forecastGraph, knownPreparationTopics, calculateForecast, completionEstimate,
  forecastDayStarts, readForecast, withForecastGoal, courseCompletionEstimates } from '../ui/forecast.js';
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

test('course dates split both pace budgets three ways and use only each course workload and growth', () => {
  const result = calculateForecast(fixture().inputs());
  result.pace.baseXpPerDay = 150;
  result.pace.goalBaseXpPerDay = 300;
  result.courses = [
    { code: '255', remainingTopics: 10, initialWorkBaseXp: 100, dailyDemandBaseXp: 10 },
    { code: '256', remainingTopics: 20, initialWorkBaseXp: 200, dailyDemandBaseXp: 20 },
    { code: '341', remainingTopics: 30, initialWorkBaseXp: 300, dailyDemandBaseXp: 60 },
  ];
  const before = structuredClone(result), courses = courseCompletionEstimates(result);
  assert.deepEqual(result, before);
  close(courses[0].currentPace.days, 100 / (50 - 10));
  close(courses[1].currentPace.days, 200 / (50 - 20));
  assert.equal(courses[2].currentPace.status, 'not-catching-up');
  close(courses[0].goalPace.days, 100 / (100 - 10));
  close(courses[1].goalPace.days, 200 / (100 - 20));
  close(courses[2].goalPace.days, 300 / (100 - 60));
  close(courses.reduce((sum, course) => sum + course.currentPace.baseXpPerDay, 0), 150);
  close(courses.reduce((sum, course) => sum + course.goalPace.baseXpPerDay, 0), 300);
});

test('course dates respond to saved goal conversion and isolate complete or unknown-cost tracks', () => {
  const original = calculateForecast(fixture().inputs());
  const higher = withForecastGoal(original, 400);
  const courses = courseCompletionEstimates(higher);
  for (const course of courses) close(course.goalPace.baseXpPerDay, 400 / original.pace.earnedToBaseFactor / 3);
  higher.courses[0] = { ...higher.courses[0], remainingTopics: 0, initialWorkBaseXp: null, dailyDemandBaseXp: null };
  higher.courses[1] = { ...higher.courses[1], remainingTopics: 1, initialWorkBaseXp: null };
  const changed = courseCompletionEstimates(higher);
  assert.equal(changed[0].currentPace.status, 'complete');
  assert.equal(changed[0].goalPace.status, 'complete');
  assert.equal(changed[1].currentPace.status, 'unavailable');
  assert.equal(changed[1].goalPace.status, 'unavailable');
  assert.deepEqual(changed[2], courses[2]);
});

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
  assert.equal(result.inventory.remainingLessonBaseXp, 30); // Failed attempt's frozen 20 + unstarted 10.
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

test('growth uses October 4 onward, with 28-day exponential weights and zero-growth days', () => {
  const inputs = fixture().inputs();
  addAssignment(inputs, 0, 6000, 133, new Date(2026, 8, 30, 23).getTime());
  addAssignment(inputs, 1, 6100, 135, at(10));
  const result = calculateForecast(inputs);
  assert.equal(result.growth.total.topics, 2);
  assert.equal(result.growth.total.baseXp, 30);
  assert.equal(result.growth.observedDays, 17);
  assert.equal(result.growth.windowStart, '2026-10-04');
  assert.equal(result.growth.halfLifeDays, 28);
  const weights = Array.from({ length: 17 }, (_, age) => 2 ** (-age / 28)).reduce((a, b) => a + b, 0);
  close(result.growth.weightSum, weights);
  close(result.growth.total.baseXpPerDay, 30 * 2 ** (-11 / 28) / weights);
  close(result.growth.total.unweightedBaseXpPerDay, 30 / 17);
  close(result.growth.total.baseXpPerWeek, 7 * result.growth.total.baseXpPerDay);
  assert.equal(result.growth.total.categories.target.topics, 1);
  assert.equal(result.growth.total.categories.prerequisite.topics, 1);
  assert.equal(result.growth.total.categories.queue.topics, 0);
});

test('native numeric transaction instants produce the same historical growth as ISO dates', () => {
  const inputs = fixture().inputs();
  addAssignment(inputs, 0, 6000, 133, at(5));
  addAssignment(inputs, 1, 6100, 135, at(10));
  const original = calculateForecast(inputs);
  for (const event of inputs.history) event.at = Date.parse(event.at);
  assert.deepEqual(calculateForecast(inputs).growth, original.growth);
});

test('scenario workload balances capacity and goal previews reuse measurements without altering the original', () => {
  const result = calculateForecast(fixture().inputs());
  close(result.goalPace.workload.totalBaseXp, result.goalPace.baseXpPerDay * result.goalPace.days);
  assert.ok(result.goalPace.workload.estimatedReviews > 0);
  assert.ok(result.goalPace.workload.estimatedQuizzes > 0);
  const preview = withForecastGoal(result, 300);
  assert.equal(preview.inventory, result.inventory);
  assert.equal(preview.growth, result.growth);
  assert.equal(preview.currentPace, result.currentPace);
  assert.ok(preview.goalPace.days < result.goalPace.days);
  assert.equal(result.pace.dailyEarnedXpGoal, 140);
});

test('queue/target overlap and prerequisite promotion add no work; course transfers do not create arrivals', () => {
  const x = fixture();
  x.event(19, [[1, 'learner/queue', 135, true], [1, 'learner/targets', 134, true]]);
  x.event(20, [[6, 'module/topics', 135, false], [8, 'module/topics', 135, true]]);
  const inputs = x.inputs();
  addAssignment(inputs, 0, 6000, 133, new Date(2026, 8, 30, 23).getTime());
  addAssignment(inputs, 1, 6100, 135, at(10), 4);
  const result = calculateForecast(inputs);
  assert.equal(result.growth.total.topics, 2);
  assert.equal(result.growth.total.baseXp, 30);
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

test('saved attempts take precedence over catalog prices; conflicting active attempts remain outstanding', () => {
  const x = fixture();
  x.event(19, [[1, 'learner/activity', 4000, true], ...changesFor(4000, {
    'learner-task/activity': 1135, 'learner-task/status': 23, 'learner-task/xp-base': 37,
  })]);
  assert.equal(calculateForecast(x.inputs()).inventory.remainingLessonBaseXp, 57);
  x.event(20, [[1134, 'activity/expected-seconds', 600, false]]);
  assert.equal(calculateForecast(x.inputs()).inventory.remainingLessonBaseXp, 57);
  x.event(20, [[1, 'learner/activity', 4001, true], ...changesFor(4001, {
    'learner-task/activity': 1135, 'learner-task/status': 23, 'learner-task/xp-base': 31,
  })]);
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

test('self-directed forecasts count unlearned scoped ancestors after downstream learning', () => {
  const x = fixture({ tasks: false });
  x.event(19, [[1, 'learner/self-directed', true, true],
    [1, 'learner/knowledge-profile', 4000, true], ...changesFor(4000, {
      'progress/topic': 134, 'progress/learned': true,
    })]);
  const known = knownPreparationTopics(x.f, 1);
  assert.deepEqual([...known], [134]);
  const inputs = x.inputs();
  assert.equal(calculateForecast(inputs).inventory.remainingTopics, 4);
  // The native capture's authoritative knownTopics has the same semantics as
  // the local fallback, including when refreshing an already loaded forecast.
  assert.equal(calculateForecast({ ...inputs, knownTopics: [134] }).inventory.remainingTopics, 4);
  x.event(20, [[1, 'learner/self-directed', true, false], [1, 'learner/self-directed', false, true]]);
  assert.equal(calculateForecast(x.inputs()).inventory.remainingTopics, 1);
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

test('growth ignores future changes and uses assignment dates even without retained list history', () => {
  const x = fixture();
  const inputs = x.inputs();
  addAssignment(inputs, 0, 6000, 133, at(5));
  addAssignment(inputs, 1, 6100, 135, at(10));
  inputs.history.push({ t: 100, at: iso(22), changes: [[1, 'learner/targets', 130, true]] });
  const original = calculateForecast(inputs);
  assert.equal(original.growth.total.baseXp, 70);
  inputs.history = [];
  const result = calculateForecast(inputs);
  assert.equal(result.growth.total.baseXp, 70);
  close(result.growth.total.baseXpPerDay, original.growth.total.baseXpPerDay);
  assert.equal(result.growth.reason, null);
});

test('calendar windows use seven completed dates across DST', () => {
  const boundaries = forecastDayStarts(new Date(2026, 10, 3, 12));
  assert.equal(boundaries.length, 8);
  assert.equal(new Date(boundaries[7]).getHours(), 0);
  assert.equal(boundaries[7] - boundaries[0], 7 * 86400000 + 3600000);
});

test('readForecast uses the full database scope regardless of saved graph course, Queue and week toggles', async () => {
  const original = globalThis.fetch;
  const storage = Object.getOwnPropertyDescriptor(globalThis, 'localStorage');
  let storageReads = 0;
  const prefs = new Map([['course-academy.graph-target-courses', '[]'],
    ['course-academy.graph-target-queue', 'false'], ['course-academy.graph-target-weeks', '{"kind":"unscheduled"}']]);
  Object.defineProperty(globalThis, 'localStorage', { configurable: true, value: {
    getItem(key) { storageReads++; return prefs.get(key); },
  } });
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
    assert.deepEqual(result.scope.courses, ['255', '256', '341']);
    assert.equal(result.scope.includeQueue, true);
    assert.deepEqual(result.scope.weekSelection, { kind: 'all' });
    assert.equal(storageReads, 0);
    assert.ok(result.currentPace);
    assert.ok(result.goalPace);
  } finally {
    globalThis.fetch = original;
    if (storage) Object.defineProperty(globalThis, 'localStorage', storage);
    else delete globalThis.localStorage;
  }
});

// Model an assignment imported together with its target. The original due date
// can precede import; the course history must retain that academic date.
function addAssignment(inputs, index, id, topic, due, course = 2) {
  inputs.history[index].changes.push([1, 'learner/assignments', id, true], ...changesFor(id, {
    'activity/id': `assignment-${id}`, 'activity/type': 14, 'activity/course': course,
    'activity/due': { $instant: due }, 'activity/steps': [id + 1],
  }), ...changesFor(id + 1, { 'step/content': id + 2 }),
  ...changesFor(id + 2, { 'assigned-problem/topic-coverage': [topic] }));
  const facts = new ForecastFacts({}, enums);
  for (const event of inputs.history) facts.apply(event.changes);
  inputs.records = recordsOf(facts);
}

function scheduledFixture(pastDue = new Date(2026, 8, 20, 23).getTime()) {
  const inputs = fixture().inputs();
  // Keep the historical successful lesson, but on a topic outside today's
  // unfinished assignment. It must not erase the current preparation backlog.
  inputs.history[2].changes.find(([id, a]) => id === 3000 && a === 'learner-task/activity')[2] = 1130;
  inputs.history[0].changes.find(([id, a]) => id === 2000 && a === 'activity/scope')[2] = 130;
  addAssignment(inputs, 0, 6000, 133, pastDue);
  addAssignment(inputs, 1, 6100, 135, at(22, 23));
  return inputs;
}

test('catch-up starts with work due today, not every preloaded future assignment', () => {
  const r = calculateForecast(scheduledFixture());
  assert.equal(r.inventory.selectedTopics, 5); // Same full viewer scope.
  assert.equal(r.inventory.remainingTopics, 3); // Past-due root and depth-two ancestry.
  assert.equal(r.inventory.remainingLessonBaseXp, 30);
  assert.equal(r.inventory.futureRemainingTopics, 2);
  assert.equal(r.inventory.futureLessonBaseXp, 30); // Saved failed attempt 20, plus 10.
});

test('future OHW prices and later deadlines do not alter the extrapolated catch-up estimate', () => {
  const inputs = scheduledFixture(), original = calculateForecast(inputs);
  inputs.records[1135]['activity/expected-seconds'] = [60000];
  for (const event of inputs.history) for (const change of event.changes) {
    if (change[0] === 6100 && change[1] === 'activity/due') change[2] = { $instant: new Date(2026, 11, 20, 23).getTime() };
  }
  inputs.records[6100]['activity/due'] = [{ $instant: new Date(2026, 11, 20, 23).getTime() }];
  const updated = calculateForecast(inputs);
  assert.equal(updated.inventory.remainingLessonBaseXp, original.inventory.remainingLessonBaseXp);
  assert.equal(updated.growth.total.baseXp, original.growth.total.baseXp);
  close(updated.growth.total.baseXpPerDay, original.growth.total.baseXpPerDay);
  assert.deepEqual(updated.goalPace, original.goalPace);
  assert.deepEqual(updated.currentPace, original.currentPace);
  assert.ok(updated.inventory.futureLessonBaseXp > original.inventory.futureLessonBaseXp);
});

test('pre-window assignments remain backlog and prevent their prerequisites being counted again later', () => {
  const inputs = scheduledFixture();
  addAssignment(inputs, 1, 6200, 133, at(10));
  const r = calculateForecast(inputs);
  assert.equal(r.growth.observedFrom, new Date(2026, 9, 4, 0).toISOString());
  assert.equal(r.growth.observedDays, 17);
  assert.equal(r.growth.total.baseXp, 0);
  assert.equal(r.growth.total.topics, 0);
  assert.equal(r.inventory.remainingLessonBaseXp, 30);
  close(r.courses.reduce((sum, c) => sum + c.growth.baseXpPerDay, 0), r.growth.total.baseXpPerDay);
});

test('the cutoff is the exact local due date, including today, without a current-week approximation', () => {
  const inputs = scheduledFixture();
  for (const event of inputs.history) for (const change of event.changes) {
    if (change[0] === 6000 && change[1] === 'activity/due') change[2] = { $instant: at(21, 23) };
  }
  inputs.records[6000]['activity/due'] = [{ $instant: at(21, 23) }];
  const r = calculateForecast(inputs);
  assert.equal(r.inventory.dueThrough, '2026-10-21');
  assert.equal(r.inventory.remainingLessonBaseXp, 30); // Today at 11 PM is included.
  assert.equal(r.inventory.futureLessonBaseXp, 30); // Tomorrow, in the same week, is excluded.
});

test('already caught up today stays caught up even with assignments tomorrow', () => {
  const inputs = fixture().inputs();
  addAssignment(inputs, 0, 6000, 133, at(20, 23));
  addAssignment(inputs, 1, 6100, 135, at(22, 23));
  const r = calculateForecast(inputs);
  assert.equal(r.inventory.remainingTopics, 0);
  assert.equal(r.inventory.futureRemainingTopics, 2);
  assert.equal(r.currentPace.status, 'complete');
  assert.equal(r.goalPace.status, 'complete');
  assert.equal(r.currentPace.days, 0);
});

test('historical coursework is counted if learned after it became due, but not if already known before', () => {
  const after = fixture().inputs();
  addAssignment(after, 0, 6000, 133, at(5));
  addAssignment(after, 1, 6100, 135, at(22));
  assert.equal(calculateForecast(after).growth.total.baseXp, 40); // Saved completed base 20 + two lessons at 10.
  const before = fixture().inputs();
  addAssignment(before, 0, 6000, 133, at(20));
  addAssignment(before, 1, 6100, 135, at(22));
  assert.equal(calculateForecast(before).growth.total.baseXp, 0);
});

test('Queue remains current when its topic supports an assignment due in the future', () => {
  const inputs = scheduledFixture();
  inputs.history.push({ t: 4, at: iso(19), changes: [[1, 'learner/queue', 135, true]] });
  inputs.records[1]['learner/queue'] = [135];
  const r = calculateForecast(inputs);
  assert.equal(r.inventory.remainingTopics, 5);
  assert.equal(r.inventory.futureRemainingTopics, 0);
  assert.equal(r.inventory.remainingLessonBaseXp, 60);
});

test('incomplete old lesson content uses a labeled median estimate in historical growth', () => {
  const inputs = scheduledFixture(at(5));
  // Topic 131 was required historically, but its successful review satisfies it
  // today. Its missing old price must not invalidate the priced current backlog.
  inputs.history[0].changes.find(([id, a]) => id === 2000 && a === 'activity/scope')[2] = 131;
  inputs.records[2000]['activity/scope'] = [131];
  delete inputs.records[1131]['activity/expected-seconds'];
  const r = calculateForecast(inputs, { dailyXpGoal: 500 });
  assert.equal(r.inventory.unknownCosts.length, 0);
  assert.equal(r.growth.total.unknownCosts, 0);
  assert.equal(r.growth.total.isLowerBound, false);
  assert.equal(r.growth.total.estimatedTopics[0].topicId, 131);
  assert.equal(r.growth.total.estimatedTopics[0].baseXp, 10);
  assert.equal(r.growth.total.estimatedTopics[0].source, 'lesson-median');
  close(r.growth.total.unweightedBaseXpPerDay, 30 / 17);
  assert.equal(r.goalPace.status, 'estimated');
  assert.equal(r.goalPace.optimistic, false);
  assert.equal(r.goalPace.usesFallbackEstimates, true);
  assert.match(r.warnings.join(' '), /1 lesson uses fallback XP estimates/);
});

test('fallback matches KP count before using the global median, without changing source prices or pace', () => {
  const x = fixture();
  x.event(19, [
    ...changesFor(130, { 'topic/knowledge-points': [500, 501, 502] }),
    ...changesFor(132, { 'topic/knowledge-points': [503, 504, 505] }),
    ...changesFor(135, { 'topic/knowledge-points': [506, 507, 508] }),
    [1130, 'activity/expected-seconds', 600, false], [1130, 'activity/expected-seconds', 720, true],
    [1132, 'activity/expected-seconds', 600, false], [1132, 'activity/expected-seconds', 1080, true],
    [1135, 'activity/expected-seconds', 600, false],
  ]);
  const inputs = x.inputs();
  inputs.lessonBases[1135] = { baseXp: null, reason: 'answer fields required' };
  const before = structuredClone(inputs), r = calculateForecast(inputs);
  const estimate = r.inventory.estimatedTopics.find(item => item.topicId === 135);
  assert.equal(estimate.baseXp, 15); // Median of 12 and 18; global median is 10.
  assert.equal(estimate.source, 'kp-count-median');
  assert.equal(estimate.sampleSize, 2);
  assert.equal(estimate.reason, 'answer fields required');
  assert.equal(r.inventory.remainingLessonBaseXp, 35);
  assert.equal(r.pace.baseXp, 60);
  assert.deepEqual(inputs, before);
});

test('a usable content estimate wins over the median and is not labeled as fallback', () => {
  const x = fixture(); x.event(19, [[1135, 'activity/expected-seconds', 600, false]]);
  const inputs = x.inputs(); inputs.lessonBases[1135] = { baseXp: 23 };
  const r = calculateForecast(inputs);
  assert.equal(r.inventory.remainingLessonBaseXp, 43);
  assert.deepEqual(r.inventory.estimatedTopics, []);
});

test('already learned prerequisites add zero growth, before applying missing-price fallback', () => {
  const x = fixture({ tasks: false });
  x.event(10, [[1, 'learner/knowledge-profile', 4000, true], ...changesFor(4000, {
    'progress/topic': 134, 'progress/learned': true,
  }), [1134, 'activity/expected-seconds', 600, false]]);
  const inputs = x.inputs();
  addAssignment(inputs, 0, 6000, 133, new Date(2026, 8, 30, 23).getTime());
  addAssignment(inputs, 1, 6100, 135, at(11));
  const r = calculateForecast(inputs);
  assert.equal(r.growth.total.topics, 1); // Only root 135; prerequisite 134 is already known at entry.
  assert.equal(r.growth.total.baseXp, 10);
  assert.deepEqual(r.growth.total.estimatedTopics, []);
  assert.deepEqual(r.growth.total.unknownTopics, []);
});

test('self-directed growth does not infer earlier learning for an unlearned ancestor', () => {
  const x = fixture({ tasks: false });
  x.event(10, [[1, 'learner/self-directed', true, true],
    [1, 'learner/knowledge-profile', 4000, true], ...changesFor(4000, {
      'progress/topic': 134, 'progress/learned': true,
    })]);
  const inputs = x.inputs();
  addAssignment(inputs, 0, 6000, 133, at(20));
  addAssignment(inputs, 1, 6100, 135, at(22));
  const r = calculateForecast(inputs);
  assert.equal(r.growth.total.topics, 3); // Root 133 and its two unlearned prerequisites.
  assert.equal(r.growth.total.baseXp, 30);
});

test('a target already learned when due contributes no growth, including at the same timestamp', () => {
  const x = fixture({ tasks: false });
  x.event(10, [[1, 'learner/knowledge-profile', 4000, true], ...changesFor(4000, {
    'progress/topic': 135, 'progress/learned': true,
  }), [1135, 'activity/expected-seconds', 600, false]]);
  const inputs = x.inputs();
  inputs.history.at(-1).at = iso(10, 0);
  addAssignment(inputs, 0, 6000, 133, new Date(2026, 8, 30, 23).getTime());
  addAssignment(inputs, 1, 6100, 135, at(10));
  const r = calculateForecast(inputs);
  assert.equal(r.growth.total.topics, 0);
  assert.equal(r.growth.total.baseXp, 0);
  assert.deepEqual(r.growth.total.estimatedTopics, []);
  assert.equal(r.inventory.remainingTopics, 0);
});

test('without any reliable peer prices the forecast reports unknown costs rather than inventing a median', () => {
  const x = fixture({ tasks: false });
  const inputs = x.inputs();
  addAssignment(inputs, 0, 6000, 133, new Date(2026, 8, 30, 23).getTime());
  addAssignment(inputs, 1, 6100, 135, at(10));
  for (const record of Object.values(inputs.records)) delete record['activity/expected-seconds'];
  for (const event of inputs.history) event.changes = event.changes.filter(([, attr]) => attr !== 'activity/expected-seconds');
  const r = calculateForecast(inputs);
  assert.equal(r.inventory.unknownCosts.length, 5);
  assert.deepEqual(r.inventory.estimatedTopics, []);
  assert.equal(r.growth.total.unknownCosts, 2);
  assert.equal(r.growth.total.isLowerBound, true);
  assert.equal(r.currentPace.status, 'unavailable');
});

test('twenty-eight civil days halves an addition weight across DST', () => {
  const inputs = fixture({ tasks: false }).inputs();
  addAssignment(inputs, 0, 6000, 133, at(21));
  addAssignment(inputs, 1, 6100, 135, new Date(2026, 11, 1).getTime());
  const original = calculateForecast(inputs);
  assert.equal(original.growth.total.baseXp, 30);
  close(original.growth.total.weightedBaseXp, 30);
  inputs.capturedAt = new Date(2026, 10, 18, 12).toISOString();
  const later = calculateForecast(inputs);
  assert.equal(later.growth.total.baseXp, 30);
  close(later.growth.total.weightedBaseXp, 15);
});

test('clock time within today does not change the daily growth rate', () => {
  const inputs = scheduledFixture(at(5));
  inputs.capturedAt = iso(21, 1);
  const morning = calculateForecast(inputs).growth;
  inputs.capturedAt = iso(21, 23);
  const evening = calculateForecast(inputs).growth;
  close(morning.total.baseXpPerDay, evening.total.baseXpPerDay);
  assert.equal(morning.observedDays, evening.observedDays);
});

test('a growth window without elapsed days does not invent a rate', () => {
  const inputs = fixture({ tasks: false }).inputs();
  inputs.capturedAt = iso(4);
  inputs.timing.days = forecastDayStarts(new Date(inputs.capturedAt)).slice(0, 7)
    .map(start => ({ start, workingSeconds: 0 }));
  const r = calculateForecast(inputs);
  assert.equal(r.growth.observedDays, 0);
  assert.equal(r.growth.weightSum, 0);
  assert.equal(r.growth.total.baseXpPerDay, null);
  assert.match(r.growth.reason, /No elapsed days/);
});
