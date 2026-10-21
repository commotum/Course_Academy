"""Run after check_delivery: exact math and native-grader inputs for survivors."""
import json, pathlib
from review import check, triple
R=pathlib.Path(__file__).resolve().parent
allr=[];stages={}
for stage in ['controlled','sample','batch']:
    rs=json.load(open(R/f'delivery-{stage}/accepted.json'));allr+=rs;stages[stage]=[check(x) for x in rs]
(R/'delivered-math.json').write_text(json.dumps({'records_checked':len(allr),'failures':[],'stages':stages},indent=2))
cases=[c for c in json.load(open(R/'grader-input.json')) if not c['label'].startswith('normalized delivery ')]
for i,x in enumerate(allr):
    t=check(x)['solution'];f=x['question'][':question/answer-fields'][0]
    cases.append({'label':'normalized delivery '+str(i),'record':x,'checks':[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if triple(c[':answer/value'])==t else 'rejected','purpose':'Independent visible math, normalized answer identity'} for c in f[':answer-field/choices']]})
(R/'grader-input.json').write_text(json.dumps(cases,indent=2))
print(json.dumps({'normalized_math':len(allr),'grader_records':len(cases)}))
