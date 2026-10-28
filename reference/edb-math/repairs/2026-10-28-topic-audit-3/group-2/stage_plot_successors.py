import ast,importlib.metadata,json,re,shutil,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[4];sys.path.insert(0,str(R/'scripts'));from generator_packages import package_digest
G=json.loads((H/'generators.json').read_text());D=json.loads((H/'generator-candidates.json').read_text())
for kp in[17592186166865,17592186166866]:
 g=next(g for g in G if g['kp']==kp);old=Path(g['path']);dst=H/'generators'/str(kp);dst.mkdir(parents=True,exist_ok=True);entry=old.name;folder=dst/str(kp);folder.mkdir(exist_ok=True)
 for name in ['render.py','source.json']if kp==17592186166865 else['render.py','reference/source-current.json']:
  target=folder/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old.with_suffix('')/name,target)
 s=old.read_text();s=s.replace('import argparse,','import os\nimport argparse,',1)
 s=s.replace("out=Path(output_dir or HERE/'plots')", "out=Path(output_dir or os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'])").replace("out=Path(output_dir or HERE/'assets')", "out=Path(output_dir or os.environ['COURSE_ACADEMY_GENERATOR_OUTPUT_DIR'])")
 if kp==17592186166865:
  s=s.replace("path=HERE.parent.parent/'runs/current/ode-scalar-parser.py'", "path=Path(__file__).with_name('scalar_parser.py')");shutil.copyfile(R/'generate/runs/current/ode-scalar-parser.py',dst/'scalar_parser.py')
  for name in['ca_source_runtime.py','ca_source_policy.py',str(kp)+'-source-policy.json']:shutil.copyfile(old.parent/name,dst/name)
 else:s=s.replace("str(Path(__file__).resolve().parents[2]/'.venv/bin/python')",'sys.executable')
 # Font module is local in a flat immutable package.
 s=s.replace('from scripts.question_capture.math_format import','from math_format import')
 tree=ast.parse(s);node=next(n for n in tree.body if isinstance(n,ast.If)and'__name__'in ast.unparse(n.test));lines=s.splitlines(True);lines.insert(node.lineno-1,'\nfrom source_notation import install as _install_source_notation\n_install_source_notation(globals())\n\n');(dst/entry).write_text(''.join(lines))
 render=folder/'render.py';rr=render.read_text();start=rr.index('try:import matplotlib');end=rr.index('matplotlib.use',start);rr=rr[:start]+'import matplotlib\n'+rr[end:];render.write_text(rr)
 shutil.copyfile(R/'scripts/question_capture/math_format.py',dst/'math_format.py');(dst/'source_notation.py').write_text((H/'source_notation.py').read_text())
 evidence={'basis':9837,'kp':kp,'roles':[],'change':'Honor caller outputdir, use current declared interpreter/dependencies instead of repository or cache fallback paths, bundle circle-bank parser/policy helpers, derive final normalized question and all descendant UUIDs from content and image bytes. Preserve source math, raw evidence, current bank predicates and source guards.','defect':'Legacy generation writes plots into mutable script data folder regardless of outputdir. Circle identities include that absolute path; ellipse renderer spawns repo-relative .venv. These fail self-contained immutable-package relocation.','old_contract':'Original registered legacy path can legitimately rely on its repository layout; missing private-copy dependencies are not called live sampler bugs. These portability changes are necessary for the narrow successor packages.'};(dst/'repair-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');deps={'python':sys.version.split()[0],'packages':{n:importlib.metadata.version(n)for n in['sympy','matplotlib','numpy']}};files=sorted(str(p.relative_to(dst))for p in dst.rglob('*')if p.is_file());D.append({'kp':kp,'old_reference':g['registration'][':question-generator/script'],'directory':str(dst),'entrypoint':entry,'files':files,'dependencies':deps,'approved_digest':package_digest(dst,entry,files,dependencies=deps),'smoke_band':'easy','supported_difficulties':['easy','moderate','hard']})
(H/'generator-candidates.json').write_text(json.dumps(D,indent=2)+'\n')
