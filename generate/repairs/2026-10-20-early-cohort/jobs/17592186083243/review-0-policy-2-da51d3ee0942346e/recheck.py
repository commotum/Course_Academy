from review import *
r=json.load(open('source-replays.json'))+json.load(open('samples-independent.json'))+json.load(open('batch.json'))+json.load(open('counterfactual-records.json'))
out=[]
for x in r:
 try: out.append(mathcheck(x))
 except Exception as e:out.append({'id':x['question'][':question/id'],'template':x['generation']['template'],'error':repr(e)})
save('math-results.json',out)
print('math',len(out),'errors',sum('error' in x for x in out))
