"""Root verifies full 3D source banks and source-shaped scalar-integral stages."""
import hashlib,importlib.util,json,re,sys
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;K=17592186179725;D=R.parents[2]/f'generate/scratch/{K}'
def mod(n,p):
 spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);sys.modules[n]=m;spec.loader.exec_module(m);return m
P=mod('root_3d_reader',R/'segment-readback.py');G=mod('root_3d_generator',D.with_suffix('.py'))
S=json.load(open(D/'source.json'));assert S==json.load(open(R/'refresh-2026-10-14/sources'/f'{K}.json'));O={q[':question/math-academy-id']:q for q in S['record'][':knowledge-point/questions']}
def prose_mask(t):
 z=P.mask(t).replace('from@MATH@','from @MATH@');return re.sub(r'(?:@MATH@\s+)+@MATH@','@MATH@',z)
Fid=dict(prompts=0,normalized_full_solutions=0,fields=0,values=0,refs=0,missing_refs=0,unrated=0)
for c in json.load(open(D/'source-cases.json')):
 o=O[c['source_id']];q=G.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile'])['question']
 for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (k in q)==(k in o)
 assert q[':question/problem']==o[':question/problem'];Fid['prompts']+=1;Fid['unrated']+=(':question/difficulty' not in o)
 if ':question/difficulty' in q:assert q[':question/difficulty']==o[':question/difficulty'][':db/ident']
 for nf,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
  assert nf[':answer-field/key']==of[':answer-field/key'] and nf[':answer-field/type']==of[':answer-field/type'][':db/ident']
  remaining=list(nf[':answer-field/choices']);assert len(remaining)==len(of[':answer-field/choices'])==5
  for a in of[':answer-field/choices']:
   matches=[i for i,b in enumerate(remaining) if P.integral_equal(a[':answer/value'],b[':answer/value'])];assert len(matches)==1,(c['source_id'],a)
   b=remaining.pop(matches[0]);assert b[':answer/type']==a[':answer/type'][':db/ident'];assert (':answer/feedback' in a)==(':answer/feedback' in b);Fid['values']+=1
  assert not remaining;Fid['fields']+=1;assert (':answer-field/correct' in nf)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert P.integral_equal(next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]),of[':answer-field/correct'][':answer/value']);Fid['refs']+=1
  else:Fid['missing_refs']+=1
 if ':question/worked-solution' in o:
  assert prose_mask(o[':question/worked-solution'])==prose_mask(q[':question/worked-solution'])
  # Preserve all source operative row counts; exact normalization checked below.
  a=P.blocks(o[':question/worked-solution']);b=P.blocks(q[':question/worked-solution']);assert len(a)==len(b)
  assert [len(P.rows(x)) for x in a[1:]]==[len(P.rows(x)) for x in b[1:]];Fid['normalized_full_solutions']+=1
C=dict(records=0,choice_values=0,bank_pairs=0,source_prose_masks=0,primitive_derivatives=0,endpoint_sides=0,signed_endpoint_components=0,substitution_bounds=0)
rows=json.load(open(R/f'qa/{K}-sampled.json'))
for c in json.load(open(D/'source-cases.json')):
 try:rows.append(G.generate(c['level'],template=c['template'],parameters=c['parameters']))
 except ValueError:pass

def primitive(z):
 z=z.replace(r'\left','').replace(r'\right','');co,body=z.split('[',1);body,tail=body.rsplit(']',1);assert tail=='_{0}^{1}'
 return P.scalar(co)*P.scalar(body),P.scalar(co),P.scalar(body)
