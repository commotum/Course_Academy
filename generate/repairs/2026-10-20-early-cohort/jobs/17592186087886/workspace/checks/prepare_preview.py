"""Regenerate a small current-version render set; no publication."""
import importlib.util
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
s=importlib.util.spec_from_file_location('g',ROOT/'17592186087886.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
selected=[]
for t,shift in [('q-90600',-2),('q-14316',-2),('q-14323',-2),('q-8747',2)]:
    k=next(k for k in g.DOMAINS[t] if k!=g.ORIGINAL[t])
    selected.append(g.generate('easy',37,t,{'k':k,'shift':shift}))
(ROOT/'evidence/role-render-records.json').write_text(json.dumps(selected,indent=2)+'\n')
print('Prepared four current representative records')
