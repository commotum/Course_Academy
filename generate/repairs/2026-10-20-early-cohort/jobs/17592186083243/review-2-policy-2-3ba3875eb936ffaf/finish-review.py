from review import *
import subprocess,shutil,collections
E=ROOT;B=E.parent;P=B/'review-1-policy-2-adc52c8c9e3abed7';REPO=Path('/home/jake/Developer/Course_Academy')
manifest=json.loads((PKG/'package.json').read_text());rel=E/'relocated-package';rel.mkdir(exist_ok=True)
for n in manifest['files']+['package.json']:shutil.copy2(PKG/n,rel/n)
cmd=[sys.executable,str(rel/'generator.py'),'--difficulty','easy','--seed','3175644378','--count','5','--format','json']
p=subprocess.run(cmd,capture_output=True,text=True);a=json.loads(json.loads((E/'cli-current.json').read_text())['stdout']);b=json.loads(p.stdout);batch=json.loads((E/'batch.json').read_text())
comparison=[]
for x,y in zip(a,batch):
 qx,qy=x['question'],y['question'];fx,fy=qx[':question/answer-fields'][0],qy[':question/answer-fields'][0]
 comparison.append({'template':x['generation']['template'],'same_parameters':x['generation']['parameters']==y['generation']['parameters'],'same_problem_after_asset_prefix':qx[':question/problem'].replace(str(E/'assets'),'<assets>')==qy[':question/problem'].replace(str(B/'outputs-2'),'<assets>'),'same_solution':qx[':question/worked-solution']==qy[':question/worked-solution'],'same_bank_values':[z[':answer/value'] for z in fx[':answer-field/choices']]==[z[':answer/value'] for z in fy[':answer-field/choices']],'same_correct_value':key(x)==key(y)})
