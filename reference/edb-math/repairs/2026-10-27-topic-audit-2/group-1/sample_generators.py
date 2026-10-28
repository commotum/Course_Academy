import concurrent.futures,json,os,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];D=json.loads((H/'current.json').read_text());out=[];records=[]
def run(task):
 kp,g,band=task;p=Path('/media/jake/SSD/EDB/math')/g[':question-generator/script'];p=p if p.exists()else R/g[':question-generator/script'];asset_dir=H/'generated-assets'/str(kp)/band;asset_dir.mkdir(parents=True,exist_ok=True);env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(asset_dir)};args=[str(R/'.venv/bin/python'),str(p),'--difficulty',band,'--count','4','--seed','27102026','--format','json']
 try:r=subprocess.run(args,text=True,capture_output=True,timeout=80,env=env);data=json.loads(r.stdout)if r.returncode==0 else None;rs=data.get('records',[])if isinstance(data,dict)else data or[];return {'kp':kp,'generator':g[':db/id'],'difficulty':band,'returncode':r.returncode,'stderr':r.stderr,'records':len(rs)},rs
 except Exception as e:return {'kp':kp,'generator':g[':db/id'],'difficulty':band,'error':str(e)},[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 for report,rs in pool.map(run,[(kp,g,b)for kp,g in D['generators']for b in ['easy','moderate','hard']]):
  out.append(report);records.extend(rs);print(report['kp'],report['difficulty'],report.get('records'),report.get('stderr','')[:100],report.get('error',''),flush=True)
(H/'generator-sample-report.json').write_text(json.dumps(out,indent=2));(H/'generator-samples.json').write_text(json.dumps(records,indent=2));print('total records',len(records))
