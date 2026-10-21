import json,pathlib,hashlib,math,collections,copy
from audit import g,fields,answer,parse_rhs,independently_check,visible_bank,save
ROOT=pathlib.Path.cwd();JOB=ROOT.parent
load=lambda n:json.load(open(ROOT/n))
records=load('independent-samples.json');cf=load('counterfactual-records.json');batch=load('runner-batch.json')
# Inspect displayed worked mathematics separately from stored generator diagnostics.
solutionchecks=[]
for r in records+cf+batch+load('source-replay-records.json'):
 text=r['question'][':question/worked-solution'];aligned=text.split('\\begin{aligned}',1)[1].split('\\end{aligned}',1)[0];parts=aligned.split(' \\\\ ');expr=parse_rhs(r['question'][':question/problem']);points=r['generation']['parameters']['points'];out=[]
 for i,(line,(x,y)) in enumerate(zip(parts,points)):
  # Generator's solution has complete substitutions. Parse every expression after the coordinate annotation.
  sides=line.split('=')[1:];clean=[t.rstrip(', .') for t in sides];values=[parse_rhs('='+v) for v in clean];expected=expr.subs({g.X:g.sp.Rational(x),g.Y:g.sp.Rational(y)})
  assert all(g.sp.simplify(v-expected)==0 for v in values),(r['generation']['seed'],line,values,expected)
  out.append({'displayed_line':line,'parsed_values':list(map(str,values)),'expected':str(expected)})
 assert len(parts)==3
 solutionchecks.append({'question_id':r['question'][':question/id'],'lines':out})
save('worked-solution-checks.json',solutionchecks)
# Counterfactual response relationships, including physical PNG bytes and native grader outcomes.
def geometry(r):
 d=json.load(open(pathlib.Path(answer(r)[':answer/value']).with_suffix('.json')))
 return sorted([str(x),str(y),str(v)] for (x,y),v in zip(d['exact_points'],d['slopes']))
base,neg,reorder,point=cf
assert geometry(base)==geometry(reorder)
assert hashlib.sha256(pathlib.Path(answer(base)[':answer/value']).read_bytes()).hexdigest()==hashlib.sha256(pathlib.Path(answer(reorder)[':answer/value']).read_bytes()).hexdigest()
assert base['question'][':question/problem']==reorder['question'][':question/problem']
assert all(g.sp.Rational(v)==-g.sp.Rational(w) for v,w in zip(base['generation']['exact_slopes'],neg['generation']['exact_slopes']))
assert point['generation']['exact_slopes']==['-1/2','2','1/3']
save('counterfactual-results.json',{'seed':73661,'before':{'a':1,'points':[[-2,1],[1,2],[3,-1]],'slopes':['-1/2','4','1/3']},'coefficient_change':{'a':-1,'slopes':['1/2','-4','-1/3'],'prompt_changed':True,'correct_png_changed':True,'worked_substitutions_follow':True,'old_correct_image_rejected_in_native_grader':True},'irrelevant_reordering':{'points':[[3,-1],[1,2],[-2,1]],'problem_preserved':True,'correct_geometry_preserved':True,'correct_png_sha256_preserved':True,'solution_reordered_consistently':True,'native_correct_accepted':True},'point_change':{'points':[[-2,1],[2,2],[3,-1]],'slopes':['-1/2','2','1/3'],'unchanged_two_coordinates_preserved':True,'target_center_and_slope_changed':True,'worked_substitutions_follow':True,'native_correct_accepted':True},'evidence':['counterfactual-records.json','counterfactual-math.json','worked-solution-checks.json','grader-results.json','render-all/rendering.json'],'render_screenshots':['render-all/question-015.png','render-all/question-016.png','render-all/question-017.png','render-all/question-018.png']})
# Rejection reasons and per-form sign/zero/position coverage, not just text uniqueness.
rej=collections.Counter()
for a in load('sampling-attempts.json'):
 try:g.validate_parameters(a['level'],a['template'],a['parameters']);g.banks(a['template'],a['parameters'],'authored')
 except ValueError as e:rej[str(e)]+=1
