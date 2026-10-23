import json,pathlib,re,hashlib,collections
R=pathlib.Path(__file__).resolve().parent;J=R.parent;P=J/'workspace';REPO=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.loads((R/p).read_text())
def save(p,x):(R/p).write_text(json.dumps(x,indent=2)+'\n')
def key(f):return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
def groups(records):
 out=collections.defaultdict(list)
 for r in records:
  q=r['question'];f=q[':question/answer-fields'][0]
  if not f[':answer-field/type'].endswith('/radio'):continue
  cells=[tuple(map(int,re.search(r'_\{(\d)(\d)\}',a[':answer/value']).groups())) for a in f[':answer-field/choices']]
  target=tuple(map(int,re.search(r'_\{(\d)(\d)\}',key(f)).groups()))
  # Visible bank, dimensions and wording; do not rely on hidden profile for grouping.
  body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)[1];rows=body.split(r'\\');shape=(len(rows),len(rows[0].split('&')))
  sig=str((shape,sorted(cells),'inline' if '$$' not in q[':question/problem'] else 'display'))
  out[sig].append({'record':r,'target':target,'serialized_position':cells.index(target),'sorted_role':sorted(cells).index(target)})
 return [{'signature':s,'distinct_targets':len(set(tuple(x['target']) for x in xs)),'observations':xs} for s,xs in out.items()]
stages={}
for tag,f in [('exact_raw','batch.json'),('exact_delivered','current-delivery-batch/accepted.json'),('fresh_raw','current-fresh-batches.json'),('fresh_delivered','current-delivery-fresh/accepted.json')]:
 rs=load(f);stages[tag]={'count':len(rs),'groups':groups(rs)}
assert all(g['distinct_targets']>=2 for v in stages.values() for g in v['groups'])
save('current-delivery-analysis.json',{'stages':stages,'generator_domain':'Code inspected: choose bank before target, require at least two in-matrix targets; pair radio targets and shuffle output. No rejection loop secretly constrains correct roles.','filter':'Actual shared publisher helper used against captured basis 5667. Three repeated items in the overlapping fresh-seed batches were deduplicated; all surviving bank groups retain distinct targets.','selection':'Retired/incomplete questions are ineligible; prior-task and current-prefix items are excluded. Positive difficulty weights select a band and hash chooses within band. No supplied learner history or weights; no claim of a balanced individual sequence.','publication_preparation_present':(J/'publication/preparation.json').exists()})
# Current rendering order is UI-controlled and distinct from serialized order.
render=load('current-render/rendering.json');batch=load('current-delivery-batch/accepted.json');positions=[]
for c,r in zip(render['cases'][:5],batch):
 if 'Choose an answer' not in c['text']:continue
 t=c['text'].split('Choose an answer',1)[1].split('Correct choice selected.',1)[0]
 positions.append({'record':r,'render_index':c['index']+1,'correct_displayed_position_zero_based':t.count('Incorrect choice left unselected.')})
save('current-rendered-positions.json',{'observations':positions,'rule':'Actual UI hashes item seed and answer identity; live item IDs unavailable. Current preview correct positions are 3,3,4,4 (one-based), with both positions in each bank subgroup.'})
# Update prior pedagogical account, retaining source-based justifications and unchanged broad evidence.
v=json.loads((J/'review-1-policy-2-51ba951d744c2d08/pedagogical-variation.json').read_text())
for section in ['coverage','counterfactuals','shortcut_probes']:
 for x in v[section]:x['sample_refs']=['current-native-report.json' if f=='pair-grader-report.json' else f for f in x['sample_refs']]
