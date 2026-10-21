from audit import *
rs=json.load(open('independent-records.json'))+json.load(open('source-replays.json'))+json.load(open('../samples.json'))
checks=[]
for r in rs:
 try: checks.append(mathcheck(r))
 except Exception as e: checks.append({'id':r['question'][':question/id'],'error':repr(e),'passed':False})
save('math-results.json',checks)
src=json.load(open('source-extract.json'))['questions'];replay=json.load(open('source-replays.json'));results=[]
for q,r in zip(src,replay):
 fs={f[':answer-field/key']:f for f in r['question'][':question/answer-fields']};cs=[]
 for f in q[':question/answer-fields']:
  a=[parse(c[':answer/value']) for c in f[':answer-field/choices']];b=[parse(c[':answer/value']) for c in fs[f[':answer-field/key']][':answer-field/choices']]
  cs.append({'field':f[':answer-field/key'],'source_count':len(a),'replay_count':len(b),'full_bank_equivalent':len(a)==len(b) and all(any(s.simplify(v-w)==0 for w in b) for v in a)})
 results.append({'id':q[':question/id'],'source':q[':question/math-academy-id'],'comparisons':cs,'passed':all(c['full_bank_equivalent'] for c in cs)})
save('source-replay-results.json',results)
print(json.dumps({'math_count':len(checks),'math_failures':[c for c in checks if not c['passed']],'replay_failures':[c for c in results if not c['passed']]}))
