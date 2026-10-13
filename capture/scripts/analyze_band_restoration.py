"""Audit persistence and previous high bands using account-local frozen captures.

Run: PYTHONPATH=capture python3 -m scripts.analyze_band_restoration REPORT_FOLDER
Only reads paths present in the frozen source manifest. Course IDs remain separate.
"""
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import lru_cache
import argparse
import hashlib
import json
from pathlib import Path

from .analyze_encompassing import timestamp, collapse
from .progress import color_observation

ACCOUNTS = ('foundations', 'linear', 'multivariable', 'differential')


def iso(value):
    return datetime.fromtimestamp(value, timezone.utc).isoformat() if value is not None else None


def compact_snapshot(path, interests):
    data = json.loads(Path(path).read_text())
    observation = data.get('observations', data)
    result = {}
    conflicts = set()
    for course in observation.get('courses') or observation.get('progress') or []:
        at = timestamp(course.get('captured_at') or course.get('observed_at')
                       or observation.get('observed_at') or data.get('finished_at'))
        if at is None:
            continue
        for topic in course.get('topics', []):
            target = str(topic['topic_id'])
            if interests is not None and target not in interests:
                continue
            band = color_observation(topic)['display_band']
            if band is None:
                continue
            key = str(course['course_id']), target
            row = at, band, topic.get('title')
            if key in result and result[key] != row:
                conflicts.add(key)
            result[key] = row
    for key in conflicts:
        result.pop(key)
    return result


