"""Refresh records after restoring source intermediate-u solution steps."""
import json
import generator as g
from validate import independent
path='evidence/probe-records.json';records=json.load(open(path));count=0
for i,r in enumerate(records):
 if r['generation']['template'] not in ['slope_sqrt_quadratic_radio','slope_reciprocal_blank']:continue
 m=r['generation'];r=g.generate(r['question'][':question/difficulty'].split('/')[-1],m['seed'],template=m['template'],profile=m['bank_profile'])
 independent(r);records[i]=r;count+=1
json.dump(records,open(path,'w'),indent=2)
print('Refreshed and independently checked',count,'affected records')