v['coverage'][-1]['result']='5/5 exact candidates survive current delivery: two radio bank groups each with contrasting targets, and one symbolic blank. Compact and comma-separated indices both grade correctly.'
v['coverage'].append({'case':'Fresh engine-repair regression sample','sample_refs':['current-fresh-batches.json','current-symbolic-controls.json','current-native-input.json','current-native-report.json','current-math.json'],'result':'Fresh seeds 983041/983042, symbolic corners and off-diagonals, and source replays independently verified. 774 strict native checks pass, including retained expectations.'})
for kind,a,b in [('relevant',4,5),('irrelevant',4,6)]:
 v['counterfactuals'].append({'kind':kind,'change':'Move box from (2,3) to (3,2) in fixed A matrix.' if kind=='relevant' else 'Replace matrix entries by ones, retaining A and boxed coordinate (2,3).','expected':'Old a_{2,3} rejected; a_{3,2} accepted; prompt and explanation follow box.' if kind=='relevant' else 'a_{2,3} still accepted; solution value changes from -2 to 1.','observed':'Native outcomes meet expectations and rendered prompt, blank and worked solution track coordinates and values.','status':'passed','justification':'First subscript is row and second column; cell values do not define indices (tutorial 34f3a63d-a273-50fb-b26a-ae172c7e93e9).','sample_refs':['current-symbolic-controls.json','current-native-input.json','current-native-report.json','current-render-controls/rendering.json','current-render-controls/question-001.png','current-render-controls/question-002.png' if kind=='relevant' else 'current-render-controls/question-003.png']})
# Preserve inherited probes as inherited; add explicit current exact/fresh and actual-UI probes.
for tag in ['exact_delivered','fresh_delivered']:
 for group in stages[tag]['groups']:
  obs=group['observations']
  for attr in ['serialized_position','sorted_role']:
   hits=sum(x[attr]==0 for x in obs)
   v['shortcut_probes'].append({'cue':'option position' if attr=='serialized_position' else 'smallest bank coordinate','subgroup':tag+' '+group['signature'],'scope':'other_recognizable_subgroup','strategy':'Select first serialized option' if attr=='serialized_position' else 'Select smallest row-major coordinate without inspecting box','correct':hits,'total':len(obs),'baseline':0.2,'disposition':'not_predictive','conclusion':'Uniform five-choice guessing baseline is 0.2. These small conditional probes have counterexamples and do not prove absence of other cues. Serialized order is distinguished from actual UI order.','sample_refs':['current-delivery-analysis.json']})
for profile in ('q-13489','q-13499'):
 obs=[x for x in positions if x['record']['generation']['profile']==profile]
 v['shortcut_probes'].append({'cue':'actual rendered position','subgroup':'exact delivered '+profile+' visible bank','scope':'other_recognizable_subgroup','strategy':'Always choose third displayed option','correct':sum(x['correct_displayed_position_zero_based']==2 for x in obs),'total':len(obs),'baseline':0.2,'disposition':'not_predictive','conclusion':'Five-choice random baseline 0.2; each bank has a third-position and fourth-position correct answer. Live item-seeded order can differ.','sample_refs':['current-rendered-positions.json','current-render/rendering.json']})
