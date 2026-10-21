// Forecast calculations only; presentation is deliberately left to the caller.
import { readRequest } from './requests.js';
import { projectTargetScope, assignTargetCourses, TARGET_COURSE_CODES } from './target-scope.js';
import { buildTargetCalendar, normalizeTargetWeekSelection, targetCalendarDay } from './target-weeks.js';

const DAY = 86400000;
const positive = n => Number.isFinite(n) && n > 0;
const scalar = v => v?.$uuid ?? v?.$instant ?? v;
const terminal = state => state === 'completed' || state === 'failed';

// All values are arrays, including cardinality-one fields. EDB retraction
// withdraws an E/A/V across sources; repeated assertions are idempotent here.
export class ForecastFacts {
  constructor(records = {}, enums = {}) {
    this.records = new Map(Object.entries(records).map(([e, r]) => [Number(e),
      new Map(Object.entries(r).map(([a, values]) => [a, new Map(values.map(v => [JSON.stringify(v), v]))]))]));
    this.enums = enums;
  }
  values(e, a) { return [...(this.records.get(Number(e))?.get(a)?.values() || [])]; }
  get(e, a) { return scalar(this.values(e, a)[0]); }
  kind(e, a) { return (this.enums[this.get(e, a)] || '').split('/').at(-1); }
  ids(a) { return [...this.records].filter(([, r]) => r.get(a)?.size).map(([e]) => e); }
  apply(changes) {
    // Transaction operations are simultaneous; remove old facts before adding.
    for (const added of [false, true]) for (const [e, a, v, isAdded] of changes) {
      if (isAdded !== added) continue;
      if (!this.records.has(e)) this.records.set(e, new Map());
      const record = this.records.get(e);
      if (!record.has(a)) record.set(a, new Map());
      if (added) record.get(a).set(JSON.stringify(v), v);
      else record.get(a).delete(JSON.stringify(v));
    }
  }
}

export function forecastGraph(f, learner) {
  const ids = new Set(f.ids('topic/id'));
  const targets = f.values(learner, 'learner/targets');
  const schedule = f.values(learner, 'learner/assignments').map(activity => {
    const pending = f.values(activity, 'activity/steps').flatMap(step => f.values(step, 'step/content'));
    const visited = new Set(), topics = new Set();
    for (let i = 0; i < pending.length; i++) {
      const content = pending[i];
      if (visited.has(content)) continue;
      visited.add(content);
      for (const id of f.values(content, 'assigned-problem/topic-coverage')) if (ids.has(id)) topics.add(id);
      pending.push(...f.values(content, 'assigned-problem/content'));
      for (const step of f.values(content, 'multistep/steps')) pending.push(...f.values(step, 'step/content'));
    }
    const course = f.get(activity, 'activity/course');
    return { assignmentId: f.get(activity, 'activity/id'), courseId: f.get(course, 'course/id'),
      due: f.get(activity, 'activity/due') ?? null, topicIds: [...topics] };
  });
  const courses = f.ids('course/id').map(id => {
    const topicIds = new Set(f.values(id, 'course/units').flatMap(unit => f.values(unit, 'unit/modules'))
      .flatMap(module => f.values(module, 'module/topics')).filter(topic => ids.has(topic)));
    const courseId = f.get(id, 'course/id');
    const assigned = new Set(schedule.filter(a => a.courseId === courseId).flatMap(a => a.topicIds));
    return { id: courseId, code: f.get(id, 'course/code'), title: f.get(id, 'course/title'),
      topicIds: [...topicIds], targetTopicIds: targets.filter(topic => assigned.has(topic)) };
  });
  return {
    nodes: [...ids].map(id => ({ id, uuid: f.get(id, 'topic/id'), name: f.get(id, 'topic/title') || `Untitled topic ${id}` })),
    links: [...ids].flatMap(source => f.values(source, 'topic/next').map(target => ({ source, target }))),
    courses, targetSchedule: schedule, learner: { targets, queue: f.values(learner, 'learner/queue') },
  };
}

