import json,sys,subprocess,shutil,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[3];WORK=ROOT.parent/'workspace';PY=REPO/'.venv/bin/python'
def run(args):
 p=subprocess.run([str(x) for x in args],capture_output=True,text=True,check=True);return p.stdout
manifest=json.loads((WORK/'package.json').read_text());dst=ROOT/'relocated';dst.mkdir(exist_ok=True)
for f in manifest['files']:
 (dst/f).parent.mkdir(parents=True,exist_ok=True);shutil.copy2(WORK/f,dst/f)
records=json.loads((ROOT/'samples.json').read_text());res={'commands':[],'dependencies':manifest['dependencies'],'file_hashes':{f:hashlib.sha256((WORK/f).read_bytes()).hexdigest() for f in manifest['files']},'bands':{}}
version=run([PY,'-c','import sys,sympy,json;print(json.dumps({"python":sys.version.split()[0],"packages":{"sympy":sympy.__version__}}))']);assert json.loads(version)==manifest['dependencies']
for band in ('easy','moderate','hard'):
 args=[PY,WORK/'generator.py','--difficulty',band,'--count','8','--seed','92817'];first=run(args);second=run(args);assert first==second
 relocated=run([PY,dst/'generator.py',*args[2:]]);assert first==relocated
 input_file=ROOT/(band+'-samples.json');chosen=[r for r in records if r['question'][':question/difficulty'].endswith('/'+band)];input_file.write_text(json.dumps(chosen,indent=2)+'\n')
 command=[PY,REPO/'generate/pipeline/check_delivery.py','--input',input_file,'--source',ROOT.parent/'source/source.json','--inventory',ROOT.parent/'source/inventory.json','--difficulty',band,'--output',ROOT/('delivery-'+band),'--asset-root',WORK]
 out=run(command);res['commands'].append(' '.join(map(str,command)));res['bands'][band]={'deterministic_byte_replay':True,'relocation_identical':True,'cli_count':8,'filter_summary':out.strip()}
(ROOT/'packaging-delivery.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res['bands']))
