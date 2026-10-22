import collections,hashlib,itertools,json,pathlib,subprocess,sys
sys.dont_write_bytecode=True
from audit import E,P,REPO,visible,summary,native,correct,save,hashes
raw=json.load(open(E/'samples.json'));survivors=json.load(open(E/'delivery-samples/accepted.json'));batch=json.load(open(E/'delivery-batch/accepted.json'));pairs=json.load(open(E/'delivery-counterfactual/accepted.json'))
def cue(r):
 fs=r['question'][':question/answer-fields']
 return all((correct(f)=='true')==('invertible' in f[':answer-field/key']) for f in fs)
def subgroup(rows):return [r for r in rows if len(r['question'][':question/answer-fields'])==3]
for r in survivors+batch+pairs:visible(r)
# Actual normalized complete records feed the same native grader.
save('postdelivery-native-input.json',[native(r,'delivered-'+str(i)) for i,r in enumerate(survivors+batch+pairs)])
counts={stage:{'correct':sum(cue(r) for r in subgroup(rows)),'total':len(subgroup(rows))} for stage,rows in [('raw',raw),('accepted',survivors),('runner_batch',batch)]}
save('batch-content-shortcut.json',{'strategy':'For each three-option checkbox question, select only its invertibility claim, whether phrased invertible or not invertible. Ignore all given evidence.','subgroup':'three ordinary checkbox fields','scope':'exact runner batch, not universal generator','counts':counts,'baseline':1/7,'baseline_explanation':'uniform random choice from the seven eligible nonempty subsets','batch_records':subgroup(batch),'reproduction':'python regression.py batch; expected nonzero exit until batch-selection guard removes perfect cue','field_order_independent':True})
save('postdelivery-analysis.json',{'sample_coverage':summary(survivors),'batch_coverage':summary(batch),'stage_counts':{'samples':[len(raw),len(survivors)],'runner_batch':[5,len(batch)],'counterfactuals':[6,len(pairs)]},'controlled_pairs':{'det_zero_nonzero':{'before':visible(pairs[0]),'after':visible(pairs[1])},'irrelevant_det_sign_magnitude':{'before':visible(pairs[0]),'after':visible(pairs[2])},'claim_polarity':{'before':visible(pairs[2]),'after':visible(pairs[3])},'vector_scaling':{'before':visible(pairs[4]),'after':visible(pairs[5])}},'shortcut':counts})
# Selection rules faithfully reproduced for the finite accepted pool, using ordinal
# surrogate entity IDs. IDs cannot be known until publication (which is forbidden).
def choose(ids,seed,configured=True):
 ids=sorted(set(ids))
 if not ids:return None
 if not configured:return ids[0]
 d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53)
 return ids[int(u*len(ids))]
# All captured and accepted instances are moderate; conditional on positive
# moderate weight, the second draw is uniform within fresh eligible moderate IDs.
selection=[]
for seen in [[],[1],[2],[1,2,3]]:
 ids=[i for i in range(1,6) if i not in seen]
 draws=collections.Counter(choose(ids,str(seed)) for seed in range(1000))
 selection.append({'seen_surrogate_ids':seen,'eligible_surrogate_ids':ids,'configured_draw_counts':dict(draws),'legacy_unconfigured_first':choose(ids,'',False)})
