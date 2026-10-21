#!/usr/bin/env python3
"""Reconstruct historical complete records from source and archived generation parameters.

No stored question content is copied into the reconstructed question. IDs and metadata
come from original archived generated records; source templates supply prose/TeX,
previous independently archived executable supplies the numerical bank, and archived UUIDs are restored by
exact answer value. Compare the complete reconstructed record to captured inventory.
"""
import sys
sys.dont_write_bytecode=True
import copy,re
import review as audit
audit.g=audit.load(audit.PREV/'relocated-package/17592186059768.py','historical_generator')
sys.path.insert(0,str(audit.REPO))
from scripts.generator_publish import normalized_question
source={q[':question/math-academy-id']:q for q in audit.read(audit.JOB/'source/source.json')['material']['kp'][':knowledge-point/questions']}
inv=audit.read(audit.JOB/'source/inventory.json');stored={q[':question/id']:q for q in inv['questions']}
archive=audit.read(audit.PKG/'17592186059768/reference/replenishment/basis-2204/generated.json')
records=[];results=[]
for original in archive:
 meta=original['generation'];name=meta['template'];params=meta['parameters'];src=source[name]
 level=src[':question/difficulty'][':db/ident'].split('/')[-1]
 replay=audit.g.generate(level,meta['seed'],profile=name,parameters=params)
 raw_current_id=replay['question'][':question/id']
 q=replay['question'];q[':question/id']=original['question'][':question/id']
 for key in [':question/problem',':question/worked-solution']:
  q[key]=re.sub(r'\d+',lambda m:str(params.get(m[0],int(m[0]))),src[key])
 f=audit.field(replay);oldfield=audit.field(original);oldmap={a[':answer/value']:a[':answer/id'] for a in oldfield[':answer-field/choices']}
 assert {a[':answer/value'] for a in f[':answer-field/choices']}==set(oldmap)
 new_correct=audit.correct_id(f)
 correct_value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==new_correct)
 for a in f[':answer-field/choices']:a[':answer/id']=oldmap[a[':answer/value']]
 f[':answer-field/id']=oldfield[':answer-field/id'];f[':answer-field/correct']=[':answer/id',oldmap[correct_value]]
 assert audit.correct_id(f)==audit.correct_id(oldfield)
 replay['generation']=copy.deepcopy(meta)
 captured=stored[q[':question/id']]
 # This comparison includes exact prompt, exact worked solution, every answer value,
 # all IDs, field contract and correct designation. Bank order is a Pull set.
 assert normalized_question(q)==normalized_question(captured)
 audit.check_math(replay)
 replay['inventory_reproduction']={'entity_id':captured[':db/id'],'generation_metadata':'Exact metadata recovered from original archived generated.json by UUID','construction':'Original source prompt/solution literal substitution at archived parameters; previous independently archived executable matrix bank; historical UUIDs restored by exact value correspondence, no stored content copied','historical_replay_raw_id':raw_current_id,'complete_stored_question_match':True,'formatting':'Historical source display-dollar whitespace retained; current generator normalizes whitespace differently for q-1051/q-1052'}
 records.append(replay)
 results.append({'question_id':q[':question/id'],'entity_id':captured[':db/id'],'template':name,'seed':meta['seed'],'parameters':params,'complete_content_and_identity_match':True})
audit.save('generated-records.json',records)
audit.save('inventory-reproduction-results.json',{'command':str(audit.PY)+' -B reproduce_inventory.py','inventory_basis':inv['basis'],'reproduced':results,'generated_count':len(records),'original_source_records_not_generated':len(inv['questions'])-len(records),'comparison':'publisher.normalized_question(identity=True), including full prose/TeX and complete bank, disregarding only Pull bank order and database IDs'})
print('Exactly reconstructed',len(records),'complete historical generated records from original source and archived parameters; all content and identities match stored records.')
