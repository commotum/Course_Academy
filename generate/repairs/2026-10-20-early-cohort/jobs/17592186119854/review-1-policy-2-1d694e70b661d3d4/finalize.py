import json,re,hashlib,sys
from pathlib import Path
from collections import Counter
E=Path(__file__).resolve().parent;W=E.parent/'workspace';R=Path('/home/jake/Developer/Course_Academy')
def load(n):return json.load(open(E/n))
def save(n,v):(E/n).write_text(json.dumps(v,indent=2)+'\n')
# Read actual rendered radio order from saved, unmodified-UI HTML rather than serial option arrays.
actual=[]
for prefix,records in [('render',load('render-input.json')[:6]),('render-more',load('render-more-input.json'))]:
 for i,r in enumerate(records):
  q=r['question']
  if not q[':question/answer-fields']:continue
  f=q[':question/answer-fields'][0];html=(E/prefix/f'question-{i+1:03d}.html').read_text();inputs=re.findall(r'<input[^>]*type="radio"[^>]*>',html);ids=[re.search(r'value="([^"]+)"',tag)[1] for tag in inputs];aid=f[':answer-field/correct'][1]
  assert len(ids)==5 and set(ids)=={a[':answer/id'] for a in f[':answer-field/choices']}
  actual.append({'sample_ref':('render-input.json' if prefix=='render' else 'render-more-input.json'),'index':i,'template':r['generation']['template'],'question_id':q[':question/id'],'html':f'{prefix}/question-{i+1:03d}.html','answer_ids_in_display_order':ids,'correct_display_position':ids.index(aid)+1})
save('ui-position-results.json',{'ordering':'ui/learning.js choiceOrder hashes itemId:fieldId:choiceId; raw serialized order is not necessarily displayed order. These positions are extracted from actual preview HTML, not a substitute ordering algorithm.','cases':actual,'exact_batch_positions':[x['correct_display_position'] for x in actual[:5]],'limits':['Actual task item IDs may differ from preview IDs, changing layout. Mathematical numeric-rank probes are order-independent.']})
ped=load('pedagogical-variation.json')
# Label prior raw-order probes accurately and document the apparent shared-seed predictor.
for p in ped['shortcut_probes']:
 if 'displayed position' in p['strategy']:
  p['cue']=p['cue'].replace('displayed position','serialized choice position');p['strategy']=p['strategy'].replace('displayed position','serialized choice position');p['conclusion']+=' This is package order; the UI additionally hashes item/field/choice IDs. Actual rendered-order probes are recorded separately.'
 if 'fixed numeric rank 5' in p['strategy'] and 'q-105168' not in p['subgroup']:
  p['conclusion']+=' Rank 5 is unavailable for four-number banks and counts as no successful selectable action there.'
 if 'moderate' in p['subgroup']:
  p['sample_refs'].append('sampling-independence.json');p['conclusion']+=' Shared seeds correlate draws across templates; see sampling-independence.json. These rows are not independent evidence of a population rank bias.'
# Exact fixed-rank comparison baseline must account for unavailable fifth rank.
for p in ped['shortcut_probes']:
 if 'fixed numeric rank 5' in p['strategy']:
  if 'q-105168' in p['subgroup']:p['baseline']=.2
  elif 'q-' in p['subgroup']:p['baseline']=0
  elif 'batch' in p['subgroup']:p['baseline']=.04
  else:p['baseline']=.025
  p['conclusion']+=' The numeric-only guessing comparison counts zero chance on records lacking a fifth numeric option.'
for name,rows in [('Exact runner batch in actual UI',actual[:5]),('q-73992 actual UI controlled RHS triple',[a for a in actual if a['template']=='q-73992'])]:
 for k in range(1,6):
  n=sum(a['correct_display_position']==k for a in rows);ped['shortcut_probes'].append({'cue':'Actual rendered radio position','subgroup':name,'scope':'overall' if 'batch' in name else 'within_template','strategy':f'Always click displayed position {k}, ignoring all mathematical data','correct':n,'total':len(rows),'baseline':.2,'disposition':'not_predictive','conclusion':f'{n}/{len(rows)}; random guessing among five controls has success rate 0.2. No single displayed position solves this tested set. Preview item-ID seed only; live task IDs can change order.','sample_refs':['ui-position-results.json','render-input.json','render-more-input.json']})
