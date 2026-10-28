import hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;G=json.loads((H/'generator-audit.json').read_text());stages={r['kp']:r for r in json.loads((H/'generator-candidates.json').read_text())};out=[];samples=[]
def identity(o):
 vals=[]
 if isinstance(o,dict):
  for k,v in o.items():
   if k in [':question/id',':answer-field/id',':answer/id']:vals.append((k,v))
   else:vals+=identity(v)
 elif isinstance(o,list):
  for v in o:vals+=identity(v)
 return sorted(vals)
def assets(q):
 paths=set(re.findall(r'!\[[^]]*\]\(([^)]+)\)',json.dumps(q)))
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:
   if a[':answer/type']==':answer.type/image':paths.add(a[':answer/value'])
 return sorted(paths)
for kp in [17592186096698,17592186087839,17592186087840,*sorted(set(stages)-{17592186087839})]:
 source=Path(stages[kp]['directory'])/stages[kp]['entrypoint']if kp in stages else Path(next(g['script']for g in G if g['kp']==kp));dest=H/'relocation-packages'/str(kp);shutil.copytree(source.parent,dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'));root=H/'relocation-assets'/str(kp);records=[]
 for branch,entry in [('a',source),('b',dest/source.name)]:
  target=root/branch;target.mkdir(parents=True,exist_ok=True);env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(target.resolve()),'MPLCONFIGDIR':str((H/'mpl-cache').resolve())};p=subprocess.run([sys.executable,str(entry),'--difficulty','easy','--count','1','--seed','912233','--format','json'],capture_output=True,text=True,check=True,env=env);records.append(json.loads(p.stdout)[0])
 qa,qb=[r['question']for r in records];pa,pb=assets(qa),assets(qb);ha=[hashlib.sha256(Path(v).read_bytes()).hexdigest()for v in pa];hb=[hashlib.sha256(Path(v).read_bytes()).hexdigest()for v in pb];assert identity(qa)==identity(qb),(kp,'location-dependent identities');assert sorted(ha)==sorted(hb),(kp,'location-dependent image bytes');assert all(str((root/'a').resolve())in v for v in pa)and all(str((root/'b').resolve())in v for v in pb)
 # Simulate normal publication's content-addressed image import, preserving all entity/answer IDs.
 published=H/'published-assets';published.mkdir(exist_ok=True);text=json.dumps(qa)
 for p,digest in zip(pa,ha):
  path=published/(digest+Path(p).suffix);shutil.copyfile(p,path);text=text.replace(p,'images/'+digest[:2]+'/'+digest+Path(p).suffix)
 normalized=json.loads(text);assert identity(normalized)==identity(qa);out.append({'kp':kp,'passed':True,'normal_output_dir_honored':True,'relocated_package_and_output_dir_identities_equal':True,'asset_bytes_equal':True,'asset_count':len(pa),'asset_hashes':ha,'publication_path_rewrite_preserves_all_ids':True});samples.append({'kp':kp,'level':'easy','record':records[0],'kind':'staged-successor'if kp in stages else'graph-relocation-check'})
 print(kp,'stable',len(pa),'assets',flush=True)
(H/'generator-relocation-validation.json').write_text(json.dumps(out,indent=2));(H/'relocation-samples.json').write_text(json.dumps(samples,indent=2))
