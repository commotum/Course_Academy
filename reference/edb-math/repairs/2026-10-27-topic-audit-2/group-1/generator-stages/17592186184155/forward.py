"""Forward, source-bounded elementary integration questions for this lesson."""
import argparse,json,random,uuid,itertools
from fractions import Fraction as F
from integral_display import display_integral
from math_format import normalize_prose,normalize_tex,checked_math_content
from integration_batch_policy import validate_delivery_batch,clone_key,CONTRACT,FAMILIES,repeated_bank_shortcuts

VERSION='2.2.0-three-band-power-rule-errors-format-audit-9122-v1'
D=tuple(range(-6,0))+tuple(range(1,7))
IDS={17592186184153:'0db9b1c3-1e31-53f6-9fc2-1c611e2f9398',17592186184154:'a58c0a18-4221-50f1-b31c-ae58d099d79d',17592186184155:'007f3355-427a-5da4-8af7-22581f1cb1de'}
SOURCE_REFS={
 'polynomial-three':('q-2252','8f7dc381-ff4a-5ab2-9c80-1b180b43d77b',17592186233644),
 'expanded-square':('q-49173','b6c1d13e-58bd-57d8-918b-0a1bebf09fb1',17592186234106),
 'square-root-three':('q-2250','564c4689-85ae-5d46-8778-645d30c6800f',17592186184563),
 'root-cube-three':('e-373','8f99b603-2fba-5a58-9966-b91d3a8a773e',17592186184059),
 'positive-fractional-three':('q-113850','676d4494-4f46-573f-a890-2a8daa607201',17592186567046),
 'negative-fractional-three':('q-113848','e132caee-594d-5f81-b6a1-2e2a44a2d5f6',17592186250124),
}
def rat(n):
 n=F(n);return ('-'if n<0 else '')+(str(abs(n.numerator))if n.denominator==1 else rf'\frac{{{abs(n.numerator)}}}{{{n.denominator}}}')
def term(c,p,v,radical=True):
 c,p=abs(F(c)),F(p)
 if not p:return rat(c)
 n=abs(p.numerator);d=p.denominator;base=v if n==1 else rf'{v}^{{{n}}}'
 if d>1 and radical:base=rf'\sqrt{{{base}}}'if d==2 else rf'\sqrt[{d}]{{{base}}}'
 elif d>1:base=rf'{v}^{{{rat(abs(p))}}}'
 num=''if c.numerator==1 else str(c.numerator);den=''if c.denominator==1 else str(c.denominator)
 if p<0:den+=base;num=num or'1'
 else:num+=base
 return rf'\frac{{{num}}}{{{den}}}'if den else num
def tex(terms,v='x',radical=True):
 return ''.join(('-'if F(c)<0 else '+'if i else '')+term(c,p,v,radical)for i,(c,p)in enumerate(terms))
