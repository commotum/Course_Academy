"""Validate publisher-rewritten identity/key wiring with the native grader."""
import sys,json
sys.dont_write_bytecode=True
from audit import *
cases=json.load(open(R/'grader-input.json'));normalization=[]
for label,rawfile,acceptedfile in [('fresh','independent-delivery-input.json','delivery-independent/accepted.json'),('runner','runner-batch.json','delivery-batch/accepted.json')]:
 before=json.load(open(R/rawfile));after=json.load(open(R/acceptedfile))
 for a,r in zip(before,after):
  aq,rq=a['question'],r['question'];checks=[];matching=aq[':question/problem']==rq[':question/problem'] and aq[':question/worked-solution']==rq[':question/worked-solution']
  p,q,t,h=promptdata(r)
  for fi,f in enumerate(rq[':question/answer-fields']):
   af=aq[':question/answer-fields'][fi];matching &= [z[':answer/value'] for z in f[':answer-field/choices']]==[z[':answer/value'] for z in af[':answer-field/choices']]
   for z in f[':answer-field/choices']:
    v=expr(z[':answer/value']);valid=eq(s.diff(v,x),p*v) and v!=0 if fi==0 else eq(s.diff(v,x)+p*v,q) and eq(v.subs(x,t),h)
    checks.append({'field_index':fi,'submitted_answer_id':z[':answer/id'],'expected':'accepted' if valid else 'rejected','purpose':'Post-normalization ID wiring and mathematical validity'})
  cases.append({'label':'delivered '+label+' '+rq[':question/id'],'record':r,'checks':checks});normalization.append({'stage':label,'pre_id':aq[':question/id'],'post_id':rq[':question/id'],'prompt_solution_choice_order_values_preserved':matching})
save('delivery-normalization.json',normalization);save('grader-input-complete.json',cases);assert all(v['prompt_solution_choice_order_values_preserved'] for v in normalization)
print(len(cases),'records',sum(len(z['checks']) for z in cases),'choice outcomes')
