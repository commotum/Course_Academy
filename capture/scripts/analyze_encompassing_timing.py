"""Account-local magnitude and spacing diagnostics on frozen capture manifests.

Run: PYTHONPATH=capture python3 -m scripts.analyze_encompassing_timing REPORT_FOLDER
No browser/database calls or operational state writes. Uses the original isolation
rules, including unchanged prerequisite topics; discovery does not require a rise.
"""
from bisect import bisect_right
from collections import defaultdict
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics

from .analyze_encompassing import collapse, distances, read, snapshot, timestamp
from .progress import color_observation

ACCOUNTS = ('foundations', 'linear', 'multivariable', 'differential')
PILOTS = {'foundations': ('4387', '48'), 'linear': ('1961', '2211'),
          'multivariable': ('2110', '1951'), 'differential': ('3245', '3668')}


def age_bin(hours):
    if hours is None:
        return 'unknown'
    for upper, label in [(6, '<6h'), (12, '6–12h'), (24, '12–24h'), (48, '24–48h')]:
        if hours < upper:
            return label
    return '48h+'


def summarize(rows):
    n = len(rows)
    if not n:
        return {'n': 0}
    return dict(n=n, activities=len({r['task_id'] for r in rows}),
        pairs=len({(r['source'], r['target']) for r in rows}),
        rises=sum(r['delta'] > 0 for r in rows),
        flats=sum(r['delta'] == 0 for r in rows),
        falls=sum(r['delta'] < 0 for r in rows),
        mean_signed_steps=statistics.mean(r['delta'] for r in rows),
        mean_positive_steps=statistics.mean(max(0, r['delta']) for r in rows),
        mean_steps_given_rise=statistics.mean(r['delta'] for r in rows if r['delta'] > 0)
            if any(r['delta'] > 0 for r in rows) else None,
        multi_band_rises=sum(r['delta'] > 1 for r in rows),
        ends_darkest=sum(r['after'] == 6 for r in rows),
        mean_activity_background_steps=statistics.mean(r['background_signed_steps'] for r in rows),
        mean_background_adjusted_steps=statistics.mean(r['delta']-r['background_signed_steps'] for r in rows))


def solve(matrix, vector):
    """Small dense least-squares normal system with pivoting; no dependencies."""
    size = len(vector)
    augmented = [list(row)+[rhs] for row, rhs in zip(matrix, vector)]
    for i in range(size):
        pivot = max(range(i, size), key=lambda j: abs(augmented[j][i]))
        if abs(augmented[pivot][i]) < 1e-9:
            return None
        augmented[i], augmented[pivot] = augmented[pivot], augmented[i]
        divisor = augmented[i][i]
        augmented[i] = [x/divisor for x in augmented[i]]
        for j in range(size):
            if i != j:
                factor = augmented[j][i]
                augmented[j] = [x-factor*y for x, y in zip(augmented[j], augmented[i])]
    return [row[-1] for row in augmented]


