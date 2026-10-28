"""Complete-component practice derived from e-8889 and investigation exemplars.

The same bank construction applies to every visible family: three plausible
scale results crossed with sec/tan. No special formatting identifies a key.
"""
import hashlib, itertools, json, random, sys, uuid
import sympy as sp
from math_format import checked_math_content, normalize_prose, normalize_tex
VERSION='hyperbolic-cylinder-4'
AXES='xyz'
PERMUTATIONS=list(itertools.permutations(AXES,2))

def tex(x): return sp.latex(sp.sympify(x))
def uid(x): return str(uuid.uuid5(uuid.NAMESPACE_URL,x))
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()
def component(scale,fn): return ('' if scale==1 else tex(scale))+ '\\'+fn+' t'
def normalized(sec,tan,a2,b2): return r'\frac{'+sec+'^2}{'+str(a2)+r'}-\frac{'+tan+'^2}{'+str(b2)+'}=1'

def parameters(level,seed):
 rng=random.Random(seed)
 sec,tan=PERMUTATIONS[rng.randrange(6)]
 if level=='easy':
  a,b=rng.randint(1,4),rng.randint(1,4)
  if a==b==1:b=2
  a2,b2=a*a,b*b;weighted=False
 elif level=='moderate':
  if (seed//4)%2:
   a,b=rng.randint(2,5),rng.randint(1,5)
   a2,b2=a*a,b*b;weighted=True
  else:
   a2,b2=rng.sample([2,3,5,6,7],2);weighted=False
 else:
  # Coefficient normalization and independent, familiar square roots, as in
  # investigation's 2y²-3z²=6. No larger coefficients or new trig identities.
  a2,b2=rng.sample([2,3,5,6,7],2);weighted=True
 target=sec if (seed//2)%2==0 else tan
 # Alternate which scale is requested relative to the supplied one. Roles and
 # coordinate positions are independently randomized, so no visible function
 # signature predicts the larger/smaller answer. Consecutive CLI batches retain
 # both decision cases even at count=2.
 target_high=seed%2==0
 if a2!=b2 and ((a2>b2) if target==sec else (b2>a2)) != target_high:
  a2,b2=b2,a2
 return dict(a2=a2,b2=b2,sec_axis=sec,tan_axis=tan,target=target,weighted=weighted)

def bank_coefficients(c,d,rank,rng):
 # Cross three scale outcomes with both functions. Swapped scale, mixed-axis
 # scale, omitted scale and reciprocal scale are identifiable errors.
 pool=[]
 if c!=d:pool.append((d,'other coordinate scale'))
 radical=bool(c.is_irrational or d.is_irrational)
 plus=sp.sqrt(c*c+d*d) if radical else c+d
 minus=sp.sqrt(abs(c*c-d*d)) if radical else abs(c-d)
 if rank==0:
  candidates=[(minus,'subtract coordinate scales before rooting' if radical else 'subtract coordinate scales'),(1/c,'reciprocal scale'),(sp.Integer(1),'omitted scale'),(plus,'combine coordinate scales'),(c*c,'denominator instead of root')]
 else:
  candidates=[(plus,'add squared coordinate scales before rooting' if radical else 'add coordinate scales'),(c*c,'denominator instead of root'),(sp.Integer(1),'omitted scale'),(1/c,'reciprocal scale')]
 for value,reason in candidates:
  value=sp.simplify(value)
  if value>0 and value!=c and all(value!=v for v,_ in pool):pool.append((value,reason))
  if len(pool)==2:break
 if len(pool)<2:raise ValueError('Insufficient distinct plausible scale errors')
 return [(c,'correct square-root scale'),*pool]

@checked_math_content
def generate_component(level,seed=0,template=None,field_type=None,explicit=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('Unsupported difficulty')
 if template not in [None,'component']:raise ValueError('Use template component; raw profiles preserve source replay')
 if profile not in [None,'normal_component']:raise ValueError('Use normal_component or a raw source replay profile')
 if field_type not in [None,'radio']:raise ValueError('Component practice uses radio choices')
 p=dict(explicit) if explicit is not None else parameters(level,seed)
 if set(p)!={'a2','b2','sec_axis','tan_axis','target','weighted'}:raise ValueError('Use a2,b2,sec_axis,tan_axis,target,weighted')
 a2,b2=p['a2'],p['b2'];sec,tan=p['sec_axis'],p['tan_axis'];target=p['target']
 if type(a2) is not int or type(b2) is not int or not (1<=a2<=25 and 1<=b2<=25):raise ValueError('Small positive integer squared scales required')
 if sec not in AXES or tan not in AXES or sec==tan or target not in [sec,tan] or type(p['weighted']) is not bool:raise ValueError('Invalid coordinate roles')
 a,b=sp.sqrt(a2),sp.sqrt(b2);c,d=(a,b) if target==sec else (b,a);fn='sec' if target==sec else 'tan'
 free=next(v for v in AXES if v not in [sec,tan]);order=['first','second','third'][AXES.index(target)]
 comps={sec:component(a,'sec'),tan:component(b,'tan'),free:free}
 blank=dict(comps);blank[target]=r'\text{_____}'
 def vector(cs):return r'\langle '+r',\,'.join(cs[v] for v in AXES)+r'\rangle'
 standard=normalized(sec,tan,a2,b2)
 if p['weighted']:
  lcm=int(sp.ilcm(a2,b2));k,l=lcm//a2,lcm//b2
  eq=('' if k==1 else str(k))+sec+'^2-'+('' if l==1 else str(l))+tan+'^2='+str(lcm)
  normalize_step='Divide the Cartesian equation by $'+str(lcm)+'$:\n\n$$\n'+standard+'\n$$\n\n'
 else:eq=standard;normalize_step='The equation is already normalized. '
 prompt='The function\n\n$$\nf(t,'+free+')='+vector(blank)+'\n$$\n\nwith $-\\pi/2<t<\\pi/2$ and $'+free+r'\in\mathbb R$ parametrizes the sheet of the hyperbolic cylinder'+'\n\n$$\n'+eq+r',\qquad '+sec+r'\ge '+tex(a)+'.\n$$\n\n'
 if level=='easy':prompt+='Use $\\sec^2 t-\\tan^2 t=1$. '
 prompt+='What is the '+order+' component of $f$?'
 if target==sec:
  recovery=r'\frac{'+sec+'^2}{'+str(a2)+r'}=1+\frac{('+component(b,'tan')+r')^2}{'+str(b2)+r'}=1+\tan^2 t=\sec^2 t'
  branch='Since $'+sec+r'\ge '+tex(a)+r'$ and $\sec t\ge1$ on the given interval, take the positive root.'
 else:
  recovery=r'\frac{'+tan+'^2}{'+str(b2)+r'}=\frac{('+component(a,'sec')+r')^2}{'+str(a2)+r'}-1=\sec^2 t-1=\tan^2 t'
  branch='Choose $'+tan+'='+component(b,'tan')+'$, which takes every real value on the given interval. This is the positive-tangent orientation used in the choices.'
 sol=normalize_step+'The base curve uses $'+sec+'$ and $'+tan+'$; $'+free+'$ is the free coordinate. Substituting the supplied component gives\n\n$$\n'+recovery+'.\n$$\n\n'+branch+' The scale is $'+tex(c)+r'=\sqrt{'+str(a2 if target==sec else b2)+'}$. Thus\n\n$$\n'+target+'='+comps[target]+r',\qquad f(t,'+free+')='+vector(comps)+'.\n$$\n\nCheck in the normalized equation:\n\n$$\n'+r'\begin{aligned}\frac{('+component(a,'sec')+')^2}{'+str(a2)+r'}-\frac{('+component(b,'tan')+')^2}{'+str(b2)+r'}&=\sec^2 t-\tan^2 t\\&=1.\end{aligned}'+'\n$$\n\nThe secant coordinate satisfies the positive-sheet condition. The tangent coordinate ranges over all real values, and arbitrary real $'+free+'$ extends the base curve along the cylinder axis. Therefore the '+order+' component is $'+comps[target]+'$.'
 rng=random.Random(seed ^ 0x9e3779b9)
 coefficients=bank_coefficients(c,d,seed%2,rng)
 choices=[]
 for scale,reason in coefficients:
  for f in ['sec','tan']:
   value=normalize_tex(component(scale,f))
   choices.append({':answer/type':':answer.type/math',':answer/value':value})
 assert len({v[':answer/value'] for v in choices})==6
 correct=normalize_tex(comps[target]);q={':question/problem':normalize_prose(prompt),':question/worked-solution':normalize_prose(sol),':question/difficulty':':question.difficulty/'+level}
 token=digest([VERSION,q,choices]);q[':question/id']=uid(token);fid=uid(token+'/selection')
 for choice in choices:choice[':answer/id']=uid(fid+'/'+choice[':answer/value'])
 ci=next(v[':answer/id'] for v in choices if v[':answer/value']==correct)
 rng.shuffle(choices)
 # Rotate the keyed position across consecutive records, including tiny batches.
 current=next(i for i,v in enumerate(choices) if v[':answer/id']==ci)
 positions=list(range(6))
 random.Random((seed//6)^0x53a9c117).shuffle(positions)
 destination=positions[seed%6]
 choices[current],choices[destination]=choices[destination],choices[current]
 q[':question/answer-fields']=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',ci]}]
 return {'knowledge_point':{'db_id':17592186175973,'id':'a36a5f81-d625-5eff-af81-12f7d91e02bb','title':'Parametrizing a Hyperbolic Cylinder'},'question':q,'generation':{'version':VERSION,'seed':seed,'template':'component','parameters':p,'roles':{'sec':sec,'tan':tan,'target':target},'source_ids':['e-8889','q-164439','q-164521'],'authored_extension':True,'eligible_for_learning':True,'evidence_only':False,'parameter_fingerprint':digest(p),'content_fingerprint':token,'bank_profile':'normal_component','scale_errors':[{'value':tex(v),'reason':r} for v,r in coefficients],'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'difficulty_policy':'authored progression: normalized supported integer scales; normalization or radical; normalization with two radicals'}}
