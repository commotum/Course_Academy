#!/usr/bin/env python3
"""Read a polynomial graph and evaluate three statements (math basis 1356).

All plot formulas are plotting representatives, not recovered original formulas.
Only root locations/categories, end signs, and explicitly marked intercepts are
assessed. Exponents within an odd/even category and positive amplitude do not
count as task variety. Full observed five-option banks are retained as profiles;
source:* preserves missing fields/keys/solution presence, repaired:* explicitly
supplies mathematically verified omissions. Default uses repaired presentation.
No source question payload branch, inverse factor recovery, or graph selection.
See the private extraction, scope, source-case and independent validation files.
"""
from __future__ import annotations
import argparse,hashlib,json,math,os,pathlib,random,re,tempfile,threading,uuid
import sympy as sp
import numpy as np
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186129154-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
D=pathlib.Path(__file__).with_suffix('')
RECIPES=json.loads((D/'recipes.json').read_text())
KP_ID=17592186129154
KP_UUID='a66188f6-3228-59e9-9766-0f9bacbe8443'
TITLE='Identifying True Statements Regarding the Graph of a Given Polynomial'
VERSION='graph-statements-1'
X=sp.Symbol('x',real=True)
NAMESPACE=uuid.UUID(KP_UUID)
RENDER_LOCK=threading.RLock()
ROMAN=('I','II','III')
HARD_BANK=['I and II only','II and III only','I and III only','I only','II only']
HARD={'level':'hard','roots':[-4,-2,2,4],'multiplicities':[1,2,3,1],'coefficient':'1',
 'claims':[['simple_pair',0,2],['even',1],['limit',-1,-1]],'bank':HARD_BANK,'key':'selection',
 'field_type':':answer-field.type/radio','field_present':True,'correct_present':True,
 'solution_mask':None,'source_id':None,'unrated':False}

def dump(v):return json.dumps(v,sort_keys=True,separators=(',',':'))
def digest(v):return hashlib.sha256(dump(v).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(NAMESPACE,dump(v)))
def category(m):return 'simple' if m==1 else 'even' if m%2==0 else 'multiple_odd'
def code(s):
 if s in ['None','None of those listed']:return ()
 return tuple(i for i,w in enumerate(ROMAN) if re.search(r'\b'+w+r'\b',s))
def label(truth):
 t=[ROMAN[i] for i,v in enumerate(truth) if v]
 return 'None' if not t else t[0]+' only' if len(t)==1 else ' and '.join(t)+' only' if len(t)==2 else 'I, II, and III'
def polynomial(p):return sp.expand(sp.Rational(p['coefficient'])*sp.prod((X-r)**m for r,m in zip(p['roots'],p['multiplicities'])))
def evaluate(claim,p):
 f=polynomial(p);op=claim[0];roots=p['roots'];ms=p['multiplicities']
 if op=='value':return f.subs(X,0)==sp.Rational(claim[1])
 if op=='positive':return f.subs(X,0)>0
 if op=='limit':return sp.limit(f,X,sp.oo*claim[1])==sp.oo*claim[2]
 checks={'simple':lambda m:m==1,'not_simple':lambda m:m!=1,'even':lambda m:m%2==0,'odd':lambda m:m%2==1}
 test=checks[op.removesuffix('_pair')]
 return all(test(ms[i]) for i in claim[1:])
def claims_for(t,p):
 claims=json.loads(json.dumps(t['claims']))
 if t.get('source_id')==17592186326715:claims[1][1]=str(polynomial(p).subs(X,0))
 return claims

