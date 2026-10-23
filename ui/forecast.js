// Forecast calculations only; presentation is deliberately left to the caller.
import { readRequest } from './requests.js';
import { projectTargetScope, assignTargetCourses, targetSelectors, TARGET_COURSE_CODES } from './target-scope.js';
import { buildTargetCalendar, normalizeTargetWeekSelection, targetCalendarDay } from './target-weeks.js';

const DAY = 86400000;
export const FORECAST_GROWTH_START = '2026-10-04';
export const FORECAST_GROWTH_HALF_LIFE_DAYS = 28;
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
    this.attributes = new Map();
    for (const [e, record] of this.records) for (const [a, values] of record) if (values.size) {
      if (!this.attributes.has(a)) this.attributes.set(a, new Set());
      this.attributes.get(a).add(e);
    }
  }
  values(e, a) { return [...(this.records.get(Number(e))?.get(a)?.values() || [])]; }
  get(e, a) { return scalar(this.records.get(Number(e))?.get(a)?.values().next().value); }
  kind(e, a) { return (this.enums[this.get(e, a)] || '').split('/').at(-1); }
  ids(a) { return [...(this.attributes.get(a) || [])]; }
  apply(changes) {
    // Transaction operations are simultaneous; remove old facts before adding.
    for (const added of [false, true]) for (const [e, a, v, isAdded] of changes) {
      if (isAdded !== added) continue;
      if (!this.records.has(e)) this.records.set(e, new Map());
      const record = this.records.get(e);
      if (!record.has(a)) record.set(a, new Map());
      if (added) record.get(a).set(JSON.stringify(v), v);
      else record.get(a).delete(JSON.stringify(v));
      if (!this.attributes.has(a)) this.attributes.set(a, new Set());
      if (record.get(a).size) this.attributes.get(a).add(e); else this.attributes.get(a).delete(e);
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

// Same lesson-known evidence and mode-specific ancestry as learning::known_preparation_topics.
// Current coverage comes directly from that engine function; replay needs the
// equivalent calculation over historical facts, without invoking a scheduler.
export function knownPreparationTopics(f, learner) {
  const selfDirected = f.get(learner, 'learner/self-directed') === true;
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
    if (learned === true || (selfDirected ? repetitions >= 1 : learned === undefined && repetitions > 0)) pending.push(f.get(id, 'progress/topic'));
  }
  for (const task of f.values(learner, 'learner/activity')) {
    const activity = f.get(task, 'learner-task/activity');
    if (f.kind(task, 'learner-task/status') === 'completed' && ['lesson', 'review'].includes(f.kind(activity, 'activity/type'))) {
      const topic = f.get(activity, 'activity/scope');
      if (topic !== undefined) pending.push(topic);
    }
  }
  // Scoped study may intentionally begin above an unlearned prerequisite.
  // Completing that lesson does not remove its ancestors from remaining work.
  if (selfDirected) return new Set(pending);
  const known = new Set();
  for (let i = 0; i < pending.length; i++) if (!known.has(pending[i])) {
    known.add(pending[i]); pending.push(...(prerequisites.get(pending[i]) || []));
  }
  return known;
}

function topicPrices(f, learner, estimates) {
  const lessons = new Map(), active = new Map(), finished = new Map();
  for (const id of f.ids('activity/type')) if (f.kind(id, 'activity/type') === 'lesson') {
    const topic = f.get(id, 'activity/scope');
    if (!lessons.has(topic)) lessons.set(topic, []);
    lessons.get(topic).push(id);
  }
  for (const task of f.values(learner, 'learner/activity')) {
    const activity = f.get(task, 'learner-task/activity'), base = f.get(task, 'learner-task/xp-base');
    if (f.kind(activity, 'activity/type') === 'lesson' && positive(base)) {
      const topic = f.get(activity, 'activity/scope');
      if (terminal(f.kind(task, 'learner-task/status'))) {
        const at = f.get(task, 'learner-task/finished-at') ?? 0, previous = finished.get(topic);
        if (!previous || at > previous.at || (at === previous.at && task > previous.task)) finished.set(topic, { at, task, baseXp: base });
        continue;
      }
      if (!active.has(topic)) active.set(topic, []);
      active.get(topic).push(base);
    }
  }
  const direct = topic => {
    if (active.get(topic)?.length === 1) return { baseXp: active.get(topic)[0], source: 'saved-attempt' };
    if (active.get(topic)?.length > 1) return { baseXp: null, reason: 'Multiple unfinished lesson attempts.' };
    if (finished.has(topic)) return { baseXp: finished.get(topic).baseXp, source: 'saved-attempt' };
    const choices = lessons.get(topic) || [];
    if (choices.length !== 1) return { baseXp: null, reason: choices.length ? 'Multiple lesson definitions.' : 'No lesson definition.' };
    const seconds = f.get(choices[0], 'activity/expected-seconds');
    if (seconds !== undefined) return positive(seconds)
      ? { baseXp: Math.max(1, Math.floor(seconds / 60 + .5)), source: 'stored-duration' }
      : { baseXp: null, reason: 'Invalid lesson duration.' };
    return { ...(estimates[choices[0]] || { baseXp: null, reason: 'No lesson estimate at this historical state.' }), source: 'content-estimate' };
  };
  const kpCount = topic => new Set(f.values(topic, 'topic/knowledge-points')).size;
  let peers;
  const median = values => {
    const middle = Math.floor(values.length / 2);
    return values.length % 2 ? values[middle] : (values[middle - 1] + values[middle]) / 2;
  };
  return topic => {
    const cost = direct(topic);
    if (positive(cost.baseXp) || active.get(topic)?.length > 1) return cost;
    // Forecast estimates never change lesson content, stored prices or XP awards.
    // Only directly priced topics are peers; fallbacks never feed other fallbacks.
    if (!peers) {
      peers = new Map([[0, []]]);
      for (const id of f.ids('topic/id')) {
        const base = direct(id).baseXp;
        if (!positive(base)) continue;
        peers.get(0).push(base);
        const count = kpCount(id);
        if (!count) continue;
        if (!peers.has(count)) peers.set(count, []);
        peers.get(count).push(base);
      }
      for (const values of peers.values()) values.sort((a, b) => a - b);
    }
    const count = kpCount(topic), matched = count > 0 && peers.get(count)?.length;
    const values = peers.get(matched ? count : 0);
    if (!values.length) return cost;
    return { baseXp: median(values), source: matched ? 'kp-count-median' : 'lesson-median',
      fallback: true, sampleSize: values.length, knowledgePointCount: count, reason: cost.reason };
  };
}

const growthFields = new Set(['topic/id', 'topic/title', 'topic/next', 'course/id', 'course/code',
  'course/units', 'unit/modules', 'module/topics', 'learner/targets', 'learner/queue',
  'learner/assignments', 'activity/course', 'activity/due', 'activity/steps',
  'step/content', 'multistep/steps', 'assigned-problem/content', 'assigned-problem/topic-coverage']);
const emptyCategories = () => Object.fromEntries(['target', 'queue', 'prerequisite'].map(key => [key, { topics: 0, baseXp: 0 }]));
const emptyGrowth = () => ({ topics: 0, baseXp: 0, weightedTopics: 0, weightedBaseXp: 0,
  estimatedTopics: [], unknownCosts: 0, unknownTopics: [],
  categories: Object.fromEntries(Object.entries(emptyCategories()).map(([key, value]) => [key,
    { ...value, weightedTopics: 0, weightedBaseXp: 0 }])) });

const civilClock = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', hourCycle: 'h23',
  year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' });
function civilMilliseconds(at) {
  const parts = civilClock.formatToParts(new Date(at));
  const part = type => Number(parts.find(p => p.type === type).value);
  return Date.UTC(part('year'), part('month') - 1, part('day'), part('hour'), part('minute'), part('second'));
}
function dayStartsAt(day) {
  let at = day * DAY;
  for (let i = 0; i < 3; i++) at += day * DAY - civilMilliseconds(at);
  return at;
}
// Date admission is applied to the viewer's selected roots, before expanding
// prerequisites. A prerequisite inherits the earliest date of any needing root.
export function topicDueDays(snapshot, scope, options, datedOnly = false) {
  const calendar = buildTargetCalendar(snapshot.targetSchedule || []);
  const courseIds = targetSelectors(snapshot, scope.graph, options, calendar).targetWeekCourseIds();
  const week = options.weekSelection ?? { kind: 'all' }, rootDays = new Map();
  for (const assignment of calendar.assignments) {
    if (assignment.day === null || (courseIds && !courseIds.has(assignment.courseId))) continue;
    if (week.kind === 'unscheduled') continue;
    if (week.kind === 'range' && (assignment.day < week.start || assignment.day > week.end + 6)) continue;
    for (const topic of assignment.topicIds) if (scope.roots.has(topic)) {
      rootDays.set(topic, Math.min(rootDays.get(topic) ?? Infinity, assignment.day));
    }
  }
  const queued = new Set(options.includeQueue !== false ? snapshot.learner.queue || [] : []);
  const dueDays = new Map();
  for (const root of scope.roots) {
    // Queue and undated targets are standing work; no invented future date.
    if (datedOnly && !rootDays.has(root)) continue;
    const day = datedOnly ? rootDays.get(root) : queued.has(root) ? -Infinity : rootDays.get(root) ?? -Infinity;
    const pending = [[root, 0]], seen = new Set([root]);
    for (let i = 0; i < pending.length; i++) {
      const [id, distance] = pending[i];
      dueDays.set(id, Math.min(dueDays.get(id) ?? Infinity, day));
      if (distance >= 2) continue;
      for (const previous of scope.graph.inMap.get(id) || []) {
        if (!seen.has(previous) && scope.graph.nodeById.get(previous)?.layer >= 29) {
          seen.add(previous); pending.push([previous, distance + 1]);
        }
      }
    }
  }
  return dueDays;
}

function preparationKnownAt(inputs, facts, learner, graph) {
  const selfDirected = facts.get(learner, 'learner/self-directed') === true;
  const seeds = [], terminalDates = new Map();
  const ownedProgress = new Set(facts.values(learner, 'learner/knowledge-profile'));
  for (const event of inputs.history) {
    const at = new Date(scalar(event.at)).getTime();
    if (!Number.isFinite(at)) continue;
    for (const [id, attr, value, added] of event.changes) {
      if (!added) continue;
      if (attr === 'learner-task/status' && (inputs.enums[value] || '').endsWith('/completed')) {
        if (!terminalDates.has(id)) terminalDates.set(id, at);
      }
      if (!ownedProgress.has(id)) continue;
      const learned = facts.get(id, 'progress/learned');
      if ((attr === 'progress/learned' && value === true) ||
        (attr === 'progress/repetitions' && (selfDirected ? Number.isFinite(value) && value >= 1 : positive(value) && learned === undefined))) {
        const topic = facts.get(id, 'progress/topic');
        if (topic !== undefined) seeds.push([topic, at]);
      }
    }
  }
  for (const task of facts.values(learner, 'learner/activity')) {
    const activity = facts.get(task, 'learner-task/activity');
    if (facts.kind(task, 'learner-task/status') !== 'completed' || !['lesson', 'review'].includes(facts.kind(activity, 'activity/type'))) continue;
    const at = inputs.finishedAt[task] ?? terminalDates.get(task), topic = facts.get(activity, 'activity/scope');
    if (Number.isFinite(at) && topic !== undefined) seeds.push([topic, at]);
  }
  const parents = selfDirected ? new Map()
    : new Map([...graph.inMap].map(([topic, ids]) => [topic, new Set(ids)]));
  for (const topic of parents.keys()) for (const kp of facts.values(topic, 'topic/knowledge-points')) {
    for (const previous of facts.values(kp, 'knowledge-point/key-prerequisites')) parents.get(topic).add(previous);
  }
  const known = new Map(), pending = seeds.sort((a, b) => a[1] - b[1]);
  for (let i = 0; i < pending.length; i++) {
    const [topic, at] = pending[i];
    if ((known.get(topic) ?? Infinity) <= at) continue;
    known.set(topic, at);
    for (const previous of parents.get(topic) || []) pending.push([previous, at]);
  }
  return known;
}

export function historicalGrowth(inputs, options, currentScope, now) {
  const f = new ForecastFacts({}, inputs.enums), learner = inputs.learnerId;
  const currentFacts = new ForecastFacts(inputs.records, inputs.enums);
  const snapshot = forecastGraph(currentFacts, learner), price = topicPrices(currentFacts, learner, inputs.lessonBases);
  const knownAt = preparationKnownAt(inputs, currentFacts, learner, currentScope.graph);
  const courses = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, emptyGrowth()]));
  const total = emptyGrowth(), modeledTasks = new Set();
  let previous = null, indexedGraph, historyReason = null;
  // Retained graph membership is used only to recognize completed lessons that
  // left the Queue. It is not an additional source of forecast workload growth.
  const containment = new Set(['activity/steps', 'step/content', 'multistep/steps', 'assigned-problem/content']);
  const possibleChildren = new Map(), assignments = new Set();
  for (const event of inputs.history) for (const [e, a, v] of event.changes) {
    if (e === learner && a === 'learner/assignments') assignments.add(v);
    if (containment.has(a)) {
      if (!possibleChildren.has(e)) possibleChildren.set(e, new Set());
      possibleChildren.get(e).add(v);
    }
  }
  const assignmentEntities = new Set(assignments), pending = [...assignments];
  for (let i = 0; i < pending.length; i++) for (const next of possibleChildren.get(pending[i]) || []) {
    if (!assignmentEntities.has(next)) { assignmentEntities.add(next); pending.push(next); }
  }
  const assignmentFields = new Set([...containment, 'assigned-problem/topic-coverage', 'activity/course', 'activity/due']);
  for (const event of inputs.history) {
    const at = new Date(scalar(event.at)).getTime();
    if (!Number.isFinite(at) || at > now) continue;
    const completed = event.changes.filter(([, a, v, added]) => added && a === 'learner-task/status'
      && terminal((inputs.enums[v] || '').split('/').at(-1))).map(([task]) => task);
    f.apply(event.changes);
    if (event.changes.some(([, a]) => ['topic/id', 'topic/title', 'topic/next'].includes(a))) indexedGraph = undefined;
    for (const task of completed) {
      const topic = f.get(f.get(task, 'learner-task/activity'), 'activity/scope');
      if (previous?.nodeIds.has(topic)) modeledTasks.add(task);
    }
    if (!event.changes.some(([e, a]) => growthFields.has(a) && (!assignmentFields.has(a) || assignmentEntities.has(e)))) continue;
    if (!f.get(learner, 'learner/id') || !f.ids('topic/id').length) continue;
    try {
      previous = projectTargetScope(forecastGraph(f, learner), options, indexedGraph);
      indexedGraph = previous.graph;
    } catch (error) { historyReason = error.message; continue; }
    for (const task of completed) {
      const topic = f.get(f.get(task, 'learner-task/activity'), 'activity/scope');
      if (previous.nodeIds.has(topic)) modeledTasks.add(task);
    }
  }
  if (previous && (previous.nodeIds.size !== currentScope.nodeIds.size || [...previous.nodeIds].some(id => !currentScope.nodeIds.has(id))
    || [...previous.tracks].some(([id, course]) => currentScope.tracks.get(id) !== course))) {
    historyReason = 'Retained history does not reproduce the current filtered graph.';
  }

  const startDay = Date.parse(FORECAST_GROWTH_START + 'T00:00:00Z') / DAY;
  const today = targetCalendarDay(now), observedDays = Math.max(0, today - startDay);
  // Keep the agreed elapsed-day convention: Oct 4 -> Oct 21 is 17 daily
  // intervals. Their endpoint weights include zero-growth days and use civil
  // dates, so DST and the clock time of this read cannot change today's rate.
  const decay = Math.LN2 / FORECAST_GROWTH_HALF_LIFE_DAYS;
  const weightSum = observedDays ? -Math.expm1(-decay * observedDays) / -Math.expm1(-decay) : 0;
  // Earliest due dates are computed using ALL assignments, including those
  // before the window. Old prerequisites cannot re-enter as new growth later.
  const scheduled = topicDueDays(snapshot, currentScope, options, true);
  for (const [topic, day] of scheduled) {
    if (day < startDay || day > today || (knownAt.get(topic) ?? Infinity) <= dayStartsAt(day)) continue;
    const cost = price(topic), weight = Math.exp(-decay * (today - day));
    const course = currentScope.tracks.get(topic), category = currentScope.categories.get(topic);
    for (const item of [total, courses[course]]) {
      item.topics++; item.weightedTopics += weight;
      item.categories[category].topics++; item.categories[category].weightedTopics += weight;
      if (positive(cost.baseXp)) {
        item.baseXp += cost.baseXp; item.weightedBaseXp += cost.baseXp * weight;
        item.categories[category].baseXp += cost.baseXp;
        item.categories[category].weightedBaseXp += cost.baseXp * weight;
      } else {
        item.unknownCosts++; item.unknownTopics.push({ topicId: topic, reason: cost.reason });
      }
      if (cost.fallback) item.estimatedTopics.push({ topicId: topic, ...cost });
    }
  }
  const usable = weightSum > 0;
  const observedFrom = new Date(dayStartsAt(startDay)).toISOString();
  const summarize = item => ({ ...item, isLowerBound: item.unknownCosts > 0,
    observedFrom, observedDays,
    baseXpPerDay: usable ? item.weightedBaseXp / weightSum : null,
    baseXpPerWeek: usable ? 7 * item.weightedBaseXp / weightSum : null,
    topicsPerWeek: usable ? 7 * item.weightedTopics / weightSum : null,
    unweightedBaseXpPerDay: observedDays ? item.baseXp / observedDays : null,
    categories: Object.fromEntries(Object.entries(item.categories).map(([key, value]) => [key, { ...value,
      topicsPerWeek: usable ? 7 * value.weightedTopics / weightSum : null,
      baseXpPerWeek: usable ? 7 * value.weightedBaseXp / weightSum : null }])),
  });
  const byCourse = Object.fromEntries(Object.entries(courses).map(([code, value]) => [code, summarize(value)]));
  return { clock: 'assignment-due-dates', method: 'exponential-daily',
    windowStart: FORECAST_GROWTH_START, halfLifeDays: FORECAST_GROWTH_HALF_LIFE_DAYS, weightSum,
    observedFrom, observedThrough: new Date(now).toISOString(),
    throughDate: new Date(today * DAY).toISOString().slice(0, 10), observedDays,
    reason: usable ? null : 'No elapsed days in the forecast growth window.', historyReason,
    total: summarize(total), courses: byCourse, modeledTasks };
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

