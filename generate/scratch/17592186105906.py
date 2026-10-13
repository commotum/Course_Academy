#!/usr/bin/env python3
"""Triangle area from a concave quadrilateral; draft only, math basis 1356.

Observed hard recipes preserve source prose and arithmetic stages. Raw profiles
are public evidence only: historical scalar distractors are opaque offsets,
not recovered learner error operations. Authored easy supplies the outer area;
authored moderate supplies integer sides and a right included angle; hard uses
the observed calculator method. Every level assesses outer minus quadrilateral.
No database writes. See adjacent evidence README for validation and limitations.
"""
import argparse, hashlib, json, math, os, random, re, sys, tempfile, uuid
from pathlib import Path
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR','/tmp/kp17592186105906-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon
from threading import Lock
D=Path(__file__).with_suffix(''); KP=17592186105906
SRC=json.loads((D/'source.json').read_text()); REC=SRC['record']
QS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
CFG=json.loads((D/'source-config.json').read_text()); VERSION='1.0.1'
NS=uuid.UUID(REC[':knowledge-point/id']); LOCK=Lock()
TEMPLATES={**{k:{'level':'hard','kind':v['field_type']} for k,v in CFG.items()},'easy_area':{'level':'easy','kind':'radio'},'moderate_right':{'level':'moderate','kind':'radio'}}
BANK_PROFILES={**{'raw_'+s:{'template':s,'origin':'observed opaque evidence','eligible_for_learning':False} for s in QS},**{'repaired_'+s:{'template':s,'origin':'supported presentation/math repairs, opaque bank','eligible_for_learning':False} for s in QS},'method':{'origin':'authored complete method bank','eligible_for_learning':True}}
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def digest(x):return hashlib.sha256(canon(x).encode()).hexdigest()
def num(x):return str(int(x)) if float(x).is_integer() else str(float(x))
def rounding(x):return int(sp.floor(sp.N(x,40)+sp.Rational(1,2)))
def calculation(p):
 T=sp.Rational(str(p['a']))*sp.Rational(str(p['b']))*sp.sin(sp.pi*p['angle']/180)/2
 return T,rounding(T),rounding(T)-p['quadrilateral']
def fmt(n,u,pattern=None):
 if pattern is None:return str(n)+r'{\text{ '+u+r'}}^{2}'
 return re.sub(r'^\d+',str(n),pattern)
def replace_unit(text,old,new):
 for space in ('',' ',' '):
  text=text.replace(r'\text{'+space+old+'}',r'\text{'+space+new+'}')
 return text.replace(old+'^{2}',new+'^{2}')

def source_solution(s,p,raw=False):
 """Parameterized per-source row masks, retaining omissions and complete prose."""
 q=QS[s]; original=q.get(':question/worked-solution')
 if original is None and raw:return None
 if original is None:return normal_solution(p, 'product')
 a=CFG[s]['parameters'];T,R,c=calculation(p);T0,R0,c0=calculation(a)
 rows=original.split(r'\\')
 # Every source starts with formal area, substitution, product evaluation.
 subs=rows[1];tokens=list(re.finditer(r'(?<=\\cdot )\d+(?:\.\d+)?',subs))
 if len(tokens)!=2:raise AssertionError('source substitution mask')
 for hit,v in reversed(list(zip(tokens,[p['a'],p['b']]))):subs=subs[:hit.start()]+num(v)+subs[hit.end():]
 subs=subs.replace('{'+num(a['angle'])+'}^{∘}','{'+num(p['angle'])+'}^{∘}')
 rows[1]=subs
 product=rows[2]
 if CFG[s]['style'].startswith('product'):
  product=product.replace(r'\cdot '+num(a['a']*a['b'])+r'\cdot',r'\cdot '+num(p['a']*p['b'])+r'\cdot')
 else:product=product.replace(num(a['a']*a['b']/2),num(p['a']*p['b']/2))
 rows[2]=product.replace('{'+num(a['angle'])+'}^{∘}','{'+num(p['angle'])+'}^{∘}')
 text=r'\\'.join(rows)
 dec0=f'{math.floor(float(T0)*1000)/1000:.3f}';dec=f'{math.floor(float(T)*1000)/1000:.3f}'
 text=text.replace(dec0,dec)
 text=text.replace('≈'+str(R0),'≈'+str(R))
 text=text.replace(f'={R0}-{a["quadrilateral"]}',f'={R}-{p["quadrilateral"]}')
 text=text.replace('='+str(c0)+r'{\text','='+str(c)+r'{\text')
 # All source units are whole math text components, never variable substrings.
 text=replace_unit(text,a['unit'],p['unit'])
 if not raw and s=='q-285754':text=text.replace(r'{\text{ m}}^{2}',r'{\text{ '+p['unit']+r'}}^{2}')
 return text

