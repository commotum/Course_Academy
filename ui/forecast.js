// Forecast calculations only; presentation is deliberately left to the caller.
import { readRequest } from './requests.js';
import { projectTargetScope, assignTargetCourses, targetSelectors, TARGET_COURSE_CODES } from './target-scope.js';
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
function calendarExposure(start, end) {
  return Math.max(0, (civilMilliseconds(end) - civilMilliseconds(start)) / DAY);
}

// Date admission is applied to the viewer's selected roots, before expanding
// prerequisites. A prerequisite inherits the earliest date of any needing root.
export function topicDueDays(snapshot, scope, options) {
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
    const day = queued.has(root) ? -Infinity : rootDays.get(root) ?? -Infinity;
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

export function historicalGrowth(inputs, options, currentScope, now) {
  const f = new ForecastFacts({}, inputs.enums), learner = inputs.learnerId;
  const courses = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, emptyGrowth()]));
  const total = emptyGrowth(), modeledTasks = new Set();
  let previous = null, previousDue = new Set(), observedFrom = null, invalid = null, indexedGraph;
  // Review/lesson preparation creates steps too. Only assignment-owned
  // containment can change the Targets calendar or course associations.
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
  const dueDays = new Set();
  for (const event of inputs.history) for (const [e, a, v] of event.changes) {
    if (a === 'activity/due' && assignments.has(e)) {
      const day = targetCalendarDay(scalar(v));
      if (day !== null) dueDays.add(day);
    }
  }
  const events = [...inputs.history.map(event => ({ ...event, instant: new Date(scalar(event.at)).getTime() })),
    ...[...dueDays].map(day => ({ instant: dayStartsAt(day), changes: [], virtual: true, t: -1 }))]
    .filter(event => Number.isFinite(event.instant) && event.instant <= now)
    .sort((a, b) => a.instant - b.instant || a.t - b.t);
  for (const event of events) {
    const at = event.instant;
    const completed = event.changes.filter(([, a, v, added]) => added && a === 'learner-task/status'
      && terminal((inputs.enums[v] || '').split('/').at(-1))).map(([task]) => task);
    f.apply(event.changes);
    if (event.changes.some(([, a]) => ['topic/id', 'topic/title', 'topic/next'].includes(a))) indexedGraph = undefined;
    // Task completion can remove its queue root in the same transaction. Its
    // lesson still belongs to the scope it was in immediately before finishing.
    for (const task of completed) {
      const topic = f.get(f.get(task, 'learner-task/activity'), 'activity/scope');
      if (previous?.nodeIds.has(topic)) modeledTasks.add(task);
    }
    if (!event.virtual && !event.changes.some(([e, a]) => growthFields.has(a) && (!assignmentFields.has(a) || assignmentEntities.has(e)))) continue;
    if (!f.get(learner, 'learner/id') || !f.ids('topic/id').length) continue;
    let scope, snapshot;
    try {
      snapshot = forecastGraph(f, learner);
      scope = projectTargetScope(snapshot, options, indexedGraph); indexedGraph = scope.graph;
    } catch (error) { invalid = error.message; continue; }
    for (const task of completed) if (scope.nodeIds.has(f.get(f.get(task, 'learner-task/activity'), 'activity/scope'))) modeledTasks.add(task);
    const activation = topicDueDays(snapshot, scope, options), today = targetCalendarDay(at);
    const due = new Set([...scope.nodeIds].filter(topic => activation.get(topic) <= today));
    if (previous === null) {
      // Retained opening inventory is not an arrival. Future preloads become
      // arrivals only when their actual due day is reached, without a new tx.
      if (!scope.nodeIds.size) continue;
      previous = scope; previousDue = due; observedFrom = at; continue;
    }
    const additions = [...due].filter(topic => !previousDue.has(topic));
    const known = additions.length ? knownPreparationTopics(f, learner) : new Set();
    const price = additions.length ? topicPrices(f, learner, inputs.lessonBases) : null;
    for (const topic of additions) {
      if (known.has(topic)) continue;
      const cost = price(topic), course = courses[scope.tracks.get(topic)], category = scope.categories.get(topic);
      for (const item of [total, course]) {
        item.topics++; item.categories[category].topics++;
        if (positive(cost.baseXp)) { item.baseXp += cost.baseXp; item.categories[category].baseXp += cost.baseXp; }
        else item.unknownCosts++;
      }
    }
    previous = scope; previousDue = due;
  }
  if (previous === null || observedFrom === null) invalid ||= 'No reliable opening inventory in retained history.';
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
  return { clock: 'assignment-due-date-or-standing-entry', observedFrom: observedFrom === null ? null : new Date(observedFrom).toISOString(), observedThrough: new Date(now).toISOString(),
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

// Known scheduled work and average growth describe the same incoming demand.
// Use the larger cumulative amount per course, never their sum: known deadlines
// are honored, while the historical trend can cover work not mapped yet.
export function forecastWorkloadAt(forecast, days) {
  const o = forecast.overhead, d = forecast.pace.observedDays;
  const future = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, 0]));
  const unknownCosts = [...forecast.inventory.unknownCosts];
  for (const step of forecast.demandCurve.steps) {
    if (step.days > days) break;
    for (const topic of step.topics) {
      if (positive(topic.baseXp)) future[topic.course] += topic.baseXp;
      else unknownCosts.push(topic);
    }
  }
  if (unknownCosts.length || !positive(o.retryFactor) || !Number.isFinite(o.reviewOtherBaseXpPerDay)
    || forecast.courses.some(c => c.growth.baseXpPerDay === null)) return null;
  let lessonBaseXp = 0, knownIncomingBaseXp = 0, additionalIncomingBaseXp = 0, slope = o.reviewOtherBaseXpPerDay;
  for (const course of forecast.courses) {
    const known = future[course.code], trend = course.growth.baseXpPerDay * days;
    knownIncomingBaseXp += known;
    additionalIncomingBaseXp += Math.max(0, trend - known);
    lessonBaseXp += course.remainingLessonBaseXp + Math.max(known, trend);
    if (trend >= known) slope += o.retryFactor * course.growth.baseXpPerDay;
  }
  const lessonAttemptBaseXp = o.retryFactor * lessonBaseXp;
  const reviewBaseXp = d ? forecast.pace.reviewBaseXp / d * days : 0;
  const otherBaseXp = d ? forecast.pace.otherBaseXp / d * days : 0;
  const quizBaseXp = o.quizRatio * (lessonAttemptBaseXp + reviewBaseXp + otherBaseXp);
  return { lessonBaseXp, lessonAttemptBaseXp, reviewBaseXp, otherBaseXp, quizBaseXp,
    knownIncomingBaseXp, additionalIncomingBaseXp,
    totalBaseXp: lessonAttemptBaseXp + reviewBaseXp + otherBaseXp + quizBaseXp,
    slope: (1 + o.quizRatio) * slope,
    estimatedReviews: d ? forecast.pace.reviewAttempts / d * days : 0,
    estimatedQuizzes: quizBaseXp / o.averageQuizBaseXp };
}

