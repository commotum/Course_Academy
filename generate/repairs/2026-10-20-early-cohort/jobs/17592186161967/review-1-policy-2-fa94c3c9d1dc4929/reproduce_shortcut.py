"""Run with context Python; exits 1 when the family-wide frequency leak is present."""
import sys,json,importlib.util,pathlib,collections,re
sys.dont_write_bytecode=True
p=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent.parent/'workspace/17592186161967.py'
s=importlib.util.spec_from_file_location('subject',p);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def coefficients(r):
 return [[int(s+(n or '1')) for s,n in re.findall(r'R_\{\d\}:=R_\{\d\}([+-])(\d*)R_',a[':answer/value'])] for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
params={'A':[[1,2,3],[2,5,4],[-3,7,8]],'pivot':0,'column':0,'ks':[0,-2,3]}
r=g.generate(seed=472,bank_profile='q-42531',parameters=params);bank=coefficients(r)
print(json.dumps({'parameters':params,'bank_profile':'q-42531','bank':bank,'inferred_first_coefficient':collections.Counter(x[0] for x in bank).most_common(1)[0][0],'correct_first_coefficient':-2}))
results=[]
for profile in ['q-42531','q-130451','q-91162']:
 for seed in range(38191,38203):
  rr=g.generate(seed=seed,bank_profile=profile);bb=coefficients(rr);f=rr['question'][':question/answer-fields'][0];ci=next(i for i,c in enumerate(f[':answer-field/choices']) if c[':answer/id']==f[':answer-field/correct'][1]);mode,n=collections.Counter(x[0] for x in bb).most_common(1)[0];results.append(mode==bb[ci][0] and n==3)
print(json.dumps({'leaked':sum(results),'tested':len(results),'acceptance':'Generalized unit-perturbation profiles must not make the most frequent first coefficient always correct.'}))
sys.exit(1 if all(results) else 0)