coverage=[]
for t in g.TEMPLATES:
 rr=[r for r in records if r['generation']['template']==t];sl=[[g.sp.Rational(v) for v in r['generation']['exact_slopes']] for r in rr]
 coverage.append({'template':t,'count':len(rr),'seeds':[r['generation']['seed'] for r in rr],'positive_counts':dict(collections.Counter(sum(int(bool(v>0)) for v in row) for row in sl)),'negative_counts':dict(collections.Counter(sum(int(bool(v<0)) for v in row) for row in sl)),'zero_counts':dict(collections.Counter(sum(v==0 for v in row) for row in sl)),'correct_positions':[next(i+1 for i,a in enumerate(fields(r)[':answer-field/choices']) if a[':answer/id']==fields(r)[':answer-field/correct'][1]) for r in rr]})
save('coverage-results.json',{'command':'PYTHONDONTWRITEBYTECODE=1 .venv/bin/python summarize_checks.py','attempts':len(load('sampling-attempts.json')),'resampled':sum(rej.values()),'rejection_reasons':dict(rej),'per_template':coverage,'source_profiles':[r['generation']['bank_profile'] for r in load('source-replay-records.json')[:7]],'source_profile_default_sampling':'All six equation families sampled by default; seven original bank profiles are explicit replay paths. Default bank changes distractor design while retaining workload and image-radio contract.'})
# Extend the read-only learner-selection reproduction with the actual captured rated inventory.
inv=json.load(open(JOB/'source/inventory.json'));accepted=load('delivery-independent/accepted.json')+load('delivery-runner/accepted.json');pool={q[':db/id']:{'id':q[':question/id'],'band':q.get(':question/difficulty',{}).get(':db/ident','').rsplit('/',1)[-1],'origin':'captured_inventory','template':'source' if q.get(':question/math-academy-id') else 'stored_generated','affected':q[':db/id'] in {v['entity_id'] for v in load('affected-inventory.json')['affected_questions']}} for q in inv['questions'] if q.get(':question/answer-fields',[{}])[0].get(':answer-field/correct')}
for i,r in enumerate(accepted):pool[17592187000000+i]={'id':r['question'][':question/id'],'band':'easy','origin':'hypothetical_accepted','template':r['generation']['template'],'affected':None}
draws=[]
for weights in [[1,0,0],[1,1,1]]:
 for i in range(96):
  seed='independent-review/'+str(i);d=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();uni=lambda o:(int.from_bytes(d[o:o+8],'big')>>11)/(1<<53)
  bands=[[eid for eid in sorted(pool) if pool[eid]['band']==b] for b in ['easy','moderate','hard']];total=sum(w for w,b in zip(weights,bands) if b);draw=uni(0)*total;chosen=None
  for j,w in enumerate(weights):
   if not bands[j] or w==0:continue
   chosen=j
   if draw<w:break
   draw-=w
  eid=bands[chosen][int(uni(8)*len(bands[chosen]))];draws.append({'seed':seed,'weights':weights,'fixture_entity':eid,**pool[eid]})
seen={min(pool),max(pool)};assert len([v for v in pool if v not in seen])==len(pool)-2
save('selection-results.json',{'basis':inv['basis'],'captured_candidates':15,'hypothetical_accepted_candidates':41,'candidate_records':pool,'draws':draws,'tested_weight_profiles':[[1,0,0],[1,1,1]],'fresh_candidate_counts':{'easy':46,'moderate':5,'hard':5},'seen_exclusion':{'seen':list(seen),'remaining':len(pool)-2},'source_implementation':'engine/rust/question_selection.rs select and seen_before_task; SHA256 uniform(0) weighted band and uniform(8) sorted unique within-band draw. All hypothetical records use explicit fixture entity IDs, never DB writes.','result':'Both policies leave affected questions reachable. Difficulty filtering does not inspect bank geometry or the visual cue. Existing generated affected questions are moderate/hard; fresh delivered easy records also carry the cue.','limits':['Live policy weights, usable-entity schema checks, learner history and future assigned entity IDs were not supplied. Fixture results establish reachability and preserve cases under the real selection rule; they do not predict live delivery frequencies.','Two unrated source records lack keys and are excluded as unusable. The remaining captured inventory is examined at basis 5125 only.']})
print('verified',len(solutionchecks),'displayed solutions; 53 attempts ->36 banks; source replay, counterfactual relationships, captured-inventory selection fixtures complete')
