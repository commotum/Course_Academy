exec(open('review.py').read().split("batch=load(ROOT/'batch.json')")[0])
# Exercise duplicate rejection and the bounded retry boundary without touching package files.
original_sample=g.sample
rr=load(ROOT/'samples.json')[:2];calls=[]
try:
 def repeated(rng,seed):
  import copy
  calls.append(seed)
  return copy.deepcopy(rr[0 if len(calls)<=2 else 1])
 g.sample=repeated
 out=g.generate(count=2,seed=61409)
 assert [r['generation']['attempt'] for r in out]==[1,3]
 attempts=len(calls)
 g.sample=lambda rng,seed:__import__('copy').deepcopy(rr[0])
 try:g.generate(count=2,seed=61409);raise AssertionError('duplicate exhaustion did not fail')
 except ValueError as e:assert 'could not fill unique batch' in str(e)
finally:g.sample=original_sample
save('rejection-boundaries.json',{'method':'Temporarily replace in-memory sample function with already independently validated records; restore in finally; package never modified.','seed':61409,'duplicate_then_distinct_attempts':attempts,'accepted_attempts':[1,3],'all_duplicates_exhausts_bound':True,'counterexample_records':'samples.json'})
# Confirm native grader and rendered content propagate both types of intervention.
pairs=load(ROOT/'counterfactual-records.json');specs=load(ROOT/'counterfactual-results.json')
graded=load(ROOT/'grader-results.json');graded_by={r['label']:r for r in graded['records']}
rendered=load(ROOT/'render-pairs/rendering.json');assert len(rendered['cases'])==len(pairs)==12 and rendered['passed']
pair_confirm=[]
for spec in specs:
 entry={**spec,'native_field_outcomes':[],'rendered':[]}
 for idx in spec['indices']:
  r=pairs[idx];want=expected(r);q=r['question'];view=rendered['cases'][idx]
  assert view['passed'] and not view['mathErrors'] and not view['javascriptErrors']
  end=q[':question/worked-solution'].split('\n\n')[-1]
  # Text leaves math in split glyphs, but the response conclusion and None literal remain readable.
  if bank:=r['generation']['bank_profile']:
   if bank!='checkbox':assert want[0] in view['text']
   elif want[-1]=='true':assert 'Therefore, select "None of the above".' in view['text']
  native=graded_by['pairs-'+str(idx)]
  inputs=next(x for x in load(ROOT/'grader-input.json') if x['label']=='pairs-'+str(idx))
  assert len(inputs['checks'])==len(native['checks'])
  for a,b in zip(inputs['checks'],native['checks']):assert a['expected']==b['outcome']
  entry['native_field_outcomes'].append({'record_index':idx,'accepted':sum(c['outcome']=='accepted' for c in native['checks']),'rejected':sum(c['outcome']=='rejected' for c in native['checks']),'expected_response':want})
  entry['rendered'].append({'index':idx,'passed':True,'final_solution':end})
 pair_confirm.append(entry)
