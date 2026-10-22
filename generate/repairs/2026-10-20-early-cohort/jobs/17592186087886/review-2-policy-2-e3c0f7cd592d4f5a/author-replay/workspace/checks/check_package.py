"""Executable regression for feedback legacy_packaging_or_sampling (history has no finding ID)."""
import ast
import hashlib
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
    files = manifest['files']
    assert 'package.json' not in files
    assert manifest['entrypoint'] in files
    assert manifest['dependencies']['python'] == sys.version.split()[0]
    modules = {Path(f).stem for f in files if f.endswith('.py') and '/' not in f}
    import importlib.metadata
    packages = manifest['dependencies']['packages']
    for name, version in packages.items():
        assert importlib.metadata.version(name) == version
    for name in files:
        p = Path(name)
        assert not p.is_absolute() and '..' not in p.parts
        if p.suffix == '.py':
            tree = ast.parse((ROOT/p).read_text())
            for n in ast.walk(tree):
                names = [a.name.split('.')[0] for a in n.names] if isinstance(n, ast.Import) else [n.module.split('.')[0]] if isinstance(n,ast.ImportFrom) and n.module else []
                for imported in names:
                    assert imported in sys.stdlib_module_names or imported in packages or imported in modules, f'Undeclared/unresolved runtime import: {imported}'
    with tempfile.TemporaryDirectory(prefix='ode-package-',dir=ROOT/'evidence') as temp:
        temp = Path(temp); package = temp/'relocated'; package.mkdir(); assets=temp/'assets';assets.mkdir()
        for name in files:
            dest = package/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
        before = {str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in package.rglob('*') if p.is_file()}
        env = {**os.environ,'PYTHONPATH':'','PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets)}
        command=[sys.executable,str(package/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','71','--format','json']
        a=subprocess.run(command,cwd=temp,env=env,capture_output=True,text=True,check=True,timeout=60)
        b=subprocess.run(command,cwd=temp,env=env,capture_output=True,text=True,check=True,timeout=60)
        assert a.stdout == b.stdout
        rows=json.loads(a.stdout);assert len(rows)==5
        for r in rows:
            f=r['question'][':question/answer-fields'][0]
            assert len(f[':answer-field/choices'])==5
            assert sum(a[':answer/id']==f[':answer-field/correct'][1] for a in f[':answer-field/choices'])==1
        after={str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in package.rglob('*') if p.is_file()}
        assert before==after,'Runtime wrote inside immutable package'
    report={'status':'pass','feedback_code':'legacy_packaging_or_sampling','history_finding_ids':[], 'note':'History retains an event code, with no named finding IDs. The event code is used in repair-regressions.json.', 'declared_files_only':True,'static_import_closure':True,'relocated_cli_records':5,'seed_determinism':True,'runtime_package_unchanged':True,'command':command}
    (ROOT/'evidence/package-regression.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','static_import_closure','relocated_cli_records')}))
if __name__=='__main__':main()
