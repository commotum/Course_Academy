import pathlib,json,collections,hashlib
exec(pathlib.Path('audit.py').read_text().split("manifest=json.load")[0])
rs=json.load(open('independent-records.json'));batch=json.load(open('runner-batch.json'))
catalog=[];stage=[]
for band in ['easy','moderate']:
 raw=[g.generate(band,seed=71933,parameters=[sid,k,t]) for sid in g.CASES if g.level(sid)==band for _,k in g.domain(sid) for t in range(5)]
 survivors=g.candidates(band,71933);dedup=list({g.fingerprint(q(r)):r for r in survivors}.values())
 stage.append({'band':band,'raw_count':len(raw),'inventory_rejected':len(raw)-len(survivors),'unique_survivors':len(dedup),'surviving_ranks':{sid:sorted({rank(r) for r in dedup if r['generation']['template']==sid}) for sid in g.CASES if g.level(sid)==band}})
 catalog+=dedup
save('normal-catalog-records.json',catalog)
def stats(records):
 out={}
 for sid in sorted({r['generation']['template'] for r in records}):
  z=[r for r in records if r['generation']['template']==sid]
  out[sid]={'count':len(z),'correct_ranks':dict(collections.Counter(str(rank(r)) for r in z)),'correct_positions':dict(collections.Counter(str(next(i for i,a in enumerate(f(r)[':answer-field/choices']) if a[':answer/id']==key(r)[':answer/id'])) for r in z))}
 return out
accepted=[]
for band in ['easy','moderate']:accepted+=json.load(open('delivery-'+band+'/accepted.json'))
bd=json.load(open('delivery-batch/accepted.json'))
assert g.batch('easy',5,4258185931)==batch
sub=[r for r in bd if r['generation']['template']=='q-73439']
assert len(sub)==3 and all(rank(r)==0 for r in sub)
for r in sub:
 m=mats(q(r)[':question/problem'])[0];k=r['generation']['parameters'][1]
 assert m==S.Matrix([[3,9,6*k],[2,7,3*k]])
save('minimal-failing-batch.json',sub)
control=g.generate('easy',seed=4258185931,parameters=['q-73439',5,4]);assert rank(control)==4
save('minimum-strategy-counterexample.json',[control])
selection=[]
for i in range(100):
 seed='independent-delivery-'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);idx=int(u*len(bd))
 selection.append({'seed':seed,'pool_index':idx,'id':q(bd[idx])[':question/id'],'template':bd[idx]['generation']['template'],'rank':rank(bd[idx])})
assert len({x['pool_index'] for x in selection})==5
save('delivery-selection.json',{'basis':5461,'stages':stage,'sample_before':stats(rs),'sample_after':stats(accepted),'batch_before':stats(batch),'batch_after':stats(bd),'selection_rule':'Faithful select uniform(8) draw for positive easy weight, empty seen set. DB entity sort is an unknown permutation and cannot alter rank constancy within the coefficient subgroup.','draws':selection,'limits':['No live learner histories or configured weights captured; empty-history positive-easy scenario analyzed read-only.','Publication preparation absent; actual prepare_records helper used against captured inventory basis 5461.']})
post=[]
for r in bd+accepted:
 verify(r)
 post.append({'label':'post-delivery '+str(r['generation']['parameters']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==key(r)[':answer/id'] else 'rejected','purpose':'Independently parsed post-normalization matrix and optional pair'} for a in f(r)[':answer-field/choices']]})
save('grader-final-input.json',json.load(open('grader-input.json'))+post)
probes=[]
def probe(subgroup,z,scope,disposition,refs):
 wins=sum(rank(r)==0 for r in z)
 probes.append({'cue':'minimum lower-right matrix entry','subgroup':subgroup,'scope':scope,'strategy':'Choose smallest lower-right value without using input RHS.','correct':wins,'total':len(z),'baseline':0.2,'disposition':disposition,'conclusion':f'{wins}/{len(z)} versus random five-choice baseline 1/5. '+('Batch-only incidental predictor; broader generator has counterexamples.' if disposition=='defect' else 'Not a universal answer rule across this tested group.'),'sample_refs':refs})
probe('exact runner batch',bd,'overall','not_predictive',['runner-batch.json','delivery-batch/accepted.json'])
probe('coefficient block [[3,9],[2,7]], exact runner batch',sub,'within_template','defect',['minimal-failing-batch.json','delivery-batch/accepted.json'])
for sid in g.CASES:
 z=[r for r in rs if r['generation']['template']==sid][:5]
 probe(sid+' controlled common-bank targets',z,'within_template','not_predictive',['independent-records.json','counterfactual-results.json'])
 wins=sum(f(r)[':answer-field/choices'][0][':answer/id']==key(r)[':answer/id'] for r in z)
 probes.append({'cue':'first displayed answer','subgroup':sid+' common-bank targets','scope':'within_template','strategy':'Always click first radio option.','correct':wins,'total':5,'baseline':0.2,'disposition':'not_predictive','conclusion':f'{wins}/5 equals random five-choice baseline 0.2. Same bank/order, each option correct once.','sample_refs':['independent-records.json','grader-results.json']})
