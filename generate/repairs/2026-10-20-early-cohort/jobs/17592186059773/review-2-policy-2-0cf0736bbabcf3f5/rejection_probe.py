import random,sys
from review import E,save,module,inspect,load
sys.dont_write_bytecode=True
g=module(E/'runtime/17592186059773.py','rejection_generator')
p=['q-130098',0,0,-2,[0,1,2],0]
try:g.generate(seed=711,parameters=p);raise AssertionError('identity swap was accepted')
except g.InvalidInstance as ex:rejection={'parameters':p,'exception':type(ex).__name__,'message':str(ex),'reason':'Changing 7 to 5 makes rows 1 and 3 equal; the swap produces identity, and some distractor outcomes coincide.'}
# Independently search RNG proposals only for a seed that exercises that exact rejection.
domains={s:g.domain(s) for s in g.CASES}
for seed in range(20000):
 rng=random.Random(seed);sid=rng.choice(list(g.CASES));key=rng.choice(g.eligible_keys(sid));q=rng.choice(domains[sid])+[key]
 if q[:4]==p[:4] and key==0:break
else:raise AssertionError('witness seed missing')
records=g.batch('moderate',5,seed);assert len(records)==5
for r in records:inspect(r)
assert records[0]['generation']['parameters']!=q
save('rejection-witness-records.json',records);save('rejection-witness.json',{'explicit_rejection':rejection,'batch_seed':seed,'first_draw_rejected':q,'returned_count':5,'first_returned_parameters':records[0]['generation']['parameters'],'passed':True})
print({'batch_seed':seed,'first_draw':q,'returned':len(records)})
