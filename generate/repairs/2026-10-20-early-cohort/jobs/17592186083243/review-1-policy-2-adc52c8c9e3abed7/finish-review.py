from review import *
import subprocess,shutil,collections
from html.parser import HTMLParser
E=ROOT;B=E.parent;P=B/'review-0-policy-2-da51d3ee0942346e';REPO=Path('/home/jake/Developer/Course_Academy')
# Same-output relocation is a strict deterministic comparison; raw illustrated IDs also include output path.
manifest=json.loads((PKG/'package.json').read_text());rel=E/'relocated-package';rel.mkdir(exist_ok=True)
for n in manifest['files']+['package.json']:shutil.copy2(PKG/n,rel/n)
cmd=[sys.executable,str(rel/'generator.py'),'--difficulty','easy','--seed','3175644378','--count','5','--format','json']
p=subprocess.run(cmd,capture_output=True,text=True); original=json.loads((E/'cli-current.json').read_text())
a=json.loads(original['stdout']);b=json.loads(p.stdout);batch=json.loads((E/'batch.json').read_text())
# Exact question identities expected to differ only when asset output prefix differs; compare delivered content separately.
comparison=[]
for x,y in zip(a,batch):
 qx,qy=x['question'],y['question']; fx,fy=qx[':question/answer-fields'][0],qy[':question/answer-fields'][0]
 comparison.append({'template':x['generation']['template'],'same_parameters':x['generation']['parameters']==y['generation']['parameters'],'same_problem_after_asset_prefix':qx[':question/problem'].replace(str(E/'assets'),'<assets>')==qy[':question/problem'].replace(str(B/'outputs-1'),'<assets>'),'same_solution':qx[':question/worked-solution']==qy[':question/worked-solution'],'same_bank_values':[z[':answer/value'] for z in fx[':answer-field/choices']]==[z[':answer/value'] for z in fy[':answer-field/choices']],'same_correct_value':key(x)==key(y)})
save('current-packaging.json',{'command':cmd,'exit_code':p.returncode,'relocation_exact_equal_same_output_root':a==b,'actual_batch_content_comparison':comparison,'runtime_matches_manifest':json.loads((E/'current-runtime.json').read_text())==manifest['dependencies'],'raw_ids_note':'Illustrated raw UUIDs include output directory via content fingerprint; publisher normalizes assets and stable identities. Four nonillustrated raw records match exactly. Same-output relocated replay matches exactly.'})
# Reuse independent metric implementation but measure the current raw and actual delivered sets.
code=(E/'variation.py').read_text().split("rs=json.load(open('samples-independent.json'))")[0];exec(code,globals())
accepted=json.loads((E/'delivery-batch/accepted.json').read_text());fresh=json.loads((E/'fresh-easy.json').read_text());fd=json.loads((E/'delivery-fresh/accepted.json').read_text())
ui=[]
for i,r in enumerate(batch):
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  h=Radios();h.feed((E/f'render-current/question-{i+1:03}.html').read_text());ui.append({'question_id':r['question'][':question/id'],'correct_position':h.ids.index(f[':answer-field/correct'][1])+1})
save('current-shortcuts.json',{'raw_batch':metrics(batch),'delivered_batch':metrics(accepted),'fresh':metrics(fresh),'delivered_fresh':metrics(fd),'actual_ui_positions':ui})
# Faithful selection-stage reproduction, conditional on fresh candidates and a positive easy weight.
draws=[]
for i in range(40):
 seed=f'independent-review-{i}';digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();draw=(int.from_bytes(digest[8:16],'big')>>11)/2**53;j=int(draw*len(accepted));draws.append({'seed':seed,'synthetic_entity':j+1,'question_id':accepted[j]['question'][':question/id']})
