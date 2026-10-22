"""Decision, delivery and learner-selection assessment for the bounded revision."""
import pathlib,json,collections,hashlib,copy,sys
E=pathlib.Path(__file__).resolve().parent;B=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy');P=B/'review-1-policy-2-45a9ed86924bfc07'
ns={'__file__':str(E/'audit.py')};exec(compile((E/'audit.py').read_text().split('source=json.load')[0],'audit.py','exec'),ns);parse=ns['parse'];save=ns['save']
load=lambda n:json.loads((E/n).read_text())
# Preserve independent exhaustive decision-assignment results only as unchanged evidence.
prov=load('reuse-provenance.json')
for name in ['decision-records.json','decision-results.json']:
 dest=E/('prior-'+name);dest.write_bytes((P/name).read_bytes());prov.append({'file':dest.name,'from':str(P/name),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'reuse':'All eligible source-bank truth assignments were tested in prior independent review; generate(), source-current.json and policy are unchanged except version metadata (runtime-change.diff). Fresh math, pair, batch and native checks cover current package.'})
save('reuse-provenance.json',prov)
refs={'normal_cli_raw':['fresh-cli-records.json','current-profile/profile-omission-records.json'],'moderate_raw':['delivery-input-moderate.json'],'hard_raw':['delivery-input-hard.json'],'moderate_delivered':['delivery-moderate/accepted.json'],'hard_delivered':['delivery-hard/accepted.json'],'batch_raw':['runner-batch.json'],'batch_delivered':['delivery-batch/accepted.json']}
stages={s:sum([load(p) for p in ps],[]) for s,ps in refs.items()};profiles={};probes=[]
def add(cue,group,scope,strategy,correct,total,baseline,conclusion,paths,disposition='not_predictive'):
 probes.append(dict(cue=cue,subgroup=group,scope=scope,strategy=strategy,correct=int(correct),total=int(total),baseline=baseline,disposition=disposition,conclusion=conclusion,sample_refs=paths))
def fnv(s):
 h=2166136261
 for c in s:h=((h^ord(c))*16777619)&0xffffffff
 return h
for stage,rows in stages.items():
 groups=collections.defaultdict(list)
 for r in rows:groups[r['generation']['profile']].append(r)
 profiles[stage]={k:{'count':len(rs),'truth_subsets':dict(collections.Counter(parse(r)['label'] for r in rs)),'ranks':sorted({parse(r)['rank'] for r in rs}),'nullities':sorted({parse(r)['nullity'] for r in rs}),'dimensions':sorted({parse(r)['n'] for r in rs})} for k,rs in groups.items()}
 for template,rs in groups.items():
  if len(rs)<2:continue
  ctr=collections.Counter(parse(r)['label'] for r in rs);label,hits=ctr.most_common(1)[0];radio=len(rs[0]['question'][':question/answer-fields'])==1
  add('Recognizable source template',stage+':'+template,'within_template','Always return '+label,hits,len(rs),.2 if radio else 1/7,'Complete response success, not just number of checked boxes. Comparison is uniform five-choice radio or seven nonempty subsets. Sample-specific best constant is not perfect; no universal absence-of-shortcuts claim.',refs[stage])
 for radio in [True,False]:
  rs=[r for r in rows if (len(r['question'][':question/answer-fields'])==1)==radio]
  if not rs:continue
  if radio:
   # FNV order is the real learning.js choiceOrder, task-item IDs held explicit.
   indices=[]
   for r in rs:
    f=r['question'][':question/answer-fields'][0]
    for item in range(1,11):
     choices=sorted(f[':answer-field/choices'],key=lambda a:fnv(f"{item}:{f[':answer-field/id']}:{a[':answer/id']}"));indices.append(next(i for i,a in enumerate(choices) if a[':answer/id']==f[':answer-field/correct'][1]))
   pos,hits=collections.Counter(indices).most_common(1)[0]
   add('Rendered radio answer position',stage+' radio, task-item contexts 1..10','other_recognizable_subgroup',f'Always choose displayed position {pos+1}',hits,len(indices),.2,'Reproduces ui/learning.js choiceOrder exactly using explicit IDs; baseline 1/5. Future numeric field/entity/task IDs are not known, so this tests dependence on position, not the future order. The runner contains one radio record; ten contexts prevent mistaking its stored position for a fixed delivered cue.',refs[stage])
  else:
   ctr=collections.Counter(tuple(parse(r)['truths']) for r in rs);mask,hits=ctr.most_common(1)[0]
   add('Checkbox layout positions',stage+' checkbox','other_recognizable_subgroup','Always submit '+str(mask),hits,len(rs),1/7,'Full question success compared with uniform nonempty subset guessing (1/7). In the exact batch TFT solves 2/4 checkbox questions; selecting only the final field solves 1/4. All four last fields happen to be true, a partial correlation that does not solve the three-judgment tasks.',refs[stage])
   for template,sub in groups.items():
    if len(sub[0]['question'][':question/answer-fields'])!=3 or len(sub)<2:continue
    mask,hits=collections.Counter(tuple(parse(r)['truths']) for r in sub).most_common(1)[0]
    add('Fixed checkbox action within template',stage+':'+template,'within_template','Always select positions '+str([i+1 for i,t in enumerate(mask) if t]),hits,len(sub),1/7,'Comparison 1/7 over nonempty three-checkbox responses. Different exact masks occur inside this recognizable template; selection count alone does not determine which statements qualify.',refs[stage])
