"""Draft: QI-only reciprocal ratios. Registered numeric baseline is immutable.

Raw observed banks are parameterized evidence profiles, never default learning
banks: several scalar patterns have opaque intent. Easy: rational complement;
moderate: non-square complement with given coefficient one; hard: nonunit
radical given coefficient with a non-square complement. All use
unit-circle identification, identity, positive root, reciprocal, and (as needed)
rationalization. Explicit inputs use the same reduced-object guards as sampling.
"""
import argparse,functools,hashlib,json,math,os,random,re,subprocess,sys,uuid,threading
from pathlib import Path
import sympy as sp
D=Path(__file__).with_suffix('');ROOT=D.parents[2];K=17592186110756
SOURCE=json.loads((D/'source.json').read_text());REC=SOURCE['record'];VERSION='reciprocal-qi-draft-2';RENDERER_REVISION='theta-centered-adaptive-2'
SOURCES={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
CONFIG={'q-124750':('y',5,1),'q-65066':('y',5,9),'q-124743':('x',3,1),'q-65062':('y',3,3),'q-65064':('x',5,15),'q-85234':('y',3,2)}
os.environ.setdefault('MPLCONFIGDIR','/tmp/reciprocal-qi-draft-mpl')
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_prose,normalize_tex,validate_generated_record

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(REC[':knowledge-point/id']),v))
def tex(v):return sp.latex(sp.simplify(v)).replace(' ','')
def frac(a,b):return rf'\frac{{{a}}}{{{b}}}'
def parts(p):return _parts(p['b'],p['r'])
@functools.lru_cache(None)
def _parts(bval,rval):
 b,r=map(sp.Integer,(bval,rval));d=b*b-r
 if not (2<=b<=15 and 0<r<b*b):raise ValueError('Requires 2<=b<=15 and 0<r<b²')
 c,s=sp.sqrt(d).as_coeff_Mul();s=sp.simplify(s*s)
 a,n=sp.sqrt(r).as_coeff_Mul();n=sp.simplify(n*n)
 return b,r,d,c,s,a,n,sp.sqrt(r)/b,sp.sqrt(d)/b,sp.simplify(b/sp.sqrt(d))
def slots(p):
 b,r,d,c,s,a,n,known,missing,correct=parts(p)
 return {'known':tex(known),'squared':frac(r,b*b),'complement':frac(d,b*b),'missing':tex(missing),'unrational':frac(b,tex(sp.sqrt(d))),'multiplier':frac(tex(sp.sqrt(s)),tex(sp.sqrt(s))),'intermediate':frac(str(b)+tex(sp.sqrt(s)),str(c)+r'\cdot '+str(s)) if c!=1 else frac(str(b)+tex(sp.sqrt(s)),s),'correct':tex(correct)}
@functools.lru_cache(None)
def masks(name,key):
 """Slot full mathematical components before any substitutions; never short tokens."""
 q=SOURCES[name];text=q[key];old=slots({'b':CONFIG[name][1],'r':CONFIG[name][2]})
 # The source contains this structural unsimplified rationalization row.
 replacements={value:'@@'+role+'@@' for role,value in old.items()}
 # Where stages coincide numerically, missing coordinate takes precedence.
 replacements[old['missing']]='@@missing@@';replacements[old['known']]='@@known@@'
 if old['intermediate']==old['correct']:replacements[old['intermediate']]='@@intermediate@@'
 pattern=re.compile('|'.join(re.escape(x) for x in sorted(replacements,key=len,reverse=True)))
 return pattern.sub(lambda m:replacements[m[0]],text)
def prose(name,key,p):
 text=masks(name,key);v=slots(p)
 for role,val in v.items():text=text.replace('@@'+role+'@@',val)
 return text

def source_bank(name,p):
 """Exact observed expression-pattern profiles; opaque compound patterns explicit."""
 b,r,d,c,s,a,n,k,m,z=parts(p)
 if name=='q-124750':vs=[(b+4)*sp.sqrt(s)/c,b*sp.sqrt(s)/(b+4),sp.sqrt(s)/c,z,(b+2)*sp.sqrt(s)/(c*s)]
 elif name=='q-124743':vs=[z,c*sp.sqrt(2*b)/b,(b+2)*sp.sqrt(s)/c,b*sp.sqrt(b)/c,b/c]
 elif name=='q-65062':return ['-'+frac(tex(sp.sqrt(r)),tex(sp.sqrt(d))),tex(-z),tex(z/b),frac(tex(sp.sqrt(r)),tex(sp.sqrt(d))),tex(z)]
 elif name=='q-65064':vs=[z,b*sp.sqrt(b)/(c*s),2*b*sp.sqrt(b)/(c*s),m,b]
 elif name=='q-85234':vs=[d/r,sp.sqrt(d)/r,(b+2)/sp.sqrt(d),z,d/b]
 else:vs=[d/b,b/d,d/(b*b),m,z]
 return [tex(v) for v in vs]
