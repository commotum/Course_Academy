"""Distinguish legitimate reading simplification from bank-only predictors."""
from audit import *
results=[]
for r in load(E/'delivery-batch/accepted.json'):
 target=visible(r['question']);f=r['question'][':question/answer-fields'][0]
 vals=[mat(a[':answer/value']) for a in f[':answer-field/choices']]
 eligible=[i for i,m in enumerate(vals) if len(m)==2 and len(m[0])==3]
 singles=[]
 for row in range(2):
  for col in range(3):
   hits=[i for i in eligible if vals[i][row][col]==target[row][col]]
   if len(hits)==1:singles.append({'row':row,'column':col,'visible_entry':str(target[row][col]),'answer_index':hits[0]})
 assert singles
 choice=f[':answer-field/choices'][singles[0]['answer_index']]
 assert choice[':answer/id']==f[':answer-field/correct'][1]
 results.append({'question_id':r['question'][':question/id'],'possible_sufficient_readings':singles,'selected_answer':choice[':answer/id'],'success':True})
save('sufficient-entry-results.json',{'command':f'{PY} -B {E}/sufficient_entry.py','rule':'Read the displayed equations to obtain a signed coefficient or RHS value, then use a unique match among correctly shaped options. The cell may vary by item.','results':results,'correct':sum(x['success'] for x in results),'total':len(results),'interpretation':'This uses relevant equation evidence and the intended mapping; it is not an incidental answer-bank-only strategy.'})
print(json.dumps({'sufficient_entry_success':len(results)}))
