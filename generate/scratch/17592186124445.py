#!/usr/bin/env python3
"""Local gradient-zero recipes. Public raw profiles preserve source anomalies.

No graph is assessed. Source mathematics is parameterized through complete
expression masks; source strings serve as fixed prose/layout templates, never
as an original-parameter answer branch. All finite samplers are enumerated.
"""
import argparse, hashlib, itertools, json, random, re, sys, uuid
from pathlib import Path
import sympy as S
ID=17592186124445
VERSION='gradient-zero-1'
HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
KP=SOURCE['record']
QS=KP[':knowledge-point/questions']
x,y,z=S.symbols('x y z',real=True)
NS=uuid.UUID('75784b57-0796-5e32-a08d-45838ac06e21')
FAMILIES=['quadratic','branch3','trig','coupled','entropy','logquad','reciprocal2','reciprocal3']
TEMPLATES=dict(zip(FAMILIES,QS))
LEVELS={'easy':['shifted_log'],'moderate':['quadratic','trig','coupled','logquad','reciprocal2'],'hard':['branch3','entropy','reciprocal3']}
ORIGINAL={'quadratic':dict(a=3,b=1,c=1),'branch3':dict(a=1,b=1,c=1),'trig':dict(b=1,k=1),'coupled':dict(k=2),'entropy':dict(d=1,e=1,f=1),'logquad':dict(a=2,b=3,c=1),'reciprocal2':dict(n=3,m=3),'reciprocal3':dict(p=1,q=1)}

def tex(v):
 return S.latex(S.sympify(v)).replace(r'\log',r'\ln').replace(r'\left', '').replace(r'\right','')
def coeff(n,t):return t if n==1 else tex(n)+t

def pt(*v):return '('+','.join(tex(i) for i in v)+')'
def txt(points,only=False):return ' and '.join('$'+pt(*p)+'$' for p in points)+(' only' if only else '')
def mask(t,rules):
 # One pass: never replace inside generated text, TeX commands or numeric slots.
 return re.sub('|'.join(re.escape(k) for k in sorted(rules,key=len,reverse=True)),lambda m:rules[m[0]],t)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(NS,v))


