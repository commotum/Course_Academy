#!/usr/bin/env python3
"""Measure bank-only cues and stage survival, preserving all complete inputs."""
import sys,json,pathlib,re,hashlib,collections
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;J=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(E));from retained_predictor import predict
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,o):(E/n).write_text(json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def f(r):return r['question'][':question/answer-fields'][0]
def features(r):
 prompt=r['question'][':question/problem'];m=re.search(r'=\\frac\{(-?\d*)(x\^3|x)\+(y\^3|2y|y)\}',prompt);assert m
 t='cube_root' if m[2]=='x^3' else 'affine' if m[3]=='2y' else 'linear_log'
 def num(z):return -1 if z=='-' else 1 if z=='' else int(z)
 a=num(m[1]);cs=[]
 for c in f(r)[':answer-field/choices']:
  z=c[':answer/value']
  if t=='cube_root':v=int(re.search(r'\{(-?\d+)\\ln',z)[1])
  elif t=='affine':
   mm=re.search(r'\^2([+-])(\d*)x',z);v=(1 if mm[1]=='+' else -1)*int(mm[2] or 1)
  else:v=num(re.search(r'y=(-?\d*)x',z)[1])
  cs.append(v)
 return t,a,cs
def fnv(text):
 v=2166136261
 for ch in text:v=((v^ord(ch))*16777619)&0xffffffff
 return v
def choices_by_ui(r):
 # A concrete preview task identity; actual task identity can reshuffle again.
 q=r['question'];fi=f(r);seed=q[':question/id']+':'+fi[':answer-field/id']
 return sorted(fi[':answer-field/choices'],key=lambda c:fnv(seed+':'+c[':answer/id']))
def strategies(r):
 t,a,cs=features(r);bank=f(r)[':answer-field/choices'];ids=[c[':answer/id'] for c in bank]
 out={'retained unique-shape/coefficient cue':predict(f(r))[1], 'shortest string':min(bank,key=lambda c:len(c[':answer/value']))[':answer/id'],'longest string':max(bank,key=lambda c:len(c[':answer/value']))[':answer/id']}
 for k in range(5):
  out[f'author position {k+1}']=ids[k]
  out[f'UI position {k+1} (concrete task seed)']=choices_by_ui(r)[k][':answer/id']
  out[f'signed coefficient rank {k+1}']=ids[sorted(range(5),key=lambda i:cs[i])[k]]
  out[f'absolute coefficient rank {k+1}']=ids[sorted(range(5),key=lambda i:abs(cs[i]))[k]]
 # Deliberately reads the equation, reflecting the legitimate reduced mathematical calculation.
 target=3*a if t=='cube_root' else -a if t=='affine' else a
 out['solve surviving coefficient from ODE']=ids[cs.index(target)]
 return out
stagefiles={'raw':'delivery-input.json','delivered':'delivery-independent/accepted.json','batch_raw':'runner-batch.json','batch_delivered':'delivery-batch/accepted.json','controlled':'controlled-records.json'}
stages={k:load(E/v) for k,v in stagefiles.items()};rows=[];measure={};outcomes=[]
for stage,records in stages.items():
 for i,r in enumerate(records):
  t,a,cs=features(r);key=f(r)[':answer-field/correct'][1];pred=strategies(r)
  outcomes.append({'stage':stage,'index':i,'question_id':r['question'][':question/id'],'family':t,'a':a,'candidate_coefficients':cs,'correct_candidate_index':next(i for i,c in enumerate(f(r)[':answer-field/choices']) if c[':answer/id']==key),'predictions':{name:{'id':p,'correct':p==key} for name,p in pred.items()}})
 measure[stage]={'records':len(records),'family_sign_counts':dict(collections.Counter(features(r)[0]+(' positive' if features(r)[1]>0 else ' negative') for r in records)),'bank_indices_per_template':{t:sorted({r['generation']['bank_index'] for r in records if features(r)[0]==t}) for t in ('cube_root','affine','linear_log')}}
 subsets=[('all',records)]+[(t,[r for r in records if features(r)[0]==t]) for t in ('cube_root','affine','linear_log')]
 subsets += [(t+' '+sg,[r for r in records if features(r)[0]==t and (features(r)[1]>0)==positive]) for t in ('cube_root','affine','linear_log') for sg,positive in [('positive',True),('negative',False)]]
 for subgroup,rs in subsets:
  if not rs:continue
  for name in strategies(rs[0]):
   predictions=[strategies(r)[name] for r in rs]
   rows.append({'stage':stage,'subgroup':subgroup,'strategy':name,'correct':sum(p==f(r)[':answer-field/correct'][1] for p,r in zip(predictions,rs)),'total':len(rs),'attempts':sum(p is not None for p in predictions),'baseline':0.2})
save('shortcut-results.json',{'baseline':'Uniform random one-of-five response has success 0.2. Cue functions never read key; only intended mathematical coefficient calculation reads the ODE. Full outcome records permit reproducing every count. UI position uses an explicitly stated task seed and actual learning.js FNV ordering; actual task IDs may reshuffle positions.','stage_files':stagefiles,'stage_counts':measure,'probes':rows,'outcomes':outcomes})
# Every fixed bank supports all five mathematical answer roles, including negative-only, sign-crossing and wraparound windows.
control=stages['controlled'];groups=[]
for t in ('cube_root','affine','linear_log'):
 for bi in (0,7,17):
  rs=[r for r in control if features(r)[0]==t and r['generation']['bank_index']==bi]
  vals=[tuple(c[':answer/value'] for c in f(r)[':answer-field/choices']) for r in rs]
  keys=[next(c[':answer/value'] for c in f(r)[':answer-field/choices'] if c[':answer/id']==f(r)[':answer-field/correct'][1]) for r in rs]
  assert len(set(vals))==1 and len(set(keys))==5
  groups.append({'family':t,'bank_index':bi,'same_ordered_visible_bank':True,'all_five_correct_roles':True,'target_a':[features(r)[1] for r in rs],'keyed_values':keys})
# Conditional easy-band selection reproduces the actual deterministic second SHA-256 draw.
inv=load(J/'source/inventory.json');old=load(E/'affected-inventory.json');affected={z['question_id'] for z in old['affected_questions']}
def ident(v):
 if isinstance(v,dict):return v.get(':db/ident','')
 return v
existing=[q for q in inv['questions'] if ident(q.get(':question/difficulty'))==':question.difficulty/easy']
eidmax=max(q[':db/id'] for q in inv['questions']); proposed=[]
for i,r in enumerate(stages['batch_delivered']):proposed.append({':db/id':eidmax+i+1,':question/id':r['question'][':question/id'],'template':features(r)[0],'a':features(r)[1]})
candidates=existing+proposed;byid={q[':db/id']:q for q in candidates}
def select(ids,seed):
 ids=sorted(set(ids));d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();u=(int.from_bytes(d[8:16],'big')>>11)/(1<<53);return ids[int(u*len(ids))]
draws=[]
for i in range(48):
 seed='targeted-review-720241-'+str(i);eid=select(byid,seed);q=byid[eid]
 draws.append({'seed':seed,'entity_id':eid,'question_id':q[':question/id'],'proposed_surrogate':eid>eidmax,'legacy_affected':q[':question/id'] in affected})
remaining=list(byid);history=[]
while remaining:
 eid=select(remaining,'targeted-review-history-'+str(len(history)));remaining.remove(eid);history.append(byid[eid][':question/id'])
assert set(history)=={q[':question/id'] for q in candidates}
save('selection.json',{'inventory_basis':inv['basis'],'implementation_file':str(R/'engine/rust/question_selection.rs'),'implementation_sha256':hashlib.sha256((R/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'review':'Re-read weights, seen_before_task and select. Conditional on eligible easy band with positive weight, sorted/deduplicated candidates are uniform via second 53-bit SHA256 draw; seen history and current prefix exclude already used entries. No family/shape filter. Unconfigured policy chooses lowest remaining entity.','existing_easy_count':len(existing),'proposed_easy_count':len(proposed),'proposed_surrogate_ids':proposed,'draws':draws,'sequential_history':history,'limits':'Read-only branch reproduction, not live user policy or history. Proposed IDs are clearly synthetic support witnesses; actual reserved IDs alter draws but not positive support. Captured original and five legacy generated questions remain eligible and retain old shortcuts. This accepts repaired generator output only, not remediation of stored legacy content.','stage_coverage':'All five current batch records remain eligible. Old inventory cannot make a current bank-only strategy determine which target in an independently chosen five-member bank is correct.'})
probes=[]
for z in rows:
 if z['stage'] not in ('raw','delivered','batch_delivered','controlled'):continue
 if ' positive' in z['subgroup'] or ' negative' in z['subgroup']:continue
 intended=z['strategy']=='solve surviving coefficient from ODE'
 perfect=z['correct']==z['total']
 conclusion='Comparison baseline 0.2 is random choice among five.'
 if intended:conclusion+=' Computing the surviving coefficient and its integration multiplier is the intended mathematical operation; correct prediction expresses the skill.'
 elif z['attempts']==0:conclusion+=' Prior cue has no unique selection in same-shape banks.'
 elif z['stage']=='batch_delivered' and perfect:conclusion+=' Perfect on this tiny subgroup alone; inspect complete controlled role sets and broader post-delivery subgroup before inferring a structural rule.'
 else:conclusion+=' Does not consistently identify the key; complete same-bank role sets change correctness while holding this mathematical cue fixed.'
 probes.append({'cue':z['strategy'],'subgroup':z['stage']+' / '+z['subgroup'],'scope':'overall' if z['subgroup']=='all' else 'within_template','strategy':z['strategy'],'correct':z['correct'],'total':z['total'],'baseline':0.2,'disposition':'intended_skill' if intended else 'not_predictive','conclusion':conclusion,'sample_refs':[stagefiles[z['stage']],'shortcut-results.json']})
cf=load(E/'counterfactual-results.json')['pairs']
pv={'learner_operation':'Use y=vx to obtain xv\'=F(v)-v, separate/integrate and back-substitute; distinguish the surviving signed coefficient in five mathematical solution candidates. A valid shortcut through differentiation or linearity of the parameter still expresses this operation.','fixed_features':[{'feature':'Homogeneous first-order ODE; provided substitution y=v(x)x; five mathematical radio choices','justification':'All three easy source questions explicitly provide that substitution and radio response. Tutorial fe0a9e9e-ab23-5364-99bb-cddbfd67a4a4 derives xv\'=F(v)-v.'},{'feature':'Cubic inverse-square cancellation, affine coefficient two, and affine coefficient one templates','justification':'Represent the three labelled easy integrations. Fixing one template per instance preserves workload; all three appear in sampling. The varied x-term coefficient is eligible answer-bearing evidence.'},{'feature':'Nonzero small integer a from -9 through 9','justification':'Nonzero prevents collapse to y\'=y/x and removal of integration work. Nine is a conservative arithmetic bound, not an intrinsic learning constraint. Signed coefficients preserve the source method.'},{'feature':'Same mathematical solution form for all five extension choices','justification':'Correct form is information available in the source differential equation; requiring the multiplier/sign to be determined removes the old unique-shape and fixed-magnitude cues without introducing a new method.'}], 'answer_roles':[{'role':'Coefficient of surviving separated term','eligible_variation':'Small nonzero signs and magnitudes, derived into logarithm multiplier or affine particular solution','observed':'Fresh samples exercise all 18 bank indices per family; controlled negative, sign-crossing and wraparound banks exercise all five target coefficients.'},{'role':'Correct candidate and response position','eligible_variation':'Each of five candidates can solve an eligible ODE with the bank held fixed; order and actual UI layout are incidental','observed':'Nine same-bank groups cover all five correct mathematical roles. Actual UI shuffles UUIDs; raw-position, concrete UI-position, string-length and coefficient-rank probes saved.'}], 'coverage':[{'case':'Changed bank construction and fresh random sampler','sample_refs':['independent-samples.json','controlled-records.json','shortcut-results.json'],'result':'54 fresh bank-window constructions, 24 fresh random instances, and 45 controlled role assignments; all three families and signed boundary cases.'},{'case':'Exact runner batch and survivors','sample_refs':['runner-batch.json','delivery-batch/accepted.json','shortcut-results.json'],'result':'5/5 survive; affine 1, cube-root 2, linear-log 2. No old prompt-blind shape predictor applies. Across the full batch no tested fixed rank, length or position strategy solves all five.'},{'case':'Retained counterexample and supplied strict executable checks','sample_refs':['retained-counterexample.json','repair-preflight-verification.json'],'result':'Old cube-root a=2 seed=826033 exhibits original unique-root defect. Identical parameters now give five root candidates. Supplied assertions fail on old construction and pass current construction.'}], 'counterfactuals':[{'kind':kind,'change':'; '.join(p['name'] for p in cf if p['kind']==kind),'expected':'Changing the ODE coefficient with bank and presentation seed fixed changes correct solution and explanation; the old mathematical response must be rejected.' if kind=='relevant' else 'Reversing candidate order leaves prompt, solution, accepted mathematical response and key relationship unchanged.','observed':'All nine relevant pairs change prompt, solution and mathematical answer while retaining exactly the same ordered candidate strings; native grader rejects old response.' if kind=='relevant' else 'All three irrelevant pairs preserve prompt, solution and accepted mathematical response. Native grader accepts the preserved response.','status':'passed','justification':'Tutorial fe0a9e9e-ab23-5364-99bb-cddbfd67a4a4 makes F(v)-v determine the integral; order of radio candidates does not alter an ODE solution. Rendered before/after pairs for all three templates inspected.','sample_refs':['counterfactuals.json','counterfactual-results.json','grader-input.json','grader-results.json','render-records.json','render-remaining-records.json']} for kind in ('relevant','irrelevant')], 'shortcut_probes':probes,'delivery':{'stages_examined':['valid parameter construction and explicit invalid-input rejection; no valid easy rejection loop','actual shared publication normalization and validation','captured inventory and within-batch deduplication','requested easy difficulty filtering','read-only learner selection and history exclusion rules'], 'sample_refs':['packaging.json','delivery-input.json','delivery-independent/delivery.json','delivery-independent/accepted.json','delivery-batch/delivery.json','delivery-batch/accepted.json','shortcut-results.json','selection.json'],'result':'123 independent records become 106 after duplicate suppression; current batch 5 becomes 5. All families and sign cases remain in independent survivors. Exact current batch tested separately. Positive easy weight leaves each fresh surviving current record eligible; no answer-role filter. Five legacy affected stored generated records separately reproduced.'}, 'limitations':['No finite sample proves absence of every shortcut; conditional probes and all-five-role same-bank tests address the demonstrated construction risk.','Requested easy band only. Nine supported source replays retained; unimplemented moderate arctangent and unlabelled canonical image family explicitly recorded outside this requested band.','Live weights/history/concurrent inventory changes are unavailable; selection is a faithful read-only branch reproduction at captured basis 5449.','Five captured legacy generated questions still exhibit old shortcuts; saved affected-inventory.json and exact generated-records.json document these independently of repaired output. No database content was changed.']}
save('pedagogical-variation.json',pv)
save('decision-summary.json',{'controlled_groups':groups,'stage_counts':measure,'full_batch_perfect_prompt_blind_probes':[z for z in rows if z['stage']=='batch_delivered' and z['subgroup']=='all' and z['correct']==z['total'] and z['strategy']!='solve surviving coefficient from ODE'],'structural_justification':'Choose a bank independently, then choose one of its five target coefficients uniformly. The same fixed mathematical bank therefore supports all five keys for each family. Shuffling is not the source of the answer-role variation.','legacy_pool_disposition':'Retained as affected inventory; repaired package review does not certify legacy records.'})
assert not load(E/'decision-summary.json')['full_batch_perfect_prompt_blind_probes']
print(json.dumps({'stage_counts':{k:v['records'] for k,v in measure.items()},'controlled_groups':len(groups),'all_batch_blind_predictors':0,'pedagogical_probes':len(probes)}))
