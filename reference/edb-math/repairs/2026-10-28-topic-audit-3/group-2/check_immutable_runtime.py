"""Read-only installed-package regression: actual0444/0555 runtime, writable callers."""
import concurrent.futures,hashlib,json,os,shutil,stat,subprocess,sys,tempfile,time
from pathlib import Path
H=Path(__file__).resolve().parent;AUDIT=H.parent;OUT=H/'immutable-runtime-check';OUT.mkdir(exist_ok=True);D=json.loads((H/'generator-candidates.json').read_text());needed={d['kp']for d in D};pubs={}
for batch in json.loads((AUDIT/'publication-batches.json').read_text()):
 p=AUDIT/batch/'generator-publications.json'
 if p.exists():
  for r in json.loads(p.read_text()):
   if r['kp']in needed:pubs[r['kp']]=r
assert len(pubs)==len(D)==22 and os.geteuid()==1000
BASE=Path(tempfile.mkdtemp(prefix='course-academy-g2-readonly-'));(OUT/'runtime-root.txt').write_text(str(BASE)+'\n')
def state(root):
 out={}
 for p in[root,*sorted(root.rglob('*'))]:
  st=p.stat();out[str(p.relative_to(root))]={'mode':stat.S_IMODE(st.st_mode),'inode':st.st_ino,'mtime_ns':st.st_mtime_ns,'ctime_ns':st.st_ctime_ns,'bytes':st.st_size if p.is_file()else None,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()if p.is_file()else None,'symlink':p.is_symlink()}
 return out

def worker(d):
 kp=d['kp'];pub=pubs[kp];assert pub['digest']==d['approved_digest'],kp;actual=Path('/media/jake/SSD/EDB/math')/Path(pub['new_reference']).parent;before=state(actual);assert all(v['mode']&0o222==0 for v in before.values()),('Writable installed files/dirs',kp,[k for k,v in before.items()if v['mode']&0o222]);assert not any(v['symlink']for v in before.values()),('Installed symlink',kp)
 base=BASE/str(kp);base.mkdir();copy=base/'copy-canary';shutil.copytree(actual,copy)
 for p in copy.rglob('*'):
  if p.is_file():p.chmod(0o444)
 for p in sorted([p for p in copy.rglob('*')if p.is_dir()],key=lambda p:len(p.parts),reverse=True):p.chmod(0o555)
 copy.chmod(0o555);canary=[]
 for label,p,action in [('rewrite-existing-file',copy/d['entrypoint'],lambda p:p.write_bytes(p.read_bytes())),('create-runtime-file',copy/'__read_only_canary__',lambda p:p.write_text('test')),('create-runtime-directory',copy/'__read_only_dir_canary__',lambda p:p.mkdir())]:
  try:action(p);canary.append({'operation':label,'denied':False})
  except PermissionError as e:canary.append({'operation':label,'denied':True,'errno':e.errno})
 assert all(c['denied']for c in canary),(kp,canary)
 cases=[]
 for index,band in enumerate(d['supported_difficulties']):
  caller=base/('caller-'+band);caller.mkdir();output=caller/'generated';output.mkdir();tmp=caller/'tmp';tmp.mkdir();env={k:v for k,v in os.environ.items()if k not in['PYTHONPATH','COURSE_ACADEMY_REPO_ROOT','PYTHONDONTWRITEBYTECODE']};env.update({'MPLBACKEND':'Agg','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output),'TMPDIR':str(tmp)});args=[sys.executable,str(actual/d['entrypoint']),'--difficulty',band,'--count','3','--seed',str(10028671+index),'--format','json'];started=time.monotonic()
  p=subprocess.run(args,cwd=caller,env=env,capture_output=True,text=True,timeout=180);(OUT/(str(kp)+'-'+band+'.stderr')).write_text(p.stderr);(OUT/(str(kp)+'-'+band+'.stdout')).write_text(p.stdout)
  record={'band':band,'exit_code':p.returncode,'seconds':round(time.monotonic()-started,3),'command':args,'cwd':str(caller),'output_dir':str(output),'tmpdir':str(tmp),'python_bytecode_writes_not_disabled':True}
  if p.returncode:record.update(passed=False,error=p.stderr[-6000:])
  else:
   try:
    rows=json.loads(p.stdout);rows=rows if isinstance(rows,list)else[rows];assert len(rows)==3 and all(isinstance(r.get('question'),dict)for r in rows);record.update(passed=True,records=len(rows),output_files=[str(f.relative_to(caller))for f in caller.rglob('*')if f.is_file()])
   except Exception as e:record.update(passed=False,error=repr(e))
  cases.append(record)
 after=state(actual);unchanged=before==after;differences=[{'path':k,'before':before.get(k),'after':after.get(k)}for k in sorted(set(before)|set(after))if before.get(k)!=after.get(k)];report={'kp':kp,'installed_reference':pub['new_reference'],'approved_digest':d['approved_digest'],'effective_uid':os.geteuid(),'installed_all_files_and_dirs_nonwritable':True,'installed_file_count':sum(v['sha256']is not None for v in before.values()),'read_only_copy_canaries':canary,'all_declared_bands_executed':[c['band']for c in cases],'cases':cases,'installed_tree_metadata_and_content_unchanged':unchanged,'installed_tree_differences':differences,'passed':unchanged and all(c['passed']for c in cases)};(OUT/(str(kp)+'.json')).write_text(json.dumps(report,indent=2)+'\n');return report
reports=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:
 futures=[pool.submit(worker,d)for d in D]
 for f in concurrent.futures.as_completed(futures):
  try:r=f.result()
  except Exception as e:r={'passed':False,'worker_error':repr(e)}
  reports.append(r);print('package',r.get('kp'),'passed',r['passed'],'bands',[(c['band'],c['passed'])for c in r.get('cases',[])],flush=True);(OUT/'progress.json').write_text(json.dumps({'completed':len(reports),'packages':22,'failures':[r for r in reports if not r['passed']]},indent=2)+'\n')
result={'passed':len(reports)==22 and all(r['passed']for r in reports),'packages':len(reports),'declared_band_runs':sum(len(r.get('cases',[]))for r in reports),'successful_records':sum(c.get('records',0)for r in reports for c in r.get('cases',[])if c.get('passed')),'effective_uid':os.geteuid(),'runtime_root':str(BASE),'method':'Actual installed registered package paths executed with every package file and directory already nonwritable (0444/0555); copied packages independently chmod0444/0555 prove same-text rewrite/new-file/new-directory denial. Fresh writable caller output/TMPDIR; ordinary Python, no -B or PYTHONDONTWRITEBYTECODE. Check inode,mtime,ctime,permissions and hash/tree membership before/after, not hashes alone.','failures':[r for r in reports if not r['passed']],'reports':reports,'frozen_descriptors_sha256':hashlib.sha256((H/'generator-candidates.json').read_bytes()).hexdigest(),'database_writes':0,'source_package_mutations_requested':0};(OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print('FINAL',json.dumps({k:result[k]for k in['passed','packages','declared_band_runs','successful_records','failures']})[:6000],flush=True)
