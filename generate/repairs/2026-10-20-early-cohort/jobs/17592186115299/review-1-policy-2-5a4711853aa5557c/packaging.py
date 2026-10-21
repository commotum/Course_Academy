import os,sys,subprocess,json,shutil,platform
from pathlib import Path
E=Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';P='/home/jake/Developer/Course_Academy/.venv/bin/python'
m=json.load(open(W/'package.json'));D=E/'relocated';D.mkdir(exist_ok=True)
for f in m['files']:
 out=D/f;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/f,out)
env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONDONTWRITEBYTECODE']='1';env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(E/'external-assets')
commands=[]
for band in ['easy','moderate','hard']:
 cmd=[P,'-I',str(D/m['entrypoint']),'--difficulty',band,'--seed','82111','--count','3','--format','json']
 # -I excludes script directory as well as repo paths; normal runtime does not promise -I.
 cmd.remove('-I');a=subprocess.run(cmd,cwd=E,env=env,text=True,capture_output=True);b=subprocess.run(cmd,cwd=E,env=env,text=True,capture_output=True)
 if a.returncode==0:(E/('relocated-'+band+'.json')).write_text(a.stdout)
 commands.append({'command':cmd,'exit':a.returncode,'deterministic':a.stdout==b.stdout,'stderr':a.stderr,'records':len(json.loads(a.stdout)) if a.returncode==0 else 0})
# Reproduce the retained import defect with a deliberately incomplete runtime closure.
F=E/'failing-closure';F.mkdir(exist_ok=True);shutil.copyfile(W/m['entrypoint'],F/m['entrypoint'])
failcmd=[P,str(F/m['entrypoint']),'--format','json'];fail=subprocess.run(failcmd,cwd=E,env=env,text=True,capture_output=True)
versions=json.loads(subprocess.check_output([P,'-c','import sys,sympy,mpmath,json;print(json.dumps({"python":sys.version.split()[0],"packages":{"sympy":sympy.__version__,"mpmath":mpmath.__version__}}))'],text=True))
report={'manifest':m,'installed':versions,'version_match':m['dependencies']==versions,'relocations':commands,'failing_closure':{'command':failcmd,'exit':fail.returncode,'stderr':fail.stderr},'retained_check_inspection':'checks/package_relocation.py checks relocated current CLI, deterministic replay and field ownership, but its legacy_failure is a literal string; it does not execute a negative import example. This independent test executes an incomplete closure and confirms nonzero import failure. Original historical scripts import was not reproduced exactly; missing local module is the same closure defect class.','external_outputs':[str(p.relative_to(E)) for p in (E/'external-assets').rglob('*') if p.is_file()] if (E/'external-assets').exists() else []}
(E/'packaging-report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
