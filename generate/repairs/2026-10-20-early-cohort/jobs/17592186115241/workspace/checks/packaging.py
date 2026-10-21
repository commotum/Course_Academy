"""Relocate only declared runtime files and verify seeded CLI output."""
import hashlib,json,os,platform,shutil,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import sympy
manifest=json.load(open(ROOT/'package.json'));dest=ROOT/'evidence/relocated';dest.mkdir(exist_ok=True)
actual={'python':platform.python_version(),'packages':{'sympy':sympy.__version__}}
assert actual==manifest['dependencies']
assert 'package.json' not in manifest['files']
for name in manifest['files']:
 path=Path(name);assert not path.is_absolute() and '..' not in path.parts
 target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,target)
cmd=['--difficulty','easy','--count','5','--seed','90217','--format','json']
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(ROOT/'evidence/runtime-assets')}
def run(entry):
 cp=subprocess.run([sys.executable,'-B',str(entry)]+cmd,cwd=dest,env=env,capture_output=True,text=True);assert cp.returncode==0,cp.stderr
 return json.loads(cp.stdout)
one=run(ROOT/manifest['entrypoint']);two=run(dest/manifest['entrypoint']);three=run(dest/manifest['entrypoint']);assert one==two==three
assert one==json.load(open(ROOT/'evidence/samples.json'))
report={'dependencies':actual,'declared_files':manifest['files'],'deterministic':True,'relocatable':True,'same_five_sample_records':True,'command':[sys.executable,'-B','<relocated>/'+manifest['entrypoint']]+cmd,'runtime_hashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in manifest['files']},'assets':'none emitted; the package has no image generation or publication code'}
(ROOT/'evidence/packaging.json').write_text(json.dumps(report,indent=2));print(json.dumps({'deterministic':True,'relocatable':True,'runtime_files':len(manifest['files'])}))
