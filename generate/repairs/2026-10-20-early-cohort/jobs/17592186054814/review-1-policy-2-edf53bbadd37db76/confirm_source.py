import json,pathlib,hashlib
job=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186054814')
prev=job/'review-0-policy-2-0209d130634fb923'
src=json.load(open(job/'source/source.json')); a=json.load(open(prev/'source-analysis.json'))
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values(): yield from walk(v)
 elif isinstance(x,list):
  for v in x: yield from walk(v)
objs=list(walk(src)); results=[]
for c in a['source_cases']:
 matches=[o for o in objs if o.get(':question/id')==c['id'] and ':question/problem' in o]
 assert matches
 q=matches[0]
 assert q[':question/problem']==c['prompt']
 assert q.get(':question/answer-fields',[])==c['fields']
 assert q.get(':question/worked-solution')==c['solution']
 results.append({'id':c['id'],'prompt_fields_solution_match':True})
strings=[v for o in objs for v in o.values() if isinstance(v,str)]
for p in a['source_passages']:
 assert any(p['quote'] in s for s in strings),p
json.dump({'source_hash':hashlib.sha256((job/'source/source.json').read_bytes()).hexdigest(),'confirmed_cases':results,'confirmed_passages':a['source_passages'],'provenance':str(prev/'source-analysis.json')},open('source-confirmation.json','w'),indent=2)
a['provenance']={'reused_from':str(prev/'source-analysis.json'),'confirmation':'source-confirmation.json','note':'All cited passages and complete case data reconfirmed before reading current author material.'}
json.dump(a,open('source-analysis.json','w'),indent=2)
assert pathlib.Path('source-analysis.json').stat().st_size>0
print('Confirmed and wrote source-analysis.json:',len(results),'source cases')
