#!/usr/bin/env python3
"""Steps 3–7 local exact triangle-area inverse generator; no database actions.

Observed moderate: solve ½bc sin A for a side or acute included angle.
Raw whole-bank profiles are public evidence only; historical wrong numbers are
opaque, parameterized by geometric dilation rather than claimed error intent.
Normal defaults select all source-shaped eligible families before parameters.
Easy authored: side unknown, supplied sine value (one linear isolation).
Moderate: special angle evaluation then side isolation / acute inverse recognition.
Hard authored: same inverse formula with nonintegral side coefficients, no new
trig method. Rational workload bounds are enforced on explicit calls as well.
"""
from __future__ import annotations
import argparse,hashlib,json,math,os,random,re,sys,tempfile,threading,uuid
from pathlib import Path
import sympy as sp
os.environ.setdefault('MPLCONFIGDIR','/tmp/inverse-triangle-mpl')
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Wedge
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).with_suffix('')
KP_ID=17592186105904;VERSION='inverse-triangle-area-4'
CAP=json.loads((ROOT/'generate/runs/current/sources/17592186105904.json').read_text())
REC=CAP['record'];TITLE=REC[':knowledge-point/title'];KP_UUID=REC[':knowledge-point/id']
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
# Extracted side lengths, included angles and units from full-resolution rasters.
ANCHORS={
 'q-43310':('side','7','3',30,'cm'), 'q-43343':('angle','6','5',60,'cm'),
 'q-161107':('side','4','5',60,'cm'), 'q-161109':('side','7','6',45,'cm'),
 'q-280279':('side','5','10',120,'cm'), 'q-280282':('angle','4','sqrt(3)',60,'mm'),
 'q-365424':('angle','10','8',45,'cm'), 'q-43328':('angle','sqrt(6)','sqrt(2)',45,'cm'),
 'q-43339':('angle','12','5',30,'cm')}
TEMPLATES={sid:('moderate',a[0], 'blank' if sid in ('q-280279','q-280282','q-365424') else 'radio') for sid,a in ANCHORS.items()}
TEMPLATES.update({lev+'_'+kind: (lev,'side',kind) for lev in ('easy','hard') for kind in ('radio','blank')})
LOCK=threading.Lock()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),str(v)))
def exact(v):
 e=sp.sympify(str(v));
 if e.free_symbols or e.is_real is not True or e.is_positive is not True:raise ValueError('Positive exact lengths required')
 return e

def tex(v):return sp.latex(sp.factor(v)).replace(' ','')
def factor(v):return '('+tex(v)+')'
def sine(t):return sp.simplify(sp.sin(sp.pi*t/180))
def block(rows):return r'\begin{aligned}'+' \\\\ '.join(rows)+r'\end{aligned}'
def replace_blocks(text,blocks):
 it=iter(blocks)
 return re.sub(r'\$\$\n.*?\n\$\$',lambda _: '$$\n'+next(it)+'\n$$',text,flags=re.S)

