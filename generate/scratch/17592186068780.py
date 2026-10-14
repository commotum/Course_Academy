#!/usr/bin/env python3
"""Frozen-basis reciprocal unknowns generator; steps 3–7 only.

Observed templates: unshifted scalar radio (unrated), vertical-shift sum radio
and two scalar blanks, two-shift sum radio/fieldless, three scalar blanks.
Raw profiles preserve all omissions and opaque historical bank offsets, and
are evidence-only. Normal radio profiles are complete method-derived banks;
blank profiles preserve the source fragment shapes and operative solution masks.
Easy is authored from the unrated unshifted source: one familiar product.
Moderate: read one nonzero vertical shift, subtract it, solve a, then sum
or enter a/k. Hard: additionally read a nonzero horizontal shift and subtract
it from the marked x coordinate, with signed integer differences of 1–3.
No graphing task or new rational-function branch is introduced.
"""
from __future__ import annotations
import argparse,hashlib,json,os,random,re,sys,tempfile,uuid
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/tmp/reciprocal-68780-mpl')
import sympy as sp
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
KP=17592186068780
HERE=Path(__file__).with_suffix('')
SNAP=json.loads((HERE/'source.json').read_text()); REC=SNAP['record']
TITLE=REC[':knowledge-point/title']; VERSION='reciprocal-unknowns-v1'
QS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
# Exact point/asymptote readings independently inspected at native raster size.
ANCHORS={
 'q-39046':dict(a='4',b='0',k='0',px='4',py='1'),
 'q-39047':dict(a='1.5',b='0',k='1',px='1',py='2.5'),
 'q-113479':dict(a='3',b='1',k='2',px='2',py='5'),
 'q-113476':dict(a='2',b='0',k='1.5',px='1',py='3.5'),
 'q-113478':dict(a='-0.5',b='0',k='-1.5',px='1',py='-2'),
 'q-113482':dict(a='-2',b='3',k='0.5',px='1',py='1.5'),
 'q-270750':dict(a='2.5',b='0',k='1',px='1',py='3.5'),
 'q-320718':dict(a='-3',b='-2',k='2.5',px='-5',py='3.5')}
FAMILIES={'easy_radio':('easy','radio','q-39046'),'moderate_sum':('moderate','radio','q-39047'),'moderate_blanks':('moderate','blank','q-270750'),'hard_sum':('hard','radio','q-113482'),'hard_blanks':('hard','blank','q-320718')}
SOURCE_FAMILY={'q-39046':'easy_radio','q-39047':'moderate_sum','q-113476':'moderate_sum','q-113478':'moderate_sum','q-270750':'moderate_blanks','q-113479':'hard_sum','q-113482':'hard_sum','q-320718':'hard_blanks'}
NUM=lambda x:sp.Rational(str(x))
def fmt(x):
 x=NUM(x)
 if x.q==1:return str(x.p)
 if x.q==2:return str(float(x))
 return sp.latex(x)
def add(x):return ('+' if x>=0 else '-')+fmt(abs(x))
def grouped(x):return '('+fmt(x)+')' if x<0 else fmt(x)
def frac(n,d):return r'\frac{'+n+'}{'+d+'}'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def norm(p):
 if set(p)!={'a','b','k','px','py'}:raise ValueError('parameters require exactly a,b,k,px,py')
 p={k:NUM(v) for k,v in p.items()}
 if p['a']==0 or p['px']==p['b'] or p['py']!=p['a']/(p['px']-p['b'])+p['k']:raise ValueError('marked point must lie on a nondegenerate reciprocal curve')
 return p