def domains(f,normal=True):
 if f=='shifted_log':return [dict(a=a,b=b) for a in range(-4,5) for b in range(-4,5)]
 if f=='quadratic':return [dict(a=a,b=b,c=c) for a in range(2,7) for b in range(1,5) for c in range(1,7) if S.gcd(a,S.gcd(b,c))==1]
 if f=='branch3':return [dict(a=a,b=b,c=c) for a in range(1,5) for b in range(1,5) for c in range(1,5) if S.gcd(a,S.gcd(b,c))==1]
 if f=='trig':return [dict(b=b,k=k) for b in range(1,7) for k in range(1,5)]
 if f=='coupled':return [dict(k=k) for k in range(1,13)]
 if f=='entropy':return [dict(d=d,e=e,f=f) for d,e,f in itertools.product(range(2 if normal else 1,5),repeat=3)]
 if f=='logquad':return [dict(a=a,b=b,c=c) for a in range(1,6) for b in range(1,9) for c in range(1,6)]
 if f=='reciprocal2':return [dict(n=n,m=m) for n in range(2,9) for m in range(1,9) if n*n%m==0 and n**3//m<=216]
 if f=='reciprocal3':return [dict(p=p,q=q) for p in range(1,9) for q in range(1,9)]
 raise ValueError('unknown template')

def build(f,p):
 """Return expression, roots, literal-source expression masks and bank objects.

 Each map entry is a whole mathematical component, including prose equations
 and concluding tuples. Unevaluated derivative/zero rows stay distinct.
 """
 R={}
 if f=='quadratic':
  a,b,c=[p[t] for t in 'abc'];r=S.Rational(c,2*a);s=S.Rational(c,2*b)
  E=coeff(a,'{x}^{2}')+'+'+coeff(b,'{y}^{2}')+'-'+coeff(c,'x')
  dx=coeff(2*a,'x')+'-'+str(c);dy=coeff(2*b,'y')
  R={'3{x}^{2}+{y}^{2}-x':E,'6x+0-1':coeff(2*a,'x')+'+0-'+str(c),'6x-1':dx,'0+2y-0':'0+'+dy+'-0','2y':dy,r'\frac{1}{6}':tex(r)}
  expr=a*x*x+b*y*y-c*x;roots=[(r,0)]
  raw=[(r,s),(s,r/2),(0,0),(r,0),(0,s)]
  bank=[(r,0),(2*r,0),(-r,0),(0,r),(r,s)]
 elif f=='branch3':
  a,b,c=[p[t] for t in 'abc'];r=-S.Rational(a,b)
  E=coeff(a,'xy')+'+'+coeff(b,'x{y}^{2}')+'+'+coeff(c,'{z}^{3}')
  dx=coeff(a,'y')+'+'+coeff(b,'{y}^{2}');dy=coeff(a,'x')+'+'+coeff(2*b,'xy');dz=coeff(3*c,'{z}^{2}')
  R={'xy+x{y}^{2}+{z}^{3}':E,'y+{y}^{2}':dx,'x+2xy':dy,'3{z}^{2}':dz,'y(1+y)':'y('+str(a)+'+'+coeff(b,'y')+')','y=-1':'y='+tex(r),'x+2x(0)':coeff(a,'x')+'+'+coeff(2*b,'x(0)'),'x+2x(-1)':coeff(a,'x')+'+'+coeff(2*b,'x('+tex(r)+')'),'(0,-1,0)':pt(0,r,0)}
  expr=a*x*y+b*x*y*y+c*z**3;roots=[(0,0,0),(0,r,0)]
  raw=[[roots[0],(r,r,r)],[(1,r,1)],[roots[1]],[roots[0]],roots]
  bank=[roots,[roots[0]],[roots[1]],[(0,-r,0)],[(r,r,r)]]
 elif f=='trig':
  b,k=p['b'],p['k'];ang=coeff(k,'y');cos=r'\operatorname{cos}⁡'+ang;sin=r'\operatorname{sin}⁡'+ang;yy=S.pi/(2*k)
  E='{x}^{2}-'+coeff(2*b,'x')+cos
  R={'{x}^{2}-2x\\operatorname{cos}⁡y':E,'2x-2\\operatorname{cos}⁡y':'2x-'+coeff(2*b,cos),'2x\\operatorname{sin}⁡y':coeff(2*b*k,'x')+sin,'2(x-\\operatorname{cos}⁡y)':'2(x-'+coeff(b,cos)+')','x=\\operatorname{cos}⁡y':'x='+coeff(b,cos),'2\\operatorname{cos}⁡y\\operatorname{sin}⁡y':coeff(2*b*b*k,cos)+sin,'\\operatorname{sin}⁡2y':coeff(b*b*k,r'\operatorname{sin}⁡'+coeff(2*k,'y')),r'\frac{\pi }{2}':tex(yy).replace(r'\pi}',r'\pi }'),r'0\le y<\pi':r'0\le y<'+tex(S.pi/k),'x=\\operatorname{cos}⁡0=1':'x='+coeff(b,r'\operatorname{cos}⁡0')+'='+str(b),'x=\\operatorname{cos}⁡('+r'\frac{\pi }{2}'+')=0':'x='+coeff(b,r'\operatorname{cos}⁡('+tex(k*yy).replace(r'\pi}',r'\pi }')+')')+'=0','(1,0)':pt(b,0),'(0,\\frac{\\pi }{2})':pt(0,yy).replace(r'\pi}',r'\pi }')}
  expr=x*x-2*b*x*S.cos(k*y);roots=[(b,0),(0,yy)]
  raw=[roots,[roots[0]],[roots[1]],[(b,yy)],[(-b,0),(b,yy)]];bank=raw
 elif f=='coupled':
  k=p['k'];E=coeff(2*k,'xy')+'+{y}^{2}-{x}^{2}';dx='2('+coeff(k,'y')+'-x)';dy='2('+coeff(k,'x')+'+y)'
  R={'4xy+{y}^{2}-{x}^{2}':E,'4y+0-2x':coeff(2*k,'y')+'+0-2x','4x+2y-0':coeff(2*k,'x')+'+2y-0','2(2y-x)':dx,'2(2x+y)':dy,'2y-x':coeff(k,'y')+'-x','2x+y':coeff(k,'x')+'+y','x=2y':'x='+coeff(k,'y'),'2(2y)+y':coeff(k,'('+coeff(k,'y')+')')+'+y','5y':coeff(k*k+1,'y'),'x=2\\cdot 0=0':'x='+str(k)+r'\cdot 0=0'}
  expr=2*k*x*y+y*y-x*x;roots=[(0,0)];raw=[(0,0),(-k,-1),(2*k,2),(2*k,-2),(k,1)]
  bank=[(0,0),(k,1),(-k,1),(1,-k),(1,k)]
 elif f=='entropy':
  d,e,h=p['d'],p['e'],p['f'];ds=[d,e,h];variables=['x','y','z']
  E='+'.join(v+r'\operatorname{ln}⁡'+v for v in variables)+''.join('-'+coeff(c,v) for c,v in zip(ds,variables))
  R={'x\\operatorname{ln}⁡x+y\\operatorname{ln}⁡y+z\\operatorname{ln}⁡z-x-y-z':E}
  for i,(v,c) in enumerate(zip(variables,ds)):
   original=[r'\operatorname{ln}⁡x+x\cdot \frac{1}{x}+0+0-1-0-0',r'0+\operatorname{ln}⁡y+y\cdot \frac{1}{y}+0-0-1-0',r'0+0+\operatorname{ln}⁡z+z\cdot \frac{1}{z}-0-0-1'][i]
   R[original]=original.replace('-1','-'+str(c))
   R[r'\operatorname{ln}⁡'+v+'+1-1']=r'\operatorname{ln}⁡'+v+'+1-'+str(c)
   # raw simple derivative occurs in formal input; whole formula mask protects it
   R[r'\operatorname{ln}⁡'+v]=r'\operatorname{ln}⁡'+v+('' if c==1 else '-'+str(c-1))
   R[v+'=1']=v+'='+tex(S.exp(c-1))
   if c!=1:R[r'\operatorname{ln}⁡'+v+r'\,'+'ijk'[i]]='('+r'\operatorname{ln}⁡'+v+'-'+str(c-1)+r')\,'+'ijk'[i]
  roots=[tuple(S.exp(c-1) for c in ds)];R['(1,1,1)']=pt(*roots[0])
  expr=x*S.log(x)+y*S.log(y)+z*S.log(z)-d*x-e*y-h*z
  raw=[(0,0,0),tuple(S.exp(c) for c in ds),tuple(S.exp(-c) for c in ds),(-1,-1,-1),roots[0]]
  bank=[roots[0],tuple(S.exp(-1) for c in ds),tuple(S.exp(c) for c in ds),tuple(S.exp(-c-1) for c in ds),tuple(S.exp(1-c) for c in ds)]
 elif f=='logquad':
  a,b,c=[p[t] for t in 'abc'];E=r'\operatorname{ln}⁡({x}^{2}+'+str(c)+')+'+coeff(a,'(y-'+str(b)+')^{2}')
  R={'\\operatorname{ln}⁡({x}^{2}+1)+2(y-3)^{2}':E,'\\operatorname{ln}⁡(x+1)+2(y-3)^{2}':E.replace('{x}^{2}','x'),r'\frac{1}{{x}^{2}+1}\cdot 2x+0':r'\frac{1}{{x}^{2}+'+str(c)+r'}\cdot 2x+0',r'\frac{2x}{{x}^{2}+1}':r'\frac{2x}{{x}^{2}+'+str(c)+'}','0+2\\cdot 2(y-3)':'0+'+str(a)+r'\cdot 2(y-'+str(b)+')','4(y-3)':str(2*a)+'(y-'+str(b)+')','y=3':'y='+str(b),'(0,3)':pt(0,b)}
  expr=S.log(x*x+c)+a*(y-b)**2;roots=[(0,b)]
  raw=[(0,0),(S.Rational(1,a),S.Rational(b,2*a)),(c,a),(b,0),roots[0]]
  bank=[roots[0],(0,0),(0,-b),(b,0),(0,S.Rational(b,2*a))]
 elif f=='reciprocal2':
  n,m=p['n'],p['m'];A=n**3//m;yy=-S.Rational(n*n,m)
  E=r'\frac{'+str(A)+r'}{y}-\frac{'+str(m)+r'y}{x}+x'
  R={r'\frac{9}{y}-\frac{3y}{x}+x':E,r'\frac{3y}{{x}^{2}}':r'\frac{'+str(m)+r'y}{{x}^{2}}',r'\frac{9}{{y}^{2}}':r'\frac{'+str(A)+r'}{{y}^{2}}',r'\frac{3}{x}':r'\frac{'+str(m)+'}{x}',r'\frac{3}{y}':r'\frac{'+str(m)+'}{y}',r'-\frac{{x}^{2}}{3}':r'-\frac{{x}^{2}}{'+str(m)+'}',r'\frac{9}{{(-\frac{{x}^{2}}{3})}^{2}}':r'\frac{'+str(A)+r'}{{(-\frac{{x}^{2}}{'+str(m)+'})}^{2}}',r'9\cdot {(-\frac{3}{{x}^{2}})}^{2}':str(A)+r'\cdot {(-\frac{'+str(m)+r'}{{x}^{2}})}^{2}',r'\frac{81}{{x}^{4}}':r'\frac{'+str(A*m*m)+r'}{{x}^{4}}',r'\frac{81+3{x}^{3}}{{x}^{4}}':r'\frac{'+str(A*m*m)+'+'+coeff(m,'{x}^{3}')+r'}{{x}^{4}}','81+3{x}^{3}':str(A*m*m)+'+'+coeff(m,'{x}^{3}'),'{x}^{3} & =-27':'{x}^{3} & =-'+str(n**3),'x & =-3':'x & =-'+str(n),'x=-3':'x=-'+str(n),r'y=-\frac{(-3)^{2}}{3}=-3':'y=-\\frac{(-'+str(n)+')^{2}}{'+str(m)+'}='+tex(yy),'(-3,-3)':pt(-n,yy)}
  expr=S.Rational(A)/y-m*y/x+x;roots=[(-n,yy)]
  raw=[[(n,-yy),(-n,yy)],[roots[0]],[(n,yy),(-n,-yy)],[(-n,-yy)],[(n,-yy)]];bank=raw
 elif f=='reciprocal3':
  p0,q=p['p'],p['q'];A=p0*q;E=r'\frac{'+str(A)+r'}{xy}+\frac{'+str(q)+r'}{y}+\frac{'+str(p0)+r'}{zx}-z'
  dx=r'-\frac{'+coeff(A,'z')+'+'+coeff(p0,'y')+r'}{{x}^{2}yz}'
  dy=r'-\frac{'+str(A)+'+'+coeff(q,'x')+r'}{x{y}^{2}}';dz=r'-\frac{'+str(p0)+r'+{z}^{2}x}{{z}^{2}x}'
  R={r'\frac{1}{xy}+\frac{1}{y}+\frac{1}{zx}-z':E,r'-\frac{1}{{x}^{2}y}+0-\frac{1}{z{x}^{2}}-0':r'-\frac{'+str(A)+r'}{{x}^{2}y}+0-\frac{'+str(p0)+r'}{z{x}^{2}}-0',r'-\frac{1}{x{y}^{2}}-\frac{1}{{y}^{2}}+0-0':r'-\frac{'+str(A)+r'}{x{y}^{2}}-\frac{'+str(q)+r'}{{y}^{2}}+0-0',r'0+0-\frac{1}{{z}^{2}x}-1':r'0+0-\frac{'+str(p0)+r'}{{z}^{2}x}-1',r'-\frac{z+y}{{x}^{2}yz}':dx,r'-\frac{1+x}{x{y}^{2}}':dy,r'-\frac{1+{z}^{2}x}{{z}^{2}x}':dz,'x=-1':'x=-'+str(p0),r'-\frac{1+{z}^{2}(-1)}{{z}^{2}(-1)}':r'-\frac{'+str(p0)+r'+{z}^{2}(-'+str(p0)+r')}{{z}^{2}(-'+str(p0)+')}',r'-\frac{z+y}{(-1)^{2}yz}':r'-\frac{'+coeff(A,'z')+'+'+coeff(p0,'y')+'}{(-'+str(p0)+r')^{2}yz}','z+y & =0':coeff(A,'z')+'+'+coeff(p0,'y')+' & =0','y & =-z':'y & =-'+coeff(q,'z'),'y=-1':'y=-'+str(q),'y=1':'y='+str(q),'(-1,-1,1)':pt(-p0,-q,1),'(-1,1,-1)':pt(-p0,q,-1)}
  expr=S.Rational(A)/(x*y)+S.Rational(q)/y+S.Rational(p0)/(z*x)-z;roots=[(-p0,-q,1),(-p0,q,-1)]
  raw=[[roots[0]],[(-p0,-q,-1),(-p0,q,1)],roots,[roots[1]],[(p0,-q,-1),(p0,q,1)]];bank=raw
 else:raise ValueError(f)
 # Formats retain complete original banks at source parameters; opaque scalar
 # recipes only describe the observed algebraic pattern, never inferred intent.
 textbank=f in ('branch3','trig','reciprocal2','reciprocal3')
 if textbank:
  rawvalues=[txt(v,len(v)==1) for v in raw];bankvalues=[txt(v,len(v)==1) for v in bank]
 else:
  rawvalues=[pt(*v) for v in raw];bankvalues=[pt(*v) for v in bank]
 if f=='entropy':rawvalues[2]='('+','.join(r'\frac{1}{'+tex(S.exp(c))+'}' for c in ds)+')'
 return expr,roots,R,rawvalues,bankvalues


def repaired(f,t):
 # Exact raw evidence is kept separately. These corrections have independent
 # derivative/gradient verification; the naked brace is an ord-123 literal.
 t=t.replace('{\\begin{aligned}',r'\{\begin{aligned}')
 if f in ('branch3','entropy','reciprocal3'):t=t.replace(r'0\text{ }i+0\text{ }j+0\text{ }j',r'0\text{ }i+0\text{ }j+0\text{ }k')
 if f=='branch3':t=t.replace('∇f(x,y,z)','∇h(x,y,z)')
 if f=='trig':t=t.replace('∇h(x,y)','∇f(x,y)')
 if f=='logquad':
  # The only derivative-input typo: ln(x+c), while actual input is ln(x²+c).
  t=re.sub(r'\\operatorname\{ln\}⁡\(x\+(\d+)\)',r'\\operatorname{ln}⁡({x}^{2}+\1)',t)
 if f=='reciprocal2':
  # Only the first displayed gradient has the typo; subsequent system is right.
  t=re.sub(r'(Hence, .*?\\frac\{\d+\})\{y\}(\)j)',r'\1{x}\2',t)
 return t


def easy_build(p):
 a,b=p['a'],p['b'];X=tex(x-a);Y=tex(y-b);E='('+Y+r')\ln ('+X+')';P=pt(a+1,b)
 prompt='Given that $f(x,y)= '+E+r',$ find the points $(x, y)$ where $\nabla f(x,y) = \mathbf 0.$'
 solution=("First, we find the partial derivatives: \n\n$$\n"+r'\begin{aligned}\frac{∂f}{∂x} & =\frac{∂}{∂x}('+E+') '+r'\\  & =\frac{'+Y+'}{'+X+'} '+r'\\ \frac{∂f}{∂y} & =\frac{∂}{∂y}('+E+') '+r'\\  & =\ln('+X+r')\end{aligned}'+'\n$$\n\nSo, we have\n\n$$\n'+r'\nabla f(x,y) = \dfrac {'+Y+'}{'+X+r'} \, \mathbf i + \ln('+X+r') \, \mathbf j.'+'\n$$\n\nNow, we solve $'+r'\nabla f(x,y) = \mathbf 0\mathbin{:}$'+'\n\n$$\n'+r'\dfrac {'+Y+'}{'+X+r'} \, \mathbf i + \ln('+X+r') \, \mathbf j = 0 \mathbf i + 0\mathbf j'+'\n$$\n\nBy equating the coefficients of $'+r'\mathbf{i}$ on both sides of the equation (and similarly with $\mathbf{j}$), we obtain'+'\n\n$$\n'+r'\{\begin{aligned}\frac{'+Y+'}{'+X+r'}=0 \\ \ln('+X+r')=0.\end{aligned}'+'\n$$\n\nFrom the first equation, we get $'+Y+'=0,$ which means $y='+str(b)+'.$ From the second equation, we obtain $'+r'\ln('+X+')=0,$ which means that $x='+str(a+1)+'.$\n\nTherefore, $'+r'\nabla f(x,y) =\mathbf 0$ at the point $'+P+'.$')
 bank=[P,pt(a,b),pt(a-1,b),pt(a+1,-b),pt(b,a+1)]
 # b=0 sign-reversal collides: choose eligible complete bank before parameters.
 # Canonical profile replaces sign-reversal with omitted y shift; b must nonzero.
 bank=[P,pt(a,b),pt(a-1,b),pt(a+1,0),pt(a+1,-b)]
 return prompt,solution,(y-b)*S.log(x-a),[(a+1,b)],bank


def assemble(level,f,p,seed,profile):
 if f=='shifted_log':
  problem,solution,expr,roots,values=easy_build(p);answer_type='math';raw=False;origin='authored_missing_easy'
 else:
  expr,roots,rules,rawvalues,defaultvalues=build(f,p);q=TEMPLATES[f];raw=profile=='raw_'+f
  problem=mask(q[':question/problem'],rules);solution=mask(q[':question/worked-solution'],rules)
  if not raw:solution=repaired(f,solution)
  values=rawvalues if raw else defaultvalues
  answer_type='text' if f in ('branch3','trig','reciprocal2','reciprocal3') else 'math'
  origin='observed_raw_pattern' if raw else 'authored_method_bank' if f in ('quadratic','coupled','entropy','logquad','branch3') else 'source_shaped_method_bank'
 # historical double spaces and raw fraction spelling are retained from source
 if raw:
  old=TEMPLATES[f][':question/answer-fields'][0][':answer-field/choices']
  # Choice prose/layout is itself a parameterized mask. Mask original tuple
  # components using formula-generated raw values mapped by index, not values lookup.
  values=[v for v in values]
  for i,(o,v) in enumerate(zip(old,values)):
   if f=='branch3' and i==0:v=v.replace(' and $',' and  $')
   # source pi-space syntax is different from SymPy; mathematical values remain exact
   if f=='trig':v=v.replace(r'\frac{\pi}{2}',r'\frac{\pi }{2}')
   values[i]=v
 if len(set(values))!=5:raise ValueError('whole bank rejected: exact collision')
 correct_index={'quadratic':3,'branch3':4,'trig':0,'coupled':0,'entropy':4,'logquad':4,'reciprocal2':1,'reciprocal3':2}.get(f,0) if raw else {'reciprocal2':1,'reciprocal3':2}.get(f,0)
 mathfp=digest({'expression':str(expr),'domain':domain(f,p),'skill':'gradient-zero','level':level})
 # Exclude unused/common overall polynomial scaling from mathematical fingerprint.
 if f in ('quadratic','branch3'):
  poly=S.Poly(expr,x,y,z);lc=poly.LC();mathfp=digest({'normalized_expression':str(S.expand(expr/lc)),'domain':domain(f,p),'skill':'gradient-zero','level':level})
 cid=digest({'version':VERSION,'level':level,'problem':problem,'solution':solution,'bank':sorted(zip(values,[i==correct_index for i in range(5)]))})
 fieldid=uid(cid+':field');answers=[{':answer/id':uid(fieldid+':'+v),':answer/type':':answer.type/'+answer_type,':answer/value':v} for v in values]
 correct=answers[correct_index][':answer/id'];random.Random(seed).shuffle(answers)
 question={':question/id':uid(cid),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fieldid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':question,'generation':{'version':VERSION,'basis':SOURCE['basis'],'database':SOURCE['database'],'lineage':SOURCE['lineage'],'seed':seed,'template':f,'parameters':p,'bank_profile':profile,'origin':origin,'evidence_only':raw,'eligible_for_learning':not raw,'domain':domain(f,p),'mathematical_fingerprint':mathfp,'content_fingerprint':cid,'source_id':TEMPLATES[f][':db/id'] if f in TEMPLATES else None,'python':sys.version.split()[0],'sympy':S.__version__}}

def domain(f,p):
 if f=='shifted_log':return 'x>'+str(p['a'])
 if f=='trig':return '0<=y<'+str(S.pi/p['k'])
 if f=='entropy':return 'x>0,y>0,z>0'
 if f=='reciprocal2':return 'x!=0,y!=0'
 if f=='reciprocal3':return 'x!=0,y!=0,z!=0'
 return 'all real coordinates'

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio supported')
 if profile and profile.startswith('raw_'):template=template or profile[4:]
 if template is not None and template not in LEVELS[level]:raise ValueError('template outside level')
 rng=random.Random(seed);f=template or rng.choice(LEVELS[level]);profile=profile or 'method_'+f
 if profile not in ('raw_'+f,'method_'+f) or f=='shifted_log' and profile.startswith('raw_'):raise ValueError('profile mismatch')
 raw=profile.startswith('raw_');catalog=domains(f,not raw)
 if parameters is not None:
  if not isinstance(parameters,dict) or any(type(v) is not int for v in parameters.values()):raise ValueError('parameters must be exact integers')
  if parameters not in catalog:raise ValueError('parameters outside finite equal-workload domain')
  return assemble(level,f,dict(parameters),seed,profile)
 for _ in range(256):
  p=rng.choice(catalog)
  try:return assemble(level,f,p,seed,profile)
  except ValueError:pass
 raise ValueError('no collision-free whole bank')

# EASY — authored canonical shifted logarithm; two independent equations,
# one ln(argument)=0 evaluation; no branches, no other gradient skill.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — five observed independent families. Source labels are preserved;
# source workloads include the trig pair and reciprocal cubic substitution.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — three observed 3-coordinate families. Every partial, zero contribution,
# simultaneous equation, substitution branch and returned point is retained.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0];lines=[q[':question/problem'],'']
 for a in f[':answer-field/choices']:lines.append('- '+(a[':answer/value'] if a[':answer/type'].endswith('/text') else '$'+a[':answer/value']+'$'))
 lines+=['','Correct: '+next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]),'',q[':question/worked-solution']]
 return '\n'.join(lines)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['all',*LEVELS],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--format',choices=['json','markdown'],default='markdown');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 if a.difficulty=='all' and (a.template or a.profile):ap.error('select a level for explicit template/profile')
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (LEVELS if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])

if __name__=='__main__':main()