def source_chain(sid,b,c,t):
 """Per-family ordered, unevaluated masks. s=1 exactly recovers all original rows."""
 area=sp.simplify(b*c*sine(t)/2);a=tex(area);bt,ct=tex(b),tex(c);st=tex(sine(t));k=tex(c*sine(t)/2);K=tex(b*c/2)
 sinA=r'\operatorname{sin}⁡A';sint=r'\operatorname{sin}⁡{'+str(t)+r'}^{∘}'
 formal=r'A & =\frac{1}{2}\cdot b\cdot c\cdot '+sinA
 if ANCHORS[sid][0]=='side':
  rows=[formal,a+r' & =\frac{1}{2}\cdot b\cdot '+ct+r'\cdot '+sint,a+r' & =\frac{1}{2}\cdot b\cdot '+ct+r'\cdot ('+st+')']
  if sid=='q-161107':
   rows += [a+r' & =\frac{'+tex(c*sp.sqrt(3))+r'\,b}{4}',(('' if sp.simplify(area/(c*sp.sqrt(3)))==1 else tex(area/(c*sp.sqrt(3))))+r'\cancel{'+tex(c*sp.sqrt(3))+r'} & =\frac{\cancel{'+tex(c*sp.sqrt(3))+r'}\,b}{4}'),tex(area/(c*sp.sqrt(3)))+r' & =\frac{b}{4}']
  elif sid=='q-161109':
   # Nonzero radical factor cancellation before individual integer isolation.
   u=area/sp.sqrt(2);v=c/4
   rows += [a+r' & =\frac{'+tex(c*sp.sqrt(2)/2)+r'\,b}{2}',r'\frac{'+tex(2*u)+r'\cancel{\sqrt{2}}}{\cancel{2}} & =\frac{'+tex(c/2)+r'\cancel{\sqrt{2}}\,b}{\cancel{2}}',tex(c/2)+r'b & ='+tex(2*u)]
  elif sid=='q-280279':
   rows += [a+' & ='+tex(c/2)+r'b\cdot '+st,tex(area/sine(t))+r'\cancel{'+st+'} & ='+tex(c/2)+r'b\cdot \cancel{'+st+'}',tex(c/2)+'b & ='+tex(area/sine(t))]
  else:rows += [a+' & ='+k+'b',r'b & =\frac{'+a+'}{'+k+'}']
  rows += ['b & ='+bt+r'\text{ cm}.']
 else:
  rows=[formal,a+r' & =\frac{1}{2}\cdot '+bt+r'\cdot '+ct+r'\cdot '+sinA]
  if sid=='q-43328':
   rows += [a+' & ='+tex(b/2)+r'\cdot '+ct+r'\cdot '+sinA,(('' if sp.simplify(area/(b/2))==1 else tex(area/(b/2)))+r'\cancel{'+tex(b/2)+r'} & =\cancel{'+tex(b/2)+r'}\cdot '+ct+r'\cdot '+sinA),tex(area/(b/2))+' & ='+ct+sinA,r'\frac{'+tex(area/(b/2))+'}{'+ct+'} & ='+sinA,sinA+' & ='+st]
  else:
   rows += [a+' & ='+K+r'\cdot '+sinA,r'\frac{'+a+'}{'+K+'} & ='+sinA]
   if sid=='q-280282':rows += [st+' & ='+sinA]
   rows += [sinA+' & ='+st]
  rows+=['m∠A & ={'+str(t)+'}^{∘}.']
 return block(rows)

def observed_solution(sid,b,c,t,unit):
 q=SOURCES[sid];orig=q.get(':question/worked-solution')
 if not orig:return None
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',orig,re.S)
 here=block(['c & =AB='+tex(c)+(r'\text{ cm}' if ANCHORS[sid][0]=='side' else r'\,\text{'+(' ' if sid in ('q-280282','q-43328','q-43339') else '')+unit+'}'), 'b & =AC'+('' if ANCHORS[sid][0]=='side' else '='+tex(b)+r'\,\text{'+unit+'}')]+(['m∠A & ={'+str(t)+'}^{∘}.'] if ANCHORS[sid][0]=='side' else []))
 # The three side originals have identical Here-block punctuation, all angle
 # originals have no ending full stop in their final component row.
 here=here.replace(r'} \\ b',r'}, \\ b').replace(r'=AC \\ m',r'=AC, \\ m')
 new=[blocks[0],here]
 if ANCHORS[sid][0]=='side':new += [r'\operatorname{sin}⁡{'+str(t)+'}^{∘}='+tex(sine(t))+',']
 new += [source_chain(sid,b,c,t)]
 out=replace_blocks(orig,new)
 if ANCHORS[sid][0]=='side':
  out=re.sub(r'We conclude that .*$',lambda _:'We conclude that $AC='+tex(b)+r'\,\text{'+(' ' if sid=='q-280279' else '')+'cm}.$',out)
 return out

