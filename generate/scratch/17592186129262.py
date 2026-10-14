#!/usr/bin/env python3
"""Area via an unprovided rectangularizing substitution; local draft, steps 3–7.

Easy is authored: product/ratio recognition with first-power boundaries, supported
by unrated q-160373. Moderate preserves three observed linear rearrangement masks.
Hard preserves the two observed squared monomial/quotient masks. Every instance
requires choosing its own transformation; no given-transform or type-I branch.
Raw source profiles preserve omissions and legacy fields and are evidence only.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, os, random, re, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186129262
KP_UUID='c444d700-8c19-5712-8cf5-99555938b0c5'
TITLE='Mapping an Area to a Rectangular Region: Transformations Not Given'
VERSION='rectangular-area-not-given-v1'
ROOT=Path(__file__).resolve().parent
PRIVATE=ROOT/str(KP_ID)
CAPTURE=ROOT.parent/'runs/current/sources'/f'{KP_ID}.json'
SOURCE=json.loads(CAPTURE.read_text())
QUESTIONS={q[':db/id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X,Y,U,V=sp.symbols('x y u v',positive=True)
# Whole eligible family/profile is chosen before any boundary sampling.
TEMPLATES={
 'product_ratio':dict(level='easy',sid=17592186129505,anchor=[1,2,1,2],f='xy',g=r'\frac{y}{x}',u=X*Y,v=Y/X,det=2*V),
 'linear_5_3':dict(level='moderate',sid=17592186129510,anchor=[-2,2,0,3],f='5x-3y',g='4x-2y',u=5*X-3*Y,v=4*X-2*Y,det=sp.Integer(2)),
 'linear_3_1':dict(level='moderate',sid=17592186371879,anchor=[1,3,0,2],f='3x-y',g='x-3y',u=3*X-Y,v=X-3*Y,det=sp.Integer(-8)),
 'linear_4_3':dict(level='moderate',sid=17592186371886,anchor=[-1,2,1,3],f='4x-3y',g='3x-2y',u=4*X-3*Y,v=3*X-2*Y,det=sp.Integer(1)),
 'square_product':dict(level='hard',sid=17592186371872,anchor=[2,4,1,3],f='{x}^{2}y',g='xy',u=X**2*Y,v=X*Y,det=U),
 'product_square_ratio':dict(level='hard',sid=17592186371974,anchor=[1,4,1,3],f='xy',g=r'\frac{x}{{y}^{2}}',u=X*Y,v=X/Y**2,det=-3*V),
}
MATH=re.compile(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',re.S)
def tex(e):
 e=sp.sympify(e)
 if e.is_Rational:return str(e.p) if e.q==1 else ('-' if e<0 else '')+rf'\frac{{{abs(e.p)}}}{{{e.q}}}'
 if e.func==sp.log:return r'\operatorname{ln}⁡'+tex(e.args[0])
 if e.is_Mul:
  c,l=e.as_coeff_Mul()
  if l.func==sp.log:return ('' if c==1 else '-' if c==-1 else tex(c))+tex(l)
 return sp.latex(e).replace(r'\log',r'\ln')
def parameters_checked(level,template,p,raw=False):
 if isinstance(p,dict):
  if set(p)!=set('abcd'):raise ValueError('parameters require exactly a,b,c,d')
  p=[p[k] for k in 'abcd']
 if len(p)!=4 or any(type(x)!=int for x in p):raise ValueError('integer bounds required')
 a,b,c,d=p
 if not(a<b and c<d):raise ValueError('ordered nonempty bounds required')
 if level=='moderate':
  if not all(-4<=x<=6 for x in p) or b-a>5 or d-c>5:raise ValueError('moderate arithmetic bounds exceeded')
 else:
  if not all(1<=x<=8 for x in p) or b-a>5 or d-c>5:raise ValueError('positive first-quadrant bounds 1..8, width <=5 required')
 return dict(zip('abcd',p))
def area(t,p):
 a,b,c,d=(p[k] for k in 'abcd')
 if t.startswith('linear_'):return sp.Rational((b-a)*(d-c),abs(TEMPLATES[t]['det']))
 if t=='square_product':return (d-c)*sp.log(sp.Rational(b,a))
 return sp.Rational(b-a,2 if t=='product_ratio' else 3)*sp.log(sp.Rational(d,c))
def substitutions(t,p):
 a,b,c,d=(p[k] for k in 'abcd');f,g=TEMPLATES[t]['f'],TEMPLATES[t]['g']
 return rf'{f}={a},\,{f}={b},\,{g}={c},\,{g}={d}'
def prompt(t,p):
 a,b,c,d=(p[k] for k in 'abcd');src=QUESTIONS[TEMPLATES[t]['sid']][':question/problem']
 if t=='product_ratio':eq=rf'y = \frac{{{a}}}{{x}}, y = \frac{{{b}}}{{x}}, y = '+('x' if c==1 else str(c)+'x')+', y = '+str(d)+'x';return src[:src.rfind('\n')+1]+'$'+eq+'$'
 if t=='linear_5_3':eq=rf'3y=5x'+signed(-a)+rf',\,3y=5x'+signed(-b)+rf',\,2x=y'+(signed(sp.Rational(c,2)) if c else '')+rf',\,4x=2y'+signed(d)
 elif t=='linear_3_1':eq='y=3x'+signed(-a)+r',\,y=3x'+signed(-b)+r',\,x=3y'+(signed(c) if c else '')+r',\,x=3y'+signed(d)
 elif t=='linear_4_3':eq='3y=4x'+signed(-a)+r',\,3y=4x'+signed(-b)+r',\,3x=2y'+signed(c)+r',\,3x=2y'+signed(d)
 elif t=='square_product':eq=rf'y=\frac{{{a}}}{{{{x}}^{{2}}}},\,y=\frac{{{b}}}{{{{x}}^{{2}}}},\,y=\frac{{{c}}}{{x}},\,y=\frac{{{d}}}{{x}}'
 else:eq=rf'y=\frac{{{a}}}{{x}},\,y=\frac{{{b}}}{{x}},\,x='+('' if c==1 else str(c))+r'{y}^{2},\,x='+str(d)+r'{y}^{2}'
 return re.sub(r'\$\$.*?\$\$',lambda _: '$$\n'+eq+'\n$$',src,flags=re.S)
def signed(n):return ('+' if n>=0 else '-')+tex(abs(n))
def diff(upper,lower):return f'({upper}-'+(f'({lower})' if lower<0 else str(lower))+')'
def region(p,normal=False):
 a,b,c,d=(p[k] for k in 'abcd')
 s=rf'Δ={{(u,v)\,:\,{a}\le u\le {b},\,{c}\le v\le {d}}}'
 return s.replace('={','=\\{').replace('d}', 'd}')[:-1]+r'\}' if normal else s

def solution(t,p,raw=False,asset=None):
 """Frozen shared prose + complete component masks; no short textual replacements."""
 a,b,c,d=(p[k] for k in 'abcd');cfg=TEMPLATES[t];f,g=cfg['f'],cfg['g'];ans=tex(area(t,p))
 if t=='product_ratio':
  # Explicitly authored completion; same five-stage source instruction route.
  text=QUESTIONS[TEMPLATES['linear_5_3']['sid']][':question/worked-solution']
 else:text=QUESTIONS[cfg['sid']][':question/worked-solution']
 blocks=list(MATH.finditer(text)); replacements={
 10:substitutions(t,p),11:rf'u={f},\,v={g}',17:rf'u={f}',19:rf'v={g}',
 18:rf'\begin{{aligned}} & {f}={a}\,⟹\,u={a} \\  & {f}={b}\,⟹\,u={b}\end{{aligned}}',
 20:rf'\begin{{aligned}} & {g}={c}\,⟹\,v={c} \\  & {g}={d}\,⟹\,v='+str(d-1 if raw and t=='square_product' else d)+r'\end{aligned}',
 22:region(p,not raw)}
 if t=='product_ratio':
  replacements[25]=r'\begin{aligned}\frac{∂(u,v)}{∂(x,y)} & =|\begin{aligned}\frac{∂u}{∂x} & \frac{∂u}{∂y} \\ \frac{∂v}{∂x} & \frac{∂v}{∂y}\end{aligned}| \\  & =|\begin{aligned}y & x \\ -\frac{y}{x^2} & \frac{1}{x}\end{aligned}| \\  & =\frac{y}{x}+\frac{y}{x} \\  & =2v.\end{aligned}'
  replacements[28]=r'\frac{∂(x,y)}{∂(u,v)}={(\frac{∂(u,v)}{∂(x,y)})}^{-1}=\frac{1}{2v}.'
 if t!='product_ratio':
  original=blocks[33].group(1);aa,bb,cc,dd=cfg['anchor']
  # Mask each operative component, keeping factorizations and row sequence.
  masks={rf'_{{{aa}}}^{{{bb}}}':rf'_{{{a}}}^{{{b}}}',rf'_{{{cc}}}^{{{dd}}}':rf'_{{{c}}}^{{{d}}}',diff(bb,aa):diff(b,a),diff(dd,cc):diff(d,c)}
  for lo,hi,nlo,nhi in [(aa,bb,a,b),(cc,dd,c,d)]:
   old=rf'(\operatorname{{ln}}⁡{hi}-\operatorname{{ln}}⁡{lo})';new=rf'(\operatorname{{ln}}⁡{nhi}-\operatorname{{ln}}⁡{nlo})';masks[old]=new
  # Simultaneous component masking avoids a changed first interval matching the
  # original second interval, even when the displayed bounds happen to coincide.
  original=re.sub('|'.join(re.escape(k) for k in sorted(masks,key=len,reverse=True)),lambda m:masks[m.group()],original)
  original=original[:original.rfind(' & =')]+ ' & ='+ans+r'\end{aligned}'+('\n' if original.endswith('\n') else '')
  replacements[33]=original.strip('\n')
 else:
  replacements[33]=rf'\begin{{aligned}}{{∬}}_{{D}}\text{{d}}x\text{{d}}y & ={{∬}}_{{Δ}}|\frac{{∂(x,y)}}{{∂(u,v)}}|\,\text{{d}}u\text{{d}}v \\  & ={{∬}}_{{Δ}}\frac{{1}}{{2v}}\,\text{{d}}u\text{{d}}v \\  & =\frac{{1}}{{2}}{{\int }}_{{{a}}}^{{{b}}}\,\text{{d}}u{{\int }}_{{{c}}}^{{{d}}}\frac{{1}}{{v}}\,\text{{d}}v \\  & =\frac{{1}}{{2}}\cdot {diff(b,a)}\cdot (\operatorname{{ln}}⁡{d}-\operatorname{{ln}}⁡{c}) \\  & ={ans}\end{{aligned}}'
 out=[];last=0
 for i,m in enumerate(blocks):
  out.append(text[last:m.start()]);new=replacements.get(i)
  if new is None:out.append(m.group(0))
  elif m.group(1) is not None:out.append('$$\n'+new+'\n$$')
  else:out.append('$'+new+'$')
  last=m.end()
 out.append(text[last:]);text=''.join(out)
 if asset:text=re.sub(r'!\[\]\(images/[^)]+\)',lambda _:'![]('+asset+')',text)
 return text

def bank(t,p,profile):
 a,b,c,d=(sp.Integer(p[k]) for k in 'abcd');w=b-a;h=d-c;A=area(t,p);D=TEMPLATES[t]['det'];L=sp.log(b/a);R=sp.log(d/c)
 if profile.startswith('source_'):
  # Historical complete expression profiles. Opaque operations are evidence only.
  if t=='product_ratio':values=[2*sp.log(d+c),R,R/2,3*R,sp.log(d+c)/2]
  elif t=='linear_5_3':values=[D,-w,w,-D,A]
  elif t=='linear_3_1':values=[1/abs(D),A,w,A/h,w*h]
  elif t=='linear_4_3':values=[1/h,h,A,2*h,1/w]
  elif t=='square_product':values=[-d*L,-A,A,d*L,L/h]
  else:values=[2*R,2*sp.log(b/a/2),sp.log(b/a/2),2*sp.log(b+c),A]
  return values
 if profile!='method':raise ValueError('unknown bank profile')
 # Complete method-derived banks selected before bounds. No individual replacement.
 if t.startswith('linear_'):
  if D==1:values=[A,w,h,1/A,1/w] # omit one rectangle side; invert area/one width
  else:values=[A,w*h,w/abs(D),h/abs(D),w*h*abs(D)] # omit reciprocal/side, forward determinant
 elif t=='product_ratio':values=[A,2*A,(b-a)*R/(2*d),(b-a)/(2*c),((b-a)/2)*sp.log(d)]
 elif t=='square_product':values=[A,-A,d*L,L/h,(b-a)*h] # omit abs, omit lower v, invert width, omit J
 else:values=[A,-A,3*A,R/3,(b-a)*sp.log(d)/3] # abs, factor3, omit u width/lower log
 return values

def render_plot(p,force=False):
 """Independent subprocesses: private unique temporary PNGs; atomic final writes."""
 os.environ.setdefault('MPLCONFIGDIR',str(PRIVATE/'mpl-cache'))
 import matplotlib
 matplotlib.use('Agg')
 from matplotlib.figure import Figure
 from matplotlib.backends.backend_agg import FigureCanvasAgg
 from matplotlib.patches import Rectangle
 key=hashlib.sha256(json.dumps({'bounds':p,'renderer':'rectangle-v4'},sort_keys=True).encode()).hexdigest()[:20]
 out=PRIVATE/'plots';out.mkdir(parents=True,exist_ok=True);path=out/(key+'.png');side=out/(key+'.json')
 if path.exists() and side.exists() and not force:return str(path)
 a,b,c,d=(p[k] for k in 'abcd');xmin=min(0,a)-1;xmax=max(0,b)+1;ymin=min(0,c)-1;ymax=max(0,d)+1
 fig=Figure(figsize=(4.1,3.4),dpi=120);FigureCanvasAgg(fig);ax=fig.add_axes([.11,.12,.80,.77])
 ax.set_xlim(xmin,xmax);ax.set_ylim(ymin,ymax);ax.set_aspect('equal',adjustable='box');ax.axis('off')
 ax.annotate('',xy=(xmax,0),xytext=(xmin,0),arrowprops=dict(arrowstyle='->',color='black',lw=1),zorder=1);ax.annotate('',xy=(0,ymax),xytext=(0,ymin),arrowprops=dict(arrowstyle='->',color='black',lw=1),zorder=1)
 ax.add_patch(Rectangle((a,c),b-a,d-c,facecolor='#dce9f1',edgecolor='none',zorder=0))
 for x in [a,b]:
  if x!=0:ax.plot([x,x],[min(0,c),d],color='#aaaaaa',lw=.6,ls=(0,(5,5)),zorder=2)
  ax.text(x if x else .13,-.23,str(x),ha='center' if x else 'left',va='top',fontsize=11)
 ax.plot([a,b],[c,c],color='red',lw=1.2,zorder=2);ax.plot([a,b],[d,d],color='blue',lw=1.2,zorder=2)
 mid=(a+b)/2
 label_x,label_align=(.18,'left') if a<=0<=b and abs(mid)<.6 else (mid,'center')
 delta_x=mid+(b-a)/8 if a<=0<=b and abs(mid)<.4 else mid
 ax.text(label_x,c-.25,f'$v = {c}$',color='red',ha=label_align,va='top',fontsize=11);ax.text(label_x,d+.12,f'$v = {d}$',color='blue',ha=label_align,fontsize=11)
 delta_y=(c+d)/2+(d-c)/8 if c<=0<=d and abs((c+d)/2)<.4 else (c+d)/2
 ax.text(delta_x,delta_y,r'$\Delta$',ha='center',va='center',color='#2476b5',fontsize=16)
 ax.text(xmax,.09,'$u$',fontsize=13);ax.text(.12,ymax,'$v$',fontsize=13)
 fd,tmp=tempfile.mkstemp(suffix='.png',dir=out);os.close(fd)
 try:fig.savefig(tmp,facecolor='white');os.replace(tmp,path)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 info={'bounds':p,'renderer_version':'rectangle-v4','draw_order':{'fill':0,'zero_axes':1,'colored_edges':2,'labels':3},'limits':[xmin,xmax,ymin,ymax],'horizontal_edges':{'lower':'solid red','upper':'solid blue'},'vertical_edges':'dashed grey guides; set includes both edges','axes':['u','v'],'python':sys.version.split()[0],'matplotlib':matplotlib.__version__,'png_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pixel_dimensions':[492,408]}
 fd,tmp=tempfile.mkstemp(suffix='.json',dir=out);os.close(fd);Path(tmp).write_text(json.dumps(info,indent=2));os.replace(tmp,side)
 return str(path)
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,s))
def shape(raw):
 if isinstance(raw,dict):
  if set(raw)=={':db/ident'}:return raw[':db/ident']
  return {k:shape(v) for k,v in raw.items() if k!=':db/id'}
 if isinstance(raw,list):return [shape(v) for v in raw]
 return raw

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('unknown difficulty')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('observed radio contract only')
 rng=random.Random(seed);eligible=[t for t,c in TEMPLATES.items() if c['level']==level]
 t=template or rng.choice(eligible)
 if t not in eligible:raise ValueError('template/level mismatch')
 cfg=TEMPLATES[t];profile=profile or 'method';raw=profile.startswith('source_')
 if raw and profile!=f"source_{cfg['sid']}":raise ValueError('source profile mismatch')
 for attempt in range(1000):
  if parameters is not None:p=parameters_checked(level,t,parameters,raw)
  elif raw:p=parameters_checked(level,t,cfg['anchor'],raw)
  else:
   if level=='moderate':a,c=rng.randint(-3,2),rng.randint(-1,2)
   else:a,c=rng.randint(1,4),rng.randint(1,4)
   p=parameters_checked(level,t,[a,a+rng.randint(1,4),c,c+rng.randint(1,4)])
  values=bank(t,p,profile);A=area(t,p)
  valid=all(v.is_real is not False and v.is_finite is not False for v in values) and all(sp.simplify(sp.expand_log(values[i]-values[j],force=True))!=0 for i in range(5) for j in range(i+1,5)) and sum(sp.simplify(v-A)==0 for v in values)==1
  if valid or raw:break
  if parameters is not None:raise ValueError('whole bank collision/domain invalid')
 else:raise ValueError('no valid whole instance')
 src=QUESTIONS[cfg['sid']];q=shape(src) if raw else {}
 q[':question/problem']=prompt(t,p)
 # Normal records remove duplicate legacy field and complete inferred omissions.
 if raw:
  for f in q[':question/answer-fields']:
   old=next(z for z in src[':question/answer-fields'] if z[':answer-field/id']==f[':answer-field/id'])
   amap={z[':answer/id']:i for i,z in enumerate(src[':question/answer-fields'][0][':answer-field/choices'])}
   # Duplicate old/new field banks have different ordering/IDs; match anchor value.
   for z in f[':answer-field/choices']:
    i=next(i for i,v in enumerate(src[':question/answer-fields'][0][':answer-field/choices']) if v[':answer/value']==z[':answer/value'])
    z[':answer/value']=tex(values[i])
    if r'\ln ' in z[':answer/value'] or r'\ln ' in src[':question/answer-fields'][0][':answer-field/choices'][i][':answer/value']:z[':answer/value']=z[':answer/value'].replace(r'\operatorname{ln}⁡',r'\ln ')
   if ':answer-field/correct' in f:
    ref=f[':answer-field/correct'][':answer/id'];f[':answer-field/correct']=[':answer/id',ref]
  if ':question/worked-solution' in src:q[':question/worked-solution']=solution(t,p,True)
 else:
  plot=render_plot(p);q[':question/worked-solution']=solution(t,p,False,plot)
  q[':question/difficulty']=':question.difficulty/'+level
  q[':question/answer-fields']=[{':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':tex(v)} for v in values]}]
 content=json.dumps({'version':VERSION,'level':None if raw and ':question/difficulty' not in src else level,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'fields':[{k:v for k,v in f.items() if k not in [':answer-field/id',':answer-field/correct']} for f in q[':question/answer-fields']]},sort_keys=True)
 identity=hashlib.sha256(content.encode()).hexdigest();q[':question/id']=uid(identity)
 if not raw:
  f=q[':question/answer-fields'][0];f[':answer-field/id']=uid(identity+'/field')
  for i,z in enumerate(f[':answer-field/choices']):z[':answer/id']=uid(identity+'/choice/'+z[':answer/value'])
  f[':answer-field/correct']=[':answer/id',next(z[':answer/id'] for z,v in zip(f[':answer-field/choices'],values) if sp.simplify(v-A)==0)]
  rng.shuffle(f[':answer-field/choices'])
 # Canonical task excludes banks/profiles; genuine region bounds matter to area.
 task=hashlib.sha256(str((level,sp.srepr(cfg['u']),sp.srepr(cfg['v']),tuple(p.values()))).encode()).hexdigest()
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'profile':profile,'parameters':p,'source':{k:SOURCE[k] for k in ['database','basis','lineage']},'source_id':cfg['sid'],'content_identity':identity,'mathematical_fingerprint':task,'evidence_only':raw,'eligible_for_learning':not raw,'authored_level':level=='easy','python':sys.version.split()[0],'sympy':sp.__version__,'domain':'first quadrant' if level!='moderate' else 'R2','recipes':'historical expression masks; opaque intent retained' if raw else 'complete method-derived operation bank'}}
# EASY: authored first-power product/ratio, with full transformation discovery.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# MODERATE: observed two oblique linear pairs, fixed primitive coefficient families.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# HARD: observed squared-product/ratio recovery, variable reciprocal Jacobian.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(r):
 q=r['question'];s=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):s+='\n'.join('- $'+z[':answer/value']+'$' for z in f[':answer-field/choices'])+'\n'
 return s+'\n'+q.get(':question/worked-solution','[Original worked solution absent]')
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
