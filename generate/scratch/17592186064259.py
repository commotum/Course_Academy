#!/usr/bin/env python3
"""Source-backed polynomial tangent-slope questions. No database operations.

Only moderate is supported (observed level). Seven original banks are replayed;
q-128236 is excluded because f(x) is absent from its standalone prompt.
Normal typography is standardized; derivative -> slope equation -> solve ->
branch selection is preserved. See package classification and extraction.
"""
from __future__ import annotations
import argparse, hashlib, json, random, sys, uuid
from pathlib import Path
# Same dependency environment as application inventory jobs.
try: import sympy as sp
except ImportError:
    import os
    os.execv(str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),[str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),__file__,*sys.argv[1:]])
KP_ID=17592186064259
KP_UUID='00a74f63-a4eb-5894-b4a4-eb4fd297a3f3'
TITLE='Finding a Point on a Curve With a Certain Slope'
VERSION='polynomial-tangent-slope-1.0'
SUPPORTED_LEVELS=('moderate',)
HERE=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':2207,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
x=sp.Symbol('x',real=True)
PROFILES={
 'quadratic_radio':('quadratic','radio','q-102236'),
 'quadratic_blank':('quadratic','blank','q-343735'),
 'cubic_positive_blank':('positive','blank','q-343737'),
 'positive_offsets':('positive','radio','q-48692'),
 'positive_multiples':('positive','radio','q-48970'),
 'cubic_all':('all','radio','q-48817'),
 'cubic_repeated':('repeated','radio','q-48816')}
CASES={
 'quadratic_radio':{'a':'0','b':'1','c':'-3','d':'10','m':'-1'},
 'quadratic_blank':{'a':'0','b':'2','c':'4','d':'-3','m':'1'},
 'cubic_positive_blank':{'a':'1','b':'1','c':'14','d':'-6','m':'22'},
 'positive_offsets':{'a':'1','b':'-2','c':'-5','d':'0','m':'27'},
 'positive_multiples':{'a':'8','b':'-3','c':'-12','d':'-4','m':'6'},
 'cubic_all':{'a':'-2','b':'6','c':'20','d':'-1','m':'2'},
 'cubic_repeated':{'a':'1','b':'3','c':'6','d':'-3','m':'3'}}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def tex(v):return sp.latex(v)
def canonical(p):return {k:str(v) for k,v in p.items()}
def normalize_parameters(profile,p):
 if set(p)!=set('abcdm'):raise ValueError('Require a,b,c,d,m')
 if any(isinstance(v,(float,bool)) for v in p.values()):raise ValueError('Exact rational parameters only')
 p={k:sp.Rational(v) for k,v in p.items()}
 if any(v.q!=1 or abs(v)>200 for v in p.values()):raise ValueError('Integer coefficients of magnitude <=200')
 family=PROFILES[profile][0]; f=p['a']*x**3+p['b']*x**2+p['c']*x+p['d'];roots=sp.solve(sp.diff(f,x)-p['m'],x)
 if family=='quadratic':
  if p['a']!=0 or p['b']==0 or len(roots)!=1:raise ValueError('Nondegenerate quadratic required')
 elif p['a']==0 or any(not r.is_Rational for r in roots):raise ValueError('Cubic with rational tangent locations required')
 if family=='positive' and (len(roots)!=2 or sum(bool(r>0) for r in roots)!=1 or not min(roots)<0):raise ValueError('Exactly one positive and one negative root')
 if family=='all' and (len(roots)!=2 or not min(roots)<0<max(roots)):raise ValueError('Two opposite-sign rational roots')
 if family=='repeated' and (len(roots)!=1 or roots[0]==0):raise ValueError('One repeated nonzero root')
 if family=='quadratic' and roots[0]==0:raise ValueError('Nonzero root policy avoids bank collisions')
 if profile=='positive_offsets' and max(roots)<=3:raise ValueError('Positive root >3 for observed positive offsets')
 return p