assert a==b and all(all(v for k,v in row.items() if k!='template') for row in comparison)
runtime={'python':platform.python_version(),'packages':{n:importlib.metadata.version(n) for n in manifest['dependencies']['packages']}}
assert runtime==manifest['dependencies']
save('current-runtime.json',runtime)
save('current-packaging.json',{'command':cmd,'exit_code':p.returncode,'relocation_exact_equal_same_output_root':a==b,'actual_batch_content_comparison':comparison,'runtime_matches_manifest':True,'raw_ids_note':'Illustrated raw IDs include the asset output prefix. Normalized prompt, bank and solution match runner batch; relocating at same output root preserves all record bytes.'})
hard=json.loads((E/'fresh-hard.json').read_text())[0];m=hard['generation'];same=hard==g.generate('hard',m['seed'],m['template'],parameters=m['parameters']);assert same
save('current-determinism.json',{'same_seed_equal':same,'cli_same_output_root_relocation_equal':a==b,'runner_batch_content_equal_after_asset_prefix':True,'raw_identity_note':'Directory-dependent raw plot IDs are normalized at delivery. The initial copied test accidentally compared different seeds; corrected using saved record seed.'})
code=(E/'variation.py').read_text().split("rs=json.load(open('samples-independent.json'))")[0];exec(code,globals())
accepted=json.loads((E/'delivery-batch/accepted.json').read_text());fresh=json.loads((E/'fresh-easy.json').read_text());fd=json.loads((E/'delivery-fresh/accepted.json').read_text())
ui=[]
for i,r in enumerate(batch):
 f=r['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  h=Radios();h.feed((E/f'render-current/question-{i+1:03}.html').read_text());ui.append({'question_id':r['question'][':question/id'],'correct_position':h.ids.index(f[':answer-field/correct'][1])+1})
save('current-shortcuts.json',{'raw_batch':metrics(batch),'delivered_batch':metrics(accepted),'fresh':metrics(fresh),'delivered_fresh':metrics(fd),'actual_ui_positions':ui})
draws=[]
for i in range(40):
 seed=f'independent-review-{i}';digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();draw=(int.from_bytes(digest[8:16],'big')>>11)/2**53;j=int(draw*len(accepted));draws.append({'seed':seed,'synthetic_entity':j+1,'question_id':accepted[j]['question'][':question/id']})
save('current-selection.json',{'basis':5644,'rules':'learning.rs validate_practice_question excludes retired/free/multistep. question_selection.rs uses weighted difficulty then uniform member of sorted fresh eligible pool. Reconfirmed current source lines 149-169 and select implementation.','assumptions':'All five delivered easy records fresh; positive easy weight; synthetic entities preserve candidate order. Future IDs and learner history unavailable. Unconfigured distribution chooses first candidate.','draws':draws,'counts':dict(collections.Counter(x['question_id'] for x in draws)),'result':'Every current batch case selectable under stated fresh-band assumptions.'})
v=json.loads((E/'pedagogical-variation.json').read_text())
for c in v['counterfactuals']:c['sample_refs']=[('current-grader-results.json' if x=='remaining-grader-results.json' else x) for x in c['sample_refs']]
v['limitations']=[x for x in v['limitations'] if not x.startswith('Separate native grading failure')]
v['limitations'].append('Unchanged construction and counterfactual render evidence reused with provenance; native grader suite rerun against repaired engine. Both retained exponential findings now pass.')
v['delivery']['sample_refs'] += ['regression-delivered-grader-result.json','current-grader-results.json']
v['delivery']['result']='Current batch 5/5 and fresh easy 5/5 survive actual filtering. Eight targeted hard regression records survive their hard filter. Raw/delivered cue coverage agrees. Current UI radio positions '+str([x['correct_position'] for x in ui])+'. Selection conditional on captured inventory, fresh candidates and positive easy weight.'
save('pedagogical-variation.json',v)
save('current-render-inspection.json',{'report':'render-current/rendering.json','screenshots_inspected':['render-current/question-001.png','render-current/question-002.png','render-current/question-006.png'],'result':'Inspected plot, mathematical blank, radio options, derivative steps and rational exponential solution. All legible, no broken math or overlapping controls. Six current actual-UI cases pass. Unchanged controlled-pair renderer artifacts reused.'})
invhash=hashlib.sha256((B/'source/inventory.json').read_bytes()).hexdigest();prevhash=json.loads((P/'delivery-batch/delivery.json').read_text())['input_sha256']['inventory'];assert invhash==prevhash
save('current-inventory-review.json',{'basis':5644,'sha256':invhash,'captured_inventory_matches_previous':True,'conclusion':'Five non-source stored records are selectable trigonometric questions. No generated reciprocal-exponential blank exists in captured pool, so no stored generated instance of either retained defect. Original source records remain distinct. This verifies absence of this specific affected family only.','evidence':'inventory-review.json'})
save('affected-inventory.json',{'affected_questions':[]})
# Verify original author regressions retain both strict failures and negative controls.
inputs=json.loads((E/'regression-grader-input.json').read_text());checks=[c for r in inputs for c in r['checks']]
for val in ['8/(5*sqrt(5)*exp(1/2))','8*exp(-1/4)*exp(-1/4)/(5*sqrt(5))']:
 assert any(c.get('submitted')==val and c['expected']=='accepted' for c in checks)
save('repair-review.json',{'retained_findings':[x['id'] for x in json.loads((E/'repair-history-findings.json').read_text())],'preflight':'repair-preflight-captured.json','verification':'Read both retained findings and author executable checks. The strict old-failure inputs are present, with wrong-sign, wrong-factor and wrong-exponent rejection controls. Prior independent failure logs retained. Adapted author checks only redirect imports/output into evidence_root; current native execution passes before and after delivery. Independent fresh probes and full retained suite also pass.','prior_failing_evidence':['minimal-grader-execution.json','grading-failure-execution.json'],'current_evidence':['regression-result.json','regression-grader-result.json','regression-delivered-grader-result.json','current-grader-results.json','fresh-engine-results.json']})
after={str(p.relative_to(PKG)):hashlib.sha256(p.read_bytes()).hexdigest() for p in PKG.rglob('*') if p.is_file()};save('package-after.json',after);assert after==json.loads((E/'package-before.json').read_text())
save('package-integrity.json',{'unchanged':True,'files_checked':len(after),'manifest':manifest,'before':'package-before.json','after':'package-after.json'})
(E/'session-state.md').write_text('Completed: confirmed source account; 22 current source replays; 14 fresh/batch math records; 8 targeted hard regressions; full native grader suite 786 checks; 21 independent multiplicity probes; actual delivery batch 5/5, fresh easy 5/5, hard 8/8; six current UI renders, three screenshots visually inspected; reused unchanged controlled-pair renders; exact runtime, CLI replay, relocation, selection and inventory eligibility. Package hashes unchanged. Both retained findings resolved. Final evidence contract pending.\n')
print('Final checks passed; UI positions',[x['correct_position'] for x in ui])
