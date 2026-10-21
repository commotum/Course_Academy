"""Retain reproduced historical defects; examine read-only selection boundaries."""
import sys
sys.dont_write_bytecode=True
import collections, hashlib, importlib.util, json, pathlib, re
E=pathlib.Path(__file__).resolve().parent;J=E.parent;P=J/'workspace';R=pathlib.Path('/home/jake/Developer/Course_Academy')
def load(p):return json.loads(pathlib.Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def module(n,p):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=module('frozen_old',P/'evidence/old/17592186078584.py')
def number(a):return int(re.search(r'-?\d+',a[':answer/value'])[0])
def info(r):
 q=r.get('question',r);f=q[':question/answer-fields'][0];c=f[':answer-field/correct'];cid=c[1] if isinstance(c,list) else c[':answer/id'];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==cid);vals=[number(a) for a in f[':answer-field/choices']]
 return dict(id=q[':question/id'],answer=number(a),rank=sorted(vals).index(number(a))+1,values=vals,template=r.get('generation',{}).get('template'))
def norm(s):return re.sub(r'\s+','',s.replace('\\\\','\\').replace(r'\left','').replace(r'\right','').replace(r'\,',''))
inventory=load(J/'source/inventory.json');stored={q[':question/id']:q for q in inventory['questions']}
generated=[];matches=[];affected=[]
for r in load(E/'previous-generated-records.json'):
 meta=r['generation'];lv=r['question'][':question/difficulty'].split('/')[-1]
 candidates=[old.generate(lv,meta['seed']),old.generate(lv,meta['seed'],meta['template'])]
 rr=next(x for x in candidates if x==r);generated.append(rr)
 q=stored[rr['question'][':question/id']];v=info(rr);sv=info(q)
 matched=norm(q[':question/problem'])==norm(rr['question'][':question/problem']) and norm(q[':question/worked-solution'])==norm(rr['question'][':question/worked-solution']) and sorted(sv['values'])==sorted(v['values']) and sv['answer']==v['answer']
 assert matched and v['rank']==4
 matches.append(dict(question_id=v['id'],entity_id=q[':db/id'],exact_generation_replay=rr==r,stored_prompt_solution_bank_key_match=matched,rank=v['rank'],generation=meta))
 affected.append(dict(question_id=v['id'],entity_id=q[':db/id'],finding='Historical pre-repair generated target-time bank has a fixed second-largest correct value in its recognizable template. Current repair does not update stored records.',reproduction=f"{sys.executable} -B {E}/inventory-and-selection.py; frozen old generate({lv!r}, seed={meta['seed']}, template={meta['template']!r})",evidence_path='generated-records.json'))
save('generated-records.json',generated);save('affected-inventory.json',{'affected_questions':affected})
original={q[':question/id'] for q in load(J/'source/source.json')['material']['kp'][':knowledge-point/questions']}
assert not original.intersection({a['question_id'] for a in affected})
save('inventory-results.json',{'basis':inventory['basis'],'provenance':'Earlier independent generated records copied with matching source/inventory bindings, then all seven freshly reproduced using old executable whose bytes match earlier package hash. Stored complete prompt, solution, bank and key compared.','matches':matches,'original_questions_excluded':len(original),'unclassified_stored_question_ids':sorted(set(stored)-original-{a['question_id'] for a in affected}),'assessment':'Seven historical generated questions remain affected. This is an existing-pool follow-up, not a demonstrated failure in the repaired generator or its new runner batch.'})

# Rust select() reproduction: SHA-256 draw, sorted deduplicated fresh IDs,
# weighted rated band first and uniform member second. Explicit zero weights
# cannot fall back to a zero-weight rated band. Unknowns only if no rated pool.
def select(candidates,distribution,seed,seen=()):
 candidates=sorted({c['entity_id']:c for c in candidates if c['entity_id'] not in seen}.values(),key=lambda q:q['entity_id'])
 if distribution is None:return candidates[0] if candidates else None
 digest=hashlib.sha256(('course-academy/question-selection/v1/'+seed).encode()).digest()
 def u(offset):return (int.from_bytes(digest[offset:offset+8],'big')>>11)/(1<<53)
 bands=[[q for q in candidates if q['band']==b] for b in ['easy','moderate','hard']]
 total=sum(w for w,qs in zip(distribution,bands) if qs)
 if total:
  draw=u(0)*total;chosen=None
  for w,qs in zip(distribution,bands):
   if not qs or w==0:continue
   chosen=qs
   if draw<w:break
   draw-=w
  pool=chosen
 else:pool=[q for q in candidates if q['band'] is None]
 return pool[int(u(8)*len(pool))] if pool else None
