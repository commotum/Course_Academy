#!/usr/bin/env python3
"""Retain the feedback's exact relocated CLI failure and cold-asset checks."""
import hashlib, importlib.metadata, json, os, pathlib, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'package.json').read_text())
assert manifest['dependencies']['python']=='.'.join(map(str,sys.version_info[:3]))
for name,version in manifest['dependencies']['packages'].items():assert importlib.metadata.version(name)==version
assert manifest['entrypoint'] in manifest['files']
assert all(not pathlib.Path(x).is_absolute() and '..' not in pathlib.Path(x).parts for x in manifest['files'])
report=[]
with tempfile.TemporaryDirectory(prefix='sign-generator-relocation-') as temp:
 package=pathlib.Path(temp)/'package';package.mkdir();assets=pathlib.Path(temp)/'output'
 for name in manifest['files']:
  out=package/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,out)
 before={str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in package.rglob('*') if p.is_file()}
 env=dict(os.environ,PYTHONPATH='',PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(assets))
 for difficulty in ['moderate','easy','hard']:
  command=[sys.executable,str(package/manifest['entrypoint']),'--difficulty',difficulty,'--count','5','--seed','0','--format','json']
  proc=subprocess.run(command,capture_output=True,text=True,cwd=temp,env=env)
  assert proc.returncode==0,proc.stderr
  records=json.loads(proc.stdout);assert len(records)==5
  again=subprocess.run(command,capture_output=True,text=True,cwd=temp,env=env,check=True)
  assert proc.stdout==again.stdout
  report.append({'difficulty':difficulty,'command':['python','<relocated>/'+manifest['entrypoint']]+command[2:],'records':len(records),'deterministic':True,'exit_code':proc.returncode})
 # Cold renderer actually ran, without package writes or machine-specific imports.
 assert list(assets.rglob('*.png')) and list(assets.rglob('*.json'))
 after={str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in package.rglob('*') if p.is_file()}
 assert before==after,'Generator modified its runtime package'
 result={'passed':True,'tests':report,'runtime_files_unchanged':True,'cold_generated_plots':len(list(assets.rglob('*.png'))),'versions':manifest['dependencies']}
(ROOT/'evidence/runtime-closure.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