def validate_parameters(level,t,p):
 if set(p)!={'roots','multiplicities','coefficient'}:raise ValueError('Exactly roots, multiplicities, coefficient are required')
 roots=p['roots'];ms=p['multiplicities'];co=sp.Rational(p['coefficient'])
 if len(roots)!=len(t['roots']) or len(ms)!=len(roots) or len(set(roots))!=len(roots):raise ValueError('Distinct root slots and exact slot count required')
 if any(type(r)is not int or abs(r)>6 for r in roots) or roots!=sorted(roots):raise ValueError('Roots must be increasing integers from -6 to 6')
 if not roots[0]<0<roots[-1]:raise ValueError('Visible roots must span the y-axis')
 if any(type(m)is not int for m in ms) or any(category(m)!=category(a) or m not in [1,2,3,4,5] for m,a in zip(ms,t['multiplicities'])):raise ValueError('Preserve simple/even/multiple-odd category; representatives 1–5')
 # Workload domains are per level, not a permissive common polynomial guard.
 if level=='easy' and (len(roots)!=3 or sum(m==1 for m in ms)<1):raise ValueError('Easy: three displayed roots and at least one simple root')
 if level=='moderate' and (len(roots)!=3 or 0 not in roots):raise ValueError('Moderate: three roots including the y-axis root')
 if level=='hard' and (len(roots)!=4 or set(map(category,ms))!={'simple','even','multiple_odd'}):raise ValueError('Hard: four roots spanning all three visible categories')
 if co==0 or abs(co)>6 or (co>0)!=(sp.Rational(t['coefficient'])>0):raise ValueError('Preserve source leading sign and nonzero magnitude at most 6')
 if t.get('source_id')==17592186129698 and not(roots[0]==-roots[1] and roots[2]>roots[1]):raise ValueError('Paired ± roots must remain symmetric')
 if t.get('source_id') in [17592186129699,17592186233151,17592186247289,17592186247290] and roots[t['roots'].index(0)]!=0:raise ValueError('The assessed y-axis root stays zero')
 if t.get('source_id')==17592186326715 and not(roots[0]<0<roots[1]):raise ValueError('Marked positive intercept requires negative first root and positive others')
 if t.get('source_id')==17592186326715 and polynomial(p).subs(X,0) not in [1,2,3,4]:raise ValueError('Marked exact intercept must remain an integer 1–4')
 # All lobes must remain legible in one linear-axis source-style viewport.
 coeff=np.asarray([float(v) for v in sp.Poly(polynomial(p),X).all_coeffs()]);ext=np.roots(np.polyder(coeff))
 heights=[abs(float(np.polyval(coeff,r.real))) for r in ext if abs(r.imag)<1e-5 and abs(float(np.polyval(coeff,r.real)))>1e-5]
 if not heights or min(heights)/max(heights)<.04:raise ValueError('Whole instance rejected: root lobes would be visually ambiguous')
 return {'roots':roots,'multiplicities':ms,'coefficient':str(co)}

def sample(level,t,rng):
 roots=sorted(rng.sample(range(-5,6),len(t['roots'])))
 if t.get('source_id')==17592186129698:
  a=rng.choice([1,2,3]);roots=[-a,a,rng.choice(range(a+1,6))]
 if level=='moderate' or t.get('source_id')==17592186129699:
  roots=[rng.choice([-4,-3,-2,-1]),0,rng.choice([1,2,3,4])]
 if t.get('source_id')==17592186326715:
  roots=[rng.choice([-5,-4,-3,-2]),rng.choice([1,2]),rng.choice([3,4,5])]
 ms=list(t['multiplicities']) # Category, rather than unassessed exact exponent, is the sampling unit.
 co=sp.sign(sp.Rational(t['coefficient']))
 if t.get('source_id')==17592186326715:
  raw=sp.prod((-r)**m for r,m in zip(roots,ms));co=sp.Rational(rng.choice([1,2,3,4]),raw)
 return {'roots':roots,'multiplicities':ms,'coefficient':str(co)}

def statement(c,p):
 op=c[0]
 if op=='value':return f'$p(0)={c[1]}.$'
 if op=='positive':return '$p(0)$ is positive.'
 if op=='limit':return r'$p(x)\to '+('-' if c[2]<0 else '')+r'\infty$ as $x\to '+('-' if c[1]<0 else '')+r'\infty.$'
 names=[f'$x={p["roots"][i]}$' for i in c[1:]]
 if op.endswith('_pair'):return ' and '.join(names)+' are '+('simple roots.' if op=='simple_pair' else 'roots of '+op.split('_')[0]+' multiplicity.')
 return names[0]+(' is **not** a simple root.' if op=='not_simple' else ' is a simple root.' if op=='simple' else ' is a root of '+op+' multiplicity.')

def explanation(c,p):
 op=c[0];f=polynomial(p)
 if op=='value' or op=='positive':
  y=f.subs(X,0)
  if y!=0:
   side='above' if y>0 else 'below';sign='>' if y>0 else '<'
   return f'The graph meets the $y$-axis {side} the $x$-axis, so $p(0){sign}0.$'
  return 'The graph passes through the $y$-axis at $y=0$, which means that $p(0)=0.$'
 if op=='limit':
  end=sp.limit(f,X,sp.oo*c[1]);direction='right' if c[1]>0 else 'left';sgn='positive' if c[1]>0 else 'negative';up='up' if end==sp.oo else 'down';ysgn='positive' if end==sp.oo else 'negative'
  return f'As $x$ moves {direction} in the {sgn} direction towards $'+('-' if c[1]<0 else '')+r'\infty,$'+f' the $y$ value moves {up} in the {ysgn} direction towards $'+('-' if end==-sp.oo else '')+r'\infty.$'
 parts=[]
 for i in c[1:]:
  r=p['roots'][i];m=p['multiplicities'][i]
  if m==1:parts.append(f'The root $x={r}$ is a simple root because the graph crosses the $x$-axis at the point and the curve is not tangent to the $x$-axis at that point.')
  elif m%2==0:parts.append(f'The root $x={r}$ has an even multiplicity because at $x={r}$ the graph just touches the $x$-axis and reverses direction.')
  else:parts.append(f'The root $x={r}$ has an odd multiplicity because the graph passes through the $x$-axis at this point. The curve is tangent to the $x$-axis at that point, so the root is not simple.')
 return ' '.join(parts)

