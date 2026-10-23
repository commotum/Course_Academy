"""Strict regression. Exit 1 demonstrates the current family shortcut; no package writes.
Run: ../.../.venv/bin/python reproduce-shortcut.py [entrypoint]
"""
import sys,json,importlib.util,pathlib,re
from fractions import Fraction
sys.dont_write_bytecode=True
root=pathlib.Path(__file__).resolve().parent
entry=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'workspace/17592186059776.py'
spec=importlib.util.spec_from_file_location('target',entry);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
records=[];results=[]
for template in ['q-73544','q-73551','q-73554','q-73555']:
 for p in [[0,0],[1,1],[2,3],[-3,-3],[3,-3],[-3,3]]:
  r=g.generate('easy',31817,template,p);records.append(r);f=r['question'][':question/answer-fields'][0];key=f[':answer-field/correct'][1]
  vals=[]
  for a in f[':answer-field/choices']:
   body=re.search(r'\\begin\{array\}\{cc\|c\}(.*?)\\end\{array\}',a[':answer/value'],re.S)[1]
   vals.append(Fraction(body.split(r'\\')[1].split('&')[2].strip()))
  second=sorted(vals)[1];picked=[a[':answer/id'] for a,v in zip(f[':answer-field/choices'],vals) if v==second]
  results.append({'template':template,'parameters':p,'id':r['question'][':question/id'],'values':[str(v) for v in vals],'strategy_correct':picked==[key]})
(root/'shortcut-reproduction-records.json').write_text(json.dumps(records,indent=2))
(root/'shortcut-reproduction-results.json').write_text(json.dumps(results,indent=2))
failed=[t for t in {r['template'] for r in results} if all(r['strategy_correct'] for r in results if r['template']==t)]
print(json.dumps({'strategy':'Choose unique second-smallest bottom-right matrix entry','correct':sum(r['strategy_correct'] for r in results),'total':len(results),'failing_families':sorted(failed)}))
assert not failed, 'Fixed incidental answer rank survives changed equations in '+str(sorted(failed))