def primitive(ts):return [(F(c)/(F(p)+1),F(p)+1)for c,p in ts]
def serial(ts):return [[str(c),str(p)]for c,p in ts]
def draw(kp,family,rng):
 v=rng.choice(('x','y','t'));extra={};kind='radio'
 if family in ('constant-polynomial','derivative-blank','constant-reciprocal'):
  p=F(rng.choice((-F(3,2),-5)))if family=='constant-reciprocal'else F(rng.randint(2,6))
  ts=[(F(rng.choice(D)),F(0)),(F(rng.choice((-1,1))),p)];domains=[D,(-1,1)]
  if family=='derivative-blank':kind='blank';v='t'
 elif family=='quarter-power-blank':
  ts=[(F(rng.choice((-1,1))),F(1,4)),(F(rng.choice((-1,1))),F(rng.randint(2,6)))];domains=[(-1,1)]*2;kind='blank'
 elif family=='polynomial-pair':
  ps=rng.choice(((1,2),(1,3),(2,3)));domain=tuple(n for n in D if abs(n)>1);ts=[(F(rng.choice(domain)),F(p))for p in ps];domains=[domain]*2
 elif family=='radical-product':
  domain=(-4,-3,-2,-1,1,2,3,4);a,b=rng.choice(domain),rng.choice(domain);ts=[(F(a),F(3,2)),(F(b),F(1,2))];domains=[domain]*2
 elif family in ('power-quotient','direct-quotient-blank'):
  m,n=(rng.randint(2,4),rng.choice((2,3)))if family=='power-quotient'else(0,rng.choice((2,3)))
  ts=[(F(rng.choice(D)),F(m)),(F(rng.choice(D)),F(-n if m else -2))];domains=[D]*2;extra={'denominator':n}
  if family=='direct-quotient-blank':kind='blank'
 elif family=='easy-power-three':
  domains=[(-3,-2,-1,1,2,3)]*3;ts=[(F(rng.choice(dom)),F(p))for dom,p in zip(domains,(2,1,0))]
 elif family=='polynomial-three':
  domains=[D,D,(-3,-2,-1,F(-1,2),F(1,2),1,2,3)];ts=[(F(rng.choice(dom)),F(p))for dom,p in zip(domains,(2,1,0))]
 elif family in ('square-root-three','root-cube-three'):
  # Choose the source-supported rewrite case before coefficients and ordering.
  p=F(1,2) if family=='square-root-three' else F(3,2)
  domains=[D]*3;ts=[(F(rng.choice(D)),q)for q in (F(2),p,F(0))]
 elif family=='expanded-square':
  a=rng.randint(1,4);b=rng.choice(D);ts=[(F(a*a),F(0)),(F(2*a*b),F(2)),(F(b*b),F(4))];extra={'square_a':a,'square_b':b};domains=[]
 else:
  d=rng.choice((3,5,7));p=F(-(d+1),d)if family=='negative-fractional-three'else F(rng.randint(1,d-1),d)
  ts=[(F(rng.choice(D)),p),(F(rng.choice(D)),F(rng.randint(1,5))),(F(rng.choice(D)),F(-rng.randint(2,4)))];domains=[D]*3
 # Term order changes together in prompt, primitive, options and explanation.
 order=list(range(len(ts)));rng.shuffle(order)
 return ts,v,kind,domains,order,extra
def integrand(family,ts,v,order,extra):
 if family=='radical-product':return rf'\sqrt{{{v}}}\left('+tex([(ts[0][0],1),(ts[1][0],0)],v)+r'\right)'
 if family in ('power-quotient','direct-quotient-blank'):
  n=extra['denominator'];return r'\frac{'+tex([(c,p+n)for c,p in ts],v)+'}{'+v+'^{'+str(n)+'}}'
 if family=='expanded-square':return r'\left('+tex([(extra['square_a'],0),(extra['square_b'],2)],v)+r'\right)^{2}'
 if family=='root-cube-three':
  return tex([ts[j]for j in order],v).replace(rf'\sqrt{{{v}^{{3}}}}',rf'\left(\sqrt{{{v}}}\right)^{{3}}')
 return tex([ts[j]for j in order],v)
def power_error_pool(c,p):
 """Same-power alternatives from specific power-rule coefficient errors.

 Keep a correctly integrated term shared when no two-sided error pool exists
 (notably p=-2). This avoids a uniquely extreme correct coefficient.
 """
 c,p=F(c),F(p);q=p+1;sign=1 if c/q>0 else -1
 candidates={abs(c),abs(c)*abs(q),abs(c)/(q*q),F(1)/abs(q)}
 for divisor in (p,p+2):
  if divisor:candidates.add(abs(c/divisor))
 correct=abs(c/q);below={v for v in candidates if v<correct};above={v for v in candidates if v>correct}
 return sorted({c/q}|{sign*v for v in below|above}) if below and above else [c/q]