// Same evidence and prerequisite closure as learning::known_preparation_topics.
// Current coverage comes directly from that engine function; replay needs the
// equivalent calculation over historical facts, without invoking a scheduler.
export function knownPreparationTopics(f, learner) {
  const prerequisites = new Map(f.ids('topic/id').map(id => [id, new Set()]));
  for (const id of prerequisites.keys()) {
    for (const next of f.values(id, 'topic/next')) prerequisites.get(next)?.add(id);
    for (const kp of f.values(id, 'topic/knowledge-points')) {
      for (const previous of f.values(kp, 'knowledge-point/key-prerequisites')) prerequisites.get(id).add(previous);
    }
  }
  const pending = [];
  for (const id of f.values(learner, 'learner/knowledge-profile')) {
    const learned = f.get(id, 'progress/learned'), repetitions = f.get(id, 'progress/repetitions') ?? 0;
    if (!Number.isFinite(repetitions) || repetitions < 0) throw new Error('Invalid imported repetition position.');
    if (learned === true || (learned === undefined && repetitions > 0)) pending.push(f.get(id, 'progress/topic'));
  }
  for (const task of f.values(learner, 'learner/activity')) {
    const activity = f.get(task, 'learner-task/activity');
    if (f.kind(task, 'learner-task/status') === 'completed' && ['lesson', 'review'].includes(f.kind(activity, 'activity/type'))) {
      const topic = f.get(activity, 'activity/scope');
      if (topic !== undefined) pending.push(topic);
    }
  }
  const known = new Set();
  for (let i = 0; i < pending.length; i++) if (!known.has(pending[i])) {
    known.add(pending[i]); pending.push(...(prerequisites.get(pending[i]) || []));
  }
  return known;
}

function topicPrices(f, learner, estimates) {
  const lessons = new Map(), active = new Map();
  for (const id of f.ids('activity/type')) if (f.kind(id, 'activity/type') === 'lesson') {
    const topic = f.get(id, 'activity/scope');
    if (!lessons.has(topic)) lessons.set(topic, []);
    lessons.get(topic).push(id);
  }
  for (const task of f.values(learner, 'learner/activity')) {
    if (terminal(f.kind(task, 'learner-task/status'))) continue;
    const activity = f.get(task, 'learner-task/activity'), base = f.get(task, 'learner-task/xp-base');
    if (f.kind(activity, 'activity/type') === 'lesson' && positive(base)) {
      const topic = f.get(activity, 'activity/scope');
      if (!active.has(topic)) active.set(topic, []);
      active.get(topic).push(base);
    }
  }
  return topic => {
    if (active.get(topic)?.length === 1) return { baseXp: active.get(topic)[0] };
    if (active.get(topic)?.length > 1) return { baseXp: null, reason: 'Multiple unfinished lesson attempts.' };
    const choices = lessons.get(topic) || [];
    if (choices.length !== 1) return { baseXp: null, reason: choices.length ? 'Multiple lesson definitions.' : 'No lesson definition.' };
    const seconds = f.get(choices[0], 'activity/expected-seconds');
    if (seconds !== undefined) return positive(seconds)
      ? { baseXp: Math.max(1, Math.floor(seconds / 60 + .5)) }
      : { baseXp: null, reason: 'Invalid lesson duration.' };
    return estimates[choices[0]] || { baseXp: null, reason: 'No lesson estimate at this historical state.' };
  };
}

const growthFields = new Set(['topic/id', 'topic/title', 'topic/next', 'course/id', 'course/code',
  'course/units', 'unit/modules', 'module/topics', 'learner/targets', 'learner/queue',
  'learner/assignments', 'activity/course', 'activity/due', 'activity/steps',
  'step/content', 'multistep/steps', 'assigned-problem/content', 'assigned-problem/topic-coverage']);
const emptyCategories = () => Object.fromEntries(['target', 'queue', 'prerequisite'].map(key => [key, { topics: 0, baseXp: 0 }]));
const emptyGrowth = () => ({ topics: 0, baseXp: 0, unknownCosts: 0, categories: emptyCategories() });

function calendarExposure(start, end) {
  const position = ms => {
    const parts = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', hourCycle: 'h23',
      hour: 'numeric', minute: 'numeric', second: 'numeric' }).formatToParts(new Date(ms));
    const part = type => Number(parts.find(p => p.type === type).value);
    return targetCalendarDay(ms) + (part('hour') * 3600 + part('minute') * 60 + part('second')) / 86400;
  };
  return Math.max(0, position(end) - position(start));
}

