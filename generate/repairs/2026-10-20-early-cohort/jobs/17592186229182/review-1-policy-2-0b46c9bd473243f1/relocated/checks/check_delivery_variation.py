"""Compare visible decision cues through actual delivery, plus bounded selection analysis."""
import pathlib,json,sys,hashlib,collections
sys.dont_write_bytecode=True
P=pathlib.Path(__file__).resolve().parents[1];E=P/'evidence';sys.path.insert(0,str(P/'checks'))
from validate_repair import coverage,score,key,g,w
accepted=[];stages={}
for level in ['easy','moderate','hard']:
 r=json.loads((E/f'delivery-{level}/accepted.json').read_text());accepted+=r
 stages[level]={k:v for k,v in json.loads((E/f'delivery-{level}/delivery.json').read_text()).items() if k in ['input_count','duplicate_count','accepted_count','inventory_basis','database_writes']}
c=coverage(accepted);(E/'coverage-after.json').write_text(json.dumps(c,indent=2))
one=c['q-336439:single-digit'];assert one['count']>=5 and len(one['ranks'])>=3 and one['second_smallest_successes']<one['count']
for name,rows in c.items():
 # A small subgroup can have only one observed item, so do not claim it tests a predictor.
 if rows['count']>=8:
  assert len(rows['ranks'])>1,(name,rows)
  assert len(rows['positions'])>1,(name,rows)
semantic=collections.defaultdict(set)
for r in accepted:semantic[r['question'][':question/difficulty']].add(r['generation']['mathematical_fingerprint'])
# Retain read-only model of the actual selector conditional on positive weight for easy.
# Its SHA uniform within a band cannot read choice rank. Fresh usable candidate IDs
# are hypothetical; histories/policy/reservations are not available in the snapshot.
easy=[r for r in accepted if r['question'][':question/difficulty'].endswith('/easy')]
selected=[]
for seed in range(1000,1100):
 h=hashlib.sha256(('course-academy/question-selection/v1/'+str(seed)).encode()).digest()
 draw=(int.from_bytes(h[8:16],'big')>>11)/float(1<<53)
 selected.append(easy[int(draw*len(easy))])
selection=coverage(selected)
# Measure ordinary sampling independently of controlled sign cases.
normal=[];signs={};attempts={}
for ma,m in g.M.items():
 rows=[];trials=[];old=g.guard
 def observe(p,meta,level,evidence=False):
  try:
   d=old(p,meta,level,evidence);trials.append({'passed':True,'sign':int(w.sp.sign(d['beta']))});return d
  except ValueError as exc:
   trials.append({'passed':False,'reason':str(exc)});raise
 g.guard=observe
 try:
  for seed in [0,1,5]:
   r=g.generate(m['level'],seed,template=ma);env=w.check_math(r);normal.append(r);rows.append(int(w.sp.sign(env['beta'])))
 finally:g.guard=old
 assert set(rows)=={-1,0,1},(ma,rows)
 signs[ma]=rows;attempts[ma]={'trials':len(trials),'accepted':sum(z['passed'] for z in trials),'reasons':dict(collections.Counter(z.get('reason') for z in trials if not z['passed']))}
(E/'normal-sampling.json').write_text(json.dumps(normal,indent=2))
report={'stages':stages,'post_delivery_single_digit':one,'semantic_instances':{k:len(v) for k,v in semantic.items()},'semantic_definition':'Easy: initial mass only. Moderate/hard: physical parameters and time; numerical tasks are genuine here; repeated distractors/IDs/positions do not count. This conservatively inherited fingerprint can overcount proportional flow/volume changes in moderate/hard, so normalized ODE count below is authoritative.','normal_sign_coverage':signs,'generator_rejection':attempts,'selector':{'implementation':'engine/rust/question_selection.rs:105-198','conditional_easy_weight_positive':True,'fresh_candidate_count':len(easy),'simulated_draws':100,'coverage':selection,'limits':'Hypothetical monotone entity IDs in accepted order; no actual learner history, reservations, future inventory or weights supplied. Disabled difficulty weights can remove a whole band; histories can remove arbitrary instances. No claim of universal learner pool balance.'},'cue_limits':'One-choice radio count is required. Easy initial mass directly supplies alpha+beta by the stated initial condition: this is the intended source simplification. No mathematical reason to vary the requested operation within a difficulty. Small subgroups report observations, not universal absence of predictors.'}
normalized=collections.defaultdict(set)
for r in accepted:
 env=w.physics(r);level=r['question'][':question/difficulty']
 normalized[level].add(str(env['q']) if env['kind']=='sum' else str((env['J'],env['B'],env['m'],env['s'],env['q'],env['T'])))
report['normalized_ODE_semantic_instances']={k:len(v) for k,v in normalized.items()}
(E/'pedagogical-variation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'delivery':stages,'single_digit':one,'normalized_semantic_instances':report['normalized_ODE_semantic_instances'],'ordinary_signs_all_profiles':True}))