def common_scope(source, assessment_topics):
    """All-topic paired observations, with equal isolation rules for task types."""
    audits = {str(r['task_id']): r for r in source['activity_audit']}
    times = sorted(r['time'] for r in source['activity_audit'])
    diagnostics = sorted((r.get('finished_at') or r['time'], r['time']) for r in source['activity_audit'] if r['kind'] == 'diagnostic')
    groups = defaultdict(lambda: dict(n=0, activities=set(), large_tasks=set(),
        deltas=Counter(), one_to_six=0, grades=Counter()))
    large = []
    skipped = Counter()
    initialization = defaultdict(Counter)
    @lru_cache(maxsize=4)
    def snapshot(path):
        raw = compact_snapshot(path, None)
        return {key:(v[1],v[0],v[2]) for key,v in raw.items()}
    for source_row in source['sources']:
        audit = audits[str(source_row['task_id'])]
        kind = audit['kind']
        if kind not in ('lesson','review','assessment','multistep'):
            continue
        if not source_row.get('before_path') or not Path(source_row['before_path']).is_file():
            skipped['missing_baseline'] += 1
            continue
        if 'late_or_recovered' in audit['exclusion_reasons']:
            skipped['late_or_recovered'] += 1
            continue
        before, after = snapshot(source_row['before_path']), snapshot(source_row['path'])
        paired, conflicts = collapse(before, after)
        skipped['course_conflicting_topics'] += len(conflicts)
        grades = audit['grades']
        grade_n = sum(grades.values())
        correct = grades.get('Correct', 0)
        accuracy = correct/grade_n if grade_n and set(grades) <= {'Correct','Incorrect','Skipped Question'} else None
        task = str(audit['task_id'])
        assessment = assessment_topics.get(task, {})
        direct_topics = set(assessment.get('topics', [])) if kind in ('assessment','multistep') else {audit['source']}
        latest_diagnostic = max((d for d in diagnostics if d[0] < audit['time']), default=None)
        source_bands = {value[0] for (course, topic),value in before.items() if topic == audit['source']}
        practiced_before = bool(latest_diagnostic) and any(r['source'] == audit['source']
            and r['kind'] in ('lesson','review') and r['outcome'] == 'passed'
            and (r.get('finished_at') or r['time']) < latest_diagnostic[1] for r in source['activity_audit'])
        lesson_regime = 'source_white_relearning_after_diagnostic' if practiced_before and source_bands == {0} else 'other'
        first_answer = None
        if audit['pipeline'] == 'current':
            content_path = Path(source_row['path']).parent/'content.json'
            if content_path.is_file():
                content = json.loads(content_path.read_text())
                first_answer = min((a['started_at'] for a in content.get('attempts', [])
                                    if isinstance(a.get('started_at'), (int,float))), default=None)
        for target, (old, new, start, end, courses) in paired.items():
            initial_lesson = kind == 'lesson' and target in direct_topics and old == 0
            if not 1 <= old <= 5 and not initial_lesson:
                continue
            if not 0 < end-start <= 1800 or not start < audit['time'] <= end or bisect_right(times,end)-bisect_right(times,start) != 1:
                skipped['nonisolated_topic_intervals'] += 1
                continue
            if first_answer is not None and start >= first_answer:
                skipped['baseline_after_first_answer'] += 1
                continue
            if initial_lesson:
                for label in ('all', f'outcome:{audit["outcome"]}', f'pipeline:{audit["pipeline"]}', f'regime:{lesson_regime}'):
                    initialization[label][str(new)] += 1
                continue
            direct = target in direct_topics
            target_grades = Counter(q['grade'] for q in assessment.get('questions', []) if q['topic'] == target)
            delta = new-old
            labels = [f'kind:{kind}', f'kind_accuracy:{kind}:{accuracy}', f'kind_before:{kind}:{old}',
                      f'kind_pipeline:{kind}:{audit["pipeline"]}', f'kind_outcome:{kind}:{audit["outcome"]}']
            if kind == 'lesson':
                labels += [f'lesson_regime:{lesson_regime}']
            if direct:
                labels += [f'direct_kind:{kind}', f'direct_kind_accuracy:{kind}:{accuracy}', f'direct_kind_before:{kind}:{old}']
                if target_grades:
                    labels += [f'direct_assessed_correctness:{kind}:'+('all_correct' if set(target_grades)=={'Correct'} else 'some_incorrect_or_missing')]
            for label in labels:
                item = groups[label]
                item['n'] += 1
                item['activities'].add(task)
                item['deltas'][delta] += 1
                item['one_to_six'] += old == 1 and new == 6
                item['grades'].update(target_grades)
                if delta >= 2:
                    item['large_tasks'].add(task)
            if delta >= 2:
                large.append(dict(account=source['account'], task_id=task, source=audit['source'],
                    target=target,before=old,after=new,delta=delta,kind=kind,pipeline=audit['pipeline'],
                    direct=direct,accuracy=accuracy,at=iso(end),target_question_grades=dict(target_grades),
                    common_scope_courses=courses))
    result = {}
    for label, item in groups.items():
        delta = item['deltas']
        result[label] = dict(topic_opportunities=item['n'], activities_eligible=len(item['activities']),
            activities_with_large_jump=len(item['large_tasks']), large_jump_targets=sum(n for d,n in delta.items() if d >= 2),
            falls=sum(n for d,n in delta.items() if d < 0), rises=sum(n for d,n in delta.items() if d > 0),
            one_to_six=item['one_to_six'], signed_delta_counts=dict(sorted(delta.items())),
            assessed_target_question_grades=dict(item['grades']))
    return dict(groups=result, exclusions=dict(skipped),
        direct_lesson_initialization={key:dict(activities=sum(counts.values()), after_band_counts=dict(counts)) for key,counts in initialization.items()},
        method='All-topic common scope: same course-ID/topic pairs, agreeing repeated-course displays collapsed once, before bands 1–5, intervals at most 30 minutes with exactly one captured activity and the candidate event inside the interval. Current baselines precede the first answer. Outcomes and grading do not select tasks; completed assessment observations are included even without a task pass/fail label.'), large


def previous_peak(rows, cutoff):
    eligible = [r for r in rows if r[0] <= cutoff]
    if not eligible:
        return None
    peak = max(eligible, key=lambda r: (r[1], r[0]))
    return {'band': peak[1], 'at': iso(peak[0]), 'path': peak[2]}


