#!/usr/bin/env python3
"""Source replay and exact solution helpers adapted from the supplied entrypoint.

The public supported-band sampler is generator.py. Captured banks and source
solution masks remain here for fidelity checks. Runtime assets use the caller's
explicit output directory and the local Matplotlib renderer.
"""
from __future__ import annotations
import argparse,hashlib,json,math,os,random,re,sys,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
KP_ID=17592186087657
VERSION='diameter-circle-frozen-1'
CAPTURE=json.loads((HERE/'source-data.json').read_text())
KP=CAPTURE['material']['kp']; QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
X,Y=sp.symbols('x y',real=True)
PARAMS={'q-15292':(2,2,-4,2),'q-15297':(6,4,-4,2),'q-117102':(2,4,2,0),'q-117103':(2,-1,2,1),'q-117105':(-3,0,1,-2),'q-117106':(-2,0,0,2),'q-117107':(-1,-3,3,1),'q-70987':(7,3,-1,3),'q-70990':(-3,2,3,4)}
LEVELS={q:('hard' if q in ('q-15297','q-117105','q-117106','q-117107','q-70990') else 'moderate') for q in QS}
TEMPLATES={q:{'level':LEVELS[q],'observed':True,'source_ids':[q]} for q in QS}
TEMPLATES.update({l+'_diameter':{'level':l,'observed':False,'source_ids':[]} for l in ('easy','moderate','hard')})


def tex(v):return sp.latex(sp.sympify(v)).replace(' \\sqrt','\\sqrt')
def group(v):return '('+tex(v)+')' if v<0 else tex(v)
def shift(v,c,raw=False):
 if raw:return '('+v+'-'+group(c)+')^{2}'
 if c==0:return '{'+v+'}^{2}'
 return '('+v+('+' if c<0 else '-')+tex(abs(c))+')^{2}'
def eq(h,k,z,minus=False,raw=False):return shift('x',h,raw)+('-' if minus else '+')+shift('y',k,raw)+'='+tex(z)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp-diameter:'+v))
def values(p):
 x1,y1,x2,y2=(p[k] for k in ('x1','y1','x2','y2'));h=sp.Rational(x1+x2,2);k=sp.Rational(y1+y2,2);D=sp.Integer((x1-x2)**2+(y1-y2)**2);return h,k,D,D/4,sp.sqrt(D),sp.sqrt(D)/2

def guard(level,p,profile):
 if not isinstance(p,dict) or set(p)!=set(('x1','y1','x2','y2')):raise ValueError('Exactly four endpoint coordinate parameters required')
 if any(isinstance(v,bool) or not isinstance(v,(int,sp.Integer)) for v in p.values()):raise ValueError('Finite integer endpoint coordinates required')
 if any(abs(v)>12 for v in p.values()):raise ValueError('Endpoint coordinate ceiling is 12')
 h,k,D,z,d,r=values(p)
 if D==0 or D>(400 if level=='easy' else 200) or not (h.is_Integer and k.is_Integer):raise ValueError('Distinct endpoints, integer midpoint, squared diameter within the level ceiling required')
 dx=p['x1']-p['x2'];dy=p['y1']-p['y2']
 if level=='easy':
  if h!=0 or k!=0 or dx*dy!=0 or not 2<=r<=10:raise ValueError('Easy: origin midpoint, axial diameter, radius 2–10')
 elif level=='moderate':
  if dx*dy!=0 or h==k==0 or not 1<=r<=6 or abs(h)>5 or abs(k)>5:raise ValueError('Moderate: translated axial diameter, radius 1–6, center magnitude <=5')
 elif level=='hard':
  if dx*dy==0 or abs(dx)>10 or abs(dy)>10 or z.is_Integer is not True or sp.sqrt(z).is_Integer or not 2<=z<=50 or abs(h)>5 or abs(k)>5 or h==k==0:raise ValueError('Hard: diagonal integer half-vector components ≤5, nonsquare radius squared 2–50, translated center <=5')
 else:raise ValueError('Unknown difficulty')
 if profile in QS:
  if LEVELS[profile]!=level:raise ValueError('Observed profile difficulty mismatch')
  if profile=='q-117103' and k!=0:raise ValueError('Zero-y-center profile requires k=0')
  if profile=='q-70990' and h!=0:raise ValueError('Zero-x-center profile requires h=0')
  if profile=='q-117105' and (abs(dx)!=2*abs(dy)):raise ValueError('This distance-factorization profile requires |dx|=2|dy|')
  if profile in ('q-117106','q-117107') and abs(dx)!=abs(dy):raise ValueError('Equal-component factorization profile required')