def authored_solution(b,c,t,unit,easy=False):
 a=tex(b*c*sine(t)/2);st=tex(sine(t));ct=tex(c);bt=tex(b);sinA=r'\operatorname{sin}⁡A'
 rows=[r'A & =\frac{1}{2}\cdot b\cdot c\cdot '+sinA,a+r' & =\frac{1}{2}\cdot b\cdot '+ct+r'\cdot \operatorname{sin}⁡{'+str(t)+'}^{∘}',a+r' & =\frac{1}{2}\cdot b\cdot '+ct+r'\cdot ('+st+')',a+' & ='+tex(c*sine(t)/2)+'b',r'b & =\frac{'+a+'}{'+tex(c*sine(t)/2)+'}',r'b & ='+bt+r'\text{ '+unit+'}.']
 return 'The formula for the area of the triangle is \n\n$$\n'+r'A=\frac{1}{2}bc\operatorname{sin}⁡A,'+'\n$$\n\nwhere $∠A$ is between the sides of lengths $b$ and $c.$ \n\nHere\n\n$$\n'+block(['c & =AB='+ct+r'\text{ '+unit+'}', 'b & =AC', 'm∠A & ={'+str(t)+'}^{∘}.'])+'\n$$\n\nSince \n\n$$\n'+r'\operatorname{sin}⁡{'+str(t)+'}^{∘}='+st+',\n$$\n\nwe can calculate $b=AC,$ as follows:\n\n$$\n'+block(rows)+'\n$$\n\nWe conclude that $AC='+bt+r'\,\text{'+unit+'}.$'

