#!/usr/bin/env python3
"""Basis2275 derivative-matched definite substitution. No database operations.

Easy: linear denominator; moderate: polynomial inner and matched numerator;
hard: quadratic inner, square root of its cube. Each level has fixed method
and arithmetic bounds. Frozen evidence, formatter and parser live beside this
script. Observed-pattern banks are explicitly distinct from authored defaults.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import argparse,hashlib,importlib.util,json,random,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).with_suffix('')
def module(name,file):
 spec=importlib.util.spec_from_file_location(name,HERE/'reference'/file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=module('kp00877_format','math_format.py')
KP=17592186100877;VERSION='definite-rational-b2275-v1'
SOURCE=json.loads((HERE/'source.json').read_text());REC=SOURCE['record'];QS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
x,u=s.symbols('x u',real=True)
# Every original MA question has its own prompt/solution structural family.
# Parameters: polynomial degree n, inner scale a/shift b, numerator scale c,
# and ORIGINAL x-limits lo/hi. No independently sampled dependent quantities.
CONFIG={
'q-12912':('moderate','radio',(2,1,1,1,0,1)),
'q-12917':('moderate','radio',(3,1,9,1,-2,0)),
'q-113747':('moderate','radio',(2,3,1,1,0,1)),
'q-13189':('easy','radio',(1,3,2,1,1,2)),
'q-15877':('easy','radio',(1,1,-4,-4,5,8)),
'q-19129':('moderate','radio',(2,1,1,4,0,2)),
'q-336717':('easy','blank',(1,4,-1,1,1,3)),
'q-336729':('moderate','blank',(4,5,4,10,0,1)),
'q-336745':('hard','blank',(2,1,1,6,0,1)),
'q-73432':('moderate','radio',(4,1,9,1,0,2)),
'q-73434':('moderate','radio',(3,1,2,1,-1,1)),
}
SLOTS=('n','a','b','c','lo','hi')
def parameters(vals):return dict(zip(SLOTS,vals))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def uid(t):return str(uuid.uuid5(uuid.NAMESPACE_URL,VERSION+str(t)))
def tex(v):return fmt.normalize_tex(s.latex(s.expand_log(s.sympify(v)),fold_short_frac=False))
def eq(a,b):return s.simplify(s.expand_log(a-b))==0

def guard(sid,p):
 if set(p)!=set(SLOTS) or any(type(p[k])is not int for k in SLOTS):raise ValueError('integer slots n,a,b,c,lo,hi required')
 n,a,b,c,L,H=[p[k]for k in SLOTS];level=CONFIG[sid][0]
 if n!=(1 if level=='easy' else 2 if level=='hard' else CONFIG[sid][2][0]):raise ValueError('fixed family degree')
 if not(1<=a<=5 and -9<=b<=12 and 1<=abs(c)<=12 and -3<=L<H<=8 and H-L<=4):raise ValueError('outside bounded comparable arithmetic workload')
 T=a*x**n+b
 # Polynomial extrema on the entire real closed interval, not endpoint-only.
 critical=[s.Integer(L),s.Integer(H)]+([s.Integer(0)]if n%2==0 and L<=0<=H else [])
 vals=[T.subs(x,z)for z in critical]
 if min(vals)<=0 or max(vals)>150:raise ValueError('whole interval requires strictly positive inner, finite bounded endpoints')
 ul=T.subs(x,L);uh=T.subs(x,H)
 if sid=='q-15877'and ul!=1:raise ValueError('source drops ln(lower) because lower inner is one')
 if sid in ('q-13189','q-15877','q-73432','q-12917'):
  power=3 if sid=='q-13189'else 2
  if not s.real_root(uh,power).is_Integer:raise ValueError('preserve source perfect-power endpoint arithmetic')
  if sid=='q-73432'and not s.sqrt(ul).is_Integer:raise ValueError('both endpoints remain perfect squares')
 if level=='hard'and c<0:raise ValueError('positive source hard numerator')
 return n,s.Integer(a),s.Integer(b),s.Integer(c),s.Integer(L),s.Integer(H)

def integral(body,var,L,H):return r'\int_{'+tex(L)+'}^{'+tex(H)+'}'+body+r'\,\text{d}'+var

def bank(sid,p,profile,correct,ul,uh,r):
 n,a,b,c,L,H=[s.Integer(p[k])for k in SLOTS]
 if CONFIG[sid][1]=='blank':return [correct]
 if profile=='authored':return [correct,-correct,(a*n)*correct,correct/(a*n),r*(uh*s.log(uh)-ul*s.log(ul))]
 # Complete observed banks. Some scalar evidence underdetermines intent; these
 # explicitly recorded algebraic patterns are selectable source-pattern variants, never inferred intent.
 if sid=='q-12912':return [s.log(uh),s.Integer(0),correct,2*s.log(uh),r]
 if sid=='q-12917':return [r*s.log(s.sqrt(uh)),2*r*s.log(s.sqrt(uh)),s.log(s.sqrt(uh)),s.Rational(3,2)*s.log(s.sqrt(uh)),2*s.log(s.sqrt(uh))]
 if sid=='q-113747':return [r*s.log(a),s.log(uh),a*n*s.log(uh),s.log(a),correct]
 if sid=='q-13189':
  h=s.real_root(uh,3);return [s.log(h)-a*s.log(ul),-r*s.log(h)-r*s.log(ul),r*s.log(h)-r*s.log(ul),correct,-s.log(h)-r*s.log(ul)]
 if sid=='q-15877':return [-correct,-correct/2,correct,3*correct/4,-3*correct/4]
 if sid=='q-19129':return [s.log(r*uh),r*s.log(r),uh*s.log(r),correct,(c+2)*s.log(r)]
 if sid=='q-73432':
  z=s.sqrt(ul)/H;w=s.sqrt(uh)/s.sqrt(ul);return [2*r*s.log(z),r*s.log(z),r*s.log(H),r*s.log(w),2*r*s.log(w)]
 if sid=='q-73434':return [2*s.log(uh/b),2*r*s.log(uh),s.log(uh/b),correct,n*s.log(uh)]
 raise ValueError('unknown bank')

def core(sid,p,profile):
 n,a,b,c,L,H=guard(sid,p);T=a*x**n+b;D=s.diff(T,x);N=c*x**(n-1);r=c/(a*n);ul=T.subs(x,L);uh=T.subs(x,H);hard=CONFIG[sid][0]=='hard'
 if sid=='q-12917'and profile=='observed'and ul!=1:raise ValueError('observed q12917 bank assumes transformed lower endpoint one')
 # The source explicitly uses a radical denominator in its hard family.
 den=r'\sqrt{('+tex(T)+r')^{3}}'if hard else tex(T)
 F=N/(T**s.Rational(3,2))if hard else N/T
 body=r'\frac{'+tex(N)+'}{'+den+'}';I=integral(body,'x',L,H)
 correct=s.simplify((-2*r/s.sqrt(uh)+2*r/s.sqrt(ul))if hard else r*s.log(uh/ul))
 values=[s.simplify(v)for v in bank(sid,p,profile,correct,ul,uh,r)]
 if any(v.is_real is not True or v.is_finite is not True for v in values):raise ValueError('non-real/nonfinite bank')
 for i,v in enumerate(values):
  if any(eq(v,z)for z in values[:i]):raise ValueError('reject whole colliding profile instance')
 if sum(eq(v,correct)for v in values)!=1:raise ValueError('complete bank missing unique correct answer')
 blank=CONFIG[sid][1]=='blank'
 if blank:prompt='Compute the exact value of the definite integral.\n\n$'+I+'=$\n{{field-1}}'
 elif sid=='q-13189':prompt='Evaluate the definite integral $'+I+'.$'
 elif sid=='q-15877':prompt='$'+I+'=$'
 else:prompt='Calculate the definite integral $'+I+'.$'
 # Preserve original source operative row presence: no reciprocal differential
 # row for q15877/hard, unscaled x^(n-1) for q336729, scaled numerator elsewhere.
 rows=['u & ='+tex(T),r'\frac{\text{d}u}{\text{d}x} & ='+tex(D),r'\text{d}u & ='+tex(D)+r'\,\text{d}x']
 if sid not in ('q-15877','q-336745'):
  scale=s.Integer(1)/(a*n)if sid=='q-336729'else r
  operand=x**(n-1)if sid=='q-336729'else N
  rows.append(tex(scale)+r'\,\text{d}u & ='+tex(operand)+r'\,\text{d}x')
 aligned=lambda rr:r'\begin{aligned}'+r' \\ '.join(rr)+r'\end{aligned}'
 display=lambda z:'\n\n$$\n'+z+'\n$$'
 solution='We start by changing the variable:'+display(aligned(rows))
 solution+='\n\nNext, we create a table for the limits of integration using the rule $u='+tex(T)+'.$'
 solution+=display(aligned(['x & '+tex(L)+' & '+tex(H),'u & '+tex(ul)+' & '+tex(uh)]))
 if hard:transbody=r'\frac{'+tex(r)+r'}{\sqrt{u^{3}}}'
 elif sid=='q-15877':transbody=r'\frac{'+tex(r)+'}{u}'
 elif sid=='q-336729':transbody=r'\frac{'+tex(c)+r'}{u}\cdot '+tex(1/(a*n))
 else:transbody=r'\frac{1}{u}\cdot '+tex(r)
 J=integral(transbody,'u',ul,uh)
 conversion=I
 if sid in ('q-113747','q-19129','q-73432','q-73434'):
  conversion=integral(r'\frac{1}{('+tex(T)+r')}\cdot '+tex(N),'x',L,H)
 solution+='\n\nSo, the integral in terms of the new variable is'+display(conversion+'='+J+'.')
 if hard:
  prim=-2*r/s.sqrt(u);evalrow=tex(-2*r)+r'\frac{1}{\sqrt{'+tex(uh)+'}}+'+tex(2*r)+r'\frac{1}{\sqrt{'+tex(ul)+'}}'
  finalrows=[integral(tex(r)+r'u^{-3/2}','u',ul,uh)+' & ='+tex(prim)+r'|_{'+tex(ul)+'}^{'+tex(uh)+'}', ' & ='+evalrow,' & ='+tex(2*r/s.sqrt(ul))+'-'+tex(2*r)+r'\frac{1}{\sqrt{'+tex(uh)+'}}',' & ='+tex(correct)+'.']
 else:
  prim=r*s.log(u);evalrow=tex(r)+r'(\ln('+tex(uh)+r')-\ln('+tex(ul)+'))'
  finalrows=[J+' & ='+tex(r)+integral(r'\frac{1}{u}','u',ul,uh),' & ='+tex(r)+r'\ln(u)|_{'+tex(ul)+'}^{'+tex(uh)+'}',' & ='+evalrow]
  # Preserve the extra log-power expansion stages in these observed families.
  if sid in ('q-13189','q-15877','q-73432'):
   power=3 if sid=='q-13189'else 2;root=s.real_root(uh,power)
   expanded=tex(r)+r'(\ln(('+tex(root)+')^{'+str(power)+r'})-\ln('+tex(ul)+'))'
   factors=tex(r)+'('+tex(power)+r'\ln('+tex(root)+r')-\ln('+tex(ul)+'))'
   if sid=='q-15877':
    expanded=tex(r)+r'\ln(('+tex(root)+')^{2})';factors=tex(r)+r'\cdot 2\ln('+tex(root)+')'
   if sid=='q-73432':
    rootl=s.sqrt(ul);expanded=tex(r)+r'(\ln(('+tex(root)+r')^{2})-\ln(('+tex(rootl)+r')^{2}))';factors=tex(r)+r'(2\ln('+tex(root)+r')-2\ln('+tex(rootl)+'))'
   finalrows.extend([' & ='+expanded,' & ='+factors])
   if sid=='q-73432':finalrows.append(' & ='+tex(r)+r'\cdot 2(\ln('+tex(root)+r')-\ln('+tex(rootl)+'))')
  finalrows.append(' & ='+tex(correct)+'.')
 solution+='\n\nFinally, we can solve it and get'+display(aligned(finalrows))
 return fmt.normalize_prose(prompt),fmt.normalize_prose(solution),values,correct,dict(F=F,T=T,D=D,L=L,H=H,ul=ul,uh=uh,r=r)

def sample(sid,rng,profile):
 level=CONFIG[sid][0];n=CONFIG[sid][2][0]
 for _ in range(3000):
  a=rng.randint(1,5);b=rng.randint(-9,12);c=rng.choice([1,2,3,4,6,8,10,12]if level!='hard'else[2,4,6,8,10,12]);L=rng.randint(-3,3);H=L+rng.randint(1,4)
  if sid=='q-15877':
   c=-rng.randint(1,8);a=rng.choice([1,2,3,5]);b=1-a*L
  elif sid=='q-13189':b=rng.choice([8,27,64])-a*H
  elif sid=='q-73432':a,b,L,H=rng.choice([(5,4,0,1),(1,9,0,2),(1,9,-2,0),(5,4,-1,0)])
  p=parameters((n,a,b,c,L,H))
  try:core(sid,p,profile)
  except ValueError:continue
  return p
 raise ValueError('no eligible complete profile instance')

# EASY: linear logarithm; fixed substitution/table/log-evaluation workload.
# MODERATE: matched x^(n-1), fixed family degree2/3/4, same log workload.
# HARD: quadratic inner, inverse3/2 power, same root evaluation workload.
@fmt.checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if type(seed)is not int:raise ValueError('seed must be a builtin integer')
 level={'medium':'moderate'}.get(level,level)
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 rng=random.Random(seed);eligible=[k for k,v in CONFIG.items()if v[0]==level and(field_type is None or field_type in(v[1],':answer-field.type/'+v[1]))]
 if template is not None:
  if template not in eligible:raise ValueError('template/level/field mismatch')
  sid=template
 else:sid=rng.choice(eligible)
 # Select the whole profile BEFORE sampling its parameter instance.
 profile=profile or('observed'if CONFIG[sid][1]=='blank'else'authored')
 if profile not in ('observed','authored'):raise ValueError('profile')
 p=dict(parameters)if parameters is not None else sample(sid,rng,profile)
 prompt,solution,values,correct,data=core(sid,p,profile)
 fieldkind=CONFIG[sid][1];key='field-1'if fieldkind=='blank'else'selection'
 contents={'prompt':prompt,'solution':solution,'field_type':fieldkind,'key':key,'bank':sorted(tex(v)for v in values),'correct':tex(correct)}
 content_id=digest(contents);qid=uid(content_id);fid=uid(qid+key)
 answers=[{':answer/id':uid(fid+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)}for v in values]
 correctid=next(a[':answer/id']for a,v in zip(answers,values)if eq(v,correct))
 if fieldkind=='radio':rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+fieldkind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]}
 math_id=digest({'integrand':s.srepr(s.cancel(data['F'])),'bounds':[str(data['L']),str(data['H'])],'domain':'inner>0 on closed real interval'})
 return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},'generation':{'version':VERSION,'seed':seed,'basis':2275,'template':sid,'parameters':p,'bank_profile':profile,'source_ids':[sid],'math_fingerprint':math_id,'content_fingerprint':content_id,'domain':'a*x^n+b>0 throughout closed original x interval; no poles','eligible':True,'evidence_only':False,'source_basis':2275,'origin':'authored_completion'if sid in('q-12912','q-12917')else'authored_bank'if profile=='authored'else'observed_source_pattern','authored_completion':sid in('q-12912','q-12917'),'source_repairs':['independently derived missing key','authored shared-method worked solution']if sid in('q-12912','q-12917')else['normalize malformed bare ln TeX in final solution']if sid=='q-336717'else[],'authored':profile=='authored' or sid in('q-12912','q-12917'),'runtime':{'python':sys.version.split()[0],'sympy':s.__version__}}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<=0:ap.error('--count must be positive')
 rows=[generate(l,args.seed+i,template=args.template,profile=args.profile)for l in(['easy','moderate','hard']if args.difficulty=='all'else[args.difficulty])for i in range(args.count)]
 print(json.dumps(rows,indent=2,ensure_ascii=False)if args.format=='json'else'\n\n---\n\n'.join(markdown(r)for r in rows))