function scenario(forecast, pace) {
  const result = completionEstimate(forecast.initialWorkBaseXp, forecast.dailyDemandBaseXp, pace,
    Date.parse(forecast.capturedAt), forecast.inventory.remainingTopics);
  result.growthIsLowerBound = forecast.growth.total.isLowerBound;
  result.optimistic = result.status === 'estimated' && result.growthIsLowerBound;
  result.usesFallbackEstimates = forecast.inventory.estimatedTopics.length > 0 || forecast.growth.total.estimatedTopics.length > 0;
  if (result.days === null) return { ...result, workload: null };
  const T = result.days, d = forecast.pace.observedDays, o = forecast.overhead;
  const lessonAttemptBaseXp = T === 0 ? 0 : o.retryFactor * (forecast.inventory.remainingLessonBaseXp + forecast.growth.total.baseXpPerDay * T);
  const reviewBaseXp = d ? forecast.pace.reviewBaseXp / d * T : 0;
  const otherBaseXp = d ? forecast.pace.otherBaseXp / d * T : 0;
  const quizBaseXp = o.quizRatio * (lessonAttemptBaseXp + reviewBaseXp + otherBaseXp);
  return { ...result, workload: { lessonAttemptBaseXp, reviewBaseXp, otherBaseXp, quizBaseXp,
    totalBaseXp: lessonAttemptBaseXp + reviewBaseXp + otherBaseXp + quizBaseXp,
    estimatedReviews: d ? forecast.pace.reviewAttempts / d * T : 0,
    estimatedQuizzes: quizBaseXp / o.averageQuizBaseXp } };
}

