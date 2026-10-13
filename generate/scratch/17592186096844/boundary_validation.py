"""Exercise supported bounds and signed/zero shifts, and prove finite/identity limits."""
import json,subprocess
import validate as v
g=v.g
parameters={
'q-11973':[{'a':1,'b':1,'c':7},{'a':9,'b':5,'c':3}],
'q-2396':[{'a':1,'b':0,'c':2},{'a':9,'b':-5,'c':7}],
'q-11978':[{'a':1},{'a':9}],
'q-2403':[{'a':1},{'a':9}],
'q-313362':[{'a':1,'b':1,'c':1},{'a':9,'b':5,'c':7}],
'q-313365':[{'a':1,'b':0},{'a':9,'b':-5}],
'q-344143':[{'a':1,'b':0},{'a':9,'b':5}],
'q-343546':[{'a':1,'k':3},{'a':9,'k':5}],
'q-343576':[{'a':1,'b':0,'c':1},{'a':9,'b':-5,'c':1},{'a':6,'b':2,'c':2}],
'q-132975':[{'a':1,'b':1,'c':1},{'a':9,'b':5,'c':7}],
'q-313371':[{'a':1},{'a':9}]}
items=[]
for name,params in parameters.items():
 for i,p in enumerate(params):
  r=g.generate(g.CASES[name][0],53,name,p);v.independent(r)
  items.append({'label':name+' boundary '+str(i),'record':r,'checks':v.checks(r)})
  other=g.generate(g.CASES[name][0],54,name,p)
  assert other['question'][':question/id']==r['question'][':question/id']
  assert other['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
  assert {a[':answer/id'] for f in other['question'][':question/answer-fields'] for a in f[':answer-field/choices']}=={a[':answer/id'] for f in r['question'][':question/answer-fields'] for a in f[':answer-field/choices']}
r1=g.generate('moderate',1,'q-11973',{'a':1,'b':1,'c':3})
r2=g.generate('moderate',1,'q-11973',{'a':4,'b':2,'c':6})
v.independent(r1);v.independent(r2)
assert r1['generation']['parameter_fingerprint']==r2['generation']['parameter_fingerprint']
assert r1['question'][':question/id']!=r2['question'][':question/id'],'Different complete banks must not share question identity'
# Count beyond the hard universe must stop at nine genuinely different tasks.
finite=g.batch('hard',20,17);assert len(finite)==9 and len({r['generation']['parameter_fingerprint'] for r in finite})==9
for params in [{'a':1,'b':-1,'c':1}]:
 try:g.generate('moderate',1,'q-343576',params)
 except AssertionError:pass
 else:raise AssertionError('Singular evaluation admitted')
for name,params in [('q-11973',{'a':3,'b':3,'c':1}),('q-2396',{'a':7,'b':-2,'c':1})]:
 try:g.generate('moderate',1,name,params)
 except AssertionError:pass
 else:raise AssertionError('Colliding profile admitted')
try:g.batch('easy',5,1)
except AssertionError:pass
else:raise AssertionError('Unvalidated easy level admitted')
(v.H/'boundary-native-input.json').write_text(json.dumps(items,indent=2)+'\n')
subprocess.run([str(v.ROOT/'generate/runs/current/check-engine'),str(v.H/'boundary-native-input.json'),str(v.H/'boundary-native-report.json')],check=True)
report=json.loads((v.H/'boundary-native-report.json').read_text());assert report['documented_unresolved_checks']==0
(v.H/'boundary-validation.json').write_text(json.dumps({'status':'pass','tested_instances':len(items),'hard_requested':20,'distinct_hard_returned':9,'seed_and_order_do_not_change_identity':True,'singular_evaluation_rejected':True,'complete_bank_collisions_rejected':True,'easy_rejected':True,'native_report':'boundary-native-report.json'},indent=2)+'\n')
print('Boundary and finite-limit checks passed.')