save('counterfactual-verification.json',{'pairs':pair_confirm,'native_report':'grader-results.json','renderer_report':'render-pairs/rendering.json','outcome':'Relevant evidence changes propagate to visible target, membership justification, exact response and actual native outcomes. Magnitude changes in the same semantic class preserve response; displayed expressions/solutions still update.'})
shots=['render/question-002.png','render-pairs/question-002.png','render-pairs/question-004.png','render-pairs/question-007.png','render-pairs/question-012.png']
save('render-inspection.json',{'reports':['render/rendering.json','render-pairs/rendering.json'],'cases':18,'visually_inspected':shots,'passed':True,'observations':'Read actual UI screenshots: radical overbar and minus, subscripts/superscripts, complex/real symbols, checkbox and shuffled radio controls, explicit None and worked conclusions display legibly without clipping. Zero checkbox now instructs selecting None. Radio root rationality and universal sign changes visibly update both response and explanation. All 12 pair views also checked for renderer errors and native outcomes.','limit':'Initial preview uses default six-record limit: all five batch records plus first controlled instance. Separate pair renderer explicitly uses limit12.'})
coverage=load(ROOT/'coverage-results.json');stage=load(ROOT/'stage-analysis.json');shortcuts=load(ROOT/'shortcut-results.json');source_account=load(ROOT/'source-analysis.json')
ped={
'learner_operation':source_account['learner_operation'],
'fixed_features':[
 {'feature':'Four ordinary candidate sets and one elementary real target or named real number class.','justification':'All eleven target sources and canonical e8b7d098 use four candidates; easy work is a classification/containment decision with at most one elementary simplification.'},
 {'feature':'Use only taught number-set hierarchy and strict sign/zero-subscript meanings.','justification':'Tutorial8214 explicitly excludes zero from N and defines N/Z/Q/R/C; tutorial8215 defines sign and zero restrictions.'},
 {'feature':'Complete five-choice combination banks for radio profiles; explicit None complement for new checkbox records.','justification':'Retain observed response shape and full source banks. Source f51862bd explicitly models zero qualifiers with None; other sources include false None distractors. Bank-specific feasible subset constraints are necessary to ensure a valid supplied radio response, rather than fixed qualifying objects.'}],
'answer_roles':[
 {'role':'Target sign, zero status, integrality/rationality, or named universal class.','eligible_variation':'Change within the lesson number types and representations; keep comparable elementary workload.','observed':'Fresh seed493127 covers all six representation profiles; decimal includes all five permitted sign/integrality categories. Fixed-candidate root, zero/decimal and universal-class interventions change answers as expected.'},
 {'role':'Which four candidate sets qualify and their positions.','eligible_variation':'Assign any distinct taught symbols and qualifying subset represented by the response bank and feasible for the target.','observed':'Construction chooses feasible roles then compatible candidate symbols; no candidate position is globally fixed. Fresh records vary each radio bank answer; radio10 remaining choice II-and-III is exercised by controlled positive-integer universal instance.'},
 {'role':'Correct response count and radio label.','eligible_variation':'All feasible checkbox counts; any feasible subset encoded in each complete captured radio bank.','observed':'No fixed correct count across production. The actual five-record batch has five different exact answers; repeated radio10 bank uses different combinations. Explicit None is selected only when all ordinary candidates are false.'}],
'coverage':[
 {'case':'Complete source replay and corrected None response contract.','sample_refs':['source-replays.json','source-replay-results.json','retained-regression-results.json'],'result':'All eleven full banks/prompts and available worked solutions preserved; seven retained regressions independently fail the baseline and pass the current code.'},
 {'case':'Fresh easy profile and response-bank sampling.','sample_refs':['samples.json','coverage-results.json','rejection-trace.json'],'result':'90 fresh records: decimal18, fraction17, reciprocal16, root14, pi14, universal11. Checkbox13 and every radio bank present. All90 survive actual delivery.'},
 {'case':'Actual batch, separately measured.','sample_refs':['batch.json','delivery-batch/accepted.json','shortcut-results.json'],'result':'All five survive; decimal/root/pi targets, checkbox and two radio banks. Five distinct exact responses. No tested fixed answer-producing action solves all five or the two-member radio10 subgroup.'},
 {'case':'Captured historical bank.','sample_refs':['generated-records.json','inventory-results.json','affected-inventory.json'],'result':'Five stored generated records reproduced exactly by parameters, fingerprints and publisher UUIDs. One old all-false bank lacks None and is excluded by current fresh-practice source eligibility; current constructor produces valid explicit None at those parameters.'}],
'counterfactuals':[],
'shortcut_probes':[],
'delivery':{'stages_examined':['generator role feasibility and bounded identity rejection','nonempty-checkbox policy','requested easy filtering','normalization and stable identity','captured inventory and within-batch deduplication','fresh/usable/seen filtering and conditional difficulty-weighted learner selection'], 'sample_refs':['rejection-trace.json','rejection-boundaries.json','delivery-samples/delivery.json','delivery-batch/delivery.json','stage-analysis.json','selection-sample.json'], 'result':'Combined independently chosen131 inputs yield122 accepted records; all90 fresh sample records and exact batch5/5 survive. Source rules for current learner selection faithfully reproduced read-only: all current generated records eligible, captured old all-false item excluded, uniform within positive easy band; no policy and zero-weight alternatives disclosed. Historical seeds and future learner policy/history unavailable.'},
'limitations':stage['limits']+['Finite shortcut probes and small conditional groups do not establish absence of all shortcuts. Singleton subgroup coincidences cannot establish a family rule; fixed assignment freedom is checked in construction and controlled pairs.','No diagram assets occur in the target questions; tutorial hierarchy is already defined explicitly in prose.','Historical inventory remains unchanged. Its one known old defect is retained in affected-inventory.json rather than attributed to the fixed current constructor.']}
for s in specs:
 ped['counterfactuals'].append({'kind':s['kind'],'change':s['label'],'expected':'Response preserved while expression updates.' if s['kind']=='irrelevant' else 'Fixed candidate bank requires reconsidering which sets contain the changed target; response changes.','observed':str(s['expected'])+'; prompts, conclusions and native outcomes checked in counterfactual-verification.json; all12 pair UI previews passed.','status':'passed','justification':'Sign, zero and rationality are answer-bearing by tutorials8214/8215; magnitude within one sign/integrality/rationality class is irrelevant to the listed membership predicates.','sample_refs':['counterfactual-records.json','counterfactual-verification.json','grader-results.json','render-pairs/rendering.json']})
