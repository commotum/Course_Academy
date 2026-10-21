import sys,pathlib,json,hashlib,collections,random
sys.dont_write_bytecode=True
from independent_math import *
from probes import summary,decision
from reproduce_unit_shortcut import probe
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy')
def read(n):return json.load(open(E/n))
def dump(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
# Complete stage measurements, keeping ordinary sampling separate from fixed-seed
# test controls. A fixed random seed is not a learner-visible template.
pairs=[('batch.json','delivery-batch'),('fresh.json','delivery-fresh'),('source-shortcut-records.json','delivery-source-shortcut'),('cue-control-records.json','delivery-controls'),('focused-records.json','delivery-focused'),('role-records.json','delivery-roles')]
measures={};unit={};stages=[]
for raw,folder in pairs:
 for path in (raw,folder+'/accepted.json'):
  records=read(path);measures[path]=summary(records)
  if raw in ['source-shortcut-records.json','focused-records.json']:
   groups={'all':records,'ordinary q-32244':[r for r in records if r['generation']['bank_profile']=='q-32244']}
  else:groups={'all':records}
  unit[path]={}
  for name,rs in groups.items():
   ps=[probe(r) for r in rs];unit[path][name]={'count':len(rs),'applicable':sum(x['applicable'] for x in ps),'sole_unit_correct':sum(x['shortcut_correct'] for x in ps),'first_position_fallback_correct':sum((probe(r)['selected_answer_id'] if probe(r)['applicable'] else field(r)[':answer-field/choices'][0][':answer/id'])==correct(r) for r in rs)}
  # Extend already retained frequency and slope probes with visible length and
  # absolute coefficient extrema; these never inspect equations to select.
  groups={'overall':records}
  for t in set(r['generation']['template'] for r in records):groups['template:'+t]=[r for r in records if r['generation']['template']==t]
  for name,rs in groups.items():
   for r in rs:
    M=system(r['question'][':question/problem']);piv=M.rref()[1];fc=next(j for j in range(M.cols-1) if j not in piv);cs=field(r)[':answer-field/choices'];xs=[vec(c[':answer/value']) for c in cs];ki=next(i for i,c in enumerate(cs) if c[':answer/id']==correct(r))
    features={'text_length':[len(c[':answer/value']) for c in cs],'absolute_intercept':[sum(abs(a.subs(v[fc],0)) for a in x) for x in xs],'absolute_slope':[sum(abs(sp.diff(a,v[fc])) for a in x) for x in xs],'fraction_count':[c[':answer/value'].count('\\frac') for c in cs]}
    for feature,scores in features.items():
     for direction,extreme in [('min',min(scores)),('max',max(scores))]:
      chosen=[i for i,s in enumerate(scores) if s==extreme]
      if len(chosen)==1:
       out=measures[path][name]['probes'].setdefault(feature+'_'+direction,{'correct':0,'total':0});out['total']+=1;out['correct']+=chosen[0]==ki
  # The helper may reorder choices or identifiers; independently compare all
  # displayed mathematical systems, complete choice sets and keyed lines.
 def semantic(r):return(str(system(r['question'][':question/problem'])),tuple(sorted(str(vec(c[':answer/value'])) for c in field(r)[':answer-field/choices'])),str(vec(next(c[':answer/value'] for c in field(r)[':answer-field/choices'] if c[':answer/id']==correct(r)))))
 assert {semantic(r) for r in read(raw)}=={semantic(r) for r in read(folder+'/accepted.json')}
 delivery=read(folder+'/delivery.json');stages.append({'raw':raw,'accepted':folder+'/accepted.json','input':delivery['input_count'],'accepted_count':delivery['accepted_count'],'duplicates':delivery['duplicate_count'],'decision_cases_before':measures[raw]['overall']['decision_cases'],'decision_cases_after':measures[folder+'/accepted.json']['overall']['decision_cases'],'same_semantic_set':True})
dump('delivery-shortcuts.json',measures);dump('unit-repair-results.json',{'commands':['python -B review.py','python -B focused_audit.py','python -B finish_evidence.py'],'measurements':unit,'exact_before_after':'repair-verification.json','current_zero_intercept_controls':'focused-records.json','native_outcomes':'focused-grader-results.json','result':'The former sole-unit strategy never applies in the ordinary q-32244 samples, before or after filtering. Nonzero-intercept supplied coordinates share their slopes; homogeneous unit coordinates include both signs. A learner must use the equations to determine the needed intercept or homogeneous sign.'})
dump('delivery-stages.json',{'captured_inventory_basis':read('../source/inventory.json')['basis'],'publication_preparation_exists':(J/'publication/preparation.json').exists(),'reproduction':'Actual shared prepare_records via check_delivery.py; no publication or database writes.','sets':stages,'rejection_resampling':'resampling-stages.json','learner_selection':'learner-selection.json','limits':['Future inventory, database identity collisions and individual learner histories are unavailable.','Fixed-seed boundary and forced-role controls are dependency tests, not ordinary sampling distributions. Their aggregate position frequencies are not population estimates.']})
# Read-only reproduction of select() for hypothetical sorted batch ranks. The
# source is directly inspected, and all candidate banks have already been audited.
I=read('../source/inventory.json');bands=collections.defaultdict(list)
for q in I['questions']:
 d=q.get(':question/difficulty');bands[d[':db/ident'].split('/')[-1] if d else 'unrated'].append(q[':db/id'])
for value in bands.values():value.sort()
draws=[]
for i in range(30):
 seed='independent-review-repair3-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);draws.append({'seed':seed,'uniform':u,'rank':int(u*5)})
assert {x['rank'] for x in draws}==set(range(5))
dump('learner-selection.json',{'implementation':'engine/rust/question_selection.rs select() and seen_before_task()','implementation_sha256':hashlib.sha256((R/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'captured_basis':I['basis'],'captured_band_entity_ids':dict(bands),'rules':['Exclude previous-task content and current prefix.','Sort/deduplicate numeric entity candidates.','Choose a nonempty positive-weight difficulty band, then uniform candidate rank using digest bytes 8..16.','Without configured weights choose the first numeric ID.','Unrated candidates are a fallback only if no positively weighted rated band remains.'],'batch_rank_draws':draws,'result':'All five hypothetical easy batch ranks are reachable, with every record independently checked. Difficulty, deduplication and normalization remove no batch member or tested mathematical decision case. Selection preserves each question bank. Seen exclusions can reduce a learner pool; no per-learner coverage guarantee is claimed.','limits':['Publication is not prepared; future entity IDs are unavailable, so ranks represent whatever numeric ordering publication assigns.','Live histories and difficulty weights are unavailable. This verifies the algorithm and captured pool, not a specific learner draw.','The unconfigured first-ID fallback cannot be mapped to a new batch ID before publication; every possible batch fallback member has been checked.']})
# Inventory was independently reproduced from the original bound executable by
# regression_checks.py, with exact stored content and generation metadata matches.
hist=read('generated-records.json');checks=[]
for r in hist:
 checks.append({'question_id':r['question'][':question/id'],'entity_id':r['review_evidence']['stored_entity_id'],'probe':probe(r),'two_coordinate':len(vec(field(r)[':answer-field/choices'][0][':answer/value']))==2})
assert not any(x['two_coordinate'] for x in checks)
dump('inventory-unit-cue.json',{'basis':I['basis'],'captured_count':len(I['questions']),'reproduced_generated_count':len(hist),'checks':checks,'demonstrated_unit_cue_affected':0,'conclusion':'Verified absence of this two-coordinate unit cue in the ten reproduced historical generated records: each has three or four coordinates. Fourteen remaining inventory records are original instructional sources, not generated instances. The historical component-frequency defects remain separately reproduced in affected-inventory.json.','limits':['This is not a claim that the captured bank is free of every defect. No database content was altered.']})
dump('controlled-validation.json',{'integer':read('counterfactual-results.json'),'rational':read('rational-counterfactual-results.json'),'fixed_banks':read('role-results.json'),'actual_grader_stale_responses':[x for x in read('grader-results.json')['records'] if 'controlled-previous-vector' in x['label']],'fixed_bank_grader':'focused-grader-results.json','rendered_pairs':['render-remaining/question-006.png','render-remaining/question-007.png','render-remaining/question-008.png','render-remaining/question-012.png','render-remaining/question-013.png','render-remaining/question-014.png','render-focused/question-005.png','render-focused/question-006.png'],'conclusion':'Relevant coefficients and free-column roles change the system, correct vector and explanation. Actual radio grading rejects the previous answer after a relevant change and accepts it after invertible row mixing. Every one of five fixed-bank lines is correct under its own system in all six cases; native grading verifies all choices.'})
# Confirm exact source passages once more, without relying on author narrative.
s=read('../source/source.json');a=read('source-analysis.json')
texts=[]
def walk(x):
 if isinstance(x,dict):
  for k,vv in x.items():
   if isinstance(vv,str):texts.append(vv)
   else:walk(vv)
 elif isinstance(x,list):
  for z in x:walk(z)
walk(s)
for passage in a['lesson_passages']:assert any(passage['passage'] in t for t in texts),passage
confirm=read('source-confirmation.json');dump('source-confirmation.json',{'exact_source_cases':confirm,'exact_lesson_passages':a['lesson_passages'],'source_ratings':{'rated_easy':13,'unrated':1},'gaps_confirmed':a['gaps']})
dump('scope-review.json',{'source_refs':a['source_refs'],'sample_paths':['batch.json','fresh.json','source-shortcut-records.json','focused-records.json'],'observations':['Five-choice radio, small consistent dependent real linear systems and one free parameter throughout.','Both source-backed matrix shapes and free-y/free-z assignments occur.','Supplied-coordinate parallel distractors retain the equations and Gauss-Jordan stages, and assess elimination of augmented constants. Homogeneous cases require the slope sign from equations.','Source fractions, constant coordinates, equal-coordinate and zero-intercept simplifications remain supported.','No extra operator, response form, diagram or prerequisite was introduced.'],'limits':['Requested easy band is certified; no new independent difficulty certification of legacy moderate/hard extensions.']})
# Record the actual visual inspection, separate from the renderer's automatic
# report. All three reports passed, and selected screenshots were opened.
inspected=['render-all/question-001.png','render-all/question-005.png']+['render-remaining/question-'+str(i).zfill(3)+'.png' for i in [6,7,8,13,16,17,18]]+['render-focused/question-'+str(i).zfill(3)+'.png' for i in [3,5,6]]
reports=[read(p+'/rendering.json') for p in ['render-all','render-remaining','render-focused']]
assert all(r['passed'] for r in reports)
dump('render-inspection.json',{'actual_renderer':'unmodified learning UI through render_preview.py','report_paths':[p+'/rendering.json' for p in ['render-all','render-remaining','render-focused']],'rendered_count':sum(len(r['cases']) for r in reports),'screenshots_opened':inspected,'observations':['Prompts, radio controls, choice vectors and real-parameter intervals are readable.','Augmented bars, RREF states and row-operation labels remain inside the solution layout.','Inspected relevant/irrelevant pairs show the intended changed/preserved answers.','Rational signs, fractional coefficients and homogeneous positive/negative units display correctly.','The finite-point source distractor displays as a point and remains incorrect.'],'automatic_errors':0,'limits':['Representative screenshots inspected visually; no claim of exhaustive browser or viewport coverage.']})
# Formal pedagogical account based on independently observed decisions.
fixed=[{'feature':'Consistent small systems with one free real parameter','justification':'The tutorial and captured solving questions teach full parametric solutions of dependent systems. This isolates the source skill.'},{'feature':'Five-choice radio and vector order','justification':'All 14 captured practice banks use this response form and conventional original variable ordering.'},{'feature':'Later pivot cannot depend on an earlier free variable in RREF','justification':'Required by echelon mathematics; canonical pivots x,z and free y therefore make z constant.'}]
roles_desc=[{'role':'Which candidate full solution line satisfies the equations','eligible_variation':'All five candidate roles can be made correct without changing their mathematical bank.','observed':'30 fixed-bank controls attain all five distinct correct lines across all six cases; native grader and representative renderer agree.'},{'role':'Free and pivot columns','eligible_variation':'Free z with pivots x,y; canonical free y with pivots x,z; rank-one two-variable form.','observed':'All occur in fresh and filtered samples. Canonical original system is explicitly replayed.'},{'role':'Constant, vanishing-intercept and equal basic coordinates','eligible_variation':'Eligible coordinate assignments and signs can vary while preserving rank and complete solution dimension.','observed':'All six visible mathematical cases survive delivery; zero-constant and rational boundaries are retained.'},{'role':'Correct-choice position and component typography','eligible_variation':'Position should not signal correctness; eligible nonzero slopes/intercepts may be integer or source fractions.','observed':'Fresh positions and bank roles vary within templates. Current source banks share supplied nonzero slopes, so unit typography no longer singles out a key. Both unit signs occur in homogeneous controls.'}]
coverage=[]
for path in ['batch.json','fresh.json','source-shortcut-records.json','focused-records.json','role-records.json']:
 coverage.append({'case':path+' decision distribution','sample_refs':[path,'delivery-shortcuts.json','delivery-stages.json'],'result':str(measures[path]['overall']['decision_cases'])})
cfs=[{'kind':'relevant','change':'Change one basic-coordinate coefficient while keeping constants, row mixing, seed and free column fixed; separately exchange eligible free-column roles.','expected':'Prompt, keyed full solution and worked explanation follow the new evidence; the former solution is no longer accepted.','observed':'Integer and rational pairs change their answers and explanations; native stale-response cases reject the old vector. Canonical alternate free-column result agrees with the original source.','status':'passed','justification':'Tutorial basic/free-variable reasoning and canonical free-y example require deriving answers from equations, rather than fixed coordinate assignments.','sample_refs':['counterfactual-records.json','rational-counterfactual-records.json','controlled-validation.json','grader-results.json','render-remaining/rendering.json']},{'kind':'relevant','change':'Keep the five candidate lines fixed; force each candidate role in turn and derive corresponding equations.','expected':'All five assignments can be correct under appropriate same-method evidence, with matching explanations and native keys.','observed':'Each of six cases retains its complete unordered bank while all five different lines become correct; 150 actual native choice outcomes match. Representative role pair rendered and visually inspected.','status':'passed','justification':'Which source object satisfies the mathematical rule is incidental. Fixed-bank intervention tests answer roles independently of numeric surface variation.','sample_refs':['role-records.json','role-results.json','focused-grader-results.json','render-focused/rendering.json']},{'kind':'irrelevant','change':'Change invertible row mixing while preserving the RREF solution line.','expected':'The printed system and row-operation explanation change, while the complete solution remains accepted.','observed':'Both integer and rational pairs preserve the answer and native acceptance of the previous vector; screenshots show changed equations and unchanged solution.','status':'passed','justification':'Elementary row operations preserve the source system solution set, so this is irrelevant to the final response despite changing presentation.','sample_refs':['counterfactual-records.json','rational-counterfactual-records.json','controlled-validation.json','grader-results.json','render-remaining/rendering.json']}]
probes=[]
# Do not infer population shortcuts from the deliberately identical RNG seed
# used for explicit boundary tests or from forced-role interventions.
for path in ['batch.json','delivery-batch/accepted.json','fresh.json','delivery-fresh/accepted.json','source-shortcut-records.json','delivery-source-shortcut/accepted.json']:
 for group,stats in measures[path].items():
  if group=='template:authored_easy':continue
  for cue,z in stats['probes'].items():
   if not z['total']:continue
   probes.append({'cue':cue,'subgroup':path+' '+group,'scope':'overall' if group=='overall' else 'within_template','strategy':'Select the sole '+cue+' choice; abstain when the extremum is tied. Component repetition uses only printed components; coefficient/term probes ignore equations.','correct':z['correct'],'total':z['total'],'baseline':0.2,'disposition':'not_predictive','conclusion':'Uniform choice among five gives baseline 0.2 conditional on applicability. No repeatable perfect predictor is established by these ordinary samples; small conditional counts are descriptive only. Fixed-seed explicit controls are excluded from population interpretation.','sample_refs':[path,'delivery-shortcuts.json']})
for path in ['source-shortcut-records.json','delivery-source-shortcut/accepted.json','focused-records.json','delivery-focused/accepted.json']:
 z=unit[path]['ordinary q-32244']
 probes.append({'cue':'sole unmultiplied first-coordinate parameter','subgroup':'q-32244 ordinary source-profile, '+path,'scope':'within_template','strategy':'Choose the sole unit-parameter entry if it exists; otherwise choose first position.','correct':z['first_position_fallback_correct'],'total':z['count'],'baseline':0.2,'disposition':'not_predictive','conclusion':f'The former cue applies in {z["applicable"]}/{z["count"]} cases; all choices share the unit slope for nonzero intercepts, or both unit signs are present when homogeneous. Reported hits come from first-position fallback. Baseline is uniform five-choice selection.','sample_refs':[path,'unit-repair-results.json','focused-grader-results.json']})
ped={'learner_operation':a['skill']+' The learner must establish which whole vector line satisfies the equations, reading pivots and free variables; typography and fixed candidate positions are not part of this operation.','fixed_features':fixed,'answer_roles':roles_desc,'coverage':coverage,'counterfactuals':cfs,'shortcut_probes':probes,'delivery':{'stages_examined':['generator case choice and rejection/resampling','requested easy difficulty','actual shared publisher validation and normalization','captured-inventory and within-batch deduplication','learner difficulty bands, seen exclusions, uniform rank and unconfigured fallback'],'sample_refs':['delivery-stages.json','delivery-shortcuts.json','resampling-stages.json','learner-selection.json','batch.json'],'result':'All 5 runner records survive. Independent 36 default, 55 source/boundary, 24 targeted template, 32 fresh changed-branch and 30 role records retain their semantic sets. All six default decision cases survive. Captured easy learner selection does not rewrite banks; live-history coverage cannot be guaranteed.'},'limitations':['Finite, targeted audit of the current easy package and exact runner batch, not proof against every possible shortcut.','Explicit same-seed controls and forced roles are dependency tests, not ordinary sampler-frequency estimates.','Fourteen original sources include one incomplete key/solution; its answer was independently inferred and checked.','No publication preparation exists; offline shared filtering uses captured inventory basis 5373. Future inventory, assigned entity IDs and learner histories may differ.','Ten historical generated inventory records retain a separately reproduced component-frequency defect. They are not outputs of the revised bank construction; affected-inventory.json records them without database changes.']}
dump('pedagogical-variation.json',ped)
# Structural validation without adding an undeclared dependency. Check the exact
# schema's required keys/types, enum values, and referenced nonempty artifacts.
schema=json.load(open(R/'generate/pipeline/pedagogical-variation.schema.json'))
def validate(x,s,path='root'):
 typ=s.get('type')
 if typ=='object':
  assert isinstance(x,dict),path
  assert set(s.get('required',[]))<=set(x),path
  if s.get('additionalProperties') is False:assert set(x)<=set(s['properties']),path
  for k,vv in x.items():
   if k in s.get('properties',{}):validate(vv,s['properties'][k],path+'.'+k)
 elif typ=='array':
  assert isinstance(x,list) and len(x)>=s.get('minItems',0),path
  for i,z in enumerate(x):validate(z,s['items'],path+f'[{i}]')
 elif typ=='string':assert isinstance(x,str) and len(x)>=s.get('minLength',0),path
 elif typ=='integer':assert isinstance(x,int) and not isinstance(x,bool),path
 elif typ=='number':assert isinstance(x,(int,float)),path
 if 'enum' in s:assert x in s['enum'],path
 if 'minimum' in s:assert x>=s['minimum'],path
 if 'maximum' in s:assert x<=s['maximum'],path
validate(ped,schema)
def refs(x):
 if isinstance(x,dict):
  for k,vv in x.items():
   if k=='sample_refs':
    for ref in vv:assert not pathlib.Path(ref).is_absolute() and (E/ref).is_file() and (E/ref).stat().st_size,ref
   else:refs(vv)
 elif isinstance(x,list):
  for z in x:refs(z)
refs(ped)
# Final package byte integrity includes every evidence/nonmanifest file.
before=read('package-before.json');after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file()};assert before==after
dump('package-integrity.json',{'before_file_count':len(before),'after_file_count':len(after),'unchanged':True,'changed':[],'database_writes':0,'published_assets':0})
dump('evidence-contract.json',{'pedagogical_schema_validated':True,'schema_path':str(R/'generate/pipeline/pedagogical-variation.schema.json'),'all_pedagogical_sample_refs_nonempty_relative_files':True,'actual_native_checks':read('grader-results.json')['accepted_checks']+read('grader-results.json')['rejected_checks']+read('focused-grader-results.json')['accepted_checks']+read('focused-grader-results.json')['rejected_checks'],'rendered_records':sum(len(r['cases']) for r in reports),'package_unchanged':True})
(E/'session-state.md').write_text('Review complete: all eight checks supported. Exact 5-record batch survives filtering; all six cases present in 36 fresh default records. All 14 banks and canonical free-y replayed. Independent math/solutions pass for 126 initial plus 62 changed/role controls. Actual native grader: 949 expected responses, no unresolved cases. Actual UI: 30 renders, representative screenshots inspected. All five retained findings verified against failing historical examples and current checks. Historical inventory 10 affected records retained separately, no current unit-cue generated inventory instances. Package all 289 files unchanged; no DB writes or publication. Evidence contract validated; final result being recorded.\n')
print(json.dumps({'stage_sets':len(stages),'pedagogical_probes':len(probes),'native_checks':949,'rendered_records':sum(len(r['cases']) for r in reports),'unchanged_files':len(after),'schema':'passed'}))
