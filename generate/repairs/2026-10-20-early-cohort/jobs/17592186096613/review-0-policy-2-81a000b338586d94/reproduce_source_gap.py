"""Strict source-coverage regression. Exits 1 on the currently demonstrated gaps."""
import argparse,importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
p=argparse.ArgumentParser();p.add_argument('--package',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent.parent/'workspace');p.add_argument('--output',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent/'source-gap.json');a=p.parse_args()
spec=importlib.util.spec_from_file_location('candidate',a.package/'17592186096613.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
results=[]
for name,kwargs in [('source q-70887',dict(profile='raw-q-70887',parameters=dict(n=1,d=4,k=0))),('unit-fraction normal practice',dict(parameters=dict(n=1,d=4,k=0))),('source q-70889',dict(profile='raw-q-70889',parameters=dict(n=6,d=1,k=1)))]:
 try:
  r=g.generate_easy(seed=917,**kwargs);results.append({'case':name,'kwargs':kwargs,'record':r,'passed':True})
 except Exception as e:results.append({'case':name,'kwargs':kwargs,'passed':False,'error':str(e)})
a.output.write_text(json.dumps({'command':sys.argv,'tests':results},indent=2));print(json.dumps({'passed':all(r['passed'] for r in results),'failures':[r['case'] for r in results if not r['passed']]}));sys.exit(0 if all(r['passed'] for r in results) else 1)