def coefficient_bank(ts,domains,family,rng):
 if family in ('easy-power-three','polynomial-three','expanded-square','square-root-three','root-cube-three','positive-fractional-three','negative-fractional-three'):
  answer=primitive(ts);pools=[power_error_pool(c,p) if p else [c] for c,p in ts]
  candidates=[]
  for coefficients in itertools.product(*pools):
   row=[(c,p+1)for c,(_,p)in zip(coefficients,ts)]
   if row!=answer:candidates.append(row)
  if len(candidates)<4:raise ValueError('Insufficient distinct plausible power-rule errors')
  return [answer]+rng.sample(candidates,4)

 # Start with the sampled integrand and its computed primitive. Other choices
 # change coefficients under the same powers. Conditional on the visible bank,
 # every sampled coefficient assignment is an eligible assessed instance.
 rows=[primitive(ts)];seen={tuple(c for c,p in rows[0])}
 if family in ('constant-polynomial','constant-reciprocal'):
  # The copied constant is common to every choice. Vary the integrated unit
  # power's divisor without a fixed coefficient rank, sign, or exponent cue.
  correct=rows[0][1][0];pool=sorted({F(n,d)for n in range(1,9)for d in range(1,13)}-{abs(correct)})
  rank=rng.randrange(5);below=[x for x in pool if x<abs(correct)];above=[x for x in pool if x>abs(correct)]
  wrong=rng.sample(below,rank)+rng.sample(above,4-rank)
  return rows+[[(rows[0][0]),(c*(1 if correct>0 else -1),rows[0][1][1])]for c in wrong]
 while len(rows)<5:
  if family=='expanded-square':
   a=int(abs(ts[0][0])**F(1,2));sign=1 if ts[1][0]>0 else -1;b=sign*rng.randint(1,6);coeffs=(a*a,2*a*b,b*b)
  else:coeffs=tuple(c if p==0 else rng.choice([v for v in dom if (v>0)==(c>0)])for dom,(c,p)in zip(domains,ts))
  candidate=[(F(c)/(p+1),p+1)for c,(_,p)in zip(coeffs,ts)];key=tuple(c for c,p in candidate)
  if key not in seen:rows.append(candidate);seen.add(key)
 return rows
