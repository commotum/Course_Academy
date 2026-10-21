"""Strict review regressions. Nonzero exit is expected on the reviewed package.
Run with the job Python: python -B regression_acceptance.py
A repair can override --entrypoint and --batch while retaining the assertions.
"""
import argparse,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--entrypoint',type=Path,default=E.parent/'workspace/17592186068840.py');ap.add_argument('--batch',type=Path,default=E/'batch-records.json');a=ap.parse_args()
spec=importlib.util.spec_from_file_location('current',a.entrypoint);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
checks=[]
def check(label,condition,detail): checks.append({'label':label,'passed':bool(condition),'detail':detail})
ma={t.get('source',{}).get(':question/math-academy-id') for t in g.TEMPLATES.values()}
for source in ['q-14251','q-168070','q-168084']:
 check('complete captured source coverage '+source,source in ma,'Template extraction must include this captured source family, bank and response contract.')
def cue(v):
 return '^{2}' in v and 'C +' in v and (v.startswith(r'y=\sqrt[3]{C +') or v.startswith(r'y=\ln{\left(C +') or (v.startswith(r'y=\left(C +') and v.endswith('^{3}')))
def shortcut(r):
 f=r['question'][':question/answer-fields'][0];selected=[c for c in f[':answer-field/choices'] if cue(c[':answer/value'])]
 return len(selected)==1 and selected[0][':answer/id']==f[':answer-field/correct'][1]
rows=[]
for old in json.load(open(E/'independent-easy.json')):
 m=old['generation'];rows.append(g.generate_easy(m['seed'],m['template'],parameters=m['parameters'],profile=m['bank_profile']))
for family in ['reciprocal_cube','negative_exp','cube_power']:
 part=[r for r in rows if r['generation']['template']==family]
 check('equation-independent shape must not predict all '+family,part and not all(map(shortcut,part)),{'success':sum(map(shortcut,part)),'total':len(part),'rule':'Choose C + square nested in inverse/cube, without inspecting ODE.'})
batch=json.load(open(a.batch));check('exact runner batch must not be completely answered by fixed shape',not all(map(shortcut,batch)),{'success':sum(map(shortcut,batch)),'total':len(batch)})
(E/'strict-regression-results.json').write_text(json.dumps({'entrypoint':str(a.entrypoint),'batch':str(a.batch),'checks':checks,'passed':all(c['passed'] for c in checks)},indent=2)+'\n')
print(json.dumps({'passed':all(c['passed'] for c in checks),'failed':[c['label'] for c in checks if not c['passed']]}))
sys.exit(0 if all(c['passed'] for c in checks) else 1)
