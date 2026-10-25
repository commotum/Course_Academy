"""Validation for KP 17592186184154's complete two-term linearity progression."""
from fractions import Fraction as F
CONTRACT='sum-factor-kp2-v3'
FAMILIES={'easy':{'polynomial-pair','linear-constant','reciprocal-pair'},'moderate':{'radical-product','power-quotient'},'hard':{'radical-quotient'}}
def clone_key(r):
 m=r['generation'];return m['family'],tuple(sorted((str(abs(F(c))),str(F(p)))for c,p in m['input_terms']))
def validate_delivery_batch(records,kp_id):
 if int(kp_id)!=17592186184154:return
 groups={}
 for r in records:
  q=r['question'];m=r.get('generation',{});band=str(q[':question/difficulty']).rsplit('/',1)[-1];family=m.get('family')
  if m.get('batch_contract')!=CONTRACT or family not in FAMILIES.get(band,set()):raise ValueError('Unsupported sum/constant-factor progression')
  ts=[(F(c),F(p))for c,p in m['input_terms']];ps=[p for c,p in ts]
  if len(ts)!=2 or any(c.denominator!=1 or not 1<=abs(c)<=6 or p==-1 for c,p in ts):raise ValueError('Expected two small signed power terms')
  valid={'polynomial-pair':tuple(ps)in((1,2),(1,3),(2,3)),'linear-constant':ps==[1,0],'reciprocal-pair':ps[0]in(1,2)and ps[1]in(-2,-3),'radical-product':ps==[F(3,2),F(1,2)],'power-quotient':ps[0]in(2,3,4)and ps[1]in(-2,-3),'radical-quotient':ps[0]in(F(3,2),F(5,2))and ps[1]==F(-1,2)}[family]
  if not valid:raise ValueError('Power pattern outside reviewed progression')
  f=q[':question/answer-fields'][0];kind=f[':answer-field/type'].rsplit('/',1)[-1]
  if kind!=('blank'if band=='hard'else'radio'):raise ValueError('Response support outside reviewed progression')
  if len(f[':answer-field/choices'])!=(1 if kind=='blank'else 5):raise ValueError('Incomplete answer bank')
  groups.setdefault(band,[]).append(r)
 for band,rows in groups.items():
  for i in range(len(rows)):
   recent=rows[max(0,i-4):i+1]
   if len({clone_key(r)for r in recent})!=len(recent):raise ValueError('Repeated sign-only structure')
  if len({r['generation']['family']for r in rows})<min(len(rows),len(FAMILIES[band])):raise ValueError('Lost supported family coverage')
