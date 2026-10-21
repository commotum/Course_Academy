"""Execute disposable copies of the actual committed immutable packages."""
import concurrent.futures,os
from read import *
from scripts.generator_packages import materialize_package,verify_package
from scripts.generator_policy import checkbox_selection
from scripts.generator_publish import validate_question

def run(update):
 runtime=HERE/'delivered'/str(update['kp']);script=materialize_package(update['reference'],Path(DB.config.math_root),runtime)
 prior=next(r for r in json.loads((HERE/'cli-audit.json').read_text())if r['kp']==update['kp']);level=next(r['level']for r in prior['levels']if r.get('passed'))
 p=subprocess.run([str(ROOT/'.venv/bin/python'),'-B',str(script),'--difficulty',level,'--count','4','--seed','37','--format','json'],cwd=runtime,env=dict(DB.environment,PYTHONPATH=''),capture_output=True,text=True,timeout=120);(runtime/'execution.stdout').write_text(p.stdout);(runtime/'execution.stderr').write_text(p.stderr);p.check_returncode();records=json.loads(p.stdout);records=records.get('records',[records])if isinstance(records,dict)else records
 count=0
 for r in records:
  validate_question(r['question']);selection=checkbox_selection(r)
  if selection:
   assert any(selection);fields=r['question'][':question/answer-fields'];assert len([f for f in fields if f[':answer-field/key']=='None of the above'])==1;count+=1
 assert count>0;verify_package(runtime,update['digest'],allow_outputs=True)
 return {'kp':update['kp'],'reference':update['reference'],'difficulty':level,'records':len(records),'checkbox_records':count,'passed':True,'executed_without_repository_pythonpath':True}
if __name__=='__main__':
 updates=json.loads((HERE/'package-updates.json').read_text());reports=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:
  for f in concurrent.futures.as_completed([ex.submit(run,u)for u in updates]):reports.append(f.result())
 assert len(reports)==8 and all(r['passed']for r in reports);save('delivery-verification.json',{'passed':True,'packages':reports,'records':sum(r['records']for r in reports)})
 v=json.loads((HERE/'verification.json').read_text());v['published_package_execution_verified']=True;v['published_packages_executed']=len(reports);v['published_execution_records']=sum(r['records']for r in reports);save('verification.json',v)
 print(json.dumps({'passed':True,'published_packages':len(reports),'records':sum(r['records']for r in reports)}))