function scenario(forecast, pace) {
  const now = Date.parse(forecast.capturedAt);
  if (!forecast.inventory.remainingTopics) return { status: 'complete', days: 0,
    date: forecast.capturedAt, baseXpPerDay: pace, workload: { totalBaseXp: 0 } };
  const unavailable = { status: 'unavailable', days: null, date: null, baseXpPerDay: pace, workload: null };
  if (typeof pace !== 'number' || !Number.isFinite(pace) || pace < 0) return unavailable;
  // Inspect every linear segment chronologically. A binary search could skip
  // an early catch-up followed by another assignment becoming due tomorrow.
  const boundaries = new Set([0]), steps = forecast.demandCurve.steps;
  const known = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, 0]));
  for (let i = -1; i < steps.length; i++) {
    const start = i < 0 ? 0 : steps[i].days, end = steps[i + 1]?.days ?? Infinity;
    if (i >= 0) {
      boundaries.add(start);
      for (const topic of steps[i].topics) if (positive(topic.baseXp)) known[topic.course] += topic.baseXp;
    }
    for (const course of forecast.courses) {
      const g = course.growth.baseXpPerDay;
      if (positive(g)) {
        const crossing = known[course.code] / g;
        if (crossing > start && crossing < end) boundaries.add(crossing);
      }
    }
  }
  const points = [...boundaries].sort((a, b) => a - b);
  for (let i = 0; i < points.length; i++) {
    const start = points[i], end = points[i + 1] ?? Infinity;
    const work = forecastWorkloadAt(forecast, start);
    if (work === null) return unavailable;
    const gap = work.totalBaseXp - pace * start;
    let days = gap <= 1e-8 ? start : pace > work.slope ? start + gap / (pace - work.slope) : Infinity;
    // At a due-day boundary the new day's work must already be included.
    if (!Number.isFinite(days) || (Number.isFinite(end) && days >= end - 1e-9)) continue;
    const at = now + days * DAY;
    if (!Number.isFinite(at) || Math.abs(at) > 8.64e15) return { ...unavailable, status: 'out-of-range' };
    return { status: 'estimated', days, date: new Date(at).toISOString(), baseXpPerDay: pace,
      workload: forecastWorkloadAt(forecast, days) };
  }
  return { ...unavailable, status: 'not-catching-up' };
}