# Full observed profiles: h,k denote midpoint; z=r²; d²=4z.
# Their intent is inferred from operations, not recovered original author code.
def bank(profile,p):
 h,k,D,z,d,r=values(p)
 if profile=='q-15292':b=[(0,0,z),(-h,k,z),(h,k,z),(h,k,D),(-h,k,D)]
 elif profile=='q-15297':b=[(0,k,r),(k,h,r),(0,k,z),(h,k,r),(h,k,z)]
 elif profile=='q-117102':b=[(-h,-k,z),(h,k,D),(-h,-k,D),(h,-k,z),(h,k,z)]
 elif profile=='q-117103':b=[(h,k,z),(-h,k,D),(h,k,D),(k,h,D),(-h,k,z)]
 elif profile in ('q-117105','q-117107'):b=[(h,-k,z),(-h,-k,D),(h,k,D),(-h,-k,z),(h,k,z)]
 elif profile=='q-117106':b=[(h,k,D),(-h,-k,D),(h,-k,z),(-h,-k,z),(h,k,z)]
 elif profile=='q-70987':b=[(-h,-k,r),(h,k,z),(-h,-k,r,True),(h,k,r),(-h,-k,z)]
 elif profile=='q-70990':b=[(k,h,z,True),(k,h,z),(h,k,z),(-k,h,z),(h,-k,z)]
 elif profile=='authored_easy':b=[(h,k,z),(h,k,D),(h,k,r),(p['x1'],p['y1'],z),(p['x2'],p['y2'],z)]
 elif profile=='authored_method':b=[(h,k,z),(-h,-k,z),(h,k,D),(p['x1'],p['y1'],z),(2*h,2*k,z)]
 else:raise ValueError('Unknown profile')
 return [eq(*a) for a in b]

# Independent complete-equation normalization uses the whole coefficient vector,
# including all algebraic coefficients from every displayed bank member.
def parse_equation(s):
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 def expression(t):
  t=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',t).replace('^','**').replace('{','(').replace('}',')')
  if re.search(r'[^xy0-9+*(). /squrt-]',t):raise ValueError('Unsupported displayed equation token')
  return parse_expr(t,local_dict={'x':X,'y':Y,'sqrt':sp.sqrt},transformations=standard_transformations+(implicit_multiplication_application,))
 a,b=s.split('=');return sp.expand(expression(a)-expression(b))
def fingerprint_eq(s):
 e=parse_equation(s);pol=sp.Poly(e,X,Y) if e.free_symbols <= {X,Y} else sp.Poly(e,*sorted(e.free_symbols,key=str))
 coeff=pol.coeffs();return tuple((mon,sp.simplify(c/coeff[0])) for mon,c in pol.terms())
def equivalent(a,b):
 ea=parse_equation(a);eb=parse_equation(b)
 ratio=sp.cancel(ea/eb)
 return ratio!=0 and not ratio.free_symbols and ratio.is_finite is True

def render_plots(p):
 from plot_circle import render
 output=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
 if not output:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required for new assets')
 path=Path(output).resolve()/(digest(p)[:24]+'.png')
 return str(path),render(p,path)