def normal_solution(p,style='product'):
 T,R,c=calculation(p);a,b,t,Q,u=[p[k] for k in ('a','b','angle','quadrilateral','unit')]
 if style=='easy':
  return "The difference of the areas of $△ABD$ and the quadrilateral $ABCD$ gives the area of $△BCD.$ Therefore,\n\n$$\n"+r'\begin{aligned}{A}_{△BCD} & ={A}_{△ABD}-{A}_{ABCD} \\ & ='+f'{p["outer"]}-{Q}'+r' \\ & ='+fmt(p['outer']-Q,u)+r'.\end{aligned}'+'\n$$'
 prod=(num(a*b/2)+r'\cdot ') if style=='half' else (r'\frac{1}{2}\cdot '+num(a*b)+r'\cdot ')
 decimal='' if t==90 else r' \\ & ='+f'{math.floor(float(T)*1000)/1000:.3f}'+'…'
 return "Let's start by finding the area of $△ABD.$ We get \n\n$$\n"+r'\begin{aligned}{A}_{△ABD} & =\frac{1}{2}\cdot AB\cdot AD\cdot \operatorname{sin}⁡A \\ & =\frac{1}{2}\cdot '+num(a)+r'\cdot '+num(b)+r'\cdot \operatorname{sin}⁡{'+str(t)+r'}^{∘} \\ & ='+prod+r'\operatorname{sin}⁡{'+str(t)+r'}^{∘}'+decimal+r' \\ & ≈'+fmt(R,u)+r'\end{aligned}'+'\n$$\n\nrounded to the nearest integer.\n\nThe difference of the areas of $△ABD$ and the quadrilateral $ABCD$ gives the area of $△BCD.$ Therefore,\n\n$$\n'+r'\begin{aligned}{A}_{△BCD} & ={A}_{△ABD}-{A}_{ABCD} \\ & ='+f'{R}-{Q}'+r' \\ & ='+fmt(c,u)+r'.\end{aligned}'+'\n$$'

def geometry(p):
 T,_,_=calculation(p);Q=p['quadrilateral'];a,b,t=p['a'],p['b'],math.radians(p['angle'])
 A=[0.,0.];B=[-a*math.sin(t),a*math.cos(t)];DD=[0.,float(b)]
 C=[Q/float(T)*(B[0]+DD[0])/2,Q/float(T)*(B[1]+DD[1])/2]
 rot=math.radians(p.get('orientation',0));ct,st=math.cos(rot),math.sin(rot)
 return {k:[ct*x-st*y,st*x+ct*y] for k,(x,y) in zip('ABCD',[A,B,C,DD])}

