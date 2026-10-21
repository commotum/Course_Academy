import sys,json,importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from witness import shortcut
spec=importlib.util.spec_from_file_location('generator',ROOT/'17592186115241.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
p={'free_coefficients':[2,-3],'constants':[1,4],'mix':[1,1]}
results=[]
for name,kw in [('shortcut',{'parameters':p}),('zero-slope',{'parameters':{**p,'free_coefficients':[0,-3]}}),('equal-coordinates',{'parameters':{**p,'free_coefficients':[2,2],'constants':[1,1]}}),('source',{'profile':'q-131714','parameters':{'scale':1,'offsets':[0,0,0]}})]:
 try:
  r=g.generate_easy(seed=90217,**kw)
  probe=shortcut(r)
  if name=='shortcut':assert not(probe.get('unique_modes') and probe.get('correct')),'component modes recover key'
  results.append({'case':name,'pass':True,'probe':probe})
 except Exception as e:results.append({'case':name,'pass':False,'error':str(e)})
print(json.dumps(results,indent=2))
if len(sys.argv)>1:(ROOT/sys.argv[1]).write_text(json.dumps(results,indent=2))
assert all(r['pass'] for r in results)
