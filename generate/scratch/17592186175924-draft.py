#!/usr/bin/env python3
"""Private frozen, no-write perpendicular-line generator; basis 2275.
Source replay is separate from eligible authored repairs and parameter variants.
All profiles are whole observed banks, transported by explicitly documented recipes.
"""
from __future__ import annotations
import sys
sys.dont_write_bytecode=True
import argparse,copy,hashlib,importlib.util,json,random,re,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().with_suffix('')
def frozen(name):
 spec=importlib.util.spec_from_file_location('private_perp_'+name,HERE/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
fmt=frozen('math_format');parser=frozen('math_parser')
x,y=parser.SYMS['x'],parser.SYMS['y']
KP_ID=17592186175924
KP_UUID='c52fd5dd-780e-5dab-805f-561383873dd4'
TITLE='Finding the Equation of a Line Perpendicular to a Line in Standard Form'
VERSION='perpendicular-coefficient-point-3'
LEVELS=('easy','moderate','hard')
SOURCE=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
INCOMPLETE={'q-214033','q-23633'}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def tex(v):return fmt.normalize_tex(sp.latex(sp.expand(v)))
def eq(a,b,c):return tex(a*x+b*y)+'='+tex(c)
def standard_eq(a,b,c):
 scale=sp.ilcm(*[sp.denom(v) for v in (a,b,c)]);return eq(scale*a,scale*b,scale*c)
def line(t):
 l,r=t.split('=');e=sp.Poly(sp.expand(parser.parse(l)-parser.parse(r)),x,y)
 if e.total_degree()!=1:raise ValueError('not a line')
 return e.coeff_monomial(x),e.coeff_monomial(y),-e.coeff_monomial(1)
def canonical(a,b,c):
 k=a if a else b
 if not k:raise ValueError('degenerate line')
 return tuple(str(sp.cancel(v/k)) for v in (a,b,c))
def printed(prompt):
 if 'perpendicular' not in prompt:raise ValueError('missing requested perpendicular role')
 pts=[tuple(map(int,z)) for z in re.findall(r'\((-?\d+),\s*(-?\d+)\)',prompt)]
 if 'line passing through the points' in prompt:
  (u,v),(w,z)=pts[1:];A=z-v;B=u-w;C=A*u+B*v
 else:
  ref=prompt.split('perpendicular to ',1)[1];ref=ref[ref.index('$')+1:];ref=ref.split('$')[0].rstrip('.?');A,B,C=line(ref)
 return pts[0],(A,B,C),pts[1:]
def original(s):
 q=SOURCES[s];pt,(A,B,C),pts=printed(q[':question/problem']);return {'A':int(A),'B':int(B),'C':int(C),'px':pt[0],'py':pt[1],**({'points':[list(z) for z in pts]} if pts else {})}
def source_level(s):return ('moderate' if s=='q-23633' else 'easy') if s in INCOMPLETE else SOURCES[s][':question/difficulty'][':db/ident'].split('/')[-1]
def raw_replay(s):
 """Every raw attribute preserved, missing keys remain missing; never serving eligible."""
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':copy.deepcopy(SOURCES[s]),'generation':{'source_id':s,'source_basis':2275,'origin':'raw MA evidence','eligible':False,'missing':(['key','solution']+(['bank'] if s=='q-214033' else [])) if s in INCOMPLETE else []}}
def profile(s,p):
 """Per-source whole bank. A/B multipliers and incidence residual reproduce all options.
 For old perpendicular normal (a0,b0)=(-B0,A0), option (oa,ob,oc):
 new normal=(oa*a/a0,ob*b/b0), new constant=na*px+nb*py+(oc-oa*px0-ob*py0).
 Residual recipe interpretation is unresolved, not a claimed learner error.
 """
 old=SOURCES[s][':question/answer-fields'][0];a,b=-sp.Integer(p['B']),sp.Integer(p['A']);u,v=p['px'],p['py'];base=original(s);a0,b0=-base['B'],base['A'];out=[]
 for o in old.get(':answer-field/choices',[]):
  if old[':answer-field/type'][':db/ident'].endswith('/blank'):return [tex(sp.Rational(p['B'],p['A'])*x+v-sp.Rational(p['B'],p['A'])*u)]
  oa,ob,oc=line(o[':answer/value']);na=oa*a/a0;nb=ob*b/b0;nc=na*u+nb*v+oc-oa*base['px']-ob*base['py'];out.append(standard_eq(na,nb,nc))
 return out or [tex(sp.Rational(p['B'],p['A'])*x+v-sp.Rational(p['B'],p['A'])*u)]
def block(rows):return '$$\n\\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def solution(s,p):
 A,B,C=map(sp.Integer,(p['A'],p['B'],p['C']));u,v=p['px'],p['py'];m1=-A/B;m=B/A;b=v-m*u;d=m.q;n=m.p
 if 'points' in p:
  (u1,v1),(u2,v2)=p['points'];rows=[r'm_1 &= \frac{y_2-y_1}{x_2-x_1}',rf'&= \frac{{{v2}-({v1})}}{{{u2}-({u1})}}']
  if s=='q-103449':
   subtract=lambda a,b:str(a)+('+'+str(-b) if b<0 else '-'+str(b))
   rows.append(rf'&= \frac{{{subtract(v2,v1)}}}{{{subtract(u2,u1)}}}')
  else:rows.append(rf'&= \frac{{{v2-v1}}}{{{u2-u1}}}')
  rows.append(f'&= {tex(m1)}')
  start=f"Perpendicular lines have slopes which are negative reciprocals of each other.\n\nFirst, let's find the slope $m_1$ of the line passing through the points $({u1},{v1})$ and $({u2},{v2}):$\n\n"+block(rows)
  mid=f"Since we want a perpendicular line, the slope $m$ of the line we're trying to find must satisfy\n\n$$\nm\\cdot ({tex(m1)})=-1\\,\\Rightarrow\\,m={tex(m)}.\n$$\n\nWe know that the line passes through the point $({u},{v}).$ Using point-slope form and simplifying, we obtain the equation of the line:"
 else:
  rows=[eq(A,B,C).replace('=',' &=')]
  if s!='q-237230' or B!=1:rows.append(tex(B*y)+' &= '+tex(-A*x+C))
  rows.append('y &= '+tex(m1*x+C/B))
  start=f'First, we write the equation ${eq(A,B,C)}$ in its slope-intercept form as follows:\n\n'+block(rows)
  mid=f'Since perpendicular lines have slopes that are negative reciprocals of each other, the slope of the new line should be the negative reciprocal of the slope of the given line $y={tex(m1*x+C/B)}.$ The given line has a slope of ${tex(m1)},$ so our perpendicular line must have a slope of ${tex(m)}.$\n\nOur perpendicular line must have the slope $m={tex(m)}$ and pass through the point $(x_1,y_1)=({u},{v}).$ Using point-slope form and simplifying, we obtain the equation of the line'+(' in slope-intercept form:' if not SOURCES[s][':question/answer-fields'][0][':answer-field/type'][':db/ident'].endswith('/radio') else ':')
 rows=[r'y-y_1 &= m(x-x_1)',f'y-({v}) &= {tex(m)}(x-({u}))']
 if s in ('q-23631','q-237230','q-103449'):rows.append(f'y-({v}) &= {tex(m)}(x'+('+'+str(-u) if u<0 else '-'+str(u))+')')
 if s=='q-252524':rows.extend([f'{d}(y-({v})) &= {n}(x-({u}))',tex(d*y-d*v)+' &= '+tex(n*x-n*u),tex(d*y)+' &= '+tex(n*x+d*v-n*u),'y &= '+tex(m*x+b)])
 elif s=='q-237231' and v==0:rows.extend([f'y &= {tex(m)}(x-({u}))','y &= '+tex(m*x+b)])
 else:rows.extend([f'y-({v}) &= '+tex(m*(x-u)),'y &= '+tex(m*x+b)])
 if s=='q-23631':rows += [tex(d*y)+' &= '+tex(n*x+d*b),eq(-n,d,d*b).replace('=',' &=')]
 result=start+'\n\n'+mid+'\n\n'+block(rows)
 if 'points' in p:
  result+=f'\n\nHowever, we want to write the equation in standard form. So, we will bring the $x$ term to the left-hand side and multiply both sides of the equation by ${d}:$\n\n'+block(['y &= '+tex(m*x+b),tex(-m*x+y)+' &= '+tex(b),f'{d}\\cdot ({tex(-m*x+y)}) &= {d}\\cdot ({tex(b)})',eq(-n,d,d*b).replace('=',' &=')])
 return result

def render_prompt(s,p):
 if s=='q-214033':return fmt.normalize_prose(f"What is the equation of the line that passes through the point $({p['px']},{p['py']})$ and is perpendicular to ${eq(p['A'],p['B'],p['C'])}?$\n\n$y=$\n{{{{field-1}}}}")
 q=SOURCES[s][':question/problem'];old=original(s);pairs=re.findall(r'\((-?\d+),\s*(-?\d+)\)',q)
 if 'points' in p:
  coords=[(p['px'],p['py']),*p['points']];i=iter(coords);q=re.sub(r'\((-?\d+),\s*(-?\d+)\)',lambda _: '('+','.join(map(str,next(i)))+')',q)
 else:
  q=re.sub(r'\((-?\d+),\s*(-?\d+)\)',f"({p['px']},{p['py']})",q,count=1)
  q=re.sub(r'(perpendicular to \$)[^$]+',lambda m:m[1]+eq(p['A'],p['B'],p['C'])+('?' if '?$' in q else '.'),q)
 return fmt.normalize_prose(q)

def validate_parameters(s,p):
 base=original(s)
 if set(p)!=set(base) or any(type(p[k])!=int for k in ('A','B','C','px','py')):raise ValueError('invalid parameter contract')
 if p['A']==0 or p['B']==0:raise ValueError('source scope is finite nonzero slopes; axis cases require a different solution branch absent from evidence')
 if max(abs(p[k]) for k in ('A','B','C','px','py'))>100:raise ValueError('outside integer domain')
 if 'points' in p:
  pts=p['points'];
  if len(pts)!=2 or any(len(z)!=2 or any(type(v)!=int for v in z) for z in pts):raise ValueError('two integer reference points required')
  (u,v),(w,z)=pts
  if u==w or v==z or (p['A'],p['B'],p['C'])!=(z-v,u-w,(z-v)*u+(u-w)*v):raise ValueError('stale two-point coefficients')

def sample(s,rng):
 p=original(s);p['px']=rng.randint(-9,9);p['py']=rng.randint(-9,9)
 if 'points' in p:
  u,v=rng.randint(-5,5),rng.randint(-5,5);dx,dy=rng.choice([i for i in range(-7,8) if i]),rng.choice([i for i in range(-7,8) if i]);p.update(A=dy,B=-dx,C=dy*u-dx*v,points=[[u,v],[u+dx,v+dy]])
 else:p.update(A=rng.choice([i for i in range(-7,8) if i]),B=rng.choice([i for i in range(-7,8) if i]),C=rng.randint(-12,12))
 return p

@fmt.checked_math_content
def generate(level,seed=0,template=None,parameters=None):
 if type(seed)is not int:raise ValueError('builtin integer seed required')
 if level not in LEVELS:raise ValueError('invalid difficulty')
 rng=random.Random(seed);available=[s for s in SOURCES if source_level(s)==('moderate' if level=='hard' else level)];s=template or rng.choice(available)
 if s not in available:raise ValueError('template/level mismatch')
 for attempt in range(1000):
  p=copy.deepcopy(parameters) if parameters is not None else sample(s,rng);validate_parameters(s,p);values=profile(s,p);old=SOURCES[s];of=old[':question/answer-fields'][0];kind=of[':answer-field/type'][':db/ident'];m=sp.Rational(p['B'],p['A']);b=p['py']-m*p['px']
  canonical_bank=[canonical(*line(v)) if kind.endswith('/radio') else str(parser.parse(v)) for v in values]
  correct=[i for i,v in enumerate(values) if (canonical(*line(v))==canonical(-m,1,b) if kind.endswith('/radio') else sp.simplify(parser.parse(v)-(m*x+b))==0)]
  if len(set(canonical_bank))==len(values) and len(correct)==1:break
  if parameters is not None:raise ValueError('whole-bank collision')
 else:raise ValueError('no eligible full bank')
 replay=p==original(s) and s not in INCOMPLETE
 prompt=fmt.normalize_prose(old[':question/problem']) if replay else render_prompt(s,p)
 sol=fmt.normalize_prose(old[':question/worked-solution']) if replay else fmt.normalize_prose(solution(s,p))
 if replay:values=[fmt.normalize_tex(a[':answer/value']) for a in of[':answer-field/choices']]
 semantic=digest([canonical(p['A'],p['B'],0),p['px'],p['py'],'perpendicular',kind,'real coordinate plane'])
 contract=[prompt,sol,kind,of[':answer-field/key'],sorted(values),values[correct[0]]];qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'content:'+digest(contract)));fid=str(uuid.uuid5(uuid.UUID(qid),'field:'+of[':answer-field/key']))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':of[':answer-field/key'],':answer-field/type':kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct[0]][':answer/id']]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':s,'parameters':p,'bank_profile':s if kind.endswith('/radio') else None,'source_id':s,'source_basis':2275,'eligible':True,'mathematical_fingerprint':semantic,'content_hash':digest(contract),'domain':'real coordinate plane; source finite nonzero reference slopes; integer coefficients/points','origin':'normalized source replay' if replay else ('authored completion of incomplete raw source' if s in INCOMPLETE else 'authored parameter variation of source stages'),'difficulty_origin':'authored hard at same moderate workload; no hard source' if level=='hard' else ('authored inferred level for incomplete source' if s in INCOMPLETE else 'observed level'),'dependencies':{'sympy':sp.__version__}}}

def batch(level,count,seed=0):
 if type(seed)is not int:raise ValueError('builtin integer seed required')
 if type(count)is not int or count<1:raise ValueError('positive builtin integer count required')
 if level not in LEVELS:raise ValueError('invalid difficulty')
 out=[];seen=set()
 for i in range(count*50):
  r=generate(level,seed+i);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
  if len(out)==count:return out
 raise ValueError('unable to produce requested distinct tasks')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=('all',*LEVELS),default='all');a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');o=a.parse_args();rs=[r for level in (LEVELS if o.difficulty=='all' else (o.difficulty,)) for r in batch(level,o.count,o.seed)];print(json.dumps(rs,indent=2) if o.format=='json' else '\n\n'.join(map(markdown,rs)))
