#!/usr/bin/env python3
"""KP17592186096698: integrate once and identify a translated curve family.
Adapted from the supplied generator. Observed banks replay canonical source assets;
normal banks are declared same-method extensions with independent target selection.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,math,os,random,re,subprocess,tempfile,uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose,checked_math_content
HERE=Path(__file__).resolve().parent
VERSION='2.0.0'
RECIPES=json.loads((HERE/'recipes.json').read_text());SPECS={r['name']:r for r in RECIPES}
X=sp.Symbol('x',real=True)
NAMESPACE=uuid.UUID('e9ed35b8-50e2-5476-8e2f-cb47421d6d36')
KP={'db_id':17592186096698,'id':'23789a74-f1e3-5e26-8678-21f84a11a12b','title':'Sketching the Solution Curves of a Differential Equation'}
SUPPORTED={'easy':['linear','quadratic','cubic','logarithmic','reciprocal'],'moderate':['cubic','exponential']}

def output_directory():
    name=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
    if not name:raise ValueError('Set COURSE_ACADEMY_GENERATOR_OUTPUT_DIR to an external asset directory')
    path=Path(name).resolve()
    if path==HERE or HERE in path.parents:raise ValueError('Generated assets must be outside the runtime package')
    path.mkdir(parents=True,exist_ok=True)
    return path

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(NAMESPACE,str(v)))
def exact(v):
 z=sp.sympify(v);assert z.is_Rational;return z

def tex(v):return sp.latex(v).replace('\\log','\\ln')
def expr(s):return sp.sympify(s,locals={'x':X})
def primitive(p):
 a,h,k=map(exact,[p['a'],p['h'],p['k']]);u=X-h;fam=p['family']
 return {'linear':lambda:a*X,'quadratic':lambda:a*u**2,'cubic':lambda:a*u**3,'exponential':lambda:a*sp.exp(k*(X-h)),'logarithmic':lambda:a*sp.log(u),'reciprocal':lambda:a/u}[fam]()
def curve_domains(curves):
 out=[]
 for s in curves:
  c=expr(s);minima=[]
  for term in sp.preorder_traversal(c):
   if term.func==sp.log or (term.is_Pow and term.exp.is_Rational and (term.exp.q==2 or term.exp<0)):
    base=term.args[0];roots=sp.solve(base,X)
    if len(roots)==1 and roots[0].is_real:minima.append(float(roots[0]))
  out.append(max(minima) if minima else None)
 return out

def make_spec(curves,colors,p,labels=None):
 fam=p['family'];h=float(exact(p['h']));a=float(exact(p['a']));k=float(exact(p['k']))
 if fam in ('logarithmic','reciprocal'):xmin=min(-1,h-1);xmax=max(5,h+5);yrange=5
 elif fam=='exponential':xmin=-3/abs(k);xmax=3/abs(k);yrange=max(6,abs(a)*4+3)
 else:xmin=min(-3,h-2);xmax=max(3,h+2);yrange=max(5,abs(a)*5+3)
 spec={'curves':curves,'colors':colors,'bounds':[xmin,xmax,-yrange,yrange],'tick':1 if yrange<=10 else 2,'domain_minima':curve_domains(curves)}
 if fam in ('logarithmic','reciprocal'):
  spec['domain_minima']=[max(0,m) if m is not None else 0 for m in spec['domain_minima']]
 if labels:spec['labels']=labels
 return spec

def render_plots(specs):
 cache=output_directory();paths=[];request=[]
 for spec in specs:
  path=cache/(digest([VERSION,spec])+'.png');paths.append(str(path.resolve()))
  if not path.exists() or not path.with_suffix('.json').exists():request.append({'path':str(path.resolve()),'spec':spec})
 if request:
  fd,name=tempfile.mkstemp(prefix='render-input-',suffix='.json',dir=cache)
  import os
  try:
   with os.fdopen(fd,'w') as f:json.dump(request,f)
   subprocess.run([__import__('sys').executable,str(HERE/'render.py'),name],check=True)
  finally:
   Path(name).unlink(missing_ok=True)
   assert not Path(name).exists(), 'Current render request leaked'
 return paths

def source_text(spec,p):
 old=spec['parameters'];q=spec['source'];family=p['family'];F=primitive(p);g=sp.diff(F,X);a,h,k=map(exact,[p['a'],p['h'],p['k']]);u=X-h
 # Source spelling at the reference parameters belongs to each component mask.
 # Equivalent alternate spelling away from those parameters is explicitly
 # normalized, while the row/prose structure is retained.
 fields={
 'q-119137':[(r'=-1?',r'='+tex(g)+'?'),(r'-\int',tex(a)+r'\int'),(r'-x+C',tex(F)+'+C')],
 'q-50195':[(r'2(x-1)',tex(g)),(r'(x-1)^{2}',tex(F)),(r'2\int',tex(2*a)+r'\int'),(r'(x-1)',tex(u))],
 'q-50196':[(r'-3(x+1)^{2}',tex(g)),(r'-(x+1)^{3}',tex(F)),(r'-3\int',tex(3*a)+r'\int'),(r'(x+1)^{2}',tex(u**2))],
 'q-119132':[(r'\frac{{e}^{-x/4}}{2}',tex(g)),(r'-2{e}^{-x/4}',tex(F)),(r'-4{e}^{-x/4}',tex(sp.exp(k*(X-h))/k)),(r'\frac{1}{2}',tex(a*k)),(r'{e}^{-x/4}',tex(sp.exp(k*(X-h))))],
 'q-49947':[(r'x\cdot \frac{\text{d}y}{\text{d}x}=1',r'x\cdot \frac{\text{d}y}{\text{d}x}='+tex(a)),(r'\frac{1}{x}',tex(a/X)),('\\operatorname{ln}⁡|x|',tex(a)+r'\ln|x|' if a!=1 else '\\operatorname{ln}⁡|x|'),('\\operatorname{ln}⁡x',tex(F))],
 'q-50197':[(r'{x}^{2}\cdot \frac{\text{d}y}{\text{d}x}+1=0',r'{x}^{2}\cdot \frac{\text{d}y}{\text{d}x}+'+tex(a)+'=0'),(r'-\frac{1}{{x}^{2}}',tex(g)),(r'\frac{1}{x}',tex(F)),(r'-\int \frac{1}{{x}^{2}}',tex(-a)+r'\int \frac{1}{{x}^{2}}')],
 'q-50198':[(r'=-2.',r'='+tex(g)+'.'),(r'-2\int',tex(a)+r'\int'),(r'-2x',tex(F))],
 'q-79565':[(r'=2x?',r'='+tex(g)+'?'),(r'2\int x',tex(2*a)+r'\int x'),(r'{x}^{2}',tex(F))],
 'q-79566':[(r'\frac{3}{2}(x+2)^{2}',tex(g)),(r'\frac{1}{2}(x+2)^{3}',tex(F)),(r'\frac{3}{2}',tex(3*a)),(r'(x+2)^{2}',tex(u**2))],
 'q-119139':[(r'-4{e}^{2x}',tex(g)),(r'-2{e}^{2x}',tex(F)),(r'\frac{{e}^{2x}}{2}',tex(sp.exp(k*X)/k)),(r'-4\int',tex(a*k)+r'\int'),(r'-4(',tex(a*k)+'('),(r'{e}^{2x}',tex(sp.exp(k*X)))],
 'q-119142':[(r'-\frac{3(x-1)^{2}}{4}',tex(g)),(r'-\frac{(x-1)^{3}}{4}',tex(F)),(r'\frac{(x-1)^{3}}{3}',tex(u**3/3)),(r'-\frac{3}{4}',tex(3*a)),(r'(x-1)^{2}',tex(u**2))],
 'q-79563':[(r'=3.',r'='+tex(g)+'.'),(r'3\int',tex(a)+r'\int'),(r'3x',tex(F))]}
 replacements=fields[spec['name']]
 # A component's source spelling is reproduced through its mask; changing any
 # relevant parameters inserts newly calculated mathematics, never a payload.
 changes={key:(key if sp.simplify(F-primitive(old))==0 and p['family']==old['family'] else val) for key,val in replacements}
 def apply(text):
  slots={};
  for i,(key,val) in enumerate(changes.items()):
   token='@@COMPONENT'+str(i)+'@@';text=text.replace(key,token);slots[token]=val
  for token,val in slots.items():text=text.replace(token,val)
  oldcs=','.join(old['constants']);newcs=','.join(map(str,p['constants']));text=text.replace('C='+oldcs,'C='+newcs)
  return text
 return apply(q[':question/problem']),apply(q[':question/worked-solution'])

def normalize_source(q):
 q=copy.deepcopy(q)
 q[':question/difficulty']=q[':question/difficulty'][':db/ident'] if ':question/difficulty' in q else None
 if q[':question/difficulty'] is None:del q[':question/difficulty']
 for f in q.get(':question/answer-fields',[]):
  f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
 return q

def worked(p,F,g,path):
 fam=p['family'];a,h,k=map(exact,[p['a'],p['h'],p['k']]);u=X-h
 rows=[r'\int \frac{\text{d}y}{\text{d}x}\,\text{d}x & =\int ('+tex(g)+r')\,\text{d}x']
 if fam in ('quadratic','cubic'):
  n=2 if fam=='quadratic' else 3;coef=n*a;rows += ['y & ='+tex(coef)+r'\int \left('+tex(u**(n-1))+r'\right)\,\text{d}x',' & ='+tex(coef)+r'\left('+tex(u**n/n)+r'\right)+C']
 elif fam=='exponential':rows += ['y & ='+tex(a*k)+r'\int '+tex(sp.exp(k*(X-h)))+r'\,\text{d}x',' & ='+tex(a*k)+r'\left('+tex(sp.exp(k*(X-h))/k)+r'\right)+C']
 elif fam=='logarithmic':rows+=['y & ='+tex(a)+r'\int \frac{1}{x}\,\text{d}x',' & ='+tex(a)+r'\ln|x|+C']
 elif fam=='reciprocal':rows+=['y & ='+tex(-a)+r'\int x^{-2}\,\text{d}x',' & ='+tex(-a)+r'\left(-x^{-1}\right)+C']
 rows+=['y & ='+tex(F)+'+C.']
 cs=','.join(p['constants']);domain=' for $x>0$' if fam in ('logarithmic','reciprocal') else ''
 return 'Integrating the equation, we get\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$\n\nWe can now plot the solution curves by selecting different values for $C.$ The sketch below shows the solution curves for $C='+cs+'$'+domain+'.'+'\n\n![]('+path+')'


def parameter(family,a,h='0',k='1',constants=None):
    return {'family':family,'a':str(a),'h':str(h),'k':str(k),'constants':constants or ['-2','0','2']}

def sample_bank(level,rng,family):
    """A complete bank sampled independently of the selected answer-bearing slot."""
    if family in ('linear','logarithmic','reciprocal'):
        return [parameter(family,a) for a in rng.sample(['-3','-2','-1','1/2','1','2','3'],5)]
    if family in ('quadratic','cubic'):
        magnitudes=['1'] if family=='quadratic' else (['1/2','1','2'] if level=='easy' else ['1/4','1/2','1','2'])
        magnitude=exact(rng.choice(magnitudes))
        slots=rng.sample([(sign,h) for sign in [-1,1] for h in [-2,-1,0,1,2]],5)
        return [parameter(family,sign*magnitude,h) for sign,h in slots]
    rate=exact(rng.choice(['1/4','1/2','2']))
    return [parameter(family,a,k=k) for a,k in rng.sample([(a,sign*rate) for a in ['-2','-1','-1/2','1/2','1','2'] for sign in [-1,1]],5)]

def validate_bank(level,bank):
    if level not in SUPPORTED:raise ValueError('Unsupported difficulty: '+level)
    if len(bank)!=5:raise ValueError('Expected a complete five-family bank')
    family=bank[0]['family']
    if family not in SUPPORTED[level]:raise ValueError('Family outside supported band')
    for p in bank:
        if set(p)!={'family','a','h','k','constants'}:raise ValueError('Unexpected parameter keys')
        if p['family']!=family or not exact(p['a']) or not exact(p['k']):raise ValueError('Invalid bank parameter')
        if len(p['constants'])!=3 or len(set(map(exact,p['constants'])))!=3:raise ValueError('Expected three distinct constants')
        if family in ('logarithmic','reciprocal','linear') and (exact(p['h'])!=0 or exact(p['k'])!=1):raise ValueError('Unexpected domain or shift')
        if family=='exponential':
            if exact(p['h'])!=0:raise ValueError('Redundant exponential shift')
            if str(p['a']) not in ['-2','-1','-1/2','1/2','1','2'] or str(p['k']) not in ['-2','-1/2','-1/4','1/4','1/2','2']:raise ValueError('Outside exponential catalogue')
        elif family in ('quadratic','cubic'):
            magnitudes=[sp.Rational(1)] if family=='quadratic' else list(map(exact,['1/2','1','2'] if level=='easy' else ['1/4','1/2','1','2']))
            if abs(exact(p['a'])) not in magnitudes or exact(p['h']) not in [-2,-1,0,1,2] or exact(p['k'])!=1:raise ValueError('Outside polynomial catalogue')
        elif exact(p['a']) not in list(map(exact,['-3','-2','-1','1/2','1','2','3'])):raise ValueError('Outside coefficient catalogue')
    if family in ('quadratic','cubic') and len({abs(exact(p['a'])) for p in bank})!=1:raise ValueError('Bank must share a polynomial magnitude')
    for i,p in enumerate(bank):
        for q in bank[i+1:]:
            if sp.simplify(sp.diff(primitive(p)-primitive(q),X))==0:raise ValueError('Equivalent solution families')

def bank_plot_specs(bank):
    specs=[]
    for p in bank:
        curves=[sp.sstr(primitive(p)+exact(c)) for c in p['constants']]
        specs.append(make_spec(curves,['red','black','blue'],p))
    # A bank has identical bounds for every option. Target selection cannot affect them.
    bounds=[min(s['bounds'][0] for s in specs),max(s['bounds'][1] for s in specs),min(s['bounds'][2] for s in specs),max(s['bounds'][3] for s in specs)]
    for s in specs:
        s['bounds']=bounds;s['tick']=2 if bounds[3]>10 else 1
        if bounds[1]-bounds[0]<=3.1:s['xtick']=0.5
    return specs

@checked_math_content
def generate(level='moderate',seed=0,template=None,field_type=None,parameters=None,profile=None,bank_parameters=None,target_index=None,shuffle=True):
    if level not in SUPPORTED:raise ValueError('Unsupported difficulty: '+level)
    if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only image radio is supported')
    rng=random.Random(seed)
    if profile and profile.startswith('raw-'):
        spec=SPECS[profile[4:]]
        if level!=spec['level']:raise ValueError('Source replay preserves original difficulty')
        if parameters is not None and parameters!=spec['parameters']:raise ValueError('Observed raster banks are replay-only at original parameters')
        p=copy.deepcopy(spec['parameters']);q=normalize_source(spec['source'])
        q[':question/problem'],q[':question/worked-solution']=map(normalize_prose,source_text(spec,p))
        return {'knowledge_point':dict(KP),'question':q,'generation':{'version':VERSION,'seed':seed,'evidence_only':True,'eligible_for_learning':False,'source_ids':[spec['source_id']],'parameters':p,'bank_profile':profile,'source_basis':4689,'replay':'Canonical images; original complete fields, banks and key designations preserved'}}
    if profile not in (None,'authored-independent-target'):raise ValueError('Unknown bank profile')
    if parameters is not None:raise ValueError('Use bank_parameters with target_index for controlled generated instances')
    # Select answer-bearing assignment BEFORE compatible values or presentation.
    target=rng.randrange(5) if target_index is None else target_index
    if target not in range(5):raise ValueError('Invalid target slot')
    family=template or (bank_parameters[0]['family'] if bank_parameters else rng.choice(SUPPORTED[level]))
    if family not in SUPPORTED[level]:raise ValueError('Unsupported family for band')
    bank=copy.deepcopy(bank_parameters) if bank_parameters is not None else sample_bank(level,rng,family)
    validate_bank(level,bank)
    p=bank[target];F=primitive(p);g=sp.diff(F,X)
    specs=bank_plot_specs(bank)
    solution_spec=copy.deepcopy(specs[target]);solution_spec['labels']=p['constants']
    if family=='exponential':
        solution_spec['label_x']=-2/float(exact(p['k']))
        solution_spec['label_offsets']=[[4,-12] if exact(c)<0 else [4,5] for c in p['constants']]
    paths=render_plots(specs+[solution_spec]);solution_path=paths.pop()
    domain=' for $x>0$' if family in ('logarithmic','reciprocal') else ''
    if family=='logarithmic':equation=r'x\cdot\frac{\text{d}y}{\text{d}x}='+tex(exact(p['a']))
    elif family=='reciprocal':equation=r'x^2\cdot\frac{\text{d}y}{\text{d}x}'+('+' if exact(p['a'])>0 else '')+tex(exact(p['a']))+'=0'
    else:equation=r'\frac{\text{d}y}{\text{d}x}='+tex(g)
    prompt='Which of the following shows some of the solution curves of the differential equation $'+equation+'$'+domain+'?'
    solution=worked(p,F,g,solution_path)
    if family in ('logarithmic','reciprocal'):
        solution='Rearranging the equation, we get $'+r'\frac{\text{d}y}{\text{d}x}='+tex(g)+r'$.'+'\n\n'+solution
    prompt,solution=map(normalize_prose,[prompt,solution])
    # IDs are independent of output location and seed. Duplicate math is allowed to dedup.
    identity=digest([VERSION,level,bank,target])
    fid=uid(identity+':selection')
    choices=[{':answer/id':uid(fid+':'+str(i)),':answer/type':':answer.type/image',':answer/value':path} for i,path in enumerate(paths)]
    correct_id=choices[target][':answer/id']
    if shuffle:rng.shuffle(choices)
    q={':question/id':uid(identity),':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]}
    return {'knowledge_point':dict(KP),'question':q,'generation':{'version':VERSION,'seed':seed,'source_basis':4689,'level':level,'template':family,'bank_profile':'authored-independent-target','provenance':'Conservative same-method bank extension; independent correct-family assignment','parameters':p,'bank_parameters':bank,'target_index':target,'curves':dict(zip(paths,[s['curves'] for s in specs])),'plot_geometry':dict(zip(paths,specs)),'correct_plot':paths[target],'solution_plot':solution_path,'solution_geometry':solution_spec,'domain':'x>0' if family in ('logarithmic','reciprocal') else 'real x','generator_rejections':0,'source_ids':[r['source_id'] for r in RECIPES if r['parameters']['family']==family]}}

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--difficulty',choices=['easy','moderate','hard'],default='moderate')
    ap.add_argument('--count',type=int,default=1);ap.add_argument('--seed',type=int,default=0)
    ap.add_argument('--format',choices=['json'],default='json');ap.add_argument('--template');ap.add_argument('--profile')
    a=ap.parse_args()
    if a.count<1:ap.error('--count must be positive')
    if a.difficulty not in SUPPORTED:ap.error('hard is unsupported by supplied source practice')
    print(json.dumps([generate(a.difficulty,a.seed+i,template=a.template,profile=a.profile) for i in range(a.count)],indent=2))
