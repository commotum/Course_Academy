"""Verify the declared runtime files alone suffice after relocation."""
import hashlib,json,os,platform,shutil,subprocess,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parents[1];E=W/'evidence/repair2';manifest=json.loads((W/'package.json').read_text())
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{}}
assert 'package.json' not in manifest['files']
args=['--difficulty','moderate','--seed','431440324','--count','5','--format','json']
with tempfile.TemporaryDirectory(dir=E,prefix='relocation-') as d:
 d=Path(d)
 for name in manifest['files']:
  p=Path(name);assert not p.is_absolute() and '..' not in p.parts
  (d/p).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/p,d/p)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(d/'assets'))
 native=subprocess.check_output([sys.executable,str(W/manifest['entrypoint'])]+args,text=True,env=env)
 relocated=subprocess.check_output([sys.executable,str(d/manifest['entrypoint'])]+args,text=True,env=env,cwd='/tmp')
 assert native==relocated
 records=json.loads(native);(E/'requested-batch.json').write_text(json.dumps(records,indent=2)+'\n')
(E/'package-results.json').write_text(json.dumps({'isolated_declared_files_only':True,'relocation_deterministic':True,'requested_count':len(records),'dependencies':manifest['dependencies'],'runtime_files':manifest['files'],'sha256':{p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in manifest['files']+['package.json']}},indent=2)+'\n')
print('Isolated relocation, deterministic replay and five-record requested batch passed.')
