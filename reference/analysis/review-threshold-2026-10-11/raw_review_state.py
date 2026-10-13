"""Recheck frozen raw progress captures for review state and intervening credit.

Run from the repository root with Python 3. Reads captures only; writes this
analysis folder. A visible implicit rise is a lower bound on implicit practice:
fractional credit may remain inside a band and therefore be invisible.
"""
from bisect import bisect_right
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import statistics
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'capture'))
from scripts.analyze_encompassing import collapse, timestamp
from scripts.progress import color_observation

HERE = Path(__file__).resolve().parent
FROZEN = ROOT / 'reference/mathacademy/encompassing-analysis-2026-10-11'
ACCOUNTS = ('foundations', 'linear', 'multivariable', 'differential')


@lru_cache(maxsize=6)
def snapshot(path):
    data = json.loads(Path(path).read_text())
    data = data.get('observations', data)
    rows, duplicates = {}, set()
    for course in data.get('courses') or data.get('progress') or []:
        at = timestamp(course.get('captured_at') or course.get('observed_at')
                       or data.get('observed_at') or data.get('finished_at'))
        for topic in course.get('topics', []):
            key = str(course['course_id']), str(topic['topic_id'])
            if key in rows:
                duplicates.add(key)
            rows[key] = color_observation(topic)['display_band'], at, topic.get('title')
    for key in duplicates:
        rows.pop(key)
    return rows


def stats(rows):
    ages = [r['hours_since_passed_direct'] for r in rows
            if r['hours_since_passed_direct'] is not None]
    return dict(n=len(rows), starting_bands=dict(sorted(Counter(r['before'] for r in rows).items())),
                rises=sum(r['after'] > r['before'] for r in rows),
                falls=sum(r['after'] < r['before'] for r in rows),
                flat=sum(r['after'] == r['before'] for r in rows), known_direct_age=len(ages),
                median_direct_age_hours=statistics.median(ages) if ages else None,
                visible_intervening_implicit_rises=sum(bool(r['intervening_implicit_rises']) for r in rows))


