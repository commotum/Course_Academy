"""Root actual both-base rewrites, full ordinary/reciprocal/product banks and stages."""
import sys,re,json,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent

def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','reader');x=p.x
count=dict(records=0,choices=0,whole_banks=0,base_identities=0,exponential_stages=0,linear_stages=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0,fieldless_originals=0,unrated_originals=0)
def read(t,var):
 t=re.sub(r'\\[A-Za-z]+|'+re.escape(var),lambda m:m[0] if m[0].startswith('\\') else 'x',t.strip().rstrip('.,').replace('&',''))
 return p.scalar(t)
def logs(a,b):return s.simplify(s.expand_log(s.log(a),force=True)-s.expand_log(s.log(b),force=True))
def root(l,r,exp):
 F=logs(l,r) if exp else s.expand(l-r);P=s.Poly(F,x);assert P.degree()==1;v=s.simplify(-P.coeff_monomial(1)/P.coeff_monomial(x));assert v.is_Rational and v!=0;return v

def check(rec):
 q=rec['question'];g=rec['generation'];parts=re.findall(r'\$([^$]+)\$',q[':question/problem']);var=next(z.strip() for z in parts if re.fullmatch(r'[xydbqmna](?:=)?',z.strip())).rstrip('=');math=next(z for z in parts if '=' in z and '^' in z).rstrip('.,');lhs,rhs=math.split('=');L,V=read(lhs,var),read(rhs,var);answer=root(L,V,True);sol=q.get(':question/worked-solution')
 # Base identities are explicit instructional inputs, even in changed source profiles.
 if sol:
  identities=re.findall(r'\$(\d+)=\{(\d+)\}\^\{(\d+)\}',sol);assert len(identities)>=2
  for value,base,power in identities:assert int(value)==int(base)**int(power);count['base_identities']+=1
  base=int(identities[0][1]);u=int(identities[0][2]);w=int(identities[1][2]);assert base==int(identities[1][1]) and u>=2 and w>=2 and u!=w
 else:
  # The only unrated originals have no solution; derive a primitive common base
  # from their printed numeric bases solely to check mathematical correctness.
  bases=[int(z) for z in re.findall(r'(\d+)\^\{',math)];assert len(bases)==2
  possibilities=[(B,U,W) for B in range(2,7) for U in range(2,6) for W in range(2,6) if B**U==bases[0] and B**W==bases[1]];assert possibilities;base,u,w=possibilities[0]
 product=r'\cdot' in lhs;reciprocal=r'\frac{1}' in rhs
 if product:
  assert sol and len(identities)==3;t=int(identities[2][2]);assert read(rhs,var)==base**t
  # Printed product's two original bases and exponents are complete component slots.
  factors=re.fullmatch(r'\{(\d+)\}\^\{(.*?)\}\\cdot \{(\d+)\}\^\{(.*?)\}',lhs);assert factors,lhs;B1,E1,B2,E2=factors.groups();assert int(B1)==base**u and int(B2)==base**w
  E=read(E1,var);F=read(E2,var)
 else:
  E=s.simplify(s.expand_log(s.log(L),force=True)/(u*s.log(base)));F=s.simplify(s.expand_log(s.log(V),force=True)/(w*s.log(base)))*(-1 if reciprocal else 1)
 a,h=s.expand(E).coeff(x),s.expand(E).subs(x,0);c,k=s.expand(F).coeff(x),s.expand(F).subs(x,0)
 assert all(z.is_Integer for z in (a,h,c,k)),(math,E,F)
 for field in q.get(':question/answer-fields',[]):
  vs=[read(z[':answer/value'],var) for z in field[':answer-field/choices']];assert len(vs)==5 and len(set(vs))==5 and sum(z==answer for z in vs)==1
  if ':answer-field/correct' in field:assert next(z[':answer/id'] for z,v in zip(field[':answer-field/choices'],vs) if v==answer)==field[':answer-field/correct'][1]
  if g['eligible_for_learning']:
   if product:
    D=u*a+w*c;expected=[answer,s.Rational(t-h-w*k,a+w*c),s.Rational(t-u*h-k,u*a+c),s.Rational(t-h-k,D),s.Rational(t-u*h+w*k,u*a-w*c)]
   elif reciprocal:
    D=u*a+w*c;N=-w*k-u*h;expected=[answer,s.Rational(w*k-u*h,u*a-w*c),s.Rational(-k-h,D),-answer,s.Rational(N,u*a-w*c)]
   else:
    D=u*a-w*c;N=w*k-u*h;expected=[answer,-answer,s.Rational(k-h,D),s.Rational(u*k-w*h,w*a-u*c),s.Rational(N,u*a+w*c)]
   assert set(vs)==set(expected),(math,vs,expected)
  count['choices']+=5;count['whole_banks']+=1
 if sol:
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==(4 if reciprocal else 3)
  for idx,block in enumerate(blocks):
   rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\')
   assert len(rows)==(2 if product and idx==1 else 3 if idx==len(blocks)-1 and q.get(':question/difficulty','').endswith('/easy') else 4 if idx==len(blocks)-1 else 1)
   for row in rows:
    l,r=row.replace('&','').split('=');exp=idx<len(blocks)-1;assert root(read(l,var),read(r,var),exp)==answer,(g['template'],idx,row)
    count['exponential_stages' if exp else 'linear_stages']+=1
 count['records']+=1
if __name__=='__main__':
 kp=17592186115219;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'g');source=json.load(open(D/'source.json'));assert source==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  lv=c.get('level',c.get('difficulty',c.get('assigned_level')));z=g.generate(lv,template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(z);q=z['question'];o=olds[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):
   assert (key in q)==(key in o)
   if key in o and key!=':question/answer-fields':assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  for f,of in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
   assert sorted(z[':answer/value'] for z in f[':answer-field/choices'])==sorted(z[':answer/value'] for z in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   if ':answer-field/correct' in of:
    val=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);assert val==of[':answer-field/correct'][':answer/value'];count['source_refs']+=1
   count['source_values']+=5
  count['source_prompts']+=1;count['source_solutions']+=int(':question/worked-solution' in o);count['fieldless_originals']+=int(':question/answer-fields' not in o);count['unrated_originals']+=int(':question/difficulty' not in o)
 for z in json.load(open(D/'review.json')):check(z.get('record',z))
 for lv in ('easy','moderate','hard'):
  for seed in range(20):check(g.generate(lv,seed=96000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(count,indent=2)+'\n');print(count)
