"""Read the live source mathematics independently; never rewrite source entities."""
import importlib.util, re
from pathlib import Path
import sympy as s
H=Path(__file__).parent
spec=importlib.util.spec_from_file_location('region_reader',H.parents[2]/'generate/runs/current/qa-triple-volume.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
x,y,z=p.x,p.y,p.z;u,v,w=p.UVW
INVERSE={
 17592186198624:(u,(2*v+w)/5,(v-2*w)/5),
 17592186198965:(v-s.sqrt(u),u,1/w-1),
 17592186374152:(u,v-u*u,w/u),
 17592186374159:(u,v-u,w-u*u-(v-u)**2),
 17592186374166:(u-v+w,v,v-w),
 17592186374173:(u,u*u-v-w*w,w*w),
 17592186482547:(v+u*w+1,u,u*w+1),
 17592186482580:(u,v,w+s.log(v*v+1)),
 17592186482615:(u,v-3*w**s.Rational(1,3),w**s.Rational(1,3)),
 17592186482616:(v*v-u,v,w),
 17592186499512:(s.log(v-u),v,w*(v-u)),
 17592186499523:(v,v*v-u,w),
}
FAMILY=dict(zip(INVERSE,('linear_yz','reciprocal','log','shear','linear_xz','sqrt','rational_y','log_shear','cube_triangular','quadratic_y','exp_coupled','quadratic_x')))
def scalar(t):return p.scalar(t.replace('\\\\','\\').replace(r'\u2061',''))
def region(q):
    q=dict(q);q[':question/problem']=q[':question/problem'].replace(r'\leq',r'\le').replace(r'\:', ' ')
    return p.region(q[':question/problem'])
def fingerprint(q):
 trans,bounds=region(q);parts=[]
 for e,(lo,hi) in zip(trans,bounds):
  content,primitive=s.primitive(e);leading=primitive.as_ordered_terms()[0].as_coeff_Mul()[0]
  factor=content*(-1 if leading<0 else 1)
  low,high=(lo/factor,hi/factor) if factor>0 else (hi/factor,lo/factor)
  parts.append([s.srepr(s.expand(e/factor)),s.srepr(low),s.srepr(high)])
 import hashlib,json
 return hashlib.sha256(json.dumps({'region':sorted(parts),'criterion':'volume_from_region'},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def check_source(q):
 eid=q[':db/id'];trans,bounds=region(q);inv=INVERSE[eid]
 for f,target in zip(trans,(u,v,w)):
  assert s.simplify(s.expand_log(f.subs(dict(zip((x,y,z),inv)),simultaneous=True),force=True)-target)==0,(eid,f)
 for lo,hi in bounds:assert hi>lo
 if eid==17592186499512:assert bounds[1][0]>=bounds[0][1] # v-u>0 throughout interior
 J=s.simplify(s.Abs(s.Matrix(inv).jacobian((u,v,w)).det()))
 V=s.simplify(s.integrate(J,(w,*bounds[2]),(v,*bounds[1]),(u,*bounds[0])))
 assert V.is_positive
 fields=q[':question/answer-fields'];issues=[]
 if len({f[':answer-field/key'] for f in fields})!=len(fields):issues.append('duplicate answer-field key')
 for f in fields:
  vs=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
  assert len(vs)==5 and all(s.simplify(a-b)!=0 for i,a in enumerate(vs) for b in vs[:i])
  correct=f.get(':answer-field/correct')
  if not correct:issues.append('missing correct reference');continue
  assert s.simplify(scalar(correct[':answer/value'])-V)==0
  assert any(a[':answer/id']==correct[':answer/id'] for a in f[':answer-field/choices'])
 sol=q.get(':question/worked-solution','');assert sol
 final=sol.rsplit(' & =',1)[1].split(r'.\end{aligned}')[0]
 assert s.simplify(scalar(final)-V)==0
 if eid==17592186198965:issues.append('source introduction incorrectly prints double-integral dA formula for volume')
 return {'id':eid,'family':FAMILY[eid],'difficulty':str(q[':question/difficulty'][':db/ident']).split('/')[-1],'volume':str(V),'inverse':[str(e) for e in inv],'jacobian':str(J),'mathematics_validated':True,'complete_bank_checked':len(fields),'plots':'none','issues':issues,'count_eligible':not issues,'math_fingerprint':fingerprint(q)}
