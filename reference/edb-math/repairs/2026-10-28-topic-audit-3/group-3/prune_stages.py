import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent;rows=json.loads((H/'generator-stage-plan.json').read_text());rawproof=[]
extra={17592186129269:['readback.py'],17592186129283:['asset-index.json','render.py'],17592186133927:['render.py'],17592186172130:['lessons.json'],17592186198361:['templates.json'],17592186198398:['raw-recipes.json'],17592186198399:['raw-recipes.json']}
for row in rows:
 p=Path(row['directory']);kp=row['kp']
 if not row['legacy']:continue
 allow={row['entrypoint'],'math_format.py','audit_runtime.py','ca_source_runtime.py','ca_source_policy.py','generator_source_policy.py','generator_policy.py',str(kp)+'-source-policy.json',str(kp)+'/source.json'}|{str(kp)+'/'+s for s in extra.get(kp,[])}
 for file in p.rglob('*'):
  if file.is_file()and str(file.relative_to(p))not in allow:file.unlink()
 original=Path('generate/scratch');kept=[]
 for file in p.rglob('*.json'):
  rel=file.relative_to(p);src=original/rel
  if src.exists():assert src.read_bytes()==file.read_bytes();kept.append({'file':str(rel),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'original':str(src)})
 rawproof.append({'kp':kp,'retained_raw_json_unchanged':kept})
 row['dependencies']={'python':'3.13','packages':{'sympy':'1.14.0',**({'matplotlib':'3.11.2','numpy':'2.5.4','pillow':'12.3.0'}if kp in[17592186129283,17592186133927,17592186198374]else{})}}
(H/'generator-stage-plan.json').write_text(json.dumps(rows,indent=2));(H/'staged-raw-input-proof.json').write_text(json.dumps(rawproof,indent=2))
