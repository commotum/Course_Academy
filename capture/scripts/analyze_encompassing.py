"""Read saved band observations; estimate visible response strength, never exact FIRe.

Run: PYTHONPATH=capture python3 -m scripts.analyze_encompassing --output /tmp/bands
No browser or database calls. Full unchanged-topic observations supply denominators.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys

from .progress import color_observation


def timestamp(value):
    if isinstance(value, (float, int)):
        return float(value)
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()
    return None


def read(path):
    return json.loads(Path(path).read_text())


@lru_cache(maxsize=4)
def snapshot(path):
    data = read(path)
    rows, issues = {}, []
    for course in data.get('courses') or data.get('progress') or []:
        at = timestamp(course.get('captured_at') or course.get('observed_at')
                       or data.get('observed_at') or data.get('finished_at'))
        for topic in course.get('topics', []):
            key = str(course['course_id']), str(topic['topic_id'])
            band = color_observation(topic)['display_band']
            if key in rows:
                issues.append(key)
            rows[key] = (band, at, topic.get('title'))
    for key in issues:
        rows.pop(key, None)
    return rows


def collapse(before, after):
    """Shared topics count once; disagreeing course displays are excluded."""
    groups = defaultdict(list)
    for key in sorted(before.keys() & after.keys()):
        old, new = before[key], after[key]
        if old[0] is not None and new[0] is not None:
            groups[key[1]].append((old[0], new[0], old[1], new[1], key[0]))
    accepted, conflicts = {}, []
    for topic, values in groups.items():
        if len({(v[0], v[1]) for v in values}) > 1:
            conflicts.append(topic)
        else:
            accepted[topic] = (values[0][0], values[0][1],
                               min(v[2] for v in values if v[2] is not None),
                               max(v[3] for v in values if v[3] is not None),
                               [v[4] for v in values])
    return accepted, conflicts


def wilson(success, total):
    if not total:
        return None
    z = 1.96
    p = success / total
    denominator = 1 + z*z / total
    center = (p + z*z/(2*total)) / denominator
    radius = z * ((p*(1-p)/total + z*z/(4*total*total)) ** .5) / denominator
    return [max(0., center-radius), min(1., center+radius)]


def observed_outcome(outcome, completion):
    if outcome in ('passed', 'failed'):
        return outcome
    if isinstance(completion, dict):
        completion = str(completion.get('text') or completion.get('source_text') or '')
    value = str(completion or '').lower()
    if "you've completed the lesson" in value or "you've completed the review" in value:
        return 'passed'
    if 'halted' in value or 'not passed' in value:
        return 'failed'
    return None


def discover(root):
    events = []
    paths = list((root/'reference/mathacademy/question-capture').glob('*/knowledge-state/*-completed.json'))
    paths += list((root/'reference/mathacademy/question-capture-workers').glob('*/*/knowledge-state/*-completed.json'))
    for path in sorted(paths):
        data = read(path)
        state_path = path.parents[1]/'state.json'
        if not state_path.exists():
            continue
        state = read(state_path)
        questions = state.get('questions', {})
        questions = list(questions.values()) if isinstance(questions, dict) else questions
        grades = [q.get('actual_result') or q.get('history', {}).get('result')
                  or q.get('after', {}).get('result') for q in questions]
        account = 'foundations' if 'question-capture-workers' not in path.parts else path.parts[-4]
        events.append(dict(account=account, task_id=str(data['task_id']),
            kind=state.get('task_type'), source=str(state['topic_id']) if state.get('topic_id') else None,
            path=str(path), before_path=state.get('previous_activity_snapshot'),
            time=timestamp(data['started_at']), finished_at=timestamp(data['finished_at']),
            late=bool(data.get('recovered_after_interruption')), grades=grades,
            outcome=observed_outcome(state.get('activity_outcome'), state.get('completion')),
            logged=data.get('changes', []),
            first_answer_at=None, pipeline='legacy', earned_xp=state.get('earned_xp')))
    for path in sorted((root/'reference/mathacademy/capture').glob('*/*/post-activity.json')):
        data = read(path)
        activity = read(path.parent/'activity.json')
        content = read(path.parent/'content.json')
        observation = data.get('observations', {})
        # Persist a reference to the actual saved read, rather than creating a new snapshot.
        courses = observation.get('courses') or observation.get('progress') or []
        comparison = data.get('progress_comparison', {})
        attempts = content.get('attempts', [])
        grades = [a.get('grade') or a.get('last_observation', {}).get('grade') for a in attempts]
        first = [a['started_at'] for a in attempts if isinstance(a.get('started_at'), (int, float))]
        marker = read(path.parent/'capture-complete.json') if (path.parent/'capture-complete.json').exists() else {}
        events.append(dict(account=path.parts[-3], task_id=str(activity['task_id']),
            kind=activity.get('kind'), source=str(activity['topic_id']) if activity.get('topic_id') else None,
            title=activity.get('title'), path=str(path), before_path=str(path.parent/'progress-before.json'),
            time=marker.get('completed_at', observation.get('observed_at')),
            finished_at=max([c.get('captured_at', 0) for c in courses], default=0),
            late=bool(comparison.get('late_read')), grades=grades,
            outcome=observed_outcome(None, content.get('completion')),
            logged=comparison.get('changes', []), first_answer_at=min(first) if first else None,
            pipeline='current', earned_xp=data.get('completion', {}).get('earned_xp')))
    # An account/task is the observational unit, even if both pipelines captured it.
    unique = {}
    for event in events:
        key = event['account'], event['task_id']
        if key not in unique or event['pipeline'] == 'current':
            unique[key] = event
    return sorted(unique.values(), key=lambda e: (e['account'], e['time']))


def distances(origin, adjacency):
    result, queue = {origin: 0}, deque([origin])
    while queue:
        topic = queue.popleft()
        for child in adjacency.get(topic, []):
            if child not in result:
                result[child] = result[topic] + 1
                queue.append(child)
    return result


def load_graph(root, account):
    available = []
    for path in sorted((root/'.local/capture'/account/'context').glob('[0-9]*.json')):
        contents = path.read_bytes()
        context = json.loads(contents)
        if 'graph' in context:
            available.append((context.get('basis', -1), str(path), context, contents))
    if not available:
        return {}, {}, []
    basis, path, context, contents = max(available, key=lambda value: (value[0], value[1]))
    graph = {str(k): [str(v) for v in vs] for k, vs in context['graph'].items()}
    names = {str(t['id']): t['title'] for t in context.get('topics', [])}
    return names, graph, [{'path': path, 'basis': basis,
                          'sha256': hashlib.sha256(contents).hexdigest()}]


def analyze(root, account, events=None):
    events = [e for e in (discover(root) if events is None else events) if e['account'] == account]
    names, graph, graph_sources = load_graph(root, account)
    upstream = defaultdict(set)
    for source, targets in graph.items():
        for target in targets:
            upstream[target].add(source)
    by_account = defaultdict(list)
    for event in events:
        by_account[event['account']].append(event)
    summary = Counter()
    changes, candidates, audit = [], set(), []
    controls = defaultdict(lambda: [0, 0])
    background = defaultdict(lambda: [0, 0])
    passed_controls = defaultdict(lambda: [0, 0])
    passed_background = defaultdict(lambda: [0, 0])
    usable_by_source = defaultdict(list)
    for account, group in by_account.items():
        print(f'Analyzing {account}: {len(group)} saved activities', file=sys.stderr, flush=True)
        times = [e['time'] for e in group]
        for index, event in enumerate(group):
            if event['pipeline'] == 'current':
                observation = read(event['path']).get('observations', {})
                # Reuse the same palette/indexing routine without introducing a saved file.
                current = {}
                for c in observation.get('courses') or observation.get('progress') or []:
                    for t in c.get('topics', []):
                        current[str(c['course_id']), str(t['topic_id'])] = (
                            color_observation(t)['display_band'], timestamp(c.get('captured_at') or event['time']), t.get('title'))
            else:
                current = snapshot(event['path'])
            names.update({key[1]: row[2] for key, row in current.items() if row[2]})
            previous_path = event['before_path']
            previous = snapshot(previous_path) if previous_path and Path(previous_path).is_file() else {}
            summary['activities'] += 1
            summary['logged_course_changes'] += len(event['logged'])
            summary['pipeline_'+event['pipeline']] += 1
            summary['kind_'+str(event['kind'])] += 1
            summary['comparison_available'] += bool(previous)
            mismatch = 0
            for logged in event['logged']:
                key = str(logged['course_id']), str(logged['topic_id'])
                if key in previous and key in current:
                    mismatch += (previous[key][0], current[key][0]) != (logged.get('before_band'), logged.get('after_band'))
                else:
                    summary['logged_missing_topic_pairs'] += 1
            summary['logged_snapshot_mismatches'] += mismatch
            topics, conflicts = collapse(previous, current)
            summary['conflicting_course_topic_observations'] += len(conflicts)
            grades = event['grades']
            perfect = bool(grades) and all(g == 'Correct' for g in grades)
            fully_graded = bool(grades) and all(g in ('Correct', 'Incorrect', 'Skipped Question') for g in grades)
            quality_class = round(5 * grades.count('Correct')/len(grades)) if fully_graded else None
            summary['all_correct_activities'] += perfect
            reasons = []
            if not previous:
                reasons.append('no_baseline')
            if event['late']:
                reasons.append('late_or_recovered')
            if event['kind'] not in ('lesson', 'review') or not event['source']:
                reasons.append('multiple_or_nonpractice_origins')
            # Check time intervals separately for each course-qualified read.
            safe_topics = {}
            for topic, row in topics.items():
                old, new, before_at, after_at, courses = row
                if before_at is None or after_at is None or not 0 < after_at-before_at <= 1800:
                    summary['excluded_stale_or_unordered_topic_intervals'] += 1
                    continue
                intervening = bisect_right(times, after_at) - bisect_right(times, before_at)
                if not before_at < event['time'] <= after_at or intervening != 1:
                    summary['excluded_intervening_activity_topic_intervals'] += 1
                    continue
                if event['first_answer_at'] is not None and before_at >= event['first_answer_at']:
                    summary['excluded_baseline_after_first_answer'] += 1
                    continue
                safe_topics[topic] = (old, new)
            clean = not reasons
            event['topics'] = safe_topics if clean else {}
            event['perfect'] = perfect
            event['clean'] = clean
            event['quality_class'] = quality_class
            event['passed_graded'] = fully_graded and event['outcome'] == 'passed'
            summary['isolated_practice_activities'] += clean and bool(safe_topics)
            summary['isolated_all_correct_activities'] += clean and perfect and bool(safe_topics)
            if clean:
                usable_by_source[event['source']].append(event)
            for topic, row in topics.items():
                old, new = row[:2]
                if old == new:
                    continue
                summary['deduplicated_topic_changes'] += 1
                summary['rising_topic_changes' if new > old else 'falling_topic_changes'] += 1
                isolated = clean and topic in safe_topics
                changes.append(dict(account=account, task_id=event['task_id'], source=event['source'],
                    target=topic, before=old, after=new, courses=row[4],
                    isolated=isolated, all_correct=perfect, kind=event['kind'],
                    snapshot=event['path']))
                if isolated and new > old and topic != event['source']:
                    candidates.add((event['source'], topic))
            if clean and perfect:
                for topic, (old, new) in safe_topics.items():
                    if not 1 <= old <= 5:
                        continue  # admission and saturation are separate observations
                    if topic == event['source']:
                        if event['kind'] == 'review':
                            control = controls[account, old]
                            control[0] += new > old
                            control[1] += 1
                    else:
                        bg = background[account, topic, old]
                        bg[0] += new > old
                        bg[1] += 1
            if clean and event['passed_graded']:
                for topic, (old, new) in safe_topics.items():
                    if not 1 <= old <= 5:
                        continue
                    if topic == event['source']:
                        if event['kind'] == 'review':
                            control = passed_controls[old, quality_class]
                            control[0] += new > old
                            control[1] += 1
                    else:
                        bg = passed_background[topic, old, quality_class]
                        bg[0] += new > old
                        bg[1] += 1
            audit.append({k: event[k] for k in ['account', 'task_id', 'source', 'kind', 'pipeline', 'path', 'perfect', 'outcome', 'earned_xp']}
                         | {'exclusion_reasons': reasons, 'isolated_topics': len(safe_topics),
                            'course_conflicts': conflicts, 'grades': dict(Counter(str(g) for g in grades)),
                            'time': event['time'], 'finished_at': event['finished_at']})
    pairs = []
    upstream_distances, downstream_distances = {}, {}
    for source, target in sorted(candidates):
        exposures, positives, unobservable, eligible, passed_exposures = [], [], 0, [], []
        for event in usable_by_source[source]:
            row = event['topics'].get(target)
            if row is None:
                continue
            old, new = row
            if new > old:
                positives.append(event)
            if event['passed_graded'] and 1 <= old <= 5:
                quality_class = event['quality_class']
                bg_up, bg_n = passed_background[target, old, quality_class]
                same_source = [e for e in usable_by_source[source]
                    if e['passed_graded'] and e['quality_class'] == quality_class
                    and e['topics'].get(target, (None,))[0] == old]
                bg_up -= sum(e['topics'][target][1] > old for e in same_source)
                bg_n -= len(same_source)
                direct_up, direct_n = passed_controls[old, quality_class]
                passed_exposures.append(dict(task_id=event['task_id'], kind=event['kind'],
                    before=old, after=new, quality_class=quality_class, snapshot=event['path'],
                    background_n=bg_n, background_up_rate=(bg_up+.5)/(bg_n+1) if bg_n else 0.,
                    direct_control_n=direct_n,
                    direct_control_up_rate=(direct_up+.5)/(direct_n+1) if direct_n else None))
            if not event['perfect']:
                continue
            if not 1 <= old <= 5:
                unobservable += 1
                continue
            eligible.append(event)
            up = new > old
            bg_up, bg_n = background[event['account'], target, old]
            # Remove this source's exposures from the target-specific background.
            same_source = [e for e in usable_by_source[source]
                           if e['perfect'] and e['account'] == event['account']
                           and e['topics'].get(target, (None,))[0] == old]
            bg_up -= sum(e['topics'][target][1] > old for e in same_source)
            bg_n -= len(same_source)
            bg_rate = (bg_up + 0.5)/(bg_n + 1) if bg_n else 0.0
            direct_up, direct_n = controls[event['account'], old]
            direct_rate = (direct_up + 0.5)/(direct_n + 1) if direct_n else None
            exposures.append(dict(account=event['account'], task_id=event['task_id'],
                before=old, after=new, snapshot=event['path'], background_n=bg_n,
                background_up_rate=bg_rate, direct_control_n=direct_n,
                direct_control_up_rate=direct_rate))
        n = len(exposures)
        up = sum(e['after'] > e['before'] for e in exposures)
        supported = [e for e in exposures if e['direct_control_n'] >= 3 and e['background_n'] >= 3]
        proxy = None
        if supported:
            # Shrink towards no excess effect with four pseudo-observations.
            excess = sum(float(e['after'] > e['before']) - e['background_up_rate'] for e in supported)/(len(supported)+4)
            reference = sum(e['direct_control_up_rate']-e['background_up_rate'] for e in supported)/len(supported)
            if reference > 0:
                proxy = max(0., min(1., excess/reference))
        passed_supported = [e for e in passed_exposures if e['background_n'] >= 3 and e['direct_control_n'] >= 3]
        passed_proxy = None
        if passed_supported:
            excess = sum(float(e['after'] > e['before'])-e['background_up_rate'] for e in passed_supported)/(len(passed_supported)+4)
            reference = sum(e['direct_control_up_rate']-e['background_up_rate'] for e in passed_supported)/len(passed_supported)
            if reference > 0:
                passed_proxy = max(0., min(1., excess/reference))
        if source not in upstream_distances:
            upstream_distances[source] = distances(source, upstream)
            downstream_distances[source] = distances(source, graph)
        up_dist = upstream_distances[source]
        down_dist = downstream_distances[source]
        relation = 'prerequisite' if target in up_dist else 'downstream' if target in down_dist else 'other_or_disconnected'
        pairs.append(dict(account=account, source=source, source_title=names.get(source), target=target,
            target_title=names.get(target), graph_relation=relation,
            prerequisite_distance=up_dist.get(target), downstream_distance=down_dist.get(target),
            isolated_positive_events=len(positives), positive_accounts=sorted({e['account'] for e in positives}),
            perfect_unsaturated_exposures=n, perfect_unsaturated_rises=up,
            crossing_probability_interval=wilson(up, n), capped_or_unlearned_exposures=unobservable,
            control_supported_exposures=len(supported), response_strength_proxy=proxy,
            confidence='repeated' if up >= 3 else 'limited',
            passed_unsaturated_exposures=len(passed_exposures),
            passed_unsaturated_rises=sum(e['after'] > e['before'] for e in passed_exposures),
            passed_control_supported_exposures=len(passed_supported),
            passed_response_strength_proxy=passed_proxy,
            positive_tasks=[{'account': e['account'], 'task_id': e['task_id'], 'perfect': e['perfect'], 'snapshot': e['path']} for e in positives],
            exposures=exposures, passed_exposures=passed_exposures))
    pairs.sort(key=lambda p: (-p['perfect_unsaturated_rises'], -len(p['positive_accounts']), -p['isolated_positive_events'], p['source'], p['target']))
    summary['candidate_effective_pairs'] = len(pairs)
    summary['repeated_all_correct_pairs'] = sum(p['perfect_unsaturated_rises'] >= 3 for p in pairs)
    summary['control_supported_pairs'] = sum(p['response_strength_proxy'] is not None for p in pairs)
    summary['repeated_passed_pairs'] = sum(p['passed_unsaturated_rises'] >= 3 for p in pairs)
    source_manifest = [{'account': e['account'], 'task_id': e['task_id'], 'path': e['path'], 'before_path': e['before_path']} for e in events]
    return dict(account=account, created_at=datetime.now(timezone.utc).isoformat(), summary=dict(summary),
        methods={'unit': 'account/task/topic; cross-course duplicates count once',
                 'maximum_interval_seconds': 1800,
                 'all_correct': 'every saved presentation has observed Correct grade, not intended answer or XP',
                 'estimand': 'background-adjusted, shrunken band-crossing response relative to pooled same-account/band direct all-correct reviews; NOT identified encompassing coverage',
                 'shrinkage_pseudo_observations': 4,
                 'controls_minimum': 3,
                 'passed_estimand': 'same-account mixed-outcome sensitivity estimate; matched to before-band and rounded accuracy class, normalized against direct passed reviews; NOT identified coverage',
                 'limitations': ['Display thresholds are unknown and darkest band is right-censored.',
                     'Legacy timing uses snapshot collection start as a completion proxy.',
                     'No control for unseen external work, target ability, early discount, or initial placement.',
                     'Candidate selection uses observed rises; crossing intervals are descriptive, not selection-adjusted weight uncertainty.',
                     'Effective pair effects can arise through transitive encompassing paths.',
                     'Mixed-outcome rises identify candidates but do not enter response-strength estimates.',
                     'Bot timing and accuracy are not human learner estimates.']},
        graph_sources=graph_sources, direct_controls=[dict(account=k[0], before_band=k[1], rises=v[0], n=v[1], interval=wilson(*v)) for k,v in sorted(controls.items())],
        passed_direct_controls=[dict(before_band=k[0], quality_class=k[1], rises=v[0], n=v[1], interval=wilson(*v)) for k,v in sorted(passed_controls.items())],
        pairs=pairs, changes=changes, activity_audit=audit, sources=source_manifest,
        manifest_sha256=hashlib.sha256(json.dumps(source_manifest, sort_keys=True).encode()).hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--account', choices=['foundations', 'linear', 'multivariable', 'differential'])
    parser.add_argument('--output', type=Path, required=True, help='Directory for separate account reports')
    args = parser.parse_args()
    events = discover(args.root.resolve())
    args.output.mkdir(parents=True, exist_ok=True)
    accounts = [args.account] if args.account else ['foundations', 'linear', 'multivariable', 'differential']
    for account in accounts:
        result = analyze(args.root.resolve(), account, events)
        (args.output/(account+'.json')).write_text(json.dumps(result, indent=2)+'\n')
        print(json.dumps({'account': account, 'summary': result['summary']}, indent=2), flush=True)


if __name__ == '__main__':
    main()