variation={
'learner_operation':json.load(open('source-analysis.json'))['skill'],
'fixed_features':[
 {'feature':'Nonsingular 2x3 augmented matrix, nonzero first pivot, normalized forward REF, optional solve and five radio choices','justification':'Canonical 0a9e6824 and tutorial 2112d3af establish pivot normalization, elimination and back substitution; complete source banks have five choices.'},
 {'feature':'Ten coefficient profiles, bounded RHS scaling and target shifts','justification':'Conservative finite same-operation arithmetic family preserves source denominator workload; supports focused practice, not arbitrary-matrix transfer. Nothing in the source fixes candidate rank in a delivered subgroup.'}],
'answer_roles':[{'role':'Correct lower-right value, corresponding x,y and radio option','eligible_variation':'Each candidate may qualify when the lower input RHS changes; option order can independently permute.','observed':'All five ranks per profile before/after catalog rejection; actual batch q-73439 retains rank zero exclusively, 3/3.'}],
'coverage':[{'case':s['band']+' catalog rejection and uniqueness','sample_refs':['normal-catalog-records.json','delivery-selection.json'],'result':str(s)} for s in stage]+[{'case':'Exact runner batch before and after delivery','sample_refs':['runner-batch.json','delivery-batch/accepted.json','delivery-selection.json'],'result':'5/5 accepted; three scaled q-73439 instances all select minimum lower-right value.'}],
'counterfactuals':[
 {'kind':'relevant','change':'Hold profile, scale, bank/order, first input row and coefficients fixed; change lower input RHS across targets 0 through 4.','expected':'Each of five different choices becomes correct; prompt, solution and native acceptance follow.','observed':'Ten profiles each reach five different answers; exact readbacks and native grader agree. Actual-UI renders include easy endpoint pairs and a moderate pair.','status':'passed','justification':'Tutorial 2112d3af Step 2 changes the augmented column along with coefficient columns; lower RHS determines normalized y.','sample_refs':['independent-records.json','counterfactual-results.json','math-results.json','grader-results.json','render-records.json','render/rendering.json']},
 {'kind':'irrelevant','change':'Change seed to permute options while profile, scale and target stay fixed.','expected':'Same matrix, solution and mathematical key; native acceptance follows choice identity.','observed':'Ten permutations preserve prompt and key value; every option checked in native grader. Representative permutation rendered.','status':'passed','justification':'Choice order is incidental to Gaussian elimination and the one-choice radio contract.','sample_refs':['independent-records.json','counterfactual-results.json','grader-results.json','render-records.json','render/rendering.json']}],
'shortcut_probes':probes,
'delivery':{'stages_examined':['deterministic generation and parameter rejection','captured-system rejection in candidates','semantic uniqueness in batch','requested difficulty','actual publisher normalization and inventory/batch deduplication','fresh rated learner-selection rule, read-only positive-easy empty-history scenario'],'sample_refs':['packaging-results.json','normal-catalog-records.json','delivery-selection.json','delivery-batch/delivery.json','delivery-easy/delivery.json','delivery-moderate/delivery.json'],'result':'5/5 batch records survive, retaining conditional minimum-choice shortcut. Independent samples accept 28/36 easy and 37/45 moderate. Selection cannot supply absent target ranks within this subgroup.'},
'limitations':['Demonstrated batch-selection defect, not a universal decision_instance defect; controlled ranks refute a universal minimum rule.','No finite audit excludes every possible cue.','Live selection weights/history unavailable; inventory fixed at basis 5461.','Two incomplete captures not invented; ten complete banks tested.']}
save('pedagogical-variation.json',variation)
save('batch-shortcut-results.json',{'command':PY+' -B reproduce_batch_shortcut.py','seed':4258185931,'parameters':[r['generation']['parameters'] for r in sub],'successes':3,'attempts':3,'baseline':0.2,'failure':'Recognizable q-73439 subgroup contains three positive RHS-scale variants, all target rank 0.','scope':'Exact accepted runner batch; current generator supports other ranks.','ids':[q(r)[':question/id'] for r in sub]})
print(json.dumps({'stages':stage,'batch_shortcut':'minimum-y 3/3 in q-73439','post_grader_records':len(post)}))
