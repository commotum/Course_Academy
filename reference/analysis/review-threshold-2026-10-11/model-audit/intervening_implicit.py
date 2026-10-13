#!/usr/bin/env python3
"""Stratify direct-reference responses by captured intervening implicit credit.

Visible rises are lower-resolution evidence of fractional credit, not a complete
credit ledger: a flat band can also contain positive fractional repetition.
"""
from collections import defaultdict
from datetime import datetime
import json
import numpy as np
from profile_threshold import ACCOUNTS, SOURCE, OUT, metrics, profile


def stamp(row):
    return datetime.fromisoformat(row['at']).timestamp()


def describe(rows):
    if not rows:
        return {'n':0}
    def median(k):
        return float(np.median([r[k] for r in rows if r[k] is not None]))
    return {'n':len(rows),'rising_fraction':float(np.mean([r['after']>r['before'] for r in rows])),
            'median_direct_age_hours':median('hours_since_target_direct'),
            'median_potential_practice_age_hours':median('hours_since_potential_target_practice'),
            'median_prior_implicit_rises':median('intervening_implicit_rises'),
            'median_prior_implicit_exposures':median('intervening_implicit_exposures')}


def run():
    base=json.loads((OUT/'threshold-profile.json').read_text())
    result={'method':'For each target, count eligible captured implicit exposures and rises strictly after its prior captured direct practice and before the current direct review.',
            'limits':['An observed rise establishes visible implicit-credit evidence; a flat band can still receive fractional credit.',
                      'Structural potential practice overcounts true encompassing practice. No potential practice is a conservative captured-history subset, not proof of globally complete history.',
                      'Direct-review completions and band response are not ordinary due-state labels.',
                      'This is stratification and a clean-subset response fit, not replay of an unobserved upstream numerical memory state.'],
            'accounts':{}}
    for account in ACCOUNTS:
        timing=json.loads((SOURCE/'timing-magnitude'/(account+'.json')).read_text())
        pilot=json.loads((SOURCE/'calibration-pilot'/(account+'.json')).read_text())
        train_ids=set(pilot['split']['train_tasks'])
        implicit=defaultdict(list)
        for row in timing['observations']:
            if not row['direct']:
                implicit[str(row['target'])].append((stamp(row),row))
        for values in implicit.values():
            values.sort(key=lambda pair:pair[0])
        rows=[]
        for original in timing['observations']:
            if not original['direct'] or original['kind']!='review' or original['hours_since_target_direct'] is None:
                continue
            row=dict(original)
            now=stamp(row)
            then=now-row['hours_since_target_direct']*3600
            exposures=[other for at,other in implicit[str(row['target'])] if then+0.01<at<now-0.01]
            rises=[r for r in exposures if r['after']>r['before']]
            row.update(intervening_implicit_exposures=len(exposures),intervening_implicit_rises=len(rises),
                       observed_implicit_palette_steps=sum(r['after']-r['before'] for r in rises),
                       intervening_rise_task_ids=[r['task_id'] for r in rises],
                       no_intervening_potential_practice=(row['hours_since_potential_target_practice'] is not None
                                                         and row['hours_since_potential_target_practice']>=row['hours_since_target_direct']-0.01/3600),
                       split='train' if str(row['task_id']) in train_ids else 'test')
            rows.append(row)
        strata={'all':rows,
                'observed_intervening_implicit_rise':[r for r in rows if r['intervening_implicit_rises']>0],
                'no_observed_intervening_implicit_rise':[r for r in rows if r['intervening_implicit_rises']==0],
                'no_intervening_potential_practice':[r for r in rows if r['no_intervening_potential_practice']]}
        models=base['accounts'][account]['variants']['direct_known']['profile']
        fixed=next(m for m in models if m['threshold']==.5)
        selected=base['accounts'][account]['variants']['direct_known']['selected_from_training']
        summary={}
        for name,subset in strata.items():
            later=[r for r in subset if r['split']=='test']
            summary[name]={'all_descriptive':describe(subset),
                           'band1_accuracy60_descriptive':describe([r for r in subset if r['before']==1 and abs(r['accuracy']-.6)<1e-9]),
                           'later_fixed_threshold05_metrics':metrics(later,fixed,'hours_since_target_direct'),
                           'later_training_selected_metrics':metrics(later,selected,'hours_since_target_direct')}
        clean=strata['no_intervening_potential_practice']
        training=[r for r in clean if r['split']=='train'];testing=[r for r in clean if r['split']=='test']
        clean_fit={'train_n':len(training),'test_n':len(testing)}
        if len(training)>=10 and len(testing)>=5:
            fitted=profile(training,'hours_since_target_direct')
            for m in fitted:m['test_metrics']=metrics(testing,m,'hours_since_target_direct')
            clean_fit.update(profile=fitted,selected_from_training=max(fitted,key=lambda x:x['train_log_likelihood']))
        result['accounts'][account]={'strata':summary,'clean_subset_fit':clean_fit,
                                    'rows':[{k:r[k] for k in ('account','task_id','source','target','before','after','accuracy','hours_since_target_direct','hours_since_potential_target_practice','intervening_implicit_exposures','intervening_implicit_rises','observed_implicit_palette_steps','intervening_rise_task_ids','no_intervening_potential_practice','split')} for r in rows]}
        print(account,{k:v['all_descriptive']['n'] for k,v in summary.items()},'clean fit',
              clean_fit.get('selected_from_training',{}).get('threshold'),len(training),len(testing),flush=True)
    (OUT/'intervening-implicit.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__':run()