export function historicalGrowth(inputs, options, currentScope, now) {
  const f = new ForecastFacts({}, inputs.enums), learner = inputs.learnerId;
  const courses = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, emptyGrowth()]));
  const total = emptyGrowth(), modeledTasks = new Set();
  let previous = null, observedFrom = null, invalid = null;
  for (const event of inputs.history) {
    const at = Date.parse(event.at);
    if (!Number.isFinite(at) || at > now) continue;
    const completed = event.changes.filter(([, a, v, added]) => added && a === 'learner-task/status'
      && terminal((inputs.enums[v] || '').split('/').at(-1))).map(([task]) => task);
    f.apply(event.changes);
    // Task completion can remove its queue root in the same transaction. Its
    // lesson still belongs to the scope it was in immediately before finishing.
    for (const task of completed) {
      const topic = f.get(f.get(task, 'learner-task/activity'), 'activity/scope');
      if (previous?.nodeIds.has(topic)) modeledTasks.add(task);
    }
    if (!event.changes.some(([, a]) => growthFields.has(a))) continue;
    if (!f.get(learner, 'learner/id') || !f.ids('topic/id').length) continue;
    let scope;
    try { scope = projectTargetScope(forecastGraph(f, learner), options); }
    catch (error) { invalid = error.message; continue; }
    for (const task of completed) if (scope.nodeIds.has(f.get(f.get(task, 'learner-task/activity'), 'activity/scope'))) modeledTasks.add(task);
    if (previous === null) {
      // First nonempty retained scope is opening inventory, not weekly demand.
      if (!scope.nodeIds.size) continue;
      previous = scope; observedFrom = at; continue;
    }
    const known = knownPreparationTopics(f, learner), price = topicPrices(f, learner, inputs.lessonBases);
    for (const topic of scope.nodeIds) {
      if (previous.nodeIds.has(topic) || known.has(topic)) continue;
      const cost = price(topic), course = courses[scope.tracks.get(topic)], category = scope.categories.get(topic);
      for (const item of [total, course]) {
        item.topics++; item.categories[category].topics++;
        if (positive(cost.baseXp)) { item.baseXp += cost.baseXp; item.categories[category].baseXp += cost.baseXp; }
        else item.unknownCosts++;
      }
    }
    previous = scope;
  }
  if (!previous || !observedFrom) invalid ||= 'No reliable opening inventory in retained history.';
  if (previous && (previous.nodeIds.size !== currentScope.nodeIds.size || [...previous.nodeIds].some(id => !currentScope.nodeIds.has(id))
    || [...previous.tracks].some(([id, course]) => currentScope.tracks.get(id) !== course))) {
    invalid = 'Retained history does not reproduce the current filtered graph.';
  }
  const observedDays = observedFrom === null ? 0 : calendarExposure(observedFrom, now);
  const summarize = item => ({ ...item,
    baseXpPerDay: !invalid && observedDays > 0 && !item.unknownCosts ? item.baseXp / observedDays : null,
    baseXpPerWeek: !invalid && observedDays > 0 && !item.unknownCosts ? 7 * item.baseXp / observedDays : null,
    topicsPerWeek: !invalid && observedDays > 0 ? 7 * item.topics / observedDays : null,
    categories: Object.fromEntries(Object.entries(item.categories).map(([key, value]) => [key, { ...value,
      topicsPerWeek: observedDays > 0 && !invalid ? value.topics * 7 / observedDays : null,
      baseXpPerWeek: observedDays > 0 && !invalid && !item.unknownCosts ? value.baseXp * 7 / observedDays : null }])),
  });
  return { observedFrom: observedFrom === null ? null : new Date(observedFrom).toISOString(), observedThrough: new Date(now).toISOString(),
    observedDays, reason: invalid || (observedDays > 0 ? null : 'No elapsed growth observation period.'),
    total: summarize(total), courses: Object.fromEntries(Object.entries(courses).map(([code, value]) => [code, summarize(value)])), modeledTasks };
}

