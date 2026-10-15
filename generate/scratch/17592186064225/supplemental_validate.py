"""Semantic finite-capacity and correlated endpoint-mutation checks."""
import sys
sys.dont_write_bytecode=True
import copy,importlib.util,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
z=importlib.util.spec_from_file_location('product_validation',HERE/'validate.py');V=importlib.util.module_from_spec(z);z.loader.exec_module(V);G=V.G
seen=set();profiles={}
for profile,f,base in G.CASES:
 if G.level(profile)!='easy':continue
 keys=list(base);domains=[range(2,10)if k=='n'else range(1,6)for k in keys];count=0
 for values in itertools.product(*domains):
  rec=G.generate('easy',0,profile,dict(zip(keys,values)));V.check(rec);seen.add(rec['generation']['task_fingerprint']);count+=1
 profiles[profile]=count
assert len(seen)==116
# Scaled radio banks have exactly the three zero-integral symmetric pairs excluded.
accepted=[];rejected=[]
for k in range(2,7):
 for l,h in itertools.combinations(G.ANGLES,2):
  try:rec=G.generate('moderate',0,'q-51109',dict(k=k,l=l,h=h))
  except ValueError as err:
   assert 'collides'in str(err)and l==-h;rejected.append([k,l,h]);continue
  V.check(rec);accepted.append([k,l,h])
assert len(accepted)==90 and len(rejected)==15
mutations=[]
for profile,f,params in G.CASES:
 if G.level(profile)=='easy':continue
 rec=G.generate(G.level(profile),0,profile,params);q=rec['question'];sol=q[':question/worked-solution'];parts=list(V.rowparts(sol));i=next(i for i,p in enumerate(parts)if '|_'in V.clean(p));bartext=V.clean(parts[i]);prefix,after=bartext.split('|_',1);lo,j=V.D.group(after,0);assert after[j]=='^';hi,j=V.D.group(after,j+1);assert not after[j:];bar=V.E.scalar(prefix);var=V.u if bar.has(V.u)else V.x;lo,hi=V.E.scalar(lo),V.E.scalar(hi)
 # Both signed endpoint components are shifted by1. Their difference remains
 # correct, so only independent per-component reading can reject this mutation.
 changed='('+G.tex(bar.subs(var,hi)+1)+')-('+G.tex(bar.subs(var,lo)+1)+')'
 bad=copy.deepcopy(rec);bad['question'][':question/worked-solution']=sol.replace(parts[i+1],changed,1)
 try:V.check(bad)
 except (AssertionError,ValueError):mutations.append(profile)
 else:raise AssertionError('correlated endpoint shift escaped '+profile)
 # Change only the supplied limit; stale solution/table/bank must be rejected.
 bad=copy.deepcopy(rec);problem=bad['question'][':question/problem'];bad['question'][':question/problem']=problem.replace('^{'+G.tex(hi if var==V.x else hi/params['k'])+'}','^{0}',1)
 if bad['question'][':question/problem']!=problem:
  try:V.check(bad)
  except (AssertionError,ValueError):pass
  else:raise AssertionError('stale limit mutation escaped '+profile)
report={'easy_exhaustive_tasks':len(seen),'easy_profiles':profiles,'moderate_scaled_bank_tasks':len(accepted),'moderate_scaled_profile_collision_rejections':rejected,'semantic_capacity':{'easy':116,'moderate':636,'hard':6615},'capacity_derivation':{'easy':'Four independent positive1..5 coefficient pairs plus two denominator2..9 slots:4*25+2*8.','moderate':'Unscaled cos-tan21 endpoint tasks (radio/blank aliases collapse), reciprocal-sec25*21 tasks (two prose profiles collapse), scaled cos-tan90 tasks:21+525+90.','hard':'Two one-term masks each9 outer coefficients*5 frequencies*21 endpoint pairs, plus two-term mask additionally5 inner coefficients:2*945+4725.'},'correlated_endpoint_mutations_rejected':mutations}
(HERE/'supplemental-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
