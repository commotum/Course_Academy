import concurrent.futures,hashlib,json,os,re,shutil,subprocess,tempfile
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];cfg=json.loads((H/'generator-stage-config.json').read_text());before=json.loads((H/'generator-stage-samples.json').read_text());reports=json.loads((H/'generator-stage-test.json').read_text());outside=Path(tempfile.mkdtemp(prefix='ca-topic3-g1-identity-'));env=dict(os.environ);env.pop('PYTHONPATH',None);env.pop('_CA_SOURCE_POLICY_CHILD',None);env['PYTHONDONTWRITEBYTECODE']='1'
def canonical(value):
 if isinstance(value,dict):return {k:canonical(v)for k,v in value.items()}
 if isinstance(value,list):return [canonical(v)for v in value]
 if not isinstance(value,str):return value
 def image(m):
  p=Path(m[1]);p=p if p.is_file()else Path('/media/jake/SSD/EDB/math')/m[1]
  assert p.is_file(),str(p)
  return m[0][:m[0].rfind('](')+2]+'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()+')'
 return re.sub(r'!\[[^\]]*\]\(([^)]+)\)',image,value)
def run(c):
 root=outside/'different-ancestor'/'package'/str(c['kp']);root.mkdir(parents=True)
 for name in c['files']:p=root/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(c['directory'])/name,p)
 initial={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()for p in root.rglob('*')if p.is_file()};out=[]
 for band in[r['band']for r in reports if r['kp']==c['kp']]:
  output=outside/'entirely-different-output-root'/str(c['kp'])/band
  r=subprocess.run([str(R/'.venv/bin/python'),str(root/c['entrypoint']),'--difficulty',band,'--count','3','--seed','28109837','--format','json'],cwd=outside,env={**env,'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(output)},text=True,capture_output=True,timeout=120)
  if r.returncode:out.append({'kp':c['kp'],'band':band,'passed':False,'stderr':r.stderr});continue
  data=json.loads(r.stdout);rows=data.get('records',data.get('instances',[]))if isinstance(data,dict)else data;old=[v for v in before if v.get('knowledge_point',{}).get('db_id')==c['kp']and v['question'].get(':question/difficulty')==':question.difficulty/'+band];assert len(old)==len(rows)==3
  oldq=[canonical(v['question'])for v in old];newq=[canonical(v['question'])for v in rows];out.append({'kp':c['kp'],'band':band,'passed':oldq==newq,'records':3,'all_question_field_answer_ids_and_content_asset_hashes_equal':oldq==newq,'old_ids':[v[':question/id']for v in oldq],'new_ids':[v[':question/id']for v in newq],'package_location':str(root),'output_dir':str(output)})
 final={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()for p in root.rglob('*')if p.is_file()};unchanged=initial==final
 return {'kp':c['kp'],'package_files_unchanged':unchanged,'unexpected_files':sorted(set(final)-set(initial)),'changed_declared_files':[p for p in initial if initial[p]!=final.get(p)],'bands':out}
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
 for result in pool.map(run,cfg):results.append(result);(H/'generator-relocation-proof.json').write_text(json.dumps(results,indent=2)+'\n');print(result['kp'],result['package_files_unchanged'],[(r['band'],r['passed'])for r in result['bands']],result['unexpected_files'],flush=True)