def fill(mask,p,asset):
 for i,r in enumerate(p['roots']):mask=mask.replace('{r'+str(i)+'}',str(r))
 mask=mask.replace('{asset}',asset).replace('{symmetric_root}',str(p['roots'][1])).replace('{y0}',str(polynomial(p).subs(X,0)))
 return mask

def render_plots(p,marked_intercept=False):
 # Matplotlib's shared state is not thread safe, although paths/temp inputs are.
 with RENDER_LOCK:return _render_plots(p,marked_intercept)

def _render_plots(p,marked_intercept=False):
 """Actual polynomial values, linear axes; unlabeled vertical units except assessed intercept.

 Derivative extrema determine vertical range; viewport ends are extended until both
 end directions are visible. Atomic files and per-call temp files support concurrency.
 """
 f=polynomial(p);key=digest({'f':str(f),'marked':marked_intercept,'renderer':'linear-v6'})
 folder=D/'plots';folder.mkdir(exist_ok=True);png=folder/(key+'.png');side=folder/(key+'.json')
 if png.exists() and side.exists():return str(png.resolve())
 roots=p['roots'];lo=min(roots)-.9;hi=max(roots)+.9
 extrema=[]
 for v in sp.polys.polytools.intervals(sp.diff(f,X),eps=sp.Rational(1,10**8)):
  (a,b),m=v;r=float((a+b)/2)
  if lo<r<hi:extrema.append(r)
 fn=sp.lambdify(X,f,'numpy');values=[float(fn(v)) for v in extrema]+[float(fn(0))]
 upper=max([0]+values);lower=min([0]+values);span=max(upper-lower,1)
 ylim=[lower-.28*span,upper+.28*span]
 for _ in range(40):
  if ylim[0]<float(fn(lo))<ylim[1]:lo-=.3
  else:break
 for _ in range(40):
  if ylim[0]<float(fn(hi))<ylim[1]:hi+=.3
  else:break
 # A single visible coordinate system with exact axes at x=0 and y=0.
 fig,ax=plt.subplots(figsize=(6.1,4.6),dpi=160)
 xx=np.sort(np.unique(np.r_[np.linspace(lo,hi,3000),roots,extrema,0]))
 yy=np.asarray(fn(xx),dtype=float);ax.plot(xx,yy,color='#ed2525',lw=1.7)
 ax.set_xlim(lo,hi);ax.set_ylim(*ylim)
 ax.spines[['top','right']].set_visible(False);ax.spines['bottom'].set_position('zero');ax.spines['left'].set_position('zero')
 ax.set_xticks(sorted(set(roots+[0])));ax.set_yticks([float(f.subs(X,0))] if marked_intercept else [])
 ax.tick_params(axis='both',labelsize=11,pad=4)
 ax.set_axisbelow(False)
 for tick in ax.get_xticklabels()+ax.get_yticklabels():
  tick.set_bbox({'facecolor':'white','edgecolor':'none','pad':.35})
 if marked_intercept:ax.scatter([0],[float(f.subs(X,0))],s=12,color='#ed2525',zorder=4)
 ax.text(hi,0,' x',fontsize=12,va='bottom');ax.text(0,ylim[1],' y',fontsize=12,va='top')
 # Axes have arrowheads; curve endpoints exiting the viewport convey end behavior.
 ax.plot([hi],[0],marker='>',color='#333333',ms=5,clip_on=False);ax.plot([0],[ylim[1]],marker='^',color='#333333',ms=5,clip_on=False)
 fig.tight_layout(pad=1.4)
 fig.canvas.draw()
 label_boxes=[list(map(float,tick.get_window_extent().extents)) for tick in ax.get_xticklabels()+ax.get_yticklabels()]
 fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.png',dir=folder);os.close(fd)
 try:fig.savefig(tmp,facecolor='white');os.replace(tmp,png)
 finally:plt.close(fig);pathlib.Path(tmp).unlink(missing_ok=True)
 payload={'polynomial':str(f),'coefficients':[str(c) for c in sp.Poly(f,X).all_coeffs()], 'roots':roots,'multiplicities':p['multiplicities'],'xlim':[lo,hi],'ylim':ylim,'extrema':extrema,'axes_bbox_pixels':[float(v) for v in ax.bbox.bounds],'label_boxes_pixels':label_boxes,'marked_intercept':marked_intercept,'axis_scale':'linear','zero_axes':True,'matplotlib':matplotlib.__version__,'dimensions':[976,736]}
 fd,tmp=tempfile.mkstemp(prefix=key+'-',suffix='.json',dir=folder);os.close(fd)
 try:pathlib.Path(tmp).write_text(json.dumps(payload,indent=2));os.replace(tmp,side)
 finally:pathlib.Path(tmp).unlink(missing_ok=True)
 return str(png.resolve())

