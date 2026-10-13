#!/usr/bin/env python3
"""Tangent vectors to coordinate-plane slices of z=f(x,y), frozen math basis1356.

All fifteen observed practice ENUMs are hard. Easy (constant supplied partial)
and moderate (one coordinate multiplication) are authored, justified in classification.
Hard serves ALL fifteen observed derivative families with a common coefficient
1..9 (no extra differentiation, new functions, or parameterized-space-curve task).
Raw source profiles are evidence-only; z translation is a genuine mathematical
parameterization, keeping tangent banks invariant. Normal hard profiles preserve
family substitution/evaluation chains and source shared prose while correcting
stale points/planes and the unmatched literal system brace. Historical opaque
banks are never used for learner sampling. Five method-derived options are a
complete bank: tangent; reverse vertical sign; swap slope components; normal to
slice; normal to tangent-line plane. Entire instance rejected on direction collision.

CLI and generate API are review-only, no database writes, no engine edits.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186124439
ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
KP=CAPTURE['record']; TITLE=KP[':knowledge-point/title']; VERSION='tangent-vector-1'
X,Y,Z=sp.symbols('x y z',real=True)
# Independent symbolic definitions transcribed from actual printed derivatives.
SPECS=[
 ('linear_x','y',(2,-3,3),6*(X-1)),
 ('factored_y','x',(1,-1,2),X**2*(2*X*Y-1)),
 ('exp_cos_x','y',(2,1,4),sp.exp(Y-1)+2*X*sp.cos(Y-1)),
 ('polynomial_y','x',(-2,2,3),X**2*Y+2*X-Y),
 ('log_polynomial_x','y',(0,1,7),X**2+Y**2-sp.log(X+Y)),
 ('exp_cos_y','x',(1,0,-1),X*sp.exp(X*Y)-2*sp.cos(Y)),
 ('affine_x','y',(1,1,1),2*(X+Y)-2),
 ('radical_y','x',(-2,-6,1),(Y-X)/sp.sqrt(X*(Y+X))),
 ('exp_log_x','y',(-1,1,-1),3*sp.exp(X+Y)-sp.log(sp.Abs(X*Y))),
 ('quotient_y','x',(-1,0,sp.Rational(1,2)),X*(Y-X)/(2*X*(Y+1))),
 ('trig_difference_y','x',(sp.pi/2,1,0),2*sp.sin(X*Y)-sp.cos(sp.pi*Y/2)),
 ('trig_product_y','x',(-sp.pi/2,0,2),sp.sin(X)*sp.cos(Y)/2),
 ('trig_product_x','y',(1,sp.pi/4,0),sp.sqrt(2)*sp.sin(2*Y)*sp.cos(Y)),
 ('log_cube_y','x',(1,0,-1),3*sp.log(Y+1)-(X+Y)**3),
 ('radical_x','y',(4,5,-2),sp.sqrt(Y**2-X**2)/(2*X-Y))]
TEMPLATES={}
for s,q in zip(SPECS,KP[':knowledge-point/questions']):
 name,plane,point,derivative=s
 TEMPLATES[name]={'level':'hard','plane':plane,'point':tuple(map(sp.sympify,point)),
 'derivative':derivative,'source':q}
TEMPLATES['constant']={'level':'easy'};TEMPLATES['scaled_coordinate']={'level':'moderate'}

def tex(e):return sp.latex(sp.sympify(e)).replace(r'\log',r'\ln')
def vector(v):return '⟨'+','.join(tex(a) for a in v)+'⟩'
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def digest(o):return hashlib.sha256(json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def parallel(a,b):
 a,b=sp.Matrix(a),sp.Matrix(b)
 return a!=sp.zeros(3,1) and b!=sp.zeros(3,1) and all(sp.simplify(x)==0 for x in a.cross(b))
def parse_math(s):
 """Small exact TeX parser for this closed family's printed arithmetic; no proxy metadata."""
 s=s.strip().rstrip('.,:').replace('⁡','').replace(r'\,','').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\{([ef])\}',r'\1',s)
 s=s.replace(r'\operatorname{sin}','sin').replace(r'\operatorname{cos}','cos').replace(r'\operatorname{ln}','log')
 s=s.replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\ln','log').replace(r'\log','log')
 s=s.replace(r'\pi','pi')
 def group_at(t,i):
  assert t[i]=='{',t
  n=1;j=i+1
  while n:
   if t[j]=='{':n+=1
   if t[j]=='}':n-=1
   j+=1
  return t[i+1:j-1],j
 while r'\frac' in s or r'\sqrt' in s:
  # outermost first; recurse through complete groups
  m=re.search(r'\\(frac|sqrt)',s);i=m.start();k=m.end()
  while s[k].isspace():k+=1
  a,j=group_at(s,k)
  if m.group(1)=='frac':
   while s[j].isspace():j+=1
   b,j=group_at(s,j);v='(('+str(parse_math(a))+')/('+str(parse_math(b))+'))'
  else:v='sqrt('+str(parse_math(a))+')'
  s=s[:i]+v+s[j:]
 s=re.sub(r'log\s*\|([^|]*)\|',r'log(Abs(\1))',s)
 s=re.sub(r'\|([^|]*)\|',r'Abs(\1)',s)
 s=s.replace('{','(').replace('}',')').replace('^','**')
 # Function atoms without parentheses in source: cos0, sin(pi/4), cos y.
 s=re.sub(r'(sin|cos|log)\s*(0|1|x|y)(?![a-z])',r'\1(\2)',s)
 s=re.sub(r'(sin|cos)\s*(x|y)(?=(sin|cos))',r'\1(\2)',s)
 s=re.sub(r'(?<=\d)(?=[ijk])','*',s)
 s=re.sub(r'(?<=[0-9xyz)])(?=(sin|cos|log|Abs|sqrt))','*',s)
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
 return parse_expr(s,local_dict={'x':X,'y':Y,'z':Z,'e':sp.E,'pi':sp.pi},transformations=standard_transformations+(implicit_multiplication_application,convert_xor),evaluate=True)
