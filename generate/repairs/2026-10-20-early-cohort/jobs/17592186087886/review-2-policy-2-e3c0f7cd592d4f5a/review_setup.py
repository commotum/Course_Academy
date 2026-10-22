from pathlib import Path
import json,hashlib,shutil,subprocess,os,sys
E=Path(__file__).resolve().parent
J=E.parent
P=J/'workspace'
def snapshot():return {str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()}
(E/'package-before.json').write_text(json.dumps(snapshot(),indent=2))
R=E/'author-replay'/'workspace'
shutil.copytree(P,R,dirs_exist_ok=True)
shutil.copytree(J/'source',R.parent/'source',dirs_exist_ok=True)
(E/'batch-records.json').write_bytes((J/'samples.json').read_bytes())
report={}
for name in ['check_package.py','check_repair.py']:
 cmd=[sys.executable,str(R/'checks'/name)]
 p=subprocess.run(cmd,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,cwd=E)
 report[name]={'command':cmd,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
 (E/'retained-checks.json').write_text(json.dumps(report,indent=2))
 print(name,p.returncode,p.stdout[-1500:],p.stderr[-600:],flush=True)
assert snapshot()==json.load(open(E/'package-before.json'))
