import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
const source = await readFile(new URL('../ui/target-weeks.js', import.meta.url), 'utf8');
const { buildTargetCalendar, targetCalendarDay, targetWeekStart, targetWeekLabel, normalizeTargetWeekSelection,
  selectTargetWeek, filterScheduledTargets, targetWeekSelectionLabel } = await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'));
const assignment = (due, topicIds, courseId = '255') => ({ due, topicIds, courseId });
const now = Date.parse('2026-10-12T12:00:00Z');

function calendar() {
  return buildTargetCalendar([
    assignment('2026-09-30T06:59:59Z', [1, 2]),
    assignment('2026-10-04T06:59:59Z', [2, 3], '256'), // Saturday in the study timezone.
    assignment('2026-10-16T06:59:59Z', [2, 4]),
    assignment(null, [5]),
    assignment('invalid', [6]),
  ], now);
}

test('Sunday–Saturday weeks use the requested labels, include gaps, and mark today independently', () => {
  const c = calendar();
  assert.deepEqual(c.weeks.map(targetWeekLabel), [
    'Week 1 - 9/27-10/03', 'Week 2 - 10/04-10/10', 'Week 3 - 10/11-10/17',
  ]);
  assert.deepEqual(c.weeks.map(week => week.current), [false, false, true]);
  const [first, second] = c.weeks;
  assert.deepEqual(filterScheduledTargets([1, 2, 3, 4, 5], c, selectTargetWeek(c, {}, first.startDay)), [1, 2, 3]);
  assert.deepEqual(filterScheduledTargets([1, 2, 3, 4, 5], c, selectTargetWeek(c, {}, second.startDay)), []);
  assert.equal(targetWeekStart(targetCalendarDay('2026-10-04T07:00:00Z')), second.startDay);
});

test('shared targets can appear in several weeks; ranges deduplicate and exclude unsaved targets', () => {
  const c = calendar(), [first, , last] = c.weeks;
  let selection = selectTargetWeek(c, {}, first.startDay);
  assert.deepEqual(filterScheduledTargets([1, 2, 4], c, selection), [1, 2]);
  selection = selectTargetWeek(c, selection, last.startDay, true);
  assert.deepEqual(filterScheduledTargets([1, 2, 4, 5], c, selection), [1, 2, 4]);
  assert.equal(targetWeekSelectionLabel(c, selection), 'Weeks 1–3 - 9/27-10/17');
  assert.deepEqual(selectTargetWeek(c, selection, c.weeks[1].startDay, true),
    { kind: 'range', start: first.startDay, end: c.weeks[1].startDay, anchor: first.startDay });
});

test('backward ranges retain the original anchor; a plain click resets it', () => {
  const c = calendar(), [first, middle, last] = c.weeks;
  let selection = selectTargetWeek(c, {}, last.startDay);
  selection = selectTargetWeek(c, selection, first.startDay, true);
  assert.equal(selection.anchor, last.startDay);
  selection = selectTargetWeek(c, selection, middle.startDay, true);
  assert.equal(selection.start, middle.startDay); assert.equal(selection.end, last.startDay);
  selection = selectTargetWeek(c, selection, first.startDay);
  assert.equal(selection.anchor, first.startDay); assert.equal(selection.start, selection.end);
});

test('week matching respects the source assignment course even for a topic shared by courses', () => {
  const c = calendar(), selection = selectTargetWeek(c, {}, c.weeks[0].startDay);
  assert.deepEqual(filterScheduledTargets([1, 2, 3], c, selection, new Set(['255'])), [1, 2]);
  assert.deepEqual(filterScheduledTargets([1, 2, 3], c, selection, new Set(['256'])), [2, 3]);
  assert.deepEqual(filterScheduledTargets([1, 2, 3], c, selection, new Set()), []);
});

test('All and Unscheduled preserve manual targets; invalid and missing dates remain unscheduled', () => {
  const c = calendar(), targets = [1, 2, 3, 4, 5, 6, 7];
  assert.deepEqual(filterScheduledTargets(targets, c, { kind: 'all' }), targets);
  assert.deepEqual(filterScheduledTargets(targets, c, { kind: 'unscheduled' }), [5, 6, 7]);
  const undated = buildTargetCalendar([assignment(null, [1, 2])], now);
  assert.equal(undated.weeks.length, 0);
  assert.deepEqual(filterScheduledTargets([1, 2], undated, { kind: 'unscheduled' }), [1, 2]);
});

test('calendar weeks remain seven civil days across DST and year boundaries', () => {
  const c = buildTargetCalendar([
    assignment('2026-11-01T07:00:00Z', [1]),
    assignment('2026-11-08T07:59:59Z', [2]),
    assignment('2026-11-08T08:00:00Z', [3]),
  ], now);
  assert.deepEqual(c.weeks.map(targetWeekLabel), ['Week 1 - 11/01-11/07', 'Week 2 - 11/08-11/14']);
  assert.deepEqual(filterScheduledTargets([1, 2, 3], c, selectTargetWeek(c, {}, c.weeks[0].startDay)), [1, 2]);
  const year = buildTargetCalendar([assignment('2026-12-30T12:00:00Z', [1]), assignment('2027-01-05T12:00:00Z', [2])], now);
  assert.deepEqual(year.weeks.map(targetWeekLabel), ['Week 1 - 12/27-1/02', 'Week 2 - 1/03-1/09']);
});

test('persisted ranges are validated against the installed calendar instead of stale week numbers', () => {
  const c = calendar(), selected = selectTargetWeek(c, {}, c.weeks[0].startDay);
  assert.deepEqual(normalizeTargetWeekSelection(c, JSON.parse(JSON.stringify(selected))), selected);
  for (const invalid of [null, {}, { kind: 'range', start: -1, end: 999999 }, { kind: 'range', start: c.weeks[2].startDay, end: c.weeks[0].startDay }]) {
    assert.deepEqual(normalizeTargetWeekSelection(c, invalid), { kind: 'all' });
  }
});
