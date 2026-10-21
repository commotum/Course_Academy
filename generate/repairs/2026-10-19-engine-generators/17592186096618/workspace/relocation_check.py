"""Run declared runtime files from an isolated relocated package directory."""
import hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent;target=root/'evidence/relocated-package';target.mkdir(exist_ok=True)
manifest=json.loads((root/'package.json').read_text())
for name in manifest['files']:
 p=Path(name);assert not p.is_absolute() and '..' not in p.parts;shutil.copy2(root/name,target/name)
env=os.environ.copy();env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(root/'evidence/relocated-assets');env['PYTHONPATH']=''
cmd=[sys.executable,str(target/manifest['entrypoint']),'--difficulty',manifest['default_difficulty'],'--count','5','--seed','555','--format','json']
p=subprocess.run(cmd,cwd=target,env=env,text=True,capture_output=True,check=True);records=json.loads(p.stdout);assert len(records)==5
p2=subprocess.run(cmd,cwd=target,env=env,text=True,capture_output=True,check=True);assert p2.stdout==p.stdout
(root/'evidence/final-five.json').write_text(p.stdout)
report={'passed':True,'record_count':5,'deterministic_stdout':True,'runtime_files':manifest['files'],'dependencies':manifest['dependencies'],'package_hashes':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in manifest['files']},'undeclared_runtime_files':[str(p.relative_to(target)) for p in target.rglob('*') if p.is_file() and '__pycache__' not in p.parts and str(p.relative_to(target)) not in manifest['files']],'stderr':p.stderr}
assert not report['undeclared_runtime_files'];(root/'evidence/relocation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':True,'records':5,'deterministic':True}))
