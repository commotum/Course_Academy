import json,re,pathlib,shutil
D=pathlib.Path(__file__).resolve().parent
s=json.load(open(D/'source.json'))
specs=[('q-161044','moderate','xy2',5,0,2,4),('q-38076','moderate','twoxy',4,-.5,.5,0),('q-161038','moderate','exp',16,1,1.5,3),('q-161039','easy','diff',4,0,2,3),('q-161041','easy','log',16,0,2,0),('q-83499','moderate','sum',4,-.5,0,4),('q-83500','moderate','linear',2,0,1,3),('q-83954','moderate','x',3,.5,1,4),('q-161043','easy','y2',25,0,2,2)]
data={};cases=[]
for qid,level,fam,n,a,b,ci in specs:
 q=next(q for q in s['record'][':knowledge-point/questions'] if q[':question/math-academy-id']==qid)
 rel=re.search(r'!\[\]\(([^)]+)\)',q[':question/problem'])[1]
 dest=D/'originals'/pathlib.Path(rel).name;dest.parent.mkdir(exist_ok=True);shutil.copyfile(pathlib.Path('/media/jake/SSD/EDB/math')/rel,dest)
 item={'level':level,'family':fam,'n':n,'alpha':str(a),'beta':str(b),'correct_index':ci,'image':str(dest),'source_id':qid,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'), 'bank':[x[':answer/value'] for x in q[':question/answer-fields'][0][':answer-field/choices']]}
 data[qid]=item;cases.append({'source_id':qid,'template':fam,'level':level,'parameters':{'radius_squared':n,'rotation':0},'bank_profile':qid,'authored_level':qid=='q-161044','missing_correct_designation':qid=='q-161044'})
(D/'templates.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n');(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
# Ordered curriculum route, using next pointers rather than collection order.
a=json.load(open('generate/runs/current/lessons/17592186049084.json'))['record'][0];ss={v[':db/id']:v for v in a[':activity/steps']};n=a[':activity/first-step'][':db/id'];route=[]
while n in ss:
 v=ss[n];c=v[':step/content'];route.append({'step':n,'content':c.get(':knowledge-point/title',c.get(':tutorial/title'))});n=v.get(':step/next',{}).get(':db/id')
(D/'lesson-route.json').write_text(json.dumps(route,indent=2)+'\n')
