import sys,os,json,shutil,subprocess,hashlib
from pathlib import Path
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';R=Path('/home/jake/Developer/Course_Academy');P=str(R/'.venv/bin/python')
def save(n,d):(E/n).write_text(json.dumps(d,indent=2)+'\n')
# Reproduce retained historical repo-dependent lookup with the actual old entrypoint.
D=E/'legacy-relocated';D.mkdir(exist_ok=True)
shutil.copyfile(R/'generate/scratch/17592186115299.py',D/'17592186115299.py')
shutil.copyfile(W/'math_format.py',D/'math_format.py')
(D/'17592186115299').mkdir(exist_ok=True)
for n in ['templates.json','current-layouts.json']:shutil.copyfile(W/'17592186115299'/n,D/'17592186115299'/n)
env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1'
cmd=[P,str(D/'17592186115299.py'),'--format','json'];r=subprocess.run(cmd,cwd=D,env=env,capture_output=True,text=True)
save('legacy-negative.json',{'command':cmd,'exit':r.returncode,'stderr':r.stderr,'reproduced_historical_closure_failure':r.returncode!=0 and ('StopIteration' in r.stderr or 'scripts' in r.stderr)})
# Run retained author regression ONLY in evidence-owned full clone; it writes a report relative to its root.
C=E/'regression-copy';C.mkdir(exist_ok=True)
for f in json.load(open(W/'package.json'))['files']+['package.json','checks/package_relocation.py']:
 out=C/f;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,out)
(C/'evidence').mkdir(exist_ok=True)
cmd2=[P,str(C/'checks/package_relocation.py')];r2=subprocess.run(cmd2,cwd=C,env=env,capture_output=True,text=True)
save('retained-regression.json',{'command':cmd2,'exit':r2.returncode,'stdout':r2.stdout,'stderr':r2.stderr,'negative_control':'legacy-negative.json'})
print('historical negative',r.returncode,r.stderr.splitlines()[-1:],'current retained',r2.returncode)
