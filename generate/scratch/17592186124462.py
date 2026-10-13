#!/usr/bin/env python3
"""Plane-curve normal lines; steps 3–7 only, math basis 1356.
Observed profiles are public evidence-only affine-coordinate recipes. Normal
profiles are complete method-derived banks. Easy is explicitly authored; moderate
retains all observed function families; hard retains the observed axis cases.
No plots occur in this KP's practice/canonical questions. No database operations.
"""
from pathlib import Path
import argparse,copy,hashlib,json,random,re,sys,uuid
import sympy as s
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text())
KP=SOURCE['record']; ID=17592186124462; VERSION='plane-normal-1'
x,y=s.symbols('x y',real=True)
QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
# f, original level value, original point, original prompt sides.
DATA={
'q-36339':(5*x*x+y*y-6*x*y,0,(1,1),6*x*y,5*x*x+y*y),
'q-65173':(x*x+y*y-x*y,7,(2,-1),x*y,x*x+y*y-7),
'q-130718':(x*x-3*y*y,6,(3,1),x*x-3*y*y,s.Integer(6)),
'q-130723':(4*x*y+2*x*x-x-2*y,0,(2,-1),4*x*y+2*x*x,x+2*y),
'q-130724':(s.sqrt(x*x+y*y)-2*y+x,-2,(0,2),s.sqrt(x*x+y*y),2*y-x-2),
'q-36347':(2*x*y+6*y*y-x,-2,(8,-3),2*x*y+6*y*y,x-2),
'q-71385':(x*x+y*y,4,(2,0),x*x+y*y,s.Integer(4)),
'q-71388':(s.sqrt(x*x-y*y)-2*x-y,-1,(1,0),2*x+y-1,s.sqrt(x*x-y*y)),
'q-71390':(y*y+3*x*x-4*x*y,0,(-1,-3),y*y+3*x*x,4*x*y),
'q-71393':(s.log(x+y)-2*x*y,0,(0,1),s.log(x+y),2*x*y),
'q-71394':(y*y/16-x*x/9,1,(0,4),y*y/16-x*x/9,s.Integer(1)),
'q-71386':(x*x/9+y*y,1,(3,0),x*x/9+y*y,s.Integer(1)),
'q-71389':(s.cos(x*y)-x*x-y,0,(-1,0),s.cos(x*y),x*x+y),
'q-130719':(s.log(x/(2*y))-2*y+x,0,(2,1),2*y-x,s.log(x/(2*y))),
'q-130721':(s.exp(x*x*y)-y*y+x**3,9,(2,0),s.exp(x*x*y),y*y-x**3+9)}
HARD=['q-71385','q-71394','q-71386']; MOD=[k for k in DATA if k not in HARD]
TEMPLATES={'easy_quadratic':'easy',**{k:('hard' if k in HARD else 'moderate') for k in DATA}}
def tex(v): return s.latex(v,fold_short_frac=False).replace('\\log','\\ln')
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,default=str).encode()).hexdigest()
def uid(v): return str(uuid.uuid5(uuid.NAMESPACE_URL,digest(v)))
def line(a,b,p,q): return s.expand(b*(x-p)-a*(y-q))
def key(e):
 e=s.Poly(s.expand(e),x,y);cs=e.coeffs();return tuple(s.simplify(c/cs[0]) for c in [e.coeff_monomial(x),e.coeff_monomial(y),e.coeff_monomial(1)])
def equation(e):
 e=s.expand(e); den=s.ilcm(1,*[v.q for v in s.Poly(e,x,y).coeffs()]);e=s.expand(e*den)
 nums=[abs(int(v)) for v in s.Poly(e,x,y).coeffs()]; g=s.igcd(*nums) if len(nums)>1 else nums[0];e=e/g
 if s.Poly(e,x,y).coeffs()[0]<0:e=-e
 return tex(e)+'=0'
