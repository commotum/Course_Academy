"""Add normalized records to native/UI fixtures after running check_delivery."""
from independent import *
records=json.load(open(ROOT/'delivery-batch/accepted.json'))
render=json.load(open(ROOT/'render-records.json'));render[:5]=records;save('render-records.json',render)
cases=[c for c in json.load(open(ROOT/'grader-input.json')) if not c['label'].startswith('post-normalization ')]
for r in records:
    a=analyze(r);vs=r['question'][':question/answer-fields'][0][':answer-field/choices']
    cases.append({'label':'post-normalization '+a['id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if j==a['position'] else 'rejected','purpose':'Post-delivery identity rewrite: independent exact Fraction evaluation'} for j,v in enumerate(vs)]})
save('grader-input.json',cases)
save('delivery-identity-results.json',[{'raw_question_id':raw['question'][':question/id'],'delivered_question_id':after['question'][':question/id'],'generation_metadata_preserved':raw['generation']==after['generation'],'visible_problem_preserved':raw['question'][':question/problem']==after['question'][':question/problem'],'analysis':analyze(after)} for raw,after in zip(json.load(open(ROOT/'runner-batch.json')),records)])