// Goal previews reuse the measured workload/rates and update immediately,
// without replaying history, fetching data, or writing the saved goal.
export function withForecastGoal(forecast, dailyEarnedXpGoal) {
  const factor = forecast.pace.earnedToBaseFactor;
  const goalBaseXpPerDay = positive(dailyEarnedXpGoal) && positive(factor) ? dailyEarnedXpGoal / factor : null;
  return { ...forecast, pace: { ...forecast.pace, dailyEarnedXpGoal, goalBaseXpPerDay },
    goalPace: scenario(forecast, goalBaseXpPerDay) };
}

// Keep one shared budget: every course receives exactly one third, even
// after another course catches up. Each track retains its own work/demand.
export function courseCompletionEstimates(forecast) {
  const split = pace => Number.isFinite(pace) ? pace / TARGET_COURSE_CODES.length : null;
  return forecast.courses.map(course => ({ ...course,
    currentPace: completionEstimate(course.initialWorkBaseXp, course.dailyDemandBaseXp,
      split(forecast.pace.baseXpPerDay), Date.parse(forecast.capturedAt), course.remainingTopics),
    goalPace: completionEstimate(course.initialWorkBaseXp, course.dailyDemandBaseXp,
      split(forecast.pace.goalBaseXpPerDay), Date.parse(forecast.capturedAt), course.remainingTopics),
  }));
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
  const activation = topicDueDays(graph, scope, scopeOptions), today = targetCalendarDay(now);
  const courses = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, { code, selectedTopics: 0, remainingTopics: 0,
    remainingLessonBaseXp: 0, estimatedTopics: [], unknownCosts: [], futureRemainingTopics: 0, futureLessonBaseXp: 0,
    futureEstimatedTopics: [], futureUnknownCosts: [], categories: emptyCategories() }]));
  for (const topic of scope.nodeIds) {
    const course = courses[scope.tracks.get(topic)]; course.selectedTopics++;
    if (known.has(topic)) continue;
    const cost = price(topic), day = activation.get(topic), category = course.categories[scope.categories.get(topic)];
    if (cost.fallback) course[day > today ? 'futureEstimatedTopics' : 'estimatedTopics'].push({ topicId: topic, ...cost });
    if (day > today) {
      course.futureRemainingTopics++;
      if (positive(cost.baseXp)) course.futureLessonBaseXp += cost.baseXp;
      else course.futureUnknownCosts.push({ topicId: topic, dueDay: day, reason: cost.reason || 'Unknown lesson cost.' });
      continue;
    }
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
    successfulLessonBaseXp: 0, quizBaseXp: 0, quizAttempts: 0, nonQuizBaseXp: 0, reviewBaseXp: 0, reviewAttempts: 0,
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
    if (kind === 'assessment') { totals.quizBaseXp += base; totals.quizAttempts++; continue; }
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
  if (growth.historyReason) warnings.push(growth.historyReason);
  if (growth.total.unknownCosts) warnings.push(`Historical growth is a lower bound: ${growth.total.unknownCosts} topics have no usable XP estimate.`);
  const estimated = new Set([...growth.total.estimatedTopics, ...values.flatMap(c => c.estimatedTopics)].map(item => item.topicId));
  if (estimated.size) warnings.push(`${estimated.size} ${estimated.size === 1 ? 'lesson uses' : 'lessons use'} fallback XP estimates.`);
  if (retry === null) warnings.push('No successful dated lessons available to estimate retries.');
  if (totals.missingBases) warnings.push('Recent finished attempts are missing base XP.');
  if (totals.missingTiming) warnings.push('Some recent attempts have incomplete recorded time.');
  if (!positive(conversion)) warnings.push('No positive earned-to-base conversion is available.');
  const { modeledTasks, ...publicGrowth } = growth;
  const forecast = { basis: inputs.basis, capturedAt: inputs.capturedAt, scope: scopeOptions,
    inventory: { selectedTopics: scope.nodeIds.size, roots: scope.roots.size, remainingTopics,
      remainingLessonBaseXp: sum('remainingLessonBaseXp'), unknownCosts: values.flatMap(c => c.unknownCosts),
      estimatedTopics: values.flatMap(c => c.estimatedTopics),
      dueThrough: new Date(today * DAY).toISOString().slice(0, 10), futureRemainingTopics: sum('futureRemainingTopics'),
      futureLessonBaseXp: sum('futureLessonBaseXp'), futureEstimatedTopics: values.flatMap(c => c.futureEstimatedTopics),
      futureUnknownCosts: values.flatMap(c => c.futureUnknownCosts) },
    pace: { observedFrom: new Date(start).toISOString(), observedThrough: new Date(end).toISOString(), observedDays: d,
      ...totals, workingMinutes, baseXpPerDay: pace, activeMinutesPerDay: d ? workingMinutes / d : null,
      baseXpPerActiveMinute: positive(workingMinutes) && !totals.missingTiming && !totals.missingBases ? totals.baseXp / workingMinutes : null,
      earnedToBaseFactor: conversion, dailyEarnedXpGoal: goal, goalBaseXpPerDay: goalPace },
    overhead: { retryFactor: retry, retryWindow: positive(totals.successfulLessonBaseXp) ? 'recent' : 'all-dated-history',
      quizRatio, quizRatioSource: positive(totals.nonQuizBaseXp) ? 'observed' : '15/150 approximation',
      averageQuizBaseXp: totals.quizAttempts ? totals.quizBaseXp / totals.quizAttempts : 15,
      reviewOtherBaseXpPerDay: reviewOtherPerDay, reviewsPerDay: d ? totals.reviewAttempts / d : null },
    growth: publicGrowth, courses: values, initialWorkBaseXp: B, dailyDemandBaseXp: k,
    warnings };
  return { ...forecast, currentPace: scenario(forecast, pace), goalPace: scenario(forecast, goalPace) };
}

export function forecastDayStarts(now = new Date()) {
  return Array.from({ length: 8 }, (_, i) => new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7 + i).getTime());
}

// Read database evidence independently of browser graph-view preferences.
// Defaults cover all three courses and Queue. Assignment work enters the
// current backlog only on its local due date; future-only work stays separate.
export async function readForecast(options = {}) {
  const { signal, ...scope } = options;
  const boundaries = forecastDayStarts();
  const response = await readRequest('/api/forecast-inputs?dayStarts=' + boundaries.join(','), { signal });
  const inputs = await response.json();
  if (!response.ok) throw new Error(inputs.error || 'Unable to read forecast inputs.');
  return calculateForecast(inputs, { ...scope, windowEnd: boundaries[7] });
}
