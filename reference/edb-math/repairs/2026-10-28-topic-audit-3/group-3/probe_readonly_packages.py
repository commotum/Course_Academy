import concurrent.futures,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;rows=json.loads((H/'generator-candidates.json').read_text())+json.loads((H/'generator-followup-candidates.json').read_text());fix=json.loads((H/'readonly-renderer-stage-plan.json').read_text());rows=[fix if r['kp']==fix['kp']else r for r in rows];rows.sort(key=lambda r:r['kp']!=fix['kp']);work=Path(tempfile.mkdtemp(prefix='ca9837-readonly-'));reports=[];samples=[]
def run(row,band,branch='a'):
 base=work/str(row['kp'])/band/branch;package=base/'package';package.mkdir(parents=True);source=Path(row['directory'])
 for name in row['files']:
  dest=package/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/name,dest);dest.chmod(0o444)
 for d in sorted([package,*[p for p in package.rglob('*')if p.is_dir()]],key=lambda p:len(p.parts),reverse=True):d.chmod(0o555)
 output=base/'generated-assets';output.mkdir();env={k:v for k,v in os.environ.items()if k not in['PYTHONPATH','_CA_SOURCE_POLICY_CHILD']};env.update(PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(output),MPLCONFIGDIR=str(output/'mpl-cache'));writable=os.access(package,os.W_OK);r={'kp':row['kp'],'band':band,'branch':branch,'package':str(package),'directory_mode':'0555','file_mode':'0444','package_write_access':writable,'outside_repository':True,'output_directory':str(output)}
 try:
  assert not writable,'Test user can write supposedly immutable package'
  p=subprocess.run([sys.executable,str(package/row['entrypoint']),'--difficulty',band,'--count','1','--seed','983731','--format','json'],cwd='/tmp',env=env,capture_output=True,text=True,timeout=100);r.update(exit=p.returncode,stderr=p.stderr[-1800:],passed=p.returncode==0)
  if p.returncode:return r,[]
  data=json.loads(p.stdout);data=data.get('instances',data)if isinstance(data,dict)else data;rec=data[0];refs=set(re.findall(r'!\[[^]]*\]\(([^)]+)\)',json.dumps(rec)))
  for f in rec['question'].get(':question/answer-fields',[]):
   for a in f[':answer-field/choices']:
    if a[':answer/type']==':answer.type/image':refs.add(a[':answer/value'])
  hashes={str(ref):hashlib.sha256(Path(ref).read_bytes()).hexdigest()for ref in refs if Path(ref).is_absolute()and Path(ref).exists()};r.update(asset_hashes=sorted(hashes.values()),provenance_files=[str(p.relative_to(output))for p in output.rglob('*provenance*.json')],package_files_unchanged=all((package/name).read_bytes()==(source/name).read_bytes()for name in row['files']));assert r['package_files_unchanged'];return r,[{'kp':row['kp'],'level':band,'branch':branch,'record':rec}]
 except Exception as ex:r.update(error=str(ex),passed=False);return r,[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 jobs=[pool.submit(run,row,band,branch)for row in rows for band in row['supported_difficulties']for branch in(['a','b']if row['kp']==fix['kp']else['a'])]
 for f in concurrent.futures.as_completed(jobs):
  r,rs=f.result();reports.append(r);samples+=rs;(H/'readonly-package-probes.json').write_text(json.dumps(reports,indent=2));(H/'readonly-package-samples.json').write_text(json.dumps(samples,indent=2));print(r['kp'],r['band'],r['branch'],r['passed'],r.get('error',r.get('stderr',''))[-150:],flush=True)
print('readonlyprobes',len(reports),'passed',sum(r['passed']for r in reports))
