"""Strict delivered-pool role regression; exits 1 for a frozen checkbox label.
Usage: python3 batch_role_probe.py delivery-batch/accepted.json batch-role-results.json
Control: python3 batch_role_probe.py delivery-independent/accepted.json control-role-results.json
"""
import json,re,sys
from pathlib import Path
r=json.load(open(sys.argv[1])); roles={x:[] for x in 'ABC'}
for record in r:
 for f in record['question'][':question/answer-fields']:
  label=re.search(r'\$([ABC])\s*=',f[':answer-field/key'])[1]
  c=f[':answer-field/correct']; aid=c[1] if isinstance(c,list) else c[':answer/id']
  selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==aid)=='true'
  roles[label].append({'question_id':record['question'][':question/id'],'selected':selected,'generation':record['generation']})
result={'command':' '.join(sys.argv),'input':sys.argv[1],'counts':{label:{'selected':sum(x['selected'] for x in entries),'unselected':sum(not x['selected'] for x in entries),'total':len(entries)} for label,entries in roles.items()},'cases':roles,'passed':all({x['selected'] for x in entries}=={False,True} for entries in roles.values()),'criterion':'For this role-variable finite practice pool, prevent a label-only action from correctly answering one checkbox decision in every record. This criterion is about this delivered pool, not every random seed or every mathematical family.'}
Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':result['passed'],'counts':result['counts']}))
sys.exit(0 if result['passed'] else 1)
