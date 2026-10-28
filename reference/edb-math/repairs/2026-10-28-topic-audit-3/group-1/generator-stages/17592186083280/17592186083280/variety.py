"""Exhaust actual public normal parameter representatives and canonical tasks.

Nonzero component multipliers and translations are quotiented out; each relevant
coefficient ratio, root radicand, frequency, phase and interval is still enumerated.
There are no hardcoded task-count products. Counts are hashes of rendered records.
"""
from itertools import product
import sympy as s

def representatives(g,name):
    anchor=dict(g.TEMPLATES[name][2])
    domains={
        'exponential':{'b':range(1,6),'c':range(1,13),'u':range(2,9)},
        'logarithmic':{'k':range(2,9)},
        'quadratic':{'b':range(1,5),'c':range(2,25)},
        'cubic':{'n':range(2,13)},
        'shifted_trig':{'p':('1/3','1/4','1/6')},
        'frequency_trig':{'k':range(2,7)},
        'legacy_trig':{'k':range(2,7)},
        'two_period_trig':{'k':range(2,7),'p':tuple(str(v)for v in g.HARD_PHASE_INPUTS),'q':g.HARD_INTERVAL_SHIFTS},
    }[name]
    # These parameters do not affect zero sets or regularity. Parameter bounds
    # still apply to every public record; validate.py tests independent scaling.
    for key in ('a','b','l','m'): 
        if key in anchor and key not in domains:anchor[key]=1
    if name=='exponential':anchor['k']=1
    if 'h'in anchor:anchor['h']=1 if name=='cubic'else 0
    if 'j'in anchor:anchor['j']=0
    for values in product(*domains.values()):yield {**anchor,**dict(zip(domains,values))}

def enumerate_tasks(g,verify):
    summary={};catalog={};records={}
    for name,(level,_,_)in g.TEMPLATES.items():
        tasks={};attempts=0;rejections={}
        for p in representatives(g,name):
            attempts+=1
            try:r=g.generate(level,template=name,parameters=p)
            except ValueError as exc:
                reason=str(exc);rejections[reason]=rejections.get(reason,0)+1;continue
            verify(r)
            task=r['generation']['mathematical_fingerprint']
            tasks.setdefault(task,{'fingerprint':task,'task':r['generation']['mathematical_task'],'representative_parameters':p})
            records.setdefault(task,r)
        summary[name]={'parameter_representatives_attempted':attempts,'rejected_representatives':rejections,'canonical_tasks':len(tasks)}
        catalog[name]=[tasks[k]for k in sorted(tasks)]
    levels={}
    for level in ('easy','moderate','hard'):
        hashes={entry['fingerprint']for name,entries in catalog.items()if g.TEMPLATES[name][0]==level for entry in entries}
        levels[level]=len(hashes)
    return {'method':'render public normal records, read displayed mathematics independently, deduplicate zero-candidate/regularity/domain fingerprints','families':summary,'deduplicated_level_counts':levels,'catalog':catalog},records
