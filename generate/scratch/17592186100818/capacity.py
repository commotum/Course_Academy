"""Exhaust actual finite task domain without rendering or bank identities."""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,itertools,json
from pathlib import Path
import sympy as s
H=Path(__file__).parent;z=importlib.util.spec_from_file_location('kp00818_capacity_gen',H.with_suffix('.py'));G=importlib.util.module_from_spec(z);z.loader.exec_module(G);x=G.x;xp=s.Symbol('positive_x',positive=True)
ratios=sorted({s.Rational(m,d)for m in range(1,7)for d in range(1,7)});assert len(ratios)==23
levels={l:set()for l in('easy','moderate','hard')};profiles={}
for sid in G.QS:
 c,F,v,lo,hi,end=G.R.integral(G.source_integral(sid));assert not end;tasks=set()
 for k in range(1,7):
  kernel=s.cancel(s.expand_log((c*F.subs(x,x/k)/k).subs(x,xp),force=False));bounds=list(map(s.srepr,[s.simplify(k*lo),s.simplify(k*hi)]))
  for t in ratios:
   fp=G.digest({'integrand':s.srepr(s.cancel(t*kernel)),'bounds':bounds,'domain':'positive x; real logarithm; original continuous u-interval, convergent endpoint allowed'});tasks.add(fp);levels[G.CONFIG[sid]].add(fp)
 profiles[sid]=len(tasks);assert len(tasks)==138
out={'reduced_coefficient_scales':list(map(str,ratios)),'per_profile_actual_math_tasks':profiles,'per_difficulty_actual_math_tasks':{k:len(v)for k,v in levels.items()},'global_actual_math_tasks':len(set.union(*levels.values())),'batch_limit':100,'profile_bank_contracts':34,'fingerprint':'Canonical integrand on positive x, actual ordered bounds and real interval domain; no seed/profile/bank/field shape'}
(H/'capacity.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in('per_profile_actual_math_tasks','reduced_coefficient_scales')},indent=2))
