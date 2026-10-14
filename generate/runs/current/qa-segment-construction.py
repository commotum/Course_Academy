"""Root checks whole definite values, source banks and all construction stages."""
import hashlib,importlib.util,json,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186179724;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);sys.modules[n]=m;spec.loader.exec_module(m);return m
P=mod('root_construct_reader',R/'segment-readback.py');G=mod('root_construct_generator',D.with_suffix('.py'));F=mod('root_construct_source',R/'root-source-fidelity.py');O,Fid=F.check(G,K,D)
C=dict(records=0,choice_values=0,bank_pairs=0,source_solution_masks=0);rows=json.load(open(R/f'qa/{K}-sampled.json'))
for c in json.load(open(D/'source-cases.json')):
 rows.append(G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
for r in rows:
 q,m=r['question'],r['generation'];f,A,B,path,dr,speed,h=P.objects(q[':question/problem'],2);expected=s.simplify(speed*s.integrate(h,(P.t,0,1)))
 F=q[':question/answer-fields'][0];vals=[P.value(a[':answer/value']) for a in F[':answer-field/choices']];assert len(vals)==5
 assert [a[':answer/id'] for a,v in zip(F[':answer-field/choices'],vals) if P.same(v,expected)]==[F[':answer-field/correct'][1]]
 for i,v in enumerate(vals):
  assert v.is_real is True and v.is_finite is True
  for w in vals[i+1:]:assert not P.same(v,w);C['bank_pairs']+=1
 if m['bank_profile'].endswith('_method'):
  numbers=list(A+B);denominators=sorted(v.q for v in numbers if v.q!=1);level=q[':question/difficulty'].split('/')[-1]
  assert denominators==({'easy':[],'moderate':[2],'hard':[2,3]}[level])
  assert all(abs(v)<=6 for v in numbers+list(dr))
  if level!='easy':assert all(dr)
  if m['template']=='exp':assert A==(0,0)
  x,y=path;ax,ay=A;n=speed**2
  wrong=[s.integrate(z,(P.t,0,1)) for z in [speed*h,h,n*h,speed*f.subs({P.p.x:ax,P.p.y:y},simultaneous=True),speed*f.subs({P.p.x:x,P.p.y:ay},simultaneous=True)]]
  assert all(any(P.same(v,w) for w in vals) for v in wrong)
 stages,bs,ri=P.stages(q[':question/worked-solution'],f,A,B,path,dr,speed,h,2)
 assert len(bs)==5 and len(ri)==3 # Construct, never learner evaluation.
 for k,v in stages.items():C[k]=C.get(k,0)+v
 sid=G.SOURCE_IDS[m['template']];assert P.mask(q[':question/worked-solution'])==P.mask(O[sid][':question/worked-solution']);C['source_solution_masks']+=1
 C['choice_values']+=5;C['records']+=1
out={'passed':True,'source_fidelity':Fid,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
