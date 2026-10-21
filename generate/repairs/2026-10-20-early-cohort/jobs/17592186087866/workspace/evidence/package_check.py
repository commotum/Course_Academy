"""Manifest-only relocation, deterministic CLI output, and exact metadata replay."""
import json,shutil,subprocess,os,sys,hashlib
from pathlib import Path
import validate_repair as a
W=a.W;E=a.E;manifest=json.loads((W/'package.json').read_text());target=E/'relocated';target.mkdir(exist_ok=True)
for relative in manifest['files']:
 p=Path(relative);assert not p.is_absolute() and '..' not in p.parts and relative!='package.json'
 dest=target/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/p,dest)
cmd=[sys.executable,str(target/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','2735275605','--format','json']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(E/'assets'))
out=subprocess.check_output(cmd,cwd=target,env=env);out2=subprocess.check_output(cmd,cwd=target,env=env);assert out==out2
records=json.loads(out);assert len(records)==5
for r in records:
 assert a.math.check(r)['passed']
 d=r['generation'];replay=a.g.generate('easy',d['seed'],d['template'],parameters=d['parameters'],decision=d['decision'])
 assert replay==r,'Metadata must reproduce a complete generated record'
a.save('runner-records.json',records)
a.save('relocation-results.json',{'command':cmd,'manifest_runtime_files':manifest['files'],'dependencies':manifest['dependencies'],'records':len(records),'byte_deterministic':out==out2,'exact_metadata_replay':True,'independent_math':True,'output_dir':env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'],'package_generated_assets':[],'hashes':{p:hashlib.sha256((W/p).read_bytes()).hexdigest() for p in manifest['files']}})
print('Relocation: 5 records, deterministic bytes, exact parameter+decision replay, independent math passed.')
