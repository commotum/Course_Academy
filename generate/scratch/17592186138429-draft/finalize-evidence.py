"""Freeze owned candidate and verify registered baseline without importing it."""
import pathlib,hashlib,json,subprocess,os,importlib.util,random
H=pathlib.Path(__file__).resolve().parent;R=H.parents[2]
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
b=json.loads((H/'registered-baseline.json').read_text());changed=[p for p,v in b['files'].items() if not pathlib.Path(p).is_file() or hashfile(pathlib.Path(p))!=v]
num=R/'generate/scratch/17592186138429';current={str(p.relative_to(R)) for p in num.rglob('*') if p.is_file()};expected=set(b['files'])-{'generate/scratch/17592186138429.py'}
assert not changed and current==expected
assert sorted(str(p.relative_to(R)) for p in num.rglob('*') if p.is_dir())==b['directories']
(H/'registered-baseline-verification.json').write_text(json.dumps({'status':'unchanged','files':len(b['files']),'registered_sha256':b['script_sha256'],'added_files':sorted(current-expected),'changed_files':changed},indent=2)+'\n')
# Built-in CLI seed and count defaults are exercised separately from explicit seed/count.
cmd=[str(R/'.venv/bin/python'),str(H.with_suffix('.py')),'--format','json'];env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
a=subprocess.check_output(cmd,text=True,env=env);bb=subprocess.check_output(cmd,text=True,env=env);assert a==bb and len(json.loads(a))==3
(H/'builtin-defaults.json').write_text(json.dumps({'format':'json','difficulty':'all','builtin_seed':0,'builtin_count':1,'record_count':3,'repeated_exact_output':True},indent=2)+'\n')
# Effective normal slots for the retained historical samplers, without rendering.
spec=importlib.util.spec_from_file_location('owned_draft',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
coverage={}
for name in g.TEMPLATES:
 rows=[g.sample(name,random.Random(i)) for i in range(500)];coverage[name]={'seeds':500,'unique_line_tasks':len({tuple(str(p[k]) for k in ['a0','a1','b0','b1']) for p in rows}),'effective_slots':{k:sorted({str(p[k]) for p in rows}) for k in ['a0','a1','b1']}}
(H/'effective-slot-coverage.json').write_text(json.dumps(coverage,indent=2)+'\n')
rs=json.loads((H/'revalidation-sampled.json').read_text());assets=[]
for r in rs:
 if r['generation']['template']=='walkers':
  for role,p in r['generation']['plot_assets'].items():assets.append({'path':str(pathlib.Path(p['path']).relative_to(R)),'role':role,'sha256':hashfile(pathlib.Path(p['path']))})
(H/'revalidation-visual-review.json').write_text(json.dumps({'status':'inspected','method':'Direct source prompt/solution PNG inspection; nine side-by-side walker prompt/solution sheets, each viewed at1664x680. Plane and tank replay solutions directly viewed; prior established template visual evidence retained.','findings':'Blue Sam and red Mary retain source roles; zero-distance endpoint clipped to physical segment; numbered/minor ticks, intersection and dashed guides agree with both blanks. All final viewed names, units, coordinate labels readable.','renderer_sha256':hashfile(H/'render.py'),'assets':assets},indent=2)+'\n')
freeze={'status':'awaiting independent root review','generator_sha256':hashfile(H.with_suffix('.py')),'registered_baseline_sha256':b['script_sha256'],'source_sha256':hashfile(H/'source.json'),'native_checker_sha256':hashfile(H/'check-engine-frozen'),'files':{str(p.relative_to(R)):hashfile(p) for p in sorted(H.rglob('*')) if p.is_file() and p.name!='freeze.json'}}
(H/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n');print(json.dumps({k:v for k,v in freeze.items() if k!='files'},indent=2))
