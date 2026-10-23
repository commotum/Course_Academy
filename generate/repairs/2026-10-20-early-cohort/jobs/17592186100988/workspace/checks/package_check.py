import hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'evidence'
m=json.loads((ROOT/'package.json').read_text());expected=json.loads((OUT/'prospective-batch.json').read_text())
with tempfile.TemporaryDirectory(prefix='relocated-',dir=OUT) as directory:
 p=pathlib.Path(directory)
 for name in m['files']:
  dest=p/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
 args=[sys.executable,str(p/m['entrypoint']),'--difficulty','easy','--count','5','--seed','4036014604','--format','json']
 result=subprocess.run(args,cwd=p,env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(OUT/'assets'),'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,check=True)
 assert json.loads(result.stdout)==expected
 guards=[]
 for extra in [['--count','0'],['--difficulty','unknown'],['--profile','overflow_locations','--field-type','blank']]:
  r=subprocess.run([sys.executable,str(p/m['entrypoint']),*extra],cwd=p,capture_output=True,text=True)
  assert r.returncode!=0;guards.append({'args':extra,'rejected':True})
report={'relocation':'passed','declared_files':m['files'],'runtime_hashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in m['files']},'dependencies':m['dependencies'],'invalid_cli':guards,'command':'/home/jake/Developer/Course_Academy/.venv/bin/python checks/package_check.py'}
(OUT/'packaging.json').write_text(json.dumps(report,indent=2)+'\n');print('Relocation, deterministic CLI replay, and invalid-input checks passed.')