export function completionEstimate(initialWork, dailyDemand, pace, now, remainingTopics = 1) {
  if (remainingTopics === 0) return { status: 'complete', days: 0, date: new Date(now).toISOString(), baseXpPerDay: pace };
  if (![initialWork, dailyDemand, pace].every(n => typeof n === 'number' && Number.isFinite(n)) || initialWork < 0 || pace < 0) {
    return { status: 'unavailable', days: null, date: null, baseXpPerDay: pace };
  }
  if (pace <= dailyDemand) return { status: 'not-catching-up', days: null, date: null, baseXpPerDay: pace };
  const days = initialWork / (pace - dailyDemand), at = now + days * DAY;
  if (!Number.isFinite(at) || Math.abs(at) > 8.64e15) return { status: 'out-of-range', days: null, date: null, baseXpPerDay: pace };
  return { status: 'estimated', days, date: new Date(at).toISOString(), baseXpPerDay: pace };
}

export function calculateForecast(inputs, options = {}) {
  const now = Date.parse(inputs.capturedAt);
  if (!Number.isFinite(now)) throw new Error('Forecast capture date is required.');
  const f = new ForecastFacts(inputs.records, inputs.enums), learner = inputs.learnerId;
  const graph = forecastGraph(f, learner);
  const scopeOptions = { courses: options.courses ?? TARGET_COURSE_CODES, includeQueue: options.includeQueue !== false,
    weekSelection: normalizeTargetWeekSelection(buildTargetCalendar(graph.targetSchedule), options.weekSelection), prerequisiteDepth: 2 };
  if (scopeOptions.courses.some(code => !TARGET_COURSE_CODES.includes(code))) throw new Error('Unknown forecast course.');
  const scope = projectTargetScope(graph, scopeOptions), known = new Set(inputs.knownTopics ?? knownPreparationTopics(f, learner));
  const price = topicPrices(f, learner, inputs.lessonBases);
  const courses = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, { code, selectedTopics: 0, remainingTopics: 0,
    remainingLessonBaseXp: 0, unknownCosts: [], categories: emptyCategories() }]));
  for (const topic of scope.nodeIds) {
    const course = courses[scope.tracks.get(topic)]; course.selectedTopics++;
    if (known.has(topic)) continue;
    const cost = price(topic), category = course.categories[scope.categories.get(topic)];
    course.remainingTopics++; category.topics++;
    if (positive(cost.baseXp)) { course.remainingLessonBaseXp += cost.baseXp; category.baseXp += cost.baseXp; }
    else course.unknownCosts.push({ topicId: topic, reason: cost.reason || 'Unknown lesson cost.' });
  }
  const growth = historicalGrowth(inputs, scopeOptions, scope, now);
  const days = inputs.timing.days, starts = days.map(day => day.start);
  const end = options.windowEnd ?? (() => {
    const date = new Date(starts.at(-1)); date.setDate(date.getDate() + 1); return date.getTime();
  })();
  if (days.length !== 7 || starts.some((at, i) => !Number.isFinite(at) || (i && at <= starts[i - 1])) || end > now) throw new Error('Seven completed local dates are required.');
  const first = inputs.firstObservedAt;
  const firstIndex = starts.findIndex((at, i) => first < (starts[i + 1] ?? end));
  const startIndex = first === null || first === undefined || firstIndex < 0 ? 7 : firstIndex;
  const observed = days.slice(startIndex), d = observed.length;
  const start = starts[startIndex] ?? end;
  const totals = { baseXp: 0, earnedXp: 0, pairedBaseXp: 0, pairedEarnedXp: 0, lessonBaseXp: 0,
    successfulLessonBaseXp: 0, quizBaseXp: 0, nonQuizBaseXp: 0, reviewBaseXp: 0, reviewAttempts: 0,
    otherBaseXp: 0, missingBases: 0, unpricedActivities: 0, undatedAttempts: 0, missingTiming: 0 };
  const attribution = new Map(assignTargetCourses(graph, scope.graph, buildTargetCalendar(graph.targetSchedule), new Set(scope.graph.nodeById.keys()))
    .flatMap(course => [...course.nodeIds].map(topic => [topic, course.key])));
  const overhead = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, 0]));
  const shares = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, 0]));
  let unassignedOverhead = 0, allLessonBase = 0, allSuccessfulBase = 0;
  for (const task of f.values(learner, 'learner/activity')) {
    const state = f.kind(task, 'learner-task/status');
    if (!terminal(state)) continue;
    const at = inputs.finishedAt[task], base = f.get(task, 'learner-task/xp-base');
    const activity = f.get(task, 'learner-task/activity'), kind = f.kind(activity, 'activity/type');
    if (kind === 'lesson' && positive(base) && Number.isFinite(at) && at <= now) {
      allLessonBase += base; if (state === 'completed') allSuccessfulBase += base;
    }
    if (!Number.isFinite(at)) { totals.undatedAttempts++; continue; }
    if (at < start || at >= end) continue;
    const earned = f.get(task, 'learner-task/xp-earned');
    if (Number.isFinite(earned)) totals.earnedXp += earned;
    if (f.get(task, 'learner-task/elapsed-seconds') === undefined || inputs.timingUnknownTasks?.includes(task)) totals.missingTiming++;
    // Assignment completion currently records work without allocating XP.
    // Its time belongs in M, but an absent assignment base is not a broken
    // lesson/quiz estimate and must not suppress every forecast.
    if (!positive(base)) { if (kind === 'assignment') totals.unpricedActivities++; else totals.missingBases++; continue; }
    totals.baseXp += base;
    if (Number.isFinite(earned)) { totals.pairedBaseXp += base; totals.pairedEarnedXp += earned; }
    if (kind === 'lesson') { totals.lessonBaseXp += base; if (state === 'completed') totals.successfulLessonBaseXp += base; }
    if (kind === 'assessment') { totals.quizBaseXp += base; continue; }
    totals.nonQuizBaseXp += base;
    const topic = f.get(activity, 'activity/scope'), course = attribution.get(topic);
    if (course) shares[course] += base;
    let isOverhead = false;
    if (kind === 'review') { totals.reviewBaseXp += base; totals.reviewAttempts++; isOverhead = true; }
    else if (kind !== 'lesson' || !(growth.modeledTasks.has(task) || scope.nodeIds.has(topic))) { totals.otherBaseXp += base; isOverhead = true; }
    if (isOverhead) { if (course) overhead[course] += base; else unassignedOverhead += base; }
  }
  const workingMinutes = observed.reduce((sum, day) => sum + day.workingSeconds / 60, 0);
  const retry = positive(totals.successfulLessonBaseXp) ? totals.lessonBaseXp / totals.successfulLessonBaseXp
    : positive(allSuccessfulBase) ? allLessonBase / allSuccessfulBase : null;
  const quizRatio = positive(totals.nonQuizBaseXp) ? totals.quizBaseXp / totals.nonQuizBaseXp : .1;
  const conversion = positive(totals.pairedBaseXp) && positive(totals.pairedEarnedXp) ? totals.pairedEarnedXp / totals.pairedBaseXp : null;
  const goal = options.dailyXpGoal ?? f.get(learner, 'learner/daily-xp-goal') ?? null;
  const pace = d && !totals.missingBases ? totals.baseXp / d : null;
  const goalPace = positive(goal) && positive(conversion) ? goal / conversion : null;
  const reviewOtherPerDay = d && !totals.missingBases ? (totals.reviewBaseXp + totals.otherBaseXp) / d : null;
  const shareTotal = Object.values(shares).reduce((a, b) => a + b, 0);
  for (const course of Object.values(courses)) {
    course.growth = growth.courses[course.code];
    const share = shareTotal > 0 ? shares[course.code] / shareTotal : 1 / TARGET_COURSE_CODES.length;
    course.reviewOtherBaseXpPerDay = d && reviewOtherPerDay !== null ? (overhead[course.code] + share * unassignedOverhead) / d : null;
    course.initialWorkBaseXp = retry === null || course.unknownCosts.length ? null : (1 + quizRatio) * retry * course.remainingLessonBaseXp;
    course.dailyDemandBaseXp = retry === null || course.growth.baseXpPerDay === null || course.reviewOtherBaseXpPerDay === null ? null
      : (1 + quizRatio) * (retry * course.growth.baseXpPerDay + course.reviewOtherBaseXpPerDay);
  }
  const values = Object.values(courses), sum = key => values.reduce((sum, course) => sum + course[key], 0);
  const remainingTopics = sum('remainingTopics');
  const B = values.some(c => c.initialWorkBaseXp === null) ? null : sum('initialWorkBaseXp');
  const k = values.some(c => c.dailyDemandBaseXp === null) ? null : sum('dailyDemandBaseXp');
  const warnings = [];
  if (values.some(c => c.unknownCosts.length)) warnings.push('Some unfinished lessons have no usable estimate.');
  if (growth.reason) warnings.push(growth.reason);
  if (growth.total.unknownCosts) warnings.push('Some historical additions have unknown costs.');
  if (retry === null) warnings.push('No successful dated lessons available to estimate retries.');
  if (totals.missingBases) warnings.push('Recent finished attempts are missing base XP.');
  if (totals.missingTiming) warnings.push('Some recent attempts have incomplete recorded time.');
  if (!positive(conversion)) warnings.push('No positive earned-to-base conversion is available.');
  const { modeledTasks, ...publicGrowth } = growth;
  return { basis: inputs.basis, capturedAt: inputs.capturedAt, scope: scopeOptions,
    inventory: { selectedTopics: scope.nodeIds.size, roots: scope.roots.size, remainingTopics,
      remainingLessonBaseXp: sum('remainingLessonBaseXp'), unknownCosts: values.flatMap(c => c.unknownCosts) },
    pace: { observedFrom: new Date(start).toISOString(), observedThrough: new Date(end).toISOString(), observedDays: d,
      ...totals, workingMinutes, baseXpPerDay: pace, activeMinutesPerDay: d ? workingMinutes / d : null,
      baseXpPerActiveMinute: positive(workingMinutes) && !totals.missingTiming && !totals.missingBases ? totals.baseXp / workingMinutes : null,
      earnedToBaseFactor: conversion, dailyEarnedXpGoal: goal, goalBaseXpPerDay: goalPace },
    overhead: { retryFactor: retry, retryWindow: positive(totals.successfulLessonBaseXp) ? 'recent' : 'all-dated-history',
      quizRatio, quizRatioSource: positive(totals.nonQuizBaseXp) ? 'observed' : '15/150 approximation',
      reviewOtherBaseXpPerDay: reviewOtherPerDay, reviewsPerDay: d ? totals.reviewAttempts / d : null },
    growth: publicGrowth, courses: values, initialWorkBaseXp: B, dailyDemandBaseXp: k,
    currentPace: completionEstimate(B, k, pace, now, remainingTopics),
    goalPace: completionEstimate(B, k, goalPace, now, remainingTopics), warnings };
}

