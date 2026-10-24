#!/usr/bin/env python3
"""Bounded, source-derived tangent-slope questions. No database side effects."""
import argparse, hashlib, itertools, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186064342
KP_UUID='2ffbc4bb-e179-543f-bcb5-3aaf6540a8a1'
TITLE='Calculating the Slope of a Tangent Line of a Curve at a Given Point'
VERSION='tangent-slope-v1'
PACKAGE=Path(__file__).with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
x=sp.Symbol('x')
PROFILES={
 'q-167637':{'difficulty':'easy','original':[3,1,2,0],'domains':[[2,3,4,5,6],[1],[1,2,3,4,5],[0]],'kind':'blank'},
 'q-10742':{'difficulty':'moderate','original':[1,6,2670,3],'domains':[[1,2],[4,5,6,7],[800,1200,1800,2400,2670],[2,3]],'kind':'radio'},
 'q-1853':{'difficulty':'moderate','original':[3,6,2],'domains':[[2,3,4],[4,5,6,7],[2,3,4]],'kind':'radio'},
 'q-342107':{'difficulty':'moderate','original':[1,4,8,4,-1],'domains':[[1,2,3],[3,4,5],[6,7,8],[4],[-2,-1,1,2]],'kind':'blank'},
 'q-342937':{'difficulty':'moderate','original':[2,2,3],'domains':[[1,2,3,4],[1,2,3],[2,3,4]],'kind':'blank'},
 'q-342942':{'difficulty':'moderate','original':[2,7,6,3],'domains':[[1,2,3],[5,6,7],[4,5,6],[2,3,4]],'kind':'blank'}
}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def tex(z):return sp.latex(z).replace('- ','-')
def expression(sid,p):
 if sid=='q-167637':a,b,c,t=p;return a*sp.exp(x)-b*x**3-c*x
 if sid=='q-10742':a,b,c,t=p;return a*x**7-b*x**5-c*x
 if sid=='q-1853':a,b,t=p;return a*x**4-b*x**3+1/x
 if sid=='q-342107':a,b,c,d,t=p;return a*x**6-b*x**4+c*x**2-d
 if sid=='q-342937':a,h,t=p;return -a*x**2+1/(x-h)**2
 if sid=='q-342942':a,b,c,t=p;return a*x**4-b*x**3-c*x**2-1/x
 raise ValueError(sid)
def bank(sid,p):
 f=expression(sid,p);t=p[-1];s=sp.diff(f,x).subs(x,t)
 if sid=='q-10742':return [s+1,s+2,s,-(s+2),-s],2,['s+1','s+2','s','-(s+2)','-s']
 if sid=='q-1853':D=sp.Integer(t)**2;N=D*s;return [N/(D-1),N/(D-2),(N-2)/D,N/D,(N+2)/D],3,['N/(D-1)','N/(D-2)','(N-2)/D','N/D','(N+2)/D']
 return [s],0,[]
def allowed(sid,p):
 if len(p)!=len(PROFILES[sid]['domains']) or any(type(z)!=int for z in p):return False
 if sid=='q-10742':
  a,b,c,t=p
  if a not in (1,2) or b not in (4,5,6,7) or t not in (2,3) or c<=0 or not -8<=7*a*t**6-5*b*t**4-c<=8:return False
 elif any(z not in domain for z,domain in zip(p,PROFILES[sid]['domains'])):return False
 if sid=='q-342937' and p[-1]==p[-2]:return False
 values,_,_=bank(sid,p)
 return len(set(values))==len(values) and all(z.is_finite is True and z.is_Rational is True for z in values)
def candidates(sid):
 if sid=='q-10742':return [[a,b,7*a*t**6-5*b*t**4-s,t] for a,b,t,s in itertools.product([1,2],[4,5,6,7],[2,3],range(-8,9)) if allowed(sid,[a,b,7*a*t**6-5*b*t**4-s,t])]
 return [list(p) for p in itertools.product(*PROFILES[sid]['domains']) if allowed(sid,list(p))]
