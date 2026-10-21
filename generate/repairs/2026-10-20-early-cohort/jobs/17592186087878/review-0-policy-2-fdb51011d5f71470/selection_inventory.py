from audit import *
inv=json.load(open('../source/inventory.json')); accepted=json.load(open('delivery-batch/accepted.json'));inventory_math=[]
sourceids={q[':question/id'] for q in json.load(open('source-extract.json'))['questions']}
for q in inv['questions']:
 if q[':question/id'] in sourceids:continue
 P,Q=equation(q);fields=[]
 for f in q[':question/answer-fields']:
  hits=[]
  for c in f[':answer-field/choices']:
   v=parse(c[':answer/value']);res=s.simplify(s.diff(v,x)-P*v if f[':answer-field/key']=='field-1' else s.diff(v,x)+P*v-Q)
   if res==0:hits.append(c[':answer/id'])
  stored=f[':answer-field/correct'][':answer/id'];fields.append({'field':f[':answer-field/key'],'hits':hits,'stored':stored,'passed':hits==[stored]})
 inventory_math.append({'id':q[':question/id'],'entity_id':q[':db/id'],'fields':fields,'passed':all(f['passed'] for f in fields)})
save('inventory-math.json',inventory_math)
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-audit.json',{'basis':inv['basis'],'question_count':len(inv['questions']),'original_source_questions':len(sourceids),'other_stored_questions':len(inventory_math),'demonstrated_current_generator_weaknesses':[],'affected_status':'None demonstrated. All five non-source stored records checked for unique mathematically valid choices and stored keys. Original source duplicate-bank defect is recorded separately and is not relabeled as generated. No current-generator defect was demonstrated to reproduce into affected inventory.','metadata_limit':'Captured stored records omit generation metadata; no invented generation provenance or IDs. This is not a claim of exhaustive historical shortcut absence.'})
def enum(v):return v.get(':db/ident') if isinstance(v,dict) else v
rows=[{'id':q[':db/id'],'band':enum(q.get(':question/difficulty')),'uuid':q[':question/id'],'origin':'inventory'} for q in inv['questions']]
nextid=max(r['id'] for r in rows)+1
rows += [{'id':nextid+i,'band':r['question'][':question/difficulty'],'uuid':r['question'][':question/id'],'origin':'accepted-batch','template':r['generation']['template']} for i,r in enumerate(accepted)]
def select(candidates,distribution,seed):
 candidates=sorted(candidates,key=lambda r:r['id'])
 if distribution is None:return candidates[0] if candidates else None
 bands=[[r for r in candidates if r['band']==':question.difficulty/'+b] for b in ['easy','moderate','hard']];unrated=[r for r in candidates if not r['band']]
 h=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 uniform=lambda offset:(int.from_bytes(h[offset:offset+8],'big')>>11)/(1<<53)
 total=sum(w for b,w in zip(bands,distribution) if b)
 if total>0:
  draw=uniform(0)*total;pool=[]
  for band,w in zip(bands,distribution):
   if not band or w==0:continue
   pool=band
   if draw<w:break
   draw-=w
 else:pool=unrated
 return pool[int(uniform(8)*len(pool))] if pool else None
cases=[]
for history in ['fresh','remove-current-batch','remove-rated-easy']:
 candidates=[r for r in rows if not (history=='remove-current-batch' and r['origin']=='accepted-batch') and not(history=='remove-rated-easy' and r['band']==':question.difficulty/easy')]
 for distribution in [None,[1,0,0],[0,1,0],[0,0,1],[1,1,1]]:
  draws=[select(candidates,distribution,'independent-review-'+str(i)) for i in range(512)]
  counts=collections.Counter(r['uuid'] if r else 'none' for r in draws)
  cases.append({'history':history,'distribution':distribution,'draws':512,'counts':dict(counts),'accepted_batch_draws':sum(1 for r in draws if r and r['origin']=='accepted-batch')})
save('selection-results.json',{'implementation':'Faithful Python reproduction of engine/rust/question_selection.rs select; SHA256 domain, 53-bit uniforms, BTreeSet order, band exclusion, fallback and uniform in-band selection preserved.','source_sha256':hashlib.sha256(pathlib.Path('/home/jake/Developer/Course_Academy/engine/rust/question_selection.rs').read_bytes()).hexdigest(),'input_records':rows,'cases':cases,'conclusions':['All five accepted runner records are reachable in the positively weighted easy band for fresh eligible candidates.','Zero-weight bands are excluded. No rated fallback is invented when a positively weighted band is empty. Unrated fallback is uniform; missing policy chooses minimum ID.','History exclusions remove only explicitly excluded items; within a supported band selection does not inspect answer values, templates, positions, roles or generation metadata.','Thus any positive easy-band weight preserves support of its remaining decision cases; weights change frequency, and history can exhaust cases.'],'limitations':['No live learner policy/history is in the captured inventory. Runs cover branches and support conditional on specified histories/weights, not a prediction of an actual future learner session.','Temporary monotone entity IDs for not-yet-published records are a read-only model. Actual allocated IDs can change individual seeded draws, but not the uniform in-band support or answer independence.','Concurrent publication can change inventory from basis 5275.']})
print('inventory math',len(inventory_math),'failures',[r for r in inventory_math if not r['passed']],'selection scenarios',len(cases))
