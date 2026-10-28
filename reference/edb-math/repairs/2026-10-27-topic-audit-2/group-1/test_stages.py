import concurrent.futures,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import validate_generated_record
C=json.loads((H/'format-generator-stage-config.json').read_text());c=json.loads((H/'generator-stage-config.json').read_text());C.append(dict(kp=17592186172038,directory=c['directory'],entrypoint=c['old_manifest']['entrypoint']))
reports=[];samples=[];prior=json.loads((H/'generator-sample-report.json').read_text());support={(r['kp'],r['difficulty'])for r in prior if r['returncode']==0};support.add((17592186172038,'hard'))
def run(task):
 c,band=task;dst=Path(c['directory']);assets=H/'staged-assets'/str(c['kp'])/band;assets.mkdir(parents=True,exist_ok=True);args=[str(R/'.venv/bin/python'),str(dst/c['entrypoint']),'--difficulty',band,'--count','4','--seed','27102026','--format','json'];r=subprocess.run(args,capture_output=True,text=True,timeout=120,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets)});rs=json.loads(r.stdout)if r.returncode==0 else[];rs=rs.get('records',[])if isinstance(rs,dict)else rs;errors=[]
 for record in rs:
  try:validate_generated_record(record)
  except Exception as ex:errors.append({'identity':record['question'].get(':question/id'),'error':str(ex)})
 return {'kp':c['kp'],'difficulty':band,'returncode':r.returncode,'stderr':r.stderr,'records':len(rs),'validation_errors':errors},rs
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for report,rs in pool.map(run,[(c,b)for c in C for b in['easy','moderate','hard']if(c['kp'],b)in support]):reports.append(report);samples.extend(rs);print(report,flush=True)
(H/'staged-sample-report.json').write_text(json.dumps(reports,indent=2));(H/'staged-samples.json').write_text(json.dumps(samples,indent=2));print('stagedrecords',len(samples))
