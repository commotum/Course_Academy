import json, hashlib, sys, re
from pathlib import Path
sys.path.insert(0, '/home/jake/Developer/Course_Academy')
from scripts.generator_evidence import record_sha256, batch_sha256
r=Path(__file__).resolve().parent
repo=Path('/home/jake/Developer/Course_Academy')
load=lambda p:json.loads(Path(p).read_text())
def save(name,value):
    (r/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
initial_hash='f4e2cdd70726c82b96396236ac7094d8f74d21fac0ebb01521765e182285e82c'
assert hashlib.sha256((r/'source-analysis.json').read_bytes()).hexdigest()==initial_hash
initial=load(r/'source-analysis.json')
source=load('/tmp/generator-live-pipeline/source/source.json')
source_refs=[
 'KP 900001 / 394508fb-b6fd-5725-ae47-ffc44fc1cb9c: Read an entry of a two-by-two integer matrix.',
 'Tutorial dff2b933-538b-5a0c-acf6-09aa02994987, Lesson: first index specifies row, second specifies column; count from top and left starting at 1; no arithmetic.',
 'Same tutorial: any entry of a two-by-two matrix with integer entries; one integer in a free-entry blank; positive, negative and zero do not change the method.',
 'Complete source practice fixture-q11/q12/q21/q22 (910011–910014): same matrix [[2,-3],[0,7]], target a_11/a_12/a_21/a_22, answers 2/-3/0/7; all easy, no choices or diagrams.'
]
bands=['easy','moderate','hard']; examples=load('/tmp/generator-live-pipeline/workspace/exemplars.json')
solved=load(r/'independent-solving.json')['cases']
source_comparisons=[];reps=[];paths=[];band_obligations={};counterfactuals=[];probe_details=[]
progressions={
 'easy':'Original easy fixture-q12 retained mathematically, including its negative single-digit result. It still requires recalling the index convention and locating row 1, column 2 without help.',
 'moderate':'Compared with easy, two-digit signed integers add a modest transcription demand. Selecting row 2, column 1 still requires precisely the same recall and two location decisions. The moderate label is authored and uncalibrated, with no extra arithmetic.',
 'hard':'Compared with moderate, three-digit integers add only a modest reading/transcription demand. Selecting row 1, column 2 still uses identical reasoning and one blank. The hard label is authored and uncalibrated; no added matrix operation or conversion is justified or present.'}
for n,band in enumerate(bands):
    raw=load(r/f'{band}-anchor.json')[0]
    assert raw==examples[n]
    delivered=load(r/f'delivery-{band}/accepted.json')[0]
    solved_raw=next(c for c in solved if c['band']==band and c['stage']=='raw')
    solved_del=next(c for c in solved if c['band']==band and c['stage']=='delivered')
    fp=record_sha256(delivered);assert fp==solved_del['record_sha256']
    matrix=solved_del['matrix'];i=solved_del['row'];j=solved_del['column'];v=solved_del['independently_computed']
    source_comparisons.append({
      'band':band,'raw_record_sha256':record_sha256(raw),'delivered_record_sha256':fp,
      'source_refs':source_refs,'operation':'Independently interpret a_ij and read one integer from a 2x2 matrix.',
      'supplied':f'Complete matrix {matrix} and requested a_{i}{j}; no index convention, marked row/column, highlighted cell or intermediate value.',
      'before_feedback':[f'Recall first index = row, second index = column.',f'Count rows from top and columns from left starting at 1; locate row {i}, column {j}.',f'Read and enter {v}, including its sign.'],
      'endpoint':'One exact-value mathematical blank; no explanation or matrix computation required.',
      'scope':'Same source operation, support level and response endpoint. The worked procedure appears only in the completed solution.',
      'origin':'Mathematically retained original fixture-q12 with corrected TeX/paragraph layout and local identities.' if band=='easy' else 'Authored local numerical instance justified by explicit integer-matrix lesson scope; not an imported original.',
      'fidelity':'No mathematical change to the easy original; the source doubles TeX escapes and the local anchor uses properly rendered pmatrix with real paragraphs and centered display. Moderate/hard vary entries and position, not the task.',
      'cue_judgment':'No answer-bearing emphasis or procedural cue in the displayed prompt. All four cell values have identical styling. Off-diagonal target makes reversed-index lookup a concrete distinguishable mistake.',
      'status':'passed'})
    band_obligations[band]={'progression':progressions[band],'records':[{'record_sha256':fp,'family':'independent-integer-entry','representative_sha256':fp,'reason':'This exact sole delivery survivor was independently solved, graded and inspected in both UI states; no other band or task stands in for it.'}]}
    reps.append({
      'record_sha256':fp,'family':'independent-integer-entry','given':f'Displayed A={matrix}, request a_{i}{j}, one empty mathematical blank.',
      'required_work':['Inspect the matrix and requested pair of subscripts.','Recall first-index row, second-index column; do not reverse them.',f'Count from top/left starting at 1; select row {i}, then its column {j}.',f'Read {v}, preserving its integer sign, and enter that value in the blank.','Perform the lookup before feedback; the row/column procedure is confined to the worked solution.'],
      'source_reasoning_steps':[0,1,2,3,4],
      'preservation':'All five frozen source-account obligations apply: full givens but no supplied selection, required indexing recall, row/column location, one-integer endpoint, and separation of independent practice from demonstration.',
      'difficulty_justification':progressions[band],
      'narrow_layout':{'status':'required','reason':'The two-dimensional matrix, subscript and blank must remain readable at a phone width. Inspected active/completed at 390x844 as well as 1280x1000.'},
      'fields':[{'field_index':0,'endpoint':f'One integer equal to a_{i}{j}={v}; field key answer.','equivalence':{'status':'tested','reason':f'No simplest-form restriction is stated; {v}/1 is the same integer. Native grading accepted it as well as {v}.'}}]
    })
    paths.append({'record_sha256':fp,'field_index':0,'template':'independent-integer-entry','field_key':'answer',
       'final_expression':str(v),'keyed_answer':str(v),'domain':'Integer entries in a two-by-two matrix; one-based i,j in {1,2}.',
       'conclusion':f'Worked solution selects row {i}, column {j}, and ends with a_{i}{j}={v}. The integer on its right side is exactly the stored key.',
       'sample_refs':['independent-solving.json',f'delivery-{band}/accepted.json','render/rendering.json'],'status':'passed','conversions':[],
       'conversion_review':{'status':'none','reason':'Direct integer lookup; the integer shown after the equals sign is identical to the key. No mathematical representation conversion or conversion negative control applies.','evidence_paths':['independent-solving.json','render/rendering.json']}})
    switched=matrix[j-1][i-1]
    changed=[row[:] for row in matrix]; changed[i-1][j-1]=v+1
    irrelevant=[row[:] for row in matrix];other=(i%2,j%2);irrelevant[other[0]][other[1]]+=1
    assert changed[i-1][j-1]==v+1 and irrelevant[i-1][j-1]==v
    counterfactuals.append({'band':band,'raw_record_sha256':record_sha256(raw),'delivered_record_sha256':fp,
      'original_matrix':matrix,'requested':[i,j],'original_answer':v,
      'relevant':{'change':f'Independently replace the selected integer {v} by {v+1}.','matrix':changed,'expected':v+1,'observed':changed[i-1][j-1],'status':'passed'},
      'irrelevant':{'change':f'Independently increment unselected row {other[0]+1}, column {other[1]+1}.','matrix':irrelevant,'expected':v,'observed':irrelevant[i-1][j-1],'status':'passed'},
      'target_position_change':{'change':f'Reverse requested indices to a_{j}{i}.','expected':switched,'observed':matrix[j-1][i-1]},
      'limit':'Counterfactuals are independent mathematical witnesses about these anchors, not outputs or tests of an unadmitted generator.'})
    probe_details.append({'band':band,'raw_record_sha256':record_sha256(raw),'delivered_record_sha256':fp,
      'upper_right_prediction':matrix[0][1],'upper_right_correct':matrix[0][1]==v,
      'minimum_value_prediction':min(x for row in matrix for x in row),'minimum_value_correct':min(x for row in matrix for x in row)==v,
      'format_review':'Uniform typography of cells, no marked row/column, no correct option rank or bank; the only target indicator is a_ij, which is the intended given.'})
save('source-comparison.json',{'initial_source_analysis_sha256':initial_hash,'source_refs':source_refs,'investigation_comparison':'Investigation correctly preserves independent lookup, one integer blank and no arithmetic. Authored moderate/hard labels are explicitly uncalibrated. No donor or exemplar redefines the objective; no conceptual amendment is needed.','cases':source_comparisons})
save('learner-obligations.json',{'families':[{'id':'independent-integer-entry','operation':'Recall index roles and locate one integer in a 2x2 matrix.','support':'Only the matrix and requested a_ij are supplied; no guided row/column selection.','response':'One exact-value mathematical blank.','reason':'Signs, digit lengths and off-diagonal positions change instances while preserving the same pre-feedback decisions and endpoint. All anchors were nevertheless individually inspected.','source_refs':source_refs}], 'bands':band_obligations,'representatives':reps})
save('solution-paths.json',{'cases':paths})
save('counterfactuals.json',{'method':'Parse the displayed matrix and target indices, then independently evaluate relevant/irrelevant changes without reading an implementation. This is not an alternative generator.','cases':counterfactuals})
save('cue-inspection.json',{'cases':probe_details,'limits':'Three design anchors, one per band, cannot establish a random-generation distribution or general absence of shortcuts. No generator implementation, resampling or learner selection is admitted. A remembered key for a single anchor is not evidence of a construction mechanism.'})
correct_upper=sum(x['upper_right_correct'] for x in probe_details);correct_min=sum(x['minimum_value_correct'] for x in probe_details)
delivery_refs=[f'delivery-{b}/delivery.json' for b in bands]
save('pedagogical-variation.json',{
 'learner_operation':'Independently recall indexing convention, select the requested row and column, and enter one displayed integer.',
 'fixed_features':[{'feature':'2x2 integer matrix; one valid named entry; one mathematical blank.','justification':'Explicit target scope and endpoint, not incidental source parameters.'},{'feature':'Unguided prompt and row-then-column worked solution.','justification':'Preserves required recall and selection before feedback; tutorial support does not migrate into independent prompts.'}],
 'answer_roles':[{'role':'Requested matrix position','eligible_variation':'a_11, a_12, a_21, a_22 supported by fixture-q11/q12/q21/q22.','observed':'Anchors request a_12, a_21, a_12. Only off-diagonal positions happen to be illustrated; no diagonal prohibition follows.'},{'role':'Selected integer','eligible_variation':'Any integer, including positive, negative or zero; no magnitude quota in source.','observed':'-3, -31, 307; signs and digit lengths vary, but no source-supported requirement to place zero or all positions among exactly three design anchors.'}],
 'coverage':[{'case':b,'result':progressions[b],'sample_refs':[f'{b}-anchor.json',f'delivery-{b}/accepted.json','source-comparison.json']} for b in bands],
 'counterfactuals':[{'kind':kind,'change':('Replace the selected value by its successor independently in each anchor.' if kind=='relevant' else 'Increment a different cell, leaving the requested cell unchanged, independently in each anchor.'),'expected':('Each lookup response changes to the replacement integer.' if kind=='relevant' else 'Each lookup response remains the original selected integer.'),'observed':('All three changes produce the expected new value.' if kind=='relevant' else 'All three changes preserve the original result.'),'justification':'Direct application of the taught entry-reading rule; these are mathematical witnesses and not runtime generator claims.','status':'passed','sample_refs':['counterfactuals.json']} for kind in ['relevant','irrelevant']],
 'shortcut_applicability':{'status':'applicable','reason':'Inspect visible cell styling and simple positional/value cues on this finite anchor set. Multiple-choice bank/rank probes are inapplicable to a free-entry endpoint.','sample_refs':['cue-inspection.json','render/rendering.json']},
 'shortcut_probes':[
    {'cue':'Always read the upper-right cell without interpreting the requested indices.','subgroup':'All three design anchors, both raw and delivered identities.','scope':'overall','strategy':'Read top-right value only; omit a_ij interpretation.','conclusion':f'Succeeds on {correct_upper}/3: fails on moderate a_21. This is diagnostic only; it establishes no recurring generator defect or shortcut-free population.','correct':correct_upper,'total':3,'baseline':0.25,'disposition':'not_predictive','claim':'diagnostic','sample_refs':['cue-inspection.json','independent-solving.json']},
    {'cue':'Choose the numerically smallest matrix value without locating the target.','subgroup':'Signed matrices: all three anchors.','scope':'other_recognizable_subgroup','strategy':'Inspect the four integers and output their minimum, ignoring the indices.','conclusion':f'Succeeds on {correct_min}/3: fails on hard. Uniform cell styling and the absence of row/column markers show no direct prompt annotation that supplies the answer. Counts are diagnostic, not proof about an unseen generator.','correct':correct_min,'total':3,'baseline':0.25,'disposition':'not_predictive','claim':'diagnostic','sample_refs':['cue-inspection.json','render/rendering.json']}
 ],
 'delivery':{'stages_examined':['requested difficulty','KP identity','image normalization','question validation','stable content identities','captured-inventory and within-batch deduplication'],'result':'All three raw anchors yield one survivor each. Mathematical values, target indices, support and response demands are preserved by normalization. This is offline preparation only.','sample_refs':delivery_refs},
 'limitations':['One fixed anchor per band cannot establish generator distribution, all-cell coverage or resistance to every shortcut.','No generator, rejection/resampling, learner history, weighted selection, refill or publication was admitted or tested.','Moderate/hard progression is an authored modest integer-reading demand; all original cases are easy.','Probe baseline 0.25 describes uniformly guessing one of four distinct displayed entries for these anchors; it is not a population estimate.']})
render=load(r/'render/rendering.json')
assert render['passed'] and len(render['cases'])==24
save('visual-inspection.json',{
 'method':'Reviewer visually inspected six sheets containing actual unanswered/completed desktop content crops and full narrow screenshots, one pair for each anchor. The report preserves full original screenshots. Each delivered frame was also verified byte-identical to its corresponding raw frame.',
 'report':'render/rendering.json','comparisons':'screenshot-comparisons.json',
 'cases':[{'band':b,'sheets':[f'visual-{b}-active.png',f'visual-{b}-completed.png'],
 'active':'Correct two rows/two columns, parentheses, ordered integer values, signed glyphs, and requested subscript. Blank empty; solution initially closed. No highlighted cell, convention reminder, intermediate value, or visible key. No clipped matrix or stray TeX at either width.',
 'completed':'Correct green integer response, expanded solution with the correct index-to-row/column explanation, and final equation agreeing with the independent answer and key. Narrow solution wraps legibly with no horizontal clipping.',
 'status':'passed'} for b in bands]})
# Preserve the supplied runner binding as metadata, not an independently claimed checkpoint.
binding={'policy_version':6,'phase':'exemplars','source_hash':'d3dede4b78d09818d0c91b54b0d44cf20a3330e77164d96632a48084ee1f7b04','inventory_hash':'161151705d878d2400c21a647e01a4c4596c75d638d85502b7fa6d142039fdd2','initial_source_analysis_sha256':initial_hash,'engine_hash':'02c0a552614ce59e2ac08acc1dc645b045a951d68b38fd6820e676aa2d7ca753','grader_sha256':'267b6ec743eb0035bd289d65057928e10c1b99dc0e425157b2532dd79e306c5e','verification_batches':{}}
expected_hashes=['dac7f4e9636e8e7fbbf6abce86545f2fd47c20a5585496566186951c10cfefc9','eb87f5c7eeb2dce913d4248441fb9512df46c045594621a04c5e3adb80e64ccb','02e7064514bff39d926c409fcc1c3e35fffb7de157e6bcc25ade35dca16d736d']
for band,h in zip(bands,expected_hashes):
    assert batch_sha256(load(r/f'{band}-anchor.json'))==h
    binding['verification_batches'][band]={'batch_file':str(r/f'{band}-anchor.json'),'batch_hash':h,'count':1,'requested_count':1,'seed':0,'assets':{}}
assert batch_sha256(source)==binding['source_hash']
assert batch_sha256(load('/tmp/generator-live-pipeline/source/inventory.json'))==binding['inventory_hash']
save('context-review-binding.json',binding)
save('artifact-review.json',{'initial_source_analysis_sha256':initial_hash,'unchanged_initial_account':True,'investigation_sha256':hashlib.sha256(Path('/tmp/generator-live-pipeline/workspace/investigation.md').read_bytes()).hexdigest(),'exemplars_sha256':hashlib.sha256(Path('/tmp/generator-live-pipeline/workspace/exemplars.json').read_bytes()).hexdigest(),'examples_equal_supplied_batches':True,'count':3,'bands':bands,'delivered_per_band':{b:1 for b in bands},'native_sources_equal_production':True,'anchor_or_investigation_edits':False,'runtime_refill_plan':'Not applicable during pre-construction exemplar review.','limits':'No generator or publication actions.'})
analysis={**initial,'evidence_paths':['source-analysis.json','source-comparison.json']}
def check(paths,details):return {'status':'passed','evidence_paths':paths,'details':details}
result={'verdict':'accepted','summary':'All three exact anchors preserve independent one-entry lookup and pass mathematical, native grading, delivery and unanswered/completed UI checks. No edits or source-account amendments were needed. Moderate/hard labels remain authored and uncalibrated.','source_analysis':analysis,
 'checks':{
 'source_replay':check(['source-comparison.json','source-analysis.json','independent-solving.json'],'Compared all anchors with eligible original fixture-q11/q12/q21/q22 and tutorial scope. Easy retains fixture-q12 mathematics with necessary representation normalization; moderate/hard are explicitly authored integer variants. No generator replay is claimed.'),
 'math':check(['independent-solving.json'],'Independently parsed and solved every raw/delivered anchor: -3, -31, 307. Each keyed value and worked-solution conclusion agrees with its selected cell; no arithmetic is involved.'),
 'variety':check(['pedagogical-variation.json','counterfactuals.json'],'Target positions and signed integer values vary within one source-supported operation. Three design anchors are not a generator-distribution sample; absent diagonal/zero targets here are not restrictions.'),
 'scope':check(['solution-paths.json','source-comparison.json'],'All delivered fields terminate at the displayed selected integer. No added matrix operation, response conversion or supplied target decision. No conversion control applies to these direct paths.'),
 'grading':check(['grading.json','native-build.json','independent-solving.json'],'Native grade_field accepted each exact integer and independently chosen integer-valued fraction and rejected both reversed-index and sign errors for all six raw/delivered records: 12 accepted, 12 rejected, zero unresolved. Isolated native inputs and binary match production/runner identities.'),
 'rendering':check(['render/rendering.json','visual-inspection.json','screenshot-comparisons.json'],'Every raw and delivered anchor inspected unanswered/completed at 1280x1000 and 390x844. All 24 actual-UI frames pass, with readable cells/signs/subscripts/blanks and correctly separated solutions. Raw/delivered corresponding frames are byte-identical.'),
 'packaging':check(['artifact-review.json']+delivery_refs,'Exactly one local complete anchor per requested band, matching supplied input batches, with fresh local identities and source provenance. All survive offline preparation. This phase checks exemplar artifacts; runtime/refill/publication is outside its scope.'),
 'decision_variation':check(['pedagogical-variation.json','cue-inspection.json','counterfactuals.json']+delivery_refs,'No direct answer-bearing prompt cue observed. Relevant/irrelevant cell counterfactuals checked mathematically for every anchor. Visible upper-right and minimum-value cue probes fail on this finite set; no unseen-generation shortcut claim is made.'),
 'progression':check(['learner-obligations.json','solution-paths.json','grading.json','render/rendering.json'],'Exact sole survivor and sole answer field of every band are self-represented and independently checked. One material operation/support/response family preserves all five frozen source obligations. Increasing integer digit length changes only modest transcription demand; empirical three-band calibration is absent.')},
 'findings':[],
 'band_verification':{b:{'status':'passed','batch_sha256':h,'evidence_paths':[f'delivery-{b}/delivery.json','grading.json','render/rendering.json','learner-obligations.json','solution-paths.json','source-comparison.json','visual-inspection.json'],'details':f'Exact {b} raw anchor plus its sole delivery survivor independently solved, natively graded with canonical/equivalent/wrong controls, and visually inspected in both states at both widths. No raw fallback used. '+progressions[b]} for b,h in zip(bands,expected_hashes)}}
save('final-result.json',result)
print('Created semantic evidence and final nine-check report; anchors, investigation and frozen account remain unchanged.')