def followup(rows, after_at, before, after, next_diagnostic):
    horizon = after_at + 6 * 3600
    stop = min(horizon, next_diagnostic) if next_diagnostic is not None else horizon
    future = [r for r in rows if after_at < r[0] < (next_diagnostic or float('inf'))]
    window = [r for r in future if r[0] <= stop]
    reversals = [r for r in window if r[1] <= before]
    declines = [r for r in window if r[1] < after]
    coverage_1h = bool(window) and any(1 <= (r[0]-after_at)/3600 <= 2 for r in future)
    coverage_6h = bool(window) and any(6 <= (r[0]-after_at)/3600 <= 7 for r in future)
    boundary = next((r for r in future if 6 <= (r[0]-after_at)/3600 <= 7), None)
    confirmed_window = [r for r in future if boundary and r[0] <= boundary[0]]
    first = reversals[0] if reversals else None
    return dict(window_hours=6, observations=len(window),
                last_observed_at=iso(window[-1][0]) if window else None,
                last_observed_after_hours=(window[-1][0]-after_at)/3600 if window else None,
                minimum_band=min([after]+[r[1] for r in window]),
                endpoint_never_fell=not declines,
                retained_some_gain=not reversals,
                confirmed_endpoint_through_6h=coverage_6h and all(r[1] >= after for r in confirmed_window),
                confirmed_some_gain_through_6h=coverage_6h and all(r[1] > before for r in confirmed_window),
                six_hour_boundary_read=dict(at=iso(boundary[0]), band=boundary[1], path=boundary[2]) if boundary else None,
                first_return_to_baseline=dict(at=iso(first[0]), band=first[1],
                    hours=(first[0]-after_at)/3600, path=first[2]) if first else None,
                same_course_coverage_1h=coverage_1h,
                same_course_coverage_6h=coverage_6h,
                right_censored_6h=not coverage_6h,
                censor_reason=('next_diagnostic' if next_diagnostic is not None
                    and next_diagnostic < horizon else 'no_later_same_course_capture')
                    if not coverage_6h else None,
                next_diagnostic_at=iso(next_diagnostic),
                coverage_note='Coverage flags require an actual within-window read and a same-course boundary read from the horizon to one hour afterward, before the next diagnostic. Changes between reads are unobserved.')


def summarize(events):
    contexts = [c for event in events for c in event['contexts']]
    return dict(target_events=len(events), activities=len({r['task_id'] for r in events}),
        course_contexts=len(contexts),
        activities_after_any_captured_diagnostic=len({r['task_id'] for r in events if r['latest_diagnostic']}),
        target_events_with_pre_diagnostic_source_practice=sum(r['source_practiced_before_latest_diagnostic'] for r in events),
        target_events_with_same_course_previous_high=sum(any(c['same_course_restoration'] for c in r['contexts']) for r in events),
        target_events_with_same_course_pre_diagnostic_high=sum(any(c['same_course_pre_diagnostic_restoration'] for c in r['contexts']) for r in events),
        target_events_with_other_course_pre_diagnostic_high=sum(any(c['other_course_pre_diagnostic_restoration'] for c in r['contexts']) for r in events),
        target_events_returning_to_baseline_within_6h=sum(any(c['followup']['first_return_to_baseline'] for c in r['contexts']) for r in events),
        target_events_with_1h_followup=sum(any(c['followup']['same_course_coverage_1h'] for c in r['contexts']) for r in events),
        target_events_with_6h_followup=sum(any(c['followup']['same_course_coverage_6h'] for c in r['contexts']) for r in events),
        target_events_retaining_endpoint_with_6h_followup=sum(any(c['followup']['confirmed_endpoint_through_6h'] for c in r['contexts']) for r in events),
        target_events_retaining_some_gain_with_6h_followup=sum(any(c['followup']['confirmed_some_gain_through_6h'] for c in r['contexts']) for r in events),
        source_white_relearning_after_diagnostic=sum(any(c['source_white_relearning_after_diagnostic'] for c in r['contexts']) for r in events),
        direct_target_events=sum(r['direct'] for r in events),
        delta_counts=dict(Counter(str(r['delta']) for r in events)))