# A perfect simplification is evaluated pedagogically instead of automatically failed.
rs=[r for r in stages['moderate_delivered']+stages['hard_delivered'] if '\\begin' in r['question'][':question/problem']]
add('Nonzero null-space generator','delivered vector profiles','other_recognizable_subgroup','Infer singularity from a visible nonzero null vector',sum(parse(r)['rank']<parse(r)['n'] for r in rs),len(rs),.5,'Baseline is binary invertibility guessing. Nontrivial null space implies noninvertibility by the source theorem: this is intended knowledge. Other numerical claims still require rank/nullity and n. Count profiles additionally reach full rank.',['delivery-moderate/accepted.json','delivery-hard/accepted.json'],'intended_skill')
save('shortcut-results.json',{'stage_coverage':profiles,'probes':probes,'limitations':['Descriptive best-constant strategies; no claim that every possible cue was tested.','The exact five-record batch has one radio and four checkbox questions; four distinct truth masks overall, with the checkbox TFT mask repeated twice. This is not sign-only repetition.','A one-record per-template subgroup in the exact batch cannot establish variation within that template; current delivered controls and unchanged prior full assignment tests supply the family check.']})
# Actual selection rules, read-only reproduction conditional on missing live weights/history.
inv=json.loads((B/'source/inventory.json').read_text());replays={r['generation']['template']:r for r in load('replay-records.json')}
base=[]
for q in inv['questions']:
 r=copy.deepcopy(replays[q[':question/math-academy-id']]);r['question'][':question/id']=q[':question/id'];base.append((q[':db/id'],r))
start=max(i for i,r in base)+1
def choose(cands,weights,seed,seen=set()):
 cands=sorted((i,r) for i,r in cands if i not in seen)
 if not cands:return None
 if weights is None:return cands[0]
 pools=[[p for p in cands if p[1]['question'][':question/difficulty'].endswith('/'+band)] for band in ['easy','moderate','hard']]
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();unit=lambda offset:(int.from_bytes(digest[offset:offset+8],'big')>>11)/(1<<53)
 total=sum(w for p,w in zip(pools,weights) if p)
 if total==0:return None
 draw=unit(0)*total;pool=None
 for p,w in zip(pools,weights):
  if not p or w==0:continue
  pool=p
  if draw<w:break
  draw-=w
 return pool[int(unit(8)*len(pool))]
selections=[]
for name,more in [('exact_batch',stages['batch_delivered']),('bounded_control',stages['moderate_delivered']+stages['hard_delivered'])]:
 cands=base+[(start+i,r) for i,r in enumerate(more)]
 for seen_name,seen in [('fresh_learner',set()),('original_sources_seen',{i for i,r in base})]:
  for weight_name,weights in [('moderate_only',[0,1,0]),('present_bands_equal',[1,1,1]),('unconfigured_legacy',None)]:
   selected=[choose(cands,weights,'revision-review-'+str(i),seen) for i in range(256)];selected=[p for p in selected if p]
   selections.append({'pool':name,'history':seen_name,'weights':weight_name,'draws':len(selected),'profile_counts':dict(collections.Counter(r['generation']['profile'] for i,r in selected)),'question_count':len({i for i,r in selected})})
 # Validate history exclusion and sole remaining positive-band record.
 last=next(p for p in reversed(cands) if p[1]['question'][':question/difficulty'].endswith('/moderate'));seen={i for i,r in cands if i!=last[0]};assert choose(cands,[0,1,0],'single-remaining',seen)==last
