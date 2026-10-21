import json,os,shutil,subprocess,sys
from pathlib import Path
import sympy
W=Path(__file__).resolve().parent.parent;E=W/'evidence';dest=E/'relocated'
m=json.loads((W/'package.json').read_text())
for name in m['files']:
 p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/name,p)
cmd=[sys.executable,str(dest/m['entrypoint']),'--difficulty','easy','--count','5','--seed','829331','--format','json']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(E/'assets'))
p=subprocess.run(cmd,cwd='/tmp',env=env,capture_output=True,text=True,check=True)
records=json.loads(p.stdout);expected=json.loads((E/'samples.json').read_text());assert records==expected
assert m['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sympy.__version__}}
(E/'packaging-results.json').write_text(json.dumps({'passed':True,'relocation_command':cmd,'cwd':'/tmp','records_identical':5,'dependencies_actual':m['dependencies'],'runtime_files':m['files'],'assets':'none'},indent=2)+'\n')
print(json.dumps({'passed':True,'relocated_records':5}))
