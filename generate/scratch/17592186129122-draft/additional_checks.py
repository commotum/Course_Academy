"""Additional draft regressions run within validate.py's independent reader namespace."""
# Verify every declared build input/output against the current engine provenance.
m=json.loads((H/'reference/grader-build.json').read_text());files={m['source']:m['source_sha256'],m['library']:m['library_sha256'],m['binary']:m['binary_sha256'],**m['engine_sources'],**m['dependencies']}
assert len(files)==42
for path,expected in files.items():assert hashlib.sha256((REPO/path).read_bytes()).hexdigest()==expected,('native provenance mismatch',path)
save('grader-provenance-check.json',{'status':'pass','verified_hashes':len(files),'files':files,'database_writes':0})
# Exact wrapper, original MA coverage and zero independently authored records.
assert (H/'source.json').read_bytes()==(REPO/'generate/runs/current/sources/17592186129122.json').read_bytes()
assert len(sources)==len(cases)==8 and {q[':question/math-academy-id'] for q in sources}=={c['source_id'] for c in cases}
assert all(':question/math-academy-id' in q for q in g.CAPTURE['record'][':knowledge-point/questions'])
# Normal original-parameter solutions preserve the full normalized source wording,
# with only the explicitly documented missing-solution/rule repairs.
normal_anchors=[];normal_changed=[]
for q,c in zip(sources,cases):
 p={k:v for k,v in c['parameters'].items() if not k.startswith('o')}
 r=g.generate('easy',template=c['template'],parameters=p);verify(r);normal_anchors.append(r)
 expected=q.get(':question/worked-solution')
 if expected is not None:
  if c['source_id']=='q-43411':expected=expected.replace('the period is ${360}^{∘}.$',r'the period is $\frac{{360}^{∘}}{B}.$')
  assert r['question'][':question/worked-solution']==g.normalize_prose(expected),('normal anchor structure',c['source_id'])
 assert r['question'][':question/problem']==g.normalize_prose(q[':question/problem'])
 for seed in (81,91):
  r=g.generate('easy',seed,template=c['template']);verify(r);normal_changed.append(r)
  sol=r['question'][':question/worked-solution'];_,period,unit,_,_=prompt_math(r['question'])
  # Preserve the original general-form opening and its identify/divide conclusion.
  assert sol.startswith(g.normalize_prose((expected or g.authored_solution(unit,g.SPECS[c['template']]['trig'],1,1,False)).split('\n\n')[0]))
  assert 'In our case, we have that $B=' in sol and 'Therefore, the period is $' in sol
  last=re.findall(r'\$(.*?)\$',sol)[-1];assert last.count('=')==(2 if c['source_id']=='q-53457' else 1) and last.startswith(r'\frac')
  assert sp.simplify(parse(last.split('=')[0])-period)==0
save('normal-anchors.json',normal_anchors)
# Hold all other parameters fixed while varying every declared numeric/context slot.
slots=[]
for level in g.LEVELS:
 for name in [n for n,l in g.TEMPLATES.items() if l==level]:
  base=g.generate(level,13,template=name);p=base['generation']['parameters']
  alternatives={}
  # Find another eligible value of each slot without changing any other slot.
  for seed in range(120):
   candidate=g.generate(level,seed,template=name)['generation']['parameters']
   for slot,keys in [('amplitude',('a_n','a_d')),('frequency',('b_n','b_d')),('shift',('c_n','c_d')),('unit',('unit',)),('trig',('trig',)),('factor',('k',))]:
    if slot in alternatives or not all(k in p for k in keys) or all(candidate[k]==p[k] for k in keys):continue
    pp={**p,**{k:candidate[k] for k in keys}}
    try:out=g.generate(level,template=name,parameters=pp)
    except ValueError:continue
    verify(out);alternatives[slot]=out
   if len(alternatives)>=(3 if level=='easy' else 5 if level=='moderate' else 6):break
  required={'frequency'}
  if level!='easy' or g.SPECS[name]['a_style']!='unit':required.add('amplitude')
  if level!='easy' or name!='rad_cos_fraction':required.add('shift')
  if level!='easy':required|={'unit','trig'}
  if level=='hard':required.add('factor')
  assert required<=set(alternatives),(name,required-set(alternatives))
  for slot,out in alternatives.items():
   assert out['question'][':question/problem']!=base['question'][':question/problem']
   ff=base['generation']['mathematical_task_fingerprint']==out['generation']['mathematical_task_fingerprint']
   assert ff==(slot in ('amplitude','shift','trig')),(name,slot)
   slots.append({'level':level,'template':name,'slot':slot,'held_parameters':p,'changed_parameters':out['generation']['parameters'],'record':out})
save('held-slot-checks.json',slots)
# Explicit C0 corruption must fail before identity generation, even if a parser
# could treat it as whitespace. Raw evidence remains separately ineligible.
original_build=g.build;original_uid=g.uid;c0_checks=0
for index in (0,1,2):
 def corrupt(*args,**kwargs):
  built=list(original_build(*args,**kwargs))
  if index<2:built[index]+='\x0c'
  else:built[2][0]+='\x0c'
  return tuple(built)
 def no_identity(*args):raise AssertionError('identity computed before C0 rejection')
 g.build=corrupt;g.uid=no_identity
 try:g.generate('moderate',6)
 except ValueError as e:assert 'C0' in str(e);c0_checks+=1
 else:raise AssertionError('C0 not rejected')
 finally:g.build=original_build;g.uid=original_uid
for c in ('\x00','\x08','\x0c','\x1f'):
 z=copy.deepcopy(normal_anchors[0]);z['question'][':question/worked-solution']+=c
 try:verify(z)
 except AssertionError:c0_checks+=1
 else:raise AssertionError('independent reader tolerated C0')
save('additional-validation.json',{'status':'pass','native_build_hashes_checked':42,'MA_sources':8,'nonMA_inventory':0,'normal_original_parameter_stage_reproductions':8,'normal_changed_parameter_stage_checks':len(normal_changed),'held_slot_checks':len(slots),'C0_rejections_before_identity_and_reader':c0_checks,'basis':1356,'basis_rationale':'Refreshed basis2275 wrapper is absent for this already-started KP. Parent explicitly authorized original1356 provenance. Registered source.json is byte-exact original wrapper.','prior_proofs_preserved':'reference/prior-17592186129122*.json and reference/reviewed.py; original basis1356 conclusions retained, current code normalization and C0 rejection revalidated.'})
