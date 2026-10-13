#!/usr/bin/env python3
"""Threshold sensitivity of a color-response model; NOT a scheduler due-state fit.

Preserves original frozen per-account 70/30 task split. Fits known ages only;
never imputes upstream memory or treats color categories as actual repetitions.
Run using /home/jake/Developer/MA/.venv/bin/python.
"""
from pathlib import Path
import hashlib
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'reference/mathacademy/encompassing-analysis-2026-10-11'
OUT = Path(__file__).resolve().parent
ACCOUNTS = ('foundations', 'linear', 'multivariable', 'differential')
THRESHOLDS = [.2, .3, .4, .5, .6, .7, .8, .9]
HALF_LIVES = [6 * 2 ** (i / 4) for i in range(25)]
AMPLITUDES = [i / 10 for i in range(1, 21)] + [2.5, 3, 4, 5]
RESIDUALS = [.01, .05, .1, .2, .4, .6]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def arrays(rows, clock):
    return (np.array([r['before'] for r in rows], dtype=int),
            np.array([r['after'] for r in rows], dtype=int),
            np.array([r[clock] for r in rows]))


def probabilities(rows, model, clock, weights=1.):
    b, y, h = arrays(rows, clock)
    mu = weights * model['amplitude'] * np.clip((1 - np.exp2(-h / (model['half_life_band_1_hours'] * 2 ** (b-1)))) / (1-model['threshold']), 0, 1)
    lower = np.floor(mu).astype(int)
    frac = mu - lower
    p = np.full((len(rows), 7), model['residual'] / 7)
    ix = np.arange(len(rows))
    np.add.at(p, (ix, np.minimum(6, b+lower)), (1-model['residual'])*(1-frac))
    np.add.at(p, (ix, np.minimum(6, b+lower+1)), (1-model['residual'])*frac)
    return p


def metrics(rows, model, clock, weights=1.):
    b, y, h = arrays(rows, clock)
    if not len(rows):
        return {'n': 0}
    p = probabilities(rows, model, clock, weights)
    rise = (p * (np.arange(7)[None, :] > b[:, None])).sum(axis=1)
    return {'n': len(rows),
            'category_log_loss': float(-np.log(p[np.arange(len(rows)), y]).mean()),
            'crossing_brier': float(np.mean((rise - (y > b)) ** 2)),
            'predicted_rise_rate': float(rise.mean()),
            'observed_rise_rate': float((y > b).mean())}


def profile(rows, clock):
    b, y, h = arrays(rows, clock)
    result = []
    for threshold in THRESHOLDS:
        best = None
        for half_life in HALF_LIVES:
            discount = np.clip((1-np.exp2(-h/(half_life*2**(b-1)))) / (1-threshold), 0, 1)
            for amplitude in AMPLITUDES:
                mu = amplitude * discount
                lower = np.floor(mu).astype(int)
                frac = mu-lower
                ordinary = ((y == np.minimum(6,b+lower)) * (1-frac)
                            + (y == np.minimum(6,b+lower+1)) * frac)
                for residual in RESIDUALS:
                    score = float(np.log((1-residual)*ordinary+residual/7).sum())
                    if best is None or score > best['train_log_likelihood']:
                        best = {'threshold': threshold,
                                'half_life_band_1_hours': half_life,
                                'band_1_discount_saturation_hours': half_life * math.log2(1/threshold),
                                'amplitude': amplitude, 'residual': residual,
                                'train_log_likelihood': score, 'training_n': len(rows)}
        result.append(best)
    return result


def run():
    result = {'method': 'Profile conditional color-response likelihood with T varied; this does not label or fit scheduler due states.',
              'formula': 'mu = A * clip((1 - 2**(-h / (H1 * 2**(before_band-1)))) / (1-T), 0, 1)',
              'caveats': ['Band spacing and exponential growth are assumptions, not observed numeric state.',
                          'Direct age may omit implicit refreshes; potential-practice age may falsely refresh on non-encompassing prerequisites.',
                          'Reviews include remediation, early review, and unknown selection mechanisms.',
                          'Account-specific serial observations are not independent trials.',
                          'Quality/ability/display calibration can trade off against amplitude and half-life.'],
              'threshold_grid': THRESHOLDS, 'half_life_grid_hours': HALF_LIVES,
              'amplitude_grid': AMPLITUDES, 'residual_grid': RESIDUALS,
              'accounts': {}}
    for account in ACCOUNTS:
        timing_path = SOURCE / 'timing-magnitude' / (account+'.json')
        pilot_path = SOURCE / 'calibration-pilot' / (account+'.json')
        timing = json.loads(timing_path.read_text())
        split = json.loads(pilot_path.read_text())['split']
        train_ids, test_ids = set(split['train_tasks']), set(split['test_tasks'])
        assert not train_ids & test_ids
        direct = [r for r in timing['observations'] if r['direct'] and r['kind']=='review']
        assert all(r['account']==account and str(r['task_id']) in train_ids | test_ids for r in direct)
        output = {'source_sha256': {str(timing_path.relative_to(ROOT)): digest(timing_path),
                                    str(pilot_path.relative_to(ROOT)): digest(pilot_path)},
                  'all_direct_reviews': len(direct), 'split_last_train_time': split['last_train_time'],
                  'split_first_test_time': split['first_test_time'], 'variants': {}}
        for name, clock, controlled in [('direct_known', 'hours_since_target_direct', False),
                                        ('direct_band1_accuracy60', 'hours_since_target_direct', True),
                                        ('potential_known', 'hours_since_potential_target_practice', False)]:
            rows = [r for r in direct if r[clock] is not None and (not controlled or r['before']==1 and abs(r['accuracy']-.6)<1e-9)]
            training = [r for r in rows if str(r['task_id']) in train_ids]
            testing = [r for r in rows if str(r['task_id']) in test_ids]
            fitted = profile(training, clock)
            selected = max(fitted, key=lambda f: f['train_log_likelihood'])
            fixed = next(f for f in fitted if f['threshold']==.5)
            for f in fitted:
                f['delta_train_log_likelihood_from_best'] = f['train_log_likelihood'] - selected['train_log_likelihood']
                f['test_metrics'] = metrics(testing, f, clock)
            variant = {'clock': clock, 'training_n': len(training), 'testing_n': len(testing),
                       'profile': fitted, 'selected_from_training': selected,
                       'fixed_threshold_05': fixed,
                       'rows': [{k: r[k] for k in ('account','task_id','source','target','before','after','accuracy',clock)} | {'split': 'train' if str(r['task_id']) in train_ids else 'test'} for r in rows]}
            if name=='direct_known':
                all_profile = profile(rows, clock)
                variant['full_data_profile_not_heldout'] = all_profile
                variant['full_data_selected_not_heldout'] = max(all_profile, key=lambda f: f['train_log_likelihood'])
            output['variants'][name] = variant
            print(account, name, 'n',len(training),len(testing),'T',selected['threshold'],
                  'H',round(selected['half_life_band_1_hours'],2),'A',selected['amplitude'],
                  'test log loss',round(selected['test_metrics']['category_log_loss'],4),
                  'vs T=.5', round(fixed['test_metrics']['category_log_loss'],4),flush=True)
        result['accounts'][account] = output
    # Different choices generate identical first-review times when H is scaled.
    result['timing_nonidentifiability_example'] = [
        {'threshold': t, 'half_life_hours': 48/math.log2(1/t),
         'due_time_hours_from_memory_1': 48} for t in THRESHOLDS]
    (OUT/'threshold-profile.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':
    run()