candidates=[dict(entity_id=q[':db/id'],id=q[':question/id'],band=q[':question/difficulty'][':db/ident'].split('/')[-1],rank=info(q)['rank'],origin='captured inventory') for q in inventory['questions']]
batch=load(E/'delivery-batch/accepted.json')
# Future IDs are unavailable before publication. Explicit simulation IDs preserve
# the actual sort/uniform mechanics without pretending to know allocation.
prospective=[dict(entity_id=max(q['entity_id'] for q in candidates)+100+i,id=r['question'][':question/id'],band='easy',rank=info(r)['rank'],origin='prospective batch; simulated entity ID') for i,r in enumerate(batch)]
draws=[]
for weights in [None,[1,0,0],[1,1,1],[0,1,0]]:
 for prefix in [0,1,3]:
  seen=[q['entity_id'] for q in candidates[:prefix]]
  for k in range(12):
   seed=f'independent-selection-9326-{k}';chosen=select(candidates+prospective,weights,seed,seen)
   draws.append(dict(weights=weights,seen_before_or_prefix=seen,seed=seed,selected=chosen))
stages={}
for label in ['batch','easy','moderate','hard']:
 raw=load(E/f'delivery-{label}-input.json');accepted=load(E/f'delivery-{label}/accepted.json')
 stages[label]={'raw_count':len(raw),'accepted_count':len(accepted),'raw_ranks':dict(collections.Counter(info(r)['rank'] for r in raw)),'accepted_ranks':dict(collections.Counter(info(r)['rank'] for r in accepted)),'raw_templates':dict(collections.Counter(info(r)['template'] for r in raw)),'accepted_templates':dict(collections.Counter(info(r)['template'] for r in accepted))}
 assert stages[label]['raw_ranks']==stages[label]['accepted_ranks'] and stages[label]['raw_templates']==stages[label]['accepted_templates']
save('selection-inputs.json',{'captured':candidates,'prospective':prospective,'draws':draws})
save('delivery-selection.json',{'inventory_basis':inventory['basis'],'publication_preparation':'Absent; shared actual read-only delivery filter run on captured inventory.','stages':stages,'generator_rejection':'Inspected guard, sample and integer_bank/generate. desired_below chosen before parameters; bank rank adapts to feasible integer room instead of rejecting valid easy IVPs. Fresh attempts logged in raw-coverage.json; explicit lower/upper rounded endpoints accepted. Only bounded domain resampling remains.','selection_source':str(R/'engine/rust/question_selection.rs'),'selection_hash':hashlib.sha256((R/'engine/rust/question_selection.rs').read_bytes()).hexdigest(),'selection_rule':'seen_before_task removes previous tasks; caller also excludes current prefix. select() sorts/deduplicates IDs; None distribution picks first; otherwise weights choose nonempty rated band, then uniform member. Unrated fallback only when no eligible weighted band.','captured_band_counts':dict(collections.Counter(q['band'] for q in candidates)),'selection_evidence':'selection-inputs.json','selection_conclusion':'Within a positively weighted band, candidate rank/option shape does not affect eligibility or draw; new batch has ranks 2,2,1,5,3. Seen exclusions can change any finite pool; no guarantee for arbitrary learner histories is asserted. Existing affected target-time inventory is separately reported.','limitations':['No live learner history or policy weights supplied. Tested conditional weighted/unconfigured rules and seen-prefix examples against captured IDs; future batch entity IDs are explicitly simulated.','Captured inventory basis5392; later inventory changes can alter deduplication and available candidates.','No publication or database writes performed.']})
print(json.dumps({'affected_inventory':len(affected),'stages':stages,'selection_draws':len(draws)},indent=2))
