"""Publication checks for the three repaired sum-rule generators.

This contract concerns the actual surviving batch, including after deduplication.
It complements source review and independent algebra/grader verification.
"""
from fractions import Fraction as F
from collections import Counter

KPS={17592186184153,17592186184154,17592186184155}
CONTRACT='integration-forward-v2'
FAMILIES={
 (17592186184153,'moderate'):{'constant-polynomial','constant-reciprocal','derivative-blank'},
 (17592186184153,'hard'):{'quarter-power-blank'},
 (17592186184154,'easy'):{'polynomial-pair'},
 (17592186184154,'moderate'):{'radical-product','power-quotient','direct-quotient-blank'},
 (17592186184155,'easy'):{'easy-power-three'},
 (17592186184155,'moderate'):{'polynomial-three','expanded-square','square-root-three','root-cube-three'},
 (17592186184155,'hard'):{'positive-fractional-three','negative-fractional-three'},
}
def clone_key(record):
 m=record['generation'];return m['family'],tuple(sorted((str(abs(F(c))),str(F(p)))for c,p in m['input_terms']))
def validate_delivery_batch(records,kp_id):
 if int(kp_id)==17592186184154 and records and records[0].get('generation',{}).get('batch_contract')=='sum-factor-kp2-v3':
  from scripts.kp2_integration_policy import validate_delivery_batch as validate_kp2
  return validate_kp2(records,kp_id)
 if int(kp_id)==17592186184153 and records and records[0].get('generation',{}).get('batch_contract')=='sum-rule-kp1-v3':
  return validate_kp1_v3(records,kp_id)
 if int(kp_id)not in KPS or not records:return
 groups={}
 for r in records:
  q=r['question'];m=r.get('generation',{})
  if m.get('batch_contract')!=CONTRACT:raise ValueError('Integration generator requires the reviewed forward-generation batch contract')
  difficulty=str(q[':question/difficulty']).rsplit('/',1)[-1];allowed=FAMILIES.get((int(kp_id),difficulty),set())
  if m['family']not in allowed:raise ValueError('Unsupported integration family or difficulty')
  terms=[(F(c),F(p))for c,p in m['input_terms']]
  if len(terms)!=(3 if int(kp_id)==17592186184155 else 2)or any(not c or p==-1 for c,p in terms):raise ValueError('Integration scope requires nonzero elementary power terms')
  powers=sorted(p for c,p in terms)
  if int(kp_id)==17592186184153:
   if difficulty=='hard':valid=powers[0]==F(1,4)and powers[1]in range(2,7)and all(abs(c)==1 for c,p in terms)
   else:valid=sum(p==0 for c,p in terms)==1 and all((abs(c)<=6 if p==0 else abs(c)==1 and p in (*range(2,7),F(-3,2),F(-5)))for c,p in terms)
  elif int(kp_id)==17592186184154:
   if difficulty=='easy':valid=len(set(powers))==2 and all(p in (1,2,3)and 2<=abs(c)<=6 for c,p in terms)
   elif m['family']=='radical-product':valid=powers==[F(1,2),F(3,2)]and all(abs(c)<=4 for c,p in terms)
   elif m['family']=='power-quotient':valid=powers[0]in(-3,-2)and powers[1]in(2,3,4)and all(abs(c)<=6 for c,p in terms)
   else:valid=powers==[-2,0]and all(abs(c)<=6 for c,p in terms)
  elif difficulty=='easy':
   valid=powers==[0,1,2] and all(c.denominator==1 and abs(c)<=3 for c,p in terms)
  elif difficulty=='moderate':
   profiles={'expanded-square':[0,2,4],'polynomial-three':[0,1,2],
             'square-root-three':[0,F(1,2),2],'root-cube-three':[0,F(3,2),2]}
   valid=powers==profiles[m['family']]
   if m['family'] in ('square-root-three','root-cube-three'):
    valid=valid and all(c.denominator==1 and abs(c)<=6 for c,p in terms)
  else:
   fractional=[p for c,p in terms if p.denominator>1];valid=len(fractional)==1 and fractional[0].denominator in(3,5,7)and (0<fractional[0]<1 if m['family']=='positive-fractional-three'else fractional[0]==F(-(fractional[0].denominator+1),fractional[0].denominator))and sum(p.denominator==1 and 1<=p<=5 for c,p in terms)==1 and sum(p in(-4,-3,-2)for c,p in terms)==1 and all(abs(c)<=6 for c,p in terms)
  if not valid:raise ValueError('Integration question crosses its source-bounded KP or difficulty')
  field=q[':question/answer-fields'][0];kind=str(field[':answer-field/type']).rsplit('/',1)[-1]
  if kind=='radio':
   expected=sorted(p+1 for c,p in terms);banks=m['bank_terms']
   if len(banks)!=5 or any(sorted(F(p)for c,p in row)!=expected for row in banks):raise ValueError('All integration options must carry the same power pattern')
   expected_signs=[1 if c/(p+1)>0 else -1 for c,p in terms]
   if any([1 if F(c)>0 else -1 for c,p in row]!=expected_signs for row in banks):raise ValueError('All integration options must share the correct sign pattern')
   for j,(c,p)in enumerate(terms):
    if p==0 and any(F(row[j][0])!=c for row in banks):raise ValueError('Copied constants must not identify a unique answer')
   correct=field[':answer-field/correct'];aid=str(correct.get(':answer/id'))if isinstance(correct,dict)else str(correct[1]);values=field[':answer-field/choices']
   if len(values)!=5 or aid not in {str(a[':answer/id'])for a in values}:raise ValueError('Invalid integration answer bank')
   if '{{'in q[':question/problem']:raise ValueError('Radio integration prompts must not contain blank markers')
  groups.setdefault(difficulty,[]).append(r)
 for difficulty,rows in groups.items():
  for end in range(len(rows)):
   recent=rows[max(0,end-4):end+1]
   if len({clone_key(r)for r in recent})!=len(recent):raise ValueError('Repeated integration structure or sign-only clone in the delivered batch')
  need=min(len(FAMILIES[(int(kp_id),difficulty)]),len(rows))
  if len({r['generation']['family']for r in rows})<need:raise ValueError('Delivered integration batch lost required family coverage')
  # Same powers deliberately tie every min/max-degree strategy in every radio.
  # Coverage is required in the real saved batch, not merely a large test sample.

