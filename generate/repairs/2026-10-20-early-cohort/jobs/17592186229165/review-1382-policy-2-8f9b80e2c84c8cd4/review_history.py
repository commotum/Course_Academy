from independent_lib import *
P=JOB/'review-1-policy-2-48d685555902faba'
spec=importlib.util.spec_from_file_location('contract',REPO/'scripts/generator_review.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
# Reproduce old review-contract error read-only. All referenced old evidence remains intact.
try:c.validate_review(load(P/'review-result.json'),P)
except ValueError as e: prior_error=str(e)
else:prior_error=None
assert prior_error=='decision_variation has an unresolved decision shortcut',prior_error
inv=load(JOB/'source/inventory.json'); old=load(ROOT/'generated-records.json');rows=[]
for r in old:
 q=next(q for q in inv['questions'] if q[':question/id']==r['question'][':question/id'])
 rows.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'generation':r['generation'],'retired':q.get(':question/retired',False),'prior_mixed_weakness':r['generation']['template']=='mixed','eligible':not q.get(':question/retired',False),'record_evidence':'generated-records.json'})
assert sum(q['retired'] and q['prior_mixed_weakness'] for q in rows)==4
assert not any(q['prior_mixed_weakness'] and q['eligible'] for q in rows)
save('inventory-eligibility.json',{'basis':inv['basis'],'stored_count':len(inv['questions']),'reproduced_generated_records':rows,'affected_eligible_questions':0,'source_originals_not_relabelled':True,'actual_rule':'engine/rust/learning.rs:149 validate_practice_question rejects question/retired=true; practice candidate paths at lines 600,1580,1674 invoke this before question_selection::select','selection_rule':'Sorted unique fresh usable candidates; weighted difficulty bands and uniform within band; replay/history not modified','limits':'Captured basis only; no live history or future inventory claims.'})
before=subprocess.run([sys.executable,str(ROOT/'test_role_exchange.py'),str(JOB/'workspace/evidence/generator-before.py')],capture_output=True,text=True)
after=subprocess.run([sys.executable,str(ROOT/'test_role_exchange.py')],capture_output=True,text=True)
assert before.returncode!=0 and 'Mixed requires first component resonant' in before.stderr
assert after.returncode==0
save('retained-finding-results.json',{'runtime_finding':'efa97df560cec8fee6e1','before_exit':before.returncode,'before_stderr':before.stderr,'current_exit':after.returncode,'current_stdout':after.stdout,'retained_author_check_current':load(ROOT/'retained-current/results.json'),'independent_checks':'targeted.py and hard-math-results.json','report_finding':'645672a4cd3f9bf609ca','old_contract_error_reproduced':prior_error,'current_resolution':'New independent report under current writable evidence_root supersedes obsolete old-report installation requirement. Current inventory excludes the prior affected cohort. Original review and package were not edited.','preflight_reviewed':True,'report_regression_inspected':'check_report_installation.py tests the stale previous destination and writes workspace evidence; not executed because writes there are forbidden. Its actual failing contract dependency was independently executed read-only. Current report contract will be tested here.'})
# Snapshot cited selection code, with provenance rather than assuming previous engine binding.
save('selection-code.json',{'question_selection_sha256':hashlib.sha256((REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'practice_filter_sha256':hashlib.sha256((REPO/'engine/rust/learning.rs').read_bytes()).hexdigest(),'practice_filter_excerpt':'\n'.join((REPO/'engine/rust/learning.rs').read_text().splitlines()[145:155]),'select_excerpt':'\n'.join((REPO/'engine/rust/question_selection.rs').read_text().splitlines()[121:200])})
(ROOT/'session-state.md').write_text('Source replay 15/15 and 40 math regressions pass. 37 hard records pass independent worked-stage checks; 24 fresh mixed are 12/12 by resonant position. Delivered batch 5/5, hard 37/37. Native grading 211 expectations pass. Four historical mixed questions exactly reproduced but retired at basis 5573, hence no eligible inventory defect. Completing actual-UI screenshot inspection and final evidence contract.\n')