def parse_vector(s):
 if s.startswith('⟨'):return tuple(parse_math(x) for x in s[1:-1].split(','))
 i,j,k=sp.symbols('i j k');e=parse_math(s)
 return tuple(sp.expand(e).coeff(v) for v in (i,j,k))
def bank(m,plane):
 v=(1,0,m) if plane=='y' else (0,1,m)
 rev=(1,0,-m) if plane=='y' else (0,1,-m)
 swap=(m,0,1) if plane=='y' else (0,m,1)
 n1=(0,1,0) if plane=='y' else (1,0,0)
 n2=(m,0,-1) if plane=='y' else (0,m,-1)
 vs=[v,rev,swap,n1,n2]
 if any(parallel(a,b) for i,a in enumerate(vs) for b in vs[i+1:]):raise ValueError('whole bank has direction collision')
 return list(map(vector,vs)),0

def make_record(level,seed,template,p,profile,prompt,solution,values,correct,extra):
 # Display bank order excluded; level included. Full mathematical fingerprint excludes height/bank.
 fingerprint=digest(extra.pop('task'))
 identity=digest({'version':VERSION,'difficulty':level,'prompt':prompt,'solution':solution,
                  'bank':sorted(values),'correct':values[correct]})
 fid=uid(identity+'/field/selection')
 answers=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 correct_id=answers[correct][':answer/id'];random.Random(seed).shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',
        ':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':TITLE},
 'question':{':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,
 ':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]},
 'generation':{'version':VERSION,'template':template,'profile':profile,'seed':seed,'parameters':{k:(int(v) if isinstance(v,sp.Integer) else str(v) if isinstance(v,sp.Basic) else v) for k,v in p.items()},
 'content_fingerprint':identity,'mathematical_fingerprint':fingerprint,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},
 'python':sys.version.split()[0],'sympy':sp.__version__,'plots':[] ,**extra}}

