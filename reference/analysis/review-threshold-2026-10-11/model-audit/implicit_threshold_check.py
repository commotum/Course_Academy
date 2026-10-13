#!/usr/bin/env python3
"""Hold coverage estimates fixed while varying target-specific timing response.

The primary panel is selected entirely from early data, and predictions are
scored only on later activities. This is a sensitivity check of implicit-credit
color observations, not an inference that the display measures memory.
"""
import json
import numpy as np
from profile_threshold import ACCOUNTS, SOURCE, OUT, digest, metrics


def key(r):
    return str(r['source']), str(r['target'])


def run():
    profiles = json.loads((OUT/'threshold-profile.json').read_text())
    result = {'interpretation': 'Color changes are observed proxies for fractional implicit repetition earned through other topics; ordinal thresholds and timing scale remain unknown.',
              'design': 'Freeze account-local coverage weights fitted only on early pilot observations; score later implicit observations at each direct-reference timing threshold. Keep all targets from a task together.',
              'selection': 'Relationships with at least one implicit rise in early training; known pre-activity direct-target ages only; no minimum support cutoff.',
              'coverage_warning': 'Original pilot fitted these weights at threshold 0.5 and its own display calibration. Holding them fixed makes this a conditional robustness check; joint refitting could trade coverage against timing.',
              'accounts': {}}
    for account in ACCOUNTS:
        pilot_path = SOURCE/'calibration-pilot'/(account+'.json')
        timing_path = SOURCE/'timing-magnitude'/(account+'.json')
        pilot = json.loads(pilot_path.read_text())
        timing = json.loads(timing_path.read_text())
        pairs = {key(p): p for p in pilot['pairs'] if p['selected_from_training_rise']}
        test_ids = set(pilot['split']['test_tasks'])
        clock = 'hours_since_target_direct'
        rows = [r for r in timing['observations'] if not r['direct'] and key(r) in pairs
                and str(r['task_id']) in test_ids and r[clock] is not None]
        assert all(r['account']==account for r in rows)
        weights = np.array([pairs[key(r)]['training_weights']['spacing'] for r in rows])
        frequency = np.array([pairs[key(r)]['train_frequency'] for r in rows])
        direct = profiles['accounts'][account]['variants']['direct_known']
        threshold_rows=[]
        for model in direct['profile']:
            threshold_rows.append({'threshold': model['threshold'],
                                   'direct_training_selected': model['threshold']==direct['selected_from_training']['threshold'],
                                   'fitted_coverage_metrics': metrics(rows,model,clock,weights),
                                   'frequency_coverage_metrics': metrics(rows,model,clock,frequency)})
        result['accounts'][account] = {'test_rows': len(rows),
                                      'test_tasks': len(set(r['task_id'] for r in rows)),
                                      'test_pairs': len(set(key(r) for r in rows)),
                                      'threshold_profiles': threshold_rows,
                                      'rows':[{k:r[k] for k in ('account','task_id','source','target','before','after',clock)} | {'coverage':float(w)} for r,w in zip(rows,weights)],
                                      'source_sha256': {str(pilot_path):digest(pilot_path),str(timing_path):digest(timing_path)}}
        print(account,'n',len(rows),'tasks',result['accounts'][account]['test_tasks'])
        for r in threshold_rows:
            if r['threshold'] in [.5,.9]:
                print(r['threshold'],r['fitted_coverage_metrics'])
    (OUT/'implicit-threshold-check.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':
    run()