export function forecastDayStarts(now = new Date()) {
  return Array.from({ length: 8 }, (_, i) => new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7 + i).getTime());
}

export function savedForecastScope(storage = globalThis.localStorage) {
  const read = (key, fallback) => { try { return JSON.parse(storage?.getItem(key)) ?? fallback; } catch { return fallback; } };
  const courses = read('course-academy.graph-target-courses', TARGET_COURSE_CODES);
  return { courses: Array.isArray(courses) ? courses.filter(code => TARGET_COURSE_CODES.includes(code)) : TARGET_COURSE_CODES,
    includeQueue: read('course-academy.graph-target-queue', true) !== false,
    weekSelection: read('course-academy.graph-target-weeks', { kind: 'all' }) };
}

// The same captured inputs can be recalculated with a different goal without
// writing learner state or refetching history: calculateForecast(inputs,{...scope,dailyXpGoal}).
export async function readForecast(options = {}) {
  const { signal, ...scope } = options;
  const boundaries = forecastDayStarts();
  const response = await readRequest('/api/forecast-inputs?dayStarts=' + boundaries.join(','), { signal });
  const inputs = await response.json();
  if (!response.ok) throw new Error(inputs.error || 'Unable to read forecast inputs.');
  return calculateForecast(inputs, { ...savedForecastScope(), ...scope, windowEnd: boundaries[7] });
}
