"""Compare observed KP correctness with mixed band effects, separately by account.

Consumes saved encompassing reports and pinned, read-only KP definition exports.
Run: PYTHONPATH=capture python3 -m scripts.analyze_kp_effects REPORT_FOLDER
"""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
import argparse
import json
from pathlib import Path

from .analyze_encompassing import read

PILOTS = {'foundations': ('4387', '48'), 'linear': ('1961', '2211'),
          'multivariable': ('2110', '1951'), 'differential': ('3245', '3668')}


@lru_cache(maxsize=16)
def answers(path, pipeline):
    path = Path(path)
    folder = path.parents[1] if pipeline == 'legacy' else path.parent
    content = read(folder/'content.json')
    result = []
    if pipeline == 'legacy':
        state = read(folder/'state.json')
        questions = state.get('questions', {})
        questions = list(questions.values()) if isinstance(questions, dict) else questions
        by_problem = {q.get('problem'): q for q in content.get('questions', [])}
        for q in questions:
            c = q.get('content') or by_problem.get(q.get('before', {}).get('problem'), {})
            kp = c.get('knowledge_point') or state.get('kps', {}).get(q.get('kp_id'), {}).get('title')
            grade = q.get('actual_result') or q.get('history', {}).get('result') or q.get('after', {}).get('result')
            result.append({'kp': kp, 'grade': grade, 'question_id': c.get('math_academy_id'),
                           'difficulty': c.get('difficulty')})
    else:
        by_id = {q.get('math_academy_id'): q for q in content.get('questions', [])}
        by_problem = {q.get('problem'): q for q in content.get('questions', [])}
        for a in content.get('attempts', []):
            q = a.get('question', {})
            c = by_id.get(q.get('math_academy_id')) or by_problem.get(q.get('problem'), {})
            result.append({'kp': c.get('knowledge_point'),
                'grade': a.get('grade') or a.get('last_observation', {}).get('grade'),
                'question_id': c.get('math_academy_id'), 'difficulty': c.get('difficulty')})
    return result


def counts(questions):
    return {'correct': sum(q['grade'] == 'Correct' for q in questions),
            'incorrect': sum(q['grade'] == 'Incorrect' for q in questions),
            'other': sum(q['grade'] not in ('Correct', 'Incorrect') for q in questions),
            'n': len(questions)}


def mixed_groups(rows, signature):
    groups = defaultdict(list)
    for row in rows:
        key = signature(row)
        if key is not None:
            groups[key].append(row)
    return [xs for xs in groups.values() if any(x['rise'] for x in xs) and any(not x['rise'] for x in xs)]