d=load('current-fresh-cue.json')
v['shortcut_probes'].append({'cue':'q13498 recognizable bank shape','subgroup':'fresh delivered matching banks','scope':'other_recognizable_subgroup','strategy':'Choose middle column in smallest row without locating highlight','correct':d['correct'],'total':d['attempts'],'baseline':0.2,'disposition':'not_predictive','conclusion':'1/3 versus five-choice random baseline 0.2; two counterexamples to formerly perfect shortcut. Exact runner batch has no matching bank, so this control is necessary.','sample_refs':['current-fresh-cue.json','current-delivery-fresh/accepted.json']})
v['delivery']['sample_refs']+=['current-delivery-batch/delivery.json','current-delivery-fresh/delivery.json','current-delivery-analysis.json']
v['delivery']['result']='Current exact batch 5/5 survives; fresh overlapping-seed candidates 7/10 survive with contrasting bank targets. Previous bound broader sample retains 32/40 fresh and 46/56 controlled records. Generator construction, requested difficulty, shared filtering, captured inventory and selection rules examined. Individual history may remove previously seen partners.'
v['limitations']=[x for x in v['limitations'] if 'rejects valid comma-separated' not in x]
v['limitations'].append('Earlier broader evidence is reused with provenance because runtime/source/batch/inventory bindings match. Native outcomes were rerun against the changed engine; scope remains easy only.')
save('pedagogical-variation.json',v)
# Inventory identity verification; inspect every original flag and the additional complete record.
inv=json.loads((J/'source/inventory.json').read_text());original={q[':question/id'] for q in json.loads((J/'source/source.json').read_text())['material']['kp'][':knowledge-point/questions']}
assert hashlib.sha256((J/'source/inventory.json').read_bytes()).hexdigest()==load('delivery-batch/delivery.json')['input_sha256']['inventory']
assert len(inv['questions'])==10
extra=[q for q in inv['questions'] if q[':question/id'] not in original];assert len(extra)==1
save('current-inventory-verification.json',{'basis':inv['basis'],'inventory_byte_hash_matches_previous':True,'question_count':10,'non_source_records':extra,'conclusion':'Rechecked current captured inventory against bound earlier inspection. The sole additional row uses separate numeric indices (1,1), with box and solution matching. No symbolic or radio field and no generation metadata: no demonstrated generated stored-record defect. Nine originals are not marked generated.','limits':'Only captured inventory basis 5667. No later pool or learner-history claim.'})
save('affected-inventory.json',{'affected_questions':[]})
sel=load('selection-analysis.json');sel['application']='All five easy candidates pass current delivery. Both radio groups retain distinct targets; symbolic blank passes current native grading. Selection rules do not guarantee per-learner sequence balance after history exclusions.';save('selection-analysis.json',sel)
ret=json.loads((J/'review-1-policy-2-51ba951d744c2d08/retained-findings-review.json').read_text())
ret['findings'][0]['evidence']=['old-failing-cue-execution.json','current-fresh-cue.json','controlled-records-cue.json','current-delivery-analysis.json']
ret['findings'][1]['now']='Current rerun accepts compact symbolic notation; source family remains in default practice. Comma repair also passes strict native checks.'
ret['findings'][1]['evidence']=['prior-grader-symbolic-strict-execution.json','current-native-input.json','current-native-report.json']
ret['findings'].append({'id':'34e5515d1b3374bbde8b','before':'Copied independent prior-engine execution strictly fails the exact delivered c_{2,2} case. This failure evidence is bound to the preceding engine and reused, not invented or rerun on repaired engine.','now':'Unchanged strict case is included in current-native-input.json and accepted. Wrong comma coordinates, labels, extra components and unbraced TeX remain rejected. Author executable current-CLI regression independently rerun with output paths redirected under evidence_root.','evidence':['comma-strict-execution.json','comma-strict-input.json','current-native-report.json','author-rerun/comma/summary.json','author-rerun/comma/commands.json']})
ret['author_checks']='Read all four retained findings and repair-preflight.json. Earlier independent baseline-failure executions reused for unchanged source/shortcut repairs; bank-cue failure additionally rerun on preserved failing batch. New comma check rerun on current output via minimally redirected copies. Passing author checks supplement 774 independently specified native checks.'
save('retained-findings-review.json',ret)
save('review-inputs.json',{'repair_preflight':json.loads((J/'repair-preflight.json').read_text()),'retained_findings':[x['id'] for x in json.loads((J/'repair-history.json').read_text())['findings']],'author_script_redirection':'Only W and E path assignments changed in copied check_repair.py/check_index_notation.py; package code untouched.'})
# Schema and all root-relative references.
import jsonschema
jsonschema.validate(v,json.loads((REPO/'generate/pipeline/pedagogical-variation.schema.json').read_text()))
refs=v['delivery']['sample_refs']+[f for section in ['coverage','counterfactuals','shortcut_probes'] for x in v[section] for f in x['sample_refs']]
assert all(not pathlib.Path(f).is_absolute() and (R/f).is_file() and (R/f).stat().st_size for f in refs)
save('variation-validation.json',{'schema':'passed','sample_refs_nonempty':True,'references':len(refs),'probes':len(v['shortcut_probes'])})
print(json.dumps({'schema':'passed','probes':len(v['shortcut_probes']),'reference_count':len(refs),'current_delivery_groups':{tag:[g['distinct_targets'] for g in val['groups']] for tag,val in stages.items()}}))
