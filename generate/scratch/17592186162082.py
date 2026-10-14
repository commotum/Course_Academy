#!/usr/bin/env python3
"""Piecewise unity arc length. Basis 2275; local review only, no EDB writes.
Six faithful empirical banks are public explicit profiles. Default banks are
separately authored complete operations. Hard is an authored rational-bookkeeping
policy within existing geometry and the same length-sum method, not a new branch.
Plot renderer runs per-call in a child process using a unique temporary directory.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as s
KP=17592186162082; TITLE='Calculating Line Integrals Over Piecewise-Smooth Curves'
VERSION='piecewise-unity-2'; ROOT=Path(__file__).with_suffix(''); ROOT.mkdir(exist_ok=True)
SOURCE=Path(__file__).resolve().parents[1]/'runs/current/refresh-2026-10-14/sources'/f'{KP}.json'
SOURCE_DATA=json.loads(SOURCE.read_text()); SOURCE_Q={q[':question/math-academy-id']:q for q in SOURCE_DATA['record'][':knowledge-point/questions']}
TEMPLATES={'semi':('easy','q-122481'),'three_quarter':('easy','q-122843'),'quarter_closed':('moderate','q-122484'),'three_segments':('moderate','q-122828'),'two_segments':('moderate','q-122845'),'quarter_open':('moderate','q-122850')}
PROFILES={v[1]:k for k,v in TEMPLATES.items()} | {'authored_arc':None,'authored_segments':None}
def tex(x):return s.latex(s.sympify(x)).replace('\\left','').replace('\\right','')
def I(part='C'):return r'{\int }_{'+(part if part=='C' else '{C}_{'+str(part)+'}')+r'}\,\text{d}s'
def equation(body):return '\n\n$$\n'+body+'\n$$'
def canonical(x):return str(s.simplify(x))
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'piecewise/'+x))
def geometry(t,p):
 r=p.get('r'); zero=s.Integer(0)
 if t=='semi':return {'center':[0,1],'arc':[r,0,s.pi],'points':[[-r,1],[r,1]],'ticks':{'x':[-r,r],'y':[1,1+r]},'endpoints':False}
 if t=='three_quarter':return {'center':[0,0],'arc':[r,0,3*s.pi/2],'points':[[0,-r],[r,-r]],'ticks':{'x':[-r,r],'y':[-r,r]},'endpoints':True}
 if t=='quarter_closed':return {'center':[0,0],'arc':[r,0,s.pi/2],'points':[[0,r],[r,0]],'ticks':{'x':[r],'y':[r]},'endpoints':False}
 if t=='quarter_open':return {'center':[0,0],'arc':[r,-s.pi/2,0],'points':[[r,0],[0,r]],'ticks':{'x':[r],'y':[-r,r]},'endpoints':True}
 if t=='three_segments':
  a,b=p['a'],p['b'];return {'points':[[0,0],[0,a],[b,0],[b,a]],'ticks':{'x':[b],'y':[a]},'endpoints':True}
 a,b,h=p['a'],p['b'],p['h'];return {'points':[[-a,0],[0,h],[b,0]],'ticks':{'x':[-a,b],'y':[h]},'endpoints':True}
def lengths(t,p):
 if 'r' in p:
  r=p['r'];return [(s.pi*r if t=='semi' else 3*s.pi*r/2 if t=='three_quarter' else s.pi*r/2),(2*r if t=='semi' else r if t=='three_quarter' else r*s.sqrt(2))]
 if t=='three_segments':return [p['a'],s.sqrt(p['a']**2+p['b']**2),p['a']]
 return [s.sqrt(p['a']**2+p['h']**2),s.sqrt(p['b']**2+p['h']**2)]
def guard(level,t,p):
 expected={'r'} if t in ('semi','three_quarter','quarter_closed','quarter_open') else {'a','b'} if t=='three_segments' else {'a','b','h'}
 if set(p)!=expected:raise ValueError('Unexpected or missing parameter slots')
 if any(not x.is_Rational or not 0<x<=12 or x.q>3 for x in p.values()):raise ValueError('Positive rational slots <=12, denominator <=3 required')
 if level!='hard' and any(x.q!=1 for x in p.values()):raise ValueError('Observed easy/moderate integer workload')
 if level=='hard' and (t not in ('quarter_open','three_segments') or all(x.q==1 for x in p.values())):raise ValueError('Hard uses only existing quarter-open/three-segment geometry with noninteger rational bookkeeping')
 if t=='three_segments' and not s.sqrt(p['a']**2+p['b']**2).is_Rational:raise ValueError('Familiar Pythagorean arithmetic required')
 if t=='two_segments' and not s.sqrt(p['a']**2+p['h']**2).is_Integer:raise ValueError('First distance must remain perfect square as observed')
 if level!='hard' and TEMPLATES[t][0]!=level:raise ValueError('Template difficulty mismatch')
def sample(level,t,rng):
 if t in ('semi','three_quarter','quarter_closed','quarter_open'):
  vals=range(1,13) if level!='hard' else [s.Rational(k,d) for d in (2,3) for k in range(1,13*d+1) if k%d]
  return {'r':rng.choice(list(vals))}
 if t=='three_segments':
  vals=[{'a':s.Rational(a,d),'b':s.Rational(b,d)} for d in ((2,3) if level=='hard' else (1,)) for a,b in ((3,4),(4,3),(5,12),(12,5),(6,8),(8,6),(9,12),(12,9))]
  vals=[v for v in vals if level!='hard' or any(x.q!=1 for x in v.values())]
  return rng.choice(vals)
 vals=[{'a':a,'h':h,'b':b} for a,h in ((3,4),(4,3),(6,8),(8,6)) for b in range(1,9) if not s.sqrt(b*b+h*h).is_Integer]
 return rng.choice(vals)
def bank(profile,t,p,L):
 r=p.get('r'); A=sum(L)
 if profile=='q-122481':return [(r*(s.pi+1),'radius_instead_diameter'),(2*r*(s.pi+2),'double_total'),(A,'correct'),(r*(2*s.pi+1),'compound_2pi_radius'),(2*r*(s.pi+1),'compound_2pi_diameter')]
 if profile=='q-122843':return [(2*r*s.pi+r/2,'empirical_4pi_1'),(A,'correct'),(3*r*s.pi/2+2*r,'double_segment'),(r*s.pi+3*r/2,'empirical_2pi_3'),(r*s.pi/2+r,'quarter_arc')]
 if profile=='q-122484':return [(r*s.pi/4+r*s.sqrt(3)/2,'empirical_pi4_sqrt3half'),(A,'correct'),(r*s.pi/2+r*s.sqrt(2)/2,'half_chord'),(r*s.pi/4+r*s.sqrt(2)/2,'half_both'),(r*s.pi+3*r*s.sqrt(2)/2,'empirical_pi_3sqrt2half')]
 if profile=='q-122828':
  a,b=p['a'],p['b'];return [(3*a,'three_vertical'),(3*b,'three_horizontal'),(A,'correct'),(2*b,'two_horizontal'),(2*L[1],'double_diagonal')]
 if profile=='q-122845':
  a,b,h=p['a'],p['b'],p['h'];return [(a+b+h,'add_coordinate_legs'),(h+L[1],'height_plus_second'),(2*a+L[1],'double_left_plus_second'),(A,'correct'),(2*L[0],'double_first')]
 if profile=='q-122850':return [(3*r*s.pi/16+r*s.sqrt(2)/4,'empirical_3pi16_sqrt2quarter'),(r*s.pi+r*s.sqrt(2)/2,'empirical_pi_halfchord'),(r*s.pi/16+r*s.sqrt(2)/4,'empirical_pi16_sqrt2quarter'),(r*s.pi/2+3*r*s.sqrt(2)/4,'three_quarter_chord'),(A,'correct')]
 # Complete authored bank chosen before any parameter sampling. No pooled fallback.
 if profile=='authored_arc':return [(A,'correct'),(L[0],'omit_segment'),(L[1],'omit_arc'),(2*L[0]+L[1],'double_arc'),(L[0]+2*L[1],'double_segment')]
 return [(A,'correct'),(L[0],'omit_rest'),(sum(L[1:]),'omit_first'),(2*L[0]+sum(L[1:]),'double_first'),(L[0]+2*sum(L[1:]),'double_rest')]
def prose(t,p,assets,L):
 n=len(L);count='three' if n==3 else 'two';r=p.get('r')
 problem=r'Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is the path shown above.'
 if t=='semi':problem=r'Calculate ${\int }_{C}\,\text{d}s,$ where $C$ is a path that traverses a semicircle of radius $'+tex(r)+r'$ once in the counterclockwise direction, as shown above.'
 if t=='quarter_closed':problem=r'Calculate $\displaystyle \int_{C}ds$, where $C$ is a path that traverses a circular segment of radius $'+tex(r)+r'$ once in the counterclockwise direction, as shown above.'
 out='The path $C$ is made up of '+count+' parts, as shown below:\n\n![]('+assets['solution']+')'
 if t=='quarter_open':out+='\n\n'+problem
 parts='\\cup '.join(r'{C}_{'+str(i)+'}' for i in range(1,n+1))
 terms='+'.join(r'{\int }_{{C}_{'+str(i)+r'}}f(x,y)\,\text{d}s' for i in range(1,n+1))
 out+='\n\nNow, we make use of the following facts:\n\n- If $C='+parts+'$ is a piecewise-smooth curve, we have'+equation(r'{\int }_{C}f(x,y)\,\text{d}s='+terms+'.')
 out+='\n\n- The line integral of unity with respect to arc length over $C$ is equal to the arc length $L$ of $C,$ i.e.,'+equation(I()+'=L.')
 if r:
  name={'semi':'a semi-circle','three_quarter':'three-quarters of a circle','quarter_open':'a quarter of a circle','quarter_closed':'a quarter of a circle'}[t]
  formula=r'\pi r' if t=='semi' else (r'\frac{3}{4}(2\pi r)' if t=='three_quarter' else r'\frac{1}{4}(2\pi r)')
  out+='\n\nThe path ${C}_{1}$ is '+name+' of radius $r='+tex(r)+'.$ Therefore, we have'+equation(I(1)+'='+formula+'='+tex(L[0])+' .')
  if t in ('semi','three_quarter'):out+='\n\nThe path ${C}_{2}$ is a line segment of length $'+tex(L[1])+'.$ Therefore, we have'+equation(I(2)+'='+tex(L[1])+'.')
  else:out+='\n\nThe path ${C}_{2}$ is the hypotenuse of a right triangle where both legs have a length of $'+tex(r)+'.$ Therefore, we have'+equation(I(2)+r'=\sqrt{{'+tex(r)+r'}^{2}+{'+tex(r)+r'}^{2}}='+tex(L[1])+'.')
 elif t=='three_segments':
  a,b=p['a'],p['b'];out+='\n\nThe paths ${C}_{1}$ and ${C}_{3}$ are line segments of length $'+tex(a)+'.$ Therefore, we have'+equation(I(1)+'='+I(3)+'='+tex(a)+'.')
  out+='\n\nThe path ${C}_{2}$ is the hypotenuse of a right triangle whose legs have lengths $'+tex(a)+'$ and $'+tex(b)+'.$ Therefore, we have'+equation(I(2)+r'=\sqrt{{'+tex(a)+r'}^{2}+{'+tex(b)+r'}^{2}}='+tex(L[1])+'.')
 else:
  for i,k in ((1,'a'),(2,'b')):
   a,h=p[k],p['h'];out+='\n\nThe path ${C}_{'+str(i)+'}$ is the hypotenuse of a right triangle whose legs have lengths $'+tex(a)+'$ and $'+tex(h)+'.$ Therefore, we have'+equation(I(i)+r'=\sqrt{{'+tex(a)+r'}^{2}+{'+tex(h)+r'}^{2}}='+tex(L[i-1])+'.')
 A=s.simplify(sum(L));summed='+'.join(tex(x) for x in L);final=(tex(p['r'])+r'(\pi+2)' if t=='semi' else tex(p['r']/2)+r'(\pi+2\sqrt{2})' if t=='quarter_open' else tex(s.factor(A)))
 out+='\n\nTherefore,'+equation(I()+'='+summed+('='+final if t in ('semi','quarter_open','three_segments') else '')+'.')
 return '![]('+assets['prompt']+')\n\n'+problem,out

def render_plots(t,p,output_dir=None):
 data={'template':t,'parameters':{k:str(v) for k,v in p.items()},'geometry':json.loads(json.dumps(geometry(t,p),default=str)),'renderer':'Matplotlib PNG','version':VERSION}
 digest=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest(); dest=Path(output_dir or ROOT/'assets');dest.mkdir(parents=True,exist_ok=True)
 assets={role:str((dest/(digest+'-'+role+'.png')).resolve()) for role in ('prompt','solution')}
 if all(Path(v).exists() and Path(v).with_suffix('.json').exists() for v in assets.values()):return assets
 with tempfile.TemporaryDirectory(prefix='render-',dir=dest) as tmp:
  inp=Path(tmp)/'input.json';inp.write_text(json.dumps({'data':data,'assets':assets}));subprocess.run([sys.executable,__file__,'--render-input',str(inp)],check=True,capture_output=True)
 return assets

def render_native(input_path):
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 payload=json.loads(Path(input_path).read_text());d=payload['data'];t=d['template'];p={k:s.Rational(v) for k,v in d['parameters'].items()};g=geometry(t,p);color='#2f7ab5'
 curves=[]
 if 'arc' in g:
  r,lo,hi=map(float,g['arc']);cx,cy=map(float,g['center']);theta=np.linspace(lo,hi,241);curves.append(np.column_stack([cx+r*np.cos(theta),cy+r*np.sin(theta)]))
 pts=np.array(g['points'],dtype=float)
 for a,b in zip(pts,pts[1:]):curves.append(np.array([a,b]))
 coords=np.concatenate(curves);x0,x1=min(0,coords[:,0].min()),max(0,coords[:,0].max());y0,y1=min(0,coords[:,1].min()),max(0,coords[:,1].max());span=max(x1-x0,y1-y0,1);pad=.23*span
 for role,final in payload['assets'].items():
  fig,ax=plt.subplots(figsize=(3.6,3.04),dpi=120);fig.subplots_adjust(left=.07,right=.94,bottom=.1,top=.92);ax.set_aspect('equal');ax.set_xlim(x0-pad,x1+pad);ax.set_ylim(y0-pad,y1+pad);ax.axis('off')
  ax.annotate('',(x1+pad*.85,0),(x0-pad,0),arrowprops={'arrowstyle':'->','lw':1,'color':'black'});ax.annotate('',(0,y1+pad*.85),(0,y0-pad),arrowprops={'arrowstyle':'->','lw':1,'color':'black'});ax.text(x1+pad*.9,-.025*span,'$x$');ax.text(.025*span,y1+pad*.86,'$y$');ax.text(-.045*span,-.065*span,'0',fontsize=8)
  for axis,vals in g['ticks'].items():
   for v in vals:
    f=float(v);ax.text(f,-.065*span,'$'+tex(v)+'$',ha='center',fontsize=9) if axis=='x' else ax.text(-.035*span,f,'$'+tex(v)+'$',ha='right',va='center',fontsize=9)
  for i,c in enumerate(curves):
   ax.plot(c[:,0],c[:,1],color=color,lw=1.5)
   for f in (.25,.5,.75):
    if len(c)>2:
     j=int(f*(len(c)-1));a,b=c[j-2],c[j+2]
    else:a=c[0]+(f-.035)*(c[1]-c[0]);b=c[0]+(f+.035)*(c[1]-c[0])
    ax.annotate('',b,a,arrowprops={'arrowstyle':'->','color':color,'lw':1,'mutation_scale':9})
   if role=='solution':
    mid=c[len(c)//2] if len(c)>2 else c.mean(axis=0);offset=np.array([.045*span,.05*span]);
    if t=='semi' and i==0:mid=c[len(c)//3];offset=np.array([.06*span,.04*span])
    if t=='semi' and i==1:mid=np.array([float(p['r'])*.55,1]);offset=np.array([0,-.1*span])
    if t=='three_quarter' and i==0:offset=np.array([-.11*span,.06*span])
    if t=='quarter_open' and i==0:offset=np.array([.1*span,-.07*span])
    if t=='two_segments':offset=np.array([-.14*span,.02*span]) if i==0 else np.array([.09*span,.02*span])
    if t=='three_segments' and i==0:offset=np.array([-.16*span,0])
    ax.text(*(mid+offset),'$C_'+str(i+1)+'$',color=color,fontsize=10)
  if g['endpoints']:
   ends=[curves[0][0],curves[-1][-1]];ax.scatter([v[0] for v in ends],[v[1] for v in ends],s=11,color=color,zorder=5)
  tmp=Path(input_path).parent/(role+'.png');fig.savefig(tmp,metadata={'Software':'Course Academy '+VERSION});plt.close(fig);os.replace(tmp,final)
  side=Path(input_path).parent/(role+'.json');side.write_text(json.dumps(d|{'role':role,'bounds':[x0-pad,x1+pad,y0-pad,y1+pad],'curves':[c.tolist() for c in curves],'labels':['C_'+str(i+1) for i in range(len(curves))] if role=='solution' else []},indent=2));os.replace(side,Path(final).with_suffix('.json'))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only radio supported')
 rng=random.Random(seed);allowed=['quarter_open','three_segments'] if level=='hard' else [k for k,v in TEMPLATES.items() if v[0]==level]
 t=template or (PROFILES.get(profile) if profile in PROFILES else None) or rng.choice(allowed)
 if t not in allowed:raise ValueError('Template outside level policy')
 selected=profile or ('authored_segments' if t.endswith('segments') else 'authored_arc')
 if selected not in PROFILES or (PROFILES[selected] is not None and PROFILES[selected]!=t):raise ValueError('Profile incompatible')
 if selected.startswith('authored') and (selected=='authored_segments') != t.endswith('segments'):raise ValueError('Authored bank geometry mismatch')
 for attempt in range(200):
  p={k:s.Rational(str(v)) for k,v in parameters.items()} if parameters is not None else {k:s.Rational(v) for k,v in sample(level,t,rng).items()};guard(level,t,p);L=lengths(t,p);A=s.simplify(sum(L));B=bank(selected,t,p,L)
  valid=all(s.simplify(x)>0 for x,_ in B) and all(s.simplify(x-y)!=0 for j,(x,_) in enumerate(B) for y,_ in B[j+1:]) and sum(s.simplify(x-A)==0 for x,_ in B)==1
  if valid:break
  if parameters is not None:raise ValueError('Whole bank ambiguous or invalid')
 else:raise ValueError('No valid instance')
 assets=render_plots(t,p);prompt,solution=prose(t,p,assets,L)
 # Native source uses no inserted placeholder for its radio widget; retain that contract.
 values=[tex(x) for x,_ in B]
 # Keep scalar answer values delimiter-free; notation normalizations are recorded.
 content=json.dumps({'version':VERSION,'problem':prompt,'solution':solution,'bank':sorted(values)},sort_keys=True);qid=uid(content);fid=uid(qid+'/selection')
 choices=[{':answer/id':uid(fid+'/'+canonical(x)),':answer/type':':answer.type/math',':answer/value':v} for (x,_),v in zip(B,values)];correct=next(a[':answer/id'] for a,(x,_) in zip(choices,B) if s.simplify(x-A)==0);rng.shuffle(choices)
 mathfinger=hashlib.sha256(json.dumps({'primitive_roles':('arc_and_segment' if 'r' in p else 'segments'),'component_lengths':[canonical(v) for v in L]},sort_keys=True).encode()).hexdigest()
 return {'knowledge_point':{'db_id':KP,'id':SOURCE_DATA['record'][':knowledge-point/id'],'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':t,'profile':selected,'seed':seed,'parameters':{k:str(v) for k,v in p.items()},'lengths':[canonical(v) for v in L],'answer':canonical(A),'recipes':[{ 'recipe':rec,'value':canonical(x)} for x,rec in B],'source_refs':[TEMPLATES[t][1]],'provenance':{'database':'math','basis':2275,'lineage':SOURCE_DATA['lineage']},'authored_level':level=='hard' or t=='quarter_closed','profile_status':'observed empirical; intention underidentified' if selected.startswith('q-') else 'authored default','mathematical_fingerprint':mathfinger,'assets':assets,'calculator_requirement':'unknown: all source flags absent'}}
# EASY: semicircle+diameter or three-quarter arc+one horizontal segment.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: source two/three segments or quarter circle+chord; inferred q122484.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: authored bounded rational bookkeeping; identical method and part counts.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--render-input');parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');a=parser.parse_args()
 if a.render_input:render_native(a.render_input)
 else:
  records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
  if a.format=='json':print(json.dumps(records,indent=2))
  else:
   for rec in records:
    q=rec['question'];print(q[':question/problem']+'\n\n'+ '\n'.join('- $'+v[':answer/value']+'$' for v in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution'])
