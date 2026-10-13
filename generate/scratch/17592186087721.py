#!/usr/bin/env python3
"""Parametric graph recognition; math/basis 1356. Local review only, no DB writes.

Observed templates reconstruct both tables from exact mathematics, using source
prose masks. Observed banks preserve all five original assets (including opaque
residual distractors); their eligibility is deliberately limited to source
parameters because those rasters do not establish a general wrong formula.
Default banks are separately authored complete coordinate-operation banks.
Moderate and hard share five rows and bounded factored quadratics; only graph
recognition differs. See classification, extraction and validation beside script.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
sys.dont_write_bytecode=True
import sympy as sp
HERE=Path(__file__).resolve().with_suffix('')
KP_ID=17592186087721
KP_UUID='e0dc11d5-8eda-52b1-b7b1-42b481813ff4'
TITLE='Graphing a Curve Defined Parametrically'
VERSION='parametric-graphs-1'
T=sp.Symbol('t',real=True);U=sp.Symbol('u',real=True);X,Y=sp.symbols('x y')
ASSET_ROOT=Path('/media/jake/SSD/EDB/math')
SOURCE=json.loads((HERE/'source.json').read_text())
SPECS=json.loads((HERE/'templates.json').read_text())

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy/'+s))
def expr(s):return sp.sympify(s,locals={'t':T,'pi':sp.pi},rational=True)
def latex(v):return sp.latex(sp.simplify(v)).replace(' ','')
def number(v,decimal=False):
 v=sp.simplify(v)
 if decimal:
  if v.is_Integer:return str(v)
  if v.is_Rational and (100*v).is_Integer:return str(float(v)).rstrip('0').rstrip('.')
  return f'{float(v):.2f}'
 return latex(v)
def table(label,ts,xs,ys):
 rows=[[f'**${label}$**']+['$'+s+'$' for s in ts],['---']*(len(ts)+1),['$x$']+['$'+s+'$' for s in xs],['$y$']+['$'+s+'$' for s in ys]]
 return '\n'.join('| '+' | '.join(r)+' |' for r in rows)

def shape(x,y,lo,hi,kind='poly',closed=True):
 return {'x':str(x),'y':str(y),'lo':str(lo),'hi':str(hi),'kind':kind,'closed':closed and kind!='rational','direction_assessed':False}

def geometry_key(s):
 """Complete supported simple arcs: implicit curve + endpoint pair/domain branch.
 No inferred Cartesian equation is displayed or required of the learner.
 """
 x,y=expr(s['x']),expr(s['y']);lo,hi=expr(s['lo']),expr(s['hi'])
 kind=s['kind']
 if kind=='ellipse':
  # All supported trig curves are axis-aligned full ellipses. Derive coefficients
  # from actual x/y evaluations, avoiding parameter spelling identity.
  h=sp.simplify((x.subs(T,0)+x.subs(T,sp.pi))/2);a=sp.simplify(x.subs(T,0)-h)
  k=sp.simplify((y.subs(T,sp.pi/2)+y.subs(T,3*sp.pi/2))/2);b=sp.simplify(y.subs(T,sp.pi/2)-k)
  if a==0 or b==0:raise ValueError('degenerate ellipse')
  poly=sp.Poly(b*b*(X-h)**2+a*a*(Y-k)**2-a*a*b*b,X,Y).monic().as_expr()
  return ('ellipse',str(poly))
 if kind=='root':x=x.subs(T,U**2).subs(sp.Abs(U),U);y=y.subs(T,U**2).subs(sp.Abs(U),U);v=U;lo=sp.sqrt(lo);hi=sp.sqrt(hi)
 else:v=T
 nx,dx=sp.fraction(sp.together(X-x));ny,dy=sp.fraction(sp.together(Y-y))
 poly=sp.Poly(sp.resultant(nx,ny,v),X,Y).sqf_part().monic().as_expr()
 if kind=='rational':
  # Only the positive-t branch is supported; coordinates of a known interior
  # point distinguish branches of the same implicit hyperbola.
  pp=sp.Poly(poly,X,Y);h=-pp.coeff_monomial(Y)/pp.coeff_monomial(X*Y);k=-pp.coeff_monomial(X)/pp.coeff_monomial(X*Y)
  branch=(str(sp.sign(x.subs(v,1)-h)),str(sp.sign(y.subs(v,1)-k)))
  return ('rational',str(poly),branch)
 ends=sorted((str(sp.simplify(x.subs(v,z))),str(sp.simplify(y.subs(v,z)))) for z in (lo,hi))
 return ('arc',str(poly),tuple(ends),s['closed'])

def valid_bank(bank):
 keys=[geometry_key(s) for s in bank]
 if len(set(keys))!=5:raise ValueError('equivalent graphs: reject whole bank')
 return keys

def build(level,template,p,profile):
 if template in SPECS:
  if level!='easy':raise ValueError('observed families are easy')
  spec=SPECS[template]
  if set(p)!={'m','n','h','k'} or any(type(v) is not int for v in p.values()):raise ValueError('easy parameters are m,n,h,k')
  if p['m'] not in (1,2) or p['n'] not in (1,2) or abs(p['h'])>2 or abs(p['k'])>2:raise ValueError('easy bounds')
  bx,by=expr(spec['x']),expr(spec['y']);x=p['m']*bx+p['h'];y=p['n']*by+p['k']
  lo,hi=expr(spec['lo']),expr(spec['hi']);kind=spec['kind'];ts=list(map(expr,spec['ts']))
  original=p=={'m':1,'n':1,'h':0,'k':0}
  xt=spec['x_tex'] if original else latex(x);yt=spec['y_tex'] if original else latex(y)
  if spec['label'].startswith('\\theta') and not original:
   xt=latex(x.subs(T,sp.Symbol('theta')));yt=latex(y.subs(T,sp.Symbol('theta')))
  prompt=spec['prompt_mask'].replace('{X}',xt).replace('{Y}',yt)
  xs=[number(x.subs(T,t),spec['decimal']) for t in ts];ys=[number(y.subs(T,t),spec['decimal']) for t in ts]
  tb1=table(spec['label'],spec['ts_tex'],xs,['']*len(ts));tb2=table(spec['label'],spec['ts_tex'],xs,ys)
  sol=spec['solution_mask'].replace('{X}',xt).replace('{Y}',yt).replace('{TABLE1}',tb1).replace('{TABLE2}',tb2)
  if profile.startswith('observed:'):
   if profile!='observed:'+template or not original:raise ValueError('residual source bank is eligible only at its observed parameters')
   bank=None;paths=[str(ASSET_ROOT/a) for a in spec['choice_assets']];correct=spec['correct_index'];solution_path=str(ASSET_ROOT/spec['solution_asset'])
  elif profile=='authored-coordinate':
   cx=sp.expand(x).as_independent(T,as_Add=True)[0];cy=sp.expand(y).as_independent(T,as_Add=True)[0]
   if cx==0 or cy==0:raise ValueError('nonzero actual coordinate constants required for omitted-origin bank')
   bank=[shape(x,y,lo,hi,kind),shape(x-cx,y,lo,hi,kind),shape(x,y-cy,lo,hi,kind),shape(x-2*cx,y-2*cy,lo,hi,kind),shape(y,x,lo,hi,kind)]
   # Swapped roots still polynomialize correctly; swapped ellipses use explicit
   # reconstruction rather than geometry_key's cosine/sine orientation.
   if kind=='ellipse':
    bank[-1]=shape(p['n']*sp.cos(T)*expr(spec['b'])+p['k'],p['m']*sp.sin(T)*expr(spec['a'])+p['h'],lo,hi,kind)
   valid_bank(bank);correct=0;paths,solution_path=render_plots(bank,ts)
   # Normal authored output removes empty display artifacts from capture.
   sol=re.sub(r'\n\n\$\$\n\n\$\$','',sol)
  else:raise ValueError('unsupported profile')
  sol=sol.replace('{ASSET}',solution_path)
  data={'x':str(x),'y':str(y),'ts':[str(t) for t in ts],'xs':xs,'ys':ys,'correct_shape':shape(x,y,lo,hi,kind),'source_id':spec['source_id']}
 else:
  if template!='factored-pair' or level not in ('moderate','hard'):raise ValueError('unsupported template/level')
  if set(p)!={'a','b','h','k'} or any(type(v) is not int for v in p.values()) or p['a'] not in (1,2,3) or p['b'] not in (1,2,3) or p['a']==p['b'] or p['h'] not in (-2,-1,1,2) or p['k'] not in (-2,-1,1,2):raise ValueError('authored bounds require a,b in1..3 unequal and nonzero shifts ±1,±2')
  expected='authored-sign-shift' if level=='moderate' else 'authored-domain-clips'
  if profile!=expected:raise ValueError('level has one fixed complete profile')
  x=T*(T-p['a'])+p['h'];y=T*(p['b']-T)+p['k'];lo,hi=-2,2;ts=list(map(sp.Integer,range(-2,3)))
  xt=f't(t-{p["a"]})'+('+' if p['h']>0 else '')+str(p['h']);yt=f't({p["b"]}-t)'+('+' if p['k']>0 else '')+str(p['k'])
  prompt='Determine the graph of the following parametrically defined curve:\n\n$$\nx='+xt+r',\,y='+yt+r',\,-2\le t\le 2'+'\n$$'
  bank=[shape(x,y,lo,hi)]
  if level=='moderate':bank.extend([shape(-x,y,lo,hi),shape(x,-y,lo,hi),shape(x-p['h'],y,lo,hi),shape(x,y-p['k'],lo,hi)])
  else:bank.extend([shape(x,y,a,b) for a,b in [(-2,1),(-1,2),(-2,3),(-3,2)]])
  valid_bank(bank);paths,solution_path=render_plots(bank,ts);correct=0
  xs=[number(x.subs(T,t)) for t in ts];ys=[number(y.subs(T,t)) for t in ts]
  sol='We need to create a table of values and then sketch the curve. First, we work out the $x$-values using the formula $x='+xt+'.$ This gives\n\n'+table('t',[str(t) for t in ts],xs,['']*5)+'\n\nNow, we work out the $y$ values using $y='+yt+'.$ This gives\n\n'+table('t',[str(t) for t in ts],xs,ys)+'\n\nPlotting these points, we obtain the following curve:\n\n![]('+solution_path+')'
  data={'x':str(x),'y':str(y),'ts':[str(t) for t in ts],'xs':xs,'ys':ys,'correct_shape':bank[0],'source_id':None}
 return prompt,sol,paths,correct,bank,data

def render_plots(bank,ts):
 """One instance drives all five plots and solution; unique input + atomic output.
 Renderer uses cached Matplotlib when primary Python lacks the dependency.
 """
 key=digest({'version':VERSION,'bank':bank,'ts':list(map(str,ts))})
 out=HERE/'assets'/key;out.mkdir(parents=True,exist_ok=True)
 expected=[out/f'choice-{i}.png' for i in range(5)]+[out/'solution.png']
 if not all(f.exists() and f.with_suffix('.json').exists() for f in expected):
  fd,name=tempfile.mkstemp(prefix='render-',suffix='.json',dir=HERE)
  try:
   with os.fdopen(fd,'w') as f:json.dump({'bank':bank,'ts':list(map(str,ts)),'output_dir':str(out)},f)
   subprocess.run([str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),str(HERE/'render.py'),name],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  finally:Path(name).unlink(missing_ok=True)
 return list(map(str,expected[:5])),str(expected[-1])

# Easy: observed source families; normal practice uses authored coordinate banks.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: ten substitutions and coordinate/sign/shift recognition.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard: ten substitutions and comparison of two endpoint pairs across four clips.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('invalid difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio image field only')
 rng=random.Random(seed)
 if profile and profile.startswith('observed:'):
  template=template or profile.split(':',1)[1]
  parameters=parameters if parameters is not None else {'m':1,'n':1,'h':0,'k':0}
 profile=profile or {'easy':'authored-coordinate','moderate':'authored-sign-shift','hard':'authored-domain-clips'}[level]
 for attempt in range(100):
  tmpl=template or (rng.choice(list(SPECS)) if level=='easy' else 'factored-pair')
  p=dict(parameters) if parameters is not None else ({'m':rng.choice([1,2]),'n':rng.choice([1,2]),'h':rng.choice([-2,-1,1,2]),'k':rng.choice([-2,-1,1,2])} if level=='easy' else {'a':rng.randint(1,3),'b':rng.randint(1,3),'h':rng.choice([-2,-1,1,2]),'k':rng.choice([-2,-1,1,2])})
  try:prompt,sol,paths,correct,bank,data=build(level,tmpl,p,profile);break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('no valid complete bank in100 attempts')
 content=digest({'version':VERSION,'prompt':prompt,'solution':sol,'bank':paths,'profile':profile,'parameters':p})
 qid=uid(content);fid=uid(content+'/selection')
 choices=[{':answer/id':uid(fid+'/'+str(i)),':answer/type':':answer.type/image',':answer/value':path} for i,path in enumerate(paths)]
 rng.shuffle(choices)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+'/'+str(correct))]}
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[field]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'seed':seed,'template':tmpl,'parameters':p,'bank_profile':profile,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'content_fingerprint':content,'mathematical_fingerprint':digest(geometry_key(data['correct_shape'])),'mathematical_dedup':'complete locus and domain; ignores parameter spelling, bank, profile and layout; traversal unassessed','plots':bank,'derived':data}}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 if a.format=='json':print(json.dumps(records,indent=2))
 else:
  for r in records:
   q=r['question'];print(q[':question/problem']);print('\n');
   for answer in q[':question/answer-fields'][0][':answer-field/choices']:print('![]('+answer[':answer/value']+')\n')
   print(q[':question/worked-solution']);print('\n')
if __name__=='__main__':main()
