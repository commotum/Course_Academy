#!/usr/bin/env python3
"""Origin-centered circular-region polar setup generator; stops at steps 3–7.

Nine complete observed radio banks, eight observed rated questions and one
unrated missing-key source. All choices are parameterized complete components.
Normal prompts require the actual transformed domain and integrand with r>=0;
coincident numerical integral values are recorded separately, because equality
of scalars is not the assessed change-of-variables setup criterion.
Hard is explicitly authored: canonical radial square-root simplification plus
an existing double-angle identity, over the same origin-centered sectors. No
integral is evaluated and no shifted circle or variable radial bound is added.
See the evidence folder for extraction, plot specification and native grading.

.venv/bin/python generate/scratch/17592186129199.py --difficulty all --count 2
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,random,re,subprocess,tempfile,uuid,os
from pathlib import Path
import sympy as sp
KP_ID=17592186129199
HERE=Path(__file__).resolve().with_suffix('')
_spec=importlib.util.spec_from_file_location('polar_math_reader',HERE/'math_reader.py');mr=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(mr)
X,Y,R,T=mr.x,mr.y,mr.r,mr.theta
SOURCE=json.loads((HERE/'source.json').read_text());RECORD=SOURCE['record'];DATA=json.loads((HERE/'templates.json').read_text())
VERSION='origin-polar-setup-v1'
TITLE=RECORD[':knowledge-point/title'];KP_UUID=RECORD[':knowledge-point/id']
TEMPLATES={v['family']:v['level'] for v in DATA.values()};TEMPLATES.update(root_product='hard',root_difference='hard')
RADII=tuple(range(2,37))
CRITERION='Choose a change-of-variables setup with $r\\geq0$ that describes $D$ and the transformed integrand, including the Jacobian.'

def tex(v):return sp.latex(sp.simplify(v)).replace(r'\log',r'\ln')
def fingerprint(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def integral(f,a,b,radius,lo=0):return r'\int_{'+tex(a)+'}^{'+tex(b)+r'}\int_{'+tex(lo)+'}^{'+tex(radius)+'}'+f+r'\,\mathrm{d}r\,\mathrm{d}\theta'
def family_expr(f):
 return {'xy2':X*Y**2,'twoxy':2*X*Y,'exp':sp.exp(X**2+Y**2),'diff':X**2-Y**2,'log':sp.log(X**2+Y**2+1),'sum':X**2+Y**2,'linear':X+Y,'x':X,'y2':Y**2,'root_product':2*X*Y*sp.sqrt(X**2+Y**2),'root_difference':(X**2-Y**2)*sp.sqrt(X**2+Y**2)}[f]
def transformed(f):return sp.trigsimp(family_expr(f).subs({X:R*sp.cos(T),Y:R*sp.sin(T)})*R)
def same_sector(a,b,c,d):
 return sp.simplify((b-a)-(d-c))==0 and sp.simplify(sp.Mod(a-c,2*sp.pi))==0

def radial_recipe(v,r0,radius):
 for base,out in [(0,0),(r0,radius),(-r0,-radius),(r0**2,radius**2),(r0/2,radius/2)]:
  if sp.simplify(v-base)==0:return sp.sympify(out)
 raise ValueError(('unmapped radial recipe',v,r0))
def remap_integrals(text,base,n,rotation):
 """Slots are full bounds; no global number replacement in prose/integrands."""
 r0=sp.sqrt(base['n']);rad=sp.sqrt(n);rot=sp.Rational(rotation,2)*sp.pi
 matches=list(re.finditer(r'\\int\s*\}?\s*_',text)); replacements=[]
 for k,m in enumerate(matches):
  i=m.end();lo,j=mr.group(text,i);hi,z=mr.group(text,j+1)
  for old,start,end in [(lo,i+1,j-1),(hi,j+2,z-1)]:
   val=mr.expr(old)
   new=val+rot if k%2==0 else radial_recipe(val,r0,rad)
   # Preserve the source's lexical notation when this complete component has
   # unchanged value. This is a general slot formatter, not payload replay.
   replacements.append((start,end,old if sp.simplify(new-val)==0 else tex(new)))
 for i,j,new in reversed(replacements):text=text[:i]+new+text[j:]
 return text

def domain(radius,a,b):return r'\Delta=\{(r,\theta):0\leq r\leq '+tex(radius)+r',\ '+tex(a)+r'\leq\theta\leq '+tex(b)+r'\}.'
def normal_solution(f,radius,a,b):
 """Authored full formal, domain, substitution, factored and simplified stages."""
 ff=tex(family_expr(f));sub=ff
 # Slots are x/y mathematical variables, protected by token boundaries.
 sub=re.sub(r'(?<![A-Za-z])x(?![A-Za-z])',r'(r\\cos\\theta)',sub)
 sub=re.sub(r'(?<![A-Za-z])y(?![A-Za-z])',r'(r\\sin\\theta)',sub)
 final=transformed(f)
 if f=='root_product':
  stages=[r'2r^3\cos\theta\sin\theta\sqrt{r^2(\cos^2\theta+\sin^2\theta)}',r'2r^4\cos\theta\sin\theta',r'r^4\sin(2\theta)']
 elif f=='root_difference':
  stages=[r'r^3(\cos^2\theta-\sin^2\theta)\sqrt{r^2(\cos^2\theta+\sin^2\theta)}',r'r^4(\cos^2\theta-\sin^2\theta)',r'r^4\cos(2\theta)']
 else:stages=[tex(final)]
 rows=[r'\iint_D '+ff+r'\,\mathrm{d}A&=\iint_\Delta '+sub+r'\,r\,\mathrm{d}r\,\mathrm{d}\theta']
 rows += ['&='+integral(z,a,b,radius) for z in stages]
 return ('We will use the change of variables formula in the form\n\n$$\n'+r'\iint_D f(x,y)\,\mathrm{d}A=\iint_\Delta f(r\cos\theta,r\sin\theta)\,r\,\mathrm{d}r\,\mathrm{d}\theta.'+'\n$$\n\nFirst, notice that the region $D$ represents '+('the disk' if sp.simplify(b-a-2*sp.pi)==0 else 'a portion of the disk')+' of radius $'+tex(radius)+'$ centered at the origin. In polar coordinates $(r,\\theta),$ the region can be expressed as\n\n$$\n'+domain(radius,a,b)+'\n$$\n\n'+('Since $r\\geq0$, $\\sqrt{r^2}=r$; also $\\cos^2\\theta+\\sin^2\\theta=1$.\n\n' if f.startswith('root_') else '')+'Therefore, using the change of variables formula, we obtain\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$')

def source_solution(base,n,rotation,a,b):
 if base['solution'] is None:return normal_solution(base['family'],sp.sqrt(n),a,b)
 s=remap_integrals(base['solution'],base,n,rotation)
 # Radius prose and Delta bounds are complete slots, distinct from all other
 # occurrences of a numeral in function arguments or exponents.
 s=re.sub(r'radius \$[^$]+\$',lambda _: 'radius $'+tex(sp.sqrt(n))+'$',s)
 blocks=list(re.finditer(r'\$\$\n(.*?)\n\$\$',s,re.S))
 for m in reversed(blocks):
  if m[1].lstrip().startswith('Δ='):
   # Keep original domain block if well formed and unchanged; escape the two
   # captured literal-set brace anomalies independently of mathematical repair.
   if n==base['n'] and rotation==0:
    t=m[1].replace('Δ={(r',r'Δ=\{(r')
    if t.endswith('}.') and not t.endswith(r'\}.'):t=t[:-2]+r'\}.'
   else:t=domain(sp.sqrt(n),a,b)
   s=s[:m.start(1)]+t+s[m.end(1):]
 return s

def render_plots(instance,output_dir=HERE/'plots'):
 """Exact instance data; unique input and atomic final files support concurrency."""
 output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
 key=fingerprint({'plot_version':3,**instance});png=output_dir/(key+'.png');side=png.with_suffix('.json')
 if not (png.exists() and side.exists()):
  fd,name=tempfile.mkstemp(prefix='render-input-',suffix='.json',dir=output_dir)
  try:
   with os.fdopen(fd,'w') as out:json.dump({'instance':instance,'png':str(png)},out)
   subprocess.run([str(Path(__file__).resolve().parents[2]/'.venv/bin/python'),str(HERE/'render.py'),name],check=True,stdout=subprocess.DEVNULL)
  finally:Path(name).unlink(missing_ok=True)
 return {'prompt':str(png),'sidecar':str(side)}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio field is supported')
 rng=random.Random(seed)
 if profile=='authored' and level!='hard':raise ValueError('authored profile belongs to hard')
 if profile in DATA:
  base=DATA[profile];template=template or base['family']
  if template!=base['family']:raise ValueError('profile/template mismatch')
 elif profile not in (None,'authored'):raise ValueError('unknown profile')
 else:
  template=template or rng.choice([k for k,v in TEMPLATES.items() if v==level])
  base=next((v for v in DATA.values() if v['family']==template),None)
 if template not in TEMPLATES or TEMPLATES[template]!=level:raise ValueError('template/difficulty mismatch')
 default={'radius_squared':rng.choice(RADII),'rotation':rng.choice((0,1,2,3)) if level!='easy' and (not base or sp.Rational(base['beta'])-sp.Rational(base['alpha'])!=2) else 0}
 p=default if parameters is None else dict(parameters)
 if set(p)!= {'radius_squared','rotation'}:raise ValueError('required radius_squared and rotation')
 n=p['radius_squared'];rot=p['rotation']
 if type(n)!=int or n not in RADII or type(rot)!=int or rot not in (0,1,2,3):raise ValueError('parameter bounds')
 if level=='easy' and rot!=0:raise ValueError('easy is a full disk; rotation must be zero')
 if base and sp.Rational(base['beta'])-sp.Rational(base['alpha'])==2 and rot!=0:raise ValueError('full disk rotation is incidental and excluded')
 radius=sp.sqrt(n)
 if base:a=(sp.Rational(base['alpha'])+sp.Rational(rot,2))*sp.pi;b=(sp.Rational(base['beta'])+sp.Rational(rot,2))*sp.pi
 else:a=sp.Rational(rot,2)*sp.pi;b=a+sp.pi/2
 original=profile in DATA
 if base:
  vals=[remap_integrals(v,base,n,rot) for v in base['bank']];ci=base['correct_index'];solution=source_solution(base,n,rot,a,b)
 else:
  f=transformed(template)
  # One complete authored bank: missing Jacobian, extra Jacobian, wrong
  # angular half-width, and doubled radius. No pool or partial substitution.
  vals=[integral(tex(f),a,b,radius),integral(tex(f/R),a,b,radius),integral(tex(f*R),a,b,radius),integral(tex(f),a,a+(b-a)/2,radius),integral(tex(f),a,b,2*radius)];ci=0;solution=normal_solution(template,radius,a,b)
 # Bank eligibility uses the assessed response form, not integral scalar alone.
 sigs=[];expected=transformed(template);valid=[]
 for i,v in enumerate(vals):
  bounds,f=mr.read_integral(v);aa,bb,lo,hi=bounds
  sig=(sp.srepr(sp.Mod(aa,2*sp.pi)),sp.srepr(bb-aa),sp.srepr(lo),sp.srepr(hi),sp.srepr(sp.trigsimp(f)))
  sigs.append(sig)
  valid.append(lo==0 and sp.simplify(hi-radius)==0 and same_sector(aa,bb,a,b) and sp.trigsimp(f-expected)==0)
 if len(set(sigs))!=5 or sum(valid)!=1 or not valid[ci]:raise ValueError('whole bank rejected: setup collision or wrong key')
 if base and n==base['n'] and rot==0:
  asset={'prompt':base['image'],'sidecar':None};prompt=re.sub(r'!\[\]\([^)]+\)',lambda _: '![]('+base['image']+')',base['prompt'])
 else:
  asset=render_plots({'radius_squared':n,'alpha_pi':str(sp.simplify(a/sp.pi)),'beta_pi':str(sp.simplify(b/sp.pi))})
  shape='circle' if b-a==2*sp.pi else 'semicircle' if b-a==sp.pi else 'quarter-circle'
  if base:prompt=re.sub(r'!\[\]\([^)]+\)',lambda _: '![]('+asset['prompt']+')',base['prompt'])
  else:prompt='![]('+asset['prompt']+')\n\nThe region $D$ is the '+shape+' shown above. What is $'+r'\iint_D '+tex(family_expr(template))+r'\,\mathrm{d}A'+'$ expressed in polar coordinates?'
 if not original:
  if template=='xy2':prompt=prompt.replace('∬_(D)xy^{2}dA',r'\iint_D xy^2\,\mathrm{d}A')
  prompt+='\n\n'+CRITERION
 # Identity is the actual complete display, with order-independent owned bank.
 key=fingerprint({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(vals),'difficulty':level})
 qid=uuid.uuid5(uuid.NAMESPACE_URL,key);fid=uuid.uuid5(qid,'selection')
 answers=[{':answer/id':str(uuid.uuid5(fid,'math:'+v)),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
 correct=answers[ci][':answer/id'];rng.shuffle(answers)
 taskkey=fingerprint({'f':sp.srepr(family_expr(template)),'radius':sp.srepr(radius),'alpha':str(sp.Mod(a,2*sp.pi)),'width':str(b-a),'criterion':'actual-D-polar-setup-r-nonnegative'})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile or (base['source_id']+'-parameterized-default' if base else 'authored'),'bank_origin':'observed' if base else 'authored','authored_difficulty':template in ('root_product','root_difference') or template=='xy2','source_id':base['source_id'] if base else None,'source_provenance':{k:SOURCE[k] for k in ('database','basis','lineage')},'parameter_fingerprint':taskkey,'content_fingerprint':key,'plot':asset,'domain':{'radius':str(radius),'alpha':str(a),'beta':str(b)},'response_criterion':'valid change-of-variables setup for actual D, with nonnegative r and transformed integrand times Jacobian'}}

# Easy: observed full circles, one direct substitution or radial Pythagorean
# reduction; n=2..36, rotation=0. No new method under numerical variation.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: observed quarter/half-circle boundary reading plus substitution;
# xy^2 unrated source is explicitly assigned moderate, not an observed label.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 if template=='xy2' and parameters is None:parameters={'radius_squared':random.Random(seed).choice(RADII),'rotation':0}
 # Full-circle xy2 rotation is forbidden, including sampler calls.
 if template is None and profile=='q-161044' and parameters is None:parameters={'radius_squared':random.Random(seed).choice(RADII),'rotation':0}
 return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: authored same origin-centered sector/setup skill; both retain a
# square-root Pythagorean reduction and a double-angle simplification. Neither
# coefficient may vanish and neither function can reduce to an easy template.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='markdown');p.add_argument('--template');p.add_argument('--profile');args=p.parse_args()
 out=[]
 for level in ('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,):
  for j in range(args.count):out.append(globals()['generate_'+level](args.seed+j,args.template,profile=args.profile))
 if args.format=='json':print(json.dumps(out,indent=2,ensure_ascii=False))
 else:
  for rec in out:
   q=rec['question'];print('\n'+q[':question/problem']+'\n')
   for k,a in enumerate(q[':question/answer-fields'][0][':answer-field/choices']):print(str(k+1)+'. $'+a[':answer/value']+'$')
   print('\n'+q[':question/worked-solution'])