def aligned(rows,period=False):return r'\begin{aligned}XY & ='+r' \\  & ='.join(rows)+('.' if period else '')+r'\end{aligned}'
def distance(q,p):
 x1,y1,x2,y2=(p[k] for k in ('x1','y1','x2','y2'));dx=x1-x2;dy=y1-y2;h,k,D,z,d,r=values(p);g=math.gcd(abs(dx),abs(dy));root=lambda a:r'\sqrt{'+a+'}'
 sub=lambda a,b:tex(a)+'-'+group(b)
 if q in ('q-70987','q-70990'):first=root('{('+sub(x1,x2)+')}^{2}+{('+sub(y1,y2)+')}^{2}')
 else:first=root('('+sub(x1,x2)+')^{2}+('+sub(y1,y2)+')^{2}')
 if q in ('q-117102','q-70987'):terms=root('{'+tex(dx)+'}^{2}+{'+tex(dy)+'}^{2}')
 elif q=='q-117105':terms=root('{'+tex(abs(dx))+'}^{2}+{'+tex(abs(dy))+'}^{2}')
 else:terms=root((group(dx) if dx<0 else '{'+tex(dx)+'}')+'^{2}+'+(group(dy) if dy<0 else '{'+tex(dy)+'}')+'^{2}')
 rows=[first,terms]
 if q=='q-117105':rows += [root(f'{dx*dx}+{dy*dy}'),root(f'{g*g}\\cdot {dx*dx//(g*g)}+{dy*dy}'),root(f'{g*g}\\cdot {D//(g*g)}'),tex(d)]
 elif q in ('q-117106','q-117107'):rows += [root(f'{dx*dx}+{dy*dy}'),root(f'{g*g}\\cdot {D//(g*g)}'),tex(d)]
 elif q=='q-70990':rows += [root(tex(D)),root(f'{g*g}\\cdot {D//(g*g)}'),tex(d)]
 else:rows += [root(tex(D)),tex(d)]
 return aligned(rows,True)

def source_solution(q,p):
 """Parameterized full-component masks preserve prose and distinct stage nodes."""
 src=QS[q].get(':question/worked-solution')
 if src is None:return None
 h,k,D,z,d,r=values(p);x1,y1,x2,y2=(p[k] for k in ('x1','y1','x2','y2'))
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',src,re.S)
 # Mask complete display components before filling, never replace numeral substrings.
 mask=src
 for i,b in enumerate(blocks):mask=mask.replace('$$\n'+b+'\n$$','$$\n{{block'+str(i)+'}}\n$$',1)
 original=PARAMS[q];op=dict(zip(('x1','y1','x2','y2'),original));oh,ok,_,_,_,orr=values(op)
 for old,new in [(f'X({original[0]},{original[1]})',f'X({x1},{y1})'),(f'Y({original[2]},{original[3]})',f'Y({x2},{y2})'),('r='+tex(orr),'r='+tex(r)),('(a,b)=('+tex(oh)+','+tex(ok)+')','(a,b)=('+tex(h)+','+tex(k)+')')]:mask=mask.replace(old,new)
 radius=(r'r=\frac{XY}{2}=\frac{'+tex(d)+r'}{2}='+tex(r)+'.') if q in ('q-117102','q-117103') else (r'r=\frac{'+tex(d)+r'}{2}='+tex(r)+'.')
 sumtex=lambda a,b:tex(a)+'+'+group(b)
 if q=='q-117105':sy=tex(y1)+'-'+tex(-y2) if y2<0 else sumtex(y1,y2)
 else:sy=sumtex(y1,y2)
 mid=r'(\frac{{x}_{1}+{x}_{2}}{2},\frac{{y}_{1}+{y}_{2}}{2})=(\frac{'+sumtex(x1,x2)+r'}{2},\frac{'+sy+r'}{2})=('+tex(h)+','+tex(k)+')'
 rp='{'+tex(r)+'}^{2}' if r.is_Integer else '{('+tex(r)+')}^{2}'
 equations=r'\begin{aligned}(x-a)^{2}+(y-b)^{2} & ={r}^{2} \\ '+eq(h,k,0,raw=True).split('=')[0]+' & ='+rp+r' \\ '+eq(h,k,z).replace('=',' & =')+r'\end{aligned}'
 replacement=[r'(x-a)^{2}+(y-b)^{2}={r}^{2}.',distance(q,p),radius,mid,equations]
 for i,b in enumerate(replacement):mask=mask.replace('{{block'+str(i)+'}}',b)
 return mask

