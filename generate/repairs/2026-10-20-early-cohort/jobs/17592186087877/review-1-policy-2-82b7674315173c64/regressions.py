"""Strict independent acceptance regressions; previous implementation must fail both."""
import sys
sys.dont_write_bytecode=True
import argparse
import revision_audit as R
p=argparse.ArgumentParser();p.add_argument('--implementation',choices=['previous','current'],required=True);p.add_argument('--finding',choices=['shortcut','canonical'],required=True);args=p.parse_args()
g=R.G if args.implementation=='current' else R.module('retained_previous',R.PREV/'relocated-package/17592186087877.py')
if args.finding=='shortcut':
 rows=[g.generate('easy',8173,'signed_constant_power',parameters={'a':a,'n':2}) for a in ['1','-1']]
 checks=[{'prediction':R.A.shortcut(r),'key':R.A.key(r),'shortcut_success':R.A.shortcut(r)==R.A.key(r)} for r in rows]
 passed=not all(c['shortcut_success'] for c in checks)
else:
 rows=[g.generate('easy',19073,t,parameters=({'a':'2','b':v} if t=='constant_cos' else {'a':'2','n':v})) for t in ['constant_cos','scaled_constant_power','signed_constant_power'] for v in range(1,5)]
 if 'constant_exp' in g.TEMPLATES:rows.append(g.generate('easy',19073,'constant_exp',parameters={'a':'2','b':2,'c':-2}))
 target=R.A.V+2*R.A.Y-2*R.S.exp(-2*R.A.X)
 checks=[{'id':r['question'][':question/id'],'canonical_equation':R.S.simplify(R.A.normalized(R.A.prompt_equation(r)[1])-target)==0} for r in rows];passed=any(c['canonical_equation'] for c in checks)
 if passed:
  canonical=next(r for r,c in zip(rows,checks) if c['canonical_equation']);R.A.math_check(canonical)
R.save(f'regression-{args.implementation}-{args.finding}.json',{'command':f'{sys.executable} '+ ' '.join(sys.argv),'passed':passed,'records':rows,'checks':checks})
print(('PASS' if passed else 'FAIL')+' '+args.implementation+' '+args.finding)
raise SystemExit(0 if passed else 1)
