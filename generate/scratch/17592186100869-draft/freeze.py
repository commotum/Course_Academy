"""Freeze/check entire owned draft plus numeric absence and current native42."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,importlib.util,json
D=Path(__file__).resolve().parent;R=D.parents[2];script=D.with_suffix('.py')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
before=json.loads((D/'numeric-before-import.json').read_text());p=D.with_name('17592186100869.py')
actual=([p] if p.exists() else [])+list(p.with_suffix('').rglob('*'))+list(p.parent.glob('__pycache__/17592186100869.*.pyc'))
assert sorted(str(x.resolve()) for x in actual)==before['paths']
assert {str(x.resolve()):sha(x) for x in actual if x.is_file()}==before['files']
current=json.loads((D/'reference/native-42-before.json').read_text())
assert len(current)==42
for path,h in current.items():assert sha(R/path)==h,path
assert sha(D/'check-engine')=='33510bf3ac27a1eb28e9bad7b4121a22d2fa787026d3102268daa4ecf98b1617'
assert sha(D/'source.json')==sha(R/'generate/runs/current/refresh-2026-10-14/sources/17592186100869.json')
sp=importlib.util.spec_from_file_location('frozen00869',script);g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
render=json.loads((D/'render-validation.json').read_text());whole=json.loads((D/'whole-input.json').read_text());whole_by_label={x['label']:x for x in whole}
for entry in render['reports']:
 rec=entry['exact_record'];meta=rec['generation'];again=g.generate(meta['level'],meta['seed'],template=meta['template'],parameters=meta['parameters'],profile=meta['profile'])
 assert again==rec,entry['name']
 assert sha(D/entry['screenshot'])==entry['screenshot_sha256']
 assert hashlib.sha256(json.dumps(rec,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==entry['record_sha256']
 native=whole_by_label['screenshot-'+entry['name']];assert native['record']==rec
 for test in entry['subsets']:
  mask=test['mask']
  for i,response in enumerate(test['responses']):assert response=={'fieldId':20+i,'choiceId':100+2*i+(1 if mask&(1<<i) else 0)}
 # Raw collapsed-source layout is explicit evidence; normal repair must be a list.
 if entry['name']=='generated-q-42374':assert '- **I.**' in rec['question'][':question/problem']
for case in json.loads((D/'source-cases.json').read_text()):
 rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile'])
assert json.loads((D/'validation.json').read_text())['passed']
assert json.loads((D/'whole-validation.json').read_text())['passed'] and render['passed']
paths=sorted([script]+[p for p in D.rglob('*') if p.is_file() and p.name!='freeze.json'])
files={str(p.relative_to(R)):sha(p) for p in paths}
state={'script':str(script.relative_to(R)),'script_sha256':sha(script),'file_count':len(files),'files':files,'directories':sorted(str(p.relative_to(R)) for p in D.rglob('*') if p.is_dir()),'numeric_path_set_and_hashes_unchanged':True,'numeric_before_import_absent':True,'native_42_hashes_rechecked':True,'source_wrapper_sha256':sha(D/'source.json'),'render_records_exact_replay':len(render['reports']),'UI_native_subset_payloads_matched':len(render['reports'])*8,'approval':'pending root QA; stop after7; no registration'}
if '--check' in sys.argv:assert state==json.loads((D/'freeze.json').read_text());print('Whole owned freeze exact:',len(files),'files; script',sha(script))
else:(D/'freeze.json').write_text(json.dumps(state,indent=2));print('Frozen:',len(files),'files; script',sha(script))
