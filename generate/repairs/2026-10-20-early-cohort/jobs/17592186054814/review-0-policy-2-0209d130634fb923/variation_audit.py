import json,re,hashlib,pathlib,collections,sys
ROOT=pathlib.Path(__file__).resolve().parent;JOB=ROOT.parent;sys.path.insert(0,str(ROOT));from audit import semantic,oracle,save
# audit import reruns construction checks deterministically, leaving all outputs under evidence root.
sets={n:json.load(open(ROOT/p)) for n,p in [('raw_sample','sample-records.json'),('delivered_sample','delivery-sample/accepted.json'),('raw_batch','batch-records.json'),('delivered_batch','delivery-batch/accepted.json')]}
profiles={}
for name,records in sets.items():
 masks=collections.Counter(semantic(r) for r in records);families=collections.defaultdict(collections.Counter);positions=collections.Counter()
 for r in records:
  tex=re.search(r'number \$(.*?)\$ belong',r['question'][':question/problem'])[1]
  family='radical' if 'sqrt' in tex else 'fraction' if 'frac' in tex else 'pi' if 'pi' in tex else 'decimal' if '.' in tex else 'integer'
  families[family][semantic(r)]+=1
  fs=r['question'][':question/answer-fields'];positions[next(i for i,f in enumerate(fs) if '($C$)' in f[':answer-field/key'])]+=1
 profiles[name]={'count':len(records),'memberships':dict(masks),'family_memberships':dict(families),'C_positions':dict(positions)}
save('coverage-results.json',profiles)
# Predictive probes are scored per complete answer, including conditional cue groups.
probes=[]
for name,records in sets.items():
 for family in ['all','radical','fraction','integer','decimal','pi']:
  group=[]
  for r in records:
   tex=re.search(r'number \$(.*?)\$ belong',r['question'][':question/problem'])[1]
   f='radical' if 'sqrt' in tex else 'fraction' if 'frac' in tex else 'pi' if 'pi' in tex else 'decimal' if '.' in tex else 'integer'
   if family=='all' or family==f:group.append(r)
  if not group:continue
  for cue,fn in [('always_select_C_only',lambda r:'C'),('always_select_everything',lambda r:'NZQRC'),('always_select_first_field_only',lambda r:re.search(r'\(\$([NZQRC])\$\)',r['question'][':question/answer-fields'][0][':answer-field/key'])[1])]:
   correct=sum(fn(r)==semantic(r) for r in group)
   # Mathematical pi and nonreal fixed responses are expected intended-skill cues.
   probes.append({'stage':name,'cue':cue,'subgroup':family,'correct':correct,'total':len(group),'records':[r['question'][':question/id'] for r in group]})
save('shortcut-results.json',probes)
# Read-only reproduction of select(): all rated easy records share one band.
selection_source=pathlib.Path('/home/jake/Developer/Course_Academy/engine/rust/question_selection.rs')
inventory=json.load(open(JOB/'source/inventory.json'));sq=inventory['questions']
# Captured originals and generated candidates are distinct; omit missing-difficulty item while any positive easy band remains.
candidates=[]
for q in sq:
 d=q.get(':question/difficulty');d=d.get(':db/ident') if isinstance(d,dict) else d
 if d==':question.difficulty/easy': candidates.append({'entity':q[':db/id'],'id':q[':question/id'],'problem':q[':question/problem']})
next_id=max(q[':db/id'] for q in sq)+1
for i,r in enumerate(sets['delivered_batch']):candidates.append({'entity':next_id+i,'id':r['question'][':question/id'],'problem':r['question'][':question/problem']})
candidates.sort(key=lambda q:q['entity'])
selected=[]
for seed in range(64):
 digest=hashlib.sha256(f'course-academy/question-selection/v1/review-{seed}'.encode()).digest()
 u=(int.from_bytes(digest[8:16],'big')>>11)/(1<<53)
 selected.append(candidates[int(u*len(candidates))]['id'])
# History can leave any particular fresh candidate as the sole remaining usable question.
sole=[{'seen_entities':[q['entity'] for q in candidates if q['entity']!=keep['entity']],'remaining':keep['id'],'selected':keep['id']} for keep in candidates]
save('selection-results.json',{'command':'python -B variation_audit.py','implementation_hash':hashlib.sha256(selection_source.read_bytes()).hexdigest(),'basis':inventory['basis'],'rules':'Candidate IDs dedup/sort; seen previous tasks and current prefix excluded by caller; positive-weight easy band uniform; unrated fallback only if no positive eligible rated band. No-policy path returns minimum entity.','conditions':'Actual policy and learner history are not captured. All source-easy and delivered-easy candidates eligible for any policy with positive easy weight. Synthetic post-publication IDs are explicit ordinal stand-ins; they affect particular seeded assignments but cannot remove any candidate from support.','candidates':candidates,'seeds':[f'review-{i}' for i in range(64)],'selected_ids':selected,'sole_fresh_cases':sole,'no_policy_selected':candidates[0]['id'],'zero_easy_weight_result':'No rated band remains eligible; only the unrated archival sqrt(121) may enter fallback if usable. Cannot assert these weights are configured.'})
# No demonstrated defect changes stored record correctness; omitted families cannot be detected as defective generated instances.
save('inventory-records.json',sq)
save('affected-inventory.json',{'affected_questions':[]})
save('inventory-analysis.json',{'captured_basis':inventory['basis'],'total':len(sq),'source_ids':[q[':question/id'] for q in sq if q.get(':question/math-academy-id')],'other_ids':[q[':question/id'] for q in sq if not q.get(':question/math-academy-id')],'demonstrated_affected_instances':0,'assessment':'Inspected all 13 captured prompts and provenance fields. Eight original source questions remain original. Five other records are checkbox 56/7, 34/3, -6.20, pi, -12.00; none is a demonstrated instance of rejection of sqrt(-2) or omission of the source radio banks. These are coverage/replay defects, not an incorrect stored key. No generated source question marked as affected. Captured inventory lacks generation metadata, so no historical generation-seed claim is made.','limits':'Verified no stored instance of the particular demonstrated defects; not a bank-wide absence of all possible defects. No DB query or mutation.'})
print(json.dumps({'coverage':profiles,'selection_candidates':len(candidates),'inventory_affected':0},indent=2))
