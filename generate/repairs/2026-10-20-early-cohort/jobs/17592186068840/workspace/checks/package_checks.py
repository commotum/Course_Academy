"""Check actual runtime closure and CLI after relocation; writes evidence only."""
from pathlib import Path
import importlib.metadata,json,os,shutil,subprocess,sys,tempfile,hashlib
W=Path(__file__).resolve().parents[1];E=W/'evidence';manifest=json.loads((W/'package.json').read_text())
assert manifest['dependencies']['python']==sys.version.split()[0]
for name,version in manifest['dependencies']['packages'].items():assert importlib.metadata.version(name)==version
assert 'package.json' not in manifest['files']
commands=[];results=[]
with tempfile.TemporaryDirectory(prefix='relocated-',dir=E) as tmp:
 root=Path(tmp)
 for name in manifest['files']:
  p=Path(name);assert not p.is_absolute() and '..' not in p.parts
  target=root/p;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/p,target)
 env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(E/'assets'),'PYTHONDONTWRITEBYTECODE':'1'}
 for level in ['easy','moderate','hard']:
  args=['--difficulty',level,'--count','5' if level=='easy' else '2','--seed','71101','--format','json']
  a=[sys.executable,'-B',str(W/manifest['entrypoint'])]+args;b=[sys.executable,'-B',str(root/manifest['entrypoint'])]+args
  commands.extend([a,b]);p=subprocess.run(a,cwd='/tmp',env=env,capture_output=True,text=True,check=True);q=subprocess.run(b,cwd='/tmp',env=env,capture_output=True,text=True,check=True)
  assert p.stdout==q.stdout
  again=subprocess.run(b,cwd='/tmp',env=env,capture_output=True,text=True,check=True);assert q.stdout==again.stdout
  records=json.loads(q.stdout);assert len(records)==(5 if level=='easy' else 2)
  assert all(r['question'][':question/difficulty'].endswith('/'+level) for r in records)
  results.append({'difficulty':level,'records':len(records),'relocation_exact':True,'seeded_repeat_exact':True})
 for args in [['--count','0'],['--count','-1'],['--difficulty','invalid']]:
  cmd=[sys.executable,'-B',str(root/manifest['entrypoint'])]+args;commands.append(cmd)
  p=subprocess.run(cmd,cwd='/tmp',env=env,capture_output=True,text=True);assert p.returncode!=0
report={'runtime_files':manifest['files'],'dependencies':manifest['dependencies'],'checks':results,'invalid_cli_rejected':True,'commands':commands,'runtime_sha256':{name:hashlib.sha256((W/name).read_bytes()).hexdigest() for name in manifest['files']},'passed':True}
(E/'packaging.json').write_text(json.dumps(report,indent=2)+'\n');print('Runtime closure, versions, relocation, determinism and CLI boundaries pass')
