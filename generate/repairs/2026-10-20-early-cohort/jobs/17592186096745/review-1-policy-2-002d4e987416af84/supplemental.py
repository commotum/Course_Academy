import sys,json,pathlib
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(E.parent/'workspace'))
import generator as g
from review_math import check,correct_index
old=json.load(open(E/'shortcut-controls.json'))
replayed=[g.generate(template=r['generation']['template'],seed=r['generation']['seed']) for r in old]
assert all(a['question']==b['question'] and a['knowledge_point']==b['knowledge_point'] and {k:v for k,v in a['generation'].items() if k!='source_basis'}=={k:v for k,v in b['generation'].items() if k!='source_basis'} for a,b in zip(old,replayed))
new=[g.generate(template=t,seed=6748291+104729*j) for t in ('q-74625','q-131634') for j in range(8)]
records=replayed+new
(E/'supplemental-records.json').write_text(json.dumps(records,indent=2))
results=[check(r) for r in records]
(E/'supplemental-results.json').write_text(json.dumps({'command':f'{sys.executable} supplemental.py','prior_controls_question_replay':True,'generation_metadata_change':'source_basis updated from prior snapshot 3937 to supplied capture 5370','new_profile_control_seeds':[6748291+104729*j for j in range(8)],'checks':results,'failures':[r for r in results if r['errors']]},indent=2,default=str))
assert not any(r['errors'] for r in results)
cases=json.load(open(E/'grader-input.json'))
for r in records:
 q=r['question'];f=q[':question/answer-fields'][0];idx=correct_index(q)
 cases.append({'label':'supplemental:'+q[':question/id'],'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if j==idx else 'rejected','purpose':'Independent exact RREF / full solution check'} for j,a in enumerate(f[':answer-field/choices'])]})
(E/'grader-all-input.json').write_text(json.dumps(cases,indent=2))
print(json.dumps({'supplemental_records':len(records),'math_failures':0,'native_cases':len(cases)}))
