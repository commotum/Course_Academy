"""One deterministic generator rejection with the bank role preserved."""
import random,math,json
import generator as g
from validate import independent,grading,save
spec=g.TEMPLATES['slope_sum_radio'];first=None
for seed in range(10000):
 rng=random.Random(seed);role=rng.randrange(5);p=g.sample(spec,rng);root=math.isqrt(p['a']*p['t']+p['b'])
 if p['a']+6*p['k']*p['t']**2*root==0:first=(seed,role,p);break
assert first is not None
seed,role,p=first
try:g.generate('easy',seed,template='slope_sum_radio',parameters=p,profile='scale_bank')
except ValueError:pass
else:raise AssertionError('zero whole bank not rejected')
r=g.generate('easy',seed,template='slope_sum_radio',profile='scale_bank')
assert r['generation']['attempts']>1 and r['generation']['bank_assignment']==role
expected=independent(r)
save('rejection-probe.json',{'seed':seed,'chosen_role':role,'first_rejected_parameters':p,'reason':'zero total slope collapses all five scale-bank choices','accepted_parameters':r['generation']['parameters'],'attempts':r['generation']['attempts'],'role_preserved':True})
save('rejection-grader-input.json',[grading(r,expected,'resampled whole bank')])
print('Seed',seed,'rejects zero bank, then accepts in',r['generation']['attempts'],'attempts; role preserved')
