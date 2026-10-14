#!/usr/bin/env python3
"""Enumerate the actual finite sampler catalog; no seed/notation/bank aliases."""
import importlib.util,itertools,json
from pathlib import Path
import sympy as s
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
counts={};total=0
for name,d in g.FAMILIES.items():
 level='easy' if name=='constant' else 'hard' if name=='canonical' else 'moderate'
 if name=='constant':
  candidates=[(tuple(v for w in widths for v in (0,w)),a) for widths in itertools.combinations(range(2,6),3) for a in range(2,10)]
 else:
  xi=[(s.exp(a),s.exp(b)) for a,b in itertools.combinations(range(4),2)] if name=='log' else [(1,2),(1,3),(1,4),(2,3),(2,4)] if name=='canonical' else g.INTERVALS
  yi=[(1,2),(1,3),(1,4),(2,3),(2,4)] if name=='canonical' else g.INTERVALS
  zi=list(itertools.combinations([-s.pi/2,0,s.pi/2,s.pi,3*s.pi/2],2)) if name=='cos' else [(s.log(a),s.log(b)) for a,b in itertools.combinations(range(1,6),2)] if name=='exp' else g.INTERVALS
  candidates=[(tuple(v for pair in parts for v in pair),2) for parts in itertools.product(xi,yi,zi)]
 valid=0
 for b,a in candidates:
  b=tuple(map(s.sympify,b))
  try:g.guard(name,b,level);g.method_bank(name,b,a)
  except ValueError:continue
  valid+=1
 counts[name]={'level':level,'eligible_semantic_tasks':valid,'candidate_tasks':len(candidates)};total+=valid
 print(name,valid,'/',len(candidates),flush=True)
(ROOT/'catalog.json').write_text(json.dumps({'counts':counts,'eligible_total':total,'easy_permutation_aliases_excluded':True,'meaning':'actual sampler objects: field/constant partial and box; raw profile aliases and seeds excluded'},indent=2)+'\n')
