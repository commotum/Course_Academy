"""Exercise the exact previously broken runtime closure from another directory."""
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT/'package.json').read_text())
with tempfile.TemporaryDirectory(prefix='imt-relocated-') as d:
    folder = Path(d)
    for name in manifest['files']:
        target = folder/name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, target)
    # Reject imports unresolved by the declared closure, even if locally available.
    imports = set()
    for name in manifest['files']:
        if name.endswith('.py'):
            for node in ast.walk(ast.parse((folder/name).read_text())):
                if isinstance(node, ast.Import): imports.update(a.name.split('.')[0] for a in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module: imports.add(node.module.split('.')[0])
    local = {Path(f).stem for f in manifest['files'] if f.endswith('.py')}
    assert not imports - local - sys.stdlib_module_names, imports-local-sys.stdlib_module_names
    # -P disallows accidental cwd injection; script directory is explicitly provided.
    command = [sys.executable, '-I', '-c',
        'import runpy,sys;sys.argv=sys.argv[1:];sys.path.insert(0,sys.argv.pop(0));runpy.run_path(sys.argv[0],run_name="__main__")',
        str(folder), str(folder/manifest['entrypoint']), '--difficulty','moderate','--count','5','--seed','24629','--format','json']
    completed = subprocess.run(command, cwd='/tmp', text=True, capture_output=True)
    assert completed.returncode == 0, completed.stderr
    rows = json.loads(completed.stdout)
    assert len(rows) == 5
    assert all(r['question'][':question/answer-fields'] for r in rows)
    assert {str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts} == set(manifest['files'])
    result = {'status':'pass','relocated_records':len(rows),'undeclared_imports':[], 'python':sys.version.split()[0],
              'command':'python -I -c <runpy launcher with only relocated package on import path> <package> <entrypoint> --difficulty moderate --count 5 --seed 24629 --format json',
              'runtime_files':manifest['files']}
    (ROOT/'evidence/relocation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
