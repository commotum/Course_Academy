"""Strict acceptance regressions; current package intentionally fails all modes.
Run: PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python reproduce_failure.py shortcut
"""
import sys,json
sys.dont_write_bytecode=True
from audit import g,dump,shortcut
mode=sys.argv[1] if len(sys.argv)>1 else 'shortcut'
if mode=='shortcut':
 p={'free_coefficients':[2,-3],'constants':[1,4],'mix':[1,1]}
 r=g.generate_easy(seed=90217,parameters=p)
 out=shortcut(r);dump('minimal-shortcut.json',{'record':r,'probe':out,'command':__doc__})
 assert not (out.get('unique_modes') and out.get('correct')), 'INCIDENTAL SHORTCUT: component modes recover the key without reading the system'
elif mode=='zero-slope':
 # Valid same-shape source-backed simplification: x constant, y parameter-dependent.
 g.generate_easy(seed=90217,parameters={'free_coefficients':[0,-3],'constants':[1,4],'mix':[1,1]})
elif mode=='equal-coordinates':
 # Valid consistent system x+y+4z=2, x+2y+6z=3; x=y=1-2z.
 g.generate_easy(seed=90217,parameters={'free_coefficients':[2,2],'constants':[1,1],'mix':[1,1]})
elif mode=='source':
 g.generate_easy(seed=90217,profile='q-131714',parameters={'scale':1,'offsets':[0,0,0]})
else:raise ValueError('mode must be shortcut, zero-slope, equal-coordinates, or source')
