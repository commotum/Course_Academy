"""Relocate only declared runtime files and check the job's exact CLI output."""
import hashlib,json,os,pathlib,shutil,subprocess,sys
root=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((root/'package.json').read_text())
out=root/'evidence'; relocated=out/'relocated';relocated.mkdir(exist_ok=True)
for name in manifest['files']:
    p=pathlib.Path(name)
    assert not p.is_absolute() and '..' not in p.parts
    dest=relocated/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/p,dest)
args=['--difficulty','easy','--count','5','--seed','3129290382','--format','json']
cmd=[sys.executable,str(relocated/manifest['entrypoint']),*args]
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(out/'assets')}
actual=json.loads(subprocess.check_output(cmd,cwd=relocated,env=env))
expected=json.loads((out/'prospective-batch.json').read_text())
assert actual==expected,'Relocation or deterministic replay mismatch'
import sympy
assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{'sympy':sympy.__version__}}
report={'passed':True,'command':cmd,'records':len(actual),'declared_runtime_files':manifest['files'],'dependencies':manifest['dependencies'],'relocation_equal':True,'asset_files':list(map(str,(out/'assets').iterdir())),'runtime_sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in manifest['files']}}
(out/'packaging.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':True,'relocation_equal':True,'runtime_files':len(manifest['files'])}))
