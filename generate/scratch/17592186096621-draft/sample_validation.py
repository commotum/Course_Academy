#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('qa',HERE/'validate.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v);g=v.g
records=[];profiles={};targets={};scales={};stages=0;formal=0;rejects=[]
for t in [*g.SPEC,g.HARD]:
 level='hard' if t==g.HARD else g.SPEC[t][3]
 for seed in [0,1,7,19,83,211]:
  r=g.generate(level,seed,t);z=v.read(r);stages+=z['stages'];formal+=z['formal_inputs'];records.append(r);profiles[r['generation']['bank_profile']]=profiles.get(r['generation']['bank_profile'],0)+1
  if 'target' in r['generation']['parameters']:targets.setdefault(t,[]).append(r['generation']['parameters']['target'])
  if 'scale' in r['generation']['parameters']:scales.setdefault(t,[]).append(r['generation']['parameters']['scale'])
 # Deterministic complete record, including option shuffle and IDs.
 assert g.generate(level,83,t)==g.generate(level,83,t)
# Every declared exact target slot is actually exercised; collision means whole profile rejection.
for t,points in g.TARGETS.items():
 for target in points:
  try:r=g.generate('moderate',83,t,{'scale':1,'target':target})
  except ValueError as e:
   assert 'complete bank rejected' in str(e),(t,target,str(e));rejects.append({'template':t,'target':target,'reason':str(e)});continue
  z=v.read(r);stages+=z['stages'];formal+=z['formal_inputs'];records.append(r)
# Valid 0 and 1 answers arise naturally without deleting substantive operands.
for target,value in [('0',1),(r'\frac{1}{3}',0)]:
 r=g.generate('moderate',0,'q-340318',{'scale':1,'target':target});z=v.read(r);assert z['answer']==value;records.append(r)
# Mathematical task dedup ignores profile, seed/order, simultaneous scale aliases.
u,w=g.SPEC['q-340309'][:2]
assert g.task_identity(u,w,None)==g.task_identity(3*u,3*w,None)
# Distinct answer-fragment contracts must not share question IDs.
a=g.generate('easy',0,'q-167328',{'scale':1});b=g.generate('easy',0,'q-167782',{'scale':1});assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
for bad in [True,1.0,'1',None]:
 try:g.generate('easy',bad,'q-340309',{'scale':1});raise AssertionError('bad seed accepted')
 except ValueError:pass
for t in g.SPEC:
 raw=g.replay_raw(t);assert raw['question']==g.SOURCES[t] and raw['generation']['evidence_only'] and not raw['generation']['eligible']
result={'records':len(records),'rendered_stages':stages,'formal_derivative_inputs':formal,'profiles':profiles,'sampled_targets':targets,'sampled_scales':scales,'whole_bank_collision_rejections':rejects,'determinism_families':16,'raw_public_replays':15,'raw_omissions_preserved':True,'natural_zero_one_answer_checks':2,'bad_seed_rejections':4,'identity_and_domain_checks':True,'failures':[]}
(HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');(HERE/'sample-records.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(result,indent=2))
