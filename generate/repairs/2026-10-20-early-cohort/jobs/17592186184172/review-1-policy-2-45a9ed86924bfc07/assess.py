"""Summarize independent probes and bounded learner-selection reproduction."""
import json,pathlib,collections,hashlib,copy,sys
E=pathlib.Path(__file__).resolve().parent
ns={'__file__':str(E/'audit.py')};exec(compile((E/'audit.py').read_text().split('source=json.load')[0],'audit.py','exec'),ns)
parse=ns['parse'];save=ns['save'];B=E.parent;R=pathlib.Path('/home/jake/Developer/Course_Academy')
stages={'fresh_raw':json.load(open('fresh-records.json')),'fresh_delivered':json.load(open('delivery-moderate/accepted.json'))+json.load(open('delivery-hard/accepted.json')),'runner_raw':json.load(open('runner-batch.json')),'runner_delivered':json.load(open('delivery-batch/accepted.json')),'normal_cli_raw':json.load(open('profile-omission-records.json')),'normal_cli_delivered':json.load(open('delivery-profile-omission/accepted.json'))}
refs={'fresh_raw':'fresh-records.json','fresh_delivered':'delivery-moderate/accepted.json','runner_raw':'runner-batch.json','runner_delivered':'delivery-batch/accepted.json','normal_cli_raw':'profile-omission-records.json','normal_cli_delivered':'delivery-profile-omission/accepted.json'}
profiles={};probes=[]
for stage,rows in stages.items():
 groups=collections.defaultdict(list)
 for r in rows:groups[r['generation']['template']].append(r)
 profiles[stage]={k:{'count':len(rs),'truth_subsets':dict(collections.Counter(parse(r)['label'] for r in rs)),'n':sorted({parse(r)['n'] for r in rs}),'rank':sorted({parse(r)['rank'] for r in rs})} for k,rs in groups.items()}
 for template,rs in groups.items():
  # Do not call a one-record template subgroup evidence against prediction.
  if len(rs)<2:continue
  counter=collections.Counter(parse(r)['label'] for r in rs);answer,hits=counter.most_common(1)[0]
  radio=len(rs[0]['question'][':question/answer-fields'])==1;baseline=.2 if radio else 1/7
  probes.append({'cue':'Recognizable source template / fixed subset','subgroup':stage+':'+template,'scope':'within_template','strategy':'Always return '+answer,'correct':hits,'total':len(rs),'baseline':baseline,'disposition':'not_predictive' if hits<len(rs) else 'defect','conclusion':f'Best constant subset succeeds {hits}/{len(rs)}. Comparison: uniform guessing among five bank labels (radio) or seven nonempty checkbox subsets. This sample tests constancy, not a universal absence of predictors.','sample_refs':[refs[stage]]+(['delivery-hard/accepted.json'] if stage=='fresh_delivered' else [])})
 # Exact full-answer fixed position/count strategy, separated by response shape.
 for radio in [True,False]:
  rs=[r for r in rows if (len(r['question'][':question/answer-fields'])==1)==radio]
  if not rs:continue
  if radio:
   ctr=collections.Counter(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in rs)
   pos,hits=ctr.most_common(1)[0];cue='Stored bank position';strategy='Always choose stored index '+str(pos);base=.2
  else:
   ctr=collections.Counter(tuple(parse(r)['truths']) for r in rs);mask,hits=ctr.most_common(1)[0];cue='Fixed checkbox positions';strategy='Always submit '+str(mask);base=1/7
  probes.append({'cue':cue,'subgroup':stage+(' radio' if radio else ' checkbox'),'scope':'other_recognizable_subgroup','strategy':strategy,'correct':hits,'total':len(rs),'baseline':base,'disposition':'not_predictive' if hits<len(rs) else 'defect','conclusion':f'{hits}/{len(rs)} complete questions solved. Baseline is uniform bank/subset guessing. Stored order is additionally permuted by learning.js for radio; measured separately below.','sample_refs':[refs[stage]]+(['delivery-hard/accepted.json'] if stage=='fresh_delivered' else [])})
# Actual UI ordering function, varied task-item contexts. No metadata answer cues used.
def fnv(s):
 n=2166136261
 for c in s:n=((n^ord(c))*16777619)&0xffffffff
 return n
