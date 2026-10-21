"""Strict repair acceptance tests. Current package intentionally exits 1.
Usage: /home/jake/Developer/Course_Academy/.venv/bin/python -B acceptance-tests.py [--package PATH]
No package files, database, or external outputs are mutated.
"""
import sys,json,pathlib,argparse,importlib.util
sys.dont_write_bytecode=True
ap=argparse.ArgumentParser();ap.add_argument('--package',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent/'workspace');args=ap.parse_args();sys.path.insert(0,str(args.package))
spec=importlib.util.spec_from_file_location('review_target',args.package/'17592186115242.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
results=[]
def test(label,f):
 try:f();results.append({'test':label,'passed':True})
 except Exception as e:results.append({'test':label,'passed':False,'error':str(e)})
def zero():
 r=g.generate('moderate',seed=932455,template='inconsistent_shift',parameters=dict(a=1,b=2,c=1,d=2,u=1,v=4,e=3));f=r['question'][':question/answer-fields'][0];key=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert key[':answer/value']=='k=0'
def source():
 r=g.generate('hard',seed=932455,profile='q-74691',parameters=dict(a=2,b=-2,c=4,d=-3,u=1,v=0,e=-6));f=r['question'][':question/answer-fields'][0];assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'k=-3','k=3','k=4','k=-1','k=5'};key=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert key[':answer/value']=='k=3'
def shortcut():
 import sympy as s
 success=0
 for seed in range(932401,932449):
  r=g.generate('easy',seed=seed);p=r['generation']['parameters'];f=r['question'][':question/answer-fields'][0];sign=p['b']*p['d'];choice=(max if sign>0 else min)(f[':answer-field/choices'],key=lambda a:s.sympify(a[':answer/value'].split('=')[1]));success+=choice[':answer/id']==f[':answer-field/correct'][1]
 assert success<48, f'sign-only extremal-choice action solved {success}/48; eligible correct relative-magnitude roles never changed'
test('valid moderate zero-root accepted',zero);test('complete q-74691 replay',source);test('easy family defeats sign-only extremum action',shortcut)
print(json.dumps({'tests':results,'passed':all(r['passed'] for r in results)},indent=2));sys.exit(0 if all(r['passed'] for r in results) else 1)
