"""Relocate declared runtime files and exercise the public CLI without repository imports."""
from common import *
import subprocess,tempfile,shutil,os,platform,math,functools,hashlib
manifest=json.loads((ROOT/'package.json').read_text());before={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in manifest['files']}
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':load_generator().sp.__version__}}
assert 'package.json' not in manifest['files']
with tempfile.TemporaryDirectory(prefix='relocation-',dir=E) as tmp:
 folder=Path(tmp)
 for p in manifest['files']:
  dest=folder/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
 assets=folder/'external-assets';assets.mkdir()
 cmd=[sys.executable,str(folder/manifest['entrypoint']),'--difficulty','easy','--count','5','--seed','2406259497','--format','json']
 r=subprocess.run(cmd,cwd=folder,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','COURSE_ACADEMY_GENERATOR_OUTPUT_DIR':str(assets)})
 assert r.returncode==0,r.stderr
 relocated=json.loads(r.stdout)
 assert relocated==json.loads((E/'batch.json').read_text())
 for item in relocated:verify(item)
 assert sorted(p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file())==sorted(manifest['files'])
 save('relocated-records.json',relocated)
# Semantic equivalence witness ignores IDs, labels, choice order, common scaling
# and row ordering. Integer primitive vector triples, canonicalized for either sign.
def semantic(r):
 _,_,(a,u,b,c,sign)=solve(r['question']);rows=list(zip(a,u,b));den=math.lcm(*(x.denominator for row in rows for x in row))
 ints=[[int(x*den) for x in row] for row in rows]
 divisor=functools.reduce(math.gcd,(abs(x) for row in ints for x in row)) or 1
 pos=tuple(sorted(tuple(x//divisor for x in row) for row in ints))
 neg=tuple(sorted(tuple(-x//divisor for x in row) for row in ints))
 return (c,sign,min(pos,neg))
allrows=json.loads((E/'all-test-records.json').read_text());batch=json.loads((E/'batch.json').read_text())
assert len({semantic(r) for r in batch})==5
coverage={}
for level in ['easy','moderate']:
 rows=json.loads((E/f'delivery-{level}/accepted.json').read_text())
 coverage[level]={'delivered_records':len(rows),'semantic_instances':len({semantic(r) for r in rows})}
assert before=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in manifest['files']}
save('packaging-results.json',{'passed':True,'dependencies_exact':True,'relocation_and_public_cli':True,'deterministic_equal':True,'runtime_files_unchanged':True,'runtime_hashes':before,'external_asset_directory':'No assets needed or produced','semantic_count_rule':'Independently parsed vector equation; coordinate permutation, common scaling, labels and banks ignored. Distinct coefficient or operation retained.','semantic_counts':coverage,'batch_semantic_instances':5,'all_test_semantic_instances':len({semantic(r) for r in allrows})})
print(json.dumps({'relocation':'passed','semantic_counts':coverage,'batch_semantic_instances':5}))