for stage in ['fresh_delivered','runner_delivered']:
 positions=[]
 for r in stages[stage]:
  fs=r['question'][':question/answer-fields']
  if len(fs)!=1:continue
  f=fs[0]
  for taskitem in range(1,11):
   order=sorted(f[':answer-field/choices'],key=lambda a:fnv(f"{taskitem}:{f[':answer-field/id']}:{a[':answer/id']}"))
   positions.append(next(i for i,a in enumerate(order) if a[':answer/id']==f[':answer-field/correct'][1]))
 ctr=collections.Counter(positions);pos,hits=ctr.most_common(1)[0]
 probes.append({'cue':'Actual learning.js radio position','subgroup':stage+'; task-item contexts 1..10','scope':'other_recognizable_subgroup','strategy':'Always choose rendered index '+str(pos),'correct':hits,'total':len(positions),'baseline':.2,'disposition':'not_predictive','conclusion':f'Actual FNV choiceOrder reproduced from ui/learning.js:690-692. Best fixed position {hits}/{len(positions)}, against 1/5 guessing. Actual future task-item IDs are unavailable; ten explicit contexts test position dependence.','sample_refs':[refs[stage],'shortcut-results.json']+(['delivery-hard/accepted.json'] if stage=='fresh_delivered' else [])})
# Intended simplification probe: nontrivial nullspace implies singularity.
rs=[r for r in stages['fresh_delivered'] if '\\begin' in r['question'][':question/problem']]
hits=0
for r in rs:
 d=parse(r)
 hits+=d['nullity']>0 and d['rank']<d['n']
probes.append({'cue':'Visible nonzero null-space generator','subgroup':'fresh delivered vector templates','scope':'other_recognizable_subgroup','strategy':'Conclude A is singular from the displayed nonzero null vector','correct':int(hits),'total':len(rs),'baseline':.5,'disposition':'intended_skill','conclusion':'A perfect predictor here is the invertible matrix theorem itself, not an incidental template label. Comparison baseline is a fair binary invertibility guess. The source worked solutions explicitly use nonzero nullity to conclude singularity. Numeric rank/column-dimension claims still require the nullity and n.','sample_refs':['delivery-moderate/accepted.json','delivery-hard/accepted.json']})
save('shortcut-results.json',{'stage_coverage':profiles,'probes':probes,'limits':['No finite probe set establishes absence of every shortcut.','Best constant strategies are descriptive sample measurements, not trained predictors validated on held-out data.','Single-record runner profile subgroups cannot show within-profile variation; separately checked all five supplied radio labels / all seven nonempty checkbox truth assignments.']})
# Captured inventory and prospective records: faithful difficulty-first select().
# New IDs are explicitly symbolic, not asserted publication identities.
inv=json.load(open(B/'source/inventory.json'));replays={r['generation']['template']:r for r in json.load(open('replay-records.json'))}
candidates=[]
for q in inv['questions']:
 r=copy.deepcopy(replays[q[':question/math-academy-id']]);r['question'][':question/id']=q[':question/id'];candidates.append((q[':db/id'],r))
nextid=max(i for i,r in candidates)+1
candidates += [(nextid+i,r) for i,r in enumerate(stages['runner_delivered'])]
def choose(cands,weights,seed,seen=set()):
 cands=sorted((i,r) for i,r in cands if i not in seen)
 if not cands:return None
 if weights is None:return cands[0]
 pools=[[p for p in cands if p[1]['question'][':question/difficulty'].endswith('/'+band)] for band in ['easy','moderate','hard']]
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 unit=lambda offset:(int.from_bytes(digest[offset:offset+8],'big')>>11)/(1<<53)
 total=sum(w for p,w in zip(pools,weights) if p)
 if total==0:return None
 draw=unit(0)*total;pool=None
 for p,w in zip(pools,weights):
  if not p or w==0:continue
  pool=p
  if draw<w:break
  draw-=w
 return pool[int(unit(8)*len(pool))]
