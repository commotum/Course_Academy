import json,re,pathlib
D=pathlib.Path(__file__).parent
s=json.load(open('generate/runs/current/sources/17592186152119.json'))
(D/'source.json').write_text(json.dumps(s,indent=2)+'\n')
settings={
'q-218518':('easy','single_legacy_blank',[3,4,6],['x'],[1],[[3],[2],[5]],'spaced'),
'q-218519':('moderate','double_legacy_blank',[2,4,5],['u','v'],[0,-2],[[2,3],[3,2],[1,4]],'spaced'),
'q-112230':('moderate','double_radio',[5,6,12],['x','y'],[-5,-2],[[5,3],[3,3],[3,2]],'compact'),
'q-222127':('easy','single_blank',[3,9,2],['x'],[5],[[4],[1],[2]],'compact'),
'q-222129':('easy','single_blank',[8,2,10],['y'],[-7],[[3],[5],[2]],'compact'),
'q-222132':('moderate','double_blank',[3,8,2],['x','y'],[-7,2],[[1,3],[3,1],[5,2]],'compact'),
'q-76247':('easy','single_radio',[6,4,8],['x'],[-5],[[1],[3],[4]],'compact'),
'q-76475':('moderate','double_radio',[20,10,12],['x','y'],[0,2],[[7,1],[6,3],[4,2]],'compact'),
}
masks={}; cases=[]
for q in s['record'][':knowledge-point/questions']:
 sid=q[':question/math-academy-id']; level,template,c,v,h,e,notation=settings[sid]
 p={'coefficients':c,'variables':v,'shifts':h,'powers':e}
 item={'level':level,'template':template,'parameters':p,'notation':notation}
 for k in ('problem','worked-solution'):
  val=q.get(':question/'+k)
  if val:
   spans=[]; last=0
   for m in re.finditer(r'\$\$([\s\S]*?)\$\$|\$([^$]*?)\$',val):
    spans.append(val[last:m.start()]);spans.append({'math': m.group(1) if m.group(1) is not None else m.group(2),'display':m.group(1) is not None});last=m.end()
   spans.append(val[last:]);item[k]=spans
 masks[sid]=item
 cases.append({'source_id':sid,'level':level,'template':template,'parameters':p,'bank_profile':('raw-'+sid if sid in ('q-218518','q-218519') else 'observed-'+sid+('-raw-error' if sid=='q-222132' else '')),'authored_level_assignment':sid in ('q-218518','q-218519'),'missing_answer_completion':sid in ('q-218518','q-218519')})
for c in cases:
 if c['source_id'] in ('q-218518','q-218519'):c['normal_completion_profile']='completion-'+c['source_id']
(D/'masks.json').write_text(json.dumps(masks,indent=2)+'\n')
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
a=json.load(open('/home/jake/Developer/MA/DATA/Lessons/2626/Source/2626.json'))
(D/'missing-widget-evidence.json').write_text(json.dumps({'path':'/home/jake/Developer/MA/DATA/Lessons/2626/Source/2626.json','widgets':[i for i in a['lesson']['items'] if i.get('question_id') in ['218518','218519']]},indent=2)+'\n')
