"""Prepare separate account reports and explicitly provisional content priors.

Consumes analyze_encompassing JSON, never browser state or EDB.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path


PILOTS = {
    'foundations': ('4387', '48', .10,
        'One of four captured source KPs contains finite-product sketches. Two of its five distinct sampled questions use two finite sets; the other three involve an interval. Equal KP weighting gives (1/4)*(2/5)=0.10 before any further discount for component breadth. This is a small content prior, despite three visible rises. Do not infer full coverage from 3/3 crossings.'),
    'linear': ('1961', '2211', .50,
        'Three of four source KPs construct transformation matrices from basis-vector images or coordinate representations; one only multiplies a supplied matrix by a vector. The source generalizes the matrix-column idea to arbitrary bases, but does not necessarily repeat the standard-basis procedure literally. 0.50 is an expert partial-coverage prior, not a measured fraction or the fitted crossing proxy.'),
    'multivariable': ('2110', '1951', 1/3,
        'One of three source KPs requires constructing a missing potential function; the other two provide the potential and use endpoint evaluation. The captured sample has 12 distinct questions in each KP, so both equal KP weighting and this sample give 1/3. That supports partial coverage of calculating potential functions, rather than full coverage of all gradient or integration skills.'),
    'differential': ('3245', '3668', 1/3,
        'One of three source KPs performs multiple Euler steps. The other two use one step for two- and three-equation systems. Equal KP weighting gives 1/3; the observed distinct-question fraction is 11/30. A single Euler step does not fully exercise the component topic multiple-step iteration.'),
}


def sensitivity(exposures):
    supported = [e for e in exposures if e['background_n'] >= 3 and e['direct_control_n'] >= 3]
    if not supported:
        return {}
    reference = sum(e['direct_control_up_rate']-e['background_up_rate'] for e in supported)/len(supported)
    if reference <= 0:
        return {}
    excess = sum(float(e['after'] > e['before'])-e['background_up_rate'] for e in supported)
    return {str(prior): max(0., min(1., excess/(len(supported)+prior)/reference)) for prior in [0, 2, 4, 8]}


def prepare(folder, account):
    report = json.loads((folder/(account+'.json')).read_text())
    assert report['account'] == account
    assert all(e['account'] == account for e in report['activity_audit'])
    assert all(e['account'] == account for e in report['changes'])
    source, target, weight, rationale = PILOTS[account]
    pair = next(p for p in report['pairs'] if p['source'] == source and p['target'] == target)
    questions = {}
    content_sources = []
    for activity in report['activity_audit']:
        if activity['source'] != source:
            continue
        path = Path(activity['path'])
        content_path = path.parents[1]/'content.json' if activity['pipeline'] == 'legacy' else path.parent/'content.json'
        if not content_path.exists():
            continue
        content_bytes = content_path.read_bytes()
        content = json.loads(content_bytes)
        content_sources.append({'path': str(content_path), 'sha256': hashlib.sha256(content_bytes).hexdigest()})
        for question in content.get('questions', []):
            key = question.get('math_academy_id') or question.get('problem')
            questions[key] = {k: question.get(k) for k in ['math_academy_id', 'knowledge_point', 'knowledge_point_id', 'problem']}
    groups = defaultdict(list)
    for question in questions.values():
        groups[question['knowledge_point']].append(question)
    recommendations = {
        'account': account,
        'status': 'analysis proposal only; no schema, policy, encompassing, or learner writes',
        'source_topic': source, 'source_title': pair['source_title'],
        'component_topic': target, 'component_title': pair['target_title'],
        'proposed_coverage_prior': weight,
        'rationale': rationale,
        'weight_status': 'provisional domain prior informed by account-local content and band evidence; not recovered MA weight',
        'assumptions': ['Source KPs are approximately equally weighted.',
            'Target-topic breadth has not been exhaustively annotated.',
            'Observed effective coupling need not be a direct encompassing edge.',
            'No other account evidence enters this proposal.'],
        'relationship_evidence': {k: pair[k] for k in ['graph_relation', 'prerequisite_distance',
            'isolated_positive_events', 'perfect_unsaturated_exposures', 'perfect_unsaturated_rises',
            'passed_unsaturated_exposures', 'passed_unsaturated_rises', 'passed_control_supported_exposures',
            'passed_response_strength_proxy']},
        'response_proxy_shrinkage_sensitivity': sensitivity(pair['passed_exposures']),
        'response_proxy_is_coverage_weight': False,
        'observed_passed_exposures': pair['passed_exposures'],
        'content_sources': content_sources,
        'source_knowledge_points': [{'title': title, 'distinct_questions': len(qs), 'questions': qs}
                                   for title, qs in groups.items()],
        'engine_parameter_recommendation': 'Keep retention, accuracy, failure, and timing parameters unchanged from this band analysis. Treat XP-based duration recommendations in methods.txt separately.',
    }
    effects_path = folder/'kp-effects'/(account+'-effects.json')
    if effects_path.exists():
        effects = json.loads(effects_path.read_text())
        assert effects['account'] == account
        recommendations['correctness_and_kp_comparison'] = {
            'evidence': str(effects_path), 'summary': effects['summary'],
            'leading_explanation': 'Target state/history and display threshold crossing, rather than better raw correctness on the current linked KP.',
            'flat_observation_means_zero_credit': False,
            'model_recommendation': 'Retain topic-level encompassing by default. KP-conditioned coverage is an optional refinement; explicit key-prerequisite links are positive, incomplete annotations, not weight measurements.',
            'content_prior_caveat': 'The proposed content prior is a rough starting value. It does not explain every activity effect; credit can rise with zero correct explicitly linked KP questions, and an unchanged band may hide credit.'}
    (folder/(account+'-recommendation.json')).write_text(json.dumps(recommendations, indent=2)+'\n')
    summary = report['summary']
    down = [c for c in report['changes'] if c['isolated'] and c['all_correct'] and c['after'] < c['before']]
    candidates = sorted([p for p in report['pairs'] if p['graph_relation'] == 'prerequisite' and p['prerequisite_distance'] <= 3],
                        key=lambda p: (-p['isolated_positive_events'], -p['passed_unsaturated_rises']))[:8]
    lines = [f'Encompassing and engine calibration analysis: {account}', '',
        'This account is analyzed independently. No observations, controls, fitted proxies, or confidence evidence are pooled across accounts.', '',
        f"Saved activities: {summary['activities']}; logged course-qualified changes: {summary['logged_course_changes']}.",
        f"Matched topic changes after collapsing agreeing cross-course duplicates: {summary['deduplicated_topic_changes']} ({summary['rising_topic_changes']} rises, {summary['falling_topic_changes']} falls).",
        f"Activities with timing-compatible isolated practice observations: {summary['isolated_practice_activities']}; all-correct subset: {summary['isolated_all_correct_activities']}.",
        f"Known-pair mismatches between change logs and before/after snapshots: {summary['logged_snapshot_mismatches']}. Missing topic pairs in logged changes: {summary['logged_missing_topic_pairs']} (often course/scope admission, not inferred progress loss).",
        f"Conflicting cross-course topic observations excluded: {summary['conflicting_course_topic_observations']}.",
        f"Timing-compatible falls following all-correct practice: {len(down)} across {len({c['task_id'] for c in down})} activities. These cannot automatically be attributed to failures in the current task.",
        f"Pairs with at least three all-correct unsaturated rises: {summary['repeated_all_correct_pairs']}. The perfect-response numerical calibration is sparse.", '',
        f"Provisional candidate: {source} {pair['source_title']} -> {target} {pair['target_title']}.",
        f'Proposed coverage prior: {weight:.3f}.', rationale, '',
        f"Visible rises in passed, fully graded, unsaturated observations: {pair['passed_unsaturated_rises']}/{pair['passed_unsaturated_exposures']}.",
        f"Observations with sufficient matched background and direct-review controls: {pair['passed_control_supported_exposures']}.",
        f"Adjusted band-crossing response proxy: {pair['passed_response_strength_proxy']}. This is NOT the encompassing weight.",
        'Response proxy sensitivity to 0, 2, 4, 8 shrinkage observations: '+json.dumps(sensitivity(pair['passed_exposures'])), '',
        'Passing mixed-outcome activities are retained in a separate sensitivity calculation, matched by starting band and an accuracy class rounded to fifths. Some estimates rely on only one or two supported exposures. Lesson exposures are normalized against direct review controls; this is a coarse approximation. Unknown display thresholds, early-practice discounts, target speed, hidden state, and outcome order remain confounded.', '',
        'Nearby curriculum candidates (each still requires content review and transitive-path checking):']
    for p in candidates:
        lines.append(f"  {p['source']} -> {p['target']}: {p['source_title']} -> {p['target_title']}; {p['passed_unsaturated_rises']}/{p['passed_unsaturated_exposures']} passed unsaturated rises; prerequisite distance {p['prerequisite_distance']}.")
    lines += ['', 'Follow-up correctness and KP comparison: kp-effects/'+account+'-effects.txt. The leading explanation for matched differences is target state/history and visible threshold crossing. A flat intermediate band can hide positive credit; it is not a zero encompassing observation. Retain topic-level encompassing as the default model. The earlier content prior is a rough starting hypothesis, not an explanation of which particular questions earned credit.', '',
        'Recommendation: use the content-derived prior as an account-specific experimental candidate. Do not install every observed pair as a shared curriculum edge. Repeated distant or unrelated fluctuations, particularly those occurring after all-correct work, need an observation-model explanation before global FIRe tuning.', '',
        f'Full evidence: {account}.json. Content and proposed prior: {account}-recommendation.json. Method, engine implications, and schema suggestions: methods.txt.']
    (folder/(account+'-analysis.txt')).write_text('\n'.join(lines)+'\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    for account in PILOTS:
        prepare(args.folder.resolve(), account)


if __name__ == '__main__':
    main()