def normal_solution(p):
 h,k,D,z,d,r=values(p);x1,y1,x2,y2=(p[a] for a in ('x1','y1','x2','y2'));dx=x1-x2;dy=y1-y2;g=math.gcd(abs(dx),abs(dy))
 rows=[r'\sqrt{('+group(x1)+'-'+group(x2)+')^2+('+group(y1)+'-'+group(y2)+')^2}',r'\sqrt{('+tex(dx)+')^2+('+tex(dy)+')^2}',r'\sqrt{'+tex(dx*dx)+'+'+tex(dy*dy)+'}',r'\sqrt{'+tex(D)+'}']
 if not d.is_Integer:rows.append(r'\sqrt{'+tex(g*g)+r'\cdot '+tex(D/(g*g))+'}')
 rows.append(tex(d))
 return ('The general equation of a circle with radius $r$ centered at the point $(a,b)$ is\n\n$$\n(x-a)^2+(y-b)^2=r^2.\n$$\n\nUsing the distance formula to compute the distance between the points '+f'$X({x1},{y1})$ and $Y({x2},{y2}),$ we find that the length of the diameter is\n\n$$\n'+aligned(rows,True)+'\n$$\n\nSo the radius of the circle is\n\n$$\nr=\\frac{XY}{2}=\\frac{'+tex(d)+'}{2}='+tex(r)+'.\n$$\n\nSince the center of a circle is the midpoint of the diameter, to find the center we use the midpoint formula as follows:\n\n$$\n(\\frac{x_1+x_2}{2},\\frac{y_1+y_2}{2})=(\\frac{'+tex(x1)+'+'+group(x2)+'}{2},\\frac{'+tex(y1)+'+'+group(y2)+'}{2})=('+tex(h)+','+tex(k)+')\n$$\n\nSo our circle has radius $r='+tex(r)+'$ and center $(a,b)=('+tex(h)+','+tex(k)+'),$ and therefore it is represented by the following equation:\n\n$$\n\\begin{aligned}(x-a)^2+(y-b)^2 & =r^2 \\\\ '+eq(h,k,0,raw=True).split('=')[0]+' & =('+tex(r)+')^2 \\\\ '+eq(h,k,z).replace('=',' & =')+'\\end{aligned}\n$$')

def source_prompt(q,p,asset):
 src=QS[q][':question/problem'].replace('XY^(―)',r'\overline{XY}').replace(r'\overset{―}{XY}',r'\overline{XY}');old=PARAMS[q];spaces=q in ('q-15292','q-15297');sep=', ' if spaces else ','
 for i,a in enumerate((old[:2],old[2:])):src=src.replace('('+sep.join(map(str,a))+')','{{point'+str(i)+'}}',1)
 for i,b in enumerate(((p['x1'],p['y1']),(p['x2'],p['y2']))):src=src.replace('{{point'+str(i)+'}}','('+sep.join(map(str,b))+')')
 return re.sub(r'!\[\]\([^)]*\)','![]('+asset+')',src)

def sample(level,rng):
 if level=='easy':
  radius=rng.randint(2,10);u,v=(radius,0) if rng.choice([True,False]) else (0,radius);u*=rng.choice([-1,1]);v*=rng.choice([-1,1]);h=k=0
 elif level=='moderate':
  h,k=rng.randint(-5,5),rng.randint(-5,5);radius=rng.randint(1,6);u,v=(radius,0) if rng.choice([True,False]) else (0,radius);u*=rng.choice([-1,1]);v*=rng.choice([-1,1])
 else:h,k=rng.randint(-5,5),rng.randint(-5,5);u,v=rng.choice([i for i in range(-5,6) if i]),rng.choice([i for i in range(-5,6) if i])
 return dict(zip(('x1','y1','x2','y2'),(h+u,k+v,h-u,k-v)))

