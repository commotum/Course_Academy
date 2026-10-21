#!/usr/bin/env python3
"""Small admissible masses retain all ranks and a correct displayed solution."""
import sys
sys.dont_write_bytecode=True
import json,importlib.util
from pathlib import Path
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
from repair_checks import measure,independent_numeric
from qa_math import independent,g
p={'H':'12','v':'10','q':'1','c':'0.2','rin':'6','rout':'4'}
rows=[]
for rank,seed in [(1,2),(2,1),(3,7),(4,0),(5,5)]:
 r=g.generate('easy',seed=seed,template='q-336506',parameters=p)
 assert measure(r)['rank']==rank
 assert independent_numeric(r)=='1.7'
 independent(r)
 rows.append({'seed':seed,'rank':rank,'question':r})
controls=json.loads((R/'evidence/same-bank-counterfactual-records.json').read_text())[:5]
for r in controls:independent(r)
(R/'evidence/low-mass-results.json').write_text(json.dumps({'passed':True,'command':sys.argv,'parameters':p,'independent_mass':'0.2*12-(10/12)^2 = 1.70555... -> 1.7','low_mass_cases':rows,'same_bank_full_displayed_equations_checked':5},indent=2)+'\n')
print(json.dumps({'passed':True,'low_mass_all_ranks':5,'same_bank_full_displayed_solutions':5}))