def objects(profile,p):
 f=p['a']*x**3+p['b']*x**2+p['c']*x+p['d'];df=sp.diff(f,x);roots=sorted(sp.solve(df-p['m'],x));family,ft,_=PROFILES[profile]
 ans=tuple(roots) if family=='all' else (max(roots) if family=='positive' else roots[0],)
 if ft=='blank':values=[ans];recipes=['correct_exact_fragment']
 elif profile in ('quadratic_radio','cubic_repeated'):
  r=ans[0];values=[(r,),(-r,),(-2*r,),(2*r,),(sp.Integer(0),)];recipes=['correct','negate_root','negative_double_root','double_root','zero']
 elif profile=='positive_offsets':
  r=ans[0];values=[(r,),(r-1,),(r+1,),(r-2,),(r-3,)];recipes=['correct','root_minus_1','root_plus_1','root_minus_2','root_minus_3']
 elif profile=='positive_multiples':
  r=ans[0];values=[(r,),(12*r,),(2*r,),(3*r,),(4*r,)];recipes=['correct','12_times_root','2_times_root','3_times_root','4_times_root']
 else:
  u,v=roots;values=[(u,v),(v,),(-v,),(-u,),tuple(sorted((-v,-u)))];recipes=['correct','positive_root_only','negate_positive_root','negate_negative_root','negate_both_roots']
 if len(set(values))!=len(values):raise ValueError('Complete bank collision')
 return f,df,roots,ans,values,recipes

def sample(profile,rng):
 family,ft,_=PROFILES[profile]
 for _ in range(1000):
  d=rng.randint(-12,12)
  if family=='quadratic':
   b=rng.choice([i for i in range(-5,6) if i]);c=rng.choice([i for i in range(-12,13) if i]);m=rng.randint(-12,12);p=dict(a=0,b=b,c=c,d=d,m=m)
  else:
   a=sp.Rational(rng.choice([-3,-2,-1,1,2,3,4,8]));u=-rng.choice([1,2,3,4,sp.Rational(3,4),sp.Rational(8,3)]);v=rng.choice([1,2,3,4,5,6,sp.Rational(4,3)])
   if profile=='positive_offsets':v=rng.choice([4,5,6,7,8])
   if family=='repeated':u=v=sp.Rational(rng.choice([-4,-3,-2,-1,1,2,3,4]))
   m=rng.randint(-12,12);p=dict(a=a,b=-3*a*(u+v)/2,c=m+3*a*u*v,d=d,m=m)
  try:
   p=normalize_parameters(profile,p);objects(profile,p);return p
  except ValueError:pass
 raise ValueError('Bounded sampler exhausted')

def mathematical_fingerprint(profile,p):
 # Entire assessed slope equation modulo nonzero scale. Vertical translation,
 # additive derivative/slope shift, bank, response type and seed do not add tasks.
 f=p['a']*x**3+p['b']*x**2+p['c']*x+p['d'];poly=sp.Poly(sp.diff(f,x)-p['m'],x).monic()
 return digest({'slope_equation':list(map(str,poly.all_coeffs())),'requested_branch':PROFILES[profile][0]})