def render(p):
 """Atomic unique-temp PNG/sidecar writes; JSON-native metadata on both paths."""
 spec={'parameters':p,'vertices':geometry(p),'renderer':'Matplotlib','matplotlib_version':matplotlib.__version__,'python_version':sys.version.split()[0],'dpi':150,'size_inches':[5,4],'layout_version':5}
 path=D/'plots'/('triangle-'+digest(spec)[:24]+'.png');side=path.with_suffix('.json');path.parent.mkdir(exist_ok=True)
 if path.exists() and side.exists():return str(path.resolve()),json.loads(side.read_text())
 with LOCK:
  if path.exists() and side.exists():return str(path.resolve()),json.loads(side.read_text())
  v=spec['vertices'];fig,ax=plt.subplots(figsize=(5,4),dpi=150);ax.set_aspect('equal');ax.axis('off')
  pts=[v[k] for k in 'ABCD'];ax.add_patch(Polygon(pts,closed=True,fill=False,edgecolor='black',linewidth=1.8))
  ax.plot(*zip(v['B'],v['D']),color='black',linestyle=(0,(4,3)),linewidth=1)
  centroid=[sum(v[k][i] for k in 'ABD')/3 for i in (0,1)];scale=max(p['a'],p['b']);r=.09*min(p['a'],p['b'])
  for k,(x,y) in v.items():
   dx,dy=x-centroid[0],y-centroid[1]
   if k=='C':dx,dy=(v['B'][0]+v['D'][0])/2-x,(v['B'][1]+v['D'][1])/2-y
   length=math.hypot(dx,dy);offset=min(.075*scale,.35*length) if k=='C' else .075*scale
   ax.text(x+dx/length*offset,y+dy/length*offset,k,fontsize=14,ha='center',va='center',fontstyle='italic',bbox={'facecolor':'white','edgecolor':'none','pad':.15} if k=='C' else None)
  for k,val in [('B',p['a']),('D',p['b'])]:
   x,y=[(v['A'][i]+v[k][i])/2 for i in (0,1)]
   dx,dy=v[k][0]-v['A'][0],v[k][1]-v['A'][1];ll=math.hypot(dx,dy);nx,ny=dy/ll,-dx/ll
   if nx*(x-centroid[0])+ny*(y-centroid[1])<0:nx,ny=-nx,-ny
   if 'outer' not in p:ax.text(x+nx*.09*scale,y+ny*.09*scale,num(val)+' '+p['unit'],ha='left' if nx>.3 else 'right' if nx<-.3 else 'center',va='bottom' if ny>.3 else 'top' if ny<-.3 else 'center',fontsize=12)
  start=90+p.get('orientation',0);end=start+p['angle']
  if 'outer' not in p:ax.add_patch(Arc(v['A'],2*r,2*r,theta1=start,theta2=end,color='#d39500',lw=2))
  if 'outer' not in p:
   mid=math.radians((start+end)/2);candidate=[v['A'][0]+3*r*math.cos(mid),v['A'][1]+3*r*math.sin(mid)]
   if p['angle']<=60 or math.dist(candidate,v['C'])<.2*scale:
    dx,dy=v['A'][0]-centroid[0],v['A'][1]-centroid[1];length=math.hypot(dx,dy)
    pos=[v['A'][0]+.26*scale*dx/length,v['A'][1]+.26*scale*dy/length]
    ax.annotate(str(p['angle'])+'°',xy=[v['A'][0]+r*math.cos(mid),v['A'][1]+r*math.sin(mid)],xytext=pos,textcoords='data',ha='center',va='center',fontsize=11,arrowprops={'arrowstyle':'-','linestyle':':','color':'#666666','linewidth':.7})
    spec['angle_label_mode']='exterior_callout';spec['angle_label_position']=pos
   else:
    ax.text(*candidate,str(p['angle'])+'°',ha='center',va='center',fontsize=11)
    spec['angle_label_mode']='interior';spec['angle_label_position']=candidate
  xs,ys=zip(*pts);ax.set_xlim(min(xs)-.3*scale,max(xs)+.3*scale);ax.set_ylim(min(ys)-.25*scale,max(ys)+.25*scale)
  with tempfile.NamedTemporaryFile(dir=path.parent,suffix='.png',delete=False) as f:temp=Path(f.name)
  try:fig.savefig(temp,facecolor='white');os.replace(temp,path)
  finally:plt.close(fig);temp.unlink(missing_ok=True)
  with tempfile.NamedTemporaryFile(dir=path.parent,suffix='.json',mode='w',delete=False) as f:json.dump(spec,f,indent=2);tmp=Path(f.name)
  os.replace(tmp,side)
 return str(path.resolve()),spec

def validate_parameters(level,p,raw=False):
 if set(p)-{'a','b','angle','quadrilateral','unit','orientation','outer'}:raise ValueError('unknown parameters')
 if not isinstance(p['angle'],int):raise ValueError('included angle must be an integer number of degrees')
 if p['unit'] not in ('cm','mm','km','mi','in'):raise ValueError('unit')
 if p.get('orientation',0) not in (0,90,180,270):raise ValueError('orientation')
 if not raw:
  if max(p['a'],p['b'])/min(p['a'],p['b'])>2.5:raise ValueError('side ratio exceeds observed geometry bounds')
  if level=='easy':
   if not (8<=p.get('outer',0)<=120 and p['angle']==90 and p['a']==p['b'] and abs(float(calculation(p)[0])-p['outer'])<1e-9):raise ValueError('easy supplied outer area bounds')
  elif level=='moderate':
   if not(p['angle']==90 and all(isinstance(p[k],int) and 4<=p[k]<=20 and p[k]%2==0 for k in ('a','b'))):raise ValueError('moderate integer right-triangle bounds')
  elif not(30<=p['angle']<=140 and all(2<=p[k]<=32 and float(2*p[k]).is_integer() for k in ('a','b'))):raise ValueError('hard bounds')
 T,R,c=calculation(p)
 if p['a']<=0 or p['b']<=0 or not(0<p['angle']<180) or not isinstance(p['quadrilateral'],int) or not(0<p['quadrilateral']<float(T)) or c<=0:raise ValueError('invalid concave geometry/area')

