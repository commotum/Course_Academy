"""Prove the retained checks fail on the frozen pre-repair implementation."""
import sys,types,runpy
from common import *
import common
old=types.ModuleType('frozen_original');old.__file__=str(ROOT/'17592186119805.py')
exec(compile((E/'generator-before.py').read_text(),str(E/'generator-before.py'),'exec'),old.__dict__)
common.load_generator=lambda:old
original_save=common.save
common.save=lambda name,data:original_save('before-'+name,data)
sys.argv=['regressions.py']
try:runpy.run_path(str(ROOT/'checks/regressions.py'),run_name='__main__')
except SystemExit as e:assert e.code==1
else:raise AssertionError('Broken original unexpectedly passed')
result=json.loads((E/'before-regressions-all.json').read_text())
assert len(result['checks'])==4 and all(not c['passed'] for c in result['checks'])
print('All four strict finding checks fail on the frozen original, as required.')
