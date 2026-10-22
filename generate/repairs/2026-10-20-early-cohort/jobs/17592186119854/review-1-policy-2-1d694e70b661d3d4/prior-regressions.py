"""Strict independent acceptance regressions. Expected to fail this package."""
import os,sys,json,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;W=E.parent/'workspace';sys.path.insert(0,str(W))
spec=importlib.util.spec_from_file_location('g',W/'17592186119854.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
failures=[];cases=[]
for b in [[5,15,4],[7,20,5]]:
 r=g.generate('moderate',613,template='q-73992',parameters={'b':b});q=r['question'];f=q[':question/answer-fields'][0];correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);numeric=sorted(int(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/value']!='No solution');cases.append({'record':r,'correct_numeric_rank':numeric.index(int(correct[':answer/value']))+1})
if len(set(c['correct_numeric_rank'] for c in cases))==1:failures.append('Same displayed A, changed b and correct answer 6 -> 7, but choose-smallest-number bypass remains correct. Family-wide bank offsets fix the answer-producing action.')
s=json.load(open(E.parent/'source/source.json'));missing=[]
for q in [s['material']['kp'][':knowledge-point/canonical-example']]+s['material']['kp'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id']
 if sid not in ['q-34243','q-74011','q-74043','e-6191']:continue
 try:g.generate('hard' if sid=='q-74011' else 'moderate',901,template=sid)
 except Exception as ex:missing.append({'source_id':q[':question/id'],'template':sid,'error':type(ex).__name__+': '+str(ex)})
if missing:failures.append('Current source families cannot replay: '+', '.join(x['template'] for x in missing))
(E/'retained-counterexample-results.json').write_text(json.dumps({'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python regressions.py','failures':failures,'shortcut_pair':cases,'missing_source_cases':missing},indent=2)+'\n')
print(json.dumps({'failures':failures,'status':'failed' if failures else 'passed'}));sys.exit(bool(failures))
