#!/usr/bin/env python3
import hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];manifest=json.loads((ROOT/'package.json').read_text());python='/home/jake/Developer/Course_Academy/.venv/bin/python'
version=subprocess.check_output([python,'-c','import platform;print(platform.python_version())'],text=True).strip()
assert manifest['dependencies']=={'python':version,'packages':{}}
assert 'package.json' not in manifest['files']
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
args=['--difficulty','easy','--count','5','--seed','827461','--format','json']
expected=subprocess.check_output([python,str(ROOT/manifest['entrypoint']),*args],env=env)
with tempfile.TemporaryDirectory(prefix='special-sets-relocation-') as temp:
    p=Path(temp)
    for name in manifest['files']:
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        dest=p/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,dest)
    output=p/'assets';output.mkdir();env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR']=str(output)
    actual=subprocess.check_output([python,str(p/manifest['entrypoint']),*args],cwd=p,env=env)
    assert actual==expected
    assert not list(output.iterdir()),'No asset files are required by this family'
    replay=json.loads(subprocess.check_output([python,str(p/manifest['entrypoint']),'--replay-source','all'],cwd=p,env=env));assert len(replay)==11
    for invalid in [['--difficulty','hard'],['--count','-1']]:
        proc=subprocess.run([python,str(p/manifest['entrypoint']),*invalid],cwd=p,env=env,capture_output=True)
        assert proc.returncode!=0
result={'status':'passed','python':version,'relocation':'identical seeded output with only declared runtime files','source_banks':11,'invalid_input_rejected':True,'runtime_hashes':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in manifest['files']}}
(ROOT/'evidence/packaging-results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='runtime_hashes'}))