def fingerprint_params(sid,p):return digest([str(sp.cancel(sp.diff(expression(sid,p),x))),p[-1]])
def render(sid,p):
 f=expression(sid,p);d=sp.diff(f,x);t=p[-1];s=d.subs(x,t);ft=tex(f);dt=tex(d);tt=str(t);st=tex(s)
 easy=sid=='q-167637';blank=PROFILES[sid]['kind']=='blank';name='k' if easy else 'f'
 if easy:
  prompt=f'Find $m,$ the slope of the tangent to the curve $y=k(x)$ at the point where $x={tt}.$\n\n'+f'We have $k(x)={ft}$ and $k\\prime(x)={dt}.$\n\n$m=$\n{{{{field-1}}}}'
 elif blank:prompt=f'Find the exact value of the slope $m$ of the tangent to the curve $y={ft}$ at the point where $x={tt}.$\n\n$m=$\n{{{{field-1}}}}'
 else:prompt=f'Find the slope of the tangent to the curve $y={ft}$ at the point where $x={tt}.$'
 # The solution keeps the source stages: derivative (or prior derivative),
 # substitution, term-by-term evaluation, simplification, slope conclusion.
 parts=sp.Add.make_args(d)
 def join(parts):
  out=''
  for z in parts:
   zs=tex(z);out+=zs if not out else ('-'+zs[1:] if zs.startswith('-') else '+'+zs)
  return out
 sub=dt.replace('x',f'({tt})')
 term_values=[z.subs(x,t) for z in parts]
 numeric=join(term_values)
 partial=''
 if sid=='q-342942':
  reciprocal=sp.Rational(1,t*t);partial=r' \\ & ='+join([sum(term_values)-reciprocal,reciprocal])
 intro=f'We have $k(x)={ft}.$' if easy else f'Let $f(x)={ft}.$'
 sol=intro+f' The slope of the tangent at $x={tt}$ is equal to ${name}\\prime({tt}).$ '
 if easy:sol+='The given derivative is\n\n$$\n'+f'k\\prime(x)={dt}.'+'\n$$'
 else:
  # Preserve the reciprocal-to-power rewriting stage of q-1853.
  rewrite=''
  if sid=='q-1853':
   a,b,_=p;rewrite=r' \\ & =\frac{\text{d}}{\text{d}x}('+tex(a*x**4-b*x**3)+r'+x^{-1})'
  if sid=='q-342107':a,b,c,dc,_=p;operative=f'{6*a}x^{{5}}-{b}(4x^{{3}})+{c}(2x)-0'
  elif sid=='q-342937':a,h,_=p;operative=f'-{2*a}x+(-2(x-{h})^{{-3}})'
  elif sid=='q-342942':a,b,c,_=p;operative=f'{a}\\cdot4x^{{3}}-{b}\\cdot3x^{{2}}-{c}\\cdot2x+x^{{-2}}'
  elif sid=='q-1853':a,b,_=p;operative=f'4\\cdot{a}x^{{3}}-3\\cdot{b}x^{{2}}-x^{{-2}}'
  else:operative=dt
  sol+='Computing the derivative, we get\n\n$$\n'+r'\begin{aligned}f\prime(x) & =\frac{\text{d}}{\text{d}x}('+ft+')'+rewrite+(r' \\ & ='+operative if sid!='q-10742' else '')+r' \\ & ='+dt+r'.\end{aligned}'+'\n$$'
 sol+=f'\n\nNow, we evaluate at $x={tt}$ and get\n\n$$\n'+r'\begin{aligned}'+f'{name}\\prime({tt}) & ='+sub+r' \\ & ='+numeric+partial+r' \\ & ='+st+r'.\end{aligned}'+'\n$$'
 if blank and not easy:sol+=f'\n\nTherefore, the slope $m$ of the tangent to the curve at $x={tt}$ is\n\n$$\nm=f\\prime({tt})={st}.\n$$'
 else:sol+=f'\n\nTherefore, the slope of the tangent to the curve is ${st}.$'
 return prompt.replace(r'\prime',r'^{\prime}'),sol.replace(r'\prime',r'^{\prime}')

def generate(difficulty='easy',seed=0,template=None,parameters=None):
 if difficulty not in ('easy','moderate'):raise ValueError('hard unsupported; see capabilities.json')
 rng=random.Random(seed);sid=template or rng.choice([k for k,t in PROFILES.items() if t['difficulty']==difficulty])
 if PROFILES[sid]['difficulty']!=difficulty:raise ValueError('difficulty/template mismatch')
 p=list(parameters) if parameters is not None else rng.choice(candidates(sid))
 if not allowed(sid,p):raise ValueError('outside bounded policy or ambiguous bank/pole')
 fp=fingerprint_params(sid,p);qid=ident(['question',VERSION,sid,fp]);key='selection' if PROFILES[sid]['kind']=='radio' else 'field-1';fid=ident([qid,key])
 values,ci,recipes=bank(sid,p)
 choices=[{':answer/id':ident([fid,str(z)]),':answer/type':':answer.type/math',':answer/value':tex(z) if key=='selection' else str(z)} for z in values]
 problem,solution=render(sid,p)
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+PROFILES[sid]['kind'],':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[ci][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':sid,'profile':sid if recipes else None,'parameters':p,'source_ids':[sid],'domain':'x real; exclude reciprocal poles; target restricted to bounded policy','mathematical_fingerprint':fp,'recipes':recipes,'sympy':sp.__version__}}
def batch(difficulty,count,seed):
 if difficulty not in ('easy','moderate'):raise ValueError('unsupported difficulty')
 if count<1:raise ValueError('positive count required')
 pairs=[(sid,p) for sid,t in PROFILES.items() if t['difficulty']==difficulty for p in candidates(sid)];random.Random(seed).shuffle(pairs);used=set();records=[]
 for i,(sid,p) in enumerate(pairs):
  r=generate(difficulty,seed+i,sid,p);fp=r['generation']['mathematical_fingerprint']
  if fp not in used:records.append(r);used.add(fp)
  if len(records)==count:return records
 raise ValueError('finite bounded family exhausted; shortage explicit')
def markdown(rec):
 q=rec['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+z[':answer/value']+'$' for z in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',default='easy');a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');v=a.parse_args();rs=batch(v.difficulty,v.count,v.seed);print(json.dumps(rs,indent=2) if v.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
