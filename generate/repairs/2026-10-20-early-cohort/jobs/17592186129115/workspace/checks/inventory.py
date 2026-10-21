"""Inspect captured inventory and attempt old-package replay without publication."""
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
from regressions import W,matrix,coords
E=W/'evidence'
sys.path.insert(0,'/home/jake/Developer/Course_Academy')
from scripts.generator_publish import stable_identities
spec=importlib.util.spec_from_file_location('old_generator',E/'generator-before.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
s=json.loads((W.parent/'source/source.json').read_text());inv=json.loads((W.parent/'source/inventory.json').read_text())
source_ids={q[':question/id'] for q in s['material']['kp'][':knowledge-point/questions']}
attempts=[];records=[]
for q in inv['questions']:
    if q[':question/id'] in source_ids: continue
    p={'matrix':matrix(q[':question/problem']),'bank':[coords(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]}
    r=old.generate('moderate',0,parameters=p)
    normalized=stable_identities(r['question'],old.KP_UUID)
    records.append(r)
    attempts.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding_observed':'fewest replacements' in q[':question/problem'],
      'parameters':p,'metadata_captured':False,'attempt_seed':0,'attempt_id':r['question'][':question/id'],
      'normalized_attempt_id':normalized[':question/id'],'identity_matches':q[':question/id'] in [r['question'][':question/id'],normalized[':question/id']],
      'prompt_matches':r['question'][':question/problem']==q[':question/problem'],
      'solution_matches':r['question'][':question/worked-solution']==q[':question/worked-solution']})
assert len(attempts)==5 and all(a['finding_observed'] for a in attempts)
# Missing original generation metadata prevents certifying identity-bound complete records.
assert not any(a['identity_matches'] for a in attempts)
(E/'inventory-attempt-records.json').write_text(json.dumps(records,indent=2)+'\n')
(E/'inventory-inspection.json').write_text(json.dumps({'basis':inv['basis'],'inspected':len(inv['questions']),'source_originals_excluded':len(source_ids),'non_source_records':attempts,'limitation':'Five stored prompts demonstrate optimization wording, but historical generation metadata is absent and exact identity replay failed. affected-inventory is empty because no matching complete generated record is certified, not because the stored defect is absent.'},indent=2)+'\n')
(E/'generated-records.json').write_text('[]\n')
(W/'affected-inventory.json').write_text('{"affected_questions": []}\n')
print(json.dumps({'inspected':20,'source_originals_excluded':15,'optimization_prompts_observed':5,'certified_identity_replays':0}))