def sample(level,rng):
 u=rng.choice(['cm','mm','km','mi','in']);o=rng.choice([0,90,180,270])
 if level=='easy':
  # Integral outer areas; internal dummy side geometry is not an assessed input.
  outer=rng.randint(8,120);a=b=math.sqrt(2*outer);t=90
 elif level=='moderate':a,b=rng.choice(range(4,21,2)),rng.choice(range(4,21,2));t=90
 else:a,b=rng.choice([v/2 for v in range(4,65)]),rng.choice([v/2 for v in range(4,65)]);t=rng.choice([v for v in range(30,141) if v!=90])
 p={'a':a,'b':b,'angle':t,'quadrilateral':1,'unit':u,'orientation':o};T,R,c=calculation(p)
 if R<5 or max(a,b)/min(a,b)>2.5:return sample(level,rng)
 p['quadrilateral']=rng.randint(max(1,math.ceil(float(T)*.45)),max(1,min(R-1,math.floor(float(T)*.85))))
 if level=='easy':p['outer']=outer
 return p

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('level')
 if profile and profile!='method':
  if profile not in BANK_PROFILES:raise ValueError('profile')
  implied=BANK_PROFILES[profile]['template']
  if template and template!=implied:raise ValueError('profile/template')
  template=implied
 template=template or ('easy_area' if level=='easy' else 'moderate_right' if level=='moderate' else random.Random(seed).choice(list(QS)))
 if template not in TEMPLATES or TEMPLATES[template]['level']!=level:raise ValueError('template/level')
 kind=field_type or TEMPLATES[template]['kind']
 if kind not in ('blank','radio'):raise ValueError('field type')
 raw=bool(profile and profile.startswith('raw_'));opaque=bool(profile and profile!='method');profile=profile or 'method'
 if opaque and kind!=TEMPLATES[template]['kind']:raise ValueError('source field type')
 if opaque and template=='q-285786' and parameters is not None and parameters['angle']!=90:raise ValueError('observed omitted decimal family requires right angle')
 rng=random.Random(seed);p=dict(parameters) if parameters is not None else dict(CFG[template]['parameters']) if opaque else None
 for attempt in range(256):
  pp={'orientation':0,**(p or sample(level,rng))}
  for component in ('a','b','angle'):
   if float(pp[component]).is_integer():pp[component]=int(pp[component])
  if not opaque and template=='q-285786' and p is None:
   pp['angle']=90
   if all(float(pp[k]).is_integer() for k in ('a','b')):pp['a']+=.5 if pp['a']<32 else -.5
   TT,RR,_=calculation(pp);pp['quadrilateral']=rng.randint(max(1,math.ceil(float(TT)*.45)),max(1,min(RR-1,math.floor(float(TT)*.85))))
  validate_parameters(level,pp,opaque)
  if not opaque and level=='hard' and ((template=='q-285786') != (pp['angle']==90) or pp['angle']==90 and all(float(pp[k]).is_integer() for k in ('a','b'))):raise ValueError('hard right-angle family requires fractional side; other hard families require nonright angle')
  T,R,c=calculation(pp);c=pp['outer']-pp['quadrilateral'] if level=='easy' else c;Q=pp['quadrilateral'];u=pp['unit']
  if opaque:
   source=QS[template];sf=source[':question/answer-fields'][0];anchor=calculation(CFG[template]['parameters'])[2]
   values=[fmt(c+int(re.match(r'\d+',a[':answer/value']).group())-anchor,u,a[':answer/value'].replace(CFG[template]['parameters']['unit'],u)) for a in sf[':answer-field/choices']]
  elif kind=='blank':values=[c]
  elif level=='easy':values=[c,pp['outer'],pp['outer']+Q,Q,rounding(sp.Rational(c,2))]
  elif level=='moderate' or pp['angle']==90:values=[c,R,R+Q,rounding(2*T)-Q,rounding(T-sp.Rational(Q,2))]
  else:values=[c,R,R+Q,rounding(2*T)-Q,rounding(sp.Rational(str(pp['a']))*sp.Rational(str(pp['b']))/2)-Q]
  if not opaque and (len(set(values))!=len(values) or min(values)<=0):
   if p is not None:raise ValueError('whole method bank collision/domain')
   continue
  if not opaque:values=[fmt(v,u) if kind=='radio' else str(v) for v in values]
  break
 else:raise ValueError('sampling exhausted')
 pp=dict(pp);q={};assets={}
 if opaque:
  src=QS[template];cp=CFG[template]['parameters'];problem=src[':question/problem'];problem=problem.replace('$'+str(cp['quadrilateral']), '$'+str(Q));problem=replace_unit(problem,cp['unit'],u)
  if pp==cp:plot=re.search(r'images/[^)]+',problem).group();assets={'prompt':str(Path('/media/jake/SSD/EDB/math')/plot)};plot_spec={'source_asset_reused':True}
  else:
   plot,plot_spec=render(pp);problem=re.sub(r'images/[^)]+',plot,problem);assets={'prompt':plot}
  solution=source_solution(template,pp,raw)
  if not raw and pp==cp and template in ('q-285754','q-285769','q-285786'):solution=source_solution(template,{**pp,'a':pp['b'],'b':pp['a']},False)
  if not raw and template=='q-18192':solution=normal_solution(pp)
  if ':question/difficulty' in src or not raw:q[':question/difficulty']=':question.difficulty/hard'
  if solution is not None:q[':question/worked-solution']=solution
 else:
  plot,plot_spec=render(pp);assets={'prompt':plot};problem=f'![]({plot})\n\nThe area of $ABCD$ is ${fmt(Q,u)}.$ '
  if level=='easy':problem+=f'The area of the enclosing $△ABD$ is ${fmt(pp["outer"],u)}.$ '
  if kind=='blank':problem+='Then, the area of $△BCD$, rounded to the **nearest integer**, is{{field-1}}$'+fmt('',u)+'.$'
  else:problem+='What is the area of $△BCD$ rounded to the nearest integer?'
  q[':question/difficulty']=':question.difficulty/'+level
  # Reuse source arithmetic sequences at changed parameters, fixing mislabeled sides via plots.
  if template in QS and template!='q-18192':q[':question/worked-solution']=source_solution(template,pp,False)
  else:q[':question/worked-solution']=normal_solution(pp,'easy' if level=='easy' else 'product')
 q[':question/problem']=problem
 fingerprint=digest({'method':'outer-minus-quadrilateral','level':level,'data':{'outer':pp['outer'],'Q':Q} if level=='easy' else {'sides':sorted([pp['a'],pp['b']]),'angle':pp['angle'],'quadrilateral':Q}})
 identity=digest({'version':VERSION,'difficulty':q.get(':question/difficulty'),'prompt':problem,'solution':q.get(':question/worked-solution'),'values':sorted(values),'correct_presence':not(raw and template=='q-18192')})
 qid=str(uuid.uuid5(NS,identity));key='field-1' if kind=='blank' else 'selection';fid=str(uuid.uuid5(uuid.UUID(qid),key));answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers}
 target=next(a for a in answers if int(re.match(r'\d+',a[':answer/value']).group())==c)
 if not(raw and template=='q-18192'):field[':answer-field/correct']=[':answer/id',target[':answer/id']]
 if kind=='radio':rng.shuffle(answers)
 q[':question/id']=qid;q[':question/answer-fields']=[field]
 return {'knowledge_point':{'db_id':KP,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':pp,'parameter_fingerprint':fingerprint,'content_fingerprint':identity,'eligible_for_learning':not opaque,'evidence_only':opaque,'authored_level':level!='hard','python_version':sys.version.split()[0],'sympy_version':sp.__version__,'source_analysis':{**{k:SRC[k] for k in ('database','basis','lineage')},'question_ids':[template] if template in QS else ['e-3297']},'plot_rating':'heavy','plot_assets':assets,'plot_spec':plot_spec,'exact_outer_area':str(T),'rounded_outer_area':R,'correct_area':c,'bank_recipes':('opaque observed scalar offsets, intention unresolved' if opaque else (['outer-minus-Q','omit subtraction','add Q','return given Q','halve difference'] if level=='easy' else ['outer-minus-Q','omit subtraction','add Q','omit half factor','omit sine' if level=='hard' and pp['angle']!=90 else 'halve Q before subtraction']))}}

# EASY: authored supplied enclosing area, one integer subtraction; no trig task.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: authored integer right-angle enclosing triangle, half-product and difference.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: source-labeled calculator sine area, round, then subtract; independent instances.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0];out=q[':question/problem']+'\n\n'
 out+='\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else '') for a in f[':answer-field/choices'])
 return out+'\n\n'+q.get(':question/worked-solution','*Source has no worked solution.*')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--template');ap.add_argument('--profile');ap.add_argument('--field-type',choices=['blank','radio']);ap.add_argument('--format',choices=['json','markdown'],default='markdown');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