def guard(level,p,raw=False):
 if raw:
  if any(abs(v)>12 or v.q>2 for v in p.values()):raise ValueError('raw recipe bounds')
  return
 a,b,k,x,y=(p[t] for t in ('a','b','k','px','py'))
 if level!='easy' and any(abs(v)>9 or v.q>2 for v in p.values()):raise ValueError('familiar integer/half-integer bounds')
 if level=='easy':
  if b!=0 or k!=0 or a<=0 or a.q!=1 or not(2<=abs(x)<=8) or not(1<=abs(y)<=4) or x.q!=1 or y.q!=1 or a>32:raise ValueError('easy requires an unshifted positive curve and familiar integer product')
 elif level=='moderate':
  if b!=0 or k==0 or x!=1 or not(sp.Rational(1,2)<=abs(a)<=4) or abs(k)>3:raise ValueError('moderate requires exactly one nonzero shift and x=1')
 elif level=='hard':
  if b==0 or k==0 or b.q!=1 or not(1<=abs(x-b)<=3) or (x-b).q!=1 or abs(b)>3 or abs(k)>3 or not(sp.Rational(1,2)<=abs(a)<=6):raise ValueError('hard requires two nonzero shifts and familiar integer coordinate difference')
 else:raise ValueError(level)

# Whole complete profiles, selected before parameters. No pooled replacements.
def bank(p,level,profile):
 a,b,k,x,y=(p[t] for t in ('a','b','k','px','py'))
 correct=a if level=='easy' else a+k if level=='moderate' else a+b+k
 if profile.startswith('raw:'):
  sid=profile[4:];q=QS[sid];anchor=norm(ANCHORS[sid]);v=anchor['a']+(anchor['k'] if level!='easy' else 0)+(anchor['b'] if level=='hard' else 0)
  fs=q.get(':question/answer-fields',[])
  if not fs:return []
  return [(correct+NUM(ans[':answer/value'])-v,'opaque_observed_offset:'+fmt(NUM(ans[':answer/value'])-v)) for ans in fs[0][':answer-field/choices']]
 if level=='easy':
  if profile=='method-unit':
   if abs(y)!=1:raise ValueError('unit bank requires unit ordinate')
   return [(a,'product'),(x+y,'add_coordinates'),(x-y,'subtract_coordinates'),(y,'omit_x_factor'),(y/x,'reverse_division')]
  if abs(y)==1:raise ValueError('product bank requires nonunit ordinate')
  return [(a,'product'),(x+y,'add_coordinates'),(x-y,'subtract_coordinates'),(x/y,'divide_coordinates'),(y/x,'reverse_division')]
 if level=='moderate':return [(correct,'sum'),(a,'omit_shift'),(k,'shift_only'),(a-k,'reverse_shift_in_sum'),(-a+k,'reverse_scale_sign')]
 return [(correct,'sum'),(a-b+k,'reverse_horizontal_shift'),(-a+b+k,'reverse_scale_sign'),(a+b-k,'reverse_vertical_shift'),(a+b,'omit_vertical_shift')]
def eligible(values):
 if len({sp.srepr(sp.simplify(v)) for v,_ in values})!=len(values):raise ValueError('complete bank has equivalent options')

# Source full prose masks: all math islands replaced by complete role components.
# The opaque raw source never enters the normal default sampler.
def solution(sid,p):
 a,b,k,x,y=(p[t] for t in ('a','b','k','px','py')); d=x-b;delta=y-k
 den='x' if b==0 else 'x'+add(-b)
 function=frac('a',den)+(add(k) if k else '')
 substitution=frac('a',fmt(x) if b==0 else fmt(x)+add(-b))+(add(k) if k else '')
 reducedden=grouped(d) if sid=='q-320718' else fmt(d)
 row3=fmt(y)+r' & =a'+add(k) if sid=='q-270750' else fmt(delta)+r' & ='+frac('a',reducedden)
 rows='y & ='+function+r' \\ '+fmt(y)+r' & ='+substitution+r' \\ '+row3+r' \\ a & ='+fmt(a)+r'.\end{aligned}'
 chain='$$\n'+r'\begin{aligned}'+rows+'\n$$'
 rewrite=function
 if sid=='q-320718' and b<0:rewrite=frac('a','x-('+fmt(b)+')')+add(k)+'='+function
 eq='$$\ny='+rewrite+'.\n$$'
 point='$('+fmt(x)+','+fmt(y)+')$'
 if sid=='q-39046':
  return 'We are given that the point '+point+' lies on the graph. Substituting its coordinates into $y=\\frac{a}{x},$ we obtain\n\n$$\n'+r'\begin{aligned}'+fmt(y)+r' & ='+frac('a',fmt(x))+r' \\ a & ='+grouped(x)+r'\cdot '+grouped(y)+'='+fmt(a)+r'.\end{aligned}'+'\n$$'
 if b==0:
  final='a+k='+(fmt(k)+add(a) if sid=='q-39047' else fmt(a)+add(k))+'='+fmt(a+k)+'.'
  tokens=['$y='+fmt(k)+'.$','$k='+fmt(k)+'$',eq,point,chain]
  if sid!='q-270750':tokens.append('$'+final+'$')
 else:
  tokens=['$y='+fmt(k)+',$','$x='+fmt(b)+'.$','$k='+fmt(k)+'$','$b='+fmt(b)+',$',eq,point,chain]
  if sid!='q-320718':tokens.append('$a+b+k='+fmt(a)+add(b)+add(k)+'='+fmt(a+b+k)+'.$')
 raw=QS[sid][':question/worked-solution'];i=iter(tokens)
 result=re.sub(r'\$\$[\s\S]*?\$\$|\$[^$]*\$',lambda m:next(i),raw)
 try:next(i);raise ValueError('unused math island')
 except StopIteration:pass
 return result

