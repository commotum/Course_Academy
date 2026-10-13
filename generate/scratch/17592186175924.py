#!/usr/bin/env python3
"""Bounded perpendicular-line generator. No database writes.

Each source is a separate prompt/solution and complete-bank profile. Sampling
translates the target point vertically by an integer t in [-8,8], preserving
all observed directions, signed coefficients, zero coordinates and field shapes.
Radio banks translate each entire line by the same t; no inferred mistake labels.
Hard is unsupported by this bounded package. Seed/order alone is not novelty.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid,sys,os
from pathlib import Path
try: import sympy as sp
except ImportError:
 runtime=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 if __name__=='__main__' and runtime.exists():os.execv(str(runtime),[str(runtime),__file__,*sys.argv[1:]])
 raise
KP_ID=17592186175924
KP_UUID='c52fd5dd-780e-5dab-805f-561383873dd4'
TITLE='Finding the Equation of a Line Perpendicular to a Line in Standard Form'
VERSION='perpendicular-vertical-translation-1'
HERE=Path(__file__).resolve().with_suffix('')
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
x,y=sp.symbols('x y',real=True)
DATA={
'q-214033':('easy',(1,-5),(1,3,12),None),
'q-23633':('moderate',(-3,-2),None,((2,6),(-3,1))),
'q-103449':('moderate',(-2,2),None,((1,-1),(4,1))),
'q-23631':('easy',(-1,1),(2,-3,-5),None),
'q-237230':('easy',(-4,3),(5,1,2),None),
'q-237231':('easy',(-7,0),(1,-6,-3),None),
'q-237232':('easy',(1,1),(4,-3,7),None),
'q-252524':('moderate',(3,4),None,((2,2),(5,8))),
'q-72571':('moderate',(5,1),None,((1,5),(-3,-1)))}
def sources():return {q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def expr(t):
 t=t.replace(' ','');t=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'(\1/\2)',t)
 t=re.sub(r'(\d|\))([xy])',r'\1*\2',t)
 return sp.expand(sp.sympify(t,locals={'x':x,'y':y}))
def line(t):
 l,r=t.split('=');e=sp.expand(expr(l)-expr(r));return e.coeff(x),e.coeff(y),-e.subs({x:0,y:0})
def direction(s):
 _,_,ab,pts=DATA[s]
 return -sp.Rational(ab[0],ab[1]) if ab else sp.Rational(pts[1][1]-pts[0][1],pts[1][0]-pts[0][0])
def tex(e):return sp.latex(sp.expand(e)).replace('- ','-')
def eq(a,b,c):return tex(a*x+b*y)+'='+tex(c)
def fingerprint(q):
 p=q[':question/problem'];pt=re.search(r'point \$\((-?\d+),\s*(-?\d+)\)\$',p)
 if not pt:raise ValueError('Unrecognized target point')
 coords=(int(pt[1]),int(pt[2]))
 if 'line passing through the points' in p:
  pairs=re.findall(r'\((-?\d+),\s*(-?\d+)\)',p);a,b=map(lambda z:tuple(map(int,z)),pairs[-2:]);m=sp.Rational(b[1]-a[1],b[0]-a[0])
 else:
  ref=p.split('perpendicular to ',1)[1].strip('$').split('$',1)[0].rstrip('.?');A,B,C=line(ref);m=-A/B
 return digest([str(m),*coords])
def solution(s,t):
 old=sources()[s]
 if t==0 and old.get(':question/worked-solution'):return old[':question/worked-solution']
 _,(u,v),ab,pts=DATA[s];v+=t;m1=direction(s);m=-1/m1;b=v-m*u
 if ab:
  A,B,C=ab;start=f'First, we write the equation ${eq(A,B,C)}$ in its slope-intercept form as follows:\n\n$$\n\\begin{{aligned}}{eq(A,B,C)} \\\\ {tex(B*y)} &= {tex(-A*x+C)} \\\\ y &= {tex(m1*x+sp.Rational(C,B))}\\end{{aligned}}\n$$'
 else:
  (u1,v1),(u2,v2)=pts
  start=f"Perpendicular lines have slopes which are negative reciprocals of each other.\n\nFirst, let's find the slope ${{m}}_{{1}}$ of the line passing through the points $({u1},{v1})$ and $({u2},{v2}):$\n\n$$\n\\begin{{aligned}}m_1 &= \\frac{{y_2-y_1}}{{x_2-x_1}} \\\\ &= \\frac{{{v2}-({v1})}}{{{u2}-({u1})}} \\\\ &= \\frac{{{v2-v1}}}{{{u2-u1}}} \\\\ &= {tex(m1)}\\end{{aligned}}\n$$"
 mid=f'\n\nSince perpendicular lines have slopes that are negative reciprocals of each other, the slope of the new line should be the negative reciprocal of the slope of the given line. The given line has a slope of ${tex(m1)},$ so our perpendicular line must have a slope of ${tex(m)}.$\n\nOur perpendicular line must have the slope $m={tex(m)}$ and pass through the point $(x_1,y_1)=({u},{v}).$ Using point-slope form and simplifying, we obtain the equation of the line in slope-intercept form:\n\n$$\n\\begin{{aligned}}y-y_1 &= m(x-x_1) \\\\ y-({v}) &= {tex(m)}(x-({u})) \\\\ y-({v}) &= {tex(m*(x-u))} \\\\ y &= {tex(m*x+b)}\\end{{aligned}}\n$$'
 if old[':question/answer-fields'][0][':answer-field/type'][':db/ident'].endswith('/radio'):
  A=-m.p;B=m.q;C=B*b
  mid+=f'\n\nHowever, we want to write the equation in standard form. So, we will bring the $x$ term to the left-hand side and multiply both sides of the equation by ${B}:$\n\n$$\n\\begin{{aligned}}y &= {tex(m*x+b)} \\\\ {tex(-m*x+y)} &= {tex(b)} \\\\ {B}({tex(-m*x+y)}) &= {B}({tex(b)}) \\\\ {tex(A*x+B*y)} &= {tex(C)}\\end{{aligned}}\n$$'
 return start+mid

def generate(level,seed=0,template=None,parameters=None):
 if level not in ('easy','moderate'):raise ValueError('Unsupported hard: no source evidence or validated hard template')
 s=template or random.Random(seed).choice([s for s,d in DATA.items() if d[0]==level]);p=parameters or {'t':random.Random(seed).randint(-8,8)};t=p['t']
 if s not in DATA or DATA[s][0]!=level or type(t)!=int or not -8<=t<=8 or set(p)!={'t'}:raise ValueError('Outside bounded template parameters')
 old=sources()[s];f=old[':question/answer-fields'][0];kind=f[':answer-field/type'][':db/ident'];u,v=DATA[s][1];m=-1/direction(s);b=v+t-m*u
 point=re.search(r'point \$\((-?\d+),\s*(-?\d+)\)\$',old[':question/problem'])
 prompt=old[':question/problem'][:point.start()]+f'point $({u},{v+t})$'+old[':question/problem'][point.end():]
 if t==0:prompt=old[':question/problem']
 values=[]
 if kind.endswith('/blank'):values=[f[':answer-field/choices'][0][':answer/value'] if t==0 and f.get(':answer-field/choices') else tex(m*x+b)]
 else:
  for a in f[':answer-field/choices']:
   A,B,C=line(a[':answer/value']);values.append(a[':answer/value'] if t==0 else eq(A,B,C+B*t))
 correct=[i for i,val in enumerate(values) if (sp.simplify(expr(val)-(m*x+b))==0 if kind.endswith('/blank') else (lambda abc: abc[1]!=0 and -abc[0]/abc[1]==m and abc[0]*u+abc[1]*(v+t)==abc[2])(line(val)))]
 if len(correct)!=1:raise ValueError('Ambiguous bank')
 fp=digest([str(direction(s)),u,v+t]);qid=str(uuid.uuid5(uuid.UUID(KP_UUID),'task:'+fp));fid=str(uuid.uuid5(uuid.UUID(qid),'field'))
 answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),'value:'+val)),':answer/type':':answer.type/math',':answer/value':val} for val in values]
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution(s,t),':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':f[':answer-field/key'],':answer-field/type':kind,':answer-field/correct':[':answer/id',answers[correct[0]][':answer/id']],':answer-field/choices':answers}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':s,'parameters':p,'source_question':s,'source_basis':1910,'bank_profile':s if kind.endswith('/radio') else None,'mathematical_fingerprint':fp,'domain':'real x,y; nonzero finite reference slope; vertical target translation -8..8','dependencies':{'sympy':sp.__version__},'solution_origin':'source exact at replay where supplied; source sequence with explicit streamlined expansion for variants','difficulty_origin':'observed source levels; unrated q-214033 easy and q-23633 moderate inferred from identical task workload'}}
def candidates(level):
 for s,d in DATA.items():
  if d[0]==level:
   for t in range(-8,9):yield s,{'t':t}
def batch(level,count,seed):
 ps=list(candidates(level));random.Random(seed).shuffle(ps);out=[];seen=set()
 for s,p in ps:
  r=generate(level,seed,s,p);fp=r['generation']['mathematical_fingerprint']
  if fp not in seen:out.append(r);seen.add(fp)
  if len(out)==count:return out
 raise ValueError(f'Finite capacity {len(out)}; requested {count}')
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',required=True);a.add_argument('--count',type=int,default=1);a.add_argument('--seed',type=int,default=0);a.add_argument('--format',choices=['json','markdown'],default='json');o=a.parse_args();rs=batch(o.difficulty,o.count,o.seed);print(json.dumps(rs,indent=2) if o.format=='json' else '\n\n'.join(map(markdown,rs)))
