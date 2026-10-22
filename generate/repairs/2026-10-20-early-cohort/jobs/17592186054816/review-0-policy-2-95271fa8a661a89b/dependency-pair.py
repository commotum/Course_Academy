exec(open('audit.py').read().split('initial=digest()')[0])
c=['Z+','Q-','Z-','N']
rr=[record for record in [explicit_none_checkbox(g.make_record(g.number_instance('root',radicand=n,sign=1),c)) for n in [1,0]]]
save('counterfactual-none-pair.json',rr)
checks=[]
for r in rr:
 ex=expected(r);fs=r['question'][':question/answer-fields'];cc=[]
 for i,f in enumerate(fs):
  for a in f[':answer-field/choices']:
   cc.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if (a[':answer/value']=='true')==ex[i] else 'rejected','purpose':'Controlled zero-boundary dependency and opposite response'})
 checks.append({'label':'root='+r['generation']['instance']['expression'],'record':r,'checks':cc})
save('counterfactual-none-grader-input.json',checks)
save('counterfactual-none-result.json',{'change':'sqrt(1) to sqrt(0), fixed Z+, Q-, Z-, N candidates','expected':[[True,False,False,True,False],[False,False,False,False,True]],'actual':[expected(r) for r in rr],'explanation_consistent':[ 'leave every box unchecked' not in r['question'][':question/worked-solution'] for r in rr],'status':'failed','failure':'Zero target correctly flips explicit None to true, but zero-target explanation still instructs all unchecked.'})
print('Controlled zero-boundary pair saved; keys respond correctly, explanation fails.')
