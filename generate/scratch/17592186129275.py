#!/usr/bin/env python3
"""Polar setup over origin-tangent off-center disks (steps 3–7, no DB writes).

Basis 1356. Nine observed complete banks, including two unrated banks. Source
replay uses radius slots and mathematical operation recipes, never literal source
payload branches. Easy is a supported authored extension: constant integrand,
full axis-centered disk; moderate has full disks and polynomial densities; hard
adds half-disk restrictions and observed composite/radial substitutions. Bounds
are deliberately familiar positive integers/halves, not general displaced disks
that require solving a quadratic. Assessment is a correct region AND transformed
integrand with Jacobian; scalar coincidence is independently reported, because
integrating a structurally invalid setup can coincidentally give zero.

Profiles: observed preserves source wording (with TeX presentation repairs);
setup uses the same complete bank and explicitly states the intended criterion.
All normal generation defaults to setup. Old missing correct refs are derived
from geometry, never counted as observed correct-designation fidelity.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,uuid,subprocess,tempfile,os
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
TEMPLATES=json.loads((HERE/'templates.json').read_text())
KP=SOURCE['record']; KP_ID=17592186129275; VERSION='polar-offset-disk-1'
x,y,r,t,a=sp.symbols('x y r t a',real=True)
LOCALS={'x':x,'y':y,'r':r,'t':t,'a':a,'cos':sp.cos,'sin':sp.sin,'exp':sp.exp,'log':sp.log,'sqrt':sp.sqrt}
DENSITIES={'difference':x*x-y*y,'xsqrt':x*sp.sqrt(x*x+y*y),'linear':x,'x2y':x*x*y,'expdiff':sp.exp(x*x-y*y),'sqrt':sp.sqrt(x*x+y*y),'xy2':x*y*y,'radial2':x*x+y*y,'log':sp.log(x*x+y*y+1)}

def tex(z):return sp.latex(sp.sympify(z),symbol_names={t:r"\theta"}).replace(r'\log',r'\ln')
def hashof(z):return hashlib.sha256(json.dumps(z,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(z):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),str(z)))
def coefficient(z):return '' if z==1 else tex(z)
def slots(s,v):
 vals={'A':tex(v),'A2':tex(v*v),'B':coefficient(2*v),'Bfull':tex(2*v),'FourA':coefficient(4*v),'Acoef':coefficient(v)}
 for key,value in vals.items():s=s.replace('@@'+key+'@@',value)
 assert '@@' not in s
 return s

def presentation(s):
 """Only visible set/system braces and source image path normalization."""
 s=s.replace('D = {','D = \\{').replace('D={','D=\\{').replace('Δ={','Δ=\\{')
 s=re.sub(r'((?:D|Δ)\s*=\s*\\\{[^$]*?)(?<!\\)\}(?=\$|,\$|\.\n)',r'\1\\}',s)
 s=s.replace('\n{\\begin{aligned}', '\n\\{\\begin{aligned}')
 return re.sub(r'!\[\]\((images/[^)]+)\)',lambda m:'![](/media/jake/SSD/EDB/math/'+m[1]+')',s)

def bounds(c):
 axis,sign,part=c['axis'],c['sign'],c['part']
 if axis=='x':
  if sign==1:return {'full':('-1/2','1/2'),'upper':('0','1/2'),'lower':('-1/2','0')}[part]
  return {'full':('1/2','3/2'),'lower':('1','3/2'),'upper':('1/2','1')}[part]
 if sign==1:return {'full':('0','1'),'right':('0','1/2'),'left':('1/2','1')}[part]
 return {'full':('1','2'),'right':('3/2','2'),'left':('1','3/2')}[part]

def circle(c,v):
 shift=('-' if c['sign']==1 else '+')+tex(v)
 return ('(x'+shift+')^{2}+y^{2}' if c['axis']=='x' else 'x^{2}+(y'+shift+')^{2}')
def radial(c,v):return 2*v*c['sign']*(sp.cos(t) if c['axis']=='x' else sp.sin(t))
def angle(z):return sp.Rational(z)*sp.pi

def integral(operation,v):
 lo,hi,lower,upper,f=operation
 return tuple(sp.sympify(z,locals=LOCALS).subs(a,v) for z in (lower,upper,f))+(angle(lo),angle(hi))
def integral_tex(data):
 low,up,f,lo,hi=data
 return r'\int_{'+tex(lo)+r'}^{'+tex(hi)+r'}\int_{'+tex(low)+r'}^{'+tex(up)+'}'+tex(f)+r'\,\mathrm{d}r\,\mathrm{d}\theta'

def render_plots(c,v):
 key=hashof({'axis':c['axis'],'sign':c['sign'],'part':c['part'],'a':str(v),'renderer':4})[:20]
 dest=HERE/'plots';dest.mkdir(exist_ok=True)
 paths=[dest/(key+'-'+role+'.png') for role in ('region','radius','angle')]
 if not all(p.exists() and p.with_suffix('.json').exists() for p in paths):
  fd,filename=tempfile.mkstemp(prefix='input-',suffix='.json',dir=dest);os.close(fd)
  try:
   Path(filename).write_text(json.dumps({'axis':c['axis'],'sign':c['sign'],'part':c['part'],'a':float(v),'radius_tex':tex(v),'square_tex':tex(v*v),'bounds':[float(angle(z)) for z in bounds(c)],'bounds_tex':[tex(angle(z)) for z in bounds(c)],'boundary_tex':circle(c,v),'upper_tex':tex(radial(c,v)),'paths':[str(p) for p in paths]}))
   subprocess.run([os.environ.get('PYTHON','python3'),str(HERE/'render.py'),filename],check=True,stdout=subprocess.PIPE)
  finally:Path(filename).unlink(missing_ok=True)
 return [str(p) for p in paths]

def normal_prompt(name,c,v):
 if name.startswith('constant_'):
  return 'If $D=\\{(x,y)\\,:\\,'+circle(c,v)+r'\le '+tex(v*v)+r'\},$ then $\iint_D 1\,\mathrm{d}A=$'
 raw=c['raw_prompt']; old=sp.Rational(c['original_a']); oldtex=tex(old)
 for vv in ('x','y'):
  for sg in ('-','+'):
   raw=raw.replace(vv+' '+sg+' '+oldtex,vv+' '+sg+' '+tex(v)).replace(vv+sg+oldtex,vv+sg+tex(v))
 # Replace complete inequality right component; powers and integrand remain fixed.
 raw=raw.replace('\\le '+tex(old*old), '\\le '+tex(v*v))
 return presentation(raw)

def authored_solution(name,c,v,images):
 lo,hi=map(angle,bounds(c)); up=radial(c,v); coord=sp.cos(t) if c['axis']=='x' else sp.sin(t)
 shift=c['sign']*v; cx=shift if c['axis']=='x' else 0;cy=shift if c['axis']=='y' else 0
 density=sp.Integer(1) if name.startswith('constant_') else DENSITIES[name]
 sub=tex(density.subs({x:r*sp.cos(t),y:r*sp.sin(t)},simultaneous=True))
 final=sp.trigsimp(density.subs({x:r*sp.cos(t),y:r*sp.sin(t)},simultaneous=True)*r)
 if name=='xsqrt':final=r**3*sp.cos(t)
 if name=='sqrt':final=r**2
 trig=r'\cos\theta' if c['axis']=='x' else r'\sin\theta'
 shifttex=('-' if shift>0 else '+')+tex(abs(shift))
 substitution=('(r\\cos\\theta'+shifttex+')^2+(r\\sin\\theta)^2' if c['axis']=='x' else '(r\\cos\\theta)^2+(r\\sin\\theta'+shifttex+')^2')
 sign='-' if shift>0 else '+'
 expanded=('r^2\\cos^2\\theta'+sign+tex(2*abs(shift))+'r'+trig+'+'+tex(v*v)+'+r^2\\sin^2\\theta' if c['axis']=='x' else 'r^2\\cos^2\\theta+r^2\\sin^2\\theta'+sign+tex(2*abs(shift))+'r'+trig+'+'+tex(v*v))
 combined='r^2(\\cos^2\\theta+\\sin^2\\theta)'+sign+tex(2*abs(shift))+'r'+trig
 reduced='r^2'+sign+tex(2*abs(shift))+'r'+trig
 factor='r(r'+sign+tex(2*abs(shift))+trig+')'
 def setup_density(d):
  return integral_tex((sp.Integer(0),up,sp.Symbol('slot'),lo,hi)).replace('slot',d)
 rows=[]
 if name=='difference':rows=[setup_density(r'r^3(\cos^2\theta-\sin^2\theta)')]
 if name=='xsqrt':rows=[setup_density(r'r^2\cos\theta\sqrt{r^2(\cos^2\theta+\sin^2\theta)}'),setup_density(r'r^3\cos\theta\sqrt{\cos^2\theta+\sin^2\theta}')]
 rows.append(integral_tex((sp.Integer(0),up,final,lo,hi)))
 finalrows=r'\\&='.join(rows)
 return ("We need to change the coordinate system from Cartesian coordinates to polar coordinates. To do this, we will use the change of variables formula in the form\n\n$$\n\\iint_D f(x,y)\\,dA=\\iint_\\Delta f(r\\cos\\theta,r\\sin\\theta)\\,r\\,dr\\,d\\theta.\n$$\n\nFirst, let's sketch our region $D:$\n\n![]("+images[0]+")\n\nNotice that the region $D$ represents "+('the disk' if c['part']=='full' else 'a portion of the disk')+' of radius $'+tex(v)+'$ centered at $('+tex(cx)+','+tex(cy)+').$\n\nCartesian and polar coordinates are connected by the following equations:\n\n$$\n\\{\\begin{aligned}x=r\\cos\\theta \\\\ y=r\\sin\\theta\\end{aligned}\n$$\n\nWith that in mind, let\'s now write the $'+circle(c,v)+'='+tex(v*v)+'$ in polar coordinates:\n\n$$\n\\begin{aligned}'+circle(c,v)+'&='+tex(v*v)+'\\\\'+substitution+'&='+tex(v*v)+'\\\\'+expanded+'&='+tex(v*v)+'\\\\'+combined+'&=0\\\\'+reduced+'&=0\\\\'+factor+'&=0\\end{aligned}\n$$\n\nSince $r$ cannot be identical to zero on the entire '+('circle' if c['part']=='full' else 'semicircle')+', we must have $r='+tex(up)+'.$\n\nNow, let\'s determine the limits for $r$ and $\\theta.$ First of all, $r$ can vary from $r=0$ (at the origin) to $r='+tex(up)+'$ (at the boundary of the region):\n\n![]('+images[1]+')\n\nSecondly, $\\theta$ can vary between $\\theta='+tex(lo)+'$ and $\\theta='+tex(hi)+'.$\n\n![]('+images[2]+')\n\nSo, in polar coordinates $(r,\\theta),$ the region can be expressed as\n\n$$\n\\Delta=\\{(r,\\theta)\\,:\\,0\\le r\\le '+tex(up)+',\\,'+tex(lo)+'\\le\\theta\\le '+tex(hi)+'\\}.\n$$\n\nTherefore, using the change of variables formula, we obtain\n\n$$\n\\begin{aligned}\\iint_D '+tex(density)+'\\,dA&=\\iint_\\Delta ('+sub+')\\,r\\,dr\\,d\\theta\\\\&='+finalrows+'.\\end{aligned}\n$$')


def _generate(level,seed,template,field_type,parameters,profile):
 rng=random.Random(seed)
 names=[k for k,v in TEMPLATES.items() if v['level']==level]
 if level=='easy':names=['constant_right','constant_left','constant_above','constant_below']
 name=template or rng.choice(names)
 if name not in names:raise ValueError('Template incompatible with difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio layout is supported')
 profile=profile or 'setup'
 if profile not in ('observed','setup'):raise ValueError('Unknown bank profile')
 if name.startswith('constant_') and profile=='observed':raise ValueError('No observed easy bank')
 if parameters is not None and set(parameters)!={'a'}:raise ValueError('Expected exactly radius a')
 v=sp.Rational(parameters['a']) if parameters is not None else (sp.Integer(rng.randint(1,5)) if level=='easy' else sp.Rational(rng.randint(1,10),2))
 if v<=0 or v>5 or v.q not in (1,2):raise ValueError('Radius must be a positive integer or half-integer at most 5')
 if level=='easy' and v.q!=1:raise ValueError('Easy radius is an integer 1–5')
 if level=='easy' and parameters is None:v=sp.Integer(rng.randint(1,5))
 if name.startswith('constant_'):
  orient=name.split('_')[1]; axis='x' if orient in ('right','left') else 'y';sign=1 if orient in ('right','above') else -1
  c={'axis':axis,'sign':sign,'part':'full'};lo,hi=bounds(c);up=radial(c,v)
  data=[(sp.Integer(0),up,r,angle(lo),angle(hi)),(sp.Integer(0),up,sp.Integer(1),angle(lo),angle(hi)),(sp.Integer(0),v,r,angle(lo),angle(hi)),(sp.Integer(0),up,r,0,2*sp.pi),(sp.Integer(0),-up,r,angle(lo),angle(hi))]
  choices=[integral_tex(z) for z in data];correct=0;imgs=render_plots(c,v);solution=authored_solution(name,c,v,imgs)
 else:
  c=TEMPLATES[name];data=[integral(z['operation'],v) for z in c['bank']];choices=[slots(z['mask'],v) for z in c['bank']];correct=c['correct']
  if c['solution_mask']:
   solution=presentation(slots(c['solution_mask'],v))
   if v!=sp.Rational(c['original_a']):
    imgs=render_plots(c,v);j=iter(imgs);solution=re.sub(r'!\[\]\([^)]+\)',lambda m:'![]('+next(j)+')',solution)
  else:imgs=render_plots(c,v);solution=authored_solution(name,c,v,imgs)
 prompt=normal_prompt(name,c,v)
 if profile=='setup':prompt+='\n\nChoose the polar setup whose bounds describe $D$ with $r\\ge 0$ and whose integrand is the given Cartesian integrand multiplied by the Jacobian $r.$'
 mathematical={'circle_axis':c['axis'],'circle_sign':c['sign'],'part':c['part'],'radius':str(v),'density':str(1 if name.startswith('constant_') else DENSITIES[name])}
 fingerprint=hashof(mathematical)
 content=hashof([VERSION,prompt,solution,sorted(choices)])
 qid=uid(content);fid=uid(content+':selection')
 answers=[{':answer/id':uid(fid+':'+s),':answer/type':':answer.type/math',':answer/value':s} for s in choices]
 corr=answers[correct][':answer/id'];rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',corr]}]},'generation':{'version':VERSION,'seed':seed,'template':name,'profile':profile,'bank_profile':profile,'parameters':{'a':str(v)},'mathematical_fingerprint':fingerprint,'content_hash':content,'provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},'authored':name.startswith('constant_'),'source_id':c.get('source_id'),'domain':'r ≥ 0; disk tangent to origin; radius integer/half ≤5','answer_operations':{s:[str(z) for z in dat] for s,dat in zip(choices,data)}}}

# EASY — authored full axis-centered disks; constant integrand, integer radius 1–5.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return _generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — observed full disks; linear/cubic monomial or quadratic difference.
# The unrated difference bank is an authored moderate assignment, not a source label.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return _generate('moderate',seed,template,field_type,parameters,profile)
# HARD — observed half-disks; radial root/log/exponential or polynomial densities.
# The unrated xsqrt bank is an authored hard assignment supported by the composite substitution.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return _generate('hard',seed,template,field_type,parameters,profile)
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 return globals()['generate_'+level](seed,template,field_type,parameters,profile)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ns=ap.parse_args()
 records=[generate(level,ns.seed+i,ns.template,profile=ns.profile) for level in (['easy','moderate','hard'] if ns.difficulty=='all' else [ns.difficulty]) for i in range(ns.count)]
 if ns.format=='json':print(json.dumps(records,ensure_ascii=False,indent=2))
 else:
  for z in records:
   q=z['question'];print(q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']+'\n')
