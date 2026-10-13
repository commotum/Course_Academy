"""Practical encompassing estimates from account-local activity crossing cadence.

Run: PYTHONPATH=capture python3 -m scripts.estimate_encompassing_frequency REPORT_FOLDER
Reads frozen encompassing reports; never writes operational learner or curriculum data.
"""
from collections import defaultdict
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path

from .analyze_encompassing import read, wilson

PILOTS = {'foundations': ('4387', '48'), 'linear': ('1961', '2211'),
          'multivariable': ('2110', '1951'), 'differential': ('3245', '3668')}


def cadence(exposures):
    """Flats contribute to waiting time; a positive jump is one crossing event."""
    rises = [i for i, e in enumerate(exposures, 1) if e['after'] > e['before']]
    waits = [b-a for a,b in zip([0]+rises, rises)]
    total = len(exposures)
    return dict(eligible_activities=total, rising_activities=len(rises),
        flat_activities=sum(e['before'] == e['after'] for e in exposures),
        falling_activities=sum(e['after'] < e['before'] for e in exposures),
        crossing_activity_numbers=rises, activities_to_each_crossing=waits,
        trailing_activities_without_crossing=total-(rises[-1] if rises else 0),
        mean_activities_per_visible_rise=total/len(rises) if rises else None,
        frequency_weight_estimate=len(rises)/total if total else None,
        summed_upward_band_steps=sum(max(0,e['after']-e['before']) for e in exposures),
        summed_downward_band_steps=sum(max(0,e['before']-e['after']) for e in exposures),
        multi_band_rising_activities=sum(e['after']-e['before']>1 for e in exposures))