# Include all strategies on substantive raw/delivered and exact batch groups, including conditional probes.
for p in shortcuts['strategies']:
 if p['subgroup'].count(';') or p['stage'] not in ['raw','fresh_delivered','batch_delivered']:continue
 ped['shortcut_probes'].append({'cue':'Stored answer slot or candidate position; '+p['subgroup'],'subgroup':p['stage']+':'+p['subgroup'],'scope':p['scope'],'strategy':p['strategy'],'correct':p['correct'],'total':p['total'],'baseline':p['baseline'],'disposition':'not_predictive','conclusion':'Baseline is uniform exact-answer guessing: 1/5 radio or 1/16 coherent four-candidate checkbox subsets, averaged for mixed groups. No deterministic production cue is shown; small/singleton matches are descriptive coincidences, with candidate assignments variable in code and controlled interventions. Radio presentation shuffles, so stored slots are not stable visual positions. See full profile+bank cross-groups and best constants in shortcut-results.json.','sample_refs':['samples.json' if p['stage']=='raw' else 'delivery-samples/accepted.json' if p['stage']=='fresh_delivered' else 'delivery-batch/accepted.json','shortcut-results.json']})
for p in shortcuts['intended_predictors']:
 if p['stage']!='fresh_delivered':continue
 ped['shortcut_probes'].append({'cue':p['cue'],'subgroup':'Delivered checkbox fields labeled '+p['cue'],'scope':'other_recognizable_subgroup','strategy':'Select unscripted '+p['cue'],'correct':p['correct'],'total':p['total'],'baseline':0.5,'disposition':'intended_skill','conclusion':p['explanation']+' Baseline0.5 is arbitrary independent checkbox Boolean guessing; this valid simplification applies taught hierarchy.','sample_refs':['delivery-samples/accepted.json','shortcut-results.json']})
