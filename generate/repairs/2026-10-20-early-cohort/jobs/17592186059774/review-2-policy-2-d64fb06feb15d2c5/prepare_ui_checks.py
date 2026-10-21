from independent import *
load=lambda n:json.load(open(ROOT/n))
batch=load('delivery-batch/accepted.json');fresh=load('delivery-independent/accepted.json');cf=load('counterfactual-records.json');src=load('source-replays.json');ret=load('delivery-retained/accepted.json')
rs=batch+fresh+cf+src+ret
grade=[]
for i,r in enumerate(rs):
 a=analyze(r);vs=r['question'][':question/answer-fields'][0][':answer-field/choices']
 grade.append({'label':str(i)+' '+a['id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if j==a['position'] else 'rejected','purpose':'Visible exact Fraction operation application, including controlled counterfactuals'} for j,v in enumerate(vs)]})
save('grader-input.json',grade)
save('render-records.json',batch+cf+[next(r for r in src if r['generation']['bank_profile']=='q-130301')])
save('delivery-identity-results.json',[{'raw_id':before['question'][':question/id'],'delivered_id':after['question'][':question/id'],'generation_preserved':before['generation']==after['generation'],'visible_prompt_preserved':before['question'][':question/problem']==after['question'][':question/problem'],'analysis':analyze(after)} for before,after in zip(load('runner-batch.json'),batch)])
print(json.dumps({'native_cases':len(grade),'checks':5*len(grade),'render_records':11}))