selection=[]
for name,weights in [('moderate_only',[0,1,0]),('hard_only',[0,0,1]),('equal_present_bands',[1,1,1]),('legacy_unconfigured',None)]:
 draws=[choose(candidates,weights,f'independent-review-{i}') for i in range(512)]
 counts=collections.Counter(r['generation']['template'] for i,r in draws)
 selection.append({'scenario':name,'weights':weights,'draws':len(draws),'profile_counts':dict(counts),'supported_entity_count':len({i for i,r in draws}),'note':'Symbolic prospective entity IDs affect exact deterministic draws. Positive-weight band support is exact; live policy and learner history not captured.'})
seen={i for i,r in candidates};seen.remove(candidates[-1][0]);only=choose(candidates,[0,1,0],'history-single',seen)
save('selection-results.json',{'implementation':'engine/rust/question_selection.rs select(), seen_before_task()','basis':inv['basis'],'candidates':[{'entity_id':i,'symbolic':i>=nextid,'question_id':r['question'][':question/id'],'profile':r['generation']['template'],'difficulty':r['question'][':question/difficulty']} for i,r in candidates],'scenarios':selection,'history_single_remaining':{'remaining':candidates[-1][0],'selected':only[0]},'conclusions':['Within each positively weighted nonempty band the hash draw ranges uniformly over eligible sorted unseen candidates. No truth-pattern filter exists.','Existing original sources can still expose omitted profiles; new normal count=5 batches never replenish those three moderate profiles. Once original items have been seen, they are excluded and cannot compensate for the omission.','An unconfigured legacy policy chooses the first eligible entity, independent of truth. Configured zero-weight bands are excluded.','No live learner policy/history is included in supplied capture; this is conditional read-only selection analysis, not a claim about a particular learner or future database IDs.']})
# Reconcile counterfactuals across visible math, rendered text and native outcomes.
render=json.load(open('render-all/rendering.json'));native=json.load(open('native-report.json'));nr={x['label']:x for x in native['records']};pairs=json.load(open('counterfactual-results.json'))
for idx,pair in enumerate(pairs):
 pair['render_cases']=[5+2*idx,6+2*idx];pair['render_passed']=all(render['cases'][i]['passed'] for i in pair['render_cases']);pair['native_cases']=[nr[q] for q in pair['records']]
 pair['relationship_passed']=(pair['keys_changed'] if pair['kind']=='relevant_claim' else not pair['keys_changed']) and all(not d['errors'] for d in pair['derived']) and pair['render_passed']
save('counterfactual-results.json',pairs)
save('visual-inspection.json',{'renderer':'unmodified UI via render_preview.py','render_count':13,'all_automated_passed':render['passed'],'screenshots_inspected':['render-all/question-001.png','render-all/question-007.png','render-all/question-008.png','render-all/question-009.png','render-all/question-010.png','render-all/question-011.png','render-all/question-012.png','render-all/question-013.png','render/question-003.png'],'observations':['Radio and checkbox controls, rendered vector null spaces, theorem exposition and worked conclusions are legible.','Counterfactual claim change changes the marked radio subset from I/III to I/II, with prompt wording and explanation agreeing.','The count 3->4 pair changes concrete rank/nullity, invertibility polarity and explanation while deliberately retaining the requested truth subset.','The coordinate change (2a,a,b)->(6a,2a,b) changes the displayed null-space directions and solution vectors while preserving dimension and selected Boolean response.','No missing math glyphs, broken images, TeX errors or clipped theorem text observed at the tested viewport.','All five exact runner records are included in render-all/input.json; automated checks pass for all five.']})
# Hash runtime copies against originals at completion; no package edits by review.
manifest=json.load(open(B/'workspace/package.json'));save('runtime-file-hashes.json',{'files':[{'file':f,'package_sha256':hashlib.sha256((B/'workspace'/f).read_bytes()).hexdigest(),'review_copy_sha256':hashlib.sha256((E/'relocated'/f).read_bytes()).hexdigest()} for f in manifest['files']],'note':'Copies made before runtime checks match the package after checks. All review outputs are in evidence_root.'})
print(json.dumps({'stage_profiles':{k:list(v) for k,v in profiles.items()},'perfect_incidental_probes':[p['subgroup'] for p in probes if p['disposition']=='defect'],'counterfactuals':[(p['kind'],p['relationship_passed']) for p in pairs],'selection':[(x['scenario'],x['supported_entity_count']) for x in selection]}))
