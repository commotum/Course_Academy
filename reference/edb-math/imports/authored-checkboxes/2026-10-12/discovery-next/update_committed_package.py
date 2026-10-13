"""Publish the verified commit handoff without changing retained requests or receipts."""
import hashlib,json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_text())
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
summary=read(OUT/'commit-receipt.json');verified=read(OUT/'verification.json');plan=read(OUT/'plan.json')
assert verified['passed']and verified['committed']and summary['solution_corrections']['committed']
assert summary['counts']['questions']==1695 and verified['counts']['new_checkbox_fields']==5178
previews=[];execution=[];qids=set();kps=set();fields=0;answers=0;original=0;responses=0;clarifications=0
for b,receipt in zip(plan['batches'],summary['batches']):
 directory=Path(b['directory']);manifest=read(directory/'plan.json');request=read(directory/'prepared-request.json');preview=read(directory/'preview.json');check=read(directory/'commit-validation.json');capture=read(directory/'capture.json')
 assert digest(directory/'transaction.edn')==manifest['transaction_sha256']==request['sha256']==preview['sha256']==receipt['transaction_sha256']==check['sha256']
 assert capture['basis']==manifest['basis']==request['basis']==receipt['basis_before']==check['basis']
 assert check['passed']and check['committed']and preview['passed']and not preview['committed']
 assert receipt['source']==request['source']==summary['source']
 previews.append({'batch':b['number'],**preview})
 execution.append({'number':b['number'],'basis_before':receipt['basis_before'],'basis_after':receipt['basis_after'],'questions':manifest['counts']['questions'],'source':request['source'],'request_key':request['request_key'],'sha256':request['sha256'],'preview':'batch-%02d/preview.json'%b['number'],'receipt':'batch-%02d/commit-receipt.json'%b['number']})
 for q in manifest['questions']:
  assert q['id']not in qids;qids.add(q['id']);kps.update(k['id']for k in q['kps']);clarifications+=q['required_prompt_clarification']
 fields+=manifest['counts']['new_checkbox_fields'];answers+=manifest['counts']['new_boolean_answers'];original+=len(manifest['retained_original_entities']);responses+=manifest['counts']['saved_responses_mapped']