def generate_legacy(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed)
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown difficulty')
 candidates=[k for k,t in RECIPES.items() if t['level']==level]
 if level=='hard':candidates=['mixed_categories_four_roots']
 # Select a whole eligible observed bank/profile before parameters.
 if profile and ':' in profile:
  mode,profile_name=profile.split(':',1)
  if mode not in ['source','repaired']:raise ValueError('Unknown presentation profile')
  if template and template!=profile_name:raise ValueError('Conflicting template/profile')
  template=profile_name;raw=mode=='source'
 else:raw=False
 name=template or rng.choice(candidates)
 if name not in candidates:raise ValueError('Template outside difficulty')
 t=HARD if level=='hard' else RECIPES[name]
 if raw and level=='hard':raise ValueError('The authored hard family has no raw source profile')
 if profile and ':' not in profile and profile not in ['observed','authored']:raise ValueError('Unknown bank profile')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only radio source contract is supported')
 bank=list(t['bank'] or ['I, II, and III','I and II only','II and III only','I only','None'])
 # Missing-field repair's complete bank is authored. Every other bank is observed.
 for attempt in range(200):
  try:p=validate_parameters(level,t,parameters if parameters is not None else sample(level,t,rng))
  except ValueError:
   if parameters is not None:raise
   continue
  claims=claims_for(t,p)
  truth=[bool(evaluate(c,p)) for c in claims];correct=tuple(i for i,v in enumerate(truth) if v)
  if len(set(map(code,bank)))!=len(bank):raise ValueError('Semantically duplicate whole subset choices')
  matches=[s for s in bank if code(s)==correct]
  if len(matches)==1:break
  if parameters is not None:raise ValueError('Correct subset missing/ambiguous in selected whole bank')
 else:raise ValueError('No eligible bank instance')
 marked=t.get('source_id')==17592186326715
 anchor={'roots':t.get('roots'),'multiplicities':t.get('multiplicities'),'coefficient':str(sp.Rational(t['coefficient']))}
 if raw and p==anchor:
  asset=str((pathlib.Path('/media/jake/SSD/EDB/math')/t['asset']).resolve())
 else:asset=render_plots(p,marked)
 if level=='hard':
  prompt=f'![]({asset})\n\nThe graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?\n\n'+'\n\n'.join(r+'. '+statement(c,p) for r,c in zip(ROMAN,claims))
 else:prompt=fill(t['prompt_mask'],p,asset)
 solution=None
 if t.get('solution_mask'):solution=fill(t['solution_mask'],p,asset)
 elif not raw:solution="Let's analyze each statement in turn.\n\n"+'\n\n'.join('- Statement '+r+' is '+('true' if v else 'false')+'. '+explanation(c,p) for r,c,v in zip(ROMAN,claims,truth))+'\n\nTherefore, the correct answer is "'+matches[0]+'".'
 # Full content identity is independent of seed, source aliases and option ordering.
 ident=uid({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(bank),'key':t.get('key') or 'selection','presence':[not raw or t['field_present'],not raw or t['correct_present']]})
 field_id=uid([ident,'selection']);answers=[{':answer/id':uid([field_id,s]),':answer/type':':answer.type/text',':answer/value':s} for s in bank]
 rng.shuffle(answers)
 q={':question/id':ident,':question/problem':prompt}
 if not raw or not t['unrated']:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 if not raw or t['field_present']:
  field={':answer-field/id':field_id,':answer-field/key':t.get('key') or 'selection',':answer-field/type':t.get('field_type') or ':answer-field.type/radio',':answer-field/choices':answers}
  if not raw or t['correct_present']:field[':answer-field/correct']=[':answer/id',uid([field_id,matches[0]])]
  q[':question/answer-fields']=[field]
 # Polynomial magnitude and exponents inside unassessed categories are incidental.
 task={'roots':p['roots'],'categories':[category(m) for m in p['multiplicities']], 'leading_sign':int(sp.sign(sp.Rational(p['coefficient']))),'claims':claims}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,
 'generation':{'version':VERSION,'template':name,'profile':('source:' if raw else 'repaired:')+name,'seed':seed,'parameters':p,'claims':claims,'truth':truth,'mathematical_fingerprint':digest(task),'source_id':t.get('source_id'),'basis':1356,'database':'math','lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','authored_level':level=='hard' or t['unrated'],'bank_origin':'authored hard family' if level=='hard' else 'observed complete subset bank' if t['bank'] else 'absent raw source' if raw else 'authored missing-field repair','authored_solution':not raw and level!='hard' and t['solution_mask'] is None,'source_presence_preserved':raw,'plot':asset,'plot_representative_not_recovered_formula':True,'python_renderer':matplotlib.__version__}}

