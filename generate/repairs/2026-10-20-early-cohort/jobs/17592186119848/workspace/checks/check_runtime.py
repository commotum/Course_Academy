"""Reproduce the retained external-import failure using only declared files."""
import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT/'package.json').read_text())
    local_modules = {Path(f).stem for f in manifest['files'] if f.endswith('.py')}
    third_party = set(manifest['dependencies']['packages'])
    unresolved = []
    for name in manifest['files']:
        if not name.endswith('.py'):
            continue
        tree = ast.parse((ROOT/name).read_text())
        for node in ast.walk(tree):
            modules = [a.name.split('.')[0] for a in node.names] if isinstance(node,ast.Import) else [node.module.split('.')[0]] if isinstance(node,ast.ImportFrom) and node.module else []
            unresolved += [m for m in modules if m not in sys.stdlib_module_names | local_modules | third_party]
    assert not unresolved, f'Undeclared/unresolved runtime import: {unresolved}'
    with tempfile.TemporaryDirectory(prefix='rank-relocation-') as tmp:
        folder = Path(tmp)
        for name in manifest['files']:
            dest = folder/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/name,dest)
        env = {k:v for k,v in os.environ.items() if k not in ('PYTHONPATH','PYTHONHOME')}
        env['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'] = str(folder/'generated-assets')
        args = [sys.executable,str(folder/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','0','--format','json']
        result = subprocess.run(args,cwd=folder,env=env,text=True,capture_output=True)
        assert result.returncode == 0, result.stderr
        records = json.loads(result.stdout)
        assert len(records)==5 and all(r['question'][':question/answer-fields'] for r in records)
        again = subprocess.run(args,cwd=folder,env=env,text=True,capture_output=True,check=True)
        assert result.stdout == again.stdout
        # Runtime must not create undeclared assets or write into the package.
        assert not list(folder.rglob('*.png'))
    report = {'passed':True,'finding':'legacy_packaging_or_sampling','tested':'AST import closure and twice executed isolated relocated CLI using only manifest files','count':len(records),'deterministic':True,'command':'python checks/check_runtime.py'}
    (ROOT/'evidence/runtime-regression.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__': main()
