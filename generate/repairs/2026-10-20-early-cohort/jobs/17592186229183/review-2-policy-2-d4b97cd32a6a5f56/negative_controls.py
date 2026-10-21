import sys,json,subprocess,shutil
from pathlib import Path
R=Path(__file__).resolve().parent
rows=[]
for script,fixture,result in [('regression_checks.py','old-source','regression-checks.json'),('shortcut_checks.py','old-bank','shortcut-results.json')]:
 cmd=[sys.executable,str(R/script),'--package',str(R/'author-check'/fixture/'workspace')]
 p=subprocess.run(cmd,capture_output=True,text=True,cwd=R);assert p.returncode==1,(cmd,p.stdout,p.stderr)
 shutil.copyfile(R/result,R/('negative-'+result));rows.append({'command':cmd,'expected_exit':1,'actual_exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'result':'negative-'+result})
for script in ['regression_checks.py','shortcut_checks.py']:
 cmd=[sys.executable,str(R/script)];p=subprocess.run(cmd,capture_output=True,text=True,cwd=R);assert p.returncode==0,(cmd,p.stdout,p.stderr)
 rows.append({'command':cmd,'expected_exit':0,'actual_exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
(R/'independent-negative-controls.json').write_text(json.dumps({'checks':rows,'passed':True},indent=2)+'\n')
print(json.dumps({'passed':True,'negative_and_current_checks':len(rows)}))
