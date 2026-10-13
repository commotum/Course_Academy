"""Origin-centered ellipse parametrization; captured basis 1356, generation only.

Easy: infer positive integer horizontal/vertical radii from labeled intercepts.
Moderate: given integer radii, additionally satisfy full-period/start/direction.
Hard (authored): infer half-unit radii from unlabeled intercepts against a half-unit
axis lattice, then satisfy the same period/start/direction. Never translates an
ellipse, eliminates its parameter, or restricts its traversal to a subarc.

Observed profiles are public raw evidence, including missing attributes and a
legacy duplicate field. Normal profiles use supported authoritative fields and
source-shaped complete banks. Opaque q-106701 is raw evidence only.
"""
from pathlib import Path
import argparse,copy,hashlib,json,os,random,re,subprocess,sys,tempfile,uuid
import sympy as sp
KP=17592186152187;HERE=Path(__file__).resolve().with_suffix('');VERSION='origin-ellipse-v7'
SOURCE=json.loads((HERE/'source.json').read_text());RECIPES=json.loads((HERE/'recipes.json').read_text());a,b=sp.symbols('a b',positive=True);theta=sp.symbols('theta',real=True)
LEVELS=('easy','moderate','hard');NS=uuid.UUID('179b5937-4b80-4c64-88b3-82e83583da95')
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def ident(v):return str(uuid.uuid5(NS,json.dumps(v,sort_keys=True,ensure_ascii=False)))
def tex(v):return sp.latex(sp.sympify(v))
def fill(mask,**slots):
 for k,v in slots.items():mask=mask.replace('{{'+k+'}}',str(v))
 return mask

def render_plots(instance,output_dir=None):
 """Use exact instance data, unique inputs, atomic PNG/sidecar; cache both files."""
 output_dir=Path(output_dir or HERE/'plots');output_dir.mkdir(exist_ok=True)
 data={k:instance[k] for k in ('a','b','marked','hard','point')};data['point']=data['point'] if data['marked'] else 'A';key=digest([VERSION,'ellipse-v7',data]);out=output_dir/(key+'.png');side=out.with_suffix('.json')
 if not(out.exists() and side.exists()):
  fd,tmp=tempfile.mkstemp(prefix='render-input-',suffix='.json',dir=output_dir);os.close(fd)
  try:
   Path(tmp).write_text(json.dumps(dict(data,output=str(out.resolve()))));subprocess.run([sys.executable,str(HERE/'render.py'),tmp],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  finally:Path(tmp).unlink(missing_ok=True)
 return {'prompt':str(out.resolve()),'sidecar':str(side.resolve()),'renderer':'Matplotlib','spec':json.loads(side.read_text())}

def bounds(level,p,raw=False):
 if set(p)-{'a','b','point'}:raise ValueError('Unknown parameter')
 A=sp.Rational(str(p['a']));B=sp.Rational(str(p['b']))
 if A<=0 or B<=0 or A==B:raise ValueError('Positive unequal semiaxes required')
 if p.get('point','A') not in ('A','J'):raise ValueError('Point label outside source scope')
 if raw:
  if A.q!=1 or B.q!=1 or not(2<=A<=9 and 2<=B<=9):raise ValueError('Observed workload: unequal integers 2..9')
 elif level in ('easy','moderate'):
  if A.q!=1 or B.q!=1 or not(2<=A<=9 and 2<=B<=9):raise ValueError('Easy/moderate semiaxes must be unequal integers 2..9')
 else:
  if not(2<=A<=9 and 2<=B<=9) or A.q not in (1,2) or B.q not in (1,2) or (A.q==1 and B.q==1):raise ValueError('Authored hard requires at least one half-integer axis, both 2..9')
 return {'a':str(A),'b':str(B),'point':p.get('point','A')}

def evaluate(recipe,p):return sp.sympify(recipe,locals={'a':a,'b':b,'sqrt':sp.sqrt}).subs({a:sp.Rational(p['a']),b:sp.Rational(p['b'])})
def components(value):
 """Independent reading of actual displayed pair/functions; retains component order."""
 value=value.replace(r'\operatorname{cos}','cos').replace(r'\operatorname{sin}','sin').replace(r'\cos','cos').replace(r'\sin','sin').replace('⁡','').replace(r'\,','').replace(r'\theta','theta').replace('θ','theta')
 pairs=re.findall(r'([xy])\s*=\s*(.*?)(cos|sin)\s*theta',value)
 if len(pairs)!=2 or [z[0] for z in pairs]!=['x','y']:raise ValueError('Malformed ordered pair '+value)
 out=[]
 for _,coef,fn in pairs:
  coef=coef.strip();coef=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',coef);coef=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',coef)
  coef=re.sub(r'(?<=\d)\s*(?=sqrt\()', '*',coef)
  c=sp.sympify(coef or '1',locals={'sqrt':sp.sqrt});out.append(c*(sp.cos(theta) if fn=='cos' else sp.sin(theta)))
 return tuple(out)
