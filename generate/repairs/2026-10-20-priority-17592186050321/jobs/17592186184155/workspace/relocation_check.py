"""Exercise only manifest runtime files, with an explicit asset output directory."""
import hashlib,json,os
from pathlib import Path
import subprocess,tempfile,shutil,sys
root=Path(__file__).resolve().parent
manifest=json.loads((root/'package.json').read_text())
with tempfile.TemporaryDirectory(prefix='power-sum-relocation-') as directory:
    stage=Path(directory)/'package';stage.mkdir();assets=Path(directory)/'assets';assets.mkdir()
    for name in manifest['files']:
        src=root/name;target=stage/name;target.parent.mkdir(exist_ok=True,parents=True);shutil.copy2(src,target)
    env={**os.environ,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets),'PYTHONDONTWRITEBYTECODE':'1'}
    cmd=[sys.executable,'-I',str(stage/manifest['entrypoint']),'--difficulty','hard','--count','5','--seed','20261020','--format','json']
    # -I excludes the script directory too; use a regular invocation with an empty PYTHONPATH instead.
    cmd.remove('-I');env['PYTHONPATH']=''
    output=subprocess.check_output(cmd,cwd=directory,env=env)
    records=json.loads(output)
    assert len(records)==5
    original=subprocess.check_output([sys.executable,str(root/manifest['entrypoint']),*cmd[2:]],cwd=root,env=env)
    assert output==original
    names=sorted(str(p.relative_to(stage)) for p in stage.rglob('*') if p.is_file())
    assert names==sorted(manifest['files'])
    result={'passed':True,'records':5,'identical_to_workspace':True,'runtime_files':names,'undeclared_runtime_files':[],
       'generated_assets':len(list(assets.iterdir())),'dependencies':manifest['dependencies'],
       'runtime_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in manifest['files']}}
(root/'evidence/relocation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'relocation_passed':True,'records':5,'generated_assets':0}))