def within_spacing(rows, outcome='delta', clocks=('hours_since_target_direct',)):
    """Demean within source/target/before/kind/exact accuracy/pipeline strata.

    No invented ages for left-censored histories. Repeated strata supply timing
    identification; singleton observations still remain in the main analysis.
    Coefficients are descriptive associations, with no iid significance claim.
    """
    assert len({r['account'] for r in rows}) <= 1, 'Timing calibration must be account-local'
    groups = defaultdict(list)
    for row in rows:
        if all(row.get(c) is not None for c in clocks):
            groups[(row['source'], row['target'], row['before'], row['kind'],
                    row['accuracy'], row['pipeline'])].append(row)
    retained = [group for group in groups.values() if len(group) > 1]
    xs, ys, records = [], [], []
    for group in retained:
        vectors = [[math.log2(1+r[c]) for c in clocks] for r in group]
        averages = [statistics.mean(x[j] for x in vectors) for j in range(len(clocks))]
        average_y = statistics.mean(r[outcome] for r in group)
        for row, vector in zip(group, vectors):
            xs.append([x-m for x, m in zip(vector, averages)])
            ys.append(row[outcome]-average_y)
            records.append(row)
    if not xs:
        return {'n': 0, 'strata': 0, 'coefficients': None}
    gram = [[sum(x[i]*x[j] for x in xs) for j in range(len(clocks))] for i in range(len(clocks))]
    rhs = [sum(x[i]*y for x, y in zip(xs, ys)) for i in range(len(clocks))]
    beta = solve(gram, rhs)
    ss = sum(y*y for y in ys)
    sse = sum((y-sum(b*v for b,v in zip(beta,x)))**2 for x,y in zip(xs,ys)) if beta else None
    return dict(n=len(xs), activities=len({r['task_id'] for r in records}),
        pairs=len({(r['source'],r['target']) for r in records}), strata=len(retained),
        coefficients=dict(zip(clocks,beta)) if beta else None,
        outcome=outcome, within_r_squared=1-sse/ss if ss and sse is not None else None,
        unit='Ordinal steps per doubling of (1 + hours); association, not causal credit.',
        controls='Account, source/target pair, starting band, activity kind, exact observed accuracy, capture pipeline.',
        limitation='Repeated pair/band strata identify the association; task and topic outcomes are dependent. No independence-based confidence interval.')


def magnitude_profiles(rows, previous):
    """Keep every prior candidate; test whether a direct-review scale is usable.

    Matching never crosses account, before band, exact accuracy, or target-age
    bin. These ratios deliberately are NOT clamped into encompassing weights:
    unsupported or >1 responses expose failures of the proposed calibration.
    """
    assert all(r['account']==previous['account'] for r in rows), 'Controls must belong to the same account'
    controls=defaultdict(list)
    by_pair=defaultdict(list)
    for row in rows:
        if row['direct'] and row['kind']=='review' and row['hours_since_target_direct'] is not None:
            controls[row['before'],row['accuracy'],age_bin(row['hours_since_target_direct'])].append(row)
        if row['nominated']:
            by_pair[row['source'],row['target']].append(row)
    profiles=[]
    for prior in previous['proposals']:
        group=by_pair[prior['source'],prior['target']]
        assert len(group)==prior['eligible_activities']
        matched=[]
        for row in group:
            age=row['hours_since_target_direct']
            pool=controls[row['before'],row['accuracy'],age_bin(age)] if age is not None else []
            specific=[c for c in pool if c['target']==row['target']]
            chosen=specific or pool
            matched.append(dict(task_id=row['task_id'],n=len(chosen),
                scope='same_target' if specific else 'same_account' if chosen else 'unavailable',
                expected_direct_steps=statistics.mean(c['positive_steps'] for c in chosen) if chosen else None))
        covered=[(r,c) for r,c in zip(group,matched) if c['n']]
        expected=sum(c['expected_direct_steps'] for _,c in covered)
        observed=sum(r['positive_steps'] for r,_ in covered)
        ratio=observed/expected if expected else None
        profiles.append(dict(account=group[0]['account'],source=prior['source'],target=prior['target'],
            source_title=prior['source_title'],target_title=prior['target_title'],
            old_frequency=prior['frequency_weight_estimate'],**summarize(group),
            positive_steps_per_activity=statistics.mean(r['positive_steps'] for r in group),
            timing_matched_exposures=len(covered),timing_matched_expected_direct_steps=expected,
            timing_matched_observed_steps=observed,relative_display_response=ratio,
            scale_status='unavailable' if not covered else 'zero_direct_anchor' if not expected else
                'above_full_coverage_scale' if ratio>1 else 'descriptive_relative_response_only',
            controls=matched,sequence=group,
            operational_weight=None,
            reason='Display steps are not established repetitions; source/target speed, hidden memory and threshold phase are unresolved. Preserve magnitude and clocks; do not silently clamp a response ratio into a coverage attribute.'))
    return profiles


