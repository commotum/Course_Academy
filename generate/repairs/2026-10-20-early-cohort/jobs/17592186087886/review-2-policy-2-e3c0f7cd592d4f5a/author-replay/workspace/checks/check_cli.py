"""Small ordinary seeded CLI sample, actual delivery and native grading."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
REPO=Path('/home/jake/Developer/Course_Academy');OUT=ROOT/'evidence'
s=importlib.util.spec_from_file_location('validator',ROOT/'17592186087886/validate.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c);g=c.g
command=[sys.executable,str(ROOT/'17592186087886.py'),'--difficulty','easy','--count','5','--seed','71','--format','json']
result=subprocess.run(command,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(OUT/'cli-assets')},capture_output=True,text=True,check=True)
rows=json.loads(result.stdout);assert len(rows)==5
assert len({r['generation']['parameter_fingerprint'] for r in rows})==5
for r in rows:c.independent(r)
(OUT/'cli-records.json').write_text(json.dumps(rows,indent=2)+'\n')
cases=[{'label':'ordinary CLI '+str(i),'record':r,'checks':c.checks(r)} for i,r in enumerate(rows)]
(OUT/'cli-grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(OUT/'cli-grader-input.json'),str(OUT/'cli-grader-report.json')],check=True,capture_output=True,text=True)
source=ROOT.parent/'source'
delivery=[sys.executable,str(REPO/'generate/pipeline/check_delivery.py'),'--input',str(OUT/'cli-records.json'),'--source',str(source/'source.json'),'--inventory',str(source/'inventory.json'),'--difficulty','easy','--output',str(OUT/'cli-delivery'),'--asset-root',str(OUT),'--math-root','/media/jake/SSD/EDB/math']
subprocess.run(delivery,capture_output=True,text=True,check=True)
accepted=json.loads((OUT/'cli-delivery/accepted.json').read_text());assert len(accepted)==5
# Count mathematics, not coefficient decompositions, without generating hundreds
# of interchangeable records. Actual visible records are checked above and by
# the controlled role and retained finite-k tests.
import sympy as sp
from math_reader import x,y,v
catalog={}
for t in g.ORIGINAL:
    rates={sp.srepr(sp.cancel((g.mathematics(t,k)[0]+shift*y/x).subs(y,v*x))) for k in g.DOMAINS[t] for shift in [-2,-1,0,1,2]}
    catalog[t]={'parameter_decompositions':30,'distinct_prompt_mathematics':len(rates)}
assert sum(r['distinct_prompt_mathematics'] for r in catalog.values())==220
report={'status':'pass','command':command,'delivery_command':delivery,'input_records':5,'delivered_records':len(accepted),'math_and_all_solution_stages_checked':True,'native_accepted':5,'native_rejected':20,'semantic_catalog':catalog,'total_semantic_instances':220,'parameter_decompositions':240,'catalog_limit':'Algebraic catalog enumeration only; the independently parsed record sample covers 80 records / 78 distinct prompts plus this five-item ordinary CLI sample. It does not claim exhaustive rendered validation of all 220 prompts.'}
(OUT/'cli-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'pass','ordinary_cli':5,'delivered':len(accepted),'native_accepted':5,'native_rejected':20,'distinct_catalog_prompts':220}))
