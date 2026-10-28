import concurrent.futures,json,os,subprocess,sys,tempfile
from pathlib import Path
sys.path.insert(0,'scripts');from question_capture.math_format import validate_generated_record
H=Path(__file__).resolve().parent;A=json.loads((H/'generator-stage-plan.json').read_text());V=json.loads((H/'generator-validation.json').read_text());reports=[];samples=[];work=Path(tempfile.mkdtemp(prefix='ca9837-stage-'))
def run(g,level):
 env={k:v for k,v in os.environ.items()if k not in['PYTHONPATH','_CA_SOURCE_POLICY_CHILD']};output=work/str(g['kp'])/level;output.mkdir(parents=True);env.update(PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(output),MPLCONFIGDIR=str(work/'mpl'/str(g['kp'])));row={'kp':g['kp'],'level':level};recs=[]
 try:
  p=subprocess.run([sys.executable,str((Path(g['directory'])/g['entrypoint']).resolve()),'--difficulty',level,'--count','2','--seed','983779','--format','json'],cwd='/tmp',env=env,capture_output=True,text=True,timeout=100);row.update(exit=p.returncode,stderr=p.stderr[-1600:]);data=json.loads(p.stdout)if p.returncode==0 else[];data=data.get('instances',data)if isinstance(data,dict)else data
  for r in data:
   try:validate_generated_record(r)
   except Exception as ex:row.setdefault('format_errors',[]).append(str(ex))
   recs.append({'kp':g['kp'],'level':level,'record':r})
  row['records']=len(recs)
 except Exception as ex:row['error']=str(ex)
 return row,recs
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 jobs=[pool.submit(run,g,l)for g in A for l in sorted({r['level']for r in V if r['kp']==g['kp']and r.get('exit')==0})]
 for f in concurrent.futures.as_completed(jobs):
  r,rs=f.result();reports.append(r);samples+=rs;print(r['kp'],r['level'],r.get('exit'),r.get('records'),r.get('format_errors',r.get('error',r.get('stderr','')))[-200:],flush=True);(H/'staged-validation.json').write_text(json.dumps(reports,indent=2));(H/'staged-samples.json').write_text(json.dumps(samples,indent=2))