// Goal previews reuse the measured workload/rates and update immediately,
// without replaying history, fetching data, or writing the saved goal.
export function withForecastGoal(forecast, dailyEarnedXpGoal) {
  const factor = forecast.pace.earnedToBaseFactor;
  const goalBaseXpPerDay = positive(dailyEarnedXpGoal) && positive(factor) ? dailyEarnedXpGoal / factor : null;
  return { ...forecast, pace: { ...forecast.pace, dailyEarnedXpGoal, goalBaseXpPerDay },
    goalPace: scenario(forecast, goalBaseXpPerDay) };
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
  const future = new Map();
  const courses = Object.fromEntries(TARGET_COURSE_CODES.map(code => [code, { code, selectedTopics: 0, remainingTopics: 0,
    remainingLessonBaseXp: 0, unknownCosts: [], futureRemainingTopics: 0, futureLessonBaseXp: 0,
    futureUnknownCosts: [], categories: emptyCategories() }]));
  for (const topic of scope.nodeIds) {
    const course = courses[scope.tracks.get(topic)]; course.selectedTopics++;
    if (known.has(topic)) continue;
    const cost = price(topic), day = activation.get(topic), category = course.categories[scope.categories.get(topic)];
    if (day > today) {
      course.futureRemainingTopics++;
      if (!future.has(day)) future.set(day, []);
      future.get(day).push({ topicId: topic, course: course.code, baseXp: cost.baseXp, reason: cost.reason });
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
  if (growth.total.unknownCosts) warnings.push('Some historical additions have unknown costs.');
  if (retry === null) warnings.push('No successful dated lessons available to estimate retries.');
  if (totals.missingBases) warnings.push('Recent finished attempts are missing base XP.');
  if (totals.missingTiming) warnings.push('Some recent attempts have incomplete recorded time.');
  if (!positive(conversion)) warnings.push('No positive earned-to-base conversion is available.');
  const { modeledTasks, ...publicGrowth } = growth;
  const forecast = { basis: inputs.basis, capturedAt: inputs.capturedAt, scope: scopeOptions,
    inventory: { selectedTopics: scope.nodeIds.size, roots: scope.roots.size, remainingTopics,
      remainingLessonBaseXp: sum('remainingLessonBaseXp'), unknownCosts: values.flatMap(c => c.unknownCosts),
      dueThrough: new Date(today * DAY).toISOString().slice(0, 10), futureRemainingTopics: sum('futureRemainingTopics'),
      futureLessonBaseXp: sum('futureLessonBaseXp'), futureUnknownCosts: values.flatMap(c => c.futureUnknownCosts) },
    pace: { observedFrom: new Date(start).toISOString(), observedThrough: new Date(end).toISOString(), observedDays: d,
      ...totals, workingMinutes, baseXpPerDay: pace, activeMinutesPerDay: d ? workingMinutes / d : null,
      baseXpPerActiveMinute: positive(workingMinutes) && !totals.missingTiming && !totals.missingBases ? totals.baseXp / workingMinutes : null,
      earnedToBaseFactor: conversion, dailyEarnedXpGoal: goal, goalBaseXpPerDay: goalPace },
    overhead: { retryFactor: retry, retryWindow: positive(totals.successfulLessonBaseXp) ? 'recent' : 'all-dated-history',
      quizRatio, quizRatioSource: positive(totals.nonQuizBaseXp) ? 'observed' : '15/150 approximation',
      averageQuizBaseXp: totals.quizAttempts ? totals.quizBaseXp / totals.quizAttempts : 15,
      reviewOtherBaseXpPerDay: reviewOtherPerDay, reviewsPerDay: d ? totals.reviewAttempts / d : null },
    growth: publicGrowth, courses: values, initialWorkBaseXp: B, dailyDemandBaseXp: k,
    demandCurve: { steps: [...future].sort(([a], [b]) => a - b).map(([day, topics]) => ({
      dueDay: day, at: new Date(dayStartsAt(day)).toISOString(), days: (dayStartsAt(day) - now) / DAY, topics })),
      growthRule: 'greater-of-known-due-work-and-average-growth-per-course' },
    warnings };
  return { ...forecast, currentPace: scenario(forecast, pace), goalPace: scenario(forecast, goalPace) };
}

export function forecastDayStarts(now = new Date()) {
  return Array.from({ length: 8 }, (_, i) => new Date(now.getFullYear(), now.getMonth(), now.getDate() - 7 + i).getTime());
}

export function savedForecastScope(storage) {
  if (storage === undefined) { try { storage = globalThis.localStorage; } catch { /* Storage is optional. */ } }
  const read = (key, fallback) => { try { return JSON.parse(storage?.getItem(key)) ?? fallback; } catch { return fallback; } };
  const courses = read('course-academy.graph-target-courses', TARGET_COURSE_CODES);
  return { courses: Array.isArray(courses) ? courses.filter(code => TARGET_COURSE_CODES.includes(code)) : TARGET_COURSE_CODES,
    includeQueue: read('course-academy.graph-target-queue', true) !== false,
    weekSelection: read('course-academy.graph-target-weeks', { kind: 'all' }) };
}

// Read the latest immutable inputs and calculate without rendering or writing.
export async function readForecast(options = {}) {
  const { signal, ...scope } = options;
  const boundaries = forecastDayStarts();
  const response = await readRequest('/api/forecast-inputs?dayStarts=' + boundaries.join(','), { signal });
  const inputs = await response.json();
  if (!response.ok) throw new Error(inputs.error || 'Unable to read forecast inputs.');
  return calculateForecast(inputs, { ...savedForecastScope(), ...scope, windowEnd: boundaries[7] });
}
