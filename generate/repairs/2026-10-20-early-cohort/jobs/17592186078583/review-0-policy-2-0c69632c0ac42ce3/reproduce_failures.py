"""Strict acceptance tests: current package must fail; do not weaken these assertions."""
import sys,importlib.util,json
from pathlib import Path
sys.dont_write_bytecode=True
P=Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186078583/workspace/17592186078583.py')
spec=importlib.util.spec_from_file_location('subject',P);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
case=sys.argv[1] if len(sys.argv)>1 else 'cake'
if case=='cake':
 r=g.generate('easy',seed=90271,template='q-106877',profile='q-106877',parameters={'S':70})
 assert r['generation']['template']=='q-106877'
 assert 'Fahrenheit' in r['question'][':question/problem']
 print(json.dumps(r,indent=2))
elif case=='shortest':
 r=g.generate('moderate',seed=92601,template='q-106883')
 f=r['question'][':question/answer-fields'][0];n=min(len(a[':answer/value']) for a in f[':answer-field/choices']);short=[a for a in f[':answer-field/choices'] if len(a[':answer/value'])==n]
 print(json.dumps(r,indent=2))
 assert not(len(short)==1 and short[0][':answer/id']==f[':answer-field/correct'][1]), 'Incidental shortest-choice strategy answers the turkey case without reading ambient or applying Newton cooling'
else:raise ValueError(case)
