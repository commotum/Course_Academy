import sys,json,importlib.util,itertools
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('draft',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
counts={};records={}
for level in ('easy','moderate','hard'):
 keys=set();small=(1,) if level=='easy' else (2,3);ratios=range(2,8) if level=='easy' else (range(3,5) if level=='moderate' else range(5,8));nonzero=[n for n in range(-7,8) if n]
 for small,m,b1,b2,X,Y in itertools.product(small,ratios,nonzero,nonzero,(-2,-1,1,2),(-2,-1,1,2)):
  p={'a1':small*m,'b1':b1,'c1':small*m*X+b1*Y,'a2':small,'b2':b2,'c2':small*X+b2*Y,'variables':'xy'}
  try:
   g.parameters_check(p,level);bank=g.bank(p,'authored-method-errors');g.check_bank(p,bank);g.check_radio_number_forms(p,bank)
  except (ValueError,ZeroDivisionError):continue
  keys.add(g.canonical_task(p))
 counts[level]=len(keys);assert len(keys)>=g.CAPACITY[level],counts
print(counts)
(D/'capacity.json').write_text(json.dumps({'status':'enumerated conservative lower bounds; no alias, row scaling, bank or layout inflation','domain':'positive first-variable coefficients; second row scaled; b coefficients signed1..7; solutions ±1,±2; xy only; ratios2..7 easy,3..4 moderate,5..7 hard','unique_systems_eligible_for_entire_authored_bank':counts,'supported_batch_capacity':g.CAPACITY,'full_sampler_cardinality':'finite but not claimed'},indent=2)+'\n')
