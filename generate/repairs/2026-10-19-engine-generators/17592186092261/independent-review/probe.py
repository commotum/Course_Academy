import json,sys,collections
from pathlib import Path
import review
import sympy as s
E=Path(__file__).resolve().parent
rs=json.load(open('records.json'))
probes=[]
for level in ['easy','moderate','hard']:
 acc=json.load(open('delivery-'+level+'/accepted.json'))
 if acc:print(level,'keys',list(acc[0]))
for r in rs:
 if r['generation']['template']=='q-107463':
  f=r['question'][':question/answer-fields'][0];print('hard',r['generation']['parameters'])
  for i,a in enumerate(f[':answer-field/choices']):print(i,a[':answer/id']==f[':answer-field/correct'][1],len(a[':answer/value']),a[':answer/value'])