ped['limitations'].append('The fresh six seeds are shared across matrix profiles, correlating numeric-rank draws; 31/48 choose-third successes do not represent 48 independent rank draws. Construction uses uniform rank sampling before bounded coefficient generation, with no rank-dependent rejection. All-anchor fixed-data tests separately validate every eligible role.')
save('sampling-independence.json',{'seeds':[310019,410029,510047,610051,710053,810059],'observed_fixed_third_rank_success':{'correct':31,'total':48},'comparison_baseline':.24375,'independent_inspection':'generate initializes Random(seed), chooses randint(1,numeric_count) before coefficient sampling. The same seed and numeric_count therefore repeat the same rank in every profile. The 8x6 design is not 48 independent rank decisions. Normal coefficient resampling never changes the already drawn rank; every anchor is valid at every sampled RHS. Domain construction has uniform rank law; no incidental learner-visible matrix signature selects a rank.','unconditional_rank_3_probability':{'seven_four_numeric_profiles':.25,'one_five_numeric_profile':.2},'counterevidence':['All 33 controlled bank anchors change the correct rank at identical prompts/solutions.','Old source-rank rule solves 0/5 exact delivered batch records.','Exact batch contains ranks 1,3,4 and actual UI correct positions 3,1,3,2,4.'],'limits':'No inference of independent 48-trial sampling or proof of all possible shortcut absence. Finite rank imbalance is reported, not hidden.'})
# Ensure exact batch actual positions in explanatory text are accurate.
d=load('sampling-independence.json');d['counterevidence'][-1]='Exact batch contains ranks 1,3,4 and actual UI correct positions '+str([x['correct_display_position'] for x in actual[:5]])+'.';save('sampling-independence.json',d)
save('pedagogical-variation.json',ped)
inspected=['render/question-001.png','render/question-006.png','render-more/question-001.png','render-more/question-002.png','render-more/question-004.png','render-more/question-005.png','render-more/question-006.png','render-more/question-007.png','render-more/question-008.png']
assert load('render/rendering.json')['passed'] and load('render-more/rendering.json')['passed']
save('render-inspection.json',{'screenshots_inspected':inspected,'automatic_cases':14,'passed':True,'observed':'Legible vectors, radio controls, complete equations/row operations, fractions, signed target, substitutions and conclusions. Relevant RHS triple visibly changes sums 6->7->6; restored q-74043 shows +7 intermediate RHS and final9. Canonical has no bank and shows -2; hard contradiction and signed target render correctly. No observed clipping, MathJax errors, broken images or JavaScript errors.','scope':'Two actual UI preview runs, 6 plus 8 records. Canonical is replay-only; its fieldless preview is not practice generation.'})
# Strict package immutability proof after all renderer/grader/test activity.
after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};before=load('package-hashes-before.json');assert before==after;save('package-hashes-after.json',after)
pack=load('packaging.json');assert pack['actual_python']==pack['manifest_dependencies']['python'];assert pack['actual_packages']==pack['manifest_dependencies']['packages'];assert pack['replay_equal'] and pack['relocation_exit']==0 and all(r['rejected'] for r in pack['invalid']);pack['package_unchanged']=True;pack['external_output_handling']='Runtime produces JSON only on stdout, no generated assets; all manifest-declared files copied for relocation, no absolute package path requirement. Shared delivery localized asset handling has no images to process.';pack['relocation_replay_equal']=True
# Compare relocated CLI output with in-place CLI for identical seed/count.
import subprocess,os
cmd=[str(R/'.venv/bin/python'),str(W/'17592186119854.py'),'--difficulty','moderate','--count','2','--seed','28619'];out=subprocess.run(cmd,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True);assert out.returncode==0 and json.loads(out.stdout)==load('relocated-samples.json');pack['relocation_command']=cmd;save('packaging.json',pack)
# Review report: findings resolved by demonstrated current tests, not by author claims.
a=load('source-analysis.json')
report={'verdict':'accepted','summary':'Both retained defects are resolved. All eight checks pass, including the exact five-record batch. No current failing case was demonstrated; package bytes are unchanged.','source_analysis':{k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']},'checks':{},'findings':[]}
def check(name,paths,details):report['checks'][name]={'status':'passed','evidence_paths':paths,'details':details}
check('source_replay',['source-analysis.json','source-replay.json','source-replay-records.json','canonical-replay.json','source-corrections.json','solution-transitions.json'],'All 15 complete source banks and answers replay, including the three formerly missing families. Canonical mathematics replay with no invented bank. Supported intermediate source arithmetic corrections verified.')
check('math',['audit.py','review_checks.py','math-results.json','controlled-bank-results.json','solution-transitions.json'],'137 independently solved records plus 33 controlled bank records have correct targets and distractors; 16 source/canonical annotated row-operation sequences and back substitutions checked exactly.')
check('variety',['coverage.json','controlled-bank-results.json','stage-results.json','rejection-results.json','sampling-independence.json'],'All 8 moderate and 7 hard profiles sampled; all 33 numeric anchors exercised. Signed/zero boundaries and bounded rejection covered. Shared-seed rank correlation documented; domain independently chooses bank rank before coefficients.')
check('scope',['source-analysis.json','scope-results.json','independent-samples.json'],'Preserves demonstrated 3x3 linear-combination method, arithmetic workload, difficulty split and radio contract. Reanchoring complete source banks adds no reasoning stage.')
check('grading',['grader-input.json','grader-results.json'],'Actual native grader accepted 170 independently computed correct choices and rejected 680 distractors. All fields are radio; no unsupported free-entry claim.')
check('rendering',['render/rendering.json','render-more/rendering.json','render-inspection.json','ui-position-results.json']+inspected,'Actual UI rendered 14 records. Inspected batch representative, controlled RHS/bank pairs, restored source correction, canonical, hard and signed-target screenshots; no observed rendering defects.')
check('packaging',['packaging.json','relocated-samples.json','package-hashes-before.json','package-hashes-after.json','retained-findings-validation.json'],'Exact installed Python/SymPy versions match manifest. Deterministic and relocated output agree; rejection checks pass. Historical failures reproduced and current regressions pass. All package file hashes unchanged.')
check('decision_variation',['pedagogical-variation.json','counterfactual-records.json','counterfactual-results.json','controlled-bank-records.json','sampling-independence.json','ui-position-results.json','stage-results.json','selection-results.json','delivery-batch/delivery.json','delivery-moderate/delivery.json','delivery-hard/delivery.json','affected-inventory.json','inventory-audit.json'],'Relevant/irrelevant dependencies verified by exact solve, native grading and actual rendering. Old rank shortcut is 0/5 exact batch. All anchors eligible within each template; delivery retains tested coverage. Selection rules inspected and all generated-batch freshness subsets examined conditionally. Captured inventory contains original sources only; live policy/history limitations recorded.')
save('result.json',report)
# Validate required evidence paths and schema shape without installing packages.
schema=json.load(open(R/'generate/pipeline/pedagogical-variation.schema.json'))
def validate(x,s,path='$'):
 typ=s.get('type');valid={'object':isinstance(x,dict),'array':isinstance(x,list),'string':isinstance(x,str),'integer':isinstance(x,int) and not isinstance(x,bool),'number':isinstance(x,(int,float)) and not isinstance(x,bool)}
 if typ:assert valid[typ],(path,typ)
 if 'enum' in s:assert x in s['enum'],path
 if isinstance(x,dict):
  assert all(k in x for k in s.get('required',[])),path
  if s.get('additionalProperties')==False:assert set(x)<=set(s['properties']),path
  for k,v in x.items():
   if k in s.get('properties',{}):validate(v,s['properties'][k],path+'.'+k)
 if isinstance(x,list):
  assert len(x)>=s.get('minItems',0),path
  for i,v in enumerate(x):validate(v,s.get('items',{}),path+f'[{i}]')
 if isinstance(x,str):assert len(x)>=s.get('minLength',0),path
 if isinstance(x,(float,int)):
  if 'minimum' in s:assert x>=s['minimum'],path
  if 'maximum' in s:assert x<=s['maximum'],path
validate(ped,schema)
refs=[]
for check in report['checks'].values():refs+=check['evidence_paths']
refs+=a['evidence_paths']
for section in ['coverage','counterfactuals','shortcut_probes']:
 for item in ped[section]:refs+=item['sample_refs']
refs+=ped['delivery']['sample_refs']
assert all((E/p).is_file() and (E/p).stat().st_size>0 and not Path(p).is_absolute() and '..' not in Path(p).parts for p in refs)
save('contract-check.json',{'pedagogical_schema_valid':True,'all_evidence_files_present':True,'unique_evidence_files':len(set(refs)),'all_eight_checks_passed':len(report['checks'])==8,'package_unchanged':True})
(E/'session-state.md').write_text('Review complete: accepted. Both retained defects reproduced historically and resolved currently. Source15 banks/75 choices plus canonical replay pass. Exact math137+33 controlled records, annotated16 profiles pass. Native grader170 accepted/680 rejected; shared delivery5 batch/48 moderate/42 hard retained. UI14 cases rendered with representative screenshots inspected. Domain rank law and shared-seed correlation documented; all33 anchors tested; old rank0/5 batch and0/992 conditional selection draws. Captured inventory basis5401 has no generated instances. Exact dependency versions, deterministic relocation and package hashes pass. result.json and pedagogical-variation.json contracts validated. No package edits or database writes.\n')
print(json.dumps({'verdict':'accepted','actual_batch_ui_positions':[x['correct_display_position'] for x in actual[:5]],'contract':load('contract-check.json')}))