def block(rows):return '$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$'
def gradienttex(a,b):return '('+tex(a)+r')\,i+('+tex(b)+r')\,j'
def choose_bank(a,b,p,q,axis=False):
 if axis:
  # Original hard source shape: horizontal/vertical intercept confusions and diagonal.
  t=p if p else q
  bank=[y-t,x-t,x,y,x+y-t]
  if not p:bank[-1]=x-y+t
  correct=line(a,b,p,q)
 else:
  # Entire profile chosen before parameters. Tangent, sign error, omitted
  # point, sign-error point, and correct line. No arbitrary normal directions.
  bank=[line(a,b,p,q),a*(x-p)+b*(y-q),line(2*a,b,p,q),line(a,b,0,0),line(a,b,-p,-q)]
  correct=bank[0]
 if len({key(e) for e in bank})!=5:raise ValueError('whole-bank collision')
 if sum(key(e)==key(correct) for e in bank)!=1:raise ValueError('ambiguous bank')
 return bank,correct
# Byte-aware affine-coordinate transform, including implicit xy. Commands,
# generic vector/line notation, formal held-coordinate labels are masked first.
def affine_text(text,h,k,point=None):
 masks={}
 def protect(m):
  z='§'+str(len(masks))+'§';masks[z]=m.group();return z
 pattern=r'\\[A-Za-z]+|f\(x,y\)|\{f\}_\{[xy]\}|∂[xy]|\{v\}_\{[xy]\}|\{[xy]\}_\{0\}'
 text=re.sub(r'(?<=\\begin\{aligned\})([^\n]*?\{v\}[^\n]*?)(?= \\\\ )',protect,text)
 text=re.sub(pattern,protect,text)
 if point:
  p,q=point
  text=text.replace(f'({p},{q})',f'({p+h},{q+k})')
 for letter,shift in [('x',h),('y',k)]:
  if shift:
   replacement='('+letter+('-' if shift>0 else '+')+str(abs(shift))+')'
   text=re.sub(letter,lambda _:replacement,text)
 for z,v in masks.items():text=text.replace(z,v)
 return text

