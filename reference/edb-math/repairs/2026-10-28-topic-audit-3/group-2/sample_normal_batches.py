import concurrent.futures,json,os,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;T=Path('/tmp/course-academy-audit3-group2-count12');T.mkdir(exist_ok=True);D=json.loads((H/'generator-candidates.json').read_text())
def worker(d):
 base=T/str(d['kp']);runtime=base/'runtime';runtime.mkdir(parents=True,exist_ok=True)
 for name in d['files']:
  p=runtime/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(d['directory'])/name,p)
 report=[];samples=[]
 for band in d['supported_difficulties']:
  output=base/('assets-'+band);output.mkdir(exist_ok=True);env={k:v for k,v in os.environ.items()if k not in['PYTHONPATH','COURSE_ACADEMY_REPO_ROOT']};env.update({'MPLBACKEND':'Agg','PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output)});args=[sys.executable,'-B',str(runtime/d['entrypoint']),'--difficulty',band,'--count','12','--seed','10028','--format','json']
  try:
   p=subprocess.run(args,cwd=base,capture_output=True,text=True,env=env,timeout=240);(base/(band+'.stderr')).write_text(p.stderr)
   if p.returncode:raise ValueError(p.stderr[-2500:])
   data=json.loads(p.stdout);data=data if isinstance(data,list)else[data];assert len(data)==12;report.append({'band':band,'passed':True,'count':12,'templates':sorted({r.get('generation',{}).get('template','')for r in data})})
   samples.extend({'kp':d['kp'],'band':band,'record':r,'kind':'normal-count12-batch','runtime':str(runtime),'output':str(output)}for r in data)
  except Exception as e:report.append({'band':band,'passed':False,'error':str(e)})
 return samples,{'kp':d['kp'],'bands':report}
S=[];V=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:
 for ss,v in pool.map(worker,D):
  S.extend(ss);V.append(v);(H/'generator-count12-samples.json').write_text(json.dumps(S,indent=2)+'\n');(H/'generator-count12-invocations.json').write_text(json.dumps(V,indent=2)+'\n');print(v['kp'],[(b['band'],b['passed'])for b in v['bands']],flush=True)
