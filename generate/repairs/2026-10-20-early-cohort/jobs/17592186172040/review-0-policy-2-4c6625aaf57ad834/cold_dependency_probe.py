"""Strict cold-cache test. Default hides undeclared Python 3.10. --allow-external is the control.
Run with repo .venv/bin/python; original package stays read-only, all writes stay under evidence_root.
"""
from review import *
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--allow-external',action='store_true');a=ap.parse_args()
name='external-control' if a.allow_external else 'declared-only'
cache=RT/('cold-'+name);cache.mkdir(exist_ok=True)
extra=['--bind',str(cache),str(PK/KP/'plots')]
if not a.allow_external:extra+=['--ro-bind',str(RT/'no-exec'),'/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10']
p=run('cold-'+name+'-result.json',[P,PK/(KP+'.py'),'--difficulty','moderate','--seed','801239','--count','1','--format','json'],extra)
if p.returncode:
 print(p.stderr[-850:]);sys.exit(p.returncode)
r=json.loads(p.stdout);assert len(r)==1
print('Cold render succeeded:',name)
