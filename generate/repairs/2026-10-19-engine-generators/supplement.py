"""Current-session canonical, counterfactual and original engine regressions.

Run from a knowledge point's independent-review directory with the repository Python.
The imported audit is the previous independent reviewer's parser/checker, rerun here.
"""
import importlib
import json
from pathlib import Path
import subprocess
import sys

E = Path.cwd()
KP = int(E.parent.name)
REPO = next(p for p in E.parents if (p/'Cargo.toml').exists())
sys.path.insert(0, str(E))
a = importlib.import_module('review' if KP == 17592186092261 else 'audit')
g = a.g

def save(name, value):
    (E/name).write_text(json.dumps(value, indent=2, default=str)+'\n')

def field(r):
    return r['question'][':question/answer-fields'][0]

def key(r):
    f = field(r)
    return next(v[':answer/value'] for v in f[':answer-field/choices'] if v[':answer/id'] == f[':answer-field/correct'][1])

if KP == 17592186096617:
    records = [g.generate(seed=88001+i, template=t, parameters={'c':1, 'n':1, **({'trig':'cos'} if t in ['q-1907','q-104300'] else {})})
        for i,t in enumerate(['q-1907','q-104300','q-47965','q-319357'])]
    checks = [a.inspect(r) for r in records]
elif KP == 17592186096618:
    records = [g.generate(seed=88001, template='polynomial_log_blank', parameters={'n':2,'h':0}, target=target) for target in ['left','right']]
    checks = [a.inspect(r) for r in records]
    assert not any(c['failures'] for c in checks)
elif KP == 17592186092261:
    records = [g.generate_easy(88001, template='e-728', parameters={'b':2,'c':3,'a':-1,'n':1,'k':0,'l':0,'d':1})]
    checks = [{'passed':a.eq(a.parse(key(r)),a.expected(r)[1]),'expected':str(a.expected(r)[1])} for r in records]
    assert all(c['passed'] for c in checks)
else:
    records = [g.generate('hard',seed=88001,template='sqrt_quadratic_blank',parameters={'a':-1,'b':0,'c':1})]
    checks = [a.math_record(r) for r in records]
    assert all(c['correct'] for c in checks)
save('canonical-current-records.json', records)
save('canonical-current-checks.json', checks)

native = []
for r in records:
    f = field(r)
    if f[':answer-field/type'].endswith('/radio'):
        cc = [{'submitted_answer_id':v[':answer/id'], 'expected':'accepted' if v[':answer/id']==f[':answer-field/correct'][1] else 'rejected', 'purpose':'canonical independently differentiated bank'} for v in f[':answer-field/choices']]
    else:
        cc = [{'submitted':key(r),'expected':'accepted','purpose':'canonical derivative'},
              {'submitted':'0','expected':'rejected','purpose':'canonical nonzero derivative rejects zero'}]
    native.append({'label':'restored canonical '+str(len(native)), 'record':r,'checks':cc})

# Original regression inputs now require actual accepted/rejected outcomes.
audit = REPO/'generate/repairs/2026-10-19-engine-blocker-audit'
for path in sorted(audit.glob(f'{KP}-*-input.json')):
    native.extend(json.loads(path.read_text()))

# Bind controlled evidence changes to actual grade outcomes, including the
# radical's positive/zero/negative slope controls and irrelevant choice reversal.
if KP == 17592186096842:
    cf = json.loads((E/'counterfactual-records.json').read_text())
    for i,j in [(0,1),(1,0),(4,5),(5,4),(5,6),(6,5)]:
        native.append({'label':f'changed evidence {i} rejects stale response {j}', 'record':cf[i],
            'checks':[{'submitted':key(cf[j]),'expected':'rejected','purpose':'changed inner constant or tangent target'}]})
    f=field(cf[-1]);matching=next(v for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1])
    native.append({'label':'irrelevant choice reversal preserves answer','record':cf[-1],
        'checks':[{'submitted_answer_id':matching[':answer/id'],'expected':'accepted','purpose':'same mathematical answer after option reversal'}]})
    probe=json.loads((E/'sum-shortcut-results.json').read_text())
    probe['why_reliable']='The previous scaling-bank proof no longer applies: every option now shares the same cubic derivative and varies the radical contribution. The observed nearest-cubic strategy is correct in 4/20 cases.'
    save('sum-shortcut-results.json',probe)
    chosen=json.loads((E/'sum-shortcut-grader-input.json').read_text())
    for c,p in zip(chosen,probe['cases'],strict=True):
        c['checks'][0]['expected']='accepted' if p['correct'] else 'rejected'
    native.extend(chosen)

save('current-regression-input.json',native)
cmd=[str(REPO/'generate/runs/current/check-engine'),'current-regression-input.json','current-regression-grading.json']
run=subprocess.run(cmd,capture_output=True,text=True,timeout=90)
save('current-regression-command.json',{'command':cmd,'exit_code':run.returncode,'stdout':run.stdout,'stderr':run.stderr})
assert run.returncode == 0,run.stderr
print(run.stdout.strip())
