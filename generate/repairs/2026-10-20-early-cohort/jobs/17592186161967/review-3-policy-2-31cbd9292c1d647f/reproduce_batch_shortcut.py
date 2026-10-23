"""Exit 1 if every delivered record permits this first-operation bypass.
Usage: context-python -B reproduce_batch_shortcut.py [records.json]
Input defaults to independently normalized runner batch, not a newly sampled batch.
"""
import sys,json,pathlib,collections
sys.dont_write_bytecode=True
from helpers import mats,ops,check
root=pathlib.Path(__file__).resolve().parent
rows=json.load(open(sys.argv[1] if len(sys.argv)>1 else root/'delivery-batch/accepted.json'))
results=[]
for r in rows:
 f=r['question'][':question/answer-fields'][0]
 pairs=[tuple(o[2] for o in ops(a[':answer/value'])) for a in f[':answer-field/choices']]
 magnitudes=tuple(collections.Counter(abs(z[d]) for z in pairs).most_common(1)[0][0] for d in (0,1))
 outlier=next(z for z in pairs if tuple(map(abs,z))!=magnitudes)
 first=(-1 if outlier[0]>0 else 1)*magnitudes[0]
 A,B=mats(r['question'][':question/problem']);p=next(i for i in range(3) if A[i]==B[i]);targets=[i for i in range(3) if i!=p]
 c=next(c for c in range(3) if A[p][c] and all(B[t][c]==0 for t in targets))
 second=-A[targets[1]][c]//A[p][c]
 idx=pairs.index((first,second));correct=check(r)
 results.append({'question_id':r['question'][':question/id'],'seed':r['generation']['seed'],'profile':r['generation']['bank_profile'],'outlier':outlier,'predicted':pairs[idx],'correct':pairs[correct],'success':idx==correct})
print(json.dumps({'strategy':'Oppose outlier first sign; use dominant first magnitude; calculate only second operation','correct':sum(z['success'] for z in results),'total':len(rows),'records':results},indent=2))
sys.exit(1 if rows and all(z['success'] for z in results) else 0)
