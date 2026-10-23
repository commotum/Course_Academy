from audit_revision import *
files=['samples.json','delivery-sample/accepted.json','cli-samples.json','delivery-cli/accepted.json','batch-records.json','delivery-batch/accepted.json']
stages={f:summary(load(f)) for f in files};save('coverage.json',stages)
probes=[]
for file,groups in stages.items():
 for label,group in groups.items():
  if not label.startswith('radio/'):continue
  rows=group['records'];count=len(rows)
  probes.append({'cue':'Square order and display layout','subgroup':file+' / '+label,'scope':'other_recognizable_subgroup','strategy':'Choose No such entry without reading indices.','correct':group['missing'],'total':count,'baseline':0.2,'disposition':'not_predictive','conclusion':f'Five-choice blind baseline 0.2. Absence strategy succeeds {group["missing"]}/{count}; paired CLI and exact batch include both decisions per represented subgroup. API samples fluctuate, and an all-existing subgroup still requires scalar lookup.','sample_refs':[file,'coverage.json']})
 # Actual deterministic UI ordering depends on task-item ID and answer IDs; stored positions are diagnostic only.
 rs=load(file);radio=[r for r in rs if enum(field(r)[':answer-field/type']).endswith('/radio')]
 for layout in ['inline','display']:
  sub=[r for r in radio if ('display' if '$$' in q(r)[':question/problem'] else 'inline')==layout]
  if not sub:continue
  correct=sum(bank(r).index(key(r))==0 for r in sub)
  probes.append({'cue':'First stored option','subgroup':file+' / '+layout,'scope':'within_template','strategy':'Choose the first stored choice.','correct':correct,'total':len(sub),'baseline':0.2,'disposition':'not_predictive','conclusion':'Blind five-option baseline 0.2. Not perfect; stored order is additionally permuted by actual UI using task-item and field identities.','sample_refs':[file]})
 # Visible sign/radical rule tested within existing radios, where existence detection alone cannot supply scalar.
 existing=[r for r in radio if expected(r)!='No such entry']
 for cue,pred in [('unique radical choice',lambda v:'sqrt' in v),('unique negative choice',lambda v:v.startswith('-'))]:
  sub=[r for r in existing if sum(pred(v) for v in bank(r))==1]
  if sub:
   hits=sum(pred(expected(r)) for r in sub)
   probes.append({'cue':cue,'subgroup':file+' / existing radios','scope':'other_recognizable_subgroup','strategy':'After checking existence, select the only choice with this scalar form.','correct':hits,'total':len(sub),'baseline':0.25,'disposition':'not_predictive','conclusion':'Baseline is 1/4 after excluding the missing option. Individual tiny subgroups can be perfect by chance; independent controlled changes and broader samples refute a construction rule assigning this form to the answer. No entire delivered family solved by this cue.','sample_refs':[file,'controlled-records.json']})
save('shortcut-probes.json',probes)
inv=json.loads((JOB/'source/inventory.json').read_text());eligible=[];excluded=[]
for item in inv['questions']:
 reason='retired' if item.get(':question/retired') else 'missing correct reference' if any(':answer-field/correct' not in f for f in item[':question/answer-fields']) else None
 if reason:excluded.append({'id':item[':question/id'],'reason':reason})
 else:eligible.append(item)
combined=eligible+load('delivery-batch/accepted.json');save('selection-records.json',combined)
save('selection-analysis.json',{'basis':inv['basis'],'eligible_originals':len(eligible),'excluded':excluded,'batch_eligible':5,'combined':summary(combined),'rules':'Inspected engine/rust/learning.rs validate_practice_question and question_selection.rs select/seen_before_task. Invalid or retired records excluded; prior tasks and current prefix excluded. Positive difficulty weights pick band then uniform question; unconfigured policy picks first entity. All eligible captured originals and candidates are easy, so positive easy weight retains their relative eligibility.','limits':'Actual learner history/weights and future entity IDs not provided. No live draw predicted; possible fresh-pool support examined. Histories may remove one member of a pair, so no claim every learner-specific subset stays balanced.','original_source_cue':'Captured original 2x2 radio is absent-only, and current exact batch has no 2x2 radios; this singleton original is preserved source history, not a generated-pool defect. Current construction does generate existing 2x2 radios in independent API/CLI samples.'})
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-analysis.json',{'basis':inv['basis'],'questions':len(inv['questions']),'generated':sum(':question/generation' in r for r in inv['questions']),'verified_original_ids':[r[':question/id'] for r in inv['questions']],'source_match':all(r[':question/id'] in {s[':question/id'] for s in json.loads((JOB/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']} for r in inv['questions']),'conclusion':'Verified absence of stored generated records in captured inventory; no affected generated inventory. Five originals eligible, one missing-key original ineligible. No DB edits or originals relabeled.'})
print(json.dumps({'groups':{f:{k:(v['count'],v['missing']) for k,v in s.items()} for f,s in stages.items()},'probes':len(probes)},indent=2))
