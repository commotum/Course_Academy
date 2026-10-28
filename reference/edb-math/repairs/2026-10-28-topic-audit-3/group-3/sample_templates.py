import concurrent.futures,json,os,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generator-audit.json').read_text());S={g['kp']:g for g in json.loads((H/'generator-stage-plan.json').read_text())};V=json.loads((H/'generator-validation.json').read_text());W=Path(json.loads((H/'relocation-validation.json').read_text())['work_directory']);work=Path(tempfile.mkdtemp(prefix='ca9837-templates-'));out=H/'template-results';out.mkdir(exist_ok=True);reports=[];samples=[]
def run(g):
 kp=g['kp'];row={'kp':kp};src=(Path(S[kp]['directory'])/S[kp]['entrypoint']).resolve()if kp in S else W/str(kp)/'a/package'/Path(g['script']).name;bands=sorted({r['level']for r in V if r['kp']==kp and r.get('exit')==0 and r['level']in['easy','moderate','hard']});output=work/str(kp);output.mkdir();env={k:v for k,v in os.environ.items()if k not in['PYTHONPATH','_CA_SOURCE_POLICY_CHILD']};env.update(PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(output),MPLCONFIGDIR=str(work/'mpl'/str(kp)));path=out/(str(kp)+'.json')
 try:
  p=subprocess.run([sys.executable,str(H/'template_worker.py'),str(src),str(path),json.dumps(bands)],cwd='/tmp',env=env,capture_output=True,text=True,timeout=200);row.update(exit=p.returncode,stdout=p.stdout[-300:],stderr=p.stderr[-1200:]);data=json.loads(path.read_text())if path.exists()else{};ss=[{'kp':kp,**s}for s in data.get('samples',[])];row['samples']=len(ss);return row,ss
 except Exception as ex:row['error']=str(ex);return row,[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 for f in concurrent.futures.as_completed([pool.submit(run,g)for g in G]):
  r,rs=f.result();reports.append(r);samples+=rs;(H/'template-validation.json').write_text(json.dumps(reports,indent=2));(H/'template-samples.json').write_text(json.dumps(samples,indent=2));print(r['kp'],r.get('exit'),r.get('samples'),r.get('error','')[-120:],flush=True)