for rec in rows:
 q,m=rec['question'],rec['generation'];f,A,B,r,dr,speed,h=P.objects(q[':question/problem'],3);t=P.t;expected=P.value(speed*s.Integral(h,(t,0,1)))
 F=q[':question/answer-fields'][0];vals=[P.value(a[':answer/value']) for a in F[':answer-field/choices']];assert len(vals)==5
 assert [a[':answer/id'] for a,v in zip(F[':answer-field/choices'],vals) if P.same(v,expected)]==[F[':answer-field/correct'][1]]
 for i,v in enumerate(vals):
  assert v.is_real is True and v.is_finite is True
  for w in vals[i+1:]:assert not P.same(v,w);C['bank_pairs']+=1
 family=m['template'];iv=s.simplify(expected/speed);n=speed**2;x,y,z=r
 if family in ('sum','quotient','radical'):
  wrong=[expected,iv,n*iv,s.sqrt(dr[0]**2+dr[1]**2)*iv,P.value(speed*s.Integral(f.subs({P.p.x:x,P.p.y:A[1],P.p.z:z},simultaneous=True),(t,0,1)))]
 elif family=='polynomial':wrong=[expected,iv,n*iv,P.value(speed*s.Integral(x*y,(t,0,1))),P.value(speed*s.Integral(A[0]*y*y,(t,0,1)))]
 elif family=='exponential':
  arg=next(iter(h.atoms(s.exp))).args[0];lo,hi=arg.subs(t,0),arg.subs(t,1);wrong=[expected,iv,speed*(s.exp(hi)+s.exp(lo)),speed*s.exp(hi),expected/dr[0]]
 else:
  arg=P.scalar(re.search(r'using the substitution \$u=(.*?)\$',q[':question/worked-solution'])[1]);alpha=s.diff(arg,t);wrong=[expected,iv,-expected,s.simplify(expected*alpha),expected/2]
 assert all(any(P.same(v,w) for w in vals) for v in wrong),(family,vals,wrong)
 sol=q[':question/worked-solution'];counts,bs,ri=P.stages(sol,f,A,B,r,dr,speed,h,3)
 for k,v in counts.items():C[k]=C.get(k,0)+v
 if family in ('sum','quotient','radical'):assert len(bs)==5 and len(ri)==3
 elif family=='polynomial':
  assert len(bs)==5 and len(ri)==6;pp,co,body=primitive(ri[3]);assert P.same(s.diff(pp,t),speed*h);C['primitive_derivatives']+=1
  groups=P.q.outer(ri[4]);assert len(groups)==2
  terms=s.Poly(body,t).terms();coeff=[c for (power,),c in terms]
  for raw,end in zip(groups,(1,0)):
   actual=P.q.outer(raw);assert len(actual)==len(terms)
   wanted=[c*s.Integer(end)**power for (power,),c in terms];unused=list(wanted)
   for v in actual:
    matches=[i for i,w in enumerate(unused) if P.same(P.scalar(v),w)];assert matches;unused.pop(matches[0]);C['signed_endpoint_components']+=1
  assert P.same(P.scalar(ri[4]),expected) and P.same(P.scalar(ri[5]),expected);C['endpoint_sides']+=2
 else:
  assert len(bs)==6 and len(ri)==3;er=P.rows(bs[5]);assert len(er)==5
  arg=P.scalar(re.search(r'using the substitution \$u=(.*?)\$',sol)[1]);lo,hi=arg.subs(t,0),arg.subs(t,1);u=P.p.u
  actual=P.complete(er[0]);integ=next(iter(actual.atoms(s.Integral)));assert integ.limits==((u,lo,hi),);assert P.same(P.value(actual),expected);C['substitution_bounds']+=2
  # Primitive display uses an evaluation bar; compare its actual coefficient/function.
  head=er[1].split(r'\,{|}')[0];head=head.replace(r'\,','');pp=P.scalar(head);assert P.same(s.diff(pp,u),actual/integ*integ.function);C['primitive_derivatives']+=1
  for row in er[2:]:assert P.same(P.scalar(row),expected);C['endpoint_sides']+=1
  if family=='exponential':
   exps=re.findall(r'\{e\}\^\{([^{}]+)\}',er[2]);assert len(exps)==2 and P.scalar(exps[0])==hi and P.scalar(exps[1])==lo;C['signed_endpoint_components']+=2
  else:
   groups=P.q.outer(er[3]);assert len(groups)==1;inner=P.q.outer(groups[0]);assert len(inner)==2
   v1=s.sin(hi) if family=='cosine' else -s.cos(hi);v0=s.sin(lo) if family=='cosine' else -s.cos(lo)
   assert P.same(P.scalar(inner[0]),v1) and P.same(P.scalar(inner[1]),v0);C['signed_endpoint_components']+=2
 sid=G.SOURCES[family]
 if ':question/worked-solution' in O[sid]:assert prose_mask(sol)==prose_mask(O[sid][':question/worked-solution']);C['source_prose_masks']+=1
 C['choice_values']+=5;C['records']+=1
out={'passed':True,'source_fidelity':Fid,'readback':C,'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'source_notation_normalized':True,'database_writes':0};(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
