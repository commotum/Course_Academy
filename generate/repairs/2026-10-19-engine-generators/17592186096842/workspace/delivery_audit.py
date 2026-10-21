#!/usr/bin/env python3
"""Read-only coverage comparison and the selector's within-band seeded draw."""
import json,hashlib,collections,math
from pathlib import Path
from validate import coverage,save,key,field
accepted=[];stages={}
for band in ['easy','moderate','hard']:
    rs=json.load(open('evidence/delivery-'+band+'/accepted.json'));accepted+=rs
    report=json.load(open('evidence/delivery-'+band+'/delivery.json'))
    stages[band]={'input':len(json.load(open('evidence/probes-'+band+'.json'))),'accepted':len(rs)}
after=coverage(accepted);save('pedagogical-variation-after.json',after)
# Native select() uniformly indexes the sorted eligible entity-ID pool after
# choosing a difficulty. Entity IDs are not assigned yet; use stable synthetic
# IDs for read-only reproduction of that final index draw. Test one draw per
# captured candidate; live history/policies are not inferred from this stand-in.
selected=[]
for band in ['easy','moderate','hard']:
    pool=sorted([r for r in accepted if r['question'][':question/difficulty'].endswith('/'+band)],key=lambda r:r['question'][':question/id'])
    for i in range(len(pool)):
        digest=hashlib.sha256(('course-academy/question-selection/v1/author-'+band+'-'+str(i)).encode()).digest()
        uniform=(int.from_bytes(digest[8:16],'big')>>11)/2**53
        selected.append(pool[math.floor(uniform*len(pool))])
save('selection-records.json',selected);save('pedagogical-variation-selection.json',coverage(selected))
probes=[]
for stage,records in [('raw',json.load(open('evidence/probe-records.json'))),('delivery',accepted),('synthetic_selection',selected)]:
    cov=coverage(records)
    for name,group in cov.items():
        if not group['probes']:continue
        # No perfect empirical cue among the explicitly tested simple strategies.
        bad=[probe for probe,v in group['probes'].items() if v['success_mass']==v['attempts']]
        assert not bad,(stage,name,bad)
        assert len(group['correct_numeric_ranks'])>1,(stage,name,'fixed rank')
        assert len(group['correct_positions'])>1,(stage,name,'fixed position')
    probes.append({'stage':stage,'n':len(records),'groups':len(cov),'tested_cues':'position, numeric rank, leading sign, shortest/longest TeX, cube notation','perfect_cues':0})
roles={}
for r in accepted:
    group=r['generation']['template'];d=roles.setdefault(group,{'a_signs':set(),'answer_signs':set(),'points':set(),'roots':set(),'bank_roles':set()})
    p=r['generation']['parameters'];spec=__import__('generator').TEMPLATES[group]
    d['a_signs'].add((p['a']>0)-(p['a']<0));d['bank_roles'].add(r['generation']['bank_assignment'])
    if 't' in p:
        d['points'].add(p['t']); val=p['a']*p['t']**spec['degree']+p['b']*(p['t'] if spec['degree']==2 else 1)+p.get('c',0)
        d['roots'].add(int(math.isqrt(val)));value=__import__('validation_math').displayed(key(r)[':answer/value']);d['answer_signs'].add(int(__import__('sympy').sign(value)))
roles={k:{name:sorted(values,key=str) for name,values in d.items()} for k,d in roles.items()}
save('delivery-audit.json',{'stages':stages,'shortcut_probes':probes,'delivered_role_coverage':roles,'selection_limits':'Synthetic entity ordering; database identities, policy weights, future inventory and live learner history unavailable. Configured positive band weights preserve uniform support within each eligible band. Unconfigured policy chooses first entity; no claim of varied delivery under that legacy policy.','generator_rejection':'Normal probe records: maximum attempts 1. Whole bank invalidity resamples all values with chosen role preserved; exact source banks replay separately.'})
print(json.dumps({'stages':stages,'shortcut_probes':probes}))
