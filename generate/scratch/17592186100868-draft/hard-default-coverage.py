"""Record actual unqualified normal hard default coverage without name/order inflation."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json
from pathlib import Path
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp100868_default_audit',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
byfamily={sid:set() for sid in g.HARD_ROW_GAINS};rows=[];allfp=set()
for seed in range(512):
 r=g.generate_hard(seed);meta=r['generation'];sid=meta['template'];fp=meta['mathematical_fingerprint'];byfamily[sid].add(fp);allfp.add(fp);rows.append({'seed':seed,'template':sid,'row_gains':meta['parameters']['row_gains'],'question_id':r['question'][':question/id'],'mathematical_fingerprint':fp})
expected=json.loads((D/'hard-domain.json').read_text());assert len(allfp)==expected['unqualified_default_distinct_tasks']
report={'status':'pass','public_api':'generate_hard(seed), no explicit template/profile/parameters','seed_count':512,'canonical_distinct':len(allfp),'per_family':{sid:{'reached':len(seen),'complete_domain':len(g.HARD_ROW_GAINS[sid])} for sid,seen in byfamily.items()},'records':rows}
(D/'hard-default-coverage.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='records'})