CURRENT_RECIPES=json.loads((D/'current-recipes.json').read_text())
CURRENT_VERSION='graph-statements-checkbox-2'
GENERATOR_UUID=str(uuid.uuid5(NAMESPACE,'question-generator'))
SUPPORTED_LEVELS=('easy','moderate','hard')

def mathematical_fingerprint(p,claims):
 concrete=[]
 for claim in claims:
  if claim[0] in ('value','positive','limit'):concrete.append(claim)
  else:concrete.append([claim[0].removesuffix('_pair'),sorted(p['roots'][i] for i in claim[1:])])
 return digest({'roots':p['roots'],'categories':[category(m) for m in p['multiplicities']],
  'leading_sign':int(sp.sign(sp.Rational(p['coefficient']))),'claims':sorted(concrete,key=dump)})

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'checkbox',':answer-field.type/checkbox'):raise ValueError('Current source contract is three checkbox fields')
 raw=bool(profile and profile.startswith('source:'))
 if profile and ':' in profile:
  name=profile.split(':',1)[1]
  if template and template!=name:raise ValueError('Conflicting template/profile')
  template=name
 legacy=generate_legacy(level,seed,template=template,parameters=parameters,profile='repaired:'+template if template else None)
 tname=legacy['generation']['template'];p=legacy['generation']['parameters'];claims=legacy['generation']['claims'];truth=legacy['generation']['truth']
 asset=legacy['generation']['plot']
 if tname in CURRENT_RECIPES:
  t=RECIPES[tname];current=CURRENT_RECIPES[tname]
  if raw and p=={k:t[k] for k in ('roots','multiplicities','coefficient')}:asset=str((pathlib.Path('/media/jake/SSD/EDB/math')/current['asset']).resolve())
  prompt=fill(current['prompt_mask'],p,asset);solution=fill(current['solution_mask'],p,asset)
 else:
  if raw:raise ValueError('Authored hard has no source profile')
  prompt=f'![]({asset})\n\nThe graph of a polynomial $p(x)$ is shown above. Which of the following statements are true?\n\nSelect all that apply.\n\n'+'\n'.join('- **'+r+'.** '+statement(c,p) for r,c in zip(ROMAN,claims))
  solution=legacy['question'][':question/worked-solution']
 fp=mathematical_fingerprint(p,claims)
 ident=uid({'version':CURRENT_VERSION,'task':fp,'prompt':prompt.replace(asset,'{asset}'),'solution':solution,'field_contract':'checkbox I II III'})
 fields=[]
 for key,correct in zip(ROMAN,truth):
  fid=uid([ident,key]);answers=[{':answer/id':uid([fid,value]),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid([fid,'true' if correct else 'false'])]})
 q={':question/id':ident,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':fields}
 if not raw or not RECIPES[tname]['unrated']:q[':question/difficulty']=':question.difficulty/'+level
 legacy['question']=q;legacy['generation'].update(version=CURRENT_VERSION,profile=('source:' if raw else 'current:')+tname,mathematical_fingerprint=fp,plot=asset,source_basis=2257,bank_origin='current field-owned boolean banks',source_presence_preserved=raw)
 return legacy

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];out=q[':question/problem']
 for f in q.get(':question/answer-fields',[]):out+='\n\n'+ '\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])
 return out+'\n\n'+q.get(':question/worked-solution','[Raw source has no worked solution.]')

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_legacy', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');a.add_argument('--seed',type=int,default=0);a.add_argument('--count',type=int,default=1);a.add_argument('--format',choices=['markdown','json'],default='markdown');a.add_argument('--template');a.add_argument('--profile');args=a.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
