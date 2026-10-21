import json,sys,copy,re
from pathlib import Path
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'workspace'))
import generator as g
b=json.load(open('runner-batch.json'))[0]
p=copy.deepcopy(b['generation']['parameters']);p.pop('cases',None)
# Exact minimal relevant edit of the first runner record: C[2,1] from 0 to 1.
p['matrices'][2][1][0]=1
c=g.generate('easy',b['generation']['seed'],profile=b['generation']['profile'],parameters=p)
r=[b,c]
Path('c-counterfactual-records.json').write_text(json.dumps(r,indent=2)+'\n')
cases=[]
for label,record,expected_selected in [('before',b,'ABC'),('after',c,'AB')]:
 checks=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  letter=re.search(r'\$([ABC])\s*=',f[':answer-field/key'])[1]
  for a in f[':answer-field/choices']:
   expected=(a[':answer/value']=='true')==(letter in expected_selected)
   checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if expected else 'rejected','purpose':'C pivot dependency: exact runner instance before/after c21=1'})
 cases.append({'label':label,'record':record,'checks':checks})
Path('c-counterfactual-grader-input.json').write_text(json.dumps(cases,indent=2)+'\n')
Path('c-counterfactual-results.json').write_text(json.dumps({'command':'PYTHONDONTWRITEBYTECODE=1 /home/jake/Developer/Course_Academy/.venv/bin/python c_counterfactual.py','before_seed':924724049,'profile':'q-129214','change':'C[2,1] 0 -> 1, all other matrix entries and target held fixed','expected_selected':['ABC','AB'],'before_C':b['generation']['parameters']['matrices'][2],'after_C':p['matrices'][2],'expected_explanation':'C second-row pivot moves to column 1, equal to first row pivot; C must become unselected. A and B remain selected.'},indent=2)+'\n')
