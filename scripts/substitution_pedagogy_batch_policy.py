"""Delivery guard for the eight reviewed inverse-trig/exponential KPs."""
from collections import defaultdict
from fractions import Fraction
import re
KPS={17592186064218,17592186064219,17592186064250,17592186064220,17592186184349,17592186184350,17592186184351,17592186184352}
def validate_delivery_batch(records,kp_id):
 kp=int(kp_id)
 if kp not in KPS:return
 if kp in(17592186064218,17592186064219,17592186064220,17592186064250):
  from scripts.inverse_substitution_batch_policy import validate_delivery_batch as inverse_policy
  return inverse_policy(records,kp)
 seen=set();groups=defaultdict(list)
 for record in records:
  q=record['question'];m=record.get('generation',{});band=str(q[':question/difficulty']).rsplit('/',1)[-1]
  if m.get('batch_contract')!='substitution-recognition-3':raise ValueError('Reviewed scaffolded substitution contract required')
  if band not in('easy','moderate','hard'):raise ValueError('Unsupported band')
  fields=q[':question/answer-fields'];problem=q[':question/problem'];sol=q[':question/worked-solution']
  from scripts.integration_support_policy import validate_prerequisite_recall
  validate_prerequisite_recall(record)
  if len(fields)!=1:raise ValueError('One assessed response required')
  f=fields[0];easy=band=='easy';choices=f[':answer-field/choices'];ref=f[':answer-field/correct'];cid=str(ref.get(':answer/id'))if isinstance(ref,dict)else str(ref[1]);key=next(a[':answer/value']for a in choices if str(a[':answer/id'])==cid)
  if m.get('provided_substitution')or m.get('operation')!='evaluate'or 'Use the substitution' in problem:raise ValueError('Practice must retain substitution recognition')
  if easy:
   if f[':answer-field/type']!=':answer-field.type/radio'or len(choices)!=5 :raise ValueError('Easy requires complete-answer choices')
   if any(r'\int'in a[':answer/value']for a in choices):raise ValueError('Complete-answer choices required')
  elif kp in(17592186064218,17592186064219,17592186064250):
   if f[':answer-field/type']!=':answer-field.type/radio'or len(choices)!=5 :raise ValueError('Inverse full calculations require the supported five-choice response ')
  else:
   if f[':answer-field/type']!=':answer-field.type/blank'or len(choices)!=1 :raise ValueError('Full calculation needs an exact blank')
   if m['model']['lower']is None and '{{answer}} $+C$'not in problem:raise ValueError('Indefinite C must be external')
  final=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)[-1].strip().rstrip('.')
  if final!=key+('+C'if m['model']['lower']is None and f[':answer-field/type']==':answer-field.type/blank'else ''):raise ValueError('Solution does not reach displayed key')
  if any(int(n)>25 for n in re.findall(r'\d+',problem)):raise ValueError('Rendered numbers exceed reviewed workload')
  p=m['parameters']
  families={17592186064218:{'sine'},17592186064219:{'tangent'},17592186064250:{'secant'},17592186064220:{'sine','tangent'},17592186184349:{'square','cube'},17592186184350:{'square','cube'},17592186184351:({'power_e','power_base'}if easy else {'log_composite'}if band=='hard'else {'sqrt_e','root_e','sqrt_base','root_base','log_e','log_base'}),17592186184352:({'square_e','linear_e'}if easy else {'log_e'}if band=='hard'else {'square_base','linear_base'})}
  if m.get('family')not in families[kp]:raise ValueError('Family not supported in this band')
  if kp in(17592186064218,17592186064219,17592186064220):
   a,b=int(p['A']),int(p['B'])
   if easy and not(a==1 and b>1)or band=='moderate'and not(a>1 and b==1):raise ValueError('Inverse band normalization mismatch')
   if band=='hard'and not(a>1 and (b==1 if kp==17592186064220 else b>1 and a!=b)):raise ValueError('Hard must add only its declared normalization/bound challenge')
  if kp==17592186064250 and not easy:
   expected='absolute_value_normalization'if band=='hard'else'visible_linear_scaling'
   if m.get('challenge')!=expected:raise ValueError('Secant band challenge mismatch')
  if kp==17592186064250:
   factor=Fraction(m['model']['factor'])
   if easy and factor.denominator!=1 or band=='moderate'and factor.denominator==1:raise ValueError('Secant easy must match the derivative; moderate requires a fractional adjustment')
  if 'numerator'in p:
   if not 1<=Fraction(p['numerator'])<=(12 if kp==17592186064250 and easy else 4) or Fraction(p['numerator']).denominator!=1:raise ValueError('No fractional numerator composition')
   if int(p['A'])not in(1,4,9,16,25)or int(p['B'])not in(1,4,9,16,25):raise ValueError('Only small perfect-square inverse coefficients')
  if 'amplitude'in p and not 1<=int(p['amplitude'])<=4:raise ValueError('Small integer amplitudes required')
  if kp in(17592186184349,17592186184350):
   if int(p['power'])not in(2,3)or abs(int(p['slope']))not in(1,2)or(int(p['slope'])<0)!=(band=='hard'):raise ValueError('Only hard adds negative inner derivative')
  identity=(band,m['mathematical_fingerprint'])
  if identity in seen:raise ValueError('Duplicate task in delivered batch')
  seen.add(identity);groups[band].append(record)
 for band,rows in groups.items():
  # Scalars may vary within a family, but a full pool must exercise several substitutions.
  if len(rows)>=8 and len({r['generation']['model']['substitution']for r in rows})<3:raise ValueError('Delivered pool overconcentrates one substitution')

  if band=='easy' and len(rows)>=8:
   profiles={tuple(sorted(r['generation']['bank_recipes']))for r in rows}
   if len(profiles)<2:raise ValueError('Fixed answer-bank profiles reveal the answer')
