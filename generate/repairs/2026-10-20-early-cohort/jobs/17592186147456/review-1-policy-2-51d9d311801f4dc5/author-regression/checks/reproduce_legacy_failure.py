"""Expected failing reproduction of the original undeclared repository import."""
import json
from pathlib import Path
import subprocess
import sys
H=Path(__file__).resolve().parents[1]
code="""
import importlib.abc, runpy, sys
class DenyRepository(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0]=='scripts':
            raise ImportError('Undeclared/unresolved runtime import: scripts')
sys.meta_path.insert(0,DenyRepository())
sys.argv=[sys.argv[1],'--difficulty','easy','--seed','0']
runpy.run_path(sys.argv[0],run_name='__main__')
"""
result=subprocess.run([sys.executable,'-I','-c',code,str(H/'evidence/legacy-relocated/17592186147456.py')],capture_output=True,text=True)
assert result.returncode!=0
assert 'Undeclared/unresolved runtime import: scripts' in result.stderr
(H/'evidence/legacy-runtime-failure.json').write_text(json.dumps({'returncode':result.returncode,'stderr':result.stderr,'command':'python -I [deny scripts bootstrap] evidence/legacy-relocated/17592186147456.py --difficulty easy --seed 0'},indent=2)+'\n')
print('Original runtime fails on the exact undeclared scripts import; failure reproduced')