def trig_signature(pair):
 return tuple(c for z in pair for c in (sp.expand(z).coeff(sp.cos(theta)),sp.expand(z).coeff(sp.sin(theta))))
def eligible(pair,p,traversal):
 # Read coefficient vectors from the actual displayed component functions.
 # cos(theta),sin(theta) are linearly independent on the stated full period.
 A=sp.Rational(p['a']);B=sp.Rational(p['b']);cx,sx,cy,sy=trig_signature(pair)
 cosine=sp.simplify(cx**2/A**2+cy**2/B**2);sine=sp.simplify(sx**2/A**2+sy**2/B**2);mixed=sp.simplify(cx*sx/A**2+cy*sy/B**2);cross=sp.simplify(cx*sy-sx*cy)
 locus=cosine==1 and sine==1 and mixed==0 and cross!=0
 if traversal:return bool(locus and cx==A and cy==0 and cross>0)
 return bool(locus)

def make_fields(field_specs,p,raw=False):
 fields=[]
 for f in field_specs:
  values=[fill(v['mask'],X=tex(evaluate(v['x'],p)),Y=tex(evaluate(v['y'],p)) if v['y'] is not None else '') for v in f['values']]
  ci=f['correct_index'];field={':answer-field/key':f['key'],':answer-field/type':f['type'],':answer-field/choices':[{':answer/type':':answer.type/math',':answer/value':v} for v in values]}
  if ci is not None:field['_correct_index']=ci
  elif not raw:
   if f['type'].endswith('/radio'):field['_correct_index']=next(i for i,v in enumerate(values) if eligible(components(v),p,False))
   else:field['_correct_index']=0
  fields.append(field)
 return fields

def common_solution(p,traversal=True):
 ref=RECIPES['q-106393' if traversal else 'q-106392']['solution_mask'];return fill(ref,A=tex(p['a']),B=tex(p['b']))
