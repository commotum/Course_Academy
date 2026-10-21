"""Resolve missing visible empty-subset answers from original database evidence."""
from audit import *
if __name__=='__main__':
 current={q[':db/id']:q for q in json.loads((HERE/'current.json').read_text())}
 candidates={q['id']:q for q in json.loads((HERE/'source-candidates.json').read_text())}
 for original in json.loads((HERE/'extra-originals.json').read_text()):
  qid=original[':db/id'];choices=[(f,a)for f in original[':question/answer-fields']for a in f[':answer-field/choices']if re.search(r'\bnone\b',a[':answer/value'],re.I)]
  assert len(choices)==1
  f,a=choices[0];candidates[qid]={'id':qid,'path':str(HERE/'originals.json'),'source_basis':1100,'source_field':f[':db/id'],'none':[{'old_answer':a[':db/id'],'old_value':a[':answer/value'],'selected':[]}],'row':{'ma_id':original[':question/math-academy-id']}}
 proof_ids=set()
 for c in candidates.values():
  row=c['row'];ids=row.get('old_fields',[row.get('old_field',c.get('source_field'))]);assert None not in ids
  c['source_fields']=ids;proof_ids.update(ids)
 # Include the explicit None field which was separately detached in the initial migration.
 old=native(HERE/'initial-original',1000,[('question',QUESTION,[17592186234490])])['question'][0]
 save(HERE/'initial-original.json',old)
 none=[(f,a)for f in old.get(':question/answer-fields',[])for a in f.get(':answer-field/choices',[])if re.search(r'\bnone\b',a.get(':answer/value',''),re.I)]
 print('initial source',[(f[':db/id'],a[':answer/value'])for f,a in none])
 if none:
  assert len(none)==1;f,a=none[0];candidates[old[':db/id']]={'id':old[':db/id'],'path':str(HERE/'initial-original.json'),'source_basis':1000,'source_fields':[f[':db/id']],'none':[{'old_answer':a[':db/id'],'old_value':a[':answer/value'],'selected':[]}],'row':{'ma_id':old[':question/math-academy-id']}};proof_ids.add(f[':db/id'])
 identity=DB.status();proof=pull_many('source-proof',proof_ids,identity['basis'],'''[* {:answer-field/type [:db/id :db/ident]} {:answer-field/correct [*]} {[:answer-field/choices :limit nil] [*]}]''')
 save(HERE/'source-proof.json',proof);byid={f[':db/id']:f for f in proof};resolved=[]
 for qid,c in sorted(candidates.items()):
  q=current[qid];fields=q[':question/answer-fields'];assert all(f[':answer-field/type'][':db/ident']==':answer-field.type/checkbox'for f in fields)
  assert len({m['old_value']for m in c['none']})==1;c0=c['none'][0]
  source=[(f,a)for fid in c['source_fields']for f in [byid[fid]]for a in f.get(':answer-field/choices',[])if a[':db/id']==c0['old_answer']]
  assert len(source)==1;f,a=source[0];assert a[':answer/value']==c0['old_value']
  assert f[':answer-field/type'][':db/ident']==':answer-field.type/radio',qid
  key='None of the above'if re.search(r'\bnone\b',a[':answer/value'],re.I)else a[':answer/value']
  assert key not in {f[':answer-field/key']for f in fields}
  correct=not any(f[':answer-field/correct'][':answer/value']=='true'for f in fields)
  if 'correct'in c['row']:assert correct==(not c['row']['correct']),qid
  # Some original keys were absent and independently repaired; retain current verified keys.
  if f.get(':answer-field/correct'):assert correct==(f[':answer-field/correct'][':db/id']in {m['old_answer']for m in c['none']}),(qid,'source key mismatch')
  resolved.append({'id':qid,'ma_id':q[':question/math-academy-id'],'source_evidence':c['path'],'source_fields':c['source_fields'],'source_none_answer':a[':db/id'],'source_none_value':a[':answer/value'],'key':key,'none_correct':correct,'prior_choice_mapping':c['row'].get('choice_mapping',[]),'reuse_field':17592186408178 if qid==17592186234490 else None})
 save(HERE/'resolutions.json',resolved)
 print(json.dumps({'resolved':len(resolved),'none_correct':sum(r['none_correct']for r in resolved),'other_no_options':sum(r['key']!='None of the above'for r in resolved),'basis':identity['basis']}))
