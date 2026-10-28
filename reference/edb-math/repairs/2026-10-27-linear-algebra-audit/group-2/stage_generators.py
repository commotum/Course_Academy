import json,re,sys,shutil,hashlib,collections
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];D=json.loads((H/'current.json').read_text());props=json.loads((H/'proposals.json').read_text());byentity=collections.defaultdict(list);uuidmap={}
for p in props:byentity[p['entity']].append(p)
for q in D['questions']:
 uuidmap[q[':question/id']]=q[':db/id']
 for f in q.get(':question/answer-fields',[]):
  uuidmap[f[':answer-field/id']]=f[':db/id']
  for a in f.get(':answer-field/choices',[]):uuidmap[a[':answer/id']]=a[':db/id']
staged=[]
for g in json.loads((H/'generators.json').read_text()):
 original=Path(g['path']).parent;dest=H/'staged-generators'/str(g['kp']);
 if dest.exists():
  dest.chmod(0o755)
  for f in dest.rglob('*'):
   f.chmod(0o755 if f.is_dir()else 0o644)
  shutil.rmtree(dest)
 shutil.copytree(original,dest,dirs_exist_ok=True);edits=[];unmatched=[]
 dest.chmod(0o755)
 for f in dest.rglob('*'):
  if f.is_file():f.chmod(0o644)
  elif f.is_dir():f.chmod(0o755)
 def visit(x):
  if isinstance(x,list):
   for y in x:visit(y)
  elif isinstance(x,dict):
   eid=x.get(':db/id')or next((uuidmap[x[k]]for k in [':question/id',':answer-field/id',':answer/id']if k in x and x[k]in uuidmap),None)
   for p in byentity.get(eid,[]):
    a=':'+p['attribute']
    if a not in x:continue
    if x[a]==p['before']:x[a]=p['after'];edits.append({'entity':eid,'attribute':p['attribute'],'reason':p['reason']})
    elif x[a]!=p['after']:unmatched.append({'entity':eid,'attribute':p['attribute'],'reason':'source snapshot differs; retained snapshot'})
   for y in x.values():visit(y)
 for path in dest.rglob('*.json'):
  if path.name=='generator-package.json':continue
  try:data=json.loads(path.read_text())
  except Exception:continue
  before=len(edits);visit(data)
  if len(edits)>before:path.write_text(json.dumps(data,indent=2)+'\n')
 helper=dest/'math_format.py';helper_changed=False
 if helper.exists():
  new=(R/'scripts/question_capture/math_format.py').read_text()
  helper_changed=helper.read_text()!=new;helper.write_text(new)
 if not edits and not helper_changed:shutil.rmtree(dest);continue

 if g['kp']==17592186119808:
  import importlib.util
  spec=importlib.util.spec_from_file_location('span_patch',H/'patch_span_generator.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.patch(dest/Path(g['path']).name)
 manifest=json.loads((dest/'generator-package.json').read_text());manifest['files']={str(p.relative_to(dest)):{'bytes':p.stat().st_size,'executable':bool(p.stat().st_mode&0o111),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in dest.rglob('*')if p.is_file()and p.name!='generator-package.json'and '__pycache__'not in str(p)};(dest/'generator-package.json').write_text(json.dumps(manifest,indent=2)+'\n')
 staged.append({**g,'staged':str(dest.resolve()),'helper_updated':helper_changed,'source_field_edits':edits,'source_mismatches_retained':unmatched,'publication':'not published or registered'})
(H/'staged-generators.json').write_text(json.dumps(staged,indent=2)+'\n');print('staged',len(staged),'source field edits',sum(len(s['source_field_edits'])for s in staged))