save('pedagogical-variation.json',ped)
save('scope-results.json',{'passed':True,'basis':'source-analysis.json','fresh_profiles':coverage['raw']['profiles'],'limits':'Targets remain real; no negative radicands or complex arithmetic; fractions have positive small denominators, roots bounded144, finite decimals at most four places. Named classes use the taught hierarchy/sign restrictions. Four candidates and full observed response banks keep comparable workload.','checked_records':['samples.json','boundary-records.json','counterfactual-records.json','source-replays.json']})
# Hash every package file, including author evidence, not merely runtime files.
after={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};save('package-hashes-after.json',after);assert after==load(ROOT/'package-hashes-before.json')
pack=load(ROOT/'packaging-results.json');pack['package_unchanged']=True;pack['all_package_files_checked']=len(after);pack['rejection_boundary_report']='rejection-boundaries.json';save('packaging-results.json',pack)
checks={}
def passed(name,files,detail):checks[name]={'status':'passed','evidence_paths':files,'details':detail}
passed('source_replay',['source-analysis.json','source-replay-results.json','source-replays.json','retained-regression-results.json'],'All eleven full source banks replay; prompts and available solutions preserved. Missing source keys/solutions independently reconstructed and identified.')
passed('math',['math-results.json','samples.json','boundary-records.json','retained-regression-results.json'],'136 independently checked records, including exact batch, eighteen boundaries and six pairs. Prior None instruction failure reproduced on baseline and corrected at unchanged explicit parameters.')
passed('variety',['coverage-results.json','samples.json','stage-analysis.json','delivery-batch/accepted.json'],'All six source-supported profiles and four full radio banks now sampled; decimal sign/integrality classes vary. All90 fresh records and exact batch5/5 survive. Finite source-bank restrictions justified by response contract.')
passed('scope',['scope-results.json','source-analysis.json','boundary-records.json'],'Variations remain elementary real-number membership/containment under taught sign and zero conventions; four-candidate workload and captured response contracts retained.')
passed('grading',['grader-input.json','grader-results.json','counterfactual-verification.json'],'Native learner grader passed882 checks:300 accepted,582 rejected,0 unresolved. Every authored choice/opposite Boolean tested against independent prompt-derived expectations; no free-entry fields apply.')
passed('rendering',['render/rendering.json','render-pairs/rendering.json','render-inspection.json','render/question-002.png','render-pairs/question-002.png'],'18 actual-UI previews cover exact batch and all controlled-pair records. Screenshots inspected; readable math, radio/checkbox controls and worked solutions, with corrected explicit None conclusion.')
passed('packaging',['packaging-results.json','package-hashes-before.json','package-hashes-after.json','rejection-boundaries.json','author-preflight-rerun.log'],'Exact Python3.13.5 standard-library manifest, declared-files relocation, deterministic replay, invalid input and retry boundaries passed. Every package file hash unchanged. Author preflight rerun only in evidence-local harness; independent baseline regressions corroborate repairs.')
passed('decision_variation',['pedagogical-variation.json','counterfactual-verification.json','shortcut-results.json','stage-analysis.json','affected-inventory.json','generated-records.json'],'Relevant and irrelevant interventions propagate through prompts, explanations, native grading and actual rendering. Conditional shortcut probes and exact batch reveal no demonstrated incidental answer-producing rule. Current-source selection modeled with disclosed policy/history/future-ID limits. Historical all-false inventory item separately retained and excluded by current fresh-practice source rule.')
result={'verdict':'accepted','summary':'Current generator and exact five-record batch pass all eight checks. Retained failures are repaired. One historical inventory defect remains documented and excluded by current selection rules; no package changes or database writes occurred.','source_analysis':{k:source_account[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':checks,'findings':[]}
save('result.json',result)
# Verify evidence contract, including every relative sample path, against the shared schema.
subprocess.run(['python3','-c','import json,jsonschema,sys; jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2])))',str(ROOT/'pedagogical-variation.json'),str(REPO/'generate/pipeline/pedagogical-variation.schema.json')],env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},check=True)
for ch in result['checks'].values():
 for n in ch['evidence_paths']:assert (ROOT/n).is_file() and (ROOT/n).stat().st_size>0,n
for group in ['coverage','counterfactuals','shortcut_probes']:
 for obj in ped[group]:
  for n in obj['sample_refs']:assert not pathlib.Path(n).is_absolute() and '..' not in pathlib.Path(n).parts and (ROOT/n).stat().st_size>0,n
for n in ped['delivery']['sample_refs']:assert (ROOT/n).stat().st_size>0
save('contract-validation.json',{'pedagogical_schema':'passed','all_evidence_nonempty':True,'relative_sample_refs':True,'checks':list(checks),'package_unchanged':True,'bindings':{'package_hash':'4eff7c602693fbb0353313f2d72defe33d5dd1d630c5228fc22973399fcd6104','batch_hash':'c163045d853e9f90c8e2720382fd598d7051dd04edb5b4319eed29a2cf8f8fbb','policy_version':2}})
(ROOT/'session-state.md').write_text('Review complete: accepted current generator/batch; all eight checks passed. See result.json.136 independently checked records;882 native grader outcomes; actual batch5/5 survives;18 UI previews including all controlled pairs. All package hashes unchanged. One captured historical bank defect reproduced and saved in affected-inventory.json, excluded by current selection source. Selection assumptions/limits explicit. No publication/database writes.\n')
print(json.dumps({'verdict':result['verdict'],'checks':len(checks),'package_files_unchanged':len(after),'pedagogical_schema':'passed','native_checks':graded['accepted_checks']+graded['rejected_checks'],'source_replays':11,'rendered':18}))
