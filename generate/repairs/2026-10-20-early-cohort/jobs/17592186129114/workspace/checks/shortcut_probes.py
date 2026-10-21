"""Visible-record shortcut probes on delivered pools and controlled records."""
from collections import Counter
from common import *

probes = []
pool_paths = [E / f'batch-{seed}/accepted.json' for seed in (924724049, 0, 802139, 920113)]
small = load(E / 'small-batches/accepted.json')
counts = load(E / 'validation-results.json')['counts']
pools = [(str(path.relative_to(ROOT)), load(path)) for path in pool_paths]
for item in counts:
    if item['count'] >= 3:
        pools.append((f"small-count-{item['count']}-seed-{item['seed']}",
                      [r for r in small if r['generation']['seed'] in item['accepted_seeds']]))

for name, rs in pools:
    cov = coverage(rs)
    for group_name, data in cov.items():
        subsets = data['subsets']
        subset_counts = Counter(subsets)
        correct_counts = Counter(map(len, subsets))
        n = len(subsets)
        role_best = {x: max(v.values()) for x,v in data['roles'].items()}
        tested = n >= 3
        if tested:
            assert max(role_best.values()) < n
            assert max(subset_counts.values()) < n
            assert max(correct_counts.values()) < n, 'Investigate fixed-count cue'
        probes.append({'input': name, 'group': group_name, 'attempts': n,
            'label_or_position_best_correct': role_best,
            'always_select_C_correct': data['roles']['C']['selected'],
            'best_fixed_subset_correct': max(subset_counts.values()),
            'best_fixed_selection_count_correct': max(correct_counts.values()),
            'subsets': dict(subset_counts), 'selection_counts': dict(correct_counts),
            'tested_for_constant_actions': tested,
            'limitation': None if tested else 'Singleton/pair: no conditional coverage claim; role support tested by preserved sampler and controlled witnesses.'})

cf = delivery(load(E / 'counterfactual-records.json'), 'counterfactual-delivery')
assert [examine(r)['subset'] for r in cf] == ['ABC','AB','ABC']
grader(cf, 'counterfactual-delivery')
save(E / 'shortcut-probes.json', {'passed': True, 'probes': probes,
    'interpretation': 'Counts test exact finite delivered pools, not statistical significance or every possible learner history. Positions coincide with A/B/C in normal generation. Full subset and selection-count rules have counterexamples in every tested group of >=3.',
    'counterfactual': {'same_shape_and_other_matrices': True, 'single_pivot_edit': 'C[2,1] 0 -> 1',
        'visible_subsets_after_delivery': [examine(r)['subset'] for r in cf],
        'actual_grader_checks': 18, 'irrelevant_trailing_edit_preserves_subset': True},
    'fixed_shape_support': 'decision-cases/accepted.json contains all seven nonempty subsets; controlled cell edits change matrix evidence while preserving dimensions, labels, polarity, and other matrices.',
    'mathematical_cues': 'Zero rows and leading-column patterns are the intended evidence (tutorial conditions I/II), so shortcuts using these are valid skill use.'})

inv = load(JOB / 'source/inventory.json')
rated = [q for q in inv['questions'] if q.get(':question/difficulty',{}).get(':db/ident') == ':question.difficulty/easy']
# Original source solution typos are retained in inventory. Classify visible
# matrices and verify their keys here; corrected replay solutions are tested above.
hist = Counter(examine(q, solution=False)['subset'] for q in rated)
save(E / 'selection-limits.json', {'captured_basis': inv['basis'], 'captured_candidates': len(inv['questions']),
    'complete_easy_candidates': len(rated), 'unrated_excluded_from_easy_scenario': len(inv['questions'])-len(rated),
    'captured_easy_subsets': dict(hist),
    'implementation': 'engine/rust/question_selection.rs: seen_before_task and select (read-only inspection)',
    'easy_selection': 'Given a positive easy weight and no freshness exclusions, select() chooses uniformly within the easy band. Other weights do not split this all-easy incoming cohort. Unconfigured policy chooses lowest entity ID.',
    'limits': ['No live learner history, configured distribution, new entity IDs or database identity collisions were available.',
        'The native selector chooses an individual item, not a coverage-balanced sequence. History can remove counterexamples; construction-time pool coverage does not guarantee every arbitrary subsequence.',
        'The shared delivery check uses the captured inventory and cannot predict concurrent publication. Each tested current five-item pool survives all five records.',
        'All captured non-source generated questions were reconstructed, not merely sampled. Their five-record stored cohort still has fixed C; no database repair or publication was performed.']})
print(json.dumps({'passed': True, 'pools': len(pools), 'tested_groups': sum(p['tested_for_constant_actions'] for p in probes),
                  'counterfactuals_delivered': len(cf), 'captured_easy_inventory': len(rated)}))
