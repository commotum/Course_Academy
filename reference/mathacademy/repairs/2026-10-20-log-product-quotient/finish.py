"""Verify committed pool eligibility, historical grading, and deployed package delivery."""
import os
from read import *
from scripts.generator_packages import materialize_package,verify_package
from scripts.generator_publish import validate_question

def flatten(entity,records):
 eid=entity[':db/id'];record={};records[str(eid)]=record
 for k,v in entity.items():
  if k==':db/id':continue
  def value(v):
   if isinstance(v,dict)and ':db/id'in v:
    if len(v)>1:flatten(v,records)
    return v[':db/id']
   if isinstance(v,list):return [value(x)for x in v]
   return str(v)if not isinstance(v,(str,int,float,bool,type(None)))else v
  record[k.lstrip(':')]=value(v)
 return eid
if __name__=='__main__':
 v=json.loads((HERE/'verification.json').read_text());assert v['passed']and v['committed'];state=json.loads((HERE/'content/committed.json').read_text());kp=state['kp'][0];records={};flatten(kp,records);fresh=[q[':db/id']for q in kp[':knowledge-point/questions']if not q.get(':question/retired')and q.get(':question/worked-solution')and all(f.get(':answer-field/correct')for f in q[':question/answer-fields'])];assert len(fresh)==7
 saved=[]
 for item in state['items']:
  q=next(q for q in kp[':knowledge-point/questions']if q[':db/id']==item[':task-item/content'][':db/id']);responseids={a[':db/id']for a in item.get(':task-item/responses',[])};response={str(f[':db/id']):str(a[':db/id'])for f in q[':question/answer-fields']for a in f[':answer-field/choices']if a[':db/id']in responseids};saved.append({'question':q[':db/id'],'responses':response})
 save('live-input.json',{'entities':records,'kp':KP,'expected_fresh':fresh,'retired':v['withdrawn_questions'],'saved':saved});deps=ROOT/'target/release/deps';cmd=['rustc','--edition=2024','-O',str(HERE/'check_live.rs')]
 for name in ('course_academy_engine','serde_json'):
  lib=max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns);cmd+=['--extern',name+'='+str(lib)]
 cmd+=['-L','dependency='+str(deps),'-o',str(HERE/'check-live')];p=subprocess.run(cmd,capture_output=True,text=True);(HERE/'live-build.stderr').write_text(p.stderr);p.check_returncode();subprocess.run([str(HERE/'check-live'),str(HERE/'live-input.json'),str(HERE/'live-verification.json')],check=True)
 runtime=HERE/'delivered';script=materialize_package(v['new_generator_reference'],Path(DB.config.math_root),runtime);p=subprocess.run([str(ROOT/'.venv/bin/python'),'-B',str(script),'--difficulty','moderate','--count','20','--seed','19','--format','json'],cwd=runtime,env=dict(DB.environment,PYTHONPATH=''),capture_output=True,text=True,timeout=90);(runtime/'stdout.json').write_text(p.stdout);(runtime/'stderr').write_text(p.stderr);p.check_returncode();out=json.loads(p.stdout);assert len(out)==20
 for r in out:
  validate_question(r['question']);params=r['generation']['parameters'];assert [params['signs'][i]for i in params['order']]==[1,1,-1]
  assert tuple(params['signs'])in (((1,1,-1),)if params['template']=='combine'else((1,-1,1),(-1,1,1)))
 verify_package(runtime,allow_outputs=True);v['published_package_executed']=True;v['published_execution_records']=len(out);v['live_pool_verification']=json.loads((HERE/'live-verification.json').read_text());v['deployed_filter_verified']=json.loads((HERE/'deployment-verification.json').read_text())['passed'];save('verification.json',v);print(json.dumps({'passed':True,'active_generated_questions':5,'fresh_gradable_questions':len(fresh),'withdrawn':len(v['withdrawn_questions']),'history_verified':len(saved),'published_execution_records':len(out)}))
