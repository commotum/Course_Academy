"""Reproduce the original cold-render dependency failure and its repair.
Output/cache empty, original package always read-only, hidden old interpreter.
"""
from review import *
import importlib.metadata,platform
for name,origin in [('old',J/'review-0-policy-2-4c6625aaf57ad834/runtime/package'),('current',W)]:
 base=E/('strict-cold-'+name);base.mkdir(exist_ok=True)
 manifest=json.loads((origin/'package.json').read_text());pk=base/'package';pk.mkdir(exist_ok=True)
 for rel in manifest['files']:
  dest=pk/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(origin/rel,dest)
 # Original assets must be absent, to preclude accidental bundled-cache success.
 (pk/KP/'plots').mkdir(exist_ok=True)
 (base/'plots').mkdir(exist_ok=True);(base/'out').mkdir(exist_ok=True);(base/'empty').mkdir(exist_ok=True)
 no=base/'no-exec';no.write_text('old Python deliberately unavailable\n')
 before=hashes(pk)
 cmd=sandbox([P,pk/(KP+'.py'),'--difficulty','moderate','--seed','801239','--count','1','--format','json'],['--ro-bind',str(no),'/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10','--ro-bind',str(base/'empty'),'/home/jake/.cache/uv','--bind',str(base/'plots'),str(pk/KP/'plots')])
 p=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(RT/'tmp'),'COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(base/'out')})
 dump('strict-cold-'+name+'.json',{'command':list(map(str,cmd)),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'package_unchanged':before==hashes(pk),'output_png_count':len(list((base/'out').rglob('*.png'))),'original_failure_expected':name=='old'})
 assert before==hashes(pk)
 if name=='old':assert p.returncode!=0 and ('Permission denied' in p.stderr or 'CalledProcessError' in p.stderr),p.stderr
 else:assert p.returncode==0 and len(json.loads(p.stdout))==1,p.stderr
 print(name,p.returncode,p.stderr[-500:])
