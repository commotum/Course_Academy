import sys,json
sys.dont_write_bytecode=True
from review_generator import *
qs=json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions'];results=[]
for label,path in [('prior',JOB/'review-0-policy-2-f24f201976da522d/relocated-package/17592186184219.py'),('current',W/'17592186184219.py')]:
 g=loadg(path);missing=[];cases=[]
 for q in qs:
  d=read(q);p={k:d[k] for k in ('m','n','k','target')};mid=q[':question/math-academy-id']
  try:r=g.generate('easy',seed=67519,template=mid,parameters=p)
  except ValueError as ex:missing.append({'source_id':q[':question/id'],'profile':mid,'parameters':p,'error':str(ex)})
  else:assert sorted(d['values'])==sorted(read(r)['values'])
 for seed in range(829001,829017):
  r=g.generate('easy',seed=seed,template='rank',profile='q-141220');d=independent(r);assert signature(r)==('rank',(1,1,1,1));cases.append({'seed':seed,'record':r,'second_largest_correct':sorted(d['values'])[-2]==d['c']})
 results.append({'package':label,'missing_source_cases':missing,'shortcut_successes':sum(x['second_largest_correct'] for x in cases),'shortcut_total':len(cases),'complete_records':cases})
assert len(results[0]['missing_source_cases'])==3 and results[0]['shortcut_successes']==16
assert len(results[1]['missing_source_cases'])==0 and results[1]['shortcut_successes']==5
save('regression-comparison.json',{'command':f'{PY} -B {E}/compare_regressions.py','results':results,'result':'Both historical defects reproduced on prior executable and absent under the same strict criteria in current executable. No self-authored check alone is used as acceptance.'})
print([(x['package'],len(x['missing_source_cases']),x['shortcut_successes'],x['shortcut_total']) for x in results])