def raw_source(level,seed,name,p):
 """Extracted text masks parameterize vertical translation h, not source payload branching."""
 d=TEMPLATES[name];q=d['source'];h=sp.sympify(p.get('h',0))
 if set(p)-{'h'} or not h.is_Integer or abs(h)>9:raise ValueError('raw h integer -9..9 only')
 xyz=d['point'];oldpoint=re.search(r'P\((.*?)\)',q[':question/problem']).group(0)
 newpoint='P('+','.join([oldpoint[2:-1].rsplit(',',1)[0],tex(xyz[2]+h)])+')' if h else oldpoint
 prompt=q[':question/problem'].replace(oldpoint,newpoint)
 sol=q[':question/worked-solution'].replace(oldpoint,newpoint)
 # Complete math fragments containing explicit z transform as an affine coordinate;
 # formal z-f stays formal since f refers to the translated surface.
 def trans(m):
  text=m.group(0)
  if not h:return text
  return re.sub(r'(?<![A-Za-z])z(?![A-Za-z]|-f)',lambda _:r'\left(z-('+tex(h)+r')\right)',text)
 sol=re.sub(r'\$\$.*?\$\$|\$(?!\$).*?\$',trans,sol,flags=re.S)
 f=q[':question/answer-fields'][0];vals=[a[':answer/value'] for a in f[':answer-field/choices']]
 ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][':answer/id'])
 return make_record(level,seed,name,{'h':int(h)},'source',prompt,sol,vals,ci,
 {'evidence_only':True,'eligible_for_learning':False,'source_id':q[':db/id'],
 'task':{'derivative':str(d['derivative']),'substitution':{str(v):str(t) for v,t in zip((X,Y),xyz[:2]) if v in d['derivative'].free_symbols},'plane':d['plane']}})

