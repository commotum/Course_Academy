import ast,collections,concurrent.futures,hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];G=[dict(x,path=str(Path(x['directory'])/x['entrypoint']))for x in json.loads((H/'generator-candidates.json').read_text())];T=Path('/tmp/course-academy-audit3-group2-successors');T.mkdir(exist_ok=True)
def digest_assets(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()for p in root.rglob('*')if p.is_file()and p.suffix.lower()in ['.png','.svg','.webp','.jpg']}
def worker(g):
 base=T/str(g['kp']);base.mkdir(exist_ok=True);reports=[];samples=[];old=Path(g['path']);legacy='generate/scratch'in str(old);runtime=base/'runtime';runtime.mkdir(exist_ok=True);dest=runtime/'generate/scratch'if legacy else runtime;dest.mkdir(parents=True,exist_ok=True)
 for name in g['files']:
  if name=='generator-package.json':continue
  p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.parent/name,p)
 if legacy:
  # Historical scripts depend on repository-relative shared modules. Reproduce
  # that declared layout in a private external tree; do not rely on repo cwd.
  for name in ['ca_source_policy.py','math_format.py']:
   source=old.parent/name
   if not source.exists():source=R/'scripts/question_capture'/name
   if source.exists():shutil.copyfile(source,dest/name)
  sd=runtime/'scripts/question_capture';sd.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/'scripts/question_capture/math_format.py',sd/'math_format.py')
 entry=dest/old.name;help_run=subprocess.run([sys.executable,'-B',str(entry),'--help'],cwd=base,capture_output=True,text=True,timeout=60);(base/'help.txt').write_text(help_run.stdout+help_run.stderr)
 choices={}
 for option in ['template','profile']:
  m=re.search('--'+option+r'\s+\{([^}]+)\}',help_run.stdout)
  if m:choices[option]=m[1].split(',')
 for band in ['easy','moderate','hard']:
  # Separate assets from immutable runtime and repeat exact same invocation with
  # another output directory, checking IDs and the full generated asset bytes.
  outs=[]
  for move in ['a','b']:
   output=base/('assets-'+band+'-'+move);output.mkdir(exist_ok=True);args=[sys.executable,'-B',str(entry),'--difficulty',band,'--count','3','--seed','9837','--format','json']
   env={k:v for k,v in os.environ.items()if k not in ('PYTHONPATH','COURSE_ACADEMY_REPO_ROOT')};env.update({'MPLBACKEND':'Agg','PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output)})
   try:
    p=subprocess.run(args,cwd=base,capture_output=True,text=True,env=env,timeout=180);(base/f'{band}-{move}.stderr').write_text(p.stderr)
    if p.returncode:raise ValueError(p.stderr[-1800:])
    data=json.loads(p.stdout);data=data if isinstance(data,list)else[data];(base/f'{band}-{move}.json').write_text(json.dumps(data,indent=2)+'\n');outs.append((data,output))
   except Exception as e:reports.append({'band':band,'passed':False,'error':str(e)});break
  if len(outs)!=2:continue
  def identities(rs):
   return [[v['question'].get(':question/id'),[[f.get(':answer-field/id'),[a.get(':answer/id')for a in f.get(':answer-field/choices',[])]]for f in v['question'].get(':question/answer-fields',[])]]for v in rs]
  reports.append({'band':band,'passed':True,'records':len(outs[0][0]),'all_ids_equal':identities(outs[0][0])==identities(outs[1][0]),'asset_bytes_equal':digest_assets(outs[0][1])==digest_assets(outs[1][1]),'asset_files':len(digest_assets(outs[0][1])),'runtime_asset_files':[str(p.relative_to(runtime))for p in runtime.rglob('*')if p.suffix.lower()in ['.png','.svg']and'/reference/'not in str(p)]})
  for rec in outs[0][0]:samples.append({'kp':g['kp'],'band':band,'record':rec,'kind':'external-normal-environment','runtime':str(dest),'output':str(outs[0][1])})
 return samples,{'kp':g['kp'],'path':g['path'],'choices':choices,'bands':reports,'external_root':str(base),'legacy_private_repository_layout':legacy}
S=[];report=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=6)as pool:
 for ss,r in pool.map(worker,G):
  S.extend(ss);report.append(r);print(r['kp'],[(x['band'],x['passed'],x.get('all_ids_equal'),x.get('asset_bytes_equal'))for x in r['bands']],flush=True);(H/'successor-samples.json').write_text(json.dumps(S,indent=2)+'\n');(H/'successor-relocation.json').write_text(json.dumps(report,indent=2)+'\n')
