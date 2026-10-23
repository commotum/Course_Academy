import json, sys, subprocess, tempfile, shutil, platform
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence'
manifest=json.loads((ROOT/'package.json').read_text())
import sympy
assert manifest['dependencies']=={'python':platform.python_version(),'packages':{'sympy':sympy.__version__}}
assert set(manifest['files'])=={'17592186096669.py','17592186096669/source.json','requirements.txt'}
with tempfile.TemporaryDirectory(prefix='generator-relocation-',dir=OUT) as tmp:
    target=Path(tmp)
    for name in manifest['files']:
        dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,dest)
    args=['--difficulty','easy','--count','5','--seed','73421','--format','json']
    cmd=[sys.executable,str(target/manifest['entrypoint']),*args]
    first=subprocess.run(cmd,cwd=tmp,capture_output=True,text=True,check=True).stdout
    second=subprocess.run(cmd,cwd=tmp,capture_output=True,text=True,check=True).stdout
    assert first==second==(OUT/'batch.json').read_text()
    invalid=[]
    for args in (['--difficulty','hard'],['--count','0'],['--scale','0'],['--scale','10']):
        result=subprocess.run([sys.executable,str(target/manifest['entrypoint']),*args],cwd=tmp,capture_output=True,text=True)
        assert result.returncode!=0
        invalid.append({'args':args,'exit':result.returncode})
(OUT/'packaging.json').write_text(json.dumps({'passed':True,'dependencies':manifest['dependencies'],'relocation':True,'deterministic':True,'invalid_inputs':invalid},indent=2))
source=json.loads((ROOT.parent/'source/source.json').read_text());inv=json.loads((ROOT.parent/'source/inventory.json').read_text())
sourceids={q[':question/id'] for q in source['material']['kp'][':knowledge-point/questions']}
rows=[{'question_id':q[':question/id'],'entity_id':q[':db/id'],'original_source':q[':question/id'] in sourceids,'generation_keys':[k for k in q if 'generat' in k],'retirement_keys':[k for k in q if 'retir' in k]} for q in inv['questions']]
assert all(r['original_source'] and not r['generation_keys'] for r in rows)
(OUT/'inventory-review.json').write_text(json.dumps({'basis':inv['basis'],'questions':rows,'generated_records':0,'conclusion':'Verified absence of generated records in the supplied inventory; all 13 are original sources and ineligible for generated-pool repair. Live database not inspected.'},indent=2))
(OUT/'affected-inventory.json').write_text(json.dumps({'affected_questions':[]},indent=2))
print(json.dumps({'package':'passed','inventory_original_sources':len(rows),'generated':0}))
