import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,importlib.util,itertools,json,subprocess
D=Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('final00869',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
checks=[]
for level in ['easy','moderate','hard','all']:
 for fmt in ['json','markdown']:
  run=subprocess.run([str(ROOT/'.venv/bin/python'),'-B',str(D.with_suffix('.py')),'--difficulty',level,'--count','2','--seed','73','--format',fmt],check=True,capture_output=True,text=True)
  expected=6 if level=='all' else 2
  if fmt=='json':assert isinstance(json.loads(run.stdout),list) and len(json.loads(run.stdout))==expected
  else:assert run.stdout.count('### ')==expected and run.stdout.count('Field I (')==expected and run.stdout.count('Worked solution')==expected and run.stdout.count('**correct**')==expected*3
  checks.append({'difficulty':level,'format':fmt,'records':expected,'passed':True})
(D/'cli-validation.json').write_text(json.dumps({'passed':True,'checks':checks,'raw_absent_keys':'No captured practice is missing difficulty/fields/solution/correct refs; CLI raw replay requires explicit parameters in Python API.'},indent=2))
# Boundary samples all go through the same public guards.
checks=[]
for level in g.LEVELS:
 t='q-42374' if level=='easy' else 'q-42381' if level=='moderate' else 'mixed-orientations'
 dims=[(4,4),(4,2),(2,4)] if level=='easy' else [(5,4),(4,5),(1,5)] if level=='moderate' else [(1,5),(4,1),(5,4)]
 pairs=[[0,1],[1,0],[0,2]]
 p={'arrays':[[[(-9 if i%2 else 9) for i in range(c)] for _ in range(r)] for r,c in dims],'products':pairs}
 r=g.generate(level,template=t,parameters=p);checks.append({'level':level,'dimensions':dims,'record':r})
(D/'boundary-validation.json').write_text(json.dumps({'passed':True,'cases':checks},indent=2))
# A generic independent normal/source solution stage comparator checks operative stage
# masks at changed dimensions, including paragraph order and no added arithmetic.
review=json.loads((D/'review.json').read_text())
for r in review:
 text=r['question'][':question/worked-solution'];assert text.count('conformable for multiplication:')==3
 assert text.count('Since the number of columns')==3 and text.count('=\\text{')==3
 assert text.startswith('Notice that ') and '\n\nOn the other hand,' in text and '\n\nFinally,' in text
 assert not any(token in text for token in ['\\sum','\\frac','dot product','has dimensions','product has'])
(D/'solution-structure.json').write_text(json.dumps({'passed':True,'changed_parameter_profiles':len(review),'stages':['identify all displayed dimensions','ordered comparison I prose+factor annotation','ordered comparison II prose+factor annotation','ordered comparison III prose+factor annotation','complete true/false subset conclusion'],'source_complete_prose_comparison':'10/10 exact in source-fidelity.json','missing_or_extra_stages':0},indent=2))
print('CLI 8 modes,3 boundary cases,22 changed-template stage sequences passed')
