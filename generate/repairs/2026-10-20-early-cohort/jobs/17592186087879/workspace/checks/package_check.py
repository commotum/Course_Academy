"""Check the declared runtime alone, after relocation, without service calls."""
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];E=ROOT/'evidence'
manifest=json.loads((ROOT/'package.json').read_text())
import sympy
assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sympy.__version__}}
assert (ROOT/'requirements.txt').read_text().strip()=='sympy=='+sympy.__version__
before={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in manifest['files']}
args=['--difficulty','easy','--count','5','--seed','811','--format','json']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(E/'assets'))
command=[sys.executable,str(ROOT/manifest['entrypoint']),*args]
a=subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True,check=True)
b=subprocess.run(command,cwd=ROOT,env=env,text=True,capture_output=True,check=True)
assert a.stdout==b.stdout
with tempfile.TemporaryDirectory(prefix='ivp-package-',dir=E) as tmp:
 rel=Path(tmp)
 for f in manifest['files']:
  target=rel/f;target.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(ROOT/f,target)
 relocated=subprocess.run([sys.executable,str(rel/manifest['entrypoint']),*args],cwd='/tmp',env=env,text=True,capture_output=True,check=True)
 assert a.stdout==relocated.stdout
 assert sorted(str(p.relative_to(rel)) for p in rel.rglob('*') if p.is_file())==sorted(manifest['files'])
assert before=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in manifest['files']}
(E/'cli-records.json').write_text(a.stdout)
(E/'package-results.json').write_text(json.dumps({'command':command,'deterministic':True,'relocated_records_identical':True,'relocation_cwd':'/tmp','undeclared_runtime_files':0,'generated_assets':0,'runtime_hashes':before,'dependencies':manifest['dependencies']},indent=2))
print(json.dumps({'records':len(json.loads(a.stdout)),'relocation':True,'deterministic':True,'runtime_files':len(manifest['files'])}))
