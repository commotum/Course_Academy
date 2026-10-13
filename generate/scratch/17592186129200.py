#!/usr/bin/env python3
"""Polar double integrals, captured math basis1356. Stop after guide step7.
Nine observed templates, complete replay banks; authored default banks use actual
integrand/bound operations, including two zero-valued families. Coefficients and
radii vary at their source difficulty. Explicit inputs obey the same bounds.
Private concurrent atomic Matplotlib plots live under the adjacent evidence.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,tempfile,uuid,os
from pathlib import Path
import sympy as S
HERE=Path(__file__).resolve().with_suffix('');VERSION='polar-double-v1'
RAW=json.loads((HERE/'source.json').read_text());KP=RAW['record'];KP_ID=17592186129200
r=S.Symbol('r',nonnegative=True);t=S.Symbol('theta',real=True);x,y=S.symbols('x y',real=True)
pi=S.pi
TEMPLATES={
 'upper_linear':('moderate','q-38140',{'R':2,'a':2,'b':1}),
 'lower_sqrt':('hard','q-83968',{'R':1,'c':1}),
 'odd_disk':('easy','q-161050',{'R':1,'c':15}),
 'square_y':('easy','q-161052',{'R':3,'c':4}),
 'exponential':('easy','q-161053',{'R':2,'c':1}),
 'radial_square':('easy','q-161054',{'R':3,'c':2}),
 'upper_ratio':('hard','q-161055',{'R':2,'c':1}),
 'rational_quarter':('moderate','q-83970',{'R':1,'c':2}),
 'quarter_difference':('moderate','q-83520',{'R':2,'c':1}),
}
SOURCES={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
def tex(z):return S.latex(S.sympify(z)).replace(r'\log',r'\ln')
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def digest(z):return hashlib.sha256(json.dumps(z,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def mathdata(name,p):
 R=S.Rational(str(p['R']));c=S.Rational(str(p.get('c',1)));a=S.Integer(p.get('a',1));b=S.Integer(p.get('b',1))
 fs={'upper_linear':a*x+b*y,'lower_sqrt':c*x*S.sqrt(x*x+y*y),'odd_disk':c*x*x*y,'square_y':c*y*y,'exponential':c*S.exp(x*x+y*y),'radial_square':c*(x*x+y*y),'upper_ratio':c*x/y,'rational_quarter':c/(x*x+y*y+1),'quarter_difference':c*(x-y)}
 bounds={'upper_linear':(0,pi,R),'lower_sqrt':(-pi/2,0,-R*S.sin(t)),'upper_ratio':(0,pi/2,R*S.sin(t)),'rational_quarter':(pi,3*pi/2,R),'quarter_difference':(0,pi/2,R)}
 lo,hi,up=bounds.get(name,(0,2*pi,R));f=fs[name];pol=S.trigsimp(f.subs({x:r*S.cos(t),y:r*S.sin(t)})*r)
 if name=='lower_sqrt':pol=c*r**3*S.cos(t)
 if name=='upper_ratio':pol=c*r*S.cos(t)/S.sin(t)
 radial=S.integrate(pol,r);angular=S.simplify(radial.subs(r,up)-radial.subs(r,0));primitive=S.integrate(S.expand_trig(angular),t)
 ans=S.simplify(primitive.subs(t,hi)-primitive.subs(t,lo))
 return dict(R=R,c=c,a=a,b=b,f=f,lo=lo,hi=hi,up=up,polar=pol,radial=radial,angular=angular,primitive=primitive,answer=ans)
def render_plots(name,p,output_dir=None):
 m=mathdata(name,p);d={'kind':'shift' if name in ('lower_sqrt','upper_ratio') else 'sector','R':float(m['R']),'a':float(m['lo']),'b':float(m['hi']),'sign':-1 if name=='lower_sqrt' else 1};h=digest([d,hashlib.sha256((HERE/'render.py').read_bytes()).hexdigest()])[:20];folder=Path(output_dir) if output_dir is not None else HERE/'plots';out=folder/f'{h}.png'
 if not (out.exists() and out.with_suffix('.json').exists()):
  folder.mkdir(exist_ok=True)
  fd,tmp=tempfile.mkstemp(prefix='input-',suffix='.json',dir=folder)
  try:
   with os.fdopen(fd,'w') as f:json.dump(dict(d,output=str(out)),f)
   subprocess.run([os.sys.executable,str(HERE/'render.py'),tmp],check=True,capture_output=True)
  finally:os.unlink(tmp)
 return str(out)
def bank(name,p,m,profile):
 R,c,A=m['R'],m['c'],m['answer'];a,b=m['a'],m['b']
 if profile=='observed':
  values={
   'upper_linear':[R**3,R**3/3,3/R**2,R,2*b*R**3/3],
   'lower_sqrt':[c*R**4/20,c*R**4/15,c*R**4/10,c*R**4/5,c*R**4/4],
   'odd_disk':[c*R**5/5,c*R**5/15,c*R**5/45,c*R**5/3,0],
   'square_y':[R**2+c*pi,R**2*pi,c*R**4*pi/4,2*R**2+c*pi/2,R**3*pi],
   'exponential':[c*R*pi*(S.exp(R)-1),c*S.exp(R)*(R*pi-1),c*pi**2,c*R*pi*S.exp(R**2),A],
   'radial_square':[c*R**3*pi/2,c*(R**2*pi-R)/2,A,c*(2*R**2*pi+c)/2,c*R**2*pi/2],
   'upper_ratio':[c*R**2*pi/4,0,A,c*R**2/2,c*R**2*pi/2],
   'rational_quarter':[c*pi/4,c*S.log(R**2+1),c*pi*S.log(R**2+1)/2,c*S.log(R**2+1)/4,A],
   'quarter_difference':[2*c*R**3/3,c*R,c*R**3/6,c*R**3/3,0],
  }[name];ops=['observed expression pattern; intent unresolved']*5
 else:
  # Select a COMPLETE five-value bank, then reject the whole instance on collision.
  if name=='odd_disk':
   v=c*R**5/15;values=[A,v,2*v,4*v,-v];ops=['correct','angle0..pi/2','angle0..pi','absolute sin over0..2pi','anglepi..3pi/2']
  elif name=='quarter_difference':
   v=c*R**3/3;values=[A,v,2*v,-v,-2*v];ops=['correct','omit-y','replace minus with plus','omit-x','anglepi/2..pi']
  elif name=='upper_linear':
   values=[A,-A,2*a*R**3/3,b*R**2,0];ops=['correct','negate-y','angle-pi/2..pi/2','omit Jacobian','angle0..2pi']
  elif name in ('square_y','radial_square'):
   omitted=c*pi*R**3/3*(2 if name=='radial_square' else 1)
   values=[A,omitted,A/16,A/2,-A];ops=['correct','omit Jacobian','radial upper R/2','angle width halved','reverse angular bounds']
  elif name=='exponential':
   values=[A,c*pi*S.exp(R**2),2*A,c*pi*(S.exp(R)-1),-A];ops=['correct','omit lower radial endpoint','omit radial factor1/2','replace R² with R','reverse angular bounds']
  elif name=='rational_quarter':
   values=[A,2*A,4*A,c*S.log(R**2+1)/2,-A];ops=['correct','semicircle angle','full disk angle','omit angular width','reverse angular bounds']
  elif name=='lower_sqrt':
   values=[A,c*R**3/12,c*R**4/4,A/16,-A];ops=['correct','omit Jacobian','omit angular divisor5','radial upper halved','reverse angular bounds']
  else:
   values=[A,c*R,c*R**2/16,c*R**2*pi/8,-A];ops=['correct','omit Jacobian','radial upper halved','replace cotθ with1','reverse angular bounds']
 values=[S.simplify(v) for v in values]
 if any(S.simplify(u-v)==0 for i,u in enumerate(values) for v in values[i+1:]):raise ValueError('Whole bank rejected: equivalent options')
 if sum(S.simplify(v-A)==0 for v in values)!=1:raise ValueError('Whole bank rejected: incorrect correct-answer multiplicity')
 return values,ops
def worked(name,p,m,img):
 R,c,a,b=[tex(m[k]) for k in ('R','c','a','b')];lo,hi,up=[tex(m[k]) for k in ('lo','hi','up')];f=tex(m['f']);ans=tex(m['answer']);C=r'\cos\theta';N=r'\sin\theta'
 I=lambda s:rf'\int_{{{lo}}}^{{{hi}}}{s}\,\mathrm{{d}}\theta'
 J=lambda s:rf'\int_0^{{{R}}}{s}\,\mathrm{{d}}r'
 B=lambda s,z:rf'\left[{s}\right]_0^{{{z}}}'
 E=lambda s:rf'\left[{s}\right]_{{{lo}}}^{{{hi}}}'
 D=lambda s:rf'\iint_\Delta {s}\,\mathrm{{d}}r\,\mathrm{{d}}\theta'
 radial=tex(m['radial']);g=tex(m['angular']);P=tex(m['primitive']);value=tex(m['R']**(5 if name=='odd_disk' else 4));rows=[]
 # Structural arithmetic masks deliberately preserve distinct source teaching stages.
 if name=='upper_linear' or name=='quarter_difference':
  h=rf'({a}{C}+{b}{N})' if name=='upper_linear' else rf'{c}({C}-{N})'
  sub=rf'({a}r{C}+{b}r{N})r' if name=='upper_linear' else rf'{c}(r{C}-r{N})r'
  coeff=tex(m['R']**3/3);hP=rf'{a}\sin\theta-{b}\cos\theta' if name=='upper_linear' else rf'{c}(\sin\theta+\cos\theta)'
  ep=lambda z:rf'{a}\sin({z})-{b}\cos({z})' if name=='upper_linear' else rf'{c}(\sin({z})+\cos({z}))'
  ep1=S.simplify((m['a']*S.sin(t)-m['b']*S.cos(t) if name=='upper_linear' else m['c']*(S.sin(t)+S.cos(t))).subs(t,m['hi']))
  ep0=S.simplify((m['a']*S.sin(t)-m['b']*S.cos(t) if name=='upper_linear' else m['c']*(S.sin(t)+S.cos(t))).subs(t,m['lo']))
  rows=[D(sub),I(rf'\int_0^{{{R}}}r^{{2}}{h}\,\mathrm{{d}}r'),I(h+J('r^2')),I(h+B(r'\frac{r^3}{3}',R)),I(h+rf'(\frac{{{R}^3}}{{3}}-0)'),coeff+I(h),coeff+E(hP),rf'{coeff}(({ep(hi)})-({ep(lo)}))',rf'{coeff}(({tex(ep1)})-({tex(ep0)}))',ans]
 elif name=='odd_disk':
  v=tex(m['c']/5);rv=tex(m['R']**5);k=tex(m['c']/15)
  rows=[D(rf'{c}(r^2\cos^2\theta\cdot r{N})r'),I(rf'\int_0^{{{R}}}{c}r^4\cos^2\theta{N}\,\mathrm{{d}}r'),I(rf'({v}\cos^2\theta{N})'+J('5r^4')),I(rf'{v}\cos^2\theta{N}'+B('r^5',R)),I(rf'{v}\cos^2\theta{N}({rv}-0)'),rv+I(rf'{v}\cos^2\theta{N}'),rv+E(rf'-{k}\cos^3\theta'),rf'-{rv}\cdot {k}(\cos^3({hi})-\cos^3({lo}))',rf'-{rv}\cdot {k}(1-1)',ans]
 elif name=='square_y':
  k=tex(m['c']/4);rv=tex(m['c']*m['R']**4/4)
  rows=[D(rf'{c}(r{N})^2r'),I(rf'\int_0^{{{R}}}{c}r^3\sin^2\theta\,\mathrm{{d}}r'),I(r'\sin^2\theta'+J(c+'r^3')),I(rf'\sin^2\theta'+B(rf'{k}r^4',R)),I(rf'\sin^2\theta({tex(m["c"]*m["R"]**4/4)}-0)'),rv+I(r'\sin^2\theta'),rv+I(r'\frac12(1-\cos2\theta)'),tex(m['c']*m['R']**4/8)+E(r'\theta-\frac12\sin2\theta'),rf'{tex(m["c"]*m["R"]**4/8)}[({hi}-0)-\frac12(\sin(4\pi)-\sin0)]',rf'{tex(m["c"]*m["R"]**4/8)}\cdot2\pi',ans]
 elif name=='radial_square':
  rv=tex(m['R']**4/4);coeff=tex(m['c']*m['R']**4/4)
  rows=[D(rf'{c}((r{C})^2+(r{N})^2)r'),D(rf'{c}r^2(\cos^2\theta+\sin^2\theta)r'),c+D('r^3'),c+I(J('r^3')),c+I(B(r'\frac{r^4}{4}',R)),c+I(rf'({rv}-0)'),coeff+I('1'),coeff+E(r'\theta'),rf'{coeff}({hi}-0)',ans]
 elif name=='exponential':
  k=tex(m['c']/2);eR=tex(m['R']**2);coef=tex(m['c']/2*(S.exp(m['R']**2)-1))
  rows=[D(rf'{c}e^{{(r{C})^2+(r{N})^2}}r'),D(rf'{c}e^{{r^2(\cos^2\theta+\sin^2\theta)}}r'),D(rf'{c}e^{{r^2}}r'),I(J(rf'{c}r e^{{r^2}}')),I(B(rf'{k}e^{{r^2}}',R)),I(rf'{k}(e^{{{eR}}}-1)'),rf'{k}(e^{{{eR}}}-1)'+E(r'\theta'),rf'{k}(e^{{{eR}}}-1)(2\pi-0)',ans]
 elif name=='rational_quarter':
  k=tex(m['c']/2);u=tex(m['R']**2+1);coef=tex(m['c']/2*S.log(m['R']**2+1))
  rows=[D(rf'\frac{{{c}}}{{(r{C})^2+(r{N})^2+1}}r'),I(J(rf'\frac{{{c}r}}{{r^2+1}}')),I(B(rf'{k}\ln(r^2+1)',R)),I(rf'{k}(\ln({u})-\ln1)'),coef+I('1'),coef+E(r'\theta'),rf'{coef}({hi}-{lo})',ans]
 elif name=='lower_sqrt':
  k=tex(m['c']/4);R4=tex(m['R']**4);kk=tex(m['c']*m['R']**4/4);kk5=tex(m['c']*m['R']**4/20)
  rows=[D(rf'{c}(r{C})\sqrt{{(r{C})^2+(r{N})^2}}r'),I(rf'{c}{C}\int_0^{{{up}}}r^3\,\mathrm{{d}}r'),I(rf'{c}{C}'+B(r'\frac{r^4}{4}',up)),k+I(rf'{C}(({up})^4-0^4)'),kk+I(rf'{C}\sin^4\theta'),kk+E(r'\frac{\sin^5\theta}{5}'),rf'{kk5}(\sin^5(0)-\sin^5(-\frac\pi2))',ans]
 else:
  k=tex(m['c']*m['R']**2/2);kh=tex(m['c']*m['R']**2/4)
  rows=[D(rf'{c}\frac{{r{C}}}{{r{N}}}r'),I(rf'{c}\frac{{{C}}}{{{N}}}\int_0^{{{up}}}r\,\mathrm{{d}}r'),I(rf'{c}\frac{{{C}}}{{{N}}}'+B(r'\frac{r^2}{2}',up)),I(rf'{c}\frac{{{C}}}{{{N}}}(\frac{{{R}^2}}{{2}}\sin^2\theta-0)'),I(rf'{k}{C}{N}'),I(rf'{kh}\sin2\theta'),E(rf'-{tex(m["c"]*m["R"]**2/8)}\cos2\theta'),rf'-{tex(m["c"]*m["R"]**2/8)}(\cos\pi-\cos0)',rf'-{tex(m["c"]*m["R"]**2/8)}(-1-1)',ans]
 src=SOURCES[TEMPLATES[name][1]]
 # Full shared prose follows the source; formal math normalized from Unicode to TeX.
 opening=src[':question/worked-solution'].split('$$')[0]
 solution=opening+'$$\n'+r'\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)r\,\mathrm{d}r\,\mathrm{d}\theta.'+'\n$$\n\n'
 if name in ('lower_sqrt','upper_ratio'):
  sign='-' if name=='lower_sqrt' else '';sigval=-m['R'] if sign else m['R'];z=tex(sigval);radius=tex(m['R']/2);center=tex(sigval/2);boundary=rf'\sqrt{{{z}y-y^2}}'
  solution+=rf'First, notice that the region $D$ represents a portion of the disk of radius ${radius}$ centered at'+f'\n$(0,{center}).$\n\n'
  solution+='Cartesian and polar coordinates are connected by the following equations:\n\n$$\n'+r'\left\{\begin{aligned}x=r\cos\theta\\y=r\sin\theta\end{aligned}\right.'+'\n$$\n\n'
  solution+=rf"With that in mind, let's now write the $x={boundary}$ in polar coordinates:"+'\n\n$$\n'
  eqs=[rf'x&={boundary}',rf'x^2&={z}y-y^2',rf'x^2+y^2&={z}y',rf'(r{C})^2+(r{N})^2&={z}r{N}',rf'r^2(\cos^2\theta+\sin^2\theta)&={z}r{N}',rf'r^2&={z}r{N}',rf'r^2-({z})r{N}&=0',rf'r(r-({z}){N})&=0']
  solution+=r'\begin{aligned}'+r'\\'.join(eqs)+r'\end{aligned}'+'\n$$\n\n'
  solution+=rf'Since $r$ cannot be identical to zero on the entire semicircle, we must have $r={up}$.'+'\n\nTherefore, in polar coordinates $(r,\\theta ),$ the region can be expressed as \n\n'
 else:solution+="First, let's sketch our region $D:$\n\n![]( "+img+")\n\nIn polar coordinates $(r,\\theta ),$ the region can be expressed as \n\n"
 solution+='$$\n'+rf'\Delta=\{{(r,\theta):0\le r\le {up},\ {lo}\le\theta\le {hi}\}}.'+'\n$$\n\n'
 solution+=('Therefore, we obtain' if name in ('lower_sqrt','upper_ratio') else 'Therefore, using the change of variables formula, we obtain ')+'\n\n$$\n'
 solution+=r'\begin{aligned}\iint_D '+f+r'\,\mathrm{d}A &='+rows[0]+r'\\'+'\n'+r'\\'.join('&='+v for v in rows[1:])+r'\end{aligned}'+'\n$$'
 if name=='upper_ratio':solution+='\n\nThe integrand is defined for $y>0$ on the interior of $D$. The point $(0,0)$ is a boundary point. The integral is the limit with angular lower bound $\\varepsilon>0$ as $\\varepsilon\\to0^+$; after radial integration the integrand is $'+g+'$, whose integral converges. No principal value is required.'
 return solution,rows

def check_parameters(name,p):
 expected=set(TEMPLATES[name][2]);
 if set(p)!=expected:raise ValueError('Parameter keys must be '+str(expected))
 for key,val in p.items():
  v=S.Rational(str(val))
  if key=='R':
   if v not in ([S.Rational(1,2),1,2,3,4,5] if name in ('lower_sqrt','upper_ratio') else [1,2,3,4,5]):raise ValueError('Radius/diameter outside documented finite domain')
  elif v.q!=1 or not 1<=v<= (30 if name=='odd_disk' else 8):raise ValueError('Coefficient outside documented workload')
 if name=='exponential' and p['R']==1:raise ValueError('R=1 collides unsquared endpoint error with correct answer')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout supported')
 rng=random.Random(seed);names=[n for n,v in TEMPLATES.items() if v[0]==level]
 name=template or rng.choice(names)
 if name not in names:raise ValueError('Template outside difficulty')
 prof=profile or 'authored'
 if prof not in ('authored','observed','observed_raw'):raise ValueError('Unknown complete profile')
 for attempt in range(1000):
  if parameters is not None:p=dict(parameters)
  else:
   p={k:rng.choice([1,2,3,4,5]) if k=='R' else rng.randint(1,30 if name=='odd_disk' else 8) for k in TEMPLATES[name][2]}
   if name=='exponential':p['R']=rng.choice([2,3,4,5])
  check_parameters(name,p);m=mathdata(name,p)
  try:values,ops=bank(name,p,m,'observed' if prof=='observed_raw' else prof);break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No eligible whole bank sampled')
 img=render_plots(name,p);solution,rows=worked(name,p,m,img)
 if prof=='authored' and name in ('upper_linear','quarter_difference'):
  def component_endpoint(z):
   if name=='upper_linear':return rf'{tex(m["a"]*S.sin(z))}-({tex(m["b"]*S.cos(z))})'
   return rf'{tex(m["c"]*S.sin(z))}+({tex(m["c"]*S.cos(z))})'
  replacement=rf'{tex(m["R"]**3/3)}(({component_endpoint(m["hi"])})-({component_endpoint(m["lo"])}))'
  solution=solution.replace(rows[-2],replacement);rows[-2]=replacement
 if prof=='observed_raw':
  if name=='odd_disk':
   solution=solution.replace(r'\iint_D '+tex(m['f'])+r'\,',r'\iint_D '+tex(S.Rational(4,5)*m['f'])+r'\,')
  if name=='exponential':
   replacement=rows[0].replace(r'(r\cos\theta)^2',r'(r\cos^2\theta)^2')
   solution=solution.replace(rows[0],replacement);rows[0]=replacement
 if name in ('lower_sqrt','upper_ratio'):prompt='![]('+img+')\n\nEvaluate the double integral $'+r'\iint_D '+tex(m['f'])+r'\,\mathrm{d}A'+',$ where the region $D$ is the semicircle shown above.'
 else:
  restriction={'upper_linear':r', where $y\ge0.$','rational_quarter':r', where $x\le0$ and $y\le0.$','quarter_difference':r', where $x\ge0$ and $y\ge0.$'}.get(name,'.')
  portion='portion of the disk' if name in ('upper_linear','rational_quarter','quarter_difference') else 'disk'
  prompt=f'Integrate the function $f(x,y)={tex(m["f"])}$ over the {portion} of radius ${tex(m["R"])}$ centered at the origin'+restriction
 # Content identity uses actual full presentation and bank, excludes seed and option order.
 key=digest([VERSION,prompt,solution,sorted(tex(v) for v in values)]);qid=uid(key);fid=uid(key+'/selection')
 choices=[{':answer/id':uid(fid+'/'+tex(v)),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in values]
 correct=next(a[':answer/id'] for a,v in zip(choices,values) if S.simplify(v-m['answer'])==0);rng.shuffle(choices)
 question={':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct]}]}
 mathematical=digest([S.srepr(m['f']),S.srepr(m['up']),S.srepr(m['lo']),S.srepr(m['hi'])])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'bank_profile':prof,'source':{k:v for k,v in RAW.items() if k!='record'},'source_ids':[TEMPLATES[name][1]],'mathematical_fingerprint':mathematical,'content_hash':key,'recipes':ops,'exact_choices':[str(v) for v in values],'stages':rows,'mathematics':{k:str(v) for k,v in m.items()},'plot':img,'domain':'r>=0; bounded disk/sector; upper_ratio y>0 interior, integrable boundary singularity','authored_extension':prof=='authored','raw_mathematical_evidence':prof=='observed_raw','repairs':None if prof=='observed_raw' else {'odd_disk':'12->displayed coefficient at initial Cartesian stage','exponential':'cos² inside squared substituted x->cos'}.get(name)}}

# EASY: four observed whole-disk integral families; coefficient/radius variations
# retain polynomial powers, exp(r²) and source half-angle identity workload.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: three observed half/quarter disk families, unchanged trig/log workload.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: two observed translated semicircles; complete boundary conversion required.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty];records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 if args.format=='json':print(json.dumps(records,ensure_ascii=False,indent=2))
 else:
  for v in records:
   q=v['question'];print(q[':question/problem']);print('\n'.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']));print(q[':question/worked-solution'])
