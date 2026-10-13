#!/usr/bin/env python3
"""Account-local, chronological calibration experiment on frozen display captures.

Requires numpy. This fits an observation model, not the private engine. It never
transacts weights or changes policy. All feature histories precede the activity.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

import numpy as np

ACCOUNTS = ('foundations', 'linear', 'multivariable', 'differential')
DIRECT_CLOCK = 'hours_since_target_direct'
POTENTIAL_CLOCK = 'hours_since_potential_target_practice'
VARIANTS = {
    'spacing': {'growth': 2, 'clock': DIRECT_CLOCK},
    'constant': {'growth': 2, 'clock': None},
    'flat_display_scale': {'growth': 1, 'clock': DIRECT_CLOCK},
    'recent_possible_practice': {'growth': 2, 'clock': POTENTIAL_CLOCK},
}
GRID = {'half_life_hours': [6, 12, 24, 48, 96],
        'amplitude': [.25, .5, .75, 1, 1.5, 2, 3, 5],
        'residual': [.01, .05, .1, .2, .4, .6]}
WEIGHTS = np.linspace(.001, .999, 101)
RECOMMENDED_FRACTIONS = tuple(Fraction(s) for s in (
    '1/5', '1/4', '1/3', '2/5', '1/2', '3/5', '2/3', '3/4', '4/5', '1'))


def read(path):
    return json.loads(Path(path).read_text())


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')


def key(row):
    return str(row['source']), str(row['target'])


def recommended_fraction(weight):
    """Nearest user-selected positive fraction; exact midpoint ties go upward.

    Whether to create a relationship is a separate content/graph decision.
    """
    value = Fraction(str(weight))
    if not 0 <= value <= 1:
        raise ValueError('Coverage must be between zero and one')
    return min(RECOMMENDED_FRACTIONS, key=lambda f: (abs(f-value), -f))


def round_fraction(weight):
    return float(recommended_fraction(weight))


def split_tasks(audit, fraction=.7):
    ordered = sorted(audit, key=lambda r: (r['time'], str(r['task_id'])))
    ids = [str(r['task_id']) for r in ordered]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate task IDs within an account')
    if not 0 < fraction < 1 or len(ids) < 2:
        raise ValueError('A chronological split needs two tasks and a fraction between zero and one')
    cut = int(len(ids) * fraction)
    # Do not split tasks sharing the boundary timestamp.
    while 0 < cut < len(ids) and ordered[cut]['time'] == ordered[cut-1]['time']:
        cut += 1
    if cut == 0 or cut == len(ids):
        raise ValueError('Timestamp ties leave no nonempty chronological train/test split')
    return set(ids[:cut]), set(ids[cut:]), {
        'train_tasks': ids[:cut], 'test_tasks': ids[cut:],
        'last_train_time': ordered[cut-1]['time'],
        'first_test_time': ordered[cut]['time'],
    }


def age_pools(training, clock):
    """Unknown histories use training-only gap quantiles, never future outcomes."""
    result = {}
    if clock is None:
        return result
    for band in range(1, 6):
        specific = [r[clock] for r in training if r[clock] is not None and r['before'] == band]
        global_pool = [r[clock] for r in training if r[clock] is not None]
        selected = specific if len(specific) >= 8 else global_pool
        if not selected:
            raise ValueError('Cannot calibrate spacing without any known training ages')
        result[str(band)] = np.quantile(selected, np.linspace(.05, .95, 11)).tolist()
    return result


def dose(rows, model, pools):
    if not rows:
        return np.empty((0, 11))
    if model['clock'] is None:
        return np.full((len(rows), 11), model['amplitude'])
    ages = np.array([[r[model['clock']]] * 11 if r[model['clock']] is not None
                     else pools[str(r['before'])] for r in rows])
    half_lives = np.array([model['half_life_hours'] * model['growth'] ** (r['before']-1)
                          for r in rows])[:, None]
    discount = np.clip(2 * (1 - np.exp2(-ages / half_lives)), 0, 1)
    return model['amplitude'] * discount


def probabilities(rows, doses, residual, weight=1.):
    """Uniform within-band phase; seven-category residual allows signed anomalies."""
    n = len(rows)
    p = np.full((n, 7), residual / 7)
    if not n:
        return p
    mu = doses * weight
    lower = np.floor(mu).astype(int)
    fraction = mu - lower
    before = np.array([r['before'] for r in rows])[:, None]
    lo = np.minimum(6, before + lower)
    hi = np.minimum(6, lo + 1)
    row_index = np.broadcast_to(np.arange(n)[:, None], lo.shape)
    factor = (1 - residual) / doses.shape[1]
    np.add.at(p, (row_index, lo), factor * (1-fraction))
    np.add.at(p, (row_index, hi), factor * fraction)
    return p


def likelihood(rows, p):
    return float(np.log(p[np.arange(len(rows)), [r['after'] for r in rows]]).sum())


def fit_direct(rows, variant):
    spec = VARIANTS[variant]
    pools = age_pools(rows, spec['clock'])
    best = None
    hs = GRID['half_life_hours'] if spec['clock'] else [None]
    for h in hs:
        for a in GRID['amplitude']:
            model = dict(spec, half_life_hours=h, amplitude=a)
            doses = dose(rows, model, pools)
            for residual in GRID['residual']:
                p = probabilities(rows, doses, residual)
                score = likelihood(rows, p)
                if best is None or score > best['train_log_likelihood']:
                    best = dict(model, residual=residual, train_log_likelihood=score,
                                training_n=len(rows), age_quantiles=pools)
    return best


def predict(rows, model, weight=1.):
    return probabilities(rows, dose(rows, model, model['age_quantiles']), model['residual'], weight)


def fit_weight(rows, model, mean, strength):
    if not rows:
        return float(mean)
    doses = dose(rows, model, model['age_quantiles'])
    scores = [likelihood(rows, probabilities(rows, doses, model['residual'], w))
              + strength * (mean * math.log(w) + (1-mean) * math.log1p(-w)) for w in WEIGHTS]
    return float(WEIGHTS[int(np.argmax(scores))])


def rise_probability(rows, p):
    return np.array([sum(v[r['before']+1:]) for r, v in zip(rows, p)])


def metrics(rows, p=None, rising=None):
    if not rows:
        return {'n': 0}
    y = np.array([r['after'] > r['before'] for r in rows], dtype=float)
    if rising is None:
        rising = rise_probability(rows, p)
    result = {'n': len(rows), 'rises': int(y.sum()),
              'rise_brier': float(np.mean((y-rising)**2)),
              'predicted_rise_rate': float(np.mean(rising)),
              'observed_rise_rate': float(np.mean(y))}
    if p is not None:
        observed = np.array([r['positive_steps'] for r in rows])
        steps = np.maximum(0, np.arange(7)[None, :] - np.array([r['before'] for r in rows])[:, None])
        expected = (p * steps).sum(axis=1)
        result.update(category_log_loss=-likelihood(rows, p)/len(rows),
                      positive_step_mae=float(np.mean(abs(observed-expected))),
                      positive_step_mse=float(np.mean((observed-expected)**2)),
                      predicted_mean_steps=float(np.mean(expected)),
                      observed_mean_steps=float(np.mean(observed)))
        result.update(observed_fall_rate=sum(r['after'] < r['before'] for r in rows)/len(rows),
                      predicted_fall_rate=float(np.mean([sum(v[:r['before']]) for r,v in zip(rows,p)])))
    return result


def strata(rows):
    return {'all': list(range(len(rows))),
            'accuracy_60': [i for i, r in enumerate(rows) if abs(r['accuracy']-.6) < 1e-9],
            'perfect': [i for i, r in enumerate(rows) if r['accuracy'] == 1],
            'known_direct_age': [i for i, r in enumerate(rows) if r[DIRECT_CLOCK] is not None],
            'unknown_direct_age': [i for i, r in enumerate(rows) if r[DIRECT_CLOCK] is None],
            'legacy': [i for i, r in enumerate(rows) if r['pipeline'] == 'legacy'],
            'current': [i for i, r in enumerate(rows) if r['pipeline'] == 'current']}


def stratified(rows, p):
    return {k: metrics([rows[i] for i in ids], p[ids]) for k, ids in strata(rows).items()}


def empirical_direct(rows, training):
    """Fair, flexible no-clock comparator: starting-band transitions, additive .5."""
    counts = np.full((7, 7), .5)
    for r in training:
        counts[r['before'], r['after']] += 1
    counts /= counts.sum(axis=1)[:, None]
    return np.array([counts[r['before']] for r in rows]).reshape((-1, 7))


def compact_row(r):
    return {k: r[k] for k in ('account', 'task_id', 'source', 'target', 'before', 'after',
                             'positive_steps', 'accuracy', 'pipeline', DIRECT_CLOCK, POTENTIAL_CLOCK)}


def account_pilot(folder, account, priors):
    timing_path = folder / 'timing-magnitude' / (account+'.json')
    audit_path = folder / (account+'.json')
    timing, audit = read(timing_path), read(audit_path)
    rows = timing['observations']
    assert all(r['account'] == account for r in rows)
    train_ids, test_ids, split = split_tasks(audit['activity_audit'])
    assert all(str(r['task_id']) in train_ids | test_ids for r in rows)
    direct_train = [r for r in rows if r['direct'] and r['kind']=='review' and str(r['task_id']) in train_ids]
    direct_test = [r for r in rows if r['direct'] and r['kind']=='review' and str(r['task_id']) in test_ids]
    models = {name: fit_direct(direct_train, name) for name in VARIANTS}
    direct_predictions = {name: predict(direct_test, model) for name, model in models.items()}
    direct_predictions['empirical_starting_band'] = empirical_direct(direct_test, direct_train)
    direct_results = {name: stratified(direct_test, p) for name, p in direct_predictions.items()}

    implicit = defaultdict(list)
    for r in rows:
        if not r['direct']:
            implicit[key(r)].append(r)
    # Do not use timing['nominated']: that field knows full-period outcomes.
    nominated = {k for k, group in implicit.items()
                 if any(str(r['task_id']) in train_ids and r['after'] > r['before'] for r in group)}
    content = {(str(p['source']), str(p['target'])): p for p in priors if p['account']==account}
    pairs, heldout = [], []
    for k in sorted(nominated | set(content)):
        group = implicit[k]
        train = [r for r in group if str(r['task_id']) in train_ids]
        test = [r for r in group if str(r['task_id']) in test_ids]
        prior = content.get(k)
        mean, strength = (prior['prior_mean'], 2.) if prior else (.5, 1.)
        frequency = sum(r['after'] > r['before'] for r in train)/len(train) if train else None
        smoothed_frequency = (sum(r['after'] > r['before'] for r in train) + strength*mean)/(len(train)+strength)
        fitted = {name: fit_weight(train, model, mean, strength) for name, model in models.items()}
        pair = dict(account=account, source=k[0], target=k[1], train_n=len(train), test_n=len(test),
                    training_rises=sum(r['after'] > r['before'] for r in train),
                    train_frequency=frequency, smoothed_frequency=smoothed_frequency, prior_mean=mean, prior_strength=strength,
                    content_prior=bool(prior), selected_from_training_rise=k in nominated,
                    training_weights=fitted)
        if prior:
            pair.update(source_title=prior['source_title'], target_title=prior['target_title'],
                        content_range=prior['plausible_content_range'], content_role=prior['pilot_role'])
        pairs.append(pair)
        p_fit = {name: predict(test, model, fitted[name]) for name, model in models.items()}
        p_fit['fraction_spacing'] = predict(test, models['spacing'], round_fraction(fitted['spacing']))
        p_freq = predict(test, models['spacing'], frequency) if frequency is not None else None
        p_smooth = predict(test, models['spacing'], smoothed_frequency)
        for i, r in enumerate(test):
            heldout.append(dict(compact_row(r), content_prior=bool(prior),
                                training_n=len(train), selected_from_training_rise=k in nominated,
                                train_frequency=frequency,
                                smoothed_frequency=smoothed_frequency,
                                predictions={name: p[i].tolist() for name, p in p_fit.items()},
                                frequency_in_spacing=p_freq[i].tolist() if p_freq is not None else None,
                                smoothed_frequency_in_spacing=p_smooth[i].tolist()))

    panels = {}
    for label, selection in (
        ('training_nominated', lambda r:r['selected_from_training_rise']),
        ('content_with_training', lambda r:r['content_prior'] and r['training_n']>0),
        ('content_without_training', lambda r:r['content_prior'] and r['training_n']==0),
        ('single_training_observation', lambda r:r['selected_from_training_rise'] and r['training_n']==1),
    ):
        sample = [r for r in heldout if selection(r)]
        panel = {name: metrics(sample, np.array([r['predictions'][name] for r in sample]))
                 for name in [*models, 'fraction_spacing']}
        with_frequency = [r for r in sample if r['train_frequency'] is not None]
        panel['original_frequency'] = metrics(with_frequency, rising=np.array([r['train_frequency'] for r in with_frequency]))
        panel['frequency_in_spacing'] = metrics(with_frequency, np.array([r['frequency_in_spacing'] for r in with_frequency]))
        panel['smoothed_frequency'] = metrics(sample, rising=np.array([r['smoothed_frequency'] for r in sample]))
        panel['smoothed_frequency_in_spacing'] = metrics(sample, np.array([r['smoothed_frequency_in_spacing'] for r in sample]))
        panels[label] = panel

    # Final estimates use all available observations only AFTER test predictions are fixed.
    full_direct = direct_train + direct_test
    full_models = {name: fit_direct(full_direct, name) for name in VARIANTS}
    for pair in pairs:
        if not pair['content_prior']:
            continue
        group = implicit[key(pair)]
        pair['all_observations_n'] = len(group)
        pair['all_observations_frequency'] = (sum(r['after'] > r['before'] for r in group)/len(group)) if group else None
        pair['all_observations_weights'] = {
            name: fit_weight(group, model, pair['prior_mean'], pair['prior_strength'])
            for name, model in full_models.items()}
        pair['recommended_fraction_weight'] = round_fraction(pair['all_observations_weights']['spacing'])
        pair['recommended_fraction'] = str(recommended_fraction(pair['all_observations_weights']['spacing']))
        pair['sequence'] = [dict(compact_row(r), split='train' if str(r['task_id']) in train_ids else 'test') for r in group]
    return dict(account=account, source_files={str(p): digest(p) for p in (timing_path, audit_path)},
                split=split, models_trained_on_early_data=models,
                direct_test_results=direct_results, panels=panels, pairs=pairs,
                direct_test_predictions=[dict(compact_row(r), predictions={name:p[i].tolist() for name,p in direct_predictions.items()})
                                         for i,r in enumerate(direct_test)],
                relationship_test_predictions=heldout, full_data_models=full_models)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--folder', type=Path, default=Path('reference/mathacademy/encompassing-analysis-2026-10-11'))
    args = parser.parse_args()
    out = args.folder / 'calibration-pilot'
    out.mkdir(exist_ok=True)
    prior_path = out / 'content-priors.json'
    priors = read(prior_path)['relationships']
    spec = dict(schema_version=1, contributor='Codex assistant',
                purpose='Concrete calibration pilot and best-guess inputs; no database mutation.',
                split='Earliest 70% of all frozen activities in each account train; remaining tasks test. Ties stay together.',
                selection='Broad panel: at least one training rise. No minimum activity count. Content panel: nine retrospectively chosen mathematical relationships.',
                variants=VARIANTS, direct_grid=GRID, weight_grid=WEIGHTS.tolist(),
                prior='Beta(1+strength*mean, 1+strength*(1-mean)); content strength2, other pairs strength1 mean.5.',
                residual='Uniform probability on categories0..6, mixed with positive-only display increments.',
                comparison='Original training K/N evaluated using Brier; same K/N also fed through spacing model for full-category comparison.',
                final_refit='Only final content-pair estimates and full_data_models see later observations; heldout predictions do not.',
                rounding='Nearest allowed positive fraction by absolute distance from unrounded fit, ties upward. Whether to create an explicit relationship is a separate content/graph decision.',
                allowed_recommendation_fractions=[str(f) for f in RECOMMENDED_FRACTIONS],
                content_priors_sha256=digest(prior_path), script_sha256=digest(__file__))
    write(out / 'experiment.json', spec)
    for account in ACCOUNTS:
        result = account_pilot(args.folder, account, priors)
        write(out / (account+'.json'), result)
        print(account, 'direct', {k:v['all'] for k,v in result['direct_test_results'].items()}, flush=True)
        print(account, 'relations', result['panels']['training_nominated'], flush=True)
        print(account, 'content', [{k:p[k] for k in ('source','target','all_observations_n','all_observations_weights')} for p in result['pairs'] if p['content_prior']], flush=True)


if __name__ == '__main__':
    main()
