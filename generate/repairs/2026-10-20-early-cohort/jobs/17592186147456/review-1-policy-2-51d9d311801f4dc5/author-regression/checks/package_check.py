"""Executable runtime closure regression, including a relocated five-item CLI run."""
import ast
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys

H=Path(__file__).resolve().parents[1]
m=json.loads((H/'package.json').read_text())
declared=set(m['files'])
assert m['entrypoint'] in declared
local={Path(p).stem for p in declared if p.endswith('.py')}
external=set(m['dependencies']['packages'])
for p in declared:
    assert (H/p).is_file()
    if not p.endswith('.py'):continue
    tree=ast.parse((H/p).read_text())
    for n in ast.walk(tree):
        names=([n.module.split('.')[0]] if isinstance(n,ast.ImportFrom) and n.module
               else [a.name.split('.')[0] for a in n.names] if isinstance(n,ast.Import) else [])
        for name in names:
            assert name in sys.stdlib_module_names|local|external, f'Undeclared/unresolved runtime import: {name}'
for name,version in m['dependencies']['packages'].items():
    assert importlib.metadata.version(name)==version
assert sys.version.split()[0]==m['dependencies']['python']
destination=H/'evidence/relocated'
destination.mkdir(parents=True,exist_ok=True)
for p in declared:
    target=destination/p
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(H/p,target)
# -I removes cwd/PYTHONPATH. Permit only the relocated runtime path, stdlib
# and installed dependencies; a finder explicitly denies the old repo import.
bootstrap="""
import importlib.abc, runpy, sys
from pathlib import Path
class DenyRepository(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0]=='scripts':
            raise ImportError('Repository runtime imports are forbidden: '+fullname)
sys.meta_path.insert(0,DenyRepository())
p=Path(sys.argv[1]).resolve()
sys.path.insert(0,str(p.parent))
sys.argv=sys.argv[1:]
runpy.run_path(str(p),run_name='__main__')
"""
command=[sys.executable,'-I','-c',bootstrap,str(destination/m['entrypoint']),
         '--difficulty','easy','--seed','42','--count','5','--format','json']
outputs=[]
for _ in range(2):
    result=subprocess.run(command,cwd=destination,capture_output=True,text=True,check=True)
    records=json.loads(result.stdout)
    assert isinstance(records,list) and len(records)==5
    outputs.append(records)
assert outputs[0]==outputs[1], 'Seeded CLI replay differs'
(H/'evidence/relocation-records.json').write_text(json.dumps(outputs[0],indent=2)+'\n')
(H/'evidence/package-check.json').write_text(json.dumps({
    'status':'passed','runtime_files':m['files'],'records':5,
    'deterministic':True,'repository_imports_denied':True,
    'command':'python -I [deny-repository-import bootstrap] relocated/17592186147456.py --difficulty easy --seed 42 --count 5 --format json'
},indent=2)+'\n')
print('Runtime closure, relocation, count and deterministic replay passed')