def analyze(folder, account):
    source_path = folder/f'{account}.json'
    timing_path = folder/'timing-magnitude'/f'{account}.json'
    source_bytes, timing_bytes = source_path.read_bytes(), timing_path.read_bytes()
    source, timing = json.loads(source_bytes), json.loads(timing_bytes)
    assert source['account'] == account and timing['account'] == account
    original = [dict(r, panels=['timing_prerequisite']) for r in timing['observations'] if r['delta'] >= 2]
    assessment_path = folder/'restoration-analysis/assessment-topics.json'
    assessment_topics = json.loads(assessment_path.read_text())['accounts'][account] if assessment_path.is_file() else {}
    comparison, common_large = common_scope(source, assessment_topics)
    combined = {(r['task_id'],r['target']):r for r in original}
    for row in common_large:
        key = row['task_id'],row['target']
        if key in combined:
            combined[key]['panels'].append('common_scope')
            combined[key]['target_question_grades'] = row['target_question_grades']
        else:
            combined[key] = dict(row, panels=['common_scope'])
    selected = list(combined.values())
    print(f'{account}: common-scope comparison complete, {len(common_large)} large target jumps', flush=True)
    assert all(r['account'] == account for r in selected)
    sources = {str(r['task_id']): r for r in source['sources']}
    audits = {str(r['task_id']): r for r in source['activity_audit']}
    diagnostics = []
    diagnostic_boundary_sources = {}
    for r in source['activity_audit']:
        if r['kind'] != 'diagnostic':
            continue
        boundary, boundary_source = r['time'], 'diagnostic_completion_capture_start; actual start unavailable'
        if r['pipeline'] == 'current':
            content = json.loads((Path(r['path']).parent/'content.json').read_text())
            starts = [a['started_at'] for a in content.get('attempts', []) if isinstance(a.get('started_at'),(int,float))]
            if starts:
                boundary, boundary_source = min(starts), 'first_captured_diagnostic_question_started_at'
        diagnostics.append((r.get('finished_at') or r['time'], str(r['task_id']), boundary))
        diagnostic_boundary_sources[str(r['task_id'])] = boundary_source
    diagnostics.sort()
    diagnostic_times = [r[0] for r in diagnostics]
    interests = {r[k] for r in selected for k in ('source', 'target')}
    required = {s[k] for r in selected for s in [sources[r['task_id']]]
                for k in ('path', 'before_path') if s.get(k)}
    paths = sorted({s[k] for s in source['sources'] for k in ('path', 'before_path') if s.get(k)})
    timeline = defaultdict(dict)
    snapshots, missing = {}, []
    for index, path in enumerate(paths):
        if not Path(path).is_file():
            missing.append(path)
            continue
        snapshot = compact_snapshot(path, interests)
        if path in required:
            snapshots[path] = snapshot
        for key, (at, band, title) in snapshot.items():
            # Baselines frequently re-store exactly the same already-read page.
            timeline[key].setdefault((at, band), path)
        if index and index % 250 == 0:
            print(f'{account}: parsed {index}/{len(paths)} frozen files', flush=True)
    conflicts = 0
    for key, values in timeline.items():
        bands_at = defaultdict(set)
        for at, band in values:
            bands_at[at].add(band)
        conflicts += sum(len(bands)>1 for bands in bands_at.values())
        timeline[key] = sorted((at, band, path) for (at, band), path in values.items() if len(bands_at[at]) == 1)
    by_topic = defaultdict(list)
    for (course, target), rows in timeline.items():
        by_topic[target].append((course, rows))
    batches = {str(r['task_id']): r for r in timing['activity_batches']}
    jumps_by_task = Counter(r['task_id'] for r in selected)
    events, missing_contexts = [], []
    for row in selected:
        task = row['task_id']
        src = sources[task]
        before, after = snapshots.get(src['before_path'], {}), snapshots.get(src['path'], {})
        matches = [key for key in before.keys() & after.keys()
                   if key[1] == row['target'] and before[key][1] == row['before']
                   and after[key][1] == row['after']]
        if not matches:
            missing_contexts.append(dict(task_id=task, target=row['target']))
        event = {key: row[key] for key in ('account', 'task_id', 'source', 'target', 'kind', 'pipeline', 'before', 'after', 'delta', 'direct', 'accuracy')}
        event['panels'] = row['panels']
        event['target_question_grades'] = row.get('target_question_grades', {})
        at = min((after[k][0] for k in matches), default=timestamp(row['at']))
        di = bisect_left(diagnostic_times, at)-1
        latest = diagnostics[di] if di >= 0 else None
        next_diag = diagnostics[di+1][2] if di+1 < len(diagnostics) else None
        practiced = [r for r in source['activity_audit'] if latest and r['source'] == row['source']
                     and r['kind'] in ('lesson', 'review') and r['outcome'] == 'passed'
                     and (r.get('finished_at') or r['time']) < latest[2]]
        event.update(at=iso(at), before_path=src['before_path'], after_path=src['path'],
            latest_diagnostic=dict(task_id=latest[1], at=iso(latest[0])) if latest else None,
            source_practiced_before_latest_diagnostic=bool(practiced),
            prior_successful_source_tasks=[r['task_id'] for r in practiced],
            activity_batch=batches.get(task), large_jump_targets_in_activity=jumps_by_task[task], contexts=[])
        for key in sorted(matches):
            course, target = key
            before_at, before_band, title = before[key]
            after_at, after_band, _ = after[key]
            rows = timeline[key]
            peak = previous_peak(rows, before_at)
            diag_peak = previous_peak(rows, latest[2]) if latest else None
            other_peaks = [dict(course_id=c, **p) for c, values in by_topic[target]
                           if latest and c != course and (p := previous_peak(values, latest[2]))]
            other_peak = max(other_peaks, key=lambda p: p['band']) if other_peaks else None
            def restored(p):
                return bool(p and p['band'] >= 4 and before_band <= 2 and after_band >= p['band']-1)
            source_before = before.get((course, row['source']))
            source_contexts = [dict(course_id=c, band=value[1], at=iso(value[0])) for (c,t),value in before.items() if t == row['source']]
            consistent_source_band = source_contexts[0]['band'] if source_contexts and len({v['band'] for v in source_contexts}) == 1 else None
            event['contexts'].append(dict(course_id=course, target_title=title,
                before_at=iso(before_at), after_at=iso(after_at),
                previous_same_course_peak=peak,
                pre_diagnostic_same_course_peak=diag_peak,
                pre_diagnostic_other_course_peak=other_peak,
                same_course_restoration=restored(peak),
                same_course_pre_diagnostic_restoration=restored(diag_peak),
                other_course_pre_diagnostic_restoration=restored(other_peak),
                exact_same_course_peak_match=bool(peak and after_band == peak['band']),
                source_before_band=source_before[1] if source_before else None,
                source_before_course_contexts=source_contexts,
                consistent_source_before_band=consistent_source_band,
                source_white_relearning_after_diagnostic=bool(row['kind'] == 'lesson' and practiced and consistent_source_band == 0),
                followup=followup(rows, after_at, before_band, after_band, next_diag)))
        events.append(event)
    result = dict(account=account, generated_at=datetime.now(timezone.utc).isoformat(),
        source_report=str(source_path), source_report_sha256=hashlib.sha256(source_bytes).hexdigest(),
        timing_report=str(timing_path), timing_report_sha256=hashlib.sha256(timing_bytes).hexdigest(),
        method=dict(eligibility='Union of original timing prerequisite panel (passed, fully graded) and common all-topic panel (all outcomes and activity types except diagnostics), ordinal delta >=2. Each event lists its panels.',
            identity='Account and course and topic; one row event can have multiple separately assessed course contexts.',
            restoration='Previous peak >=4, before <=2, after >= previous peak minus 1; exact equality is also recorded. Other-course history is reported separately and never substituted for same-course state.',
            followup='Unique (course, capture timestamp, topic, band) observations for six hours after the jump, stopping at the next captured diagnostic. No duplicate baseline reads count twice.',
            scope='Previously frozen file manifest only; no future or uncaptured events are inferred.',
            script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            assessment_topics_sha256=hashlib.sha256(assessment_path.read_bytes()).hexdigest() if assessment_path.is_file() else None,
            sources_parsed=len(paths)-len(missing), unique_course_topic_reads=sum(len(v) for v in timeline.values()),
            conflicting_same_time_topic_reads_quarantined=conflicts,
            missing_paths=missing, unmatched_events=missing_contexts),
        diagnostics=[dict(task_id=d[1], boundary_at=iso(d[2]), boundary_source=diagnostic_boundary_sources[d[1]], finished_at=iso(d[0])) for d in diagnostics],
        summary=summarize([r for r in events if 'timing_prerequisite' in r['panels']]),
        by_kind={kind:summarize([r for r in events if r['kind'] == kind and 'timing_prerequisite' in r['panels']]) for kind in ('review','lesson')},
        activity_type_comparison=comparison,
        common_scope_persistence={kind:summarize([r for r in events if r['kind'] == kind and 'common_scope' in r['panels']]) for kind in ('review','lesson','assessment','multistep')},
        events=events)
    target = folder/'restoration-analysis'/f'{account}-patterns.json'
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(account=account, summary=result['summary'], by_kind=result['by_kind'])), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', type=Path)
    parser.add_argument('--accounts', nargs='+', choices=ACCOUNTS, default=ACCOUNTS)
    args = parser.parse_args()
    for account in args.accounts:
        analyze(args.folder, account)


if __name__ == '__main__':
    main()