assert len(qids)==1695 and len(kps)==311 and fields==5178 and answers==10356 and original==10170 and clarifications==8 and 17592186329885 not in qids
solutions=OUT/'optional-solution-repairs';solution_plan=read(solutions/'plan.json');solution_receipt=read(solutions/'commit-receipt.json');solution_request=read(solutions/'prepared-request.json');assert digest(solutions/'transaction.edn')==solution_request['sha256']==solution_receipt['transaction_sha256']==solution_plan['transaction_sha256'];assert read(solutions/'commit-validation.json')['passed']and solution_plan['counts']['questions']==14
aggregate={'passed':True,'committed':False,'speculative':True,'mode':'independent_batch_previews','source':summary['source'],'batches':previews,'database_writes':0,'note':'Each batch was freshly captured, previewed and committed independently. These are not a single speculative chain.'}
(OUT/'preview.json').write_text(json.dumps(aggregate,indent=2)+'\n')
(OUT/'execution-plan.json').write_text(json.dumps({'state':'committed_verified','source':summary['source'],'mode':summary['mode'],'batches':execution,'solution_corrections':solution_receipt,'converted_question_ids':sorted(qids),'knowledge_point_ids':sorted(kps)},indent=2)+'\n')
(OUT/'package-integrity.json').write_text(json.dumps({'passed':True,'committed':True,'basis_before':summary['basis_before'],'basis_after':summary['basis_after'],'source':summary['source'],'main_request_hashes_checked':9,'solution_request_hash_checked':True,'questions':1695,'knowledge_points':311,'checkbox_fields':fields,'boolean_answers':answers,'retained_original_entities':original,'responses_mapped':responses,'necessary_prompt_clarifications':clarifications,'solution_corrections':14,'retained_radio_ids':[17592186329885],'database_writes':10},indent=2)+'\n')
status=read(OUT/'status.json');status.update({'state':'committed_verified','basis':summary['basis_after'],'prepared_cohort_basis':plan['basis'],'basis_before':summary['basis_before'],'basis_after':summary['basis_after'],'database_writes':10,'confirmed_conversions_in_this_tier':1695,'remaining_unresolved_in_scoped_tier':0,'verification':'verification.json','execution_plan':'execution-plan.json','retained_radio_ids':[17592186329885],'optional_solution_repairs':{'questions':14,'committed':True,'receipt':'optional-solution-repairs/commit-receipt.json','basis_after':solution_receipt['basis_after']},'pending_request':None});(OUT/'status.json').write_text(json.dumps(status,indent=2)+'\n')
fixture=read(OUT/'engine-fixture-verification.json');fixture.update({'actual_committed_batches':execution,'response_shapes_and_keys_preserved':True,'concurrent_format_repairs':'fresh-source-overlays.json','source_facts_identical_to_previous':False,'note':'Original grading fixture keys and response shapes retained. Concurrent label/TeX repairs were independently checked and preserved; their prompts differ from the original fixture.'});(OUT/'engine-fixture-verification.json').write_text(json.dumps(fixture,indent=2)+'\n')
text=(OUT/'README.md').read_text();text=text.replace('**Prepared and speculatively verified; nothing submitted.**','**Committed and verified.**');text=text.replace('can be converted. One remains radio.','were converted. One remains radio.');text=text.replace('The nine guarded conversion transactions create','The nine guarded conversion transactions created');text=text.replace('Its entities are excluded from every transaction.','Its entities were excluded from every transaction and read back unchanged.')
start=text.index('The captured database basis is **');end=text.index('\nEach complete question conversion is atomic.',start)
rows='\n'.join(f"| {b['number']} | {b['questions']} | {b['basis_before']} → {b['basis_after']} | [EDN](batch-{b['number']:02d}/transaction.edn) / [receipt](batch-{b['number']:02d}/commit-receipt.json) |"for b in execution)
replacement=f'''The conversions were committed **one batch at a time**: capture the current database, read that group's questions and incoming learner uses, prepare its guarded request, preview it with native validators, submit those exact bytes, and validate the receipt before preparing the next group. Actual conversion bases span **{summary['basis_before']} → {summary['basis_after_conversions']}**; external writes between groups are allowed. The separate correction transaction finished at **{summary['basis_after']}**. Ten database transactions were submitted by this migration.

The [execution plan](execution-plan.json), [commit receipts](commit-receipt.json), and [final readback verification](verification.json) are authoritative. Historical cohort preparations in `plan.json` and archived speculative chains do not override committed receipts.

| Batch | Questions | Confirmed bases | Files |
|---|---:|---|---|
'''+rows
text=text[:start]+replacement+text[end:]
text=text.replace('A separately reviewable transaction corrects **14 definite errors**','A separately submitted and verified transaction corrected **14 definite errors**');text=text.replace('are ready. It is optional relative to the checkbox conversion, but these corrections address established content errors.','were retained alongside its confirmed commit receipt. These corrections address established content errors.');text=text.replace('This correction transaction requires **all nine conversion batches to have been confirmed first**, then basis **1703**; its preview follows the entire conversion chain in memory.',f"The correction transaction was freshly captured and previewed after all nine conversions were confirmed, then committed at **{solution_receipt['basis_before']} → {solution_receipt['basis_after']}**.")
start=text.index('## Resume safely');text=text[:start]+'''## Completion and continuation

[status.json](status.json) records verified completion. The nine batch directories and `optional-solution-repairs/` retain original EDN, exact requests, submission intents, native previews, committed reports and receipts. All 1,695 converted questions and 14 corrected solutions were read back at the final confirmed basis. All 10,170 original field/answer entities and the ordered-completion radio were unchanged. The initial historical snapshot and each batch's independent historical snapshot were reproduced.

Concurrent label and TeX-brace repairs found during refresh were preserved; [fresh-source-overlays.json](fresh-source-overlays.json) records these differences and equivalence checks. No stored key was changed or replaced. Question IDs confirmed here must be excluded from the next audit. Never rebuild or resubmit this cohort under new request keys; recover an existing uncertain request exactly. Candidates outside this keyed/rated tier were not re-audited. Generator source snapshots for the affected KPs may need refreshing separately.
'''
for target in re.findall(r'\]\(([^)]+)\)',text):assert (OUT/target).exists(),target
(OUT/'README.md').write_text(text)
print(json.dumps({'handoff_updated':True,'committed':True,'basis_after':summary['basis_after'],'questions':1695,'solution_corrections':14,'retained_radio':17592186329885}))
