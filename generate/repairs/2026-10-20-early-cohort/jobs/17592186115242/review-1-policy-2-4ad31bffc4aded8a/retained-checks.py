"""Run author's retained regression checks read-only, redirecting all writes here.
Usage: job-python -B retained-checks.py
"""
import sys,pathlib,importlib.util,runpy,json,traceback
sys.dont_write_bytecode=True
R=pathlib.Path(__file__).resolve().parent; W=R.parent/'workspace'
sys.path[:0]=[str(W/'checks'),str(W)]
import validate_repair as v
reports=[]
for label,package in [('current',W),('old',R.parent/'review-0-policy-2-7164cf0480f72dae/relocated')]:
 spec=importlib.util.spec_from_file_location('target_'+label,package/'17592186115242.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 v.g=g;v.E=R/('retained-'+label);v.E.mkdir(exist_ok=True)
 for finding in ['shortcut','source','zero']:
  sys.argv=['regressions.py','--finding',finding]
  try:
   runpy.run_path(str(W/'checks/regressions.py'),run_name='__main__'); reports.append(dict(target=label,finding=finding,passed=True))
  except Exception as e:reports.append(dict(target=label,finding=finding,passed=False,error=repr(e),traceback=traceback.format_exc()))
(R/'retained-check-results.json').write_text(json.dumps(reports,indent=2))
print(json.dumps([{k:v for k,v in r.items() if k!='traceback'} for r in reports]))
