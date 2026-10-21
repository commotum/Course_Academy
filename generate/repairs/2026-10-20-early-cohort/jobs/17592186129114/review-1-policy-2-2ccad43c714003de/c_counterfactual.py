from reviewlib import *
from copy import deepcopy
old=json.load(open(ROOT/'historical-runner-batch.json'))[0]
p=deepcopy(old['generation']['parameters']);p.pop('cases',None)
assert old['generation']['seed']==924724049 and old['generation']['profile']=='q-129214'
assert p['matrices'][2]==[[-2,-2,-2,-1],[0,3,-5,5],[0,0,0,7]]
before=g.generate('easy',924724049,profile='q-129214',parameters=p)
p['matrices'][2][1][0]=1
after=g.generate('easy',924724049,profile='q-129214',parameters=p)
p['matrices'][2][1][0]=0;p['matrices'][2][0][3]=8
irrelevant=g.generate('easy',924724049,profile='q-129214',parameters=p)
rs=[before,after,irrelevant];results=[examine(r) for r in rs]
assert [x['selected'] for x in results]==['ABC','AB','ABC']
assert all(not x['errors'] for x in results)
assert 'c_{21}=1' in after['question'][':question/worked-solution']
save('c-counterfactual-records.json',rs)
save('c-counterfactual-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python c_counterfactual.py','seed':924724049,'profile':'q-129214','change':'C[2,1] 0 -> 1 invalidates strictly increasing pivots; C[1,4] -1 -> 8 does not affect pivots','results':results})
cases=[]
for i,r in enumerate(rs):
 checks=[]
 for j,f in enumerate(r['question'][':question/answer-fields']):
  yes=ref(ms(f[':answer-field/key'])[0])[0]!=('**not**' in r['question'][':question/problem'])
  for a in f[':answer-field/choices']:
   checks.append({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==yes else 'rejected','purpose':'Independent controlled C dependency, both checkbox states'})
 cases.append({'label':f'c-controlled-{i}','record':r,'checks':checks})
save('c-counterfactual-grader-input.json',cases)
print(json.dumps({'selections':[x['selected'] for x in results],'errors':sum((x['errors'] for x in results),[])}))
