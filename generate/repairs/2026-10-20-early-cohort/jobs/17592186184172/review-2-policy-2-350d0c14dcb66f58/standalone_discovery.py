import runpy,pathlib,sys
from unittest.mock import patch
orig=pathlib.Path.is_file
root=pathlib.Path(sys.argv[1]).parent
original=root/'17592186184172.py'
sys.argv=[str(original),'--difficulty','moderate','--count','5','--seed','0']
def declared_only(p):
 if str(p).endswith('/scripts/generator_policy.py'): return False
 return orig(p)
with patch.object(pathlib.Path,'is_file',declared_only):runpy.run_path(str(original),run_name='__main__')
