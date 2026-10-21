from checks import *

def measure(records):
 positions=collections.Counter();signs=collections.Counter();profiles={};math=[]
 for r in records:
  q=r['question'];opts=q[':question/answer-fields'][0][':answer-field/choices'];correct=key(q);position=next(i for i,a in enumerate(opts) if a[':answer/id']==correct);positions[position]+=1
  V,q0,c,rate,_=params(q);sign='increasing' if q0<V*c else 'decreasing';signs[sign]+=1
  assert shortcut(q) is None
  for group in ('all','context:'+r['generation']['parameters']['context'],'sign:'+sign):
   row=profiles.setdefault(group,{'total':0,'shortcut_correct':0,'positions':collections.Counter()});row['total']+=1;row['positions'][position]+=1
  math.append(visible_math(r))
 assert len(positions)==5 and len(signs)==2
 return {'count':len(records),'positions':dict(positions),'signs':dict(signs),'groups':profiles,'math_passed':len(math),'reported_shortcut_correct':0}
raw=json.loads((EVIDENCE/'samples.json').read_text());delivered=json.loads((EVIDENCE/'delivery/accepted.json').read_text());cf=json.loads((EVIDENCE/'delivery-counterfactual/accepted.json').read_text());batch=json.loads((EVIDENCE/'delivery-batch/accepted.json').read_text())
assert len(raw)==len(delivered)==30 and len(cf)==35 and len(batch)==5
report={'raw':measure(raw),'accepted':measure(delivered),'controlled':measure(cf),'batch':{'count':5,'reported_shortcut_correct':sum(shortcut(r['question'])==key(r['question']) for r in batch)},'passed':True}
# Same visible bank, all five keys after normalization, per recognizable context.
for context in sorted({r['generation']['parameters']['context'] for r in cf}):
 rs=[r for r in cf if r['generation']['parameters']['context']==context]
 banks=[tuple(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']) for r in rs]
 cv=[next(a[':answer/value'] for a in r['question'][':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']==key(r['question'])) for r in rs]
 assert len(rs)==5 and len(set(banks))==1 and len(set(cv))==5
save('delivery-analysis.json',report)
cases=[]
for rec in batch+cf[:5]:
 truth=visible_math(rec)['truth'];cases.append({'label':rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==truth else 'rejected','purpose':'delivery-normalized record, independent oracle'} for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]})
save('grader-delivery-input.json',cases)
# Captured stored records: inspect the known weakness only; never infer generator origin.
inventory=json.loads((ROOT.parent/'source/inventory.json').read_text());audit=[];affected=[];source_ids={q[':question/id'] for q in json.loads((ROOT.parent/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']}
for q in inventory['questions']:
 applicable=q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'].startswith('Q(t)')
 hit=shortcut(q) if applicable else None
 audit.append({'id':q[':question/id'],'entity_id':q[':db/id'],'captured_source':q[':question/id'] in source_ids,'applicable_expression_bank':applicable,'shortcut_matches':bool(hit and hit==key(q)),'generation_metadata_present':any('generation' in k for k in q)})
 assert not (hit and hit==key(q)),'stored affected record requires exact provenance reproduction'
save('inventory-audit.json',{'basis':inventory['basis'],'total':len(audit),'applicable_tested':sum(r['applicable_expression_bank'] for r in audit),'not_applicable_numeric':sum(not r['applicable_expression_bank'] for r in audit),'untested_applicable':0,'cases':audit,'scope':'No stored expression bank exhibits the demonstrated two/four intersection. Numeric records have no expression-bank witness. Replay API failure is not a stored-question content defect. No original source question is classified as generated. This is absence of the two retained defects in their applicable stored content, not a universal shortcut audit.'})
(ROOT/'affected-inventory.json').write_text(json.dumps({'affected_questions':affected},indent=2)+'\n')
print(json.dumps({'raw':30,'delivered':30,'controlled':35,'batch':5,'stored_applicable':sum(r['applicable_expression_bank'] for r in audit),'affected':0,'passed':True}))