# Easy: authored origin-centered axis diameters; same full requested equation.
# Moderate: observed translated axis diameters; signed midpoint bookkeeping.
# Hard: observed diagonal diameters; square-factor reduction before halving.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only observed radio field supported')
 template=template or (profile if profile in QS else level+'_diameter')
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('Template/level mismatch')
 profile=profile or (template if template in QS else ('authored_easy' if level=='easy' else 'authored_method'))
 if profile not in (*QS,'authored_easy','authored_method'):raise ValueError('Unknown bank profile')
 if profile=='authored_easy' and level!='easy' or profile=='authored_method' and level=='easy':raise ValueError('Bank/level mismatch')
 if template in QS and profile!=template:raise ValueError('Observed template owns its complete profile')
 rng=random.Random(seed)
 for attempt in range(20000):
  p=dict(parameters) if parameters is not None else sample(level,rng)
  try:
   guard(level,p,profile);p={key:int(value) for key,value in p.items()};choices=bank(profile,p)
   if len({fingerprint_eq(v) for v in choices})!=5:raise ValueError('Whole bank collision')
   h,k,D,z,d,r=values(p);correct=eq(h,k,z)
   match=[i for i,a in enumerate(choices) if equivalent(a,correct)]
   if len(match)!=1:raise ValueError('Whole bank has missing or ambiguous correct equation')
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise RuntimeError('Profile has no eligible sampled parameters')
 raw=template in QS
 original_asset=re.search(r'!\[\]\((.*?)\)',QS[template][':question/problem']).group(1) if raw else None
 source_p=dict(zip(('x1','y1','x2','y2'),PARAMS[template])) if raw else None
 if raw and p==source_p:asset=original_asset;plotmeta={'reused_original':True,'canonical_path':asset}
 else:asset,plotmeta=render_plots(p)
 prompt=source_prompt(template,p,asset) if raw else '![]('+asset+')\n\nThe line segment $\\overline{XY}$ is a diameter of a circle. Given that $X$ and $Y$ have coordinates $('+str(p['x1'])+','+str(p['y1'])+')$ and $('+str(p['x2'])+','+str(p['y2'])+')$, respectively, what is the equation of the circle?'
 solution=source_solution(template,p) if raw else normal_solution(p)
 # Source strings preserve exact choice notation using complete equation format.
 if raw:
  originals=[a[':answer/value'] for a in QS[template][':question/answer-fields'][0][':answer-field/choices']]
  if template in ('q-15292','q-15297'):
   choices=[v.replace('{x}^{2}','x^{2}').replace('{y}^{2}','y^{2}').replace('+',' + ').replace('=',' = ').replace('(x-','(x - ').replace('(x+','(x + ').replace('(y-','(y - ').replace('(y+','(y + ') for v in choices]
  # q117107 is the same complete operation bank in a different source order.
  if template=='q-117107':choices=[choices[i] for i in (4,2,1,0,3)]
 match=[i for i,a in enumerate(choices) if equivalent(a,correct)]
 present={'difficulty':not raw or ':question/difficulty' in QS[template],'solution':solution is not None,'correct':not raw or ':answer-field/correct' in QS[template][':question/answer-fields'][0]}
 content=digest([VERSION,level if present['difficulty'] else None,prompt,solution,sorted(choices),present]);qid=uid(content);fid=uid(qid+':selection')
 answers=[{':answer/id':uid(fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in choices]
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if present['correct']:field[':answer-field/correct']=[':answer/id',answers[match[0]][':answer/id']]
 rng.shuffle(answers)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if present['difficulty']:q[':question/difficulty']=':question.difficulty/'+level
 if present['solution']:q[':question/worked-solution']=solution
 # Endpoint order is incidental to the circle-construction task.
 mathematical=digest([level,sorted([(p['x1'],p['y1']),(p['x2'],p['y2'])])])
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':p,'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_ids':[template] if raw else ([profile] if profile in QS else []),'authored':not raw,'difficulty_design':level,'evidence_only':raw and not present['correct'],'eligible_for_learning':present['correct'],'inferred_correct_equation':correct if not present['correct'] else None,'presence':present,'domain':{'integer_endpoint_bound':12,'integer_center_bound':0 if level=='easy' else 5,'half_vector_component_bound':10 if level=='easy' else (6 if level=='moderate' else 5),'squared_diameter_ceiling':400 if level=='easy' else 200,'level_workload':{'easy':'origin midpoint; axis diameter radius 2–10','moderate':'translated integer midpoint; axis diameter radius 1–6','hard':'diagonal integer half-vector; nonsquare r² 2–50'}[level]},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'plot':plotmeta},'mathematical_fingerprint':mathematical,'content_fingerprint':content,'correct_value':correct,'operation_bank':profile,'plots':[asset]}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 original=g['template'] in QS and g['parameters']==dict(zip(('x1','y1','x2','y2'),PARAMS[g['template']]))
 heading=('Original source replay' if original else 'Generated variant')+' / '+('authored workload ' if ':question/difficulty' not in q else 'difficulty ')+g['difficulty_design']+' / '+g['template']+' / '+g['bank_profile']
 out=[heading,q[':question/problem'],'Choices (author review; correct labeled):']
 for a in f[':answer-field/choices']:out.append((('* CORRECT ' if ':answer-field/correct' in f else '* CORRECT (inferred; source designation absent) ') if equivalent(a[':answer/value'],g['correct_value']) else '* ')+a[':answer/value'])
 out.extend(['Worked solution:',q.get(':question/worked-solution','[Absent from original]')]);return '\n\n'.join(out)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 records=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