save('selection-analysis.json',{'implementation':'engine/rust/question_selection.rs select(), seen_before_task()','implementation_sha256':hashlib.sha256((REPO/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'captured_basis':5437,'captured_existing_inventory':{'moderate':17,'generated':0},'accepted_runner_pool':{'moderate':5},'rules':['Generator batch: template order shuffled; bounded max(200,50*count) attempts deduplicate mathematical fingerprints. Nonempty policy accepts source-backed None; no empty ordinary subsets without None.','Delivery: requested difficulty and captured-inventory/content deduplication (480 to 455, runner 5 to 5).','Learner: exclude previously seen content/current prefix; split by difficulty; configured positive moderate weight makes all surviving moderate candidates equiprobable within band. Zero moderate weight excludes rated moderate candidates. No truth-mask/claim/template balancing.','Without configured distribution choose lowest fresh entity ID.'],'simulation':selection,'simulation_basis':'Surrogate IDs 1..5 model accepted runner records in file order; numbers do not predict future assigned EDB IDs. The same selector formula is evaluated exactly; all candidates share one rated band.','limits':['No policy or learner history was included in the captured inventory; no live learner draw claimed.','Entity-identity collision validation requires live database access and was not invoked.','Future inventory may change duplicates or eligible pools.'],'conclusion':'No selector rule repairs a perfect content-based cue within the two three-option checkbox questions: if either is eligible and drawn, selecting the invertibility claim succeeds. History can remove either item but cannot supply a counterexample.'})
reg=[]
for case in ('source','batch'):
 cmd=[sys.executable,str(E/'regression.py'),case];r=subprocess.run(cmd,cwd=E,text=True,capture_output=True)
 reg.append({'case':case,'command':cmd,'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 assert r.returncode!=0
save('failing-regressions.json',reg)
# Verify source correction from the original capture, not the author source copy.
s=json.load(open(E.parent/'source/source.json'));q=next(q for q in s['material']['kp'][':knowledge-point/questions'] if q[':question/math-academy-id']=='q-142367')
save('excluded-source-case.json',{'source':q,'independent_analysis':'v=(1,0,1,-1) is nonzero and Av=0, so nullity>0, A is singular, and Col(A) != R^4. Thus exactly I is true. Captured correct answer I only and solution both confirm this. The malformed distractor lI only does not make the correct subset ambiguous.','proposed_supported_correction':{'from':'lI only','to':'II only','reason':'The other four bank members use Roman numerals, II is a valid statement, and the captured five-member bank otherwise omits the II singleton. Record the typographic correction rather than dropping the entire complete source case.'},'package_behavior':'generate(template="q-142367", replay=True) raises ValueError: Unsupported template: q-142367','reproduction':'python regression.py source','scope':'Source replay/profile omission; q-34936 separately lacks key/solution and remains an evidence gap, not alleged wrong content.'})
save('render-inspection.json',{'reports':['render/rendering.json','render-counterfactual/rendering.json'],'screenshots_inspected':['render/question-002.png','render/question-003.png','render/question-006.png']+['render-counterfactual/question-%03d.png'%i for i in range(1,7)],'observations':['Nullspace two-parameter display, vector givens, statement labels, radio controls and checkbox controls are legible.','Rendered determinant 1 -> 0 reverses all three displayed judgments and checked controls; 1 -> -3 preserves truth while updating prompt and solution.','Claim negation reverses only that claim; v -> -v preserves the correct radio subset II only.','The actual UI hashes radio-choice positions using item/field/answer identity; raw bank order is not assumed to equal learner display order. Checkbox field sequence is preserved by mountInlineFields; primary batch cue is content-based and independent of ordering.'],'result':'passed for 12 rendered cases (six initial previews, six controlled previews); no MathJax errors or broken images'})
save('package-after.json',hashes(P));assert hashes(P)==json.load(open(E/'package-before.json'))
(E/'session-state.md').write_text('Independent testing complete: 480 samples -> 455 delivery survivors; exact runner batch 5 -> 5; 15 source replays plus two recorded exclusions. Native raw grading passed 2935 checks; postdelivery native input prepared. UI: six runner/representative cases and six controlled cases rendered and screenshots inspected. Runtime relocation and exact dependency versions passed; retained guard fails historical repository-import closure and passes current. Demonstrated failures: q-142367 exclusion; batch-only choose-invertibility cue 2/2 in three-checkbox subgroup. See failing-regressions.json. Package bytes unchanged. Final pedagogical report and postdelivery native result pending.\n')
print(json.dumps({'stages':{'samples':[480,len(survivors)],'batch':[5,len(batch)]},'content_shortcut':counts,'strict_failing_regressions':len(reg),'package_unchanged':True}))
