#!/usr/bin/env python3
"""KP17592186096698: direct integration followed by selecting a translated
solution-curve family. math/basis1356. Read classification/extraction and README.

Observed raw profiles retain all banks/legacy attrs. Normal profiles are authored
complete operation banks; geometric metric uncertainty in four raw distractors
is explicitly evidence-only. All mathematics is parameterized; no source-ID
answer lookup. Raw geometry is transported by a horizontal affine substitution
and vertical scaling from the original primitive. Atomic private Matplotlib
PNG+sidecar writes use immutable unique requests. No database writes.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,math,random,re,subprocess,tempfile,uuid
from pathlib import Path
import sympy as sp
HERE=Path(__file__).with_suffix('');VERSION='1.0.1'
RECIPES=json.loads((HERE/'recipes.json').read_text());SPECS={r['name']:r for r in RECIPES};CASES=json.loads((HERE/'source-cases.json').read_text())
X=sp.Symbol('x',real=True);NAMESPACE=uuid.UUID('e9ed35b8-50e2-5476-8e2f-cb47421d6d36')
KP={'db_id':17592186096698,'id':'23789a74-f1e3-5e26-8678-21f84a11a12b','title':'Sketching the Solution Curves of a Differential Equation'}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(NAMESPACE,str(v)))
def exact(v):
 z=sp.sympify(v);assert z.is_Rational;return z

def tex(v):return sp.latex(v).replace('\\log','\\ln')
def expr(s):return sp.sympify(s,locals={'x':X})
def primitive(p):
 a,h,k=map(exact,[p['a'],p['h'],p['k']]);u=X-h;fam=p['family']
 return {'linear':lambda:a*X,'quadratic':lambda:a*u**2,'cubic':lambda:a*u**3,'exponential':lambda:a*sp.exp(k*(X-h)),'logarithmic':lambda:a*sp.log(u),'reciprocal':lambda:a/u}[fam]()
def validate_parameters(level,p,raw=None):
 assert set(p)=={'family','a','h','k','constants'},'Unexpected parameter keys'
 a,h,k=map(exact,[p['a'],p['h'],p['k']]);cs=list(map(exact,p['constants']));assert a and k and len(cs)==3 and len(set(cs))==3
 if raw:
  assert p['family']==raw['parameters']['family'];assert abs(a)<=6 and abs(h)<=4 and abs(k)<=4;return
 assert cs==[-2,0,2];assert h in [-2,-1,0,1,2], 'Normal shifts must use familiar integer coordinates'
 if p['family'] in ('linear','logarithmic','reciprocal'):assert h==0 and k==1
 if level=='easy':
  assert p['family'] in ('linear','quadratic','cubic','logarithmic','reciprocal');assert a in [-3,-2,-1,sp.Rational(1,2),1,2,3];assert k==1
 elif level=='moderate':
  assert p['family'] in ('cubic','exponential');assert a in [-2,-1,sp.Rational(-1,2),sp.Rational(-1,4),sp.Rational(1,4),sp.Rational(1,2),1,2]
  if p['family']=='exponential':assert h==0 and k in [2,-2,sp.Rational(1,2),sp.Rational(-1,2),sp.Rational(-1,4)]
  else:assert h!=0 and k==1
 elif level=='hard':
  assert p['family'] in ('cubic','exponential');assert a in [sp.Rational(-3,2),sp.Rational(-2,3),sp.Rational(2,3),sp.Rational(3,2)]
  if p['family']=='exponential':assert h==0 and k in [sp.Rational(-3,2),sp.Rational(-2,3),sp.Rational(2,3),sp.Rational(3,2)]
  else:assert h!=0 and k==1
 else:raise ValueError(level)

def sample(level,rng,family=None):
 if level=='easy':
  f=family or rng.choice(['linear','quadratic','cubic','logarithmic','reciprocal']);a=rng.choice(['-3','-2','-1','1/2','1','2','3']);h=rng.choice(['-2','-1','0','1','2']) if f in ('quadratic','cubic') else '0';k='1'
 elif level=='moderate':
  f=family or rng.choice(['cubic','exponential']);a=rng.choice(['-2','-1','-1/2','-1/4','1/4','1/2','1','2']);h=rng.choice(['-2','-1','1','2']) if f=='cubic' else '0';k='1' if f=='cubic' else rng.choice(['2','-2','1/2','-1/2','-1/4'])
 else:
  f=family or rng.choice(['cubic','exponential']);a=rng.choice(['-3/2','-2/3','2/3','3/2']);h=rng.choice(['-2','-1','1','2']) if f=='cubic' else '0';k='1' if f=='cubic' else rng.choice(['-3/2','-2/3','2/3','3/2'])
 return dict(family=f,a=a,h=h,k=k,constants=['-2','0','2'])

def authored_bank(p,level):
 f=primitive(p);a,h,k=map(exact,[p['a'],p['h'],p['k']]);u=X-h;fam=p['family']
 if fam=='linear':bases=[f,-f,2*f,f/2,(a+sp.sign(a))*X]
 elif fam=='logarithmic':bases=[f,-f,a/u,a*u,a*sp.sqrt(u)]
 elif fam=='reciprocal':bases=[f,-f,a*u,a*u**2,-a*sp.sqrt(u)]
 elif level=='hard':bases=[f,-f,2*f,f/2,f.subs(X,X+1)] if fam=='cubic' else [f,-f,sp.diff(f,X),f.subs(X,-X),f/k]
 elif fam=='quadratic':bases=[f,-f,sp.diff(f,X),a*u**3,f.subs(X,X+1)]
 elif fam=='cubic':bases=[f,-f,sp.diff(f,X),-sp.diff(f,X),f.subs(X,X+1)]
 else:bases=[f,-f,sp.diff(f,X),f.subs(X,-X),f/k]
 # General families are equivalent iff their base derivatives are identical.
 assert all(sp.simplify(sp.diff(v-w,X))!=0 for i,v in enumerate(bases) for w in bases[i+1:]),'Whole-bank family collision'
 cs=list(map(exact,p['constants']));return [[sp.sstr(v+c) for c in cs] for v in bases],[['red','black','blue']]*5,0

def transported_raw_bank(spec,p):
 old=spec['parameters'];a,h,k=map(exact,[p['a'],p['h'],p['k']]);aa,hh,kk=map(exact,[old['a'],old['h'],old['k']]);scale=a/aa
 t=hh+(X-h)*(k/kk if p['family']=='exponential' else 1)
 return [[sp.sstr(expr(c).subs(X,t)*scale) for c in row] for row in spec['curves']],spec['colors'],spec['correct_index']

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
 cache=HERE/'plots';cache.mkdir(exist_ok=True);paths=[];request=[]
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

# Parameterized source math masks. Entire mathematical components are removed
# before inserting changed components; exponent digits are never blind slots.
def source_text(spec,p):
 old=spec['parameters'];q=spec['source'];family=p['family'];F=primitive(p);g=sp.diff(F,X);a,h,k=map(exact,[p['a'],p['h'],p['k']]);u=X-h
 # Source spelling at the reference parameters belongs to each component mask.
 # Equivalent alternate spelling away from those parameters is explicitly
 # normalized, while the row/prose structure is retained.
 fields={
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
  n=2 if fam=='quadratic' else 3;coef=n*a;rows += ['y & ='+tex(coef)+r'\int '+tex(u**(n-1))+r'\,\text{d}x',' & ='+tex(coef)+r'\left('+tex(u**n/n)+r'\right)+C']
 elif fam=='exponential':rows += ['y & ='+tex(a*k)+r'\int '+tex(sp.exp(k*(X-h)))+r'\,\text{d}x',' & ='+tex(a*k)+r'\left('+tex(sp.exp(k*(X-h))/k)+r'\right)+C']
 elif fam=='logarithmic':rows+=['y & ='+tex(a)+r'\int \frac{1}{x}\,\text{d}x',' & ='+tex(a)+r'\ln|x|+C']
 elif fam=='reciprocal':rows+=['y & ='+tex(-a)+r'\int x^{-2}\,\text{d}x',' & ='+tex(-a)+r'\left(-x^{-1}\right)+C']
 rows+=['y & ='+tex(F)+'+C.']
 cs=','.join(p['constants']);domain=' for $x>0$' if fam in ('logarithmic','reciprocal') else ''
 return 'Integrating the equation, we get\n\n$$\n\\begin{aligned}'+r' \\ '.join(rows)+'\\end{aligned}\n$$\n\nWe can now plot the solution curves by selecting different values for $C.$ The sketch below shows the solution curves for $C='+cs+'.$'+domain+'\n\n![]('+path+')'

# EASY: observed direct primitive/translation families. Each draw is an equal
# workload instance; source labels include a simple shifted cubic and positive
# domain logarithmic/reciprocal forms.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: one signed shifted cubic or one scaled exponential integration, plus
# graph identification. No extra IVP, substitution problem, or difficulty ladder.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD (authored): same integral/graph task; nonunit rational primitive scale and
# similar complete plotted near-miss families require metric reading. Each draw
# uses the same workload within its elementary family, with no added ODE method.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 assert level in ('easy','moderate','hard');assert field_type in (None,'radio',':answer-field.type/radio')
 rng=random.Random(seed);raw=bool(profile and profile.startswith('raw-'))
 if raw:
  name=profile[4:];spec=SPECS[name];assert template in (None,name) and level==spec['level'];p=copy.deepcopy(parameters if parameters is not None else spec['parameters']);validate_parameters(level,p,spec)
  # Restricted rearranged source layouts have fixed independent-variable domain.
  if p['family'] in ('logarithmic','reciprocal','linear') or name=='q-79565':assert p['h']=='0' and p['k']=='1'
  curves,colors,ci=transported_raw_bank(spec,p);prompt,solution=source_text(spec,p)
  originals=[a[':answer/value'] for a in spec['source'][':question/answer-fields'][-1][':answer-field/choices']]
  reference=(p==spec['parameters'])
  if reference:paths=originals
  else:
   plot_specs=[make_spec(c,co,p) for c,co in zip(curves,colors)];plot_specs.append(make_spec([sp.sstr(primitive(p)+exact(c)) for c in p['constants']],['red','black','blue'],p,p['constants']));rendered=render_plots(plot_specs);paths=rendered[:-1];solution=re.sub(r'!\[\]\(images/[^)]+\)','![]('+rendered[-1]+')',solution)
  q=normalize_source(spec['source']);q[':question/problem']=prompt;q[':question/worked-solution']=solution
  # Source raw field attributes including missing correct designation stay raw.
  for f in q[':question/answer-fields']:
   for a in f[':answer-field/choices']:a[':answer/value']=paths[originals.index(a[':answer/value'])]
  provenance='observed raw bank; extracted metric uncertainty evidence-only'
 else:
  assert profile in (None,'authored-five-family');assert template in (None,'linear','quadratic','cubic','exponential','logarithmic','reciprocal')
  # Select the complete operation bank before selecting parameter values.
  profile='authored-five-family';p=copy.deepcopy(parameters) if parameters is not None else None
  for attempt in range(200):
   pp=p if p is not None else sample(level,rng,template);validate_parameters(level,pp)
   if template:assert pp['family']==template
   try:curves,colors,ci=authored_bank(pp,level);break
   except AssertionError:
    if parameters is not None:raise
  else:raise ValueError('No complete unambiguous bank')
  p=pp;F=primitive(p);g=sp.diff(F,X);plot_specs=[make_spec(c,co,p) for c,co in zip(curves,colors)];plot_specs.append(make_spec(curves[0],colors[0],p,p['constants']));paths=render_plots(plot_specs);solution=worked(p,F,g,paths[-1]);paths=paths[:-1]
  domain=' for $x>0$' if p['family'] in ('logarithmic','reciprocal') else ''
  prompt=r'Which of the following shows some of the solution curves of the differential equation $\frac{\text{d}y}{\text{d}x}='+tex(g)+'?$'+domain
  q={':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/image',':answer/value':v} for v in paths]}]}
  provenance='authored extension; complete assessed-operation bank'
 F=primitive(p);g=sp.diff(F,X);mathfp=digest([sp.srepr(sp.simplify(g)),p['family'] in ('logarithmic','reciprocal')])
 identity=digest([VERSION,q[':question/problem'],q[':question/worked-solution'],sorted(paths),[[f.get(':answer-field/correct') is not None,f[':answer-field/type'],f[':answer-field/key']] for f in q[':question/answer-fields']],paths[ci]])
 q[':question/id']=uid(identity)
 for i,f in enumerate(q[':question/answer-fields']):
  oldcorrect=f.get(':answer-field/correct',[None,None])[1];f[':answer-field/id']=uid(identity+':field:'+str(i));correctid=None
  for a in f[':answer-field/choices']:
   oldid=a.get(':answer/id');a[':answer/id']=uid(f[':answer-field/id']+':'+a[':answer/value'])
   if raw and oldid==oldcorrect or not raw and a[':answer/value']==paths[ci]:correctid=a[':answer/id']
  if correctid:f[':answer-field/correct']=[':answer/id',correctid]
  rng.shuffle(f[':answer-field/choices'])
 gen={'evidence_only':raw,'eligible_for_learning':not raw,'version':VERSION,'level':level,'seed':seed,'template':template or (spec['name'] if raw else p['family']),'bank_profile':profile,'parameters':p,'mathematical_fingerprint':mathfp,'content_fingerprint':identity,'provenance':provenance,'basis':1356,'curves':{path:row for path,row in zip(paths,curves)},'colors':{path:row for path,row in zip(paths,colors)},'correct_plot':paths[ci],'domain':'x>0' if p['family'] in ('logarithmic','reciprocal') else 'real x','source_ids':[spec['source_id']] if raw else [],'geometry_uncertain_options':spec['uncertain_metric_options'] if raw else [],'renderer':'Matplotlib', 'plot_geometry':{path:make_spec(c,co,p) for path,c,co in zip(paths,curves,colors)}}
 if raw and reference:
  raster=json.loads((HERE/'raster-evidence.json').read_text())
  gen['source_raster_geometry']={a['original']:{'pixel_origin':a['origin'],'pixels_per_unit':a['pixels_per_unit'],'fitted_color_curves':a['fits']} for a in raster if a['source']==spec['name']}
 return {'knowledge_point':dict(KP),'question':q,'generation':gen}

def markdown(r):
 q=r['question'];out=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  out+=['\nField '+f[':answer-field/key']]
  for j,a in enumerate(f[':answer-field/choices']):out+=['**Choice '+str(j+1)+(' — correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '**'),'![]('+a[':answer/value']+')']
 out+=['\n'+q.get(':question/worked-solution','')];return '\n\n'.join(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args();rs=[generate(l,a.seed+i,template=a.template,profile=a.profile) for l in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)];print(json.dumps(rs,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,rs)))
