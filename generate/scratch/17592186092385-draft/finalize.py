"""Confirm review replay and registered baseline, then freeze working draft evidence."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,hashlib
from pathlib import Path
from datetime import datetime,timezone
H=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v',H/'validate.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
report=json.loads((H/'validation.json').read_text());assert report['status']=='pass';base=v.baseline();assert base==report['registered_baseline']
assert hashlib.sha256((H/'private_readback.py').read_bytes()).hexdigest()==report['private_parser_sha256']
review=json.loads((H/'review.json').read_text());count=0
for r in review['originals']+review['served_replays']+review['normal_examples']+review['source_bank_examples']:
 m=r['generation']
 if m['profile'] in ('observed_raw','observed_served'):current=v.g.source_replay(m['template'],m['profile'])
 else:
  level=r['question'][':question/difficulty'].split('/')[-1];ft=r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1]
  current=v.g.generate(level,m['seed'],m['template'],m['parameters'],m['profile'],ft)
 assert current==r,'Public review replay changed';count+=1
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
producers=[H.with_suffix('.py'),H/'private_readback.py',H/'validate.py',H/'build_docs.py',H/'finalize.py']
manifest={'status':'working','approved':False,'root_independent_qa_required':True,'frozen_at':datetime.now(timezone.utc).isoformat(),'producers_stopped':True,'database':'math','basis':2275,'lineage':v.g.SOURCE['lineage'],'registered_baseline':base,'producer_hashes':{str(p):sha(p) for p in producers},'artifact_hashes':{str(p):sha(p) for p in sorted(H.rglob('*')) if p.is_file() and p.name!='frozen-manifest.json'},'shared_math_format_sha256':sha(Path('scripts/question_capture/math_format.py')),'native_engine_sha256':sha(Path('generate/runs/current/check-engine')),'native_engine_source_sha256':sha(Path('generate/runs/current/check-engine.rs')),'counts':report,'public_review_records_replayed':count,'limitations':['Zero original hard practice; canonical same-method hard extension is conservative and not difficulty-calibrated','q-10878/q-71542 remain raw-only because source answer fields are absent','q-342222 served replay adds only missing answer/correct records for captured blank fields','Radio-bank exclusions for duplicate/correct distractors are explicitly listed; equivalent mathematical tasks remain available as blanks','No DB writes, registration, commits or shared QA edits']}
(H/'frozen-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'generator_sha256':sha(H.with_suffix('.py')),'private_parser_sha256':sha(H/'private_readback.py'),'counts':{k:report[k] for k in ('ma_originals','ma_exact_prompts','ma_exact_solutions','ma_answer_values','non_ma_inventory','normal_records','distinct_normal_math_tasks','source_bank_variants','native_records','native')},'baseline':base,'review_records':count,'status':'working'},indent=2))
