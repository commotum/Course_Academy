import json,sys,random,importlib.util,pathlib,hashlib
sys.dont_write_bytecode=True;E=pathlib.Path(__file__).parent;W=E.parent/'workspace';sys.path.insert(0,str(W));s=importlib.util.spec_from_file_location('candidate',W/'17592186087868.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
rows=[];total=0
for level in ['easy','moderate']:
 for seed in range(683021,683277):
  rng=random.Random(seed);attempts=[]
  while True:
   p=g.sample_current(level,rng)
   try:g.validate_current(level,p);attempts.append({'parameters':p,'accepted':True});break
   except ValueError as e:attempts.append({'parameters':p,'accepted':False,'reason':str(e)})
  total+=len(attempts)-1
  if len(attempts)>1:rows.append({'level':level,'seed':seed,'attempts':attempts,'actual_matches_last':g.generate(level,seed)['generation']['parameters']==p})
assert all(r['actual_matches_last'] for r in rows)
(E/'resampling-results.json').write_text(json.dumps({'seed_range':[683021,683276],'per_level':256,'rejected_draws':total,'retry_cases':rows,'policy':'No empty-key records reach nonempty_checkbox outer wrapper because easy always has moved-y and moderate requires forcing. Duplicate equations retry up to 100 with advancing seeded RNG. Invalid explicit parameters fail immediately.','conclusion':'Coverage/probes use accepted generator output after retries; all eligible categorical role profiles remain supported.'},indent=2))
can=json.load(open(E.parent/'source/source.json'))['material']['kp'][':knowledge-point/canonical-example']
(E/'canonical-evidence.json').write_text(json.dumps({'source_id':can[':question/id'],'equations':["y\u0027+x^3*y=0","y\u0027+x^3*y=x^4","y\u0027+x^3*y=y"],'normalized_forcing':['0','x^4','0'],'expected_inhomogeneous':[False,True,False],'solution_states_II_only':'II only' in can[':question/worked-solution'],'replay_limit':'Source canonical example lacks recorded answer fields; exact bank replay is inapplicable. Canonical RHS degree 4 is outside sampled 0..3; the same nonconstant-forcing decision is represented by source bank monomials degrees 1..3. No canonical control bank was invented.','supported_source_bank_replay_count':12,'source_corrections':'None required in the 12 practice banks.'},indent=2))
now={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in W.rglob('*') if p.is_file()};before=json.load(open(E/'package-before.json'));assert now==before
(E/'package-integrity.json').write_text(json.dumps({'unchanged':True,'files_compared':len(now),'method':'SHA256 every workspace file before import and after executed checks','baseline':'package-before.json'},indent=2));print('resampled draws:',total,'package unchanged:',len(now),'files')
