"""Enumerate substantive finite root/category/statement tasks; never seed/amplitude aliases."""
import importlib.util,itertools,json,pathlib
import sys
sys.dont_write_bytecode=True
import numpy as np
D=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
report={}
for name,t in list(g.RECIPES.items())+[('mixed_categories_four_roots',g.HARD)]:
 tuples=[]
 for roots in itertools.combinations(range(-6,7),len(t['roots'])):
  if not roots[0]<0<roots[-1]:continue
  if name=='q-38762' and roots[0]!=-roots[1]:continue
  if name in ['q-38768','q-112591','q-112585','q-112587'] and roots[1]!=0:continue
  if name=='q-38779' and not roots[1]>0:continue
  cs=np.array([1.])
  for root,m in zip(roots,t['multiplicities']):
   for _ in range(m):cs=np.polymul(cs,[1,-root])
  crit=np.roots(np.polyder(cs));hs=[abs(float(np.polyval(cs,r.real))) for r in crit if abs(r.imag)<1e-5 and abs(float(np.polyval(cs,r.real)))>1e-5]
  if not hs or min(hs)/max(hs)<.04:continue
  tuples.append(roots)
 report[name]={'explicit_root_domain':[-6,6],'categories':[g.category(m) for m in t['multiplicities']],'eligible_root_tuples':tuples,'meaningful_tasks':len(tuples)*(4 if name=='q-38779' else 1),'marked_intercept_values':[1,2,3,4]if name=='q-38779'else None,'excluded_from_task_counts':['seed','choice order','profile aliases','positive amplitude except displayed assessed intercept','exact exponents within root category'],'bank_complete_before_parameters':True}
(D/'finite-domains.json').write_text(json.dumps(report,indent=2)+'\n')
print({name:r['meaningful_tasks']for name,r in report.items()})
