// Calendar arithmetic uses civil days in the study timezone, not elapsed
// local hours, so Sunday boundaries remain stable across daylight saving time.
const CALENDAR_DAY_MS = 86400000;
export const TARGET_WEEK_TIME_ZONE = 'America/Los_Angeles';
const calendarFormatters = new Map();

export function targetCalendarDay(instant, timeZone = TARGET_WEEK_TIME_ZONE) {
  if (instant === null || instant === undefined || instant === '') return null;
  const date = new Date(instant);
  if (!Number.isFinite(date.getTime())) return null;
  if (!calendarFormatters.has(timeZone)) calendarFormatters.set(timeZone, new Intl.DateTimeFormat('en-US', {
    timeZone, year: 'numeric', month: 'numeric', day: 'numeric',
  }));
  const parts = calendarFormatters.get(timeZone).formatToParts(date);
  const part = type => Number(parts.find(p => p.type === type).value);
  return Date.UTC(part('year'), part('month') - 1, part('day')) / CALENDAR_DAY_MS;
}

export function targetWeekStart(day) {
  return day - new Date(day * CALENDAR_DAY_MS).getUTCDay();
}

export function buildTargetCalendar(schedule = [], now = Date.now()) {
  const assignments = schedule.map(assignment => ({
    ...assignment, day: targetCalendarDay(assignment.due),
    topicIds: [...new Set((assignment.topicIds || []).filter(id => Number.isSafeInteger(id) && id > 0))],
  }));
  const dated = assignments.filter(assignment => assignment.day !== null);
  const scheduledIds = new Set(dated.flatMap(assignment => assignment.topicIds));
  const currentWeek = targetWeekStart(targetCalendarDay(now));
  const weeks = [];
  if (dated.length) {
    const first = targetWeekStart(Math.min(...dated.map(assignment => assignment.day)));
    const last = targetWeekStart(Math.max(...dated.map(assignment => assignment.day)));
    for (let startDay = first; startDay <= last; startDay += 7) {
      weeks.push({ number: weeks.length + 1, startDay, endDay: startDay + 6, current: startDay === currentWeek });
    }
  }
  return { assignments, scheduledIds, weeks };
}

export function targetWeekDate(day) {
  const date = new Date(day * CALENDAR_DAY_MS);
  return `${date.getUTCMonth() + 1}/${String(date.getUTCDate()).padStart(2, '0')}`;
}

export function targetWeekLabel(week) {
  return `Week ${week.number} - ${targetWeekDate(week.startDay)}-${targetWeekDate(week.endDay)}`;
}

export function normalizeTargetWeekSelection(calendar, selection) {
  if (selection?.kind === 'unscheduled') return { kind: 'unscheduled' };
  const starts = new Set(calendar.weeks.map(week => week.startDay));
  if (selection?.kind === 'range' && starts.has(selection.start) && starts.has(selection.end) && selection.start <= selection.end) {
    return { kind: 'range', start: selection.start, end: selection.end,
      anchor: starts.has(selection.anchor) ? selection.anchor : selection.start };
  }
  return { kind: 'all' };
}

export function selectTargetWeek(calendar, selection, startDay, extend = false) {
  if (!calendar.weeks.some(week => week.startDay === startDay)) return selection;
  const previous = normalizeTargetWeekSelection(calendar, selection);
  const anchor = extend && previous.kind === 'range' ? previous.anchor : startDay;
  return { kind: 'range', start: Math.min(anchor, startDay), end: Math.max(anchor, startDay), anchor };
}

export function filterScheduledTargets(targets, calendar, selection, courseIds = null) {
  if (selection.kind === 'all') return targets;
  if (selection.kind === 'unscheduled') return targets.filter(id => !calendar.scheduledIds.has(id));
  const included = new Set();
  for (const assignment of calendar.assignments) {
    if (assignment.day === null || assignment.day < selection.start || assignment.day > selection.end + 6) continue;
    if (courseIds && !courseIds.has(assignment.courseId)) continue;
    for (const id of assignment.topicIds) included.add(id);
  }
  return targets.filter(id => included.has(id));
}

export function targetWeekSelectionLabel(calendar, selection) {
  if (selection.kind === 'all') return 'All weeks';
  if (selection.kind === 'unscheduled') return 'Unscheduled';
  const first = calendar.weeks.find(week => week.startDay === selection.start);
  const last = calendar.weeks.find(week => week.startDay === selection.end);
  if (!first || !last) return 'All weeks';
  if (first === last) return targetWeekLabel(first);
  return `Weeks ${first.number}–${last.number} - ${targetWeekDate(first.startDay)}-${targetWeekDate(last.endDay)}`;
}
