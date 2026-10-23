"""Fail on the demonstrated q-13498 answer-only cue. Accepts explicit candidate records.
Usage: python3 regression_shortcut.py batch.json shortcut-regression.json
This tests a specific cue, not general acceptance; source/profile removal is not a repair.
"""
import json,re,sys
records=json.load(open(sys.argv[1]));out=[]
for r in records:
 for f in r['question'][':question/answer-fields']:
  if f[':answer-field/type']!=':answer-field.type/radio':continue
  opts=[]
  for a in f[':answer-field/choices']:
   m=re.search(r'_\{(\d)(\d)\}',a[':answer/value'])
   if m:opts.append((tuple(map(int,m.groups())),a))
  if len(opts)!=5:continue
  mi=min(p[0] for p,a in opts);mj=min(p[1] for p,a in opts)
  if sorted((p[0]-mi,p[1]-mj) for p,a in opts)!=[(0,0),(0,1),(0,2),(1,0),(1,1)]:continue
  prediction=next(a for p,a in opts if p==(mi,mj+1))
  out.append({'question_id':r['question'][':question/id'],'seed':r['generation']['seed'],'prediction':prediction[':answer/value'],'success':prediction[':answer/id']==f[':answer-field/correct'][1], 'record':r})
report={'command':sys.argv,'cue':'Five choices form three consecutive columns in smaller row and two leftmost columns in next row. Choose middle column of smaller row, never read matrix.','baseline':0.2,'attempts':len(out),'correct':sum(x['success'] for x in out),'observations':out,'failure':bool(out) and all(x['success'] for x in out)}
json.dump(report,open(sys.argv[2],'w'),indent=2)
print(json.dumps({k:v for k,v in report.items() if k!='observations'}));sys.exit(1 if report['failure'] else 0)
