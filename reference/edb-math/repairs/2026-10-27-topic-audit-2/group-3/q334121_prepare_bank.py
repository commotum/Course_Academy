import collections,json
from pathlib import Path
H=Path(__file__).resolve().parent;D=json.loads((H/'snapshot.json').read_text());q=next(q for q in D['questions']if q[':db/id']==17592186308563);refs=json.loads((H/'q334121-reference-evidence.json').read_text());assert all(rows==[]for rows in refs.values());source=Path('reference/mathacademy/question-capture-workers/differential/14062380/q-334121-before.json');raw=json.loads(source.read_text());repairs=[];duplicates=[];detaches=[]
for f in q[':question/answer-fields']:
 groups=collections.defaultdict(list)
 for a in f[':answer-field/choices']:groups[a[':answer/value']].append(a)
 for value,aa in groups.items():
  if len(aa)>1:duplicates.append({'field':f[':db/id'],'key':f[':answer-field/key'],'correct':f[':answer-field/correct'][':db/id'],'value':value,'answers':aa})
for aid,duplicate,field in [(17592186306650,17592186307410,17592186307984),(17592186305867,17592186306796,17592186308009)]:
 repairs.append({'entity':aid,'attribute':'answer/type','before':17592186045498,'after':17592186045499,'reason':'The retained original select option is mixed prose/text, not a delimiter-free mathematical expression.','evidence':{'question':q[':db/id'],'path':str(source),'historical_task_content_refs':[],'historical_answer_response_refs':[]},'confidence':'high'})
 detaches.append({'operation':'db/retract','entity':field,'attribute':'answer-field/choices','value':duplicate,'reason':'Remove only the unused duplicate bank membership to restore the exact original two-option bank; retain the answer entity and canonical answer ID.','evidence':{'path':str(source),'source_bank_count':2,'before_bank_count':3,'after_bank_count':2,'no_current_or_historical_task_item_content_or_response_refs_at_basis':9122,'answer_entity_retained':True}})
(H/'q334121-type-proposals.json').write_text(json.dumps(repairs,indent=2));(H/'q334121-bank-membership-proposals.json').write_text(json.dumps(detaches,indent=2));(H/'q334121-duplicate-classes.json').write_text(json.dumps({'question':q[':db/id'],'basis_t':9122,'source_expected_fields':len(raw['fields']),'source_field_banks':[{'key':f['key'],'choices':f['choices']}for f in raw['fields']],'duplicate_classes':duplicates,'retained_all_entities':True},indent=2));print('type repairs',len(repairs),'unused membership detach proposals',len(detaches))
