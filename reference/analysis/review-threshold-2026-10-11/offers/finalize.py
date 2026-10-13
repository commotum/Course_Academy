"""Enrich raw-linked offers with conservative timing contrasts; no capture writes."""
import csv
import json
import statistics
from collections import Counter
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
ACCOUNTS = ['foundations','linear','multivariable','differential']


def stats(rows):
    ages=sorted(r['hours_since_last_pass'] for r in rows if r['hours_since_last_pass'] is not None)
    return dict(n=len(rows), known_ages=len(ages), min_hours=min(ages) if ages else None,
        median_hours=statistics.median(ages) if ages else None,
        q25_hours=ages[int((len(ages)-1)*.25)] if ages else None,
        q75_hours=ages[int((len(ages)-1)*.75)] if ages else None,
        max_hours=max(ages) if ages else None,
        median_offer_bracket_minutes=statistics.median(r['offer_bracket_seconds']/60 for r in rows if r['offer_bracket_seconds'] is not None) if rows else None,
        with_intervening_assessment=sum(bool(r['intervening_assessment_tasks']) for r in rows),
        with_intervening_visible_rise=sum(r['visible_rise_sources_since_last_pass']>0 for r in rows))


all_rows,summaries=[],[]
for account in ACCOUNTS:
    path=OUT/(account+'.json')
    data=json.loads(path.read_text())
    manifest=json.loads((ROOT/'reference/mathacademy/encompassing-analysis-2026-10-11'/(account+'.json')).read_text())
    events={r['task_id']:r for r in manifest['activity_audit']}
    for row in data['offers']:
        prior=events.get(row['prior_direct_task'])
        # Drop the previous direct activity's own after snapshots.
        row['visible_changes_since_last_pass']=[c for c in row['visible_changes_since_last_pass'] if prior and c['at']>prior['finished_at']]
        row['visible_rise_sources_since_last_pass']=len({c['source'] for c in row['visible_changes_since_last_pass'] if c['after']>c['before']})
        row['intervening_assessment_tasks']=[e['task_id'] for e in events.values() if prior and e['kind']=='assessment' and prior['time']<e['time']<row['first_offer_at']]
        row['prior_direct_pass_ordinal']=sum(e['kind'] in ('lesson','review') and e['source']==row['topic_id'] and e['outcome']=='passed' and e['time']<=prior['time'] for e in events.values()) if prior else None
    base=[r for r in data['offers'] if r['classification']=='no_captured_remediation_trigger' and
        r['band'] is not None and r['band_age_hours'] is not None and r['band_age_hours']<=1 and
        r['hours_since_last_pass'] is not None and not r['prior_direct_time_recovered_late']]
    no_assessment=[r for r in base if not r['intervening_assessment_tasks']]
    conservative=[r for r in no_assessment if not r['visible_rise_sources_since_last_pass']]
    comparisons={}
    for name,rows in [('fresh_known_band_no_captured_trigger',base),('no_intervening_assessment',no_assessment),
        ('no_intervening_assessment_or_visible_rise',conservative)]:
        comparisons[name]={str(b):{kind:stats([r for r in rows if r['band']==b and r['prior_direct_kind']==kind])
            for kind in ['lesson','review']} for b in [1,2]}
    data['summary']['timing_contrasts']=comparisons
    data['summary']['fresh_known_band_no_captured_trigger']=stats(base)
    data['summary']['conservative_first_captured_pass_lesson_by_band']={str(b):stats([r for r in conservative if r['band']==b and r['prior_direct_kind']=='lesson' and r['prior_direct_pass_ordinal']==1]) for b in [1,2]}
    data['summary']['offer_classification_caution']='No captured remediation trigger is not proof of ordinary spacing. Missing visible rises do not prove missing fractional implicit credit.'
    path.write_text(json.dumps(data,indent=2)+'\n')
    summaries.append(data['summary'])
    all_rows.extend(data['offers'])
    print(account,json.dumps(comparisons['no_intervening_assessment_or_visible_rise']),flush=True)
(OUT/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
fields=[k for k in all_rows[0] if k not in ('band_evidence','visible_changes_since_last_pass')]
with (OUT/'first-review-offers.csv').open('w') as file:
    writer=csv.DictWriter(file,fieldnames=fields)
    writer.writeheader()
    writer.writerows({k:r[k] for k in fields} for r in all_rows)