save('selection-results.json',{'basis':inv['basis'],'implementation':'engine/rust/question_selection.rs: seen_before_task(), select() inspected; difficulty-first SHA256 draw and sorted unseen candidate rules faithfully reproduced.','scenarios':selections,'limits':['Future new entity IDs are symbolic; policies and learner histories are not in the capture. Results are conditional tests, not live predictions.','Unknown difficulty fallback is inapplicable: all supplied sources and generated records have moderate/hard ratings.','Legacy policy chooses first unseen entity; configured zero weights exclude that band. No truth or template restriction exists in selection code.'],'conclusion':'All delivered control profiles remain eligible in positive-weight bands. The exact batch remains five specific new questions after original sources are seen; the larger control set does not replace its separate measurements.'})
# Cross-check controlled pairs across native outcomes and actual renderer reports.
native=load('native-report.json');nrecords={r['label']:r for r in native['records']};render=load('render-all/rendering.json');pairs=load('counterfactual-results.json');records=load('counterfactual-records.json')
assert render['passed'] and len(render['cases'])==10
for i,pair in enumerate(pairs):
 rs=records[2*i:2*i+2];pair['sample_refs']=['counterfactual-records.json','native-input.json','native-report.json','render-all/input.json','render-all/rendering.json'];pair['render_indices']=[5+2*i,6+2*i];pair['actual_grader']=[nrecords[r['question'][':question/id']] for r in rs];pair['render_passed']=all(render['cases'][j]['passed'] for j in pair['render_indices']);pair['status']='passed';assert pair['render_passed']
 # native checks exhaust each field's bank, including rejection of the other pair's key.
 if i==0:assert [parse(r)['label'] for r in rs]==pair['expected']
 else:assert parse(rs[0])['truths']==parse(rs[1])['truths']
save('counterfactual-results.json',pairs)
scope=load('scope-assessment.json');scope['provenance']='Reused independent analysis of unchanged constructors; updated changed profile sampling conclusion.'
for f in scope['fixed_features_review']:
 if 'sorted starting' in f['feature']:f['feature']='Seeded permutation of source profiles before truncation';f['assessment']='Prior restriction resolved: retained failing old-package test, six current normal runs and fresh CLI samples reach all supported profiles through delivery.'