def analyze(account):
    path = FROZEN / f'{account}.json'
    raw = path.read_bytes()
    frozen = json.loads(raw)
    audits = sorted(frozen['activity_audit'], key=lambda a: a['time'])
    timing_path = FROZEN / f'timing-magnitude/{account}.json'
    timing_raw = timing_path.read_bytes()
    old = json.loads(timing_raw)
    assert old['source_report_sha256'] == hashlib.sha256(raw).hexdigest()
    # The live account graph-cache path has since changed. Preserve the graph
    # qualification recorded by the frozen timing audit instead of rereading it.
    qualified_implicit = {(r['task_id'], r['target']) for r in old['observations'] if not r['direct']}
    sources = {s['task_id']: s for s in frozen['sources']}
    times = [a['time'] for a in audits]
    direct, implicit = {}, defaultdict(list)
    rows, exclusions = [], Counter()
    for event in audits:
        source = event['source']
        grades = event['grades']
        passed = event['outcome'] == 'passed' and bool(grades) and set(grades) <= {
            'Correct', 'Incorrect', 'Skipped Question'}
        pair = sources[event['task_id']]
        old_path = pair['before_path']
        observed = {}
        if old_path and Path(old_path).is_file():
            observed, _ = collapse(snapshot(old_path), snapshot(event['path']))
        first_answer = None
        if event['pipeline'] == 'current':
            content = json.loads((Path(event['path']).parent / 'content.json').read_text())
            starts = [a['started_at'] for a in content.get('attempts', [])
                      if isinstance(a.get('started_at'), (int, float))]
            first_answer = min(starts) if starts else None
        safe = {}
        if not event['exclusion_reasons'] and passed:
            for target, values in observed.items():
                before, after, start, end, courses = values
                if (0 < end-start <= 1800 and start < event['time'] <= end
                        and bisect_right(times, end)-bisect_right(times, start) == 1
                        and (first_answer is None or start < first_answer)):
                    safe[target] = values
        if event['kind'] == 'review':
            if source in safe:
                before, after, start, end, courses = safe[source]
                previous = direct.get(source)
                intervening = [r for r in implicit[source]
                               if previous and r['event_time'] > previous['time']]
                rows.append(dict(account=account, task_id=event['task_id'], topic=source,
                    at=datetime.fromtimestamp(event['time'], timezone.utc).isoformat(),
                    before=before, after=after, courses=courses,
                    accuracy=grades.get('Correct', 0)/sum(grades.values()),
                    previous_direct_task=previous['task_id'] if previous else None,
                    previous_direct_kind=previous['kind'] if previous else None,
                    previous_direct_post_band=previous['post_band'] if previous else None,
                    hours_since_passed_direct=(event['time']-previous['time'])/3600 if previous else None,
                    intervening_implicit_rises=intervening,
                    evidence=event['path'], baseline=old_path))
            else:
                for reason in event['exclusion_reasons'] or ['no_isolated_source_pair_or_not_passed']:
                    exclusions[reason] += 1
        for target, (before, after, start, end, courses) in safe.items():
            if (event['task_id'], target) in qualified_implicit and after > before:
                implicit[target].append(dict(task_id=event['task_id'], source_topic=source,
                    before=before, after=after, event_time=event['time'], evidence=event['path']))
        if source and passed and event['kind'] in ('lesson', 'review'):
            direct[source] = dict(task_id=event['task_id'], kind=event['kind'], time=event['time'],
                                  post_band=observed.get(source, (None, None))[1])
    expected = {r['task_id']: (r['before'], r['after']) for r in old['observations']
                if r['direct'] and r['kind'] == 'review'}
    got = {r['task_id']: (r['before'], r['after']) for r in rows if 1 <= r['before'] <= 5}
    assert got == expected, (account, set(got)^set(expected))
    controls = [r for r in rows if r['before'] == 1 and r['accuracy'] == .6]
    bins = {}
    for lo, hi in [(0,6),(6,12),(12,24),(24,48),(48,float('inf'))]:
        selected = [r for r in controls if r['hours_since_passed_direct'] is not None
                    and lo <= r['hours_since_passed_direct'] < hi]
        bins[f'{lo}-{hi}h'] = stats(selected)
    return dict(account=account, frozen_manifest_sha256=hashlib.sha256(raw).hexdigest(),
        frozen_timing_sha256=hashlib.sha256(timing_raw).hexdigest(),
        audited_activities=len(audits), captured_reviews=sum(a['kind']=='review' for a in audits),
        raw_pair_verification='All old band-1–5 direct-review pairs exactly reproduced from raw captures.',
        all_bands=stats(rows), band6=stats([r for r in rows if r['before']==6]),
        known_age_with_visible_implicit_credit=stats([r for r in rows if r['intervening_implicit_rises']]),
        known_age_without_visible_implicit_rise=stats([r for r in rows
            if r['hours_since_passed_direct'] is not None and not r['intervening_implicit_rises']]),
        band1_accuracy60= bins, exclusion_counts=dict(exclusions), reviews=rows)


if __name__ == '__main__':
    result = dict(method='Raw before/after reconstruction, including darkest starting band, frozen account-specific manifests.',
        limits=['Capture completion observations are used for direct-practice ages, not exact backend event instants.',
                'Intervening visible rises are a lower bound: flat bands can hide fractional implicit credit.',
                'Intervening rises require a structural prerequisite path and an already-blue target; this supports candidate implicit credit but does not establish content coverage or a measured dose.',
                'No observed implicit rise is not proof that no implicit practice occurred.',
                'Correct assessment answers and other invisible credit are not reconstructed into the direct-practice clock.',
                'Review completion times do not identify first offer or exact due times.'],
        accounts={a: analyze(a) for a in ACCOUNTS})
    (HERE/'raw-review-state.json').write_text(json.dumps(result, indent=2)+'\n')
    for a,d in result['accounts'].items():
        print(a, json.dumps({k:v for k,v in d.items() if k not in ('reviews','band1_accuracy60')}))
