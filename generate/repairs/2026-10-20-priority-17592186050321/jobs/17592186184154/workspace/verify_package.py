#!/usr/bin/env python3
"""Check the declared runtime in an isolated, relocated directory."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

root=pathlib.Path(__file__).resolve().parent
manifest=json.loads((root/'package.json').read_text())
with tempfile.TemporaryDirectory(prefix='relocated-runtime-',dir=root/'evidence') as temporary:
    relocated=pathlib.Path(temporary)
    for name in manifest['files']:
        destination=relocated/name
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(root/name,destination)
    arguments=['--difficulty','moderate','--count','5','--seed','20261020','--format','json']
    def execute(base,args):
        return subprocess.run([sys.executable,str(base/manifest['entrypoint']),*args],cwd=root/'evidence',capture_output=True,text=True)
    local=execute(root,arguments);moved=execute(relocated,arguments)
    assert local.returncode==moved.returncode==0
    assert json.loads(local.stdout)==json.loads(moved.stdout)
    for band in ('easy','hard'):
        result=execute(relocated,['--difficulty',band,'--count','1','--seed','0','--format','json'])
        assert result.returncode!=0 and not result.stdout
    report={'relocated_runtime_files':manifest['files'],'dependency_versions':manifest['dependencies'],
            'count':5,'identical_after_relocation':True,'unsupported_bands_rejected':['easy','hard'],
            'runtime_content_writes':[], 'note':'Python may create __pycache__; no generated content assets are used.'}
    (root/'evidence'/'relocation.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Relocated runtime: deterministic five-record batch; unsupported bands rejected.')