def method_bank(p,profile):return list(_method_bank(p['b'],p['r'],profile))
@functools.lru_cache(None)
def _method_bank(bval,rval,profile):
 b,r,d,c,s,a,n,k,m,z=parts({'b':bval,'r':rval})
 if profile=='method-reciprocal':vs=[z,m,1/k,1/(1-k*k),k/m]
 elif profile=='method-sign':vs=[z,-z,m,1/k,1/(1-k*k)]
 else:raise ValueError('Unknown normal bank')
 if any(sp.simplify(v-w)==0 for i,v in enumerate(vs) for w in vs[i+1:]):raise ValueError('Ambiguous complete bank')
 return [tex(v) for v in vs]

def guard(level,p):
 b,r,d,c,s,a,n,k,m,z=parts(p)
 # Canonicalize common coordinate scaling; bounds apply to the reduced object.
 if math.gcd(int(a),int(b))!=1:raise ValueError('Coordinate must be primitive')
 if level=='easy':ok=s==1 and n<=15
 elif level=='moderate':ok=s!=1 and a==1 and n<=15
 elif level=='hard':ok=s!=1 and a>1 and n>1 and n<=15 and a<=4
 else:raise ValueError('Unknown level')
 if not ok:raise ValueError('Explicit parameter violates level workload')
 if not (.14<=float(k)<=.97):raise ValueError('Point must remain readable')
 return p
@functools.lru_cache(None)
def domain(level,profile):
 out=[]
 for b in range(2,16):
  for r in range(1,b*b):
   p={'b':b,'r':r}
   try:guard(level,p);method_bank(p,profile)
   except ValueError:continue
   out.append(p)
 return out

_RENDER_LOCK=threading.RLock()
def render_plots(axis,p,role):
 # Matplotlib mathtext has process-global mutable parser state.
 with _RENDER_LOCK:return _render_plots(axis,p,role)
