"""Offline integrity checks and handoff for an unsubmitted refreshed preparation."""
import hashlib,json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent
read=lambda path:json.loads(path.read_text())
digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
plan=read(OUT/'plan.json');preview=read(OUT/'preview.json');snapshot=read(OUT/'snapshot.json');repairs=read(OUT/'optional-solution-repairs/plan.json');repair_preview=read(OUT/'optional-solution-repairs/preview.json')
basis=plan['basis'];prior=OUT/'superseded-preparations/basis-1693';prior_plan=read(prior/'plan.json')
assert basis==1694 and prior_plan['basis']==1693
assert read(prior/'snapshot.json')['questions']==snapshot['questions'],'Source facts changed: re-review required'
assert not snapshot['items']and not snapshot['response_users']
assert digest(OUT/'snapshot.edn')==plan['snapshot_sha256']
assert preview['passed']and not preview['committed']and preview['captured_basis']==basis
assert repair_preview['passed']and not repair_preview['committed']and repairs['basis']==basis+9
assert repair_preview['basis']==repairs['basis']and repairs['counts']['questions']==14
assert not list(OUT.glob('batch-*/commit*'))and not list((OUT/'optional-solution-repairs').glob('commit*'))and not (OUT/'commit-intent.json').exists()
for row in plan['review_files']:assert digest(Path(row['path']))==row['sha256']
converted=set();old_choices=0;fields=0
for b in plan['batches']:
 directory=Path(b['directory']);manifest=read(directory/'plan.json');request=read(directory/'prepared-request.json');result=read(directory/'preview.json')
 assert digest(directory/'transaction.edn')==b['sha256']==manifest['transaction_sha256']==request['sha256']==result['sha256']
 assert request['basis']==b['basis_guard']==manifest['basis']==result['basis']==basis+b['number']-1
 assert result['passed']and not result['committed']and result['source']==request['source']==plan['source']
 assert request['must_use_basis_guard']
 previous=prior/f"batch-{b['number']:02d}"
 assert manifest['questions']==read(previous/'plan.json')['questions']
 assert digest(directory/'transaction.edn')==digest(previous/'transaction.edn')
 for q in manifest['questions']:
  assert q['id']not in converted;converted.add(q['id']);old_choices+=len(q['choice_mapping']);fields+=len(q['labels'])
assert len(converted)==1695 and fields==5178 and old_choices==8475 and 17592186329885 not in converted
assert plan['retained_original_entities']==10170
for name in ['engine-input.json','engine-report.json']:
 assert digest(OUT/name)==digest(prior/name)
fixture=read(OUT/'engine-fixture-verification.json')
assert digest(OUT/'engine-input.json')==fixture['engine_input_sha256']
assert digest(OUT/'engine-report.json')==fixture['engine_report_sha256']
fixture.update({'prepared_basis':basis,'previous_verified_basis':1693,'source_facts_identical_to_previous':True,'logical_forms_identical_to_previous':True,'transaction_hashes_checked':9})
(OUT/'engine-fixture-verification.json').write_text(json.dumps(fixture,indent=2)+'\n')
repair_request=read(OUT/'optional-solution-repairs/prepared-request.json')
assert digest(OUT/'optional-solution-repairs/transaction.edn')==repairs['transaction_sha256']==repair_request['sha256']==repair_preview['sha256']
assert repair_request['basis']==repairs['basis']and repair_request['requires_all_conversion_batches_first']
assert repairs['changes_correct_keys']is False
qs={q[':db/id']:q for q, in snapshot['questions']}
assert len({q['id']for q in repairs['questions']})==14
for q in repairs['questions']:assert q['id']in converted and qs[q['id']][':question/worked-solution']==q['solution_before']and q['solution_after']!=q['solution_before']
ledger=read(OUT/'resolutions.json');repair_ids={q['id']for q in repairs['questions']}
assert len(ledger['questions'])==1696
for q in ledger['questions']:
 q['preview_status']=f'passed_at_basis_{basis}'if q['id']in converted else'not_applicable_retained_radio'
 q['commit_status']='not_submitted'if q['id']in converted else'not_planned_retained_radio'
 if q['id']in repair_ids:q['separate_solution_repair']='optional-solution-repairs/plan.json'
