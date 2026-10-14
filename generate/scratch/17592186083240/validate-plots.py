#!/usr/bin/env python3
"""Independent plot-record consistency and concurrent fresh rendering."""
import importlib.util,json,pathlib,re,subprocess,hashlib,sys,tempfile
from PIL import Image
D=pathlib.Path(__file__).resolve().parent;REPO=D.parents[2]
s=importlib.util.spec_from_file_location('g',D.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
from math_parser import parse
checked=[]
for template,ref in json.loads((D/'plot-review.json').read_text()):
 r=g.generate(g.TEMPLATES[template]['level'],template=template,parameters={'r':'2','s':'3'},seed=8)
 image=pathlib.Path(re.findall(r'!\[\]\(([^)]+)\)',r['question'][':question/problem'])[0]);assert image==pathlib.Path(ref)
 side=json.loads(image.with_suffix('.json').read_text())
 b=re.findall(r'\$\$\n(.*?)\n\$\$',r['question'][':question/problem'],re.S)[0];xt,yt,_=re.fullmatch(r'x=(.*?),\\,y=(.*?),\\,(.*)',b,re.S).groups()
 assert g.same(parse(xt),g.sp.sympify(side['x'],locals={'t':g.T}))
 assert g.same(parse(yt),g.sp.sympify(side['y'],locals={'t':g.T}))
 assert tuple(side['parameter_window'])==g.PLOT_T[template]
 assert side['domain_endpoint_markers']==(template=='line_quad')
 with Image.open(image) as im:
  assert im.size==(600,480)
  pixels=list(im.convert('RGB').get_flattened_data());assert sum(b>r+30 and b>gg+10 for r,gg,b in pixels)>500
 checked.append({'template':template,'sha256':hashlib.sha256(image.read_bytes()).hexdigest(),'same_printed_coordinates':True,'visible_blue_curve':True})
# Three independent interpreters exercise genuinely fresh, same and different
# writes without touching any normal cache or another active producer's folder.
private_base=D/'render-concurrency';private_base.mkdir(exist_ok=True)
private=pathlib.Path(tempfile.mkdtemp(prefix='run-',dir=private_base))
script="""import importlib.util,json,sys,pathlib
s=importlib.util.spec_from_file_location('g',sys.argv[1]);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
g.HERE=pathlib.Path(sys.argv[2]);q,x,y,point,domain=g.source_recipe('trig_double',{'r':sys.argv[3],'s':sys.argv[4]})
print(g.render_plots(q[':question/problem'],'trig_double',{},x,y))
"""
procs=[subprocess.Popen([sys.executable,'-c',script,str(D.with_suffix('.py')),str(private),r,s],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True) for r,s in [('6','1/2'),('6','1/2'),('1/2','6')]]
outputs=[]
for p in procs:
 out,err=p.communicate();assert p.returncode==0,err;outputs.append(re.findall(r'!\[\]\(([^)]+)\)',out)[0])
assert outputs[0]==outputs[1] and outputs[0]!=outputs[2]
for ref in set(outputs):
 image=pathlib.Path(ref);side=json.loads(image.with_suffix('.json').read_text())
 with Image.open(image) as im:im.verify()
 assert side['template']=='trig_double' and side['matplotlib']
assert set(p.suffix for p in (private/'plots').iterdir())=={'.png','.json'},'current private render temp leaked'
result={'passed':True,'independent_source_variant_plots_checked':checked,'fresh_concurrent_calls':3,'same_and_different_parameters':True,'private_temporary_files_clean':True,'source_visual_review':'source-plots-inspected.png','generated_visual_review':'generated-plots-inspected.png'}
(D/'plot-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