def estimate(folder, account):
    source_path = folder/(account+'.json')
    report = read(source_path)
    assert report['account'] == account
    events = sorted(report['activity_audit'], key=lambda e:e['time'])
    assert all(e['account'] == account for e in events)
    by_task = {e['task_id']:e for e in events}
    source_events = defaultdict(list)
    for e in events:
        source_events[e['source']].append(e)
    target_changes = defaultdict(list)
    for c in report['changes']:
        assert c['account'] == account
        if c['task_id'] in by_task:
            target_changes[c['target']].append(c)
    results = []
    for pair in report['pairs']:
        if pair['graph_relation'] != 'prerequisite' or not pair['passed_exposures']:
            continue
        exposures = sorted(pair['passed_exposures'], key=lambda e:by_task[e['task_id']]['time'])
        # This report proposes positive relationships. No rise does not imply zero coverage.
        if not any(e['after'] > e['before'] for e in exposures):
            continue
        stats = cadence(exposures)
        sequence = []
        previous = None
        for index,e in enumerate(exposures,1):
            event = by_task[e['task_id']]
            changes = [c for c in target_changes[pair['target']] if previous is not None and
                by_task[previous['task_id']]['time'] < by_task[c['task_id']]['time'] < event['time']]
            direct = [x['task_id'] for x in events if previous is not None and x['source']==pair['target'] and
                by_task[previous['task_id']]['time'] < x['time'] < event['time']]
            total_grades = sum(event['grades'].values())
            sequence.append(dict(account=account, eligible_activity_number=index,
                captured_source_activity_number=next(i for i,x in enumerate(source_events[pair['source']],1)
                                                     if x['task_id']==e['task_id']),
                task_id=e['task_id'], kind=e['kind'], at=datetime.fromtimestamp(event['time'],timezone.utc).isoformat(),
                before=e['before'], after=e['after'], rising=e['after']>e['before'],
                accuracy=event['grades'].get('Correct',0)/total_grades if total_grades else None,
                hours_since_previous_eligible_source_activity=(event['time']-by_task[previous['task_id']]['time'])/3600 if previous else None,
                intervening_visible_target_changes=[{k:c[k] for k in ['task_id','source','before','after','isolated']} for c in changes],
                intervening_direct_target_tasks=direct,
                endpoint_discontinuity=previous is not None and e['before']!=previous['after'],
                background_crossing_rate=e['background_up_rate'], evidence=e['snapshot']))
            previous = e
        quality_counts = defaultdict(lambda: [0,0])
        for e in exposures:
            quality_counts[e['quality_class']][0] += e['after']>e['before']
            quality_counts[e['quality_class']][1] += 1
        background = sum(e['background_up_rate'] for e in exposures)/len(exposures)
        result = dict(account=account, source=pair['source'], source_title=pair['source_title'],
            target=pair['target'], target_title=pair['target_title'],
            prerequisite_distance=pair['prerequisite_distance'], **stats,
            proposed_starting_coverage_weight=round(round(stats['frequency_weight_estimate']*20)/20,2),
            weight_status='Frequency-based provisional coverage prior, assuming one visible crossing per full-credit activity. Not a recovered proprietary weight or a measurement of intrinsic coverage.',
            crossing_frequency_interval=wilson(stats['rising_activities'],stats['eligible_activities']),
            interval_status='Descriptive Wilson interval for crossing frequency; not a coverage-weight confidence interval.',
            background_expected_rises=sum(e['background_up_rate'] for e in exposures),
            background_adjusted_frequency_diagnostic=max(0,stats['frequency_weight_estimate']-background),
            background_status='Same account/target/before band/rounded quality, excluding this source; other activities may also genuinely encompass the target. This diagnostic is not the proposed weight.',
            cadence_has_intervening_target_updates=any(x['intervening_visible_target_changes'] or x['intervening_direct_target_tasks'] or x['endpoint_discontinuity'] for x in sequence),
            outcome_classes=[dict(quality_class=q,rises=k,n=n) for q,(k,n) in sorted(quality_counts.items())],
            sequence=sequence)
        results.append(result)
    results.sort(key=lambda x:(-x['rising_activities'],-x['eligible_activities'],x['source'],x['target']))
    output = dict(account=account, source_report=str(source_path),
        source_report_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
        created_at=datetime.now(timezone.utc).isoformat(),
        method='Weight prior = upward crossing activities / eligible passed activities; proposed starting value rounded to 0.05. Every flat exposure counts in the denominator. Jump sizes are retained separately.',
        assumptions=['One upward transition is one comparable visible-credit unit; larger ordinal jumps are not equated to repetitions.',
            'Crossing frequency is used as a practical stand-in for effective coverage, before fitting latent state and display thresholds.',
            'Do not divide this number by raw task accuracy: target historical accuracy and timing are distinct unknown multipliers.',
            'No observations, controls, or confidence evidence are pooled across accounts.'],
        eligibility='Previously nominated prerequisite pairs with any passed fully graded exposure; no minimum repeat count. Target starts in bands 1..5; same-account timing isolation from the original analysis.',
        limitations=['Candidate discovery used observed rises, so these estimates favor relationships that became visible in the sample.',
            'Captured-source ordinals start with the first saved activity, not the learner\'s first-ever activity.',
            'Waiting counts are counts of this source\'s eligible activities; intervening target updates can censor a clean accumulation run.',
            'Early-practice discount, slow-implicit gating, memory, accuracy history, threshold phase and transitive relationships affect frequency.',
            'Trailing flats count in the frequency denominator and are retained as unfinished waiting time.',
            'The upper band cannot reveal further positive credit and is excluded, never counted as zero.',
            'No-crossing pairs have insufficient visible evidence for this positive-edge estimator; they are not assigned zero.'],
        proposals=results)
    (folder/(account+'-frequency-estimates.json')).write_text(json.dumps(output,indent=2)+'\n')
    pilot = next(x for x in results if (x['source'],x['target'])==PILOTS[account])
    lines = [f'Activity-count encompassing weight estimates: {account}', '', output['method'], '',
        'These are usable starting estimates under an explicit crossing-unit assumption. They replace the earlier content-only proposal only if a frequency-based prior is desired; no operational data were changed.', '',
        f"Pilot: {pilot['source_title']} ({pilot['source']}) -> {pilot['target_title']} ({pilot['target']}).",
        f"Visible rises: {pilot['rising_activities']}/{pilot['eligible_activities']}; estimate {pilot['frequency_weight_estimate']:.3f}; proposed starting weight {pilot['proposed_starting_coverage_weight']:.2f}.",
        'Crossing activity numbers: '+str(pilot['crossing_activity_numbers'])+'.',
        'Activity counts to successive rises (including leading/intervening flats): '+str(pilot['activities_to_each_crossing'])+'.',
        f"Activities per rise including trailing flats: {pilot['mean_activities_per_visible_rise']:.2f}.",
        f"Sum of upward ordinal band steps: {pilot['summed_upward_band_steps']}; multi-band rising events: {pilot['multi_band_rising_activities']}. These steps are not measured repetitions.",
        f"Cadence includes intervening visible/direct target updates: {pilot['cadence_has_intervening_target_updates']}.", '',
        'Pilot activity sequence:']
    for e in pilot['sequence']:
        lines.append(f"  #{e['eligible_activity_number']} ({e['kind']}, task {e['task_id']}): {e['before']} -> {e['after']}; accuracy {e['accuracy']:.0%}; intervening target changes {len(e['intervening_visible_target_changes'])}; intervening direct target tasks {e['intervening_direct_target_tasks']}.")
    lines += ['', f'All {len(results)} positive prerequisite-pair proposals, including single-activity estimates:',
              'Source -> target | rises/activities | weight | crossing activity numbers | titles']
    for x in results:
        lines.append(f"{x['source']} -> {x['target']} | {x['rising_activities']}/{x['eligible_activities']} | {x['proposed_starting_coverage_weight']:.2f} | {x['crossing_activity_numbers']} | {x['source_title']} -> {x['target_title']}")
    lines += ['', 'Assumptions:']+output['assumptions']+['', 'Limits:']+output['limitations']
    (folder/(account+'-frequency-estimates.txt')).write_text('\n'.join(lines)+'\n')
    print(account, len(results),'proposals; pilot',pilot['frequency_weight_estimate'],
          'crossings',pilot['crossing_activity_numbers'],'waits',pilot['activities_to_each_crossing'])
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder',type=Path)
    args = parser.parse_args()
    for account in PILOTS:
        estimate(args.folder.resolve(), account)


if __name__ == '__main__':
    main()
