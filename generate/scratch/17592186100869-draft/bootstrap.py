import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,shutil,importlib.util,difflib
D=Path(__file__).resolve().parent;R=D.parents[2]
manifest=json.loads((R/'generate/runs/current/manifest.json').read_text()); row=next(r for r in manifest['items'] if r['kp_id']==17592186100869) if 'items' in manifest else None
if row is None:
 def find(x):
  if isinstance(x,dict):
   if x.get('kp_id')==17592186100869:return x
   for v in x.values():
    if (z:=find(v)):return z
  elif isinstance(x,list):
   for v in x:
    if (z:=find(v)):return z
 row=find(manifest)
(D/'reference/registration-evidence.json').write_text(json.dumps({'manifest_path':'generate/runs/current/manifest.json','manifest_sha256':hashlib.sha256((R/'generate/runs/current/manifest.json').read_bytes()).hexdigest(),'row':row,'interpretation':'Latest immutable candidate inventory says has_generator false; numeric script/tree/cache absent before import.'},indent=2))
for p in ['generate/principles.md',*[f'generate/docs/{x}' for x in ['3-classify.md','4-template-extraction.md','5-plot-extraction.md','6-template-generator.md','7-plot-generator.md']],'docs/math-content.md','scripts/question_capture/math_format.py']:
 target=D/'reference'/Path(p).name;shutil.copyfile(R/p,target)
b=json.loads((R/'generate/scratch/17592186059716-draft/reference/grader-build.json').read_text());shutil.copyfile(R/'generate/scratch/17592186059716-draft/reference/grader-build.json',D/'reference/grader-build.json')
paths={b['source']:b['source_sha256'],b['library']:b['library_sha256'],b['binary']:b['binary_sha256'],**b['engine_sources'],**b['dependencies']}
assert len(paths)==42,len(paths)
for p,h in paths.items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
(D/'reference/native-42-before.json').write_text(json.dumps(paths,indent=2))
shutil.copyfile(R/b['binary'],D/'check-engine');(D/'check-engine').chmod(0o755)
s=importlib.util.spec_from_file_location('draft00869',D.with_suffix('.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
cases=[];fidelity=[]
for t,q in m.SOURCES.items():
 p=m.source_parameters(t);rec=m.generate(m.source_level(t),template=t,parameters=p,profile='raw-'+t)
 cases.append({'source_id':q[':question/id'],'math_academy_id':t,'level':m.source_level(t),'template':t,'parameters':p,'bank_profile':'raw-'+t})
 for key in [':question/problem',':question/worked-solution']:
  if rec['question'][key]!=m.normalize_prose(q[key]):print(t,key,'\n'.join(difflib.unified_diff(m.normalize_prose(q[key]).splitlines(),rec['question'][key].splitlines())))
 fidelity.append(rec)
(D/'source-cases.json').write_text(json.dumps(cases,indent=2));(D/'replayed-sources.json').write_text(json.dumps(fidelity,indent=2))
(D/'independent-inventory.json').write_text(json.dumps({k:v for k,v in m.SNAPSHOT.items() if k!='record'}|{'questions':[],'interpretation':'All 10 practice records have MA IDs; canonical example is separate.'},indent=2))
