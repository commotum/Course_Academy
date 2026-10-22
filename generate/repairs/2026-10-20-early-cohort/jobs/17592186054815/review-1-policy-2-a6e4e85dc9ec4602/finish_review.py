import sys
sys.dont_write_bytecode=True
from review import *
from html.parser import HTMLParser
class RadioInputs(HTMLParser):
 def __init__(self):super().__init__();self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='input' and a.get('type')=='radio':self.ids.append(a['value'])
def fnv(s):
 n=2166136261
 for c in s:n=((n^ord(c))*16777619)&0xffffffff
 return n

def main():
 batch=load('batch-records.json');raw=[]
 for i,r in enumerate(batch):
  if r['generation']['response_contract']!='radio':continue
  q=r['question'];f=q[':question/answer-fields'][0];aid=f[':answer-field/correct'][1]
  dom=RadioInputs();dom.feed((E/f'render-batch/question-{i+1:03d}.html').read_text())
  choices=f[':answer-field/choices'];ids=[a[':answer/id'] for a in sorted(choices,key=lambda a:fnv(f"{i+1}:{f[':answer-field/id']}:{a[':answer/id']}"))];assert dom.ids==ids
  raw.append({'batch_index':i,'profile':r['generation']['profile'],'raw_correct_position':next(i+1 for i,a in enumerate(choices) if a[':answer/id']==aid),'rendered_correct_position':dom.ids.index(aid)+1,'dom_choice_ids':dom.ids,'question_id':q[':question/id']})
 assert [x['rendered_correct_position'] for x in raw if x['profile']=='Z0+']==[4,3]
 # Also show item identity varies the actual UI position rather than fixing an answer slot.
 identity_trials=[]
 for r in batch:
  if r['generation']['response_contract']!='radio':continue
  f=r['question'][':question/answer-fields'][0];aid=f[':answer-field/correct'][1];positions=[]
  for itemid in range(1,33):
   cs=sorted(f[':answer-field/choices'],key=lambda a:fnv(f"{itemid}:{f[':answer-field/id']}:{a[':answer/id']}"));positions.append(next(i+1 for i,a in enumerate(cs) if a[':answer/id']==aid))
  identity_trials.append({'question_id':r['question'][':question/id'],'item_ids':list(range(1,33)),'correct_positions':positions})
 save('ui-choice-order-checks.json',{'command':PY+' -B finish_review.py','source':'ui/learning.js:690 choiceOrder; fieldControl uses task itemId or preview contentId and field ID','actual_ui_batch':raw,'item_identity_trials':identity_trials,'conclusion':'Raw second-position match in both Z0+ records is absent in actual UI: 4th/3rd in exact batch fixture; changing task item identity changes order again. No learner-visible fixed second-position action demonstrated.','limits':'Preview item IDs 1..5, not live task reservation IDs. Live ordering uses same hash rule with those actual item IDs.'})
 p=load('pedagogical-variation.json')
 for probe in p['shortcut_probes']:
  if probe['sample_refs']==['batch-records.json'] and probe['subgroup']=='radio:Z0+' and probe['strategy']=='radio position 2':
   probe['conclusion']='2/2 in raw bank order versus a .2 uniform offered-choice baseline, but raw order is not the learner order. Actual unmodified UI shows correct positions fourth/third; the fixed second-position strategy succeeds 0/2 there. This is not a delivered incidental cue.';probe['sample_refs']+=['ui-choice-order-checks.json','render-batch/rendering.json']
  if probe['strategy']=='sign and zero only' and probe['correct']==probe['total'] and probe['total']>1 and probe['disposition']=='not_predictive':
   probe['conclusion']+=' This small sampled subgroup happens to match sign-only classification; controlled rational/integer cases and Q0+ versus R0+ counterfactuals require the omitted class decision.';probe['sample_refs']+=['counterfactual-records.json','controlled-records.json']
 for pos in range(1,6):
  z=[x for x in raw if x['profile']=='Z0+'];p['shortcut_probes'].append({'cue':'actual UI answer position','subgroup':'exact batch Z0+ radio','scope':'within_template','strategy':f'Choose visible position {pos}','correct':sum(x['rendered_correct_position']==pos for x in z),'total':len(z),'baseline':.2,'disposition':'not_predictive','conclusion':'Uniform offered-choice baseline .2. Exact batch correct controls appear at positions fourth and third; no fixed position succeeds on both.','sample_refs':['batch-records.json','ui-choice-order-checks.json','render-batch/rendering.json']})
 p['delivery']['stages_examined'].append('actual UI choice reordering');p['delivery']['sample_refs']+=['ui-choice-order-checks.json','render-batch/rendering.json'];p['delivery']['result']+=' Raw position coincidence in the two Z0+ radio batch members is broken by the actual UI choice order.'
 save('pedagogical-variation.json',p)
 inspected=['render/question-001.png','render/question-003.png','render/question-005.png','render/question-006.png','render/question-007.png','render/question-009.png','render/question-010.png','render/question-012.png','render-batch/question-002.png','render-batch/question-004.png']
 for name in ['render/rendering.json','render-batch/rendering.json']:assert load(name)['passed']
 save('render-inspection.json',{'automated_cases':17,'screenshots_visually_inspected':inspected,'result':'Clear math and sign/zero subscripts, radical bars, fractions, complete radio labels and checkboxes; source repaired delimiters and check/cross marks display correctly. Solutions readable without clipping. Relevant target-change and irrelevant magnitude-change pairs display consistent decisions. Batch Z0+ radio choice orders inspected directly.','counterfactual_comparisons':[{'before':'render/question-005.png','relevant_after':'render/question-006.png','irrelevant_after':'render/question-007.png','result':'radio Q0+ selects I/III; R0+ adds II; replacing 1/2 by 3/4 preserves I/III.'},{'before':'render/question-008.png','relevant_after':'render/question-009.png','irrelevant_after':'render/question-010.png','result':'checkbox counterparts have same relationship, including updated worked solutions.'}]})
 (E/'session-state.md').write_text('Completed: 11 source replays and canonical numeric case; 216 independent math/solution records, 430 exact identities; 154 controlled cases; 32 fresh and exact 5 batch; 1458 native grader checks; 200 independent + 5 batch delivery survivors; 17 actual UI renders and 10 screenshots inspected. Relevant/irrelevant counterfactuals pass. Raw Z0+ radio position cue disproven at actual UI (4th/3rd). Captured inventory retained-defect audit found no affected generated records. Final package integrity and evidence contract next.\n')
 # Exact dependency and integrity evidence is independent of author's manifest reports.
 before=load('package-hashes-before.json');after={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};assert before==after
 save('package-integrity.json',{'unchanged':True,'files_checked':len(before),'before':before,'after':after,'database_writes':0,'asset_publications':0})
 checks={
 'source_replay':(['source-analysis.json','source-replay-checks.json','source-acceptance-old.json','source-acceptance-current.json','retained-check-execution.json'],'All 11 original cases and complete ordered banks replay. Prior strict regression fails original and passes revision. Missing key/solution on 59f3318f explicitly disclosed; II only independently derived. Canonical numeric membership tested separately.'),
 'math':(['math-checks.json','replay-records.json','canonical-records.json','review.py'],'216 records, 864 solution bullets and 430 exact identities/conversions checked independently from visible TeX. Keys, distractors, classifications, and authored conclusions agree.'),
 'variety':(['coverage.json','controlled-records.json','fresh-records.json','source-replay-checks.json'],'154 controlled cases cover all masks for every radio target and both restored checkbox targets, plus retained checkbox boundaries. Both response modes and all seven source profiles supported.'),
 'scope':(['source-analysis.json','scope-checks.json'],'Four elementary real-number candidates, class/sign/zero reasoning and original response workload retained at easy difficulty.'),
 'grading':(['grader-input.json','grader-report.json','counterfactual-checks.json'],'Actual native grader: 522 acceptances and 936 rejections match independent expected outcomes. Every offered choice and both checkbox states exercised, including counterfactuals. No free-entry fields apply.'),
 'rendering':(['render/rendering.json','render-batch/rendering.json','render-inspection.json','render/question-005.png','render/question-006.png','render-batch/question-002.png','render-batch/question-004.png'],'17 actual UI renders pass; ten screenshots visually inspected, including restored sources, both counterfactual modes and exact batch members.'),
 'packaging':(['packaging-checks.json','package-integrity.json','commands.json'],'Exact installed Python 3.13.5 and empty packages contract match. Determinism, declared-files-only relocation, unsupported difficulty/negative count and zero-count boundaries pass; package unchanged.'),
 'decision_variation':(['pedagogical-variation.json','delivery-selection-checks.json','counterfactual-records.json','ui-choice-order-checks.json','inventory-review.json','affected-inventory.json'],'Independent role analysis, controlled changes and conditional shortcut probes pass. Actual delivery keeps 200 independent and all five runner records. Exact batch has five masks; raw Z0+ position coincidence does not survive UI reordering. Captured selection branches/history limits documented.')}
 a=load('source-analysis.json');a={k:a[k] for k in ['skill','reasoning_steps','invariants','permitted_variations','source_refs','evidence_paths']}
 result={'verdict':'accepted','summary':'Both retained replay defects are resolved. All eight checks pass; no demonstrated current defect. Exact batch and actual UI assessed separately. Package unchanged. Selection conclusions are bounded to the captured inventory and documented policy/history scenarios.','source_analysis':a,'checks':{k:{'status':'passed','evidence_paths':v[0],'details':v[1]} for k,v in checks.items()},'findings':[]}
 save('result.json',result)
 # Validate exact supplied pedagogy schema, plus all evidence links and sample references.
 schema_path=REPO/'generate/pipeline/pedagogical-variation.schema.json'
 validation=subprocess.run(['python3','-c','import json,jsonschema,sys;jsonschema.validate(json.load(open(sys.argv[1])),json.load(open(sys.argv[2])))',str(E/'pedagogical-variation.json'),str(schema_path)],capture_output=True,text=True)
 assert validation.returncode==0,validation.stderr
 paths=[]
 for c in result['checks'].values():paths+=c['evidence_paths']
 paths+=a['evidence_paths']
 for collection in ['coverage','counterfactuals','shortcut_probes']:
  for obj in p[collection]:paths+=obj['sample_refs']
 paths+=p['delivery']['sample_refs']
 for path in paths:
  f=E/path;assert f.is_file() and f.stat().st_size>0 and f.resolve().is_relative_to(E),path
 save('evidence-contract.json',{'passed':True,'pedagogical_variation_schema':'generate/pipeline/pedagogical-variation.schema.json','nonempty_evidence_links_checked':len(set(paths)),'eight_checks_passed':True,'findings':0})
 (E/'session-state.md').write_text('Review complete: accepted. Both retained defects reproduced on original and absent in current. All eight checks pass with result.json and evidence-contract.json. Package hashes unchanged; no database writes or publication. Captured policy/history limitations documented.\n')
 print(json.dumps({'verdict':result['verdict'],'checks':list(result['checks']),'package_unchanged':True,'evidence_contract':'passed'}))
if __name__=='__main__':main()
