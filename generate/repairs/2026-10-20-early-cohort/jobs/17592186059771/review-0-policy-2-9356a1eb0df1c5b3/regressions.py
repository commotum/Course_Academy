"""Strict independent source acceptance tests. Current package must fail these.
Run: /home/jake/Developer/Course_Academy/.venv/bin/python -B regressions.py
No package or database writes; emits regression-results.json here.
"""
import sys,json,pathlib,re
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(E.parent/'workspace'))
import generator as g
src=json.load(open(E.parent/'source/source.json'))['material']['kp'][':knowledge-point/questions']
results=[]
for sid,d,p in [('q-10251','easy',{'matrix':[[-1,0,1],[1,0,0],[-1,1,0]],'rows':[0,2]}),('q-10243','moderate',{'matrix':[[0,3,4],[0,1,2],[0,5,6]],'target':2,'source':1,'k':-5,'name':'G'})]:
 original=next(q for q in src if q[':question/math-academy-id']==sid)
 try:
  r=g.generate(d,seed=991,profile=sid,parameters=p)
  bank={re.sub(r'\s','',a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']}
  expected={re.sub(r'\s','',a[':answer/value']) for a in original[':question/answer-fields'][0][':answer-field/choices']}
  results.append({'case':sid,'parameters':p,'passed':bank==expected,'source_id':original[':question/id']})
 except Exception as e:results.append({'case':sid,'parameters':p,'passed':False,'error':type(e).__name__+': '+str(e),'source_id':original[':question/id']})
# Essential same-donor/two-destination family is present in three supplied hard cases.
# Count destinations from delivered prompts, without using generator metadata.
records=[g.generate('hard',seed) for seed in range(72011,72071)]
rows=[re.findall(r'\{R\}_\{(\d)\}\s*&\s*:=',r['question'][':question/problem']) for r in records]
results.append({'case':'hard distinct destinations supported by q-130064, q-130065, q-10245','seeds':[72011,72070],'passed':any(len(set(x))==2 for x in rows),'observed_distinct_destination_counts':sorted(set(len(set(x)) for x in rows)),'construction_proof':'hard.operations() returns p[target] for both operations; validate() requires the remaining rows as two distinct donors. Thus absence is structural, not inferred from sample size alone.'})
(E/'regression-results.json').write_text(json.dumps({'command':sys.executable+' -B regressions.py','results':results},indent=2)+'\n')
print(json.dumps(results));sys.exit(0 if all(x['passed'] for x in results) else 1)
