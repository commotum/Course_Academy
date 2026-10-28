import hashlib,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from generator_packages import package_digest
G=json.loads((H/'generators.json').read_text());descriptors=[]
helper='''\ndef asset_identity(value):
    """Content identity omits caller-owned filesystem placement."""
    value=str(value)
    def one(path):
        p=Path(path)
        return 'asset-sha256:'+hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else path
    if value.endswith(('.png','.svg')) and Path(value).is_file():return one(value)
    return re.sub(r'!\\[([^\\]]*)\\]\\(([^)]+)\\)',lambda m:'!['+m[1]+']('+one(m[2])+')',value)
\n'''
for kp in[17592186096649,17592186096700]:
 g=next(g for g in G if g['kp']==kp);old=Path(g['path']);dst=H/'generators'/str(kp);dst.mkdir(parents=True,exist_ok=True)
 for name in g['files']:
  if name=='generator-package.json':continue
  t=dst/name;t.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.parent/name,t)
 p=dst/'generator.py';s=p.read_text();s='import hashlib,re\n'+s if 'from __future__'not in s else s.replace('from __future__ import annotations','from __future__ import annotations\nimport hashlib,re')
 marker='def generate('if kp==17592186096649 else'def make_record('
 # Insertion must precede decorators, preserving checked_math_content scope.
 marker='@checked_math_content\n'+marker if kp==17592186096649 else marker
 s=s.replace(marker,helper+marker,1)
 if kp==17592186096649:
  s=s.replace("VERSION = 'parallel-vectors-3'","VERSION = 'parallel-vectors-4'")
  s=s.replace("'prompt':prompt,'bank':sorted(images),'solution':sol","'prompt':asset_identity(prompt),'bank':sorted(asset_identity(v) for v in images),'solution':asset_identity(sol)")
  s=s.replace("uid([fid,path])","uid([fid,asset_identity(path)])")
 else:
  s=s.replace("VERSION = 'parallel-diagram-4'","VERSION = 'parallel-diagram-5'")
  s=s.replace("content={'prompt':prompt,'worked':worked", "content={'version':VERSION,'prompt':asset_identity(prompt),'worked':asset_identity(worked)")
 p.write_text(s);shutil.copyfile(R/'scripts/question_capture/math_format.py',dst/'math_format.py')
 evidence={'basis':9837,'kp':kp,'old_reference':g['registration'][':question-generator/script'],'defect':'Fresh question and all descendant IDs depended on generated-asset directory path despite identical pixels.','change':'Derive identities from normalized question content with actual image-byte SHA256, before assigning question/field/answer UUIDs. Bump version for changed identity semantics. Preserve actual served absolute output paths.','raw_replay':'Existing source values and raw replay controls preserved.','PNG_byte_evidence':'Original /tmp outputdir a/b PNG bytes match. Renderer JSON sidecars differ only because their spec.output records caller paths; they are diagnostic evidence, not served graphics.','scope':'No change to geometry, truth predicates, source guards, option banks, sampler domains, or rendering methods.'}
 (dst/'repair-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');files=sorted(str(p.relative_to(dst))for p in dst.rglob('*')if p.is_file());deps=g['manifest']['dependencies'];dg=package_digest(dst,'generator.py',files,dependencies=deps)
 descriptors.append({'kp':kp,'old_reference':g['registration'][':question-generator/script'],'directory':str(dst),'entrypoint':'generator.py','files':files,'dependencies':deps,'approved_digest':dg})
(H/'generator-candidates.json').write_text(json.dumps(descriptors,indent=2)+'\n');print([(d['kp'],d['approved_digest'])for d in descriptors])