def _render_plots(axis,p,role):
 """Source grid [-2,2] with labels ±1 only; exact QI P/radius/wedge."""
 import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
 import numpy as np
 from matplotlib.patches import Wedge
 b,r,d,c,s,a,n,k,m,z=parts(p);x,y=(m,k) if axis=='y' else (k,m)
 spec={'axis':axis,'p':p,'point':[str(x),str(y)],'role':role,'version':VERSION,'renderer_revision':RENDERER_REVISION};key=digest(spec)
 folder=D/'plots';folder.mkdir(exist_ok=True);path=folder/(key+'.png');side=path.with_suffix('.json')
 if not (path.exists() and side.exists()):
  fig,ax=plt.subplots(figsize=(4.5,4.5),dpi=130);t=np.linspace(0,2*np.pi,600)
  ax.plot(np.cos(t),np.sin(t),color='#367fc0',lw=1.6);ax.set(xlim=(-2,2.25),ylim=(-2,2.15),aspect='equal');ax.axis('off')
  for v in [-2,-1,1,2]:ax.plot([-2,2],[v,v],color='#eeeeee',lw=.6);ax.plot([v,v],[-2,2],color='#eeeeee',lw=.6)
  ax.annotate('',(2,0),(-2,0),arrowprops={'arrowstyle':'->','lw':1});ax.annotate('',(0,2),(0,-2),arrowprops={'arrowstyle':'->','lw':1})
  for v in [-1,1]:ax.text(v-.06,-.17,str(v),fontsize=9);ax.text(-.18,v-.03,str(v),fontsize=9)
  ax.text(2.05,-.10,'$x$');ax.text(.07,2.01,'$y$');angle=math.degrees(math.atan2(float(y),float(x)))
  ax.plot([0,float(x)],[0,float(y)],color='black',lw=1.4);ax.scatter([float(x)],[float(y)],s=10,c='black')
  ax.add_patch(Wedge((0,0),.38,0,angle,color='#e8a900'))
  # Shallow wedges have insufficient room for a glyph between axis and ray.
  # Place the centered theta just above the ray; leave assessed geometry intact.
  theta=math.radians(angle+13 if angle<25 else angle/2)
  label_position=[.50*math.cos(theta),.50*math.sin(theta)]
  ax.text(*label_position,r'$\theta$',fontsize=10,ha='center',va='center',bbox={'facecolor':'white','edgecolor':'none','pad':.12})
  spec['theta_label']={'position':label_position,'centered':True,'shallow_adaptive':angle<25,'white_backing':True}
  label=r'$P$' if role=='prompt' else r'$P(\cos\theta,\sin\theta)$'
  ax.annotate(label,(float(x),float(y)),xytext=(6,8),textcoords='offset points',fontsize=10)
  fig.tight_layout(pad=.3)
  import tempfile
  with tempfile.NamedTemporaryFile(dir=folder,suffix='.png',delete=False) as f:temp=Path(f.name)
  fig.savefig(temp,metadata={'Software':VERSION+'/'+RENDERER_REVISION});plt.close(fig);os.replace(temp,path)
  spec['renderer']='matplotlib';spec['matplotlib']=matplotlib.__version__;spec['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
  with tempfile.NamedTemporaryFile(dir=folder,suffix='.json',mode='w',delete=False) as f:json.dump(spec,f);temp=Path(f.name)
  os.replace(temp,side)
 return {'path':str(path),**json.loads(side.read_text())}

def authored_solution(axis,p):
 # Shared source prose and ordered formal/substitution/root/reciprocal stages.
 base='q-124750' if axis=='y' else 'q-124743';sol=prose(base,':question/worked-solution',p)
 b,r,d,c,s,a,n,k,m,z=parts(p)
 if s==1:
  sol=sol.split('\n\nFinally, we rationalize')[0]
 return sol

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,plots=True):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only captured radio fields')
 rng=random.Random(seed);name=template or rng.choice(list(CONFIG));name=name.removeprefix('observed-')
 if name not in CONFIG:raise ValueError('Unknown template')
 raw=profile in ('raw','observed', 'observed-'+name);bankprofile='raw' if raw else (profile or rng.choice(['method-reciprocal','method-sign']))
 if not raw and bankprofile not in ('method-reciprocal','method-sign'):raise ValueError('Unknown normal bank profile')
 axis,b0,r0=CONFIG[name]
 if parameters is not None:
  if set(parameters)!= {'b','r'} or any(isinstance(v,bool) or not isinstance(v,int) for v in parameters.values()):raise ValueError('Expected integer b,r only')
  p=dict(parameters)
 else:p={'b':b0,'r':r0} if raw else dict(rng.choice(domain(level,bankprofile)))
 b,r,d,c,s,a,n,k,m,z=parts(p)
 if raw:
  if name=='q-65066' and (n!=1 or s!=1):raise ValueError('Raw rational-complement family')
  if name!='q-65066' and s==1:raise ValueError('Raw rationalization requires radical complement')
  if name in ('q-124750','q-124743') and r!=1:raise ValueError('Observed unit-numerator rational pattern')
  if name in ('q-65062','q-65064','q-85234') and n==1:raise ValueError('Observed radical-input pattern')
 if not raw:guard(level,p)
 bank=source_bank(name,p) if raw else method_bank(p,bankprofile)
 if raw:
  numeric=[parse_scalar(v) for v in bank]
  if any(sp.simplify(v-w)==0 for i,v in enumerate(numeric) for w in numeric[i+1:]):raise ValueError('Ambiguous complete bank')
 qsource=SOURCES[name];assets={}
 prompt=prose(name,':question/problem',p)
 sol=prose(name,':question/worked-solution',p) if ':question/worked-solution' in qsource else None
 if raw and sp.simplify(parts(p)[7]-parts({'b':b0,'r':r0})[7])!=0:
  if plots:
   for role in ('prompt','solution'):assets[role]=render_plots(axis,p,role)
   prompt=re.sub(r'!\[.*?\]\(.*?\)',lambda m:'![]('+assets['prompt']['path']+')',prompt)
   if sol:sol=re.sub(r'!\[.*?\]\(.*?\)',lambda m:'![]('+assets['solution']['path']+')',sol)
  else:
   prompt=re.sub(r'!\[.*?\]\(.*?\)\n\n','',prompt)
   if sol:sol=re.sub(r'!\[.*?\]\(.*?\)\n\n','',sol)
 if not raw:
  sol=sol or authored_solution(axis,p)
  # Normal prose replaces radical rationalization only for rational complement.
  if parts(p)[4]==1:sol=authored_solution(axis,p)
  if plots:
   for role in ('prompt','solution'):assets[role]=render_plots(axis,p,role)
   prompt=re.sub(r'!\[.*?\]\(.*?\)',lambda m:'![]('+assets['prompt']['path']+')',prompt)
   sol=re.sub(r'!\[.*?\]\(.*?\)',lambda m:'![]('+assets['solution']['path']+')',sol)
  else:prompt=re.sub(r'!\[.*?\]\(.*?\)\n\n','',prompt);sol=re.sub(r'!\[.*?\]\(.*?\)\n\n','',sol)
  prompt=normalize_prose(prompt);sol=normalize_prose(sol);bank=[normalize_tex(v) for v in bank]
 # Content identity excludes seed/option order/profile aliases and includes level.
 content={':question/problem':prompt,':question/worked-solution':sol,'bank':sorted(bank),'level':None if raw and ':question/difficulty' not in qsource else (qsource.get(':question/difficulty',{}).get(':db/ident') if raw else level),'version':VERSION}
 qid=uid('q:'+digest(content));fid=uid('field:'+qid+':selection');choices=[{':answer/id':uid('answer:'+fid+':'+v),':answer/type':':answer.type/math',':answer/value':v} for v in bank]
 # Mathematical key derived first. Missing captured designation remains absent.
 key=tex(parts(p)[-1]);correctindex=next(i for i,v in enumerate(bank) if tex(parse_scalar(v))==key) if raw else 0
 f={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices}
 if not raw or ':answer-field/correct' in qsource[':question/answer-fields'][0]:f[':answer-field/correct']=[':answer/id',choices[correctindex][':answer/id']]
 rng.shuffle(choices)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[f]}
 if sol is not None:q[':question/worked-solution']=sol
 if not raw:q[':question/difficulty']=':question.difficulty/'+level
 elif ':question/difficulty' in qsource:q[':question/difficulty']=qsource[':question/difficulty'][':db/ident']
 out={'knowledge_point':{'db_id':K,'id':REC[':knowledge-point/id'],'title':REC[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'seed':seed,'template':name,'bank_profile':bankprofile,'parameters':p,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'source_question':qsource[':db/id'],'authorship':'raw observed expression-pattern evidence' if raw else 'authored method-bank and level policy','evidence_only':raw,'diagnostic_only':not raw and not plots,'missing_assets_reason':'plots=False omits the diagram that establishes the first-quadrant branch' if not raw and not plots else None,'eligible_for_learning':not raw and plots,'render_mode':'full plot presentation' if plots else 'math-only diagnostic','assets':assets,'mathematical_fingerprint':digest({'axis':axis,'known':str(parts(p)[7]),'target':'sec' if axis=='y' else 'csc','quadrant':1}),'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'repository_sha':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()}}
 if not raw:validate_generated_record(out)
 return out

def parse_scalar(text):
 """Restricted exact scalar TeX parser; validator supplies independent checks."""
 from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
 text=text.replace('\\dfrac','\\frac').replace('\\left','').replace('\\right','').replace('\\cdot','*').replace('\\,','')
 def group(i):
  if text[i]!='{':raise ValueError('Expected TeX group')
  depth=1;j=i+1
  while depth:depth+=(text[j]=='{')-(text[j]=='}');j+=1
  return text[i+1:j-1],j
 out='';i=0
 while i<len(text):
  if text.startswith('\\frac',i):a,j=group(i+5);b,i=group(j);out+='('+str(parse_scalar(a))+')/('+str(parse_scalar(b))+')'
  elif text.startswith('\\sqrt',i):a,i=group(i+5);out+='sqrt('+str(parse_scalar(a))+')'
  else:out+=text[i];i+=1
 if not re.fullmatch(r'[0-9\s()+*/.\-sqrt]+',out):raise ValueError('Non-scalar '+out)
 return sp.simplify(parse_expr(out,transformations=standard_transformations+(implicit_multiplication_application,)))

# Easy: rational missing coordinate; reciprocal without rationalization.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# Moderate: coefficient-one input; irrational missing coordinate/rationalization.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# Hard (authored): the given radical has a nonunit coefficient.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0];key=f.get(':answer-field/correct',[None,None])[1]
 return q[':question/problem']+'\n\n'+'\n'.join('$'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==key else '') for a in f[':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','[No captured worked solution]')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['json','markdown'],default='json');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args();levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty];out=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)];print(json.dumps(out,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,out)))
if __name__=='__main__':main()
