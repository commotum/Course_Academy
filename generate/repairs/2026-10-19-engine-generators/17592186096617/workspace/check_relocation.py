import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
manifest=json.loads(Path('package.json').read_text());runtime=manifest['files']
with tempfile.TemporaryDirectory(prefix='course-academy-relocation-',dir='/tmp') as temp:
 root=Path(temp)/'package';root.mkdir();out=Path(temp)/'output';out.mkdir()
 for name in runtime:
  dest=root/name;dest.parent.mkdir(exist_ok=True,parents=True);dest.write_bytes(Path(name).read_bytes())
 env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(out),'PYTHONPATH':''}
 command=[sys.executable,str(root/manifest['entrypoint']),'--difficulty',manifest['default_difficulty'],'--count','5','--seed','2026','--format','json']
 r=subprocess.run(command,cwd='/tmp',env=env,check=True,capture_output=True,text=True)
 records=json.loads(r.stdout);assert len(records)==5
 local=subprocess.run([sys.executable,'generator.py','--difficulty','easy','--count','5','--seed','2026','--format','json'],check=True,capture_output=True,text=True)
 assert json.loads(local.stdout)==records
 assert sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())==sorted(runtime)
 assert not list(out.iterdir()) # generator has no diagrams/assets
 Path('evidence/runner-five.json').write_text(r.stdout)
 report={'passed':True,'records':len(records),'seed':2026,'difficulty':'easy','only_declared_files_copied':True,'outside_repo_cwd':'/tmp','deterministic_after_relocation':True,'no_runtime_writes':True,'runtime_files':{name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in runtime},'dependencies':manifest['dependencies']}
 Path('evidence/relocation.json').write_text(json.dumps(report,indent=2))
 print('relocation PASS: five easy records, identical output, no runtime writes')
