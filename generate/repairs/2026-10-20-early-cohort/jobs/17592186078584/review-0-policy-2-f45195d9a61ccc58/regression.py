"""Strict independent regression checks. Expected to fail on reviewed package.
Run with context Python; use --report to save the failure report without assertion.
"""
import pathlib,sys,importlib.util,json,math
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'workspace'
s=importlib.util.spec_from_file_location('generator',P/'17592186078584.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
checks=[]
for source,params,answer in [('e3e001a8-9294-59a4-82e6-b1122afdc72f',dict(ambient=23,initial=80,rate='0.25',time=4),44),('44b64320-501f-5d6a-b8c7-b8cf6a960fc2',dict(ambient=21,initial=40,rate='0.06',time=4),36)]:
 try:
  r=g.generate('easy',84199,'coffee',parameters=params);checks.append({'case':'legitimate source parameters','source_id':source,'parameters':params,'expected':f'Accept mathematically valid IVP with rounded answer {answer}','passed':True,'record':r})
 except ValueError as e:checks.append({'case':'legitimate source parameters','source_id':source,'parameters':params,'expected':f'Accept mathematically valid IVP with rounded answer {answer}','passed':False,'actual':str(e)})
for profile in ['q-107121','q-107123']:
 try:r=g.generate('easy' if profile=='q-107121' else 'moderate',84199,profile=profile);checks.append({'case':'source profile replay','profile':profile,'passed':True,'record':r})
 except ValueError as e:checks.append({'case':'source profile replay','profile':profile,'passed':False,'actual':str(e)})
# Deliberately demand a counterexample to the structural rank predictor within each easy template.
# This is not a universal diversity quota: the correct rank has no instructional role here.
for template in ['coffee','iron','exhaust','cake','compressor']:
 rs=[r for r in json.loads((E/'fresh-samples.json').read_text()) if r['generation']['template']==template]
 def rank(r):
  f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1];nums=[int(a[':answer/value'].split('}')[0][1:]) for a in f[':answer-field/choices']];v=next(int(a[':answer/value'].split('}')[0][1:]) for a in f[':answer-field/choices'] if a[':answer/id']==cid);return sorted(nums).index(v)+1
 checks.append({'case':'reject rank shortcut','template':template,'seeds':[r['generation']['seed'] for r in rs],'strategy':'select median without using prompt','correct':sum(rank(r)==3 for r in rs),'total':len(rs),'passed':any(rank(r)!=3 for r in rs)})
(E/'regression-results.json').write_text(json.dumps({'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python regression.py','checks':checks},indent=2))
print(json.dumps(checks,indent=2))
assert all(c['passed'] for c in checks),'Demonstrated source restrictions and deterministic numeric-rank shortcut remain'
