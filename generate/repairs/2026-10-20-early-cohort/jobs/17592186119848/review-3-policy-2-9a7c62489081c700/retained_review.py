import json,subprocess,os
from pathlib import Path
E=Path(__file__).resolve().parent;PY='/home/jake/Developer/Course_Academy/.venv/bin/python';runs=[]
cases=[('original-first-negative','check_batch_decisions.py','first-failing-batch.json',1),('original-second-negative','check_exclusive_subset.py','previous-batch.json',1),('original-first-current','check_batch_decisions.py','batch.json',0),('original-second-current','check_exclusive_subset.py','batch.json',0),('retained-first-negative','relocated/checks/check_batch_decisions.py','first-failing-batch.json',1),('retained-second-negative','relocated/checks/check_exclusive_subset.py','previous-batch.json',1),('retained-first-current','relocated/checks/check_batch_decisions.py','batch.json',0),('retained-second-current','relocated/checks/check_exclusive_subset.py','batch.json',0)]
for label,script,input,expected in cases:
 cmd=[PY,'-B',str(E/script),'--input',str(E/input),'--report',str(E/(label+'.json'))];c=subprocess.run(cmd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));runs.append({'label':label,'command':cmd,'returncode':c.returncode,'expected':expected,'stdout':c.stdout,'stderr':c.stderr});assert c.returncode==expected,(label,c.stdout,c.stderr)
(E/'retained-checks.json').write_text(json.dumps(runs,indent=2)+'\n');print('Retained checks passed',len(runs))