def raw_record(template,p,profile):
 """Public source recipes: translate every complete relation and point.
 Opaque banks retain uninterpreted affine transforms; never default learning.
 The zero-translation mask follows the same rendering path as every variant.
 """
 if template not in QS:raise ValueError('unknown observed template')
 q=QS[template];h,k=p.get('h',0),p.get('k',0)
 if set(p)-{'h','k'} or any(type(v)!=int or abs(v)>3 for v in (h,k)):raise ValueError('raw translation bounds')
 out={}
 for attr,val in q.items():
  if attr in (':question/problem',':question/worked-solution'):out[attr]=affine_text(val,h,k,DATA[template][2])
  elif attr==':question/answer-fields':
   fs=[]
   for f in val:
    ff={a:copy.deepcopy(v) for a,v in f.items() if a!=':db/id'}
    ff[':answer-field/type']=ff[':answer-field/type'][':db/ident']
    for a in ff[':answer-field/choices']:
     a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident'];a[':answer/value']=affine_text(a[':answer/value'],h,k)
    if ':answer-field/correct' in ff:ff[':answer-field/correct']=[':answer/id',ff[':answer-field/correct'][':answer/id']]
    fs.append(ff)
   out[attr]=fs
  elif attr==':question/difficulty':out[attr]=val[':db/ident']
  elif attr!=':db/id':out[attr]=val
 f,c,pt,*_=DATA[template];shifted=f.subs({x:x-h,y:y-k},simultaneous=True);pt=(pt[0]+h,pt[1]+k)
 record=wrap(out,template,'unrated' if ':question/difficulty' not in q else TEMPLATES[template],p,profile,shifted,c,pt,False)
 record['generation']['original_refs']={'question':q[':question/id'],'fields':[f[':answer-field/id'] for f in q.get(':question/answer-fields',[])],'answers':[a[':answer/id'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]}
 if h or k:
  out[':question/id']=uid(record['generation']['content_identity'])
  for f in out.get(':question/answer-fields',[]):
   f[':answer-field/id']=uid([out[':question/id'],f[':answer-field/key']]);mapping={}
   for a in f[':answer-field/choices']:
    original=a[':answer/id'];a[':answer/id']=uid([f[':answer-field/id'],a[':answer/value']]);mapping[original]=a[':answer/id']
   if ':answer-field/correct' in f:f[':answer-field/correct'][1]=mapping[f[':answer-field/correct'][1]]
 return record

def wrap(q,template,level,p,profile,f,c,pt,eligible):
 obj=s.expand(f-c)
 if obj.is_polynomial(x,y):
  obj=s.expand(obj/s.Poly(obj,x,y).coeffs()[0])
 fingerprint=digest([s.srepr(obj),list(pt),'normal-line'])
 identity=digest([VERSION,level,q.get(':question/problem'),q.get(':question/worked-solution'),sorted(a[':answer/value'] for fld in q.get(':question/answer-fields',[]) for a in fld[':answer-field/choices'])])
 if eligible:q[':question/id']=uid(identity)
 return {'knowledge_point':{'db_id':ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':template,'level':level,'profile':profile,'parameters':p,'mathematical_fingerprint':fingerprint,'content_identity':identity,'eligible_for_learning':eligible,'evidence_only':not eligible,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'python':sys.version.split()[0],'sympy':s.__version__}}

def normal_solution(template,f,c,pt,lhs,rhs):
 p,q=pt;a,b=[s.diff(f,v) for v in (x,y)];aa,bb=[v.subs({x:p,y:q}) for v in (a,b)];P=f'({p},{q})'
 needs=template not in HARD+['q-130718','easy_quadratic']
 text=''
 if needs:text='First, we bring all variables to one side:\n\n'+block([tex(lhs)+' & ='+tex(rhs),tex(f)+' & ='+tex(c)])+'\n\n'
 text+=f'If we set $f(x,y)={tex(f)}$, our curve can be viewed as the level curve $f(x,y)={tex(c)}.$  \n\n'
 text+=f'A normal vector to the level curve that passes through the point ${P}$ can be found by computing $∇f{P}.$ \n\nSo, we find the gradient and evaluate it at ${P}:$\n\n'
 rows=[r'∇f(x,y) & ={f}_{x}(x,y)\,i+{f}_{y}(x,y)\,j',r' & =\frac{∂}{∂x}('+tex(f)+r')\,i+\frac{∂}{∂y}('+tex(f)+r')\,j']
 if template=='q-130719':rows += [r' & =(\frac{2y}{x}\cdot\frac{1}{2y}+1)i+(\frac{2y}{x}\cdot(-\frac{x}{2y^2})-2)j']
 rows += [' & ='+gradienttex(a,b)]
 # Use unevaluated textual substitution: arguments in sqrt/denominator transform
 # along with every isolated and implicit occurrence, preserving arithmetic stage.
 def subtex(e):
  z=tex(e);z=re.sub(r'\\[A-Za-z]+',lambda m:'§'+m.group()[1:]+'§',z)
  z=z.replace('x',f'({p})').replace('y',f'({q})')
  return re.sub('§([A-Za-z]+)§',lambda m:'\\'+m.group(1),z)
 rows+=['∇f'+P+' & =('+subtex(a)+r')\,i+('+subtex(b)+r')\,j',' & ='+gradienttex(aa,bb),' & =⟨'+tex(aa)+','+tex(bb)+'⟩']
 text+=block(rows)+f'\n\nHence, $∇f{P}=⟨{tex(aa)},{tex(bb)}⟩$ is a normal vector to the curve at ${P}.$\n\n'
 text+='Finally, the Cartesian equation of the line that is parallel to $v=⟨{v}_{x},{v}_{y}⟩$ and passes through the point $({x}_{0},{y}_{0})$ can be written as:\n\n'
 sx=f'(x-({p}))';sy=f'(y-({q}))';full=line(aa,bb,p,q)
 if aa==0 or bb==0:
  lines=[r'(x-{x}_{0}){v}_{y}-(y-{y}_{0}){v}_{x} & =0',sx+'('+tex(bb)+')-'+sy+'('+tex(aa)+') & =0',tex(full)+' & =0',equation(full).replace('=',' & =')]
 else:
  lines=[r'\frac{x-{x}_{0}}{{v}_{x}} & =\frac{y-{y}_{0}}{{v}_{y}}',r'\frac{'+sx[1:-1]+'}{'+tex(aa)+r'} & =\frac{'+sy[1:-1]+'}{'+tex(bb)+'}']
  # Family-specific stage order: quotient/isolation; crossed products;
  # cancellation; expansion; collection. Source row counts retained.
  crossed=f'({tex(bb)}){sx} & =({tex(aa)}){sy}'
  d=s.gcd(aa,bb);A=aa/d;B=bb/d
  reduced=f'({tex(B)}){sx} & =({tex(A)}){sy}'
  expanded=tex(s.expand(B*(x-p)))+' & ='+tex(s.expand(A*(y-q)))
  if template=='q-36339':lines += [tex(s.expand((x-p)/A))+' & ='+tex(s.expand((y-q)/B))]
  elif template in ['q-130724','q-71388','q-71393']:lines += [tex(s.expand((x-p)/aa))+' & ='+tex(s.expand((y-q)/bb))]
  elif template=='q-36347':lines += [crossed,tex(bb*x-aa*y)+'+('+tex(-bb*p)+')+('+tex(aa*q)+') & =0']
  elif template=='q-71390':lines += [crossed,tex(s.expand(bb*(x-p)))+' & ='+tex(s.expand(aa*(y-q))),tex(full)+' & =0']
  elif template=='q-130719':lines += [crossed,f'({tex(2*bb)}){sx} & =({tex(2*aa)}){sy}',reduced,expanded]
  elif template=='q-71389':lines += [tex((x-p)/aa)+' & ='+tex(s.expand((y-q)/bb)),tex(x-p)+' & ='+tex(s.expand(aa*(y-q)/bb))]
  elif template=='q-130721':lines += [crossed,reduced]
  else:lines += [crossed,reduced,expanded]
  lines+=[equation(full).replace('=',' & =')]
 text+=block(lines)
 return text,aa,bb

# Easy: authored diagonal quadratic, two nonzero components, integer arithmetic.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate: all observed polynomial/radical/log/trig/exponential families; exact
# familiar evaluations and nonaxis normals. Points vary, levels derived exactly.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard: observed zero-component cases, avoiding division by zero using cross form.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 rng=random.Random(seed)
 if profile and profile.startswith('observed:'):
  template=template or profile.split(':',1)[1]
  if profile!='observed:'+template:raise ValueError('profile/template')
  record=raw_record(template,parameters if parameters is not None else {'h':0,'k':0},profile)
  record['generation']['seed']=seed
  return record
 eligible=['easy_quadratic'] if level=='easy' else HARD if level=='hard' else MOD
 if template and template not in eligible:raise ValueError('level/template workload')
 template=template or rng.choice(eligible)
 expected='authored-axis' if level=='hard' else 'authored-method'
 if profile not in (None,expected):raise ValueError('profile')
 for attempt in range(500):
  try:
   if template=='easy_quadratic':
    p=parameters if parameters is not None else {'a':rng.randint(1,4),'b':rng.randint(1,4),'p':rng.choice([-3,-2,-1,1,2,3]),'q':rng.choice([-3,-2,-1,1,2,3])}
    if set(p)!={'a','b','p','q'} or not all(type(v)==int for v in p.values()) or not all(1<=p[z]<=4 for z in ('a','b')) or not all(1<=abs(p[z])<=3 for z in ('p','q')):raise ValueError('easy bounds')
    f=p['a']*x*x+p['b']*y*y;pt=(p['p'],p['q']);c=f.subs(dict(zip((x,y),pt)));lhs,rhs=f,c
   else:
    p=parameters if parameters is not None else sample(template,rng)
    if set(p)!={'p','q'} or not all(type(v)==int and abs(v)<=8 for v in p.values()):raise ValueError('point bounds')
    f,_,_,oldlhs,oldrhs=DATA[template];pt=(p['p'],p['q']);c=s.simplify(f.subs(dict(zip((x,y),pt))))
    guard(template,pt)
    # Source orientation preserved. Shift the constant on its original side.
    delta=c-DATA[template][1]
    if template in ('q-36339','q-65173','q-71388','q-130719'):lhs=oldlhs+delta;rhs=oldrhs
    else:lhs=oldlhs;rhs=oldrhs+delta
   sol,a,b=normal_solution(template,f,c,pt,lhs,rhs)
   if a==b==0 or any(v.has(s.zoo,s.nan,s.oo) or v.is_real is not True for v in (c,a,b)):raise ValueError('domain/nonzero gradient')
   bank,correct=choose_bank(a,b,*pt,axis=level=='hard');break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('no eligible whole instance')
 prompt=f'Consider the plane curve ${tex(lhs)}={tex(rhs)}.$  Find the equation of the normal line to the curve at the point $({pt[0]},{pt[1]}).$'
 vals=[equation(e) for e in bank];ident=digest([level,prompt,sol,sorted(vals)])
 fid=uid([ident,'selection']);answers=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
 correctid=answers[[key(e) for e in bank].index(key(correct))][':answer/id'];rng.shuffle(answers)
 q={':question/id':uid(ident),':question/problem':prompt,':question/worked-solution':sol,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]}]}
 record=wrap(q,template,level,p,expected,f,c,pt,True)
 record['generation'].update({'seed':seed,'domain':{'point_on_curve':True,'nonzero_gradient':True,'familiar_exact_evaluation':True,'scope':'plane curve only'},'bank_operations':['axis/intercept/diagonal confusions'] if level=='hard' else ['correct normal','tangent','double x partial','omit point','negate point']})
 return record
