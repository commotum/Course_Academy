import json,re,shutil
from pathlib import Path
H=Path(__file__).resolve().parent;configs=json.loads((H/'generator-stage-config.json').read_text())
legacy={17592186083245,17592186083280,17592186129267,17592186129268,17592186133899,17592186133900,17592186157298,17592186175987,17592186176023,17592186176024,17592186198389}
for cfg in configs:
 root=Path(cfg['directory']);kp=cfg['kp']
 if kp in legacy:
  source=f'{kp}/reference/initial/source.json'if kp==17592186157298 else f'{kp}/source-current.json'if kp==17592186175987 else f'{kp}/source.json'
  files=[cfg['entrypoint'],'math_format.py','generator_policy.py','audit_presentation.py','repair-evidence.json',source]
  if kp==17592186083280:files.append(f'{kp}/mathcheck_{kp}.py')
  if kp in[17592186133900,17592186175987]:files+=['ca_source_policy.py','ca_source_runtime.py',str(kp)+'-source-policy.json']
  refs=set(re.findall(r'images/[a-f0-9]{2}/[a-f0-9]+\.(?:png|svg)',(root/source).read_text()))
  if kp in[17592186133899,17592186175987]:
   for ref in refs:
    original=Path('/media/jake/SSD/EDB/math')/ref;name=('source-assets/'if kp==17592186133899 else str(kp)+'/')+ref
    target=root/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,target);files.append(name)
  cfg['files']=sorted(set(files));cfg['dependencies']['packages']['numpy']='2.5.4'
  for f in cfg['files']:assert(root/f).is_file(),(kp,f)
 # Update runtime change evidence after the portable closure has been validated.
 p=root/'repair-evidence.json';e=json.loads(p.read_text());e['portable_runtime']='All generated plots and caches target COURSE_ACADEMY_GENERATOR_OUTPUT_DIR or a temporary cache, not the immutable source package. Source image bytes required by runtime file reads are bundled. Output-directory paths are excluded from content identity using actual image SHA256.';e['runtime_file_count']=len(cfg['files']);p.write_text(json.dumps(e,indent=2)+'\n')
 if kp==17592186157298:
  p=root/cfg['entrypoint'];s=p.read_text();s=s.replace("str(Path(__file__).with_suffix('')/'reference/mpl-cache')","str(_ca_asset_output(Path('matplotlib-cache')).parent/'matplotlib-cache')");p.write_text(s)
(H/'generator-stage-config.json').write_text(json.dumps(configs,indent=2)+'\n');print('declared closure',[(c['kp'],len(c['files']))for c in configs])