KP1_V3_FAMILIES={(17592186184153,'easy'):{'constant-polynomial'},(17592186184153,'moderate'):{'constant-radical','constant-reciprocal'},(17592186184153,'hard'):{'quarter-power-blank','mixed-powers-blank'}}
def validate_kp1_v3(records,kp_id):
 if int(kp_id)not in KPS or not records:return
 groups={}
 for r in records:
  q=r['question'];m=r.get('generation',{})
  if m.get('batch_contract')!='sum-rule-kp1-v3':raise ValueError('Integration generator requires the reviewed forward-generation batch contract')
  difficulty=str(q[':question/difficulty']).rsplit('/',1)[-1];allowed=KP1_V3_FAMILIES.get((int(kp_id),difficulty),set())
  if m['family']not in allowed:raise ValueError('Unsupported integration family or difficulty')
  terms=[(F(c),F(p))for c,p in m['input_terms']]
  if len(terms)!=(3 if int(kp_id)==17592186184155 else 2)or any(not c or p==-1 for c,p in terms):raise ValueError('Integration scope requires nonzero elementary power terms')
  powers=sorted(p for c,p in terms)
  if int(kp_id)==17592186184153:
   if difficulty=='hard':valid=(powers[0]==F(1,4)and powers[1]in range(2,7) if m['family']=='quarter-power-blank' else powers[0]in(F(-3,2),F(-5,2))and powers[1]in(F(1,4),F(1,2),F(5,2)))and all(abs(c)==1 for c,p in terms)
   else:valid=sum(p==0 for c,p in terms)==1 and all((abs(c)<=6 if p==0 else abs(c)==1 and p in (*range(1,7),F(1,2),F(3,2),F(-3,2),F(-2),F(-3),F(-4),F(-5)))for c,p in terms)
  elif int(kp_id)==17592186184154:
   if difficulty=='easy':valid=len(set(powers))==2 and all(p in (1,2,3)and 2<=abs(c)<=6 for c,p in terms)
   elif m['family']=='radical-product':valid=powers==[F(1,2),F(3,2)]and all(abs(c)<=4 for c,p in terms)
   elif m['family']=='power-quotient':valid=powers[0]in(-3,-2)and powers[1]in(2,3,4)and all(abs(c)<=6 for c,p in terms)
   else:valid=powers==[-2,0]and all(abs(c)<=6 for c,p in terms)
  elif difficulty=='moderate':valid=powers==([0,2,4]if m['family']=='expanded-square'else[0,1,2])
  else:
   fractional=[p for c,p in terms if p.denominator>1];valid=len(fractional)==1 and fractional[0].denominator in(3,5,7)and (0<fractional[0]<1 if m['family']=='positive-fractional-three'else fractional[0]==F(-(fractional[0].denominator+1),fractional[0].denominator))and sum(p.denominator==1 and 1<=p<=5 for c,p in terms)==1 and sum(p in(-4,-3,-2)for c,p in terms)==1 and all(abs(c)<=6 for c,p in terms)
  if not valid:raise ValueError('Integration question crosses its source-bounded KP or difficulty')
  field=q[':question/answer-fields'][0];kind=str(field[':answer-field/type']).rsplit('/',1)[-1]
  if kind=='radio':
   expected=sorted(p+1 for c,p in terms);banks=m['bank_terms']
   if len(banks)!=5 or any(sorted(F(p)for c,p in row)!=expected for row in banks):raise ValueError('All integration options must carry the same power pattern')
   expected_signs=[1 if c/(p+1)>0 else -1 for c,p in terms]
   if any([1 if F(c)>0 else -1 for c,p in row]!=expected_signs for row in banks):raise ValueError('All integration options must share the correct sign pattern')
   for j,(c,p)in enumerate(terms):
    if p==0 and any(F(row[j][0])!=c for row in banks):raise ValueError('Copied constants must not identify a unique answer')
   correct=field[':answer-field/correct'];aid=str(correct.get(':answer/id'))if isinstance(correct,dict)else str(correct[1]);values=field[':answer-field/choices']
   if len(values)!=5 or aid not in {str(a[':answer/id'])for a in values}:raise ValueError('Invalid integration answer bank')
   if '{{'in q[':question/problem']:raise ValueError('Radio integration prompts must not contain blank markers')
  groups.setdefault(difficulty,[]).append(r)
 for difficulty,rows in groups.items():
  for end in range(len(rows)):
   recent=rows[max(0,end-4):end+1]
   if len({clone_key(r)for r in recent})!=len(recent):raise ValueError('Repeated integration structure or sign-only clone in the delivered batch')
  need=min(len(KP1_V3_FAMILIES[(int(kp_id),difficulty)]),len(rows))
  if len({r['generation']['family']for r in rows})<need:raise ValueError('Delivered integration batch lost required family coverage')
  # Same powers deliberately tie every min/max-degree strategy in every radio.
  # Coverage is required in the real saved batch, not merely a large test sample.
