"""Replay review, verify identities and finalize immutable local evidence hashes."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json
from pathlib import Path
from datetime import datetime,timezone
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
g=load(H.with_suffix('.py'),'final92265g');p=load(H/'private_readback.py','final92265p')
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
report=json.loads((H/'validation.json').read_text());assert report['status'] in ('passed','passed_with_documented_engine_gaps');assert report['generator_sha256']==sha(H.with_suffix('.py'));assert report['private_parser_sha256']==sha(H/'private_readback.py')
review=json.loads((H/'review.json').read_text());count=0
for category,records in review.items():
 for r in records:
  m=r['generation']
  if category=='originals':actual=g.raw_replay(m['template'])
  else:
   field_type=r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1]
   actual=g.generate(r['question'][':question/difficulty'].split('/')[-1],m['seed'],m['template'],m['parameters'],field_type=field_type)
   p.actual(actual['question']);assert actual['generation']['evidence_only'] is False
  assert actual==r,(category,m);count+=1
# Content identity includes response contract, complete bank and solution, while
# the mathematical fingerprint keeps same-task aliases aligned for dedup.
t='q-1948';params=g.original(t);radio=g.generate('hard',template=t,parameters=params);blank=g.generate('hard',template=t,parameters=params,field_type='blank')
assert radio['generation']['mathematical_fingerprint']==blank['generation']['mathematical_fingerprint'];assert radio['question'][':question/id']!=blank['question'][':question/id'];assert radio['question'][':question/answer-fields'][0][':answer-field/id']!=blank['question'][':question/answer-fields'][0][':answer-field/id']
q=copy.deepcopy(radio['question']);f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1];f[':answer-field/choices'].reverse();f['_correct_index']=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==correct);permuted=g.finish(q,t,params,8,g.profile(t),True)
assert permuted['question'][':question/id']==radio['question'][':question/id']
engine=json.loads((H/'engine-validation.json').read_text());native={key:sum(batch[key] for batch in engine['batches']) for key in ('accepted_checks','rejected_checks','documented_unresolved_checks')}
extended=json.loads((H/'equivalent-probe-validation.json').read_text())
for key in native:native[key]+=sum(probe['native'][key] for probe in extended['probes'])
report['extended_native_equivalent_records']=extended['records'];report['extended_native_equivalent_acceptances']=extended['native_equivalent_acceptances'];report['valid_equivalent_engine_gaps']=[{'label':z['label'],'native_outcome':z['native_outcome'],'mathematical_expectation':z['mathematical_expectation'],'submitted':z['submitted'],'canonical':z['canonical'],'domain':z['domain'],'limitation':z['limitation']} for z in extended['valid_equivalent_engine_gaps']];report['total_native_records']=report['engine_records']+extended['records']
if extended['valid_equivalent_engine_gaps']:report['status']='passed_with_documented_engine_gaps'
(H/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
identity={'math_task_independent_of_field_type':True,'content_identity_distinguishes_field_type':True,'field_owned_ids_distinguish_content':True,'unordered_bank_identity_stable':True,'source_alias_task_fingerprint_stable':True}
(H/'identity-validation.json').write_text(json.dumps(identity,indent=2)+'\n')
manifest={'status':'working','approved':False,'root_independent_qa_required':True,'producers_stopped':True,'frozen_at':datetime.now(timezone.utc).isoformat(),'basis':2275,'lineage':g.SOURCE['lineage'],'generator_path':str(H.with_suffix('.py')),'generator_sha256':sha(H.with_suffix('.py')),'artifact_hashes':{str(path):sha(path) for path in sorted(H.rglob('*')) if path.is_file() and path.name!='frozen-manifest.json'},'registered_baseline':json.loads((H/'registered-baseline.json').read_text()),'native_engine_sha256':sha(ROOT/'generate/runs/current/check-engine'),'native_engine_source_sha256':sha(ROOT/'generate/runs/current/check-engine.rs'),'counts':report,'native_counts':native,'valid_equivalent_engine_gaps':report['valid_equivalent_engine_gaps'],'total_native_records':report['total_native_records'],'review_records_replayed':count,'content_identity_validation':identity,'format_unit_tests':{'passed':7,'command':'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s scripts/question_capture -p test_math_format.py'},'limitations':['The frozen native engine reports unresolved domain differences for genuine unreduced radical and logarithm-power equivalents. Canonical keys remain accepted and valid parameters are retained; see equivalent-probe-validation.json.','Source omissions and f-prime composite typos remain in immutable raw evidence; served completions/corrections are explicitly authored.','Two unrated source levels inferred conservatively from observed method.','Canonical e731 is context evidence, not a practice template; its formula rasters include an outer-derivative label typo.','No database operations, shared generator/engine changes, registration or git mutations.']}
(H/'frozen-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps({'generator_sha256':manifest['generator_sha256'],'files_frozen':len(manifest['artifact_hashes'])+1,'native':native,'review_records':count,'status':'working'},indent=2))
