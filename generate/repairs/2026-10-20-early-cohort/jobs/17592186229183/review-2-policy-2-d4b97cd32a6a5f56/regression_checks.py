#!/usr/bin/env python3
"""Strict independent acceptance tests; currently fails on demonstrated defects.

Usage: <job-python> regression_checks.py [--package PATH] [--source PATH]
Writes only regression-checks.json beside this script. A repair can reuse it.
"""
import sys
sys.dont_write_bytecode=True
import argparse,importlib.util,json,re
from pathlib import Path
from decimal import Decimal
root=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,default=root.parent/'workspace')
ap.add_argument('--source',type=Path,default=root.parent/'source/source.json');args=ap.parse_args()
spec=importlib.util.spec_from_file_location('candidate',args.package/'17592186229183.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
rows=[];failures=[]
for t in g.MASKS:
    ranks=[]
    for seed in (7319,7320,7321,7322):
        r=g.generate('easy',seed=seed,template=t);f=r['question'][':question/answer-fields'][0]
        ordered=sorted(f[':answer-field/choices'],key=lambda a:Decimal(re.search(r'-?\d+(?:\.\d+)?',a[':answer/value'])[0]))
        ranks.append(next(i+1 for i,a in enumerate(ordered) if a[':answer/id']==f[':answer-field/correct'][1]))
    rows.append({'template':t,'seeds':[7319,7320,7321,7322],'correct_numeric_ranks':ranks})
# Necessary bounded regression condition, not a diversity quota or complete
# future acceptance proof. Current algebra proves a forced median family.
if all(rank==3 for row in rows for rank in row['correct_numeric_ranks']):
    failures.append('All normal templates/controlled seeds retain forced median answer; choose third-smallest bypasses overflow modeling.')
source=json.loads(args.source.read_text());replay=[]
for q in source['material']['kp'][':knowledge-point/questions']:
    sid=q[':question/math-academy-id'];case={'source_uuid':q[':question/id'],'source_id':sid}
    try:
        r=g.generate('easy',seed=9041,profile='observed:'+sid)
        af=r['question'][':question/answer-fields'];sf=q[':question/answer-fields']
        case['field_count_match']=len(af)==len(sf)
        case['complete_bank_match']=[sorted(a[':answer/value'] for a in f[':answer-field/choices']) for f in af]==[sorted(a[':answer/value'] for a in f[':answer-field/choices']) for f in sf]
        if not case['field_count_match'] or not case['complete_bank_match']:failures.append(sid+': captured response fields/banks not replayed')
    except Exception as e:case['error']=str(e);failures.append(sid+': '+str(e))
    replay.append(case)
result={'command':sys.argv,'rank_tests':rows,'source_tests':replay,'failures':failures,'passed':not failures,
        'limits':'Passing these necessary regression tests does not independently certify a future repaired generator.'}
(root/'regression-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':not failures,'failure_count':len(failures),'failures':failures}));sys.exit(bool(failures))
