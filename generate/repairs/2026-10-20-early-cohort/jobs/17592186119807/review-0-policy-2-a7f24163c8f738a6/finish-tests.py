import sys,os
sys.dont_write_bytecode=True
import audit as a
import json,pathlib,collections,hashlib,copy,uuid,subprocess,shutil
E=a.E;g=a.g;sp=a.sp;save=a.save
catalog=a.load(E/'catalog.json');accepted=a.load(E/'delivery-catalog/accepted.json');batch=a.load(E/'delivery-batch/accepted.json')
# Same coefficient matrix, one relevant component changed: consistency must switch.
r0=g.generate('moderate',83,'q-34568',{'translation':0});u,v,b=a.vectors(r0);b2=sp.Matrix(b);b2[2]=7
r1=copy.deepcopy(r0);q=r1['question']; old=q[':question/problem'];matches=list(g.MATRIX.finditer(old));m=matches[2];q[':question/problem']=old[:m.start()]+g.tex(b2)+old[m.end():]
x=sp.Matrix([1,1]);q[':question/worked-solution']=g.render_solution('q-34568',u,v,b2,x,sp.Integer(7),True)
q[':question/id']=str(uuid.uuid5(uuid.NAMESPACE_URL,'independent-review-consistent-control'))
f=q[':question/answer-fields'][0]
for o in f[':answer-field/choices']:
 if o[':answer/value']=='5':o[':answer/value']='2'
f[':answer-field/correct']=[':answer/id',next(o[':answer/id'] for o in f[':answer-field/choices'] if o[':answer/value']=='2')]
r1['generation']={'audit_control':True,'not_generator_output':True,'construction':'Independent fixture: q-34568 original target (3,4,5) to (3,4,7); reuse existing solution renderer for same ordered method. Replaces distractor 5 by correct sum 2.','parameters':{'target':[3,4,7]},'seed':83}
save('consistency-pair.json',[r0,r1]);unreachable=not any(a.vectors(r)==[u,v,b2] for r in catalog)
save('consistency-pair-results.json',{'before':{'target':list(map(str,b)),'truth':a.truth(r0),'key':a.key(r0)},'after':{'target':list(map(str,b2)),'truth':a.truth(r1),'key':a.key(r1)},'generator_reaches_consistent_counterpart':not unreachable,'acceptance_test_passed':not unreachable,'explanation':'All allowed changes b=b0+t*(a1+2*a2) lie in one affine coset of the column span, so they cannot change consistency. Target (3,4,7) has coefficients (1,1); only the third target entry changed from the inconsistent original. Fixture is source-grounded and not claimed to be generated.'})
save('consistency-grader-input.json',[{'label':f'consistency-control-{i}','record':r,'checks':[{'submitted_answer_id':o[':answer/id'],'expected':'accepted' if o[':answer/value']==a.truth(r) else 'rejected','purpose':'one target component switches consistency; actual radio grader must follow response'} for o in a.choices(r)]} for i,r in enumerate([r0,r1])])
# Strict, executable tests intentionally retain failing counterexamples for repair adoption.
(E/'regression-checks.py').write_text('''import sys,json,pathlib\nsys.dont_write_bytecode=True\nimport audit as a\nimport unittest\nclass RequiredCases(unittest.TestCase):\n def test_all_source_profiles(self):\n  for q in a.source['material']['kp'][':knowledge-point/questions']:\n   with self.subTest(source=q[':question/math-academy-id']):\n    self.assertEqual(a.truth(a.g.generate('moderate',83,q[':question/math-academy-id'],{'translation':0})),q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'])\n def test_consistency_role_can_change(self):\n  target=[a.sp.Matrix([-1,3,5]),a.sp.Matrix([4,1,2]),a.sp.Matrix([3,4,7])]\n  self.assertTrue(any(a.vectors(r)==target for r in a.g.catalog()),'Same-matrix consistent counterpart omitted: (3,4,5) -> (3,4,7)')\n def test_actual_batch_has_counterexample_to_second_largest(self):\n  rs=a.load(a.E/'batch.json')\n  self.assertTrue(any(a.key(r)!=str(sorted(a.sp.Rational(o[':answer/value']) for o in a.choices(r) if o[':answer/type']==':answer.type/math')[-2]) for r in rs),'Every exact batch item is answered by second-largest numeric choice')\nif __name__=='__main__':unittest.main()\n''')
# Read-only package relocation; copy only runtime files to evidence.
rel=E/'relocated';rel.mkdir(exist_ok=True)
for file in ['17592186119807.py','math_format.py','17592186119807/source.json']:
 target=rel/file;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a.P/file,target)