def render(profile,p):
 f,df,roots,ans,values,recipes=objects(profile,p);family,ft,_=PROFILES[profile]
 target='**positive** $x$-coordinate' if family=='positive' else '$x$-coordinates' if family=='all' else '$x$-coordinate'
 point='points' if family=='all' else 'point'
 opening='Find the exact value of the ' if profile=='quadratic_blank' else 'Find the '
 prompt=opening+f'{target} of the {point} on the curve $y={tex(f)}$ whose tangent has a slope of ${tex(p["m"])}.$'
 if ft=='blank':prompt+='\n\n$x=$\n{{field-1}}'
 else:prompt+='\n\n{{selection}}'
 # Separate differentiated terms preserve the power-rule stages of the source.
 derivative_terms=' + '.join('('+tex(coef)+')'+r'\cdot '+str(power)+r'\cdot '+tex(x**(power-1)) for (power,),coef in sp.Poly(f,x).terms() if power)
 intro=f'Let $f(x)={tex(f)}.$ The slope of the tangent at the point $x$ is equal to $f^{{\\prime}}(x).$ Computing the derivative, we get'
 derivative_rows=[r'f^{\prime}(x) &= \frac{\mathrm{d}}{\mathrm{d}x}\left('+tex(f)+r'\right)', '&= '+derivative_terms, '&= '+tex(df)]
 eq=df-p['m'];rows=[tex(df)+' &= '+tex(p['m'])]
 if family=='quadratic':
  rows += [tex(2*p['b']*x)+' &= '+tex(p['m']-p['c']), 'x &= '+tex(ans[0])]
 else:
  rows += [tex(eq)+' &= 0',tex(sp.factor(eq))+' &= 0','x &= '+r',\,'.join(tex(r) for r in roots)]
 def aligned(rs):return '$$\n'+r'\begin{aligned}'+'\n'+(' '+r'\\'+'\n').join(rs)+'\n'+r'\end{aligned}'+'\n$$'
 solution=intro+'\n\n'+aligned(derivative_rows)+f'\n\nWe now set $f^{{\\prime}}(x)={tex(p["m"])}$ and solve for $x:$\n\n'+aligned(rows)+'\n\n'
 if family=='positive':solution+=f'Since $x>0$, the required coordinate is $x={tex(ans[0])}.$'
 else:solution+=f'Therefore, the slope of the tangent is equal to ${tex(p["m"])}$ at '+('the points' if family=='all' else 'the point')+' where $x='+r',\,'.join(tex(r) for r in ans)+'.$'
 return prompt,solution,values,recipes

def generate(level='moderate',seed=0,template=None,parameters=None,profile=None):
 if level not in SUPPORTED_LEVELS:raise ValueError('Only observed moderate is supported; easy/hard reserves remain unfilled')
 profile=profile or template or random.Random(seed).choice(list(PROFILES))
 if profile not in PROFILES:raise ValueError('Unknown template/profile')
 if template and template!=profile:raise ValueError('Template/profile mismatch')
 rng=random.Random(seed);p=normalize_parameters(profile,parameters) if parameters is not None else sample(profile,rng)
 prompt,solution,values,recipes=render(profile,p);ft=PROFILES[profile][1]
 fp=mathematical_fingerprint(profile,p)
 # Identity includes rendered task; mathematical dedupe is stricter than identity.
 qid=uid(VERSION+':'+digest([profile,canonical(p)]));fid=uid(qid+':field')
 answers=[]
 for value in values:
  val=(('x=' if ft=='radio' else '')+r',\,'.join(tex(v) for v in value))
  answers.append({':answer/id':uid(fid+':'+digest(list(map(str,value)))),':answer/type':':answer.type/math',':answer/value':val})
 correct=answers[0][':answer/id'];random.Random(seed).shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection' if ft=='radio' else 'field-1',':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':profile,'bank_profile':profile,'parameters':canonical(p),'source_id':PROFILES[profile][2],'source':SOURCE,'difficulty_design':level,'eligible_for_learning':True,'evidence_only':False,'mathematical_fingerprint':fp,'recipes':recipes,'domains':'Real x; polynomial. Positive templates select the sole positive root.','runtime':{'sympy':sp.__version__}}}
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$' for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',default='moderate');ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--parameters');ap.add_argument('--format',choices=['json','markdown'],default='json');args=ap.parse_args()
 if not 1<=args.count<=1000:ap.error('Count must be 1..1000')
 recs=[generate(args.difficulty,args.seed+i,args.template,json.loads(args.parameters) if args.parameters else None,args.profile) for i in range(args.count)]
 print(json.dumps(recs,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,recs)))
if __name__=='__main__':main()
