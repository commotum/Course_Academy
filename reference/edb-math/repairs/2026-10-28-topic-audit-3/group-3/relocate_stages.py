import collections,concurrent.futures,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;A=json.loads((H/'generator-stage-plan.json').read_text());A=[{**g,'script':str((Path(g['directory'])/g['entrypoint']).resolve()),'legacy_repository_relative':False}for g in A];V=json.loads((H/'generator-validation.json').read_text());work=Path(tempfile.mkdtemp(prefix='ca-9837-g3-'));report=[];samples=[]
def identities(o):
 out=[]
 if isinstance(o,dict):
  for k,v in o.items():
   if k in[':question/id',':answer-field/id',':answer/id']:out.append((k,v))
   else:out+=identities(v)
 elif isinstance(o,list):
  for v in o:out+=identities(v)
 return sorted(out)
def asset_refs(q):
 out=set()
 for attr in[':question/problem',':question/worked-solution']:out.update(re.findall(r'!\[[^]]*\]\(([^)]+)\)',q.get(attr,'')))
 for f in q.get(':question/answer-fields',[]):
  for a in f.get(':answer-field/choices',[]):
   typ=a[':answer/type'];typ=typ.get(':db/ident')if isinstance(typ,dict)else typ
   if typ==':answer.type/image':out.add(a[':answer/value'])
 return sorted(out)
def clone(g,dest):
 source=Path(g['script']);shutil.copytree(source.parent,dest,ignore=shutil.ignore_patterns('__pycache__'));return dest/source.name

def run(g):
 kp=g['kp'];bands=sorted({r['level']for r in V if r['kp']==kp and r.get('exit')==0 and r['level']in['easy','moderate','hard']});row={'kp':kp,'source':g['script'],'supported_successful_bands':bands,'outside_repo':True};records=[]
 if not bands:row['error']='No successful baseline band';return row,[]
 band='easy'if'easy'in bands else bands[0];row['smoke_band']=band
 try:
  for variant in['a','b']:
   package=work/str(kp)/variant/'package';entry=clone(g,package);output=work/str(kp)/variant/'generated-assets';output.mkdir(parents=True);env={k:v for k,v in os.environ.items()if k not in['PYTHONPATH','_CA_SOURCE_POLICY_CHILD']};env.update(PYTHONDONTWRITEBYTECODE='1',COURSE_ACADEMY_GENERATOR_OUTPUT_DIR=str(output),MPLCONFIGDIR=str(work/'mpl-cache'/str(kp)))
   p=subprocess.run([sys.executable,str(entry),'--difficulty',band,'--count','1','--seed','983731','--format','json'],cwd='/tmp',env=env,capture_output=True,text=True,timeout=90)
   if p.returncode:row['error']=p.stderr[-1600:];row['failed_variant']=variant;return row,[]
   data=json.loads(p.stdout);data=data.get('instances',data)if isinstance(data,dict)else data;r=data[0]if isinstance(data,list)else data;records.append(r)
  q1,q2=[r['question']for r in records];refs=[asset_refs(q)for q in[q1,q2]];hashes=[];generateddirs=[]
  for branch,paths in zip(['a','b'],refs):
   hs=[];honored=True
   for ref in paths:
    p=Path(ref);p=p if p.is_absolute()else Path('/media/jake/SSD/EDB/math')/ref
    if p.exists():hs.append(hashlib.sha256(p.read_bytes()).hexdigest())
    else:hs.append('MISSING:'+ref)
    if p.is_absolute()and work in p.parents and work/str(kp)/branch/'generated-assets'not in p.parents:honored=False
   hashes.append(sorted(hs));generateddirs.append(honored)
  row.update(identities_stable=identities(q1)==identities(q2),asset_bytes_stable=hashes[0]==hashes[1],asset_hashes=hashes[0],output_dir_honored=all(generateddirs),generated_asset_refs=refs,passed=identities(q1)==identities(q2)and hashes[0]==hashes[1]and all(generateddirs));return row,[{'kp':kp,'level':band,'record':records[0],'kind':'outside-repo-relocation'}]
 except Exception as ex:row['error']=str(ex);return row,[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 futures=[pool.submit(run,g)for g in A]
 for f in concurrent.futures.as_completed(futures):
  row,rs=f.result();report.append(row);samples+=rs;(H/'staged-relocation-validation.json').write_text(json.dumps({'work_directory':str(work),'packages':report},indent=2));(H/'staged-relocation-samples.json').write_text(json.dumps(samples,indent=2));print(row['kp'],row.get('passed',False),row.get('error','')[-140:],flush=True)
print('relocation',len(report),'passes',sum(r.get('passed',False)for r in report))
