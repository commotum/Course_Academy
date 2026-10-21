from auditlib import *
import shutil
manifest=json.load(open(W/'package.json'));dest=E/'relocated';dest.mkdir(exist_ok=True)
for n in manifest['files']:
 p=pathlib.Path(n);assert not p.is_absolute() and '..' not in p.parts
 out=dest/p;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/p,out)
cmd=[sys.executable,str(dest/manifest['entrypoint']),'--difficulty','easy','--seed','732511','--count','5','--format','json']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(E/'runtime-assets'))
p=subprocess.run(cmd,cwd=dest,env=env,capture_output=True,text=True);q=subprocess.run(cmd,cwd=dest,env=env,capture_output=True,text=True)
(E/'relocation-stderr.txt').write_text(p.stderr+q.stderr);(E/'relocation-records.json').write_text(p.stdout)
dep={'python':platform.python_version(),'packages':{'sympy':S.__version__}}
before=json.load(open(E/'package-before.json'));after=hashes();
save('packaging.json',{'command':cmd,'exit_codes':[p.returncode,q.returncode],'deterministic':p.stdout==q.stdout,'relocated_count':len(json.loads(p.stdout)) if p.returncode==0 else None,'declared_dependencies':manifest['dependencies'],'actual_dependencies':dep,'dependencies_exact':dep==manifest['dependencies'],'runtime_files':manifest['files'],'external_output_handling':'No asset-producing path in package; runtime stdout records captured inside evidence, declared output-directory environment set to evidence.','package_unchanged':before==after,'changed_files':[k for k in set(before)|set(after) if before.get(k)!=after.get(k)],'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()})
print('packaging',p.returncode,q.returncode,p.stdout==q.stdout,dep==manifest['dependencies'],before==after)
