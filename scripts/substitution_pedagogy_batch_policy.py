"""Delivery guard for the eight reviewed inverse-trig/exponential KPs."""
from collections import defaultdict
from fractions import Fraction
import re
KPS={17592186064218,17592186064219,17592186064250,17592186064220,17592186184349,17592186184350,17592186184351,17592186184352}
def validate_delivery_batch(records,kp_id):
 kp=int(kp_id)
 if kp not in KPS:return
 seen=set();groups=defaultdict(list)
 for record in records:
  q=record['question'];m=record.get('generation',{});band=str(q[':question/difficulty']).rsplit('/',1)[-1]
  if m.get('batch_contract')!='substitution-pedagogy-1':raise ValueError('Reviewed scaffolded substitution contract required')
  if band not in('easy','moderate','hard'):raise ValueError('Unsupported band')
  fields=q[':question/answer-fields'];problem=q[':question/problem'];sol=q[':question/worked-solution']
  if len(fields)!=1:raise ValueError('One assessed response required')
  f=fields[0];easy=band=='easy';choices=f[':answer-field/choices'];ref=f[':answer-field/correct'];cid=str(ref.get(':answer/id'))if isinstance(ref,dict)else str(ref[1]);key=next(a[':answer/value']for a in choices if str(a[':answer/id'])==cid)
  if easy:
   if f[':answer-field/type']!=':answer-field.type/radio'or len(choices)!=5 or not problem.startswith('Use the substitution $u='):raise ValueError('Easy must supply u and assess transformation')
   if any(r'\int'not in a[':answer/value']for a in choices):raise ValueError('Transformed-integral choices required')
  elif kp in(17592186064218,17592186064219,17592186064250):
   if f[':answer-field/type']!=':answer-field.type/radio'or len(choices)!=5 or 'You may use $'not in problem:raise ValueError('Inverse full calculations require the supported five-choice response and primitive')
  else:
   if f[':answer-field/type']!=':answer-field.type/blank'or len(choices)!=1 or 'You may use $'not in problem:raise ValueError('Full calculation needs supplied primitive and exact blank')
   if m['model']['lower']is None and '{{answer}} $+C$'not in problem:raise ValueError('Indefinite C must be external')
   if kp in(17592186064220,17592186184352)and m.get('provided_endpoint_values')and 'Endpoint values:'not in problem:raise ValueError('Required endpoint support absent')
  final=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)[-1].strip().rstrip('.')
  if final!=key+('+C'if not easy and m['model']['lower']is None and f[':answer-field/type']==':answer-field.type/blank'else ''):raise ValueError('Solution does not reach displayed key')
  if any(int(n)>25 for n in re.findall(r'\d+',problem)):raise ValueError('Rendered numbers exceed reviewed workload')
  p=m['parameters']
  families={17592186064218:{'sine'},17592186064219:{'tangent'},17592186064250:{'secant'},17592186064220:{'sine','tangent'},17592186184349:{'square','cube'},17592186184350:{'square','cube'},17592186184351:({'power_e','power_base'}if easy else {'log_composite'}if band=='hard'else {'sqrt_e','root_e','sqrt_base','root_base','log_e','log_base'}),17592186184352:({'square_e','linear_e'}if easy else {'log_e'}if band=='hard'else {'square_base','linear_base'})}
  if m.get('family')not in families[kp]:raise ValueError('Family not supported in this band')
  if kp in(17592186064218,17592186064219,17592186064220):
   a,b=int(p['A']),int(p['B'])
   if easy and not(a==1 and b>1)or band=='moderate'and not(a>1 and b==1):raise ValueError('Inverse band normalization mismatch')
   if band=='hard'and not(a>1 and (b==1 if kp==17592186064220 else b>1 and a!=b)):raise ValueError('Hard must add only its declared normalization/bound challenge')
  if kp==17592186064220 and not easy and ('Endpoint values:'not in problem or not m.get('provided_endpoint_values')):raise ValueError('Inverse endpoint facts required before feedback')
  if kp==17592186064250 and not easy:
   expected='absolute_value_normalization'if band=='hard'else'visible_linear_scaling'
   if m.get('challenge')!=expected:raise ValueError('Secant band challenge mismatch')
  if kp==17592186184352 and band=='hard'and 'Endpoint values:'not in problem:raise ValueError('Exponential endpoint facts required')
  if 'numerator'in p:
   if not 1<=Fraction(p['numerator'])<=4 or Fraction(p['numerator']).denominator!=1:raise ValueError('No fractional numerator composition')
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

  if band=="easy" and len(rows)>=8 and len({r["generation"].get("bank_correct_rank")for r in rows})<2:raise ValueError("A fixed numerical rank reveals the correct bank factor")