def compare(folder, account):
    report = read(folder/(account+'.json'))
    assert report['account'] == account
    definitions = read(folder/'kp-effects'/(account+'-key-prerequisites.json'))
    links = {}
    for row in definitions:
        topic = row[0]
        for kp in topic.get(':topic/knowledge-points', []):
            links[(str(topic[':topic/math-academy-id']), kp[':knowledge-point/title'])] = [
                str(t[':topic/math-academy-id']) for t in kp.get(':knowledge-point/key-prerequisites', [])]
    events = sorted(report['activity_audit'], key=lambda x: x['time'])
    assert all(e['account'] == account for e in events)
    by_task = {e['task_id']: e for e in events}
    # Selection is descriptive: these pairs already showed at least one visible rise.
    # It cannot estimate an unconditional probability of a causal encompassing edge.
    pairs = [p for p in report['pairs'] if
        0 < p['passed_unsaturated_rises'] < p['passed_unsaturated_exposures'] and
        p['passed_unsaturated_exposures'] >= 3 and p['graph_relation'] == 'prerequisite' and
        p['prerequisite_distance'] <= 2]
    pilot = next(p for p in report['pairs'] if (p['source'], p['target']) == PILOTS[account])
    if pilot not in pairs:
        pairs.append(pilot)
    observations = []
    for pair in pairs:
        for exposure in pair['passed_exposures']:
            e = by_task[exposure['task_id']]
            qs = answers(e['path'], e['pipeline'])
            groups = defaultdict(list)
            for q in qs:
                groups[q['kp']].append(q)
            all_counts = counts(qs)
            assert Counter(q['grade'] for q in qs) == Counter(e['grades']), (account, e['task_id'])
            linked = [q for q in qs if pair['target'] in links.get((pair['source'], q['kp']), [])]
            prior_source = [x for x in events if x['time'] < e['time'] and x['source'] == pair['source']]
            prior_target = [x for x in events if x['time'] < e['time'] and x['source'] == pair['target']]
            source_elapsed = (e['time']-prior_source[-1]['time'])/3600 if prior_source else None
            target_elapsed = (e['time']-prior_target[-1]['time'])/3600 if prior_target else None
            recent = [c for c in report['changes'] if c['target'] == pair['target'] and
                c['task_id'] in by_task and e['time']-3600 <= by_task[c['task_id']]['time'] < e['time']]
            observations.append(dict(account=account, source=pair['source'], target=pair['target'],
                source_title=pair['source_title'], target_title=pair['target_title'],
                task_id=e['task_id'], kind=e['kind'], time=e['time'], evidence=e['path'],
                before=exposure['before'], after=exposure['after'], rise=exposure['after']>exposure['before'],
                accuracy=all_counts['correct']/all_counts['n'] if all_counts['n'] else None,
                overall=all_counts, linked_kp=counts(linked),
                hours_since_source_activity=source_elapsed, hours_since_direct_target_activity=target_elapsed,
                target_changes_in_preceding_hour=[{k:c[k] for k in ['task_id','before','after']} for c in recent],
                kp_results=[dict(title=kp, key_prerequisites=links.get((pair['source'],kp), []),
                    outcomes=counts(xs), questions=xs) for kp,xs in sorted(groups.items(),key=lambda x:str(x[0]))],
                answer_order=qs))
    def base(x):
        return (x['source'],x['target'],x['before'],x['kind'],
                Fraction(x['overall']['correct'], x['overall']['n']))
    def kp_signature(x):
        if not all(k['title'] for k in x['kp_results']):
            return None
        return base(x) + (tuple((k['title'],k['outcomes']['correct'],k['outcomes']['incorrect'],
                                k['outcomes']['other']) for k in x['kp_results']),)
    equal_accuracy = mixed_groups(observations, base)
    equal_kps = mixed_groups(observations, kp_signature)
    equal_order = mixed_groups(observations, lambda x: kp_signature(x) +
        (tuple((q['kp'], q['grade']) for q in x['answer_order']),) if kp_signature(x) else None)
    zero_linked = [x for x in observations if x['linked_kp']['n'] and not x['linked_kp']['correct']]
    no_linked = [x for x in observations if not x['linked_kp']['n']]
    summary = dict(pairs=len(pairs), observations=len(observations),
        rises=sum(x['rise'] for x in observations),
        flat=sum(x['before'] == x['after'] for x in observations),
        declines=sum(x['after'] < x['before'] for x in observations),
        same_source_target_band_kind_accuracy_mixed_groups=len(equal_accuracy),
        same_source_target_band_kind_accuracy_kp_counts_mixed_groups=len(equal_kps),
        same_source_target_band_kind_accuracy_kp_counts_answer_order_mixed_groups=len(equal_order),
        zero_correct_on_explicit_linked_kp_observations=len(zero_linked),
        zero_correct_on_explicit_linked_kp_rises=sum(x['rise'] for x in zero_linked),
        no_explicit_linked_kp_observations=len(no_linked),
        no_explicit_linked_kp_rises=sum(x['rise'] for x in no_linked))
    output = dict(account=account, selection='Previously identified prerequisite pairs within distance two with >=3 passed unsaturated exposures and both rises and non-rises, plus the account pilot.',
        interpretation='Descriptive matched comparisons, not independent randomized trials. Exact KP links are positive annotations; missing links may be uncaptured. No target memory, fractional repetitions, or accuracy are observable from a color bin.',
        summary=summary, observations=observations,
        accuracy_distribution=dict(Counter(str(x['accuracy']) for x in observations)),
        matched_accuracy_mixed_groups=[[x['task_id'] for x in xs] for xs in equal_accuracy],
        matched_kp_mixed_groups=[[dict(task_id=x['task_id'],source=x['source'],target=x['target'],
                                    before=x['before'],after=x['after']) for x in xs] for xs in equal_kps])
    (folder/'kp-effects'/(account+'-effects.json')).write_text(json.dumps(output,indent=2)+'\n')
    lines = [f'KP correctness and varying band effects: {account}', '',
        'Leading working explanation: target state and practice history determine how much task-level encompassing credit becomes visible. An unchanged unsaturated band may conceal positive fractional credit. Do not estimate a zero edge from a flat color.', '',
        'Current-activity overall accuracy alone cannot explain the matched differences below. KP mix is a plausible modifier of effective coverage, but identical observed KP counts and correctness can still yield different visible effects. Existing key-prerequisite links identify directly used topics; their absence is not evidence of absence of use. These exports contain incomplete annotations, especially for later KP variants.', '',
        output['selection'], output['interpretation'], '', json.dumps(summary,indent=2), '',
        'Account pilot:']
    for x in observations:
        if (x['source'],x['target']) != PILOTS[account]:
            continue
        gap = x['hours_since_direct_target_activity']
        lines.append(f"  Task {x['task_id']} ({x['kind']}): {x['before']} -> {x['after']}; overall {x['overall']['correct']}/{x['overall']['n']}; explicitly linked KP {x['linked_kp']['correct']}/{x['linked_kp']['n']}; hours since captured direct target activity: {gap:.2f}" if gap is not None else
            f"  Task {x['task_id']} ({x['kind']}): {x['before']} -> {x['after']}; overall {x['overall']['correct']}/{x['overall']['n']}; explicitly linked KP {x['linked_kp']['correct']}/{x['linked_kp']['n']}; no prior captured direct target activity.")
    lines += ['', 'Matched source/target, starting band, activity kind, overall accuracy, and KP outcome counts:']
    for xs in equal_kps:
        lines.append('  '+xs[0]['source_title']+' -> '+xs[0]['target_title'])
        for x in xs:
            lines.append(f"    {x['task_id']}: {x['before']} -> {x['after']}; direct-target gap hours {x['hours_since_direct_target_activity']}; source gap hours {x['hours_since_source_activity']}")
    lines += ['', 'Estimate separately: curriculum coverage; task performance; target historical accuracy/eligibility; elapsed-time discount; fractional target repetitions; color thresholds. Keep topic/encompasses as the default model. KP-conditioned weights are an optional refinement, not the most likely explanation of these matched differences. No operational weights or learner state were changed.', '',
        'The data support state/history dependence broadly, not a particular numeric timing discount or proof that every flat event received credit. Correctness ordering, difficulty, uncaptured work, and broader display changes remain possible contributors. Many tasks were deliberately captured at 60% accuracy, limiting performance variation. Full answer order, difficulties, explicit links and per-account evidence paths are in '+account+'-effects.json.']
    (folder/'kp-effects'/(account+'-effects.txt')).write_text('\n'.join(lines)+'\n')
    print(account,json.dumps(summary))
    print(' matched KP discordance',output['matched_kp_mixed_groups'][:5])
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    for account in PILOTS:
        compare(args.folder.resolve(), account)


if __name__ == '__main__':
    main()