ledger['state']='resolved_prepared_previewed_not_submitted';ledger['database_writes']=0
(OUT/'resolutions.json').write_text(json.dumps(ledger,indent=2)+'\n')
proposals=read(OUT/'proposed-content-repairs.json')
for repair in read(OUT/'reviews/image-solution-repairs.json')['questions']:
 if not any(issue.get('id')==repair['id']and issue.get('evidence')=='reviews/image-solution-repairs.json'for issue in proposals['issues']):
  proposals['issues'].append({'id':repair['id'],'ma_id':repair['ma_id'],'evidence':'reviews/image-solution-repairs.json','solution_before':repair['before'],'solution_after':repair['after'],'reason':repair['reason'],'included_in_checkbox_transaction':False,'separate_solution_repair':'optional-solution-repairs/plan.json'})
(OUT/'proposed-content-repairs.json').write_text(json.dumps(proposals,indent=2)+'\n')
status=read(OUT/'status.json');status.update({'breakdown':'README.md','native_grading_passed':True,'engine_report':'engine-report.json','engine_fixture_verification':'engine-fixture-verification.json','optional_solution_repairs':{'questions':14,'plan':'optional-solution-repairs/plan.json','preview':'optional-solution-repairs/preview.json','basis_guard':basis+9,'requires_all_conversion_batches_first':True,'submitted':False},'retained_radio_ids':[17592186329885],'confirmed_conversions_in_this_tier':0,'review_models':{'model':'gpt-6.1-sol','reasoning':'high','agents':3},'remaining_unresolved_in_scoped_tier':0,'canonical_examples_in_scoped_tier':0,'live_basis_last_checked':basis,'needs_refresh_before_submission':False,'freshness_note':'Last held native capture, not a lock on current database state.'})
(OUT/'status.json').write_text(json.dumps(status,indent=2)+'\n')
(OUT/'last-live-basis.json').write_text(json.dumps({'basis':basis,'prepared_basis':basis,'requires_refresh':False,'evidence':'held-preview.log','note':'Last native capture is not a lock on live state. Recheck before submission.','database_writes':0},indent=2)+'\n')
readme=(OUT/'README.md').read_text();readme=readme.replace('captured database basis is **1693**','captured database basis is **1694**').replace('predicted final basis is **1702**','predicted final basis is **1703**').replace('then basis **1702**','then basis **1703**')
readme=readme.replace('A prior external write advanced 1692 to 1693 during preparation; the refreshed scoped question facts were identical, and the guards were rebuilt before preview.','External writes advanced the basis from 1692 to 1693 and then 1694 during preparation. All scoped question facts were identical on each refresh. The nine guards and optional repair guard were rebuilt and natively previewed at 1694; the complete unsubmitted 1693 package is archived in `superseded-preparations/basis-1693/`.')
for b in plan['batches']:
 n=b['number'];readme=re.sub(rf'\| {n} \| {b["questions"]} \| \d+ \|',f'| {n} | {b["questions"]} | {b["basis_guard"]} |',readme)
for target in re.findall(r'\]\(([^)]+)\)',readme):assert (OUT/target).exists(),target
(OUT/'README.md').write_text(readme)
result={'passed':True,'prepared_basis':basis,'database_writes':0,'questions_reviewed':1696,'questions_prepared':1695,'retained_radio':1,'main_request_hashes_checked':9,'original_choices_checked':old_choices,'checkbox_fields':fields,'optional_solution_repairs':14,'source_facts_unchanged_from_1693':True,'native_fixture_and_forms_unchanged':True,'review_hashes_checked':len(plan['review_files']),'markdown_links_checked':True,'committed':False}
(OUT/'package-integrity.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
