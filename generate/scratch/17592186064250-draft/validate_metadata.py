"""Structural/CLI regression for the db_id metadata repair; math is unchanged."""
import sys
sys.dont_write_bytecode=True
import hashlib,importlib.util,json,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('arcsec_metadata_draft',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
counts={}
for name in ['source-cases.json','review-cases.json','independent-role-review.json']:
 data=json.loads((H/name).read_text());records=[x['record'] for x in data] if name!='independent-role-review.json' else data
 for r in records:
  k=r['knowledge_point'];assert k['db_id']==17592186064250 and k['id']==g.KP_UUID and k['title']==g.SOURCE['record'][':knowledge-point/title']
  fields=r['question'][':question/answer-fields'];assert len(fields)==1
  for f in fields:
   assert f[':answer-field/correct'][1] in {a[':answer/id'] for a in f[':answer-field/choices']}
  if name!='source-cases.json':
   g.fmt.validate_generated_record(r);m=r['generation']
   assert r==g.generate(r['question'][':question/difficulty'].split('/')[-1],m['seed'],profile=m['profile'],parameters=m['parameters'])
 if name=='source-cases.json':
  assert len(data)==17 and {x['source_id'] for x in data}==set(g.PROFILES) and all(x['source_id']==x['label'] for x in data)
 counts[name]=len(records)
for fmt in ['json','markdown']:
 cmd=[sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--seed','2718','--count','2','--format',fmt]
 a=subprocess.run(cmd,check=True,capture_output=True).stdout;b=subprocess.run(cmd,check=True,capture_output=True).stdout;assert a==b
 if fmt=='json':
  rows=json.loads(a);assert len(rows)==6 and all(r['knowledge_point']['db_id']==17592186064250 for r in rows)
for lev,count in [('easy',23),('moderate',100),('hard',357),('all',23)]:
 try:g.batch(lev,count,0)
 except ValueError as e:assert 'capacity' in str(e)
 else:raise AssertionError('Overcapacity accepted')
z=subprocess.run([sys.executable,str(H.with_suffix('.py')),'--difficulty','easy','--seed','0','--count','23','--format','json'],capture_output=True,timeout=5)
assert z.returncode!=0 and b'capacity' in z.stderr
report={'passed':True,'repair':'knowledge_point.db_id=17592186064250','record_counts':counts,'source_adapter':'17 source_id values match MA IDs/labels; native fields intact','capacity_guard':{'validated_capacities':g.CAPACITIES,'API_excesses_rejected':4,'easy_count23_CLI':'Rejected within5second timeout'},'CLI':'all E/M/H; JSON and Markdown deterministic; JSON db_id verified','mathematics':'Unchanged from full symbolic sweep recorded in validation.json','generator_sha256':hashlib.sha256(H.with_suffix('.py').read_bytes()).hexdigest()}
(H/'metadata-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
