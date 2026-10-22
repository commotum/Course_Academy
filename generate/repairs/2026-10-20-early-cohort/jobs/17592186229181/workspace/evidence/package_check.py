"""Relocation, deterministic CLI, runtime manifest and pinned dependency checks."""
from checks import *
import hashlib,os,shutil,subprocess
m=json.loads((ROOT/'package.json').read_text());g=load()
assert m['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sp.__version__}}
relocated=EVIDENCE/'relocated';relocated.mkdir(exist_ok=True)
for name in m['files']:
 path=pathlib.Path(name);assert not path.is_absolute() and '..' not in path.parts and name!='package.json'
 dest=relocated/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
assets=EVIDENCE/'generated-assets';assets.mkdir(exist_ok=True)
cmd=[sys.executable,str(relocated/m['entrypoint']),'--difficulty','easy','--count','5','--seed','81031','--format','json']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(assets))
first=subprocess.run(cmd,cwd=relocated,env=env,capture_output=True,text=True,check=True);second=subprocess.run(cmd,cwd=relocated,env=env,capture_output=True,text=True,check=True)
assert first.stdout==second.stdout
assert json.loads(first.stdout)==json.loads((EVIDENCE/'batch.json').read_text())
for flag,value in (('--count','0'),('--difficulty','unknown')):
 bad=subprocess.run([sys.executable,str(relocated/m['entrypoint']),flag,value,'--format','json'],cwd=relocated,env=env,capture_output=True,text=True);assert bad.returncode!=0
hashes={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['package.json']+m['files']}
save('packaging.json',{'runtime_files':m['files'],'runtime_hashes':hashes,'dependencies':m['dependencies'],'relocation':str(relocated.relative_to(ROOT)),'deterministic':True,'cli_matches_batch':True,'invalid_cli_rejected':True,'new_assets':len(list(assets.iterdir())),'passed':True,'command':cmd})
print(json.dumps({'relocated':True,'deterministic':True,'runtime_files':len(m['files']),'passed':True}))