def render_plots(p,output_dir=None):
 """Atomic fresh renderer/cache, with exact geometry sidecar; no shared inputs."""
 out=Path(output_dir or HERE/'plots');out.mkdir(parents=True,exist_ok=True)
 serial={k:str(v) for k,v in p.items()};key=digest({'renderer':'mpl-v5','parameters':serial})
 path=out/(key+'.png');side=out/(key+'.json')
 if path.exists() and side.exists():return str(path),json.loads(side.read_text())
 a,b,k,x,y=(float(p[t]) for t in ('a','b','k','px','py'))
 lo=min(0,b,x,b-abs(x-b))-max(3,abs(x-b));hi=max(0,b,x,b+abs(x-b))+max(3,abs(x-b))
 bottom=min(0,k,y,k-abs(y-k))-max(3,abs(y-k));top=max(0,k,y,k+abs(y-k))+max(3,abs(y-k))
 fig=Figure(figsize=(6,5.07),dpi=120);FigureCanvasAgg(fig);ax=fig.add_axes([.07,.07,.86,.86]);ax.set(xlim=(lo,hi),ylim=(bottom,top));ax.axis('off')
 ax.annotate('',xy=(hi,0),xytext=(lo,0),arrowprops={'arrowstyle':'->','color':'black','lw':1.2});ax.annotate('',xy=(0,top),xytext=(0,bottom),arrowprops={'arrowstyle':'->','color':'black','lw':1.2})
 ax.text(hi,0,'$x$',va='top',fontsize=13);ax.text(0,top,'$y$',ha='right',fontsize=13)
 if b:ax.axvline(b,color='#888888',ls=(0,(4,4)),lw=.9);ax.text(b,0,fmt(p['b']),ha='center',va='top',fontsize=12,bbox={'fc':'white','ec':'none','pad':1})
 if k:ax.axhline(k,color='#888888',ls=(0,(4,4)),lw=.9);ax.text(0,k,fmt(p['k']),ha='right',va='top' if ((b!=0 and a/(-b)>0) or (b==0 and a<0)) else 'bottom',fontsize=12,bbox={'fc':'white','ec':'none','pad':1})
 samples=[]
 for left,right in [(lo,b-.015),(b+.015,hi)]:
  xs=np.linspace(left,right,1000);ys=a/(xs-b)+k;ax.plot(xs,ys,color='#2877bd',lw=1.5,clip_on=True)
  for xx in np.linspace(left,right,23):
   yy=a/(xx-b)+k
   if bottom+.2<yy<top-.2:samples.append([xx,yy])
 ax.plot([x],[y],'o',ms=4.5,color='#2877bd');ax.annotate('('+fmt(p['px'])+', '+fmt(p['py'])+')',(x,y),xytext=(8,9 if a>0 else -18),textcoords='offset points',fontsize=12,ha='left',bbox={'fc':'white','ec':'none','pad':.7})
 fig.canvas.draw();w,h=fig.canvas.get_width_height();transform=lambda pt:[float(v) for v in ax.transData.transform(pt)]
 evidence={'parameters':serial,'renderer':'Matplotlib','matplotlib_version':matplotlib.__version__,'python_version':sys.version.split()[0],'dimensions':[w,h],'bounds':[lo,hi,bottom,top],'origin_pixel_bottom':transform((0,0)),'point_pixel_bottom':transform((x,y)),'curve_samples':[[xx,yy,*transform((xx,yy))] for xx,yy in samples],'vertical_asymptote':b,'horizontal_asymptote':k,'branch_sign':int(sp.sign(p['a'])),'label_values':{'point':['('+fmt(p['px'])+', '+fmt(p['py'])+')'],'ticks':[fmt(p[t]) for t in ('b','k') if p[t]!=0]},'graph_equation':'y=a/(x-b)+k','artist_text_readback':[{'text':t.get_text(),'bbox_pixels_bottom':list(t.get_window_extent(fig.canvas.get_renderer()).bounds)} for t in ax.texts if t.get_text()]}
 fd,tmp=tempfile.mkstemp(suffix='.png',prefix='render-',dir=out);os.close(fd)
 try:fig.savefig(tmp,facecolor='white');os.replace(tmp,path)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 fd,tmp=tempfile.mkstemp(suffix='.json',prefix='side-',dir=out);os.close(fd)
 try:Path(tmp).write_text(json.dumps(evidence,indent=2));os.replace(tmp,side)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 return str(path),evidence

