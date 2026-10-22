import json,shutil,subprocess,os,sys
from pathlib import Path
E=Path(__file__).resolve().parent; C=E/'author-replay/workspace'; N=E/'author-negative/workspace';N.mkdir(parents=True,exist_ok=True)
for name in ['math_reader.py','requirements.txt','package.json','17592186087886/source.json','checks/check_shortcuts.py','checks/check_package.py','evidence/shortcut-before-records.json']:
 p=N/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(C/name,p)
shutil.copytree(E.parent/'source',N.parent/'source',dirs_exist_ok=True)
shutil.copyfile(C/'evidence/entrypoint-before-decision-repair.py',N/'17592186087886.py')
cmd=[sys.executable,str(N/'checks/check_shortcuts.py')]
p=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
report={'historical_shortcut':{'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'historical_version':'retained entrypoint-before-decision-repair.py v1.1.0'}}
# Controlled recreation of unresolved runtime closure: remove required local module from manifest only in evidence.
shutil.copyfile(C/'17592186087886.py',N/'17592186087886.py')
m=json.load(open(N/'package.json'));m['files'].remove('math_reader.py');(N/'package.json').write_text(json.dumps(m))
cmd=[sys.executable,str(N/'checks/check_package.py')];p=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
report['missing_runtime_module']={'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'input_change':'manifest omits math_reader.py; all changes confined to evidence copy'}
report['current']={'check_package':'retained-checks.json','check_repair_log':'author-regression.log','shortcut_report':'author-replay/workspace/evidence/shortcut-regression.json','role_report':'author-replay/workspace/evidence/role-regression.json'}
(E/'regression-controls.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:{'exit':v.get('exit'),'stdout':v.get('stdout','')[-500:]} for k,v in report.items()}))
assert report['historical_shortcut']['exit']!=0 and '"status": "fail"' in report['historical_shortcut']['stdout']
assert report['missing_runtime_module']['exit']!=0 and 'math_reader' in report['missing_runtime_module']['stderr']
