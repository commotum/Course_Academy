"""Strict independent acceptance regressions. Expected to fail current generator."""
import json,sys
import review as t
from probes import sign_strategy
sources=json.load(open(t.J/'source/source.json'))['material']['kp'][':knowledge-point/questions']
expected={q[':question/id'] for q in sources};actual={r['generation']['parameters']['source_id'] for r in t.g.replay()}
rs=t.g.generate('easy',1,913771)
checks=[{'name':'all supplied source cases replayed','passed':expected<=actual,'missing':sorted(expected-actual)},{'name':'easy bank requires more than sign comparison somewhere','passed':any(sign_strategy(r)!=r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in t.g.generate('easy',96,913771)),'counterexample_file':'fresh-easy.json','minimal_case':rs[0]['generation']}]
t.save('strict-acceptance-results.json',{'command':str(t.PY)+' '+str(t.E/'strict_acceptance.py'),'checks':checks,'passed':all(x['passed'] for x in checks)})
for x in checks:print(('PASS' if x['passed'] else 'FAIL')+': '+x['name'])
sys.exit(0 if all(x['passed'] for x in checks) else 1)