def block(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def tail(plane,point,m,style='tuple',dist=False,negrow=False,source_n2=None,tuple_cross=True,stage3='distribute'):
 a,b,z0=point; w=X if plane=='y' else Y;w0=a if plane=='y' else b
 line=sp.expand(m*(w-w0)+z0);lt=tex(line);plane_eq=plane+'='+tex(b if plane=='y' else a)
 n1=sp.Matrix((0,1,0) if plane=='y' else (1,0,0))
 n2=sp.Matrix((m,0,-1) if plane=='y' else (0,m,-1)) if source_n2 is None else sp.Matrix(source_n2)
 cross=n1.cross(n2);v=sp.Matrix((1,0,m) if plane=='y' else (0,1,m))
 def basis(t):
  return tex(t[0]*sp.Symbol('i')+t[1]*sp.Symbol('j')+t[2]*sp.Symbol('k'))
 answer=vector(v) if style=='tuple' else basis(v)
 pt='P('+','.join(tex(x) for x in point)+')';xy=','.join(tex(x) for x in point[:2]);var=str(w)
 delta=var+'-('+tex(w0)+')';lhs='z-('+tex(z0)+')'
 rows=[r'z-f('+xy+') & ={f}_{'+var+'}('+xy+')('+delta+')',lhs+' & =('+tex(m)+')('+delta+')']
 if dist:
  third_lhs=tex(Z-z0) if stage3 in ('sign','sign_distribute') else lhs
  third_rhs='('+tex(m)+')('+delta+')' if stage3=='sign' else tex(m*w-m*w0)
  rows.append(third_lhs+' & ='+third_rhs)
 rows.append('z & ='+lt)
 equation=tex(sp.expand(n2[0]*X+n2[1]*Y+n2[2]*Z-n2[2]*(z0-m*w0)))+'=0'
 determinant=r'\left|\begin{aligned}i & j & k \\ '+ ' & '.join(tex(x) for x in n1)+r' \\ '+' & '.join(tex(x) for x in n2)+r'\end{aligned}\right|'
 cr=[r'{n}_{1}\times {n}_{2} & ='+vector(n1)+r'\times '+vector(n2),' & ='+determinant,' & ='+basis(cross)]
 if tuple_cross:cr.append(' & ='+vector(cross))
 sol='Now, we use the point-slope form of a straight line:\n\n'+block(rows)+'\n\n'
 sol+='Therefore, the tangent line to the curve $C$ at $'+pt+'$ can be given as the intersection of two planes:\n\n'
 sol+=block([r'\{'+plane_eq+r' \\ z='+lt])+'\n\nNext, notice that:\n\n'
 sol+='- For the plane $'+plane_eq+',$ a normal vector to the plane is ${n}_{1}='+vector(n1)+'.$\n\n'
 sol+='- For the plane $z='+lt+'$ (or $'+equation+'$), a normal vector to the plane is ${n}_{2}='+vector(n2)+'.$\n\n'
 sol+='Finally, to find a direction vector for the tangent line, we calculate the cross product of these normal vectors:\n\n'+block(cr)+'\n\n'
 if plane=='y':
  cv=vector(cross) if style=='tuple' else basis(cross)
  sol+='Finally, since $'+cv+'$ is parallel to the tangent line, then $-('+cv+')='+answer+'$ is also parallel to it.'
 else:sol+='Therefore, a tangent vector to $C$ at $P$ is $'+(vector(cross) if style=='tuple' else basis(cross))+'.$'
 return sol

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio shape')
 rng=random.Random(seed);name=template or rng.choice([n for n,d in TEMPLATES.items() if d['level']==level])
 if name not in TEMPLATES or TEMPLATES[name]['level']!=level:raise ValueError('template level mismatch')
 profile=profile or 'method';p=dict(parameters) if parameters is not None else None
 if profile=='source':
  if level!='hard':raise ValueError('source only hard')
  return raw_source(level,seed,name,p or {'h':0})
 if profile!='method':raise ValueError('unknown complete bank')
 for attempt in range(100):
  d=TEMPLATES[name]
  if level=='hard':
   p=p if p is not None else {'c':rng.choice(range(2,10)),'h':rng.randint(-4,4)}
   if set(p)!={'c','h'}:raise ValueError('hard c,h required')
   c,h=map(sp.sympify,(p['c'],p['h']))
   if not c.is_Integer or not 1<=c<=9 or not h.is_Integer or abs(h)>9:raise ValueError('hard bounds')
   plane=d['plane'];pt=d['point'];point=(pt[0],pt[1],pt[2]+h);deriv=c*d['derivative']
   m=sp.simplify(deriv.subs({X:point[0],Y:point[1]}))
   if m in (-1,0,1):
    if parameters is not None:raise ValueError('method bank ineligible for slope -1,0,1')
    p=None;continue
   q=d['source'];prompt=q[':question/problem'];oldpoint=re.search(r'P\((.*?)\)',prompt).group(0)
   newpt='P('+','.join(tex(x) for x in point)+')'
   oldderiv=re.search(r'and that (.*?)\$, which',prompt).group(1)
   oldrhs=oldderiv.split('=',1)[1]
   newrhs=oldrhs if c==1 else tex(c)+r'\left('+oldrhs+r'\right)'
   prompt=prompt.replace(oldpoint,newpt).replace(oldderiv,oldderiv.split('=',1)[0]+'='+newrhs)
   oldsol=q[':question/worked-solution'];first=re.search(r'\$\$.*?\$\$',oldsol,re.S).group(0)
   # Preserve every original evaluation row, including same-line evaluation.
   parts=first.split('& =');prefix=parts[0];rhs=parts[1:]
   if len(rhs)==1 and '=' in rhs[0].split(r'\end')[0]:
    body,ending=rhs[0].split(r'\end',1);a,b=body.rsplit('=',1)
    evalblock=prefix+'& ='+(a if c==1 else tex(c)+r'\left('+a+r'\right)')+'='+tex(m)+r'\end'+ending
   else:
    new=[]
    for i,t in enumerate(rhs):
     if i==len(rhs)-1:new.append(tex(m)+r'\end'+t.split(r'\end',1)[1]);continue
     body,ending=t.rsplit(r'\\',1)
     new.append((body if c==1 else tex(c)+r'\left('+body.strip()+r'\right)')+r' \\'+ending)
    evalblock=prefix+'& ='+ '& ='.join(new)
   head=oldsol[:oldsol.index(first)]+evalblock+'\n\n \n\n'
   allblocks=re.findall(r'\$\$.*?\$\$',oldsol,re.S)
   second=allblocks[1];dist=second.count(r'\\')==3
   style='tuple' if f"⟨" in q[':question/answer-fields'][0][':answer-field/correct'][':answer/value'] else 'basis'
   normal=re.search(r'\{n\}_\{2\}=⟨([^⟩]*)⟩',oldsol)
   n2=tuple(parse_math(x) for x in normal.group(1).split(','));n2=(c*n2[0],c*n2[1],n2[2])
   stage3='sign' if name in ('log_cube_y','radical_x') else ('sign_distribute' if name=='exp_log_x' else 'distribute')
   solution=head+tail(plane,point,m,style,dist,source_n2=n2,tuple_cross=(allblocks[-1].count('& =')==4),stage3=stage3)
   source_ids=[q[':db/id']];task={'plane':plane,'substitution':{str(v):str(t) for v,t in zip((X,Y),point[:2]) if v in deriv.free_symbols},'derivative':str(deriv)}
  else:
   p=p if p is not None else {'plane':rng.choice(['x','y']),'a':rng.choice(list(range(-9,-1))+list(range(2,10))),
       'x':rng.choice([-4,-3,-2,-1,1,2,3,4]),'y':rng.choice([-4,-3,-2,-1,1,2,3,4]),'z':rng.randint(-4,4)}
   if set(p)!={'plane','a','x','y','z'} or p['plane'] not in ('x','y'):raise ValueError('authored parameters')
   for k in ('a','x','y','z'):
    if not isinstance(p[k],int) or abs(p[k])>(9 if k=='a' else 4) or (k!='z' and p[k]==0):raise ValueError('authored signed integer bounds')
   if abs(p['a'])<2:raise ValueError('coefficient magnitude 2..9')
   plane=p['plane'];point=tuple(sp.Integer(p[k]) for k in ('x','y','z'));w=X if plane=='y' else Y;w0=point[0] if plane=='y' else point[1]
   deriv=sp.Integer(p['a']) if level=='easy' else p['a']*w
   if level=='moderate' and abs(w0)<2: 
    if parameters is not None:raise ValueError('moderate nonunit coordinate required')
    p=None;continue
   m=sp.simplify(deriv.subs({X:point[0],Y:point[1]}))
   if m in (-1,0,1):
    if parameters is not None:raise ValueError('method bank ineligible')
    p=None;continue
   v=str(w);eq=plane+'='+tex(point[1] if plane=='y' else point[0]);xy=','.join(tex(t) for t in point[:2])
   derivative_tex=tex(deriv) if level=='easy' else '('+tex(p['a'])+')'+v
   prompt='The curve $C$ is the intersection of a surface $S,$ defined by $z=f(x,y),$ with the plane $'+eq+'.$ Given that the point $P('+','.join(tex(t) for t in point)+')$ lies on $C$, and that ${f}_{'+v+'}='+derivative_tex+'$, which of the following gives a tangent vector to $C$ at $P?$'
   evaluation=tex(m) if level=='easy' else '('+tex(p['a'])+')('+tex(w0)+')='+tex(m)
   head='The curve $C$ is the intersection of the surface with the plane $'+eq+'.$ Hence, the slope of the tangent to the curve $C$ at the point $P$ will be given by the partial derivative ${f}_{'+v+'}('+xy+').$ \n\n'
   head+='To get the slope, we evaluate the partial derivative ${f}_{'+v+'}(x,y)$ at $('+xy+'):$\n\n'+block([r'{f}_{'+v+'}('+xy+') & ='+evaluation])+'\n\n \n\n'
   solution=head+tail(plane,point,m,'tuple',dist=True);source_ids=[];task={'plane':plane,'derivative':str(deriv),'substitution':{str(w):str(w0)}}
   if level=='easy':task={'plane':plane,'slope':str(m)}
  values,ci=bank(m,plane)
  return make_record(level,seed,name,p,profile,prompt,solution,values,ci,
  {'evidence_only':False,'eligible_for_learning':True,'source_ids':source_ids,'authored':level!='hard',
   'task':task,'domain':'Real neighborhood of the supplied point; radical denominator and logarithm inputs valid.',
   'criterion':'any nonzero vector parallel to the tangent line; no orientation or unit requirement'})
 raise ValueError('no eligible whole bank after 100 samples')

# Easy: already supplied constant slope; cross normals, no differentiation.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: one coordinate multiplication with |coordinate|≥2; no zero slope/reduction to easy.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: actual observed labels; all fifteen families served with familiar eval anchors.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 rs=[generate(level,a.seed+i,template=a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(rs,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
