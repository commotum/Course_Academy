#!/usr/bin/env python3
"""Minimal retained failing acceptance tests; no package mutation or database access."""
import sys
sys.dont_write_bytecode=True
import argparse,json
import review_tests as t
p=argparse.ArgumentParser();p.add_argument('--case',choices=['shortcut','source-replay'],default='shortcut');a=p.parse_args()
g=t.load_generator(t.PKG/'17592186105745.py')
if a.case=='shortcut':
    records=[g.generate('easy',71923,'q-73743',{'rhs_scale':v}) for v in [1,-1]]
    t.save('minimal-shortcut-records.json',records)
    results=[{'parameters':r['generation']['parameters'],'selected':t.shortcut(r)[0],'correct':t.keypos(r),'success':t.shortcut(r)[0]==[t.keypos(r)]} for r in records]
    t.save('minimal-shortcut-results.json',{'acceptance_requirement':'The retained bank-only modal-row rule must not determine the answer for every member of this controlled pair. A repair should also test all bank profiles, not merely special-case these two records.','results':results})
    print(json.dumps(results));assert not all(z['success'] for z in results),'FAIL: bank-only top-row plurality plus zero-row cue answers both instances without using the given matrix'
else:
    failures=[]
    for sid,level in [('q-42156','easy'),('q-73524','easy'),('q-20959','easy'),('q-20962','moderate')]:
        try:g.generate(level,71923,sid,{'rhs_scale':1})
        except Exception as e:failures.append({'template':sid,'error':str(e)})
    t.save('minimal-source-results.json',{'unsupported_source_cases':failures})
    print(json.dumps(failures));assert not failures,'FAIL: supplied source cases excluded or absent'
