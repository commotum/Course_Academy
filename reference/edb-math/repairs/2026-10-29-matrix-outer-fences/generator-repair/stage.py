"""Stage immutable successors; preserve original mathematical generator inputs."""
import ast,json,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R))
from scripts.generator_packages import build_manifest,manifest_digest
source=(R/'scripts/question_capture/math_format.py').read_text();tree=ast.parse(source)
needed={'environment','_tex_nonspace_before','_tex_command_before','_tex_sizing_command','_scalable_composite_fences','scalable_table_fences'}
helper=['"""Narrow shared table fence normalizer; no algebra or identity changes."""','import re']
for n in tree.body:
    if isinstance(n,ast.FunctionDef)and n.name in needed or isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id in {'ENV','MATH'}for t in n.targets):helper.append(ast.get_source_segment(source,n))
helper='\n\n'.join(helper)+'\n';candidates=[]
checks=json.loads((H.parent/'generator-verification.json').read_text())['checks']
for g in json.loads((H/'affected.json').read_text()):
    old=Path('/media/jake/SSD/EDB/math')/g['reference'];manifest=json.loads((old.parent/'generator-package.json').read_text());directory=H/'packages'/str(g['kp']);directory.mkdir(parents=True,exist_ok=True)
    for name in manifest['files']:
        p=directory/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.parent/name,p);p.chmod(0o644)
    (directory/'table_fences.py').write_text(helper)
    (directory/'fence_repaired_generator.py').write_text((H/'entrypoint.py').read_text().replace('__ORIGINAL_ENTRYPOINT__',old.name))
    files=sorted(list(manifest['files'])+['table_fences.py','fence_repaired_generator.py'])
    new=build_manifest(directory,'fence_repaired_generator.py',files,dependencies=manifest['dependencies']);digest=manifest_digest(new)
    bands=[c['band']for c in checks if c['kp']==g['kp']and c['returncode']==0]
    candidates.append({'kp':g['kp'],'old_reference':g['reference'],'directory':str(directory),'entrypoint':'fence_repaired_generator.py','files':files,'dependencies':manifest['dependencies'],'approved_digest':digest,'smoke_band':bands[0],'supported_difficulties':bands})
(H/'generator-candidates.json').write_text(json.dumps(candidates,indent=2)+'\n');print('Staged',len(candidates),'immutable replacements')
