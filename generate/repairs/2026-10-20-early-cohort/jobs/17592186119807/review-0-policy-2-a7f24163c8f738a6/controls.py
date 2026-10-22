"""Rebuild irrelevant-label fixture after finish-tests.py; no package writes."""
import json,copy,uuid,pathlib
E=pathlib.Path(__file__).resolve().parent
rs=json.loads((E/'consistency-pair.json').read_text());r=copy.deepcopy(rs[0]);q=r['question']
for key in [':question/problem',':question/worked-solution']:
 q[key]=q[key].replace('{c}_{1}','{a}_{1}').replace('{c}_{2}','{a}_{2}').replace('=d','=b').replace('\\,d=','\\,b=')
q[':question/id']=str(uuid.uuid5(uuid.NAMESPACE_URL,'independent-review-renamed-control'));r['generation']={'audit_control':True,'not_generator_output':True,'construction':'Independent irrelevant-evidence control: rename c1,c2,d to a1,a2,b; every numeric entry and response preserved.'};rs.append(r)
for name in ['controlled-records.json','controlled-render-records.json']:(E/name).write_text(json.dumps(rs,indent=2))
cases=[]
for i,r in enumerate(rs):
 f=r['question'][':question/answer-fields'][0];cases.append({'label':'controlled-'+str(i),'record':r,'checks':[{'submitted_answer_id':o[':answer/id'],'expected':'accepted' if o[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'relevant consistency switch and irrelevant vector-label rename'} for o in f[':answer-field/choices']]})
(E/'controlled-grader-input.json').write_text(json.dumps(cases,indent=2))
