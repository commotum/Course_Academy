#!/usr/bin/env python3
"""Indefinite natural-log substitutions, frozen basis2275. No database writes.
Each observed source bank is a complete separately selected profile. Real
connected domains: log argument >0; nonzero log for negative powers and logAbs;
positive log for half powers. No forced logarithmic identities are used.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,importlib.util,json,random,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
spec=importlib.util.spec_from_file_location('kp00816_math_format',HERE/'math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
KP=17592186100816;VERSION='natural-log-substitution-b2275-v1'
SOURCE=json.loads((HERE/'source.json').read_text());REC=SOURCE['record'];QS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
x,u,C=s.symbols('x u C',real=True)
# level, coefficient kind, original coefficient parameter, inner scale, inner
# exponent, outer log exponent. One original-source ID per observed profile.
CONFIG={
'q-13802':('hard','integer',2,2,1,-1),
'q-13814':('moderate','integer',5,3,1,-2),
'q-2202':('easy','integer',4,1,1,1),
'q-13803':('easy','inverse',2,1,1,1),
'q-13807':('moderate','inverse',3,1,2,1),
'q-13808':('hard','integer',5,1,2,-1),
'q-13809':('easy','inverse',4,1,1,2),
'q-210742':('moderate','integer',6,1,3,1),
'q-210746':('hard','integer',2,4,1,-1),
'q-2380':('moderate','integer',1,1,1,s.Rational(-1,2)),
'q-31398':('moderate','inverse',3,1,1,s.Rational(1,2)),
'q-210743':('moderate','integer',9,3,1,s.Rational(1,2)),
'q-2194':('hard','radical',2,1,1,-1),
'q-210748':('hard','radical',3,1,2,-1),
'q-13822':('hard','inverse',3,3,1,-1),
}
def original(sid):
 _,_,k,a,n,p=CONFIG[sid];return dict(k=k,a=a,n=n,p_num=int(s.numer(p)),p_den=int(s.denom(p)))
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(z):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+str(z)))
def tex(z):return fmt.normalize_tex(s.latex(z,fold_short_frac=False).replace(r'\log',r'\ln'))
def equivalent(a,b):return s.cancel(a-b)==0

def parameters(sid,p):
 if set(p)!={'k','a','n','p_num','p_den'}or any(type(v)is not int for v in p.values()):raise ValueError('builtin integer slots required')
 k,a,n,nn,dd=(p[t]for t in('k','a','n','p_num','p_den'));level,kind,_,a0,n0,p0=CONFIG[sid]
 if not(1<=k<=12 and 1<=a<=6 and 1<=n<=4 and dd in(1,2)):raise ValueError('bounded parameter domain')
 power=s.Rational(nn,dd)
 if level=='easy':
  if a!=1 or n!=1 or power not in(1,2,3):raise ValueError('easy plain ln and positive integer powers1..3')
 else:
  if power!=p0:raise ValueError('fixed outer role for each moderate/hard family')
  if (a0==1 and a!=1)or(a0!=1 and not 2<=a<=6):raise ValueError('preserve plain/power/scaled logarithm role')
  if (n0==1 and n!=1)or(n0!=1 and n not in(2,3,4)):raise ValueError('preserve linear versus power inner role')
 if kind=='radical'and k not in(2,3,5,6,7,10,11):raise ValueError('nonsquare radical coefficient')
 coeff=s.sqrt(k)if kind=='radical'else s.Rational(1,k)if kind=='inverse'else s.Integer(k)
 return coeff,s.Integer(a),s.Integer(n),power

def bank(sid,c,a,n,p,L):
 """Every row corresponds in source order to the full original bank.
 Expressions deliberately retain compound wrong-function recipes, with no
 inferred misconception labels or pooled first-valid construction.
 """
 r=c/(n*(p+1))if p!=-1 else c/n;B=s.log(s.Abs(L));K=s.log(s.Abs(s.log(x)));LP=lambda j:L**j
 if sid=='q-13802':return [K+C,c*K+C,B+C,c*B,c*B+C]
 if sid=='q-13814':return[-a*c/L**3,c/L**2+C,-c/L+C,a*c/L+C,-1/L+C]
 if sid=='q-2202':return[r*L**(p+1)+C,r*L**(p+1)/2+C,-r*L**(p+1)/2+C,r*L**(p+1)/4+C,r*L**p+C]
 if sid=='q-13803':return[c*L**(p+1)+C,r*L**p+C,L**(p+1)+C,c*L**p+C,r*L**(p+1)+C]
 if sid=='q-13807':return[c*L**2/n+C,r*s.log(s.Abs(x))**2+C,r*L**2+C,L**2/n+C,r*L+C]
 if sid=='q-13808':return[B/n+C,x*B/n+C,c*B+C,r*B+C,r*x*B+C]
 if sid=='q-13809':return[r*L**p+C,r*L**(p+1)+C,c*L**p+C,L**(p+1)/(p+1)+C,c*L**(p+1)+C]
 if sid=='q-210742':return[L**2/2+C,L**2/n+C,c*L**3/n+C,r*L**2+C,c*s.log(x**(n-1))**3/2+C]
 if sid=='q-210746':
  H=s.log(s.Abs(s.log(a*x/2)));return[H/a+C,c*B+C,H+C,a*K+C,B/c+C]
 if sid=='q-2380':return[2*c*s.sqrt(L)+C,c*L/x+C,c/s.log(L)+C,c*L+C,c*s.sqrt(s.log(L))/x+C]
 if sid=='q-31398':return[c*L**2/3+C,r*s.sqrt(L**3)+C,r*s.sqrt(L)+C,r*L**3+C,s.sqrt(L**3)/r+C]
 if sid=='q-210743':return[r*s.sqrt(s.log(a*a*x))+C,r*s.sqrt(s.log(a*x*x)**2)+C,s.sqrt(s.log(a*a*x)**3)+C,r*s.sqrt(L**3)+C,s.sqrt(L)/r+C]
 if sid=='q-2194':return[1/B+C,B+C,x*s.log(s.log(c))+C,c*B+C,c/B+C]
 if sid=='q-210748':return[c**2*B/n+C,n*s.log(s.Abs(c*s.log(x)))+C,B/n+C,r*B+C,c*K+C]
 if sid=='q-13822':return[c*K+C,a*B/2+C,L+C,c*B+C,B+C]
 raise ValueError('unknown profile')

def generate_text(sid,c,a,n,p):
 L=s.log(a*x**n);D=n/x;T=a*x**n;kind=CONFIG[sid][1]
 F=c*L**p/x
 # Retain displayed source numerator/denominator coefficient roles.
 if kind=='inverse':
  body=r'\frac{'+tex(L**p)+'}{'+tex(x/c)+'}'if p>0 else r'\frac{1}{'+tex(x/c)+tex(L**(-p))+'}'
 else:body=r'\frac{'+tex(c*L**p)+'}{x}'if p>0 else r'\frac{'+tex(c)+'}{x'+tex(L**(-p))+'}'
 I=r'\int '+body+r'\,\text{d}x'
 prompt='Calculate the integral $'+I+'.$'
 prefix=''if c==1 else tex(c)
 integral=lambda body,var='u':r'\int '+body+r'\,\text{d}'+var
 # All source rows retain the original extraction, transformed integral,
 # coefficient collection, power-rule, simplification, back-substitution order.
 rows=[I+' & ='+prefix+integral(tex(L**p)+r'\cdot \frac{1}{x}','x')]
 if n!=1:
  rows.append(' & ='+prefix+integral(tex(u**p)+r'\cdot '+tex(1/n)))
  rows.append(' & ='+tex(c/n)+integral(tex(u**p)))
 else:rows.append(' & ='+prefix+integral(tex(u**p)))
 if p==-1:
  if sid=='q-13822':rows.append(' & ='+prefix+integral(r'\frac{1}{u}'))
  rows.extend([' & ='+tex(c/n)+r'\ln|u|+C',' & ='+tex(c/n)+r'\ln|'+tex(L)+r'|+C'])
 else:
  if p.q==2:rows.append(' & ='+tex(c/n)+integral('u^{'+tex(p)+'}'))
  rows.append(' & ='+tex(c/n)+r'\cdot '+r'\frac{u^{'+tex(p+1)+'}}{'+tex(p+1)+'}+C')
  if sid!='q-2380':rows.append(' & ='+tex(c/(n*(p+1))*u**(p+1))+'+C')
  final=c/(n*(p+1))*L**(p+1)
  if p==s.Rational(1,2):final=c/(n*(p+1))*s.sqrt(L**3)
  rows.append(' & ='+tex(final)+'+C')
 deriv=r'\frac{\text{d}u}{\text{d}x}='
 if T!=x:deriv+=r'\frac{1}{'+tex(T)+'}'+r'\cdot '+tex(s.diff(T,x))
 if T==x or sid not in('q-210746','q-210743'):deriv+=(''if T==x else'=')+tex(D)
 deriv+=r'\quad\Longrightarrow\quad '+(''if n==1 else tex(1/n))+r'\text{d}u=\frac{\text{d}x}{x}.'
 solution="Let's set $u="+tex(L)+'.$ Then, we have\n\n$$\n'+deriv+'\n$$\n\nUsing the above, we can write the integral in terms of $u$ and evaluate:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
 return prompt,solution,F,L

@fmt.checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if type(seed)is not int:raise ValueError('seed must be builtin int')
 level={'medium':'moderate'}.get(level,level)
 if level not in('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in(None,'radio',':answer-field.type/radio'):raise ValueError('only source radio fields')
 candidates=[k for k,v in CONFIG.items()if v[0]==level]
 if template is not None and template not in candidates:raise ValueError('template/level mismatch')
 rng=random.Random(seed);sid=template or rng.choice(candidates)
 # Each template owns its complete observed profile, chosen before parameters.
 if profile not in(None,'observed',sid):raise ValueError('whole observed profile only')
 for attempt in range(1000):
  par=dict(parameters)if parameters is not None else original(sid)
  if parameters is None:
   par['k']=rng.choice([2,3,5,6,7,10,11])if CONFIG[sid][1]=='radical'else rng.randint(1,12)
   if CONFIG[sid][3]!=1:par['a']=rng.randint(2,6)
   if CONFIG[sid][4]!=1:par['n']=rng.randint(2,4)
   if level=='easy':par['p_num']=rng.randint(1,3)
  c,a,n,p=globals()['parameters'](sid,par)
  prompt,solution,F,L=generate_text(sid,c,a,n,p)
  vals=bank(sid,c,a,n,p,L);correct=(c/n*s.log(s.Abs(L))+C)if p==-1 else c/(n*(p+1))*L**(p+1)+C
  # Compare exact values including presence of C. Do not conflate omitted C
  # with the complete family requested by the indefinite-integral task.
  duplicate=any(equivalent(v,w)for j,v in enumerate(vals)for w in vals[:j])
  if p==s.Rational(1,2):correct=c/(n*(p+1))*s.sqrt(L**3)+C
  good=[j for j,v in enumerate(vals)if equivalent(v,correct)]
  if not duplicate and len(good)==1:break
  if parameters is not None:raise ValueError('whole bank invalid or colliding')
 else:raise ValueError('bounded whole-profile sampling exhausted')
 repairs=[]
 if sid in('q-13807','q-210742'):repairs.append('remove source dangling multiplication marker')
 if sid=='q-2202':repairs=['complete missing key and solution; authored easy placement']
 # At original parameters use the actual observed prompt/operative source rows,
 # with only explicit typography/dangling-operator repairs. Variant renderer
 # above preserves the same prose and ordered stages without a generic rewrite.
 if par==original(sid):
  prompt=QS[sid][':question/problem']
  if sid!='q-2202':solution=QS[sid][':question/worked-solution'].replace(r'\cdot  \\',r' \\')
 prompt=fmt.normalize_prose(prompt);solution=fmt.normalize_prose(solution)
 values=[tex(v)for v in vals]
 # Original bare TeX source values retained after canonical normalization.
 if par==original(sid):values=[fmt.normalize_tex(z[':answer/value'])for z in QS[sid][':question/answer-fields'][0][':answer-field/choices']]
 content=digest({'prompt':prompt,'solution':solution,'bank':sorted(values),'correct':values[good[0]],'profile':sid});qid=uid(content);fid=uid(qid+'selection')
 answers=[{':answer/id':uid(fid+v),':answer/type':':answer.type/math',':answer/value':v}for v in values];key=answers[good[0]][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',key]}
 # Real-interval canonical task identity: x=exp(t), and separately
 # x=-exp(t) for even n. Positive a makes log(a*exp(n*t))=log(a)+n*t
 # valid here without a forced complex logarithm identity.
 t=s.Symbol('real_log_abs_x',real=True);canonical=s.cancel(s.expand(c*(s.expand_log(s.log(a))+n*t)**p))
 math_id=digest({'coefficient_over_x':s.srepr(canonical),'negative_x_branch':bool(n%2==0),'log_role':'positive'if p.q==2 else'nonzero'if p<0 else'any real'})
 domain='a*x^n>0; log(a*x^n)>0'if p.q==2 else'a*x^n>0; log(a*x^n)!=0'if p<0 else'a*x^n>0'
 return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'source_basis':2275,'template':sid,'bank_profile':sid,'source_ids':[sid],'parameters':par,'domain':domain,'eligible':True,'evidence_only':False,'origin':'authored_completion'if sid=='q-2202'else'observed_source_pattern','source_repairs':repairs,'math_fingerprint':math_id,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__}}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def generate_batch(level,seed=0,count=1,**kw):
 if type(seed)is not int or type(count)is not int or not 1<=count<=100:raise ValueError('builtin seed/count; count1..100')
 if level=='easy'and count>69:raise ValueError('easy bounded capacity at most69 distinct mathematical tasks')
 rows=[];seen=set()
 for i in range(count*100):
  row=generate(level,seed+i,**kw);fp=row['generation']['math_fingerprint']
  if fp not in seen:rows.append(row);seen.add(fp)
  if len(rows)==count:return rows
 raise ValueError('bounded capacity exhausted without repeated mathematical tasks')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 rows=[r for level in(['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty])for r in generate_batch(level,args.seed,args.count,template=args.template,profile=args.profile)]
 print(json.dumps(rows,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n---\n\n'.join(map(markdown,rows)))