@checked_math_content
def build(kp,family,ts,v,kind,domains,order,extra,rng,seed):
 original=integrand(family,ts,v,order,extra);presented=[ts[j]for j in order];answer=primitive(ts)
 positive=any(p.denominator%2==0 for c,p in ts);nonzero=any(p<0 for c,p in ts)
 domain=f' Assume ${v}>0$.'if positive else f' Assume ${v}\\ne0$.'if nonzero else''
 if kind=='blank':
  prompt='Find the antiderivative:\n\n$\\displaystyle\\int '+original+rf'\,\mathrm{{d}}{v}=$'+'\n{{field-1}}\n$+C$.'+domain
 else:prompt='Calculate $\\displaystyle\\int '+original+rf'\,\mathrm{{d}}{v}$.'+domain
 lines=[rf'\int {original}\,\mathrm{{d}}{v}',rf'\int\left({tex(presented,v,False)}\right)\,\mathrm{{d}}{v}']
 pieces=''.join(('-'if c<0 else '+'if i else '')+(''if abs(c)==1 else rat(abs(c)))+rf'\int {v}^{{{rat(p)}}}\,\mathrm{{d}}{v}'for i,(c,p)in enumerate(presented))
 lines.extend([pieces,tex([answer[j]for j in order],v)+'+C'])
 applied=''.join(('-'if c<0 else '+'if i else '')+(''if abs(c)==1 else rat(abs(c)))+rf'\left(\frac{{{v}^{{{rat(p+1)}}}}}{{{rat(p+1)}}}\right)'for i,(c,p)in enumerate(presented))+'+C'
 lines.insert(-1,applied)
 worked='Rewrite as powers, apply the sum and constant factor rules, and integrate each term using $\\int '+v+'^p\\,\\mathrm{d}'+v+'='+v+'^{p+1}/(p+1)+C$ for $p\\ne-1$:\n\n$$\n'+r'\begin{aligned}& '+r'\\ &= '.join(lines)+r'\end{aligned}'+'\n$$'
 if kind=='blank':worked+='\n\nThe constant $C$ is already supplied outside the blank.'
 banks=[answer]if kind=='blank'else coefficient_bank(ts,domains,family,rng);rng.shuffle(banks)
 values=[tex([row[j]for j in order],v)+(''if kind=='blank'else'+C')for row in banks];correct=tex([answer[j]for j in order],v)+(''if kind=='blank'else'+C');key=values.index(correct)
 prompt,worked=map(normalize_prose,(prompt,worked));values=list(map(normalize_tex,values))
 prompt=display_integral(prompt)
 qid=uuid.uuid5(uuid.UUID(IDS[kp]),json.dumps([VERSION,prompt,sorted(values),values[key]],ensure_ascii=False));fieldkey='field-1'if kind=='blank'else'selection';fid=uuid.uuid5(qid,fieldkey)
 choices=[{':answer/id':str(uuid.uuid5(fid,val)),':answer/type':':answer.type/math',':answer/value':val}for val in values]
 band=next(b for (k,b),fs in FAMILIES.items()if k==kp and family in fs)
 return {'knowledge_point':{'db_id':kp,'id':IDS[kp]},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+band,':question/problem':prompt,':question/worked-solution':worked,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':fieldkey,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[key][':answer/id']]}]},'generation':{'version':VERSION,'batch_contract':CONTRACT,'family':family,'input_terms':serial(ts),'variable':v,'order':order,'extra':extra,'bank_terms':[serial(row)for row in banks],'seed':seed,'source_refs':([dict(zip(('math_academy_id','question_id','db_id'),SOURCE_REFS[family]))]if family in SOURCE_REFS else[]),'authored_answer_bank':'Power-rule errors for this KP: copied coefficient, multiplied rather than divided by new exponent, divided twice, used old exponent or incremented twice, or dropped input coefficient. Terms without a two-sided error pool are shared. Legacy sibling families: same powers and signs, with copied constants shared. Unit-power questions vary the true coefficient rank among same-sign alternatives; other coefficient assignments come from the eligible input domain. Captured source banks replay separately.'}}
def sample(kp,count,seed,difficulty):
 if difficulty=='unclassified':difficulty='hard'if kp==17592186184155 else'moderate'
 families=sorted(FAMILIES.get((kp,difficulty),[]))
 if not families:raise ValueError('Unsupported difficulty for this knowledge point')
 if not 0<=count<=1000:raise ValueError('count must be in 0..1000')
 rng=random.Random(seed);rows=[];seen=set();cycle=[]
 while len(rows)<count:
  if not cycle:cycle=rng.sample(families,len(families))
  family=cycle[-1]
  for attempt in range(10000):
   ts,v,kind,domains,order,extra=draw(kp,family,rng);r=build(kp,family,ts,v,kind,domains,order,extra,rng,seed);key=clone_key(r)
   if key in {clone_key(old)for old in rows[-4:]}:continue
   if kp==17592186184155 and repeated_bank_shortcuts(rows+[r]):continue
   signature=r['question'][':question/problem']
   if signature in seen:continue
   rows.append(r);seen.add(signature);cycle.pop();break
  else:raise ValueError('Requested count exceeds the unique source-bounded family')
 validate_delivery_batch(rows,kp);return rows
def replay_sources(kp):
 """Keep captured banks separate from the authored same-power practice bank."""
 from pathlib import Path
 cases=json.loads(Path(__file__).with_name('source-cases.json').read_text());rows=[]
 for source in cases:
  fields=source.get(':question/answer-fields',[])
  if not fields or not all(f.get(':answer-field/correct')for f in fields):continue
  q=json.loads(json.dumps(source));qid=uuid.uuid5(uuid.UUID(IDS[kp]),'source-replay:'+source[':question/id']);q[':question/id']=str(qid);q.pop(':db/id',None);q.pop(':question/math-academy-id',None)
  fs=[]
  for field in fields:
   key=field[':answer-field/key'];fid=uuid.uuid5(qid,key);cs=[{':answer/id':str(uuid.uuid5(fid,a[':answer/value'])),':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']}for a in field[':answer-field/choices']];correct=next(c[':answer/id']for c in cs if c[':answer/value']==field[':answer-field/correct'][':answer/value']);fs.append({':answer-field/id':str(fid),':answer-field/key':key,':answer-field/type':field[':answer-field/type'][':db/ident'],':answer-field/choices':cs,':answer-field/correct':[':answer/id',correct]})
  q[':question/answer-fields']=fs
  if isinstance(q.get(':question/difficulty'),dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
  rows.append({'knowledge_point':{'db_id':kp,'id':IDS[kp]},'question':q,'generation':{'profile':'source-replay','source_id':source[':question/id'],'source_math_academy_id':source[':question/math-academy-id'],'eligible_for_learning':False}})
 return rows
def main(kp):
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',default='unclassified');parser.add_argument('--count',type=int,default=5);parser.add_argument('--seed',type=int,default=0);parser.add_argument('--format',choices=['json'],default='json');parser.add_argument('--replay-source',action='store_true');args=parser.parse_args()
 try:rows=replay_sources(kp)if args.replay_source else sample(kp,args.count,args.seed,args.difficulty)
 except ValueError as e:parser.error(str(e))
 print(json.dumps(rows,ensure_ascii=False))
