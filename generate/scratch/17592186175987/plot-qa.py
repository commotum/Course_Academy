#!/usr/bin/env python3
import concurrent.futures,hashlib,importlib.util,json,subprocess,sys,uuid
from pathlib import Path
from PIL import Image
base=Path(__file__).resolve().parent;root=base/'render-concurrency'/str(uuid.uuid4());root.mkdir(parents=True)
script=base.with_suffix('.py')
code="""import importlib.util,sys,sympy as sp
from pathlib import Path
s=importlib.util.spec_from_file_location('g',sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g);g.BASE=Path(sys.argv[2]);print(g.render_sector(int(sys.argv[3]),sp.pi/2,2*sp.pi,True))
"""
def run(radius):
 p=subprocess.run([sys.executable,'-c',code,str(script),str(root),str(radius)],capture_output=True,text=True,check=True);return p.stdout.strip()
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:paths=list(pool.map(run,[3,3,4]))
assert paths[0]==paths[1] and paths[0]!=paths[2]
for radius,path in zip([3,3,4],paths):
 png=Path(path);meta=json.loads(png.with_suffix('.json').read_text());assert meta['radius']==radius;assert meta['orientation']=='counterclockwise';assert meta['sha256']==hashlib.sha256(png.read_bytes()).hexdigest()
 with Image.open(png) as im:assert im.size==(480,480)
copy_code=code.replace('import importlib.util,sys,sympy as sp','import importlib.util,sys,sympy as sp,json').replace('print(g.render_sector(int(sys.argv[3]),sp.pi/2,2*sp.pi,True))',"print(json.dumps(g.get_plots(g.QS['q-108544'],2,2,-sp.pi/2,sp.pi/2)))")
def copy_source(_):
 p=subprocess.run([sys.executable,'-c',copy_code,str(script),str(root),'2'],capture_output=True,text=True,check=True);return json.loads(p.stdout)
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:source_paths=list(pool.map(copy_source,[0,1]))
assert source_paths[0]==source_paths[1]
assert all(Path(p).exists() for p in source_paths[0])
assert not list(root.rglob('tmp*'))
report={'fresh_directory':str(root),'same_parameter_concurrency':'passed','different_parameter_concurrency':'passed','source_copy_concurrency':'passed','temporary_file_leaks':0,'paths':paths,'dimensions':[480,480]};(base/'plot-qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
