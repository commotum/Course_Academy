"""Run with --old to demonstrate retained failures; default checks current package."""
from review_lib import *
old='--old' in sys.argv
path=JOB/'review-0-policy-2-8b996ed7d80a08a9/relocated/17592186096669.py' if old else PACKAGE/'17592186096669.py'
spec=importlib.util.spec_from_file_location('target',path);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
failures=[]
try:g.generate(profile='q-20450',scale=1)
except Exception as e:failures.append({'finding':'missing source q-20450','error':str(e)})
r=g.generate(profile='q-129453',seed=73421,scale=4);m=inspect(r);positive=[i for i,v in enumerate(m['bank']) if sp.Rational(v[1])>0]
if len(positive)==1 and positive[0]==m['correct_index']:failures.append({'finding':'unique positive middle shortcut','record':r})
# Also require actual controlled change of correct role, not just defeat one old sample.
if not old:
 rs=[g.generate(profile='q-129453',seed=73421,scale=4,target=t,signs=(1,1,1),shifts=(0,0,0)) for t in range(5)]
 assert len({inspect(v)['correct_index'] for v in rs})==5
save('strict-old-results.json' if old else 'strict-current-results.json',{'command':sys.argv,'module':str(path),'failures':failures})
assert not failures, str([f['finding'] for f in failures])