def guard(t,pt):
 p,q=pt
 if t in HARD:
  if t=='q-71394':valid=p==0 and 1<=abs(q)<=6
  else:valid=q==0 and 1<=abs(p)<=6
  if not valid:raise ValueError('hard axis bounds')
 elif t=='q-130724':
  if not(p==0 and 1<=q<=6):raise ValueError('radical positive perfect square')
 elif t=='q-71388':
  if not(q==0 and 1<=p<=6):raise ValueError('radical domain/workload')
 elif t=='q-71393':
  if p+q!=1 or max(abs(p),abs(q))>4:raise ValueError('familiar log')
 elif t=='q-130719':
  if p!=2*q or not 1<=abs(q)<=4:raise ValueError('log positive ratio one')
 elif t in ('q-71389','q-130721'):
  if q!=0 or not 1<=abs(p)<=4:raise ValueError('familiar chain-rule evaluation')
 elif not(1<=abs(p)<=8 and 1<=abs(q)<=4):raise ValueError('polynomial workload')
def sample(t,r):
 if t=='q-71394':p,q=0,r.choice([1,2,3,4,5,6,-1,-2,-3,-4,-5,-6])
 elif t in HARD:p,q=r.choice([1,2,3,4,5,6,-1,-2,-3,-4,-5,-6]),0
 elif t=='q-130724':p,q=0,r.randint(1,6)
 elif t=='q-71388':p,q=r.randint(1,6),0
 elif t=='q-71393':p=r.randint(-3,4);q=1-p
 elif t=='q-130719':q=r.choice([-4,-3,-2,-1,1,2,3,4]);p=2*q
 elif t in ('q-71389','q-130721'):p,q=r.choice([-4,-3,-2,-1,1,2,3,4]),0
 else:p,q=r.choice(list(range(-8,0))+list(range(1,9))),r.choice([-4,-3,-2,-1,1,2,3,4])
 return {'p':p,'q':q}
def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[Original has no worked solution.]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