cmd=[sys.executable,str(rel/'17592186119807.py'),'--seed','20261021','--count','5'];proc=subprocess.run(cmd,cwd=E,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
save('relocation-records.json',json.loads(proc.stdout) if proc.returncode==0 else [])
save('relocation-result.json',{'command':cmd,'exit_code':proc.returncode,'stderr':proc.stderr,'same_records':json.loads(proc.stdout)==g.batch('moderate',5,20261021) if proc.returncode==0 else False})
# Recognizable subgroup probes from delivered prompts/choices, independent of metadata truth.
probes=[]
def probe(rs,label,cue,strategy,predict,subgroup='all',scope='overall',disposition='defect'):
 if not rs:return
 correct=sum(predict(r)==a.truth(r) for r in rs)
 probes.append({'cue':cue,'subgroup':label+': '+subgroup,'scope':scope,'strategy':strategy,'correct':correct,'total':len(rs),'baseline':.2,'disposition':disposition,'conclusion':f'{correct}/{len(rs)} versus random five-choice selection baseline 0.2. Cue uses answer bank or names, not component equations.','sample_refs':['batch.json' if label=='batch' else 'delivery-catalog/accepted.json' if label=='delivered' else 'catalog.json']})
for label,rs in [('catalog',catalog),('delivered',accepted),('batch',batch)]:
 probe(rs,label,'numeric order','Select the second-largest numeric choice, ignoring No solution.',lambda r:str(sorted(sp.Rational(o[':answer/value']) for o in a.choices(r) if o[':answer/type']==':answer.type/math')[-2]),disposition='defect' if label=='batch' else 'not_predictive')
 cgroup=[r for r in rs if '{c}_{1}' in r['question'][':question/problem']]
 probe(cgroup,label,'c1,c2,d labels','Choose No solution.',lambda r:'No solution','c/d names','other_recognizable_subgroup')
 for sid in sorted({r['generation']['source_id'] for r in rs}):
  subgroup=[r for r in rs if r['generation']['source_id']==sid];first=subgroup[0]; pos=a.keypos(first)
  probe(subgroup,label,'fixed coefficient vectors identify source profile; option position','Choose position '+str(pos+1)+'.',lambda r:a.choices(r)[pos][':answer/value'],sid,'within_template')
# Explicit faithful homogeneous-moderate selection: positive moderate weight -> uniform among all eligible moderate IDs.
# No database-specific entity allocation/history is invented. Any history removes a subset; a universal cue stays correct.
selection={'implementation':'engine/rust/question_selection.rs select; seen_before_task; candidates sorted/deduplicated by entity id, choose band then uniform(8) within it','captured_basis':a.inventory['basis'],'captured_original_inventory':len(a.inventory['questions']),'staged_counts':{'raw_catalog':len(catalog),'accepted_catalog':len(accepted),'batch':len(batch)},'weighted_behavior':'All staged records moderate. With positive moderate weight, every fresh staged record is eligible with equal probability. Zero moderate weight excludes the whole rated cohort; no unweighted fallback to this cohort. Unconfigured policy returns lowest entity ID.','history_behavior':'seen_before_task and current-prefix exclusion remove previously reserved items. Perfect batch numeric-rank cue and per-profile position cue remain perfect on every nonempty subset.','limitations':['No concrete learner, policy weights, task history or eventual staged entity IDs supplied; no claim of exact future chosen question. Current bank contains only source originals; generated-batch analysis is conditional on those records entering an eligible pool.'],'coverage':{'raw':a.metrics(catalog),'post_dedup':a.metrics(accepted),'batch_post_dedup':a.metrics(batch)},'shortcut_probes':probes,'rejection_and_resampling':'generate selects a source profile and bounded translation directly; no validity rejection/resampling. batch enumerates 46 canonical unique tasks with seed=0 for each profile/translation, shuffles task order, selects prefix; catalog fixed option permutation per profile. This is distinct from fresh generate seeds.'}
save('delivery-selection-analysis.json',selection)
# Add controlled evidence fixture and renderer input, preserving original renderer snapshots in its own directory.
save('consistency-render-records.json',[r0,r1])
print(json.dumps({'consistency_control_unreachable':unreachable,'relocation_exit':proc.returncode,'catalog_post_delivery':a.metrics(accepted),'probes':len(probes)},indent=2))