def method_bank(p):
 # Complete bank chosen before parameters: correct, swapped axes, reversed trig,
 # squared axes, clockwise direction. Each member follows the displayed method.
 defs=[('a','cos','b','sin'),('b','cos','a','sin'),('a','sin','b','cos'),('a**2','cos','b**2','sin'),('a','cos','-b','sin')]
 return [{'key':'selection','type':':answer-field.type/radio','correct_index':0,'values':[{'mask':r'x={{X}}\operatorname{'+fx+r'}⁡\theta ,\,y={{Y}}\operatorname{'+fy+r'}⁡\theta ','x':x,'y':y} for x,fx,y,fy in defs]}]

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in LEVELS:raise ValueError('Unknown difficulty')
 rng=random.Random(seed);raw=bool(profile and profile.startswith('observed:'));name=profile.removeprefix('observed:') if profile else None
 if raw:
  if name not in RECIPES:raise ValueError('Unknown observed profile')
  r=RECIPES[name];actual=r['difficulty'];expected=actual.rsplit('/',1)[-1] if actual else 'easy'
  if level!=expected:raise ValueError('Observed label/raw unrated authored routing is easy')
  if template and template!=r['template']:raise ValueError('Incompatible template')
  template=r['template']
 elif level=='hard':
  template=template or ('construct' if field_type=='blank' else rng.choice(('traversal','construct')))
  if template not in ('traversal','construct'):raise ValueError('Hard reads graph and assesses traversal')
  if name not in (None,'method-hard'):raise ValueError('Hard profile must be method-hard')
  name='method-hard';r=None
 else:
  if name in RECIPES:template=template or RECIPES[name]['template']
  template=template or ('graph' if level=='easy' else ('construct' if field_type=='blank' else rng.choice(('traversal','construct'))))
  if template not in (('graph',) if level=='easy' else ('traversal','construct')):raise ValueError('Template outside level')
  pool=[k for k,v in RECIPES.items() if v['template']==template and not v['opaque']]
  if name and name not in pool:raise ValueError('Ineligible profile')
  name=name or rng.choice(pool);r=RECIPES[name]
 if field_type and field_type not in ('blank','radio'):raise ValueError('Unsupported field type')
 expected_type='blank' if template=='construct' else 'radio'
 if field_type and field_type!=expected_type:raise ValueError('Field format incompatible with template')
 # Select whole family/bank first; sampling rejects the whole candidate.
 for attempt in range(200):
  if parameters is not None:p=bounds(level,parameters,raw)
  else:
   domain=list(range(2,10)) if level!='hard' else [sp.Rational(i,2) for i in range(4,19)]
   p0={'a':str(rng.choice(domain)),'b':str(rng.choice(domain)),'point':'A'}
   try:p=bounds(level,p0,raw)
   except ValueError:continue
  fs=copy.deepcopy(r['fields']) if r else method_bank(p)
  if not raw and r and name=='q-15856':fs=fs[1:]
  if template=='construct' and not r:fs=copy.deepcopy(RECIPES['q-274855']['fields'])
  fields=make_fields(fs,p,raw)
  try:
   for f in fields:
    if f[':answer-field/type'].endswith('/radio'):
     pairs=[components(v[':answer/value']) for v in f[':answer-field/choices']]
     if any(trig_signature(pairs[i])==trig_signature(pairs[j]) for i in range(len(pairs)) for j in range(i)):raise ValueError('Whole-bank pair collision')
     valid=[bool(eligible(z,p,template!='graph')) for z in pairs]
     if sum(valid)!=1:raise ValueError('Whole-bank ambiguous/ineligible requested parametrization')
     if '_correct_index' in f and not valid[f['_correct_index']]:raise ValueError('Source correct designation mathematically invalid')
  except ValueError:
   if parameters is not None:raise
   continue
  break
 else:raise RuntimeError('No complete valid bank in domain')
 marked=template!='graph';plot={'a':p['a'],'b':p['b'],'point':p['point'],'marked':marked,'hard':level=='hard'}
 exact_source=bool(raw and p['a']==str(r['parameters']['a']) and p['b']==str(r['parameters']['b']) and (template=='graph' or p['point']==r['parameters']['point']))
 if exact_source:asset={'prompt':r['image'],'renderer':'original inspected source','original_path':str((HERE/'originals'/Path(r['image']).name).resolve())}
 else:asset=render_plots(plot)
 if r:
  prompt=fill(r['prompt_mask'],PLOT=asset['prompt'],A=tex(p['a']),B=tex(p['b']))
  # Point label changes are complete point-component replacements.
  prompt=re.sub(r'([AJ])\('+re.escape(tex(p['a']))+r',0\)',lambda m:p['point']+'('+tex(p['a'])+',0)',prompt)
  solution=fill(r['solution_mask'],A=tex(p['a']),B=tex(p['b'])) if r['solution_mask'] else (None if raw else common_solution(p,False))
 else:
  prompt='![]('+asset['prompt']+')\n\nThe axes have half-unit ticks, with even integers labeled on the grid margins. '
  prompt+='The ellipse is centered at the origin. '+('Construct a set' if template=='construct' else 'Which of the following sets')+' of parametric equations, defined for $\\theta \\in [0,2\\pi ),$ '+('that traverse' if template=='construct' else 'traverse')+' the ellipse once in the counterclockwise direction starting at the marked point $'+p['point']+'$?'
  if template=='construct':prompt+='\n\n$x=$\n{{field-1}}$,\\,y=$\n{{field-2}}$,\\,\\theta \\in [0,2\\pi ).$'
  solution=common_solution(p)
 q={':question/problem':prompt,':question/answer-fields':fields}
 if not raw or r['difficulty'] is not None:q[':question/difficulty']=r['difficulty'] if raw else ':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 task={'radii':[p['a'],p['b']],'demand':'locus' if template=='graph' else 'start_ccw_once','given_radii':level=='moderate','axis_scale':'half-unit-unlabeled-intercepts' if level=='hard' else 'labeled-intercepts'}
 # No seed, bank, profile, field layout, point-letter aliases, or source ID in task fingerprint.
 fingerprint=digest(task)
 canonical={'version':VERSION,'level':q.get(':question/difficulty'),'prompt':prompt,'solution':solution,'fields':[{k:v for k,v in f.items() if k not in (':answer-field/choices','_correct_index')}|{'correct_value':f[':answer-field/choices'][f['_correct_index']][':answer/value'] if '_correct_index' in f else None,'values':sorted(x[':answer/value'] for x in f[':answer-field/choices'])} for f in fields]}
 cid=digest(canonical);q[':question/id']=ident(cid)
 for i,f in enumerate(fields):
  f[':answer-field/id']=ident([cid,i]);ci=f.pop('_correct_index',None)
  for ans in f[':answer-field/choices']:ans[':answer/id']=ident([cid,i,ans[':answer/value']])
  if ci is not None:f[':answer-field/correct']=[':answer/id',f[':answer-field/choices'][ci][':answer/id']]
  if f[':answer-field/type'].endswith('/radio'):rng.shuffle(f[':answer-field/choices'])
 return {'knowledge_point':{'db_id':KP,'id':SOURCE['record'][':knowledge-point/id'],'title':SOURCE['record'][':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'python':sys.version.split()[0],'sympy':sp.__version__,'basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'level':level,'seed':seed,'template':template,'bank_profile':('observed:' if raw else '')+name,'parameters':p,'source_id':r['source_id'] if r else None,'source_difficulty':r['difficulty'] if r else None,'actual_difficulty':q.get(':question/difficulty'),'raw_replay':raw,'evidence_only':raw and r['evidence_only'],'eligible_for_learning':not(raw and r['evidence_only']),'authored_level':level=='hard' or (not raw and r and not r['difficulty']),'task_fingerprint':fingerprint,'content_identity':cid,'plot':asset,'domain':{'positive':True,'unequal_axes':True,'axis_bounds':[2,9],'hard_axis_denominators':[1,2]}}}

# Easy — graph reading only; source integer intercept workload.
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
# Moderate — supplied radii plus start, full period and counterclockwise direction.
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
# Hard — authored half-unit graph reading plus the complete traversal demand.
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def markdown(record):
 q=record['question'];g=record['generation'];actual=q.get(':question/difficulty');label=actual.rsplit('/',1)[-1] if actual else 'unrated (raw; easy routing authored)';out=[f"### {'ORIGINAL SOURCE EVIDENCE / parameterized replay' if g['raw_replay'] else 'GENERATED'} — {label} — {g['template']} — {g['bank_profile']}",q[':question/problem']]
 for f in q.get(':question/answer-fields',[]):
  out.append(f"Field {f[':answer-field/key']} ({f[':answer-field/type']})")
  if ':answer-field/correct' not in f:out.append('Correct designation absent in raw source.')
  for ans in f[':answer-field/choices']:
   correct=f.get(':answer-field/correct',[None,None])[1]==ans[':answer/id'];out.append(('✓ ' if correct else '• ')+'$'+ans[':answer/value']+'$')
 if ':question/worked-solution' in q:out.extend(['Worked solution',q[':question/worked-solution']])
 elif g['raw_replay']:out.append('Worked solution absent in raw source.')
 return '\n\n'.join(out)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=(*LEVELS,'all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 if args.count<1:parser.error('count must be positive')
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (LEVELS if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n'.join(map(markdown,records)))