def analyze(folder, account, discovered):
    report_path = folder/(account+'.json')
    report = read(report_path)
    audits = {e['task_id']: e for e in report['activity_audit']}
    manifest = {(s['task_id'], s['path']) for s in report['sources']}
    events = [e for e in discovered if e['account'] == account and (e['task_id'],e['path']) in manifest]
    assert len(events) == len(audits)
    assert all(e['account'] == account for e in events)
    events.sort(key=lambda e:e['time'])
    print('Reconstructing', account, len(events), 'frozen activities', flush=True)
    times = [e['time'] for e in events]
    context = read(report['graph_sources'][0]['path'])
    assert hashlib.sha256(Path(report['graph_sources'][0]['path']).read_bytes()).hexdigest() == report['graph_sources'][0]['sha256']
    upstream = defaultdict(set)
    for source, children in context['graph'].items():
        for child in children:
            upstream[str(child)].add(str(source))
    ancestors = {}
    old = read(folder/(account+'-frequency-estimates.json'))
    nominations = {(p['source'],p['target']) for p in old['proposals']}
    last_direct, last_source, last_potential, last_change = {}, {}, {}, {}
    target_accuracy = defaultdict(lambda:[0,0])
    rows = []
    batch = []
    for event_number, event in enumerate(events, 1):
        audit = audits[event['task_id']]
        source = event['source']
        if source not in ancestors:
            ancestors[source] = set(distances(source,upstream))-{source} if source else set()
        passed = event['outcome']=='passed' and bool(event['grades']) and all(
            g in ('Correct','Incorrect','Skipped Question') for g in event['grades'])
        if event['pipeline'] == 'current':
            data = read(event['path']).get('observations',{})
            after = {}
            for course in data.get('courses') or data.get('progress') or []:
                for topic in course.get('topics',[]):
                    after[str(course['course_id']),str(topic['topic_id'])] = (
                        color_observation(topic)['display_band'],timestamp(course.get('captured_at') or event['time']),topic.get('title'))
        else:
            after = snapshot(event['path'])
        before = snapshot(event['before_path']) if event['before_path'] and Path(event['before_path']).is_file() else {}
        observations,_ = collapse(before,after)
        safe = {}
        if not audit['exclusion_reasons'] and passed:
            for topic, value in observations.items():
                b,a,start,end,_ = value
                if not 1 <= b <= 5 or not 0 < end-start <= 1800:
                    continue
                if not start < event['time'] <= end or bisect_right(times,end)-bisect_right(times,start) != 1:
                    continue
                if event['first_answer_at'] is not None and start >= event['first_answer_at']:
                    continue
                safe[topic]=(b,a)
        background = defaultdict(list)
        for topic,(b,a) in safe.items():
            if topic != source and topic not in ancestors[source]:
                background[b].append(a-b)
        batch.append(dict(account=account,task_id=event['task_id'],source=source,
            changes=sum(a!=b for b,a in safe.values()),
            rises=sum(a>b for b,a in safe.values()),falls=sum(a<b for b,a in safe.values()),
            unrelated_background={str(b):dict(n=len(v),mean_signed_steps=statistics.mean(v),
                mean_positive_steps=statistics.mean(max(0,x) for x in v)) for b,v in background.items()}))
        for target,(b,a) in safe.items():
            if target != source and target not in ancestors[source]:
                continue
            def gap(history, key):
                return (event['time']-history[key]['time'])/3600 if key in history else None
            accuracy = event['grades'].count('Correct')/len(event['grades'])
            bg = background[b]
            c,n = target_accuracy[target]
            rows.append(dict(account=account,task_id=event['task_id'],source=source,target=target,
                before=b,after=a,delta=a-b,positive_steps=max(0,a-b),kind=event['kind'],
                pipeline=event['pipeline'],at=datetime.fromtimestamp(event['time'],timezone.utc).isoformat(),
                accuracy=accuracy,nominated=(source,target) in nominations,
                direct=target==source,
                hours_since_target_direct=gap(last_direct,target),
                previous_direct_task=last_direct.get(target,{}).get('task_id'),
                hours_since_source=gap(last_source,source),
                hours_since_potential_target_practice=gap(last_potential,target),
                previous_potential_task=last_potential.get(target,{}).get('task_id'),
                hours_since_visible_target_change=gap(last_change,target),
                target_prior_captured_accuracy=c/n if n else None,
                target_prior_captured_questions=n,
                background_n=len(bg),background_signed_steps=statistics.mean(bg) if bg else 0,
                background_positive_steps=statistics.mean(max(0,x) for x in bg) if bg else 0,
                background_adjusted_delta=a-b-(statistics.mean(bg) if bg else 0),
                evidence=event['path']))
        # All clocks are pre-activity. Prior capture-only history is never backfilled.
        if source:
            last_source[source]=event
            for grade in event['grades']:
                if grade in ('Correct','Incorrect','Skipped Question'):
                    target_accuracy[source][0] += grade=='Correct'
                    target_accuracy[source][1] += 1
            if passed:
                last_direct[source]=event
                for target in ancestors[source] | {source}:
                    last_potential[target]=event
        for target,value in observations.items():
            if value[0] != value[1]:
                last_change[target]=event
        if event_number % 200 == 0:
            print(account, event_number, 'activities;', len(rows), 'eligible observations', flush=True)
    implicit = [r for r in rows if not r['direct']]
    nominated = [r for r in implicit if r['nominated']]
    direct = [r for r in rows if r['direct'] and r['kind']=='review']
    results = {}
    for label, subset in [('all_prerequisites',implicit),('previously_nominated',nominated),('direct_reviews',direct)]:
        results[label]={'overall':summarize(subset)}
        for clock in ['hours_since_target_direct','hours_since_source','hours_since_potential_target_practice']:
            results[label][clock]={'bins':{b:summarize([r for r in subset if age_bin(r[clock])==b])
                for b in ['<6h','6–12h','12–24h','24–48h','48h+','unknown']},
                'within_fixed_context':within_spacing(subset,clocks=(clock,)),
                'within_fixed_context_without_darkest_end':within_spacing([r for r in subset if r['after']<6],clocks=(clock,)),
                'within_fixed_context_background_adjusted':within_spacing(subset,outcome='background_adjusted_delta',clocks=(clock,))}
        results[label]['joint_spacing']=within_spacing(subset,clocks=('hours_since_target_direct','hours_since_source'))
        results[label]['by_starting_band']={str(b):summarize([r for r in subset if r['before']==b]) for b in range(1,6)}
        results[label]['by_accuracy']={str(p):summarize([r for r in subset if r['accuracy']==p]) for p in sorted({r['accuracy'] for r in subset})}
    results['direct_band1_accuracy60']={'overall':summarize([r for r in direct if r['before']==1 and r['accuracy']==.6]),
        'target_age_bins':{b:summarize([r for r in direct if r['before']==1 and r['accuracy']==.6 and age_bin(r['hours_since_target_direct'])==b])
            for b in ['<6h','6–12h','12–24h','24–48h','48h+','unknown']}}
    profiles=magnitude_profiles(rows,old)
    pilot = [r for r in rows if (r['source'],r['target'])==PILOTS[account]]
    output=dict(account=account,created_at=datetime.now(timezone.utc).isoformat(),
        source_report=str(report_path),source_report_sha256=hashlib.sha256(report_path.read_bytes()).hexdigest(),
        window={'activities':len(events),'first':events[0]['time'],'last':events[-1]['time']},
        methodology='Reconstruct all isolated passed/graded source and prerequisite topic observations from the frozen manifest. No rise-based selection for all_prerequisites. Colors are ordinal categories.',
        clocks={'hours_since_target_direct':'Since last captured passed, fully graded lesson/review directly on this target. Unknown before capture history; excludes missing assessment topic assignments.',
            'hours_since_source':'Since last captured activity on this source, regardless of success.',
            'hours_since_potential_target_practice':'Since last passed, fully graded activity on target or any prerequisite-graph descendant. Structural proxy: not every prerequisite is truly encompassed.',
            'hours_since_visible_target_change':'Since last observed color change of either sign. Display activity proxy, not a memory update timestamp.'},
        results=results,pilot=pilot,observations=rows,activity_batches=batch,
        magnitude_profiles=profiles,
        limits=['Timing is not randomized; review scheduling, source/task choice, topic speed and target state confound associations.',
            'Clock unknown means left-censored, never zero. Recorded clock ages are upper bounds when other qualifying practice is missing.',
            'Exact repetitions, memory, half-lives and display thresholds are absent. No hours-to-repetitions conversion.',
            'Darkest-end exclusion is a sensitivity diagnostic, not deletion of main observations or estimates.',
            'Potential-practice clock uses prerequisite structure, not recovered encompassing weights.',
            'Shared movement among unrelated targets can reflect genuine omitted relations or display/model changes; background subtraction is a diagnostic only.'])
    destination=folder/'timing-magnitude'
    destination.mkdir(exist_ok=True)
    (destination/(account+'.json')).write_text(json.dumps(output,indent=2)+'\n')
    lines=[account+': captured magnitude and spacing','',
        'Display categories, not recovered numeric repetitions. All controls belong to this account. No operational weights were written.',
        '', 'Direct passed reviews, starting band 1 and 60% accuracy:',
        'Target-direct age | n | rises | mean positive palette steps']
    for b,stats in results['direct_band1_accuracy60']['target_age_bins'].items():
        lines.append(f"{b} | {stats['n']} | {stats.get('rises',0)} | {stats.get('mean_positive_steps','unknown')}")
    lines+=['','Pilot:']
    for row in pilot:
        lines.append(f"{row['task_id']}: {row['before']}->{row['after']}; direct-target age {row['hours_since_target_direct']}; source age {row['hours_since_source']}; potential-practice age {row['hours_since_potential_target_practice']}; accuracy {row['accuracy']}")
    lines+=['','All prior relationship candidates, including single-exposure profiles:',
        'Source->target | N | old frequency | mean positive palette steps | direct-control scale status | relative response diagnostic']
    for profile in profiles:
        lines.append(f"{profile['source']}->{profile['target']} | {profile['n']} | {profile['old_frequency']:.3f} | {profile['mean_positive_steps']:.3f} | {profile['scale_status']} | {profile['relative_display_response']}")
    (destination/(account+'.txt')).write_text('\n'.join(lines)+'\n')
    print(account,len(implicit),'ancestor observations;',len(nominated),'nominated;',len(direct),'direct reviews',flush=True)
    for label in results:
        if label=='direct_band1_accuracy60':
            continue
        print(label,results[label]['overall'],flush=True)
        for clock in ['hours_since_target_direct','hours_since_source','hours_since_potential_target_practice']:
            print(clock,results[label][clock]['within_fixed_context'],flush=True)
    return output


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    args=parser.parse_args()
    # Reuse recorded identities, outcomes and grades, rather than rediscovering
    # mutable runner folders or rereading every question's saved DOM.
    discovered=[]
    for account in ACCOUNTS:
        report=read(args.folder/(account+'.json'))
        sources={s['task_id']:s for s in report['sources']}
        for audit in report['activity_audit']:
            first_answer=None
            if audit['pipeline']=='current':
                content=read(Path(audit['path']).parent/'content.json')
                starts=[a['started_at'] for a in content.get('attempts',[]) if isinstance(a.get('started_at'),(int,float))]
                first_answer=min(starts) if starts else None
            discovered.append({**audit,'before_path':sources[audit['task_id']]['before_path'],
                'first_answer_at':first_answer,
                'grades':[g for g,n in audit['grades'].items() for _ in range(n)]})
    for account in ACCOUNTS:
        analyze(args.folder.resolve(),account,discovered)


if __name__=='__main__':
    main()