save('scope-assessment.json',scope)
# All screenshots were visually inspected: first five in render and last five in render-all.
assert all((E/'render'/f'question-{i:03}.png').read_bytes()==(E/'render-all'/f'question-{i:03}.png').read_bytes() for i in range(1,6))
save('visual-inspection.json',{'automated_passed':render['passed'],'case_count':10,'screenshots_inspected':[f'render-all/question-{i:03}.png' for i in range(1,11)],'observations':['All five exact runner records display readable mathematics, radio/checkbox controls, keyed responses and worked solutions.','Same-claim pivot-count pair changes I/III -> II and changes rank/nullity and invertibility explanation consistently.','Coordinate pair changes visible vectors and spanning directions but preserves dimensional facts and checkbox truth subset.','The hard parametric vector profile displays its complete vector and five-choice bank legibly.','No clipped mathematics, missing glyphs, broken assets or MathJax errors observed.'], 'renderer_limit_note':'Initial render defaulted to six cases; reran with --limit 10 before concluding. First five screenshots match byte-for-byte.'})
# Mandatory pedagogical contract, source-grounded interpretation not variable-slot restatement.
analysis=load('source-analysis.json');variation={'learner_operation':analysis['learner_operation'],'fixed_features':analysis['fixed_features']+scope['fixed_features_review'][:3],'answer_roles':[{'role':'Rank/nullity/count value and whether a numerical claim agrees','eligible_variation':'Change supplied count or compared number while preserving square-matrix theorem and three judgments.','observed':'Counts include zero and full n; controlled count3->4 flips fixed-claim response I/III to II.'},{'role':'Qualifying statement labels, positions and subset size','eligible_variation':'Any source-bank-supported subset, seven nonempty checkbox assignments, varied polarity.','observed':'Every fresh delivered template has multiple truth subsets; prior unchanged exhaustive assignment tests cover all bank outcomes. Exact batch has FFT, FTF, TFT, TFT, FTT.'},{'role':'Profile selected into normal five-question delivery','eligible_variation':'Every supported profile of requested difficulty is eligible across seeds.','observed':'Seeded permutation resolves the prior fixed-prefix omission; all eight moderate profiles survive shared delivery.'}],'coverage':[{'case':stage,'sample_refs':refs[stage],'result':json.dumps(profiles[stage],sort_keys=True)} for stage in profiles]+[{'case':'All supported source-bank truth outcomes, unchanged construction','sample_refs':['prior-decision-records.json','prior-decision-results.json','runtime-change.json'],'result':'Reused independent exhaustive assignment evidence; finite bank restrictions preserve source response contract rather than fixing qualifying labels.'}],'counterfactuals':[{'kind':'relevant','change':pairs[0]['change'],'expected':'Only pivot count changes; answer I and III only -> II only.','observed':'Seed25 production outputs keep claims identical; explanations, rendered selections and all-choice native outcomes follow changed rank/nullity.','status':'passed','justification':'Rank-nullity and the invertible matrix theorem require reconsideration when the supplied count changes, as in source 50dd3dbf-46fe-5a60-971b-ec20882fc4a4.','sample_refs':pairs[0]['sample_refs']},{'kind':'irrelevant','change':pairs[1]['change'],'expected':'Dimension and Boolean response remain invariant; displayed null-space basis changes.','observed':'Both outputs have nullity2/rank1 and TFT response, actual grader and UI agree.','status':'passed','justification':'Source 5342a760-4f6b-57f7-989c-35eadd9600b3 derives dimension from two independent directions; nonzero coordinate scaling preserves this fact.','sample_refs':pairs[1]['sample_refs']}],'shortcut_probes':probes,'delivery':{'stages_examined':['Generator parameter rejection and nonempty-checkbox policy','Seeded profile selection and within-batch fingerprint deduplication','Shared publisher normalization, validation and captured inventory deduplication','Requested moderate/hard difficulty filtering','Learner history exclusion, rated-band weights and hash choice','Exact runner batch separate from broader controls'],'sample_refs':['fresh-cli-records.json','fresh-cli-results.json','current-profile/profile-omission-records.json','rejection-results.json','delivery-batch/accepted.json','delivery-batch/delivery.json','delivery-moderate/accepted.json','delivery-moderate/delivery.json','delivery-hard/accepted.json','delivery-hard/delivery.json','selection-results.json','shortcut-results.json'],'result':'Exact batch 5/5 accepted. Moderate controls69->67, hard36->35 after duplicates; all supported profiles and per-profile decision variation retained. Weighted learner selection has no truth-pattern filter; conditional selection evidence retains profiles in positively weighted bands.'},'limitations':['No finite audit proves absence of all shortcuts.','Inventory basis5447 contains only the15 original source questions; no stored generated records were available or marked as generated. affected-inventory.json is verified empty for this capture.','Live policy, learner history, future entity/task IDs and concurrent inventory changes are unavailable; selection analysis is conditional on explicit scenarios.','Canonical example has no captured answer bank; easy difficulty is unsupported and rejected.','Exact batch has four checkbox last fields true, but this partial correlation alone solves only one of those four tasks; best constant full-checkbox response solves2/4. Larger controls show other masks in every profile.']}
# Fixed-features entries must use contract names.
variation['fixed_features']=[{'feature':f['feature'],'justification':f.get('justification',f.get('assessment'))} for f in variation['fixed_features']]
save('pedagogical-variation.json',variation)
save('batch-assessment.json',{'input':'runner-batch.json','accepted':'delivery-batch/accepted.json','count':5,'profiles':profiles['batch_delivered'],'truth_masks':[parse(r)['truths'] for r in stages['batch_delivered']],'best_full_checkbox_mask_success':'2/4','last_only_checkbox_success':'1/4','radio_note':'One radio record does not establish profile-conditioned constancy; same-claim current pair and current delivered profile controls demonstrate alternatives.','verdict':'No full-response fixed-position or fixed-mask strategy answers this batch. Five independent decisions are more than sign/coordinate copies.'})
# Capture package integrity and exact version-binding evidence.
before=load('package-before.json');after={str(p.relative_to(B/'workspace')):hashlib.sha256(p.read_bytes()).hexdigest() for p in (B/'workspace').rglob('*') if p.is_file()};assert before==after
save('package-integrity.json',{'unchanged':True,'file_count':len(after),'before_file':'package-before.json','after_sha256':after})
(E/'session-state.md').write_text('All test milestones complete:15 exact source replays;131 independently parsed records plus107 normalized delivered records; native grader498 accepted/822 rejected/0 unresolved; actual UI10 cases visually inspected; shared delivery all15 profiles retained; old omission fails/current passes; per-template shortcut, same-claim relevant and irrelevant pairs, conditional learner selection and exact batch assessed. Package hash snapshot unchanged. Final report and evidence-contract validation pending.\n')
print(json.dumps({'native':{k:v for k,v in native.items() if k!='records'},'profiles_delivered':{s:len(profiles[s]) for s in ['moderate_delivered','hard_delivered']},'shortcut_probe_count':len(probes),'counterfactuals':[p['status'] for p in pairs],'package_unchanged':before==after}))
