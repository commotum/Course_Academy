#!/usr/bin/env python3
"""Enumerate the actual finite default mathematical families, excluding evidence
translation profiles, independent-letter aliases and incidental output scaling."""
import importlib.util,itertools,json
from pathlib import Path
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('g',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
result={}
for level in g.LEVELS:
    fingerprints=set();full=set();counts={};nominal=0
    families=g.NAMES if level=='easy' else ['authored_'+level]
    for name in families:
        own=set()
        if level=='moderate':values=[dict(n=n,a=a,b=b,h=0,k=0) for n,a,b in itertools.product(range(2,6),range(1,5),range(2,6)) if n!=b]
        elif level=='hard':values=[dict(n=n,a=a,b=b,h=h,k=k) for n,a,b,h,k in itertools.product(range(2,4),range(1,4),range(1,4),[-3,-2,-1,1,2,3],[-3,-2,-1,1,2,3])]
        else:
            values=[]
            ns=range(2,5) if name in ('exp_product','trig_product','power_exp','exp_power','rational_power','root_log','root_exp','log_trig') else [g.ORIGINAL[name]['n']]
            for n,a,b in itertools.product(ns,range(1,7),range(1,6)):
                if name=='log_trig' and a!=b:continue
                values.append(dict(n=n,a=a,b=b,h=0,k=0))
        for p in values:
            r=g.generate(level,template=name,parameters=p);own.add(r['generation']['mathematical_fingerprint']);full.add(r['question'][':question/id']);nominal+=1
        counts[name]=len(own);fingerprints|=own
    result[level]={'nominal_parameter_combinations':nominal,'canonical_mathematical_tasks':len(fingerprints),'full_content_identities':len(full),'by_family':counts}
    print(level,result[level],flush=True)
(P/'variety.json').write_text(json.dumps(result,indent=2))