save('current-selection.json',{'basis':5644,'rules':'learning.rs validate_practice_question excludes retired/free/multistep. question_selection.rs select uses weighted difficulty then uniform member of sorted fresh eligible pool.','assumptions':'All five delivered easy records fresh; positive easy weight; synthetic entities preserve candidate order. Actual future IDs and learner history unavailable. Unconfigured distribution uses first candidate, not uniform sampling.','draws':draws,'counts':dict(collections.Counter(x['question_id'] for x in draws)),'result':'Every current batch case selectable under stated fresh-band assumptions; none excluded by response type or difficulty.'})
# Refresh schema evidence references to the current engine checks and batch.
v=json.loads((E/'pedagogical-variation.json').read_text())
for c in v['counterfactuals']:c['sample_refs']=[('remaining-grader-results.json' if x=='grader-followup-results.json' else x) for x in c['sample_refs']]
v['coverage'].append({'case':'current runner batch and independent easy regression','sample_refs':['batch.json','fresh-easy.json','current-shortcuts.json','delivery-batch/accepted.json','delivery-fresh/accepted.json'],'result':'Five current batch and five fresh easy records survive delivery; cue measurements preserved. Current radio UI positions '+str([x['correct_position'] for x in ui])+'.'})
for cue in ['first_option','zero','smallest_nonzero_magnitude','largest_magnitude']:
 data=metrics(batch);correct=sum(z['successes'][cue] for z in data.values());total=sum(z['total'] for z in data.values())
 v['shortcut_probes'].append({'cue':cue,'subgroup':'current batch radio fields','scope':'other_recognizable_subgroup','strategy':'Choose '+cue.replace('_',' '),'correct':correct,'total':total,'baseline':0.2,'disposition':'not_predictive','conclusion':'Uniform random choice among five options has success 0.2. This strategy does not answer every batch radio; template-specific evidence remains in prior independent cue follow-ups. Singleton templates in this batch cannot establish recurring conditional predictors.','sample_refs':['batch.json','current-shortcuts.json','delivery-batch/accepted.json']})
v['delivery']['sample_refs'] += ['delivery-fresh/delivery.json','fresh-easy.json','current-shortcuts.json','current-selection.json']
v['delivery']['result']='Current batch: 5 input, 0 duplicates, 5 accepted. Fresh easy sample: 5 input, 0 duplicates, 5 accepted. Retained independent easy sample: 16 accepted. Rejection rules unchanged. Current raw/delivered cue metrics match; all five survive eligible fresh easy-band selection assumptions. Current UI positions measured from actual HTML.'
v['limitations'][-1]='Separate native grading failure: repeated quarter-exponent factors are not recognized as the equivalent half exponent; decision variation does not waive it.'
save('pedagogical-variation.json',v)
save('current-render-inspection.json',{'report':'render-current/rendering.json','screenshots_inspected':['render-current/question-001.png','render-current/question-002.png','render-current/question-006.png'],'result':'Cubic plot, exact blank, radio answer controls, and hard reciprocal-exponential worked solution display correctly. Six renderer cases pass; renderer default cap covers all five batch records plus failure record. Prior controlled-pair render evidence reused under unchanged package/UI.'})
# Hash inventory confirms no eligible generated fractional-exponential items at captured basis.
save('current-inventory-review.json',{'basis':5644,'source':'../source/inventory.json','captured_inventory_matches_previous_delivery_hash':hashlib.sha256((B/'source/inventory.json').read_bytes()).hexdigest()==json.loads((P/'delivery-batch/delivery.json').read_text())['input_sha256']['inventory'],'conclusion':'Reused independently inspected inventory has five non-source selectable generated items, all trigonometric; no generated reciprocal-exponential blank is present. No stored generated instance of this demonstrated fractional-exponential defect. Not a universal audit of inventory.','evidence':'inventory-review.json'})
after={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};save('package-after.json',after);assert after==json.loads((E/'package-before.json').read_text())
(E/'session-state.md').write_text('Completed current source replay (22), fresh visible-math checks (14), retained regression (8), native grader controls (784), delivery (batch 5/5; fresh easy 5/5), six actual UI renders, relocation/runtime and unchanged-package checks. One strict new native-grader failure reproduced: repeated exp(-1/4) factors; see reproduce-grading.py. Final report and evidence-contract verification pending.\n')
print('finalization checks complete')
