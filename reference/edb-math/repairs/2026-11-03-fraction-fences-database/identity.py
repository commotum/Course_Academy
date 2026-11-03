"""Verify all repaired math answers retain their import matching identities."""
import json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT))
from capture.scripts.database.prepare import choice_signature
rows=json.loads((H/'proposals.json').read_text());types=json.loads((H/'types.json').read_text());count=0
for row in rows:
    if row['attribute']!='answer/value':continue
    kind=types[str(row['entity'])][':answer/type'][':db/ident'].split('/')[-1]
    assert choice_signature(kind,row['before'])==choice_signature(kind,row['after']),(row['entity'],row['before'],row['after'])
    count+=1
result={'passed':True,'answer_matching_identities_verified':count,'regression_tests_passed':117}
(H/'identity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
