import json, pathlib, hashlib
base=pathlib.Path('../workspace')
json.dump({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in base.iterdir() if p.is_file()},open('package-hashes-before.json','w'),indent=2)
x=json.load(open('../source/inventory.json'))
rows=[]
for q in x['questions']:
 rows.append({'id':q.get(':question/id'),'entity_id':q.get(':db/id'),'keys':list(q),'generation':q.get(':question/generation'),'difficulty':q.get(':question/difficulty')})
json.dump(rows,open('inventory-summary.json','w'),indent=2)
print(json.dumps(rows[-5:],indent=2)[:7000])
print('package source keys',list(json.load(open(base/'source.json'))))