def sample(level,rng):
 if level=='easy':
  x=rng.choice(list(range(2,9)));y=rng.choice([1,2,3,4]);sgn=rng.choice([-1,1]);return norm(dict(a=x*y,b=0,k=0,px=x*sgn,py=y*sgn))
 k=rng.choice([sp.Rational(i,2) for i in range(-6,7) if i]);a=rng.choice([sp.Rational(i,2) for i in range(-8,9) if i])
 b=0 if level=='moderate' else rng.choice([-3,-2,-1,1,2,3]);d=1 if level=='moderate' else rng.choice([-3,-2,-1,1,2,3]);return norm(dict(a=a,b=b,k=k,px=b+d,py=a/d+k))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 rng=random.Random(seed);raw=bool(profile and profile.startswith('raw:'))
 if raw:
  sid=profile[4:]
  if sid not in QS:raise ValueError(profile)
  inferred=SOURCE_FAMILY[sid];template=template or inferred
  if template!=inferred:raise ValueError('source family mismatch')
 else:
  available=[t for t,(lev,ft,_) in FAMILIES.items() if lev==level and (not field_type or ft==field_type)]
  if template is None:template=rng.choice(available)
  sid=FAMILIES[template][2]
  if profile and profile.startswith('style:'):
   sid=profile[6:]
   if SOURCE_FAMILY.get(sid)!=template:raise ValueError('style family mismatch')
  elif profile not in (None,'method','method-unit','method-product'):raise ValueError('unknown profile')
 lev,ft,_=FAMILIES[template]
 if lev!=level or (field_type and ft!=field_type):raise ValueError('level or field mismatch')
 selected=profile or (rng.choice(['method-unit','method-product']) if level=='easy' else 'method' if ft=='radio' else 'style:'+sid)
 if level=='easy' and selected=='method':selected='method-unit' if parameters and abs(NUM(parameters['py']))==1 else 'method-product'
 for _ in range(2000):
  p=norm(parameters) if parameters is not None else sample(level,rng)
  try:
   guard(level,p,raw)
   if raw and ((level=='easy' and (p['b']!=0 or p['k']!=0)) or (level=='moderate' and (p['b']!=0 or p['k']==0)) or (level=='hard' and (p['b']==0 or p['k']==0)) or (sid=='q-270750' and p['px']!=1)):raise ValueError('raw family operative roles violated')
   values=bank(p,level,selected) if ft=='radio' else []
   if values:eligible(values)
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('sampling domain exhausted')
 source=QS[sid];anchor=p==norm(ANCHORS[sid])
 if raw and anchor:
  imagepath=re.search(r'!\[\]\((.*?)\)',source[':question/problem']).group(1);plot={'source_asset':imagepath,'geometry_reference':'plot-extraction.json'}
 else:imagepath,plot=render_plots(p)
 prompt=re.sub(r'!\[\]\((.*?)\)',lambda _: '![]('+imagepath+')',source[':question/problem'])
 q={':question/problem':prompt}
 if not raw or ':question/difficulty' in source:q[':question/difficulty']=':question.difficulty/'+level
 if not raw or ':question/worked-solution' in source:q[':question/worked-solution']=solution(sid,p)
 a,b,k=(p[t] for t in ('a','b','k'));correct=a if level=='easy' else a+k if level=='moderate' else a+b+k
 # Preserve full raw field presence and field order. Normal fieldless source gets
 # a radio completion; normal missing designation is independently inferred.
 fs=[]
 if not raw or ':question/answer-fields' in source:
  original=source.get(':question/answer-fields',[])
  specs=[(f[':answer-field/key'],f[':answer-field/type'][':db/ident'].split('/')[-1],f) for f in original] if original else [('selection','radio',{})]
  for key,kind,old in specs:
   if kind=='radio':vals=values
   else:
    target={'field-1':a,'field-2':b if level=='hard' else k,'field-3':k}[key];vals=[(target,'fragment:'+key)]
   fs.append({'key':key,'kind':kind,'values':[(fmt(v),recipe) for v,recipe in vals],'correct':fmt(correct if kind=='radio' else target),'correct_present':not raw or ':answer-field/correct' in old})
 # Semantic tasks include assessed curve, point, response role; exclude bank/style,
 # seed and order. No incidental plot padding/renderer offsets enter this key.
 task=digest({'level':level,'curve':{t:str(p[t]) for t in ('a','b','k')},'point':[str(p['px']),str(p['py'])],'response':template.split('_',1)[1],'scale':'explicit coordinate labels'})
 content=digest({'version':VERSION,'question':q,'fields':[{**f,'values':sorted(value for value,recipe in f['values'])} for f in fs],'task':task})
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,str(KP)+':'+content));q[':question/id']=qid
 if not raw or ':question/answer-fields' in source:
  q[':question/answer-fields']=[]
  for f in fs:
   fid=str(uuid.uuid5(uuid.UUID(qid),f['key']));answers=[];cid=None
   for value,recipe in f['values']:
    aid=str(uuid.uuid5(uuid.UUID(fid),'math:'+value));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':value})
    if value==f['correct']:cid=aid
   if f['kind']=='radio':rng.shuffle(answers)
   fld={':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':':answer-field.type/'+f['kind'],':answer-field/choices':answers}
   if f['correct_present']:
    if cid is None:raise ValueError('correct answer missing from complete bank')
    fld[':answer-field/correct']=[':answer/id',cid]
   q[':question/answer-fields'].append(fld)
 return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':selected,'parameters':{t:str(v) for t,v in p.items()},'parameter_fingerprint':task,'content_fingerprint':content,'source':{t:SNAP[t] for t in ('database','basis','lineage')},'source_ids':[sid],'evidence_only':raw,'eligible_for_learning':not raw,'bank_origin':'opaque observed parameterized offset mask' if raw and ft=='radio' else 'authored method bank' if ft=='radio' else 'observed scalar fragments','authored_level':level=='easy','python_version':sys.version.split()[0],'sympy_version':sp.__version__,'matplotlib_version':matplotlib.__version__,'plot':plot,'plot_asset':imagepath,'domain':'x != b','solution_style':sid}}

# EASY: authored unshifted source extension, exactly one coordinate product.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: observed one-shift method; sum radio and two scalar blanks.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: observed two-shift method; sum radio and three scalar blanks.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];lines=[q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):lines+=['\n'+f[':answer-field/key']+': '+', '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])]
 if ':question/worked-solution' in q:lines+=['\nWorked solution\n',q[':question/worked-solution']]
 return '\n'.join(lines)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--parameters');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty];rows=[generate(l,args.seed+i,template=args.template,profile=args.profile,parameters=json.loads(args.parameters) if args.parameters else None) for l in levels for i in range(args.count)]
 print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in rows))
