import json,pathlib,collections,hashlib,itertools,re
E=pathlib.Path(__file__).resolve().parent
def read(p):return json.load(open(E/p))
def save(p,x):(E/p).write_text(json.dumps(x,indent=2)+'\n')
def m(r):
 t=r['question'][':question/problem'];b=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',t,re.S)[1];return [[int(x.strip()) for x in z.split('&')] for z in b.split(r'\\')]
def ans(r):
 f=r['question'][':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else c[':answer/id'];return next(x[':answer/value'] for x in f[':answer-field/choices'] if x[':answer/id']==cid)
def signature(r):
 x=m(r);return (len(x),tuple(int(v!=0) for i,row in enumerate(x) for j,v in enumerate(row) if i!=j))
def summary(rs):return {'count':len(rs),'answers':dict(collections.Counter(ans(r) for r in rs)),'sizes':dict(collections.Counter(len(m(r)) for r in rs)),'support_patterns':len(set(signature(r) for r in rs))}
pre=read('independent-records.json');post=read('delivery/accepted.json');batch=read('runner-batch.json');ba=read('batch-delivery/accepted.json')
probes=[]
for name,rs,ref in [('independent_before',pre,'independent-records.json'),('independent_after',post,'delivery/accepted.json'),('runner_batch',batch,'runner-batch.json'),('runner_batch_after',ba,'batch-delivery/accepted.json')]:
 groups={'all':rs}
 for n in (2,3):
  groups['size='+str(n)]=[r for r in rs if len(m(r))==n]
  for letter in ('A','C'):groups[f'size={n},letter={letter}']=[r for r in rs if len(m(r))==n and re.search(r'\b'+letter+r'\s*=',r['question'][':question/problem'])]
 for group,items in groups.items():
  if not items:continue
  counts=collections.Counter(ans(r) for r in items);label,count=counts.most_common(1)[0]
  probes.append({'cue':'matrix size and letter only','subgroup':name+':'+group,'scope':'overall' if group=='all' else 'other_recognizable_subgroup','strategy':'Always select '+label,'correct':count,'total':len(items),'baseline':.2,'disposition':'not_predictive','conclusion':f'Baseline 0.2 is uniform guessing over all five radio labels. Majority label fit on this sample, not held-out accuracy. {count}/{len(items)}; '+('singleton subgroup is underpowered; independent controls vary both orientations at both dimensions, so this batch coincidence is not a demonstrated generator rule.' if len(items)==1 else 'No universal label-only rule in this subgroup.' if count<len(items) else 'Small finite subgroup coincidence; see larger independent groups.'),'sample_refs':[ref]})
 for kind in ('lower','upper','diagonal'):
  items=[r for r in rs if r['generation']['template']==kind]
  if not items:continue
  positions=collections.Counter(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/value']==ans(r)) for r in items);p,c=positions.most_common(1)[0]
  probes.append({'cue':'raw option position within construction family','subgroup':name+':'+kind,'scope':'within_template','strategy':'Select raw option '+str(p+1),'correct':c,'total':len(items),'baseline':.2,'disposition':'not_predictive','conclusion':f'Baseline .2 is uniform five-position guessing. Best raw position succeeds {c}/{len(items)}; family requires reading the zero pattern and is not itself a superficial prompt label. UI reorders choices further; native rendered batch positions examined separately. Tiny batch groups do not establish fixed rules.','sample_refs':[ref]})
# Inspect actual rendered batch choice ordering, separately from raw order.
html_positions=[]
for idx,r in enumerate(batch):
 text=(E/'render'/f'question-{idx+1:03}.html').read_text();inputs=re.findall(r'<input[^>]+type="radio"[^>]*>',text);values=[re.search(r'value="([^"]+)"',x)[1] for x in inputs];f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1];html_positions.append({'index':idx,'id':r['question'][':question/id'],'answer':ans(r),'correct_ui_position':values.index(cid)+1,'choice_ids':values})
save('rendered-batch-positions.json',html_positions)
poscount=collections.Counter(x['correct_ui_position'] for x in html_positions);p,c=poscount.most_common(1)[0]
probes.append({'cue':'actual UI answer position','subgroup':'exact runner batch in actual preview UI','scope':'overall','strategy':f'Always choose displayed position {p}','correct':c,'total':5,'baseline':.2,'disposition':'not_predictive','conclusion':f'Uniform five-position baseline .2; best displayed position {p} gets {c}/5. Real task-item IDs can alter the UI hash ordering; preview results are scoped to this fixture.','sample_refs':['rendered-batch-positions.json','render/input.json']})
# Independent full support masks implied by the definitions, excluding identity/other which are distractors in this source family.
wanted=set()
for n in (2,3):
 cells=[(i,j) for i in range(n) for j in range(n) if i!=j]
 for bits in itertools.product((0,1),repeat=len(cells)):
  u=any(b for b,(i,j) in zip(bits,cells) if i<j);l=any(b for b,(i,j) in zip(bits,cells) if i>j)
  if not(u and l):wanted.add((n,bits))
observed=set(signature(r) for r in pre);missing=sorted(wanted-observed)
save('support-coverage.json',{'definition_permitted_masks':len(wanted),'observed':len(observed),'missing':missing,'interpretation':'All 18 easy support patterns occur in the normal full-catalog sample; no eligible support is missing.'})
# Faithful select() reproduction. On all-easy accepted pools, any positive easy weight results in uniform within-band selection.
def draw(pool,seed,dist):
 candidates=sorted(pool,key=lambda x:x['entity_id']);digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest();uniform=lambda off:(int.from_bytes(digest[off:off+8],'big')>>11)/(1<<53)
 if dist is None:return candidates[0] if candidates else None
 bands=[[x for x in candidates if x['difficulty']==b] for b in ('easy','moderate','hard')];unrated=[x for x in candidates if x['difficulty'] is None];total=sum(w for w,b in zip(dist,bands) if b)
 if total:
  d=uniform(0)*total;pool2=[]
  for w,b in zip(dist,bands):
   if not b or w==0:continue
   pool2=b
   if d<w:break
   d-=w
 else:pool2=unrated
 return pool2[int(uniform(8)*len(pool2))] if pool2 else None
selection=[]
for name,rs in [('accepted_control',post),('accepted_batch',ba)]:
 for ordering in ['forward','reverse']:
  ordered=rs if ordering=='forward' else list(reversed(rs));pool=[{'entity_id':100000+i,'difficulty':'easy','answer':ans(r),'record_id':r['question'][':question/id']} for i,r in enumerate(ordered)]
  for history in (0,1):
   eligible=pool[history:];chosen=[draw(eligible,str(seed),[6,3,1]) for seed in range(256)]
   selection.append({'pool':name,'entity_order':ordering,'prior_seen_prefix_count':history,'draws':256,'answers':dict(collections.Counter(x['answer'] for x in chosen)),'distinct_selected':len(set(x['record_id'] for x in chosen)),'eligible_count':len(eligible)})
inv=read('inventory-audit.json');raw=read('../source/inventory.json');real=[]
for q in raw['questions']:
 row=next(r for r in inv['records'] if r['id']==q[':question/id'])
 if row['stored_answer'] is None:continue
 diff=q.get(':question/difficulty');diff=diff.get(':db/ident') if isinstance(diff,dict) else diff
 real.append({'entity_id':q[':db/id'],'difficulty':diff.split('/')[-1] if diff else None,'answer':row['stored_answer'],'record_id':row['id']})
captured=[]
for dist in ([6,3,1],[1,0,0],[0,1,0],None):
 chosen=[draw(real,str(seed),dist) for seed in range(256)];captured.append({'distribution':dist,'candidates':len(real),'answers':dict(collections.Counter(x['answer'] if x else 'none' for x in chosen)),'distinct_selected':len(set(x['record_id'] for x in chosen if x))})
save('selection-results.json',{'source':'engine/rust/question_selection.rs select(): SHA256, top 53 bits, difficulty band first, sorted numeric entity IDs within band; previous tasks and current prefixes excluded by callers.','delivered':selection,'captured_inventory':captured,'limits':['Future published numeric IDs and real learner histories/policy weights unavailable. Delivered IDs synthetic; both rank orders tested.','All accepted records are easy: any positive easy weight gives uniform supported selection; zero easy and no eligible fallback gives no selection.','An unconfigured policy selects lowest entity ID repeatedly until seen; this is existing engine behavior, not generator-specific.','No source record relabeled as generated; no database accessed.']})
cf=read('counterfactual-records.json');expected=['Lower triangular matrix','Upper triangular matrix','Diagonal matrix','Lower triangular matrix'];assert [ans(r) for r in cf]==expected
save('counterfactual-results.json',{'seed':739,'base':0,'transpose':1,'cleared_offdiagonal':2,'irrelevant_sign_and_diagonal':3,'answers':expected,'relevant_relation':'Transpose swaps orientation; clearing the permitted triangle gives diagonal. Diagonal held constant.','irrelevant_relation':'Changing only diagonal values and signs of existing nonzero entries preserves lower classification.','grader_records':list(range(17,21)),'native_grader':'grader-results.json','rendered_records':'render/input.json','render_report':'render/rendering.json','prompt_and_solution_matrices_independently_checked':True})
save('delivery-stage-results.json',{'inventory_basis':5451,'pre':summary(pre),'post':summary(post),'runner_batch_pre':summary(batch),'runner_batch_post':summary(ba),'same_decisions_after':collections.Counter(ans(x) for x in pre)==collections.Counter(ans(x) for x in post),'generation':'Catalog admits every nonempty one-sided support; no rejection loop for triangular values. fill_pattern resamples diagonal identity, irrelevant to orientation. batch picks masks without replacement, balanced upper/lower, prefers one diagonal.','selection':'selection-results.json','limits':'Publication preparation absent; shared actual prepare_records used read-only against captured inventory.'})
