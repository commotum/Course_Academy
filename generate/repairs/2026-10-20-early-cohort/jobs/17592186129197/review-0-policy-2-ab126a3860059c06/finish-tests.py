import pathlib,json,hashlib,re,collections,copy
E=pathlib.Path(__file__).resolve().parent
exec((E/'audit.py').read_text().split('records=[]')[0])
source=json.load(open(E.parent/'source/source.json'));out=[]
for q in source['material']['kp'][':knowledge-point/questions']:
 o=oracle(q);c=correct(q);out.append({'source':q[':question/id'],'oracle':o,'stored_key':c[':answer/value'] if c else None,'key_correct':s.simplify(parse(c[':answer/value'])-o['area'])==0 if c else None})
q=source['material']['kp'][':knowledge-point/canonical-example'];out.append({'source':q[':question/id'],'oracle':oracle(q),'expected_canonical_area':'32/15'})
save('source-math.json',out)
short=json.load(open(E/'shortcut-results.json'));post={}
for name in ['delivery-batch','delivery-samples']:
 rs=json.load(open(E/name/'accepted.json'));post[name]=[probe(r) for r in rs]
save('post-delivery-shortcuts.json',post)
pairs=json.load(open(E/'counterfactual-records.json'));cf=[]
for k,r in enumerate(pairs):
 q=r['question'];cf.append({'case':['base','relevant-height-change','irrelevant-unit-shear-change'][k],'parameters':r['generation']['parameters'],'oracle':oracle(q),'answer':correct(q)[':answer/value'],'prompt':q[':question/problem'],'diagram_sha256':hashlib.sha256(pathlib.Path(r['generation']['plot']).read_bytes()).hexdigest(),'solution_final':q[':question/worked-solution'].split('**Step 4**')[1],'rendered_file':f'render/question-{k+1:03}.png'})
save('counterfactual-results.json',{'cases':cf,'height_response_changed':cf[0]['answer']!=cf[1]['answer'],'height_diagram_changed':cf[0]['diagram_sha256']!=cf[1]['diagram_sha256'],'shear_response_preserved':cf[0]['answer']==cf[2]['answer'],'shear_diagram_preserved':cf[0]['diagram_sha256']==cf[2]['diagram_sha256'],'grader_labels':['samples-36','samples-37','samples-38']})
# Direct, faithful reproduction of the selection function's band/hash draws.
inv=json.load(open(E.parent/'source/inventory.json'));pool=[];excluded=[]
for q in inv['questions']:
 eligible=(not q.get(':question/retired',False) and correct(q) is not None and all(f[':answer-field/type'][':db/ident']==':answer-field.type/radio' for f in q[':question/answer-fields']))
 (pool if eligible else excluded).append(q)
def select(candidates,weights,seed):
 bands={k:[] for k in ['easy','moderate','hard','unrated']}
 for q in sorted(candidates,key=lambda q:q[':db/id']):bands[q.get(':question/difficulty',{}).get(':db/ident','/unrated').split('/')[-1]].append(q)
 dg=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 uniform=lambda n:(int.from_bytes(dg[n:n+8],'big')>>11)/2**53
 total=sum(weights[i] for i,b in enumerate(['easy','moderate','hard']) if bands[b]);chosen=bands['unrated']
 if total:
  draw=uniform(0)*total
  for i,b in enumerate(['easy','moderate','hard']):
   if not bands[b] or weights[i]==0:continue
   chosen=bands[b]
   if draw<weights[i]:break
   draw-=weights[i]
 return chosen[int(uniform(8)*len(chosen))][':question/id'] if chosen else None
bad={x['question_id'] for x in json.load(open(E/'affected-inventory.json'))['affected_questions']}
draws=[select(pool,[1,0,0],f'independent-review-{seed}') for seed in range(32)]
selection={'captured_basis':inv['basis'],'rules':['learning.rs validate_practice_question excludes retired questions and malformed/missing radio keys; all inspected eligible fields are ordinary single radio questions.','question_selection.rs select: rated bands chosen by configured weights; uniform within band; seen questions are removed before selection.','Policy and learner history are not in snapshot: [1,0,0] explicitly tests the requested easy band, not an assertion about live policy.'],'eligible_counts':dict(collections.Counter(q.get(':question/difficulty',{}).get(':db/ident','unrated') for q in pool)),'excluded_ids':[q[':question/id'] for q in excluded],'eligible_easy_ids':[q[':question/id'] for q in pool if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/easy'],'draws':draws,'shortcut_draws':sum(d in bad for d in draws),'conclusion':'All five captured eligible easy questions are exactly reproduced vulnerable generated records. Any nonempty fresh subset of that band retains the shortcut. All three delivered batch additions also have it. Hard source questions are not asserted to share the shortcut.'}
save('selection.json',selection)
save('sampling-summary.json',{'fresh_templates':dict(collections.Counter(z['template'] for z in short['samples'])),'easy_heights':sorted(set(z['parameters']['h'] for z in short['samples'] if z['template']=='simple')),'batch_parameters':[z['parameters'] for z in short['batch']],'rejection_analysis':'Normal polynomial bank values are distinct fixed positive multiples of area plus its negative; no collision resampling changes the shortcut. Hyperbola samples also have the signed pair. generate() checks pairwise bank inequality, not shortcut distinguishability; CLI deduplicates mathematical fingerprints.','scope':'All tested equations are source-supported affine maps with quadratic, quartic-line, or hyperbolic transformed boundaries; easy remains a simple quadratic cap. Five unimplemented captured source profiles are listed separately in source-replay.json; no newly introduced learner skill observed.'})
print('Source math',len(out),'cases; delivered shortcut counts',[(k,len(v),sum(z['success'] for z in v)) for k,v in post.items()]);print('Selected easy',len(draws),selection['shortcut_draws'])