def plot(b,c,t,unit,kind,output_dir=None):
 """Exact mathematical geometry, equal aspect; label placements outside edges."""
 data={'b':str(b),'c':str(c),'theta':t,'unit':unit,'kind':kind,'version':VERSION};h=digest(data);out=Path(output_dir or HERE/'plots');out.mkdir(parents=True,exist_ok=True);target=out/(h+'.png');side=target.with_suffix('.json')
 with LOCK:
  if target.exists() and side.exists():return str(target),json.loads(side.read_text())
  C=(float(b),0.);B=(float(c)*math.cos(math.radians(t)),float(c)*math.sin(math.radians(t)));A=(0.,0.);maxlen=max(float(b),float(c));radius=min(float(b),float(c))*.20
  fig=Figure(figsize=(4.7,3.5),dpi=150);ax=fig.subplots();ax.set_aspect('equal');ax.axis('off')
  ax.plot([0,B[0],C[0],0],[0,B[1],0,0],color='black',lw=1.7)
  ax.add_patch(Wedge(A,radius,0,t,color='#80b4df' if kind=='side' else '#449777'))
  for name,point,off in [('A',A,(-8,-14)),('B',B,(0,12)),('C',C,(12,-6))]:ax.annotate(name,point,xytext=off,textcoords='offset points',fontstyle='italic',fontsize=13,ha='center')
  ax.text(B[0]/2-.07*maxlen,B[1]/2+.025*maxlen,'$'+tex(c)+'$ '+unit,fontsize=12,ha='right')
  if kind=='angle':ax.annotate('$'+tex(b)+'$ '+unit,(C[0]/2,0),xytext=(0,-34),textcoords='offset points',fontsize=12,ha='center')
  if kind=='side':
   if t<35 or max(float(b),float(c))/min(float(b),float(c))>2.5:
    ax.annotate('$'+str(t)+r'^\circ$',(radius*math.cos(math.radians(t/2)),radius*math.sin(math.radians(t/2))),xytext=(.2*maxlen,-.12*maxlen),textcoords='data',fontsize=11,ha='center',arrowprops={'arrowstyle':'-','linestyle':':','color':'#666666','linewidth':.7})
   else:ax.annotate('$'+str(t)+r'^\circ$',(radius*1.4*math.cos(math.radians(t/2)),radius*1.4*math.sin(math.radians(t/2))),xytext=(0,6),textcoords='offset points',fontsize=11)
  ax.set_xlim(min(0,B[0])-.27*maxlen,max(C[0],B[0])+.2*maxlen);ax.set_ylim(-.18*maxlen,B[1]+.2*maxlen)
  FigureCanvasAgg(fig);fig.canvas.draw()
  pixel_vertices={name:list(map(float,ax.transData.transform(point))) for name,point in [('A',A),('B',B),('C',C)]}
  fd,tmp=tempfile.mkstemp(suffix='.png',dir=out);os.close(fd)
  try:fig.savefig(tmp,dpi=150,facecolor='white');os.replace(tmp,target)
  finally:
   if os.path.exists(tmp):os.unlink(tmp)
  meta={**data,'renderer':'Matplotlib','matplotlib':matplotlib.__version__,'python':sys.version.split()[0],'dpi':150,'vertices':{'A':A,'B':B,'C':C},'labels':{'AB':tex(c),'AC':tex(b) if kind=='angle' else None,'angle':t if kind=='side' else None},'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'equal_aspect':True,'pixel_vertices_bottom_origin':pixel_vertices,'image_pixels':[705,525]}
  # API replay must retain the same shape on a cold render and a cache hit.
  meta=json.loads(json.dumps(meta))
  fd,tmp=tempfile.mkstemp(suffix='.json',dir=out);os.close(fd);Path(tmp).write_text(json.dumps(meta,indent=2));os.replace(tmp,side)
 return str(target),meta

def validate_params(level,template,p,raw=False):
 if set(p)!= {'b','c','theta','unit'}:raise ValueError('Exact parameters are b,c,theta,unit')
 b,c=exact(p['b']),exact(p['c']);t=p['theta'];unit=p['unit']
 if not isinstance(t,int) or t not in (30,45,60,120,135,150) or unit not in ('cm','mm'):raise ValueError('Special angle and supported units required')
 kind=TEMPLATES[template][1]
 if kind=='angle' and (t not in (30,45,60) or template=='q-43328' and t!=45):raise ValueError('Acute inverse branch required')
 if raw:
  k,b0,c0,t0,u0=ANCHORS[template];s=sp.simplify(b/exact(b0))
  if sp.simplify(c/exact(c0))!=s or t!=t0 or unit!=u0 or s not in (sp.Rational(1,2),1,2,3):raise ValueError('Raw evidence allows exact uniform dilation ½,1,2,3 only')
 else:
  if level=='easy':
   if not all(v.is_Integer and 2<=v<=12 for v in (b,c)) or t!=30:raise ValueError('Easy: integral sides 2..12, supplied sin30')
  elif level=='moderate':
   if template in ANCHORS and t!=ANCHORS[template][3]:raise ValueError('Source-family familiar angle fixed')
   # Source shape governs radical versus integral number forms.
   radical=template in ('q-280282','q-43328')
   if radical:
    b0=exact(ANCHORS[template][1]);c0=exact(ANCHORS[template][2]);br=b/b0;cr=c/c0
    if br not in (sp.Rational(1,2),*range(1,9)) or cr not in (sp.Rational(1,2),*range(1,9)) or b>12 or c>12:raise ValueError('Moderate radicals: half/integer factors through8, lengths≤12')
   elif not all(v.is_Integer and 2<=v<=12 for v in (b,c)):raise ValueError('Moderate: integer sides 2..12')
  else:
   if t not in (45,60,120,135):raise ValueError('Hard familiar45/60/120/135° required')
   if not all(v.is_Rational and 1<=v<=12 and sp.denom(v) in (2,3,4) for v in (b,c)):raise ValueError('Hard: both nonintegral reduced sides, denominators 2,3,4; 1..12')
 return b,c,t,unit

def bank_values(kind,b,c,t,profile,template):
 if profile.startswith('raw_'):
  sid=template;k,b0,c0,t0,u0=ANCHORS[sid];scale=sp.simplify(b/exact(b0));values=[]
  for a in SOURCES[sid][':question/answer-fields'][0][':answer-field/choices']:
   text=a[':answer/value'];v=re.sub(r'\\(?:,|text\{[^}]*\})','',text).replace('cm','');v=re.sub(r'\^\{∘\}','',v);v=re.sub(r'^\{(\d+)\}$',r'\1',v)
   while r'\frac' in v:
    v=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',v)
   values.append(sp.sympify(v)*(scale if kind=='side' else 1))
  return values
 if profile=='blank':return [b if kind=='side' else sp.Integer(t)]
 if kind=='side':
  area=b*c*sine(t)/2
  # Complete method-derived bank: omit half; multiply by known side
  # rather than divide; solve for the supplied side; divide known side twice.
  return [b,b/2,2*area*c/sine(t),2*area/(b*sine(t)),2*area/(c**2*sine(t))]
 if profile=='acute-recognition':
  # Complete special-angle identification bank: acute sine(30/45/60) and
  # their 60/45-degree supplementary branches (120/135). Wrong options
  # correspond to familiar-angle lookup or supplementary-branch mistakes.
  return list(map(sp.Integer,[30,45,60,120,135]))
 raise ValueError('Unknown whole bank')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed);raw=bool(profile and profile.startswith('raw_'))
 if raw:
  sid=profile.removeprefix('raw_');template=template or sid
  if template!=sid:raise ValueError('Raw profile and source template must agree')
 candidates=[k for k,v in TEMPLATES.items() if v[0]==level and (not field_type or v[2]==field_type)]
 if template is None:template=rng.choice(candidates)
 if template not in candidates:raise ValueError('Template outside level/field scope')
 lev,kind,ft=TEMPLATES[template];profile=profile or ('blank' if ft=='blank' else 'side-operations' if kind=='side' else 'acute-recognition')
 if ft=='blank' and not raw and profile!='blank':raise ValueError('Blank profile required')
 if ft=='radio' and not raw and profile!=('side-operations' if kind=='side' else 'acute-recognition'):raise ValueError('Ineligible whole bank')
 # Bank/family selected above, parameters sampled below. Reject whole bank.
 for attempt in range(500):
  if parameters is not None:p=dict(parameters)
  elif raw:
   _,b,c,t,u=ANCHORS[template];p={'b':b,'c':c,'theta':t,'unit':u}
  elif level=='easy':p={'b':str(rng.randint(2,12)),'c':str(rng.randint(2,12)),'theta':30,'unit':rng.choice(['cm','mm'])}
  elif level=='hard':
   domain=[sp.Rational(n,d) for d in (2,3,4) for n in range(d+1,12*d) if math.gcd(n,d)==1];p={'b':str(rng.choice(domain)),'c':str(rng.choice(domain)),'theta':rng.choice([45,60,120,135]),'unit':rng.choice(['cm','mm'])}
  elif template in ('q-280282','q-43328'):
   _,b,c,t,u=ANCHORS[template];db=[s for s in (sp.Rational(1,2),*range(1,9)) if exact(b)*s<=12];dc=[s for s in (sp.Rational(1,2),*range(1,9)) if exact(c)*s<=12];p={'b':str(exact(b)*rng.choice(db)),'c':str(exact(c)*rng.choice(dc)),'theta':t,'unit':u}
  else:
   t=ANCHORS[template][3];p={'b':str(rng.randint(2,12)),'c':str(rng.randint(2,12)),'theta':t,'unit':'cm'}
  b,c,t,u=validate_params(level,template,p,raw);vals=bank_values(kind,b,c,t,profile,template);correct=b if kind=='side' else sp.Integer(t)
  if len(set(map(sp.simplify,vals)))==len(vals) and all(v>0 for v in vals) and sum(sp.simplify(v-correct)==0 for v in vals)==1:break
  if raw:raise ValueError('Raw bank ambiguity')
  if parameters is not None:raise ValueError('Whole bank collision')
 else:raise ValueError('No eligible instance')
 area=sp.simplify(b*c*sine(t)/2);plotmeta=None
 if raw and b==exact(ANCHORS[template][1]) and c==exact(ANCHORS[template][2]):
  asset=re.search(r'!\[\]\(([^)]+)\)',SOURCES[template][':question/problem'])[1]
 else:asset,plotmeta=plot(b,c,t,u,kind)
 if template in SOURCES:
  source=SOURCES[template];a0=sp.simplify(exact(ANCHORS[template][1])*exact(ANCHORS[template][2])*sine(ANCHORS[template][3])/2)
  problem=re.sub(r'!\[\]\([^)]*\)',lambda _:'![]('+asset+')',source[':question/problem'])
  # Complete area component: never substitute a short numeral across prose.
  pattern=r'(is \$)(.*?)(?=(?:cm|\{|\\,|\\text))'
  # Find area math delimiters, preserving source unit spelling and punctuation.
  start=problem.index('is $')+4;end=problem.index('$',start);area_fragment=problem[start:end]
  old=tex(a0);new=tex(area)
  assert area_fragment.startswith(old),(template,area_fragment,old)
  problem=problem[:start]+new+area_fragment[len(old):]+problem[end:]
  solution=observed_solution(template,b,c,t,u)
  if not raw:
   if kind=='angle':
    problem=problem.replace('the acute triangle $△ABC$', 'the triangle $△ABC$ with acute $∠A$')
    if 'with acute' not in problem:problem=problem.replace('the triangle $△ABC$', 'the triangle $△ABC$ with acute $∠A$')
   if not solution:solution=authored_solution(b,c,t,u) if kind=='side' else observed_solution('q-43339',b,c,t,u)
 else:
  problem='![]('+asset+')\n\nThe area of the triangle $△ABC$ is $'+tex(area)+r'\,\text{'+u+r'}^{2}.$ '
  if level=='easy':problem += r'Use $\sin30^{\circ}=\frac{1}{2}.$ '
  problem+= 'Find $AC.$' if ft=='radio' else 'Then, $AC=${{field-1}} $'+r'\text{'+u+'}.$'
  solution=authored_solution(b,c,t,u,level=='easy')
 # Unit changes in source-shaped normal variants are currently fixed to source
 # units by sampler; public explicit changes must render every occurrence.
 if template in SOURCES and not raw and u!=ANCHORS[template][4]:
  problem=problem.replace(ANCHORS[template][4],u);solution=solution.replace(ANCHORS[template][4],u)
 shown=[]
 if raw:
  scale=b/exact(ANCHORS[template][1])
  for a,v in zip(SOURCES[template][':question/answer-fields'][0][':answer-field/choices'],vals):
   text=a[':answer/value']
   if kind=='side' and scale!=1:
    # Preserve original unit wrapper while scaling the whole numeric fragment.
    match=re.match(r'(.*?)(cm|\\,\\text\{cm\})$',text);text=tex(v)+(match[2] if match else '')
   shown.append(text)
 else:shown=[tex(v)+(r'\,\text{'+u+'}' if kind=='side' and ft=='radio' else r'^{\circ}' if kind=='angle' and ft=='radio' else '') for v in vals]
 key='field-1' if ft=='blank' else 'selection';rawq=SOURCES.get(template,{})
 payload={'version':VERSION,'level':level,'problem':problem,'solution':solution,'bank':sorted(shown),'field':ft,'correct':str(correct) if not raw or ':answer-field/correct' in rawq[':question/answer-fields'][0] else None}
 h=digest(payload);qid=ident(h);fid=ident(h+key)
 answers=[{':answer/id':ident(fid+text),':answer/type':':answer.type/math',':answer/value':text} for text in shown]
 f={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+ft,':answer-field/choices':answers}
 if not raw or ':answer-field/correct' in rawq[':question/answer-fields'][0]:f[':answer-field/correct']=[':answer/id',answers[next(i for i,v in enumerate(vals) if sp.simplify(v-correct)==0)][':answer/id']]
 if ft=='radio':rng.shuffle(answers)
 q={':question/id':qid,':question/problem':problem,':question/answer-fields':[f]}
 if not raw or ':question/difficulty' in rawq:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'parameters':p,'source_id':template if template in SOURCES else None,'source':{k:CAP[k] for k in ('database','basis','lineage')},'evidence_only':raw,'eligible_for_learning':not raw,'source_prose_anomaly':'whole-triangle-acute-claim-false' if template=='q-280282' else None,'presentation_repair':'specify-acute-included-angle-only' if not raw and kind=='angle' else None,'bank_origin':'opaque-observed' if raw and ft=='radio' else 'observed-blank' if raw else 'authored-method-bank' if ft=='radio' else 'observed-shaped-blank','parameter_fingerprint':digest({'kind':kind,'b':str(b),'c':str(c),'theta':t,'supplied_sine':level=='easy'}),'content_fingerprint':h,'plot':plotmeta,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__,'matplotlib':matplotlib.__version__}}}

# Easy authored: provided sine removes trig evaluation; no progression within level.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate observed: integer/radical inverse area calculation at familiar angles.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard authored: same side isolation, both reduced nonintegral coefficient lengths.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];text=q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  for a in f[':answer-field/choices']:text+='- $'+a[':answer/value']+'$\n'
 return text+'\n'+q.get(':question/worked-solution','[Original worked solution absent]')+'\n'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template');p.add_argument('--profile');args=p.parse_args()
 out=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(out,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(markdown(r) for r in out))
