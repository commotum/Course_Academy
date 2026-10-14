exec(open('generate/scratch/17592186083240/reference/read-current.py').read().split("print('basis'")[0])
raw=json.load(open(R/'generate/scratch/17592186083240/source.json'))['record'];from edn import loads
old={q[':db/id']:q for q in raw[':knowledge-point/questions']}
for q in k[':knowledge-point/questions']:
 o=old[q[':db/id']]
 if json.loads(json.dumps(q,default=str))!=o:
  print(q[':question/math-academy-id'],[(key,'changed') for key in set(q)|set(o) if json.loads(json.dumps(q.get(key),default=str))!=o.get(key)])
