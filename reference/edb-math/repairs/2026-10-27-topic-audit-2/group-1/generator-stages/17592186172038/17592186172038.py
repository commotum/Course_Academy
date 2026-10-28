#!/usr/bin/env python3
"""Three-point slope-field radio generator, basis1356. Stops at steps3–7.

Six observed mathematical forms; seven preserved source profiles, separate
exchangeable coefficient-case authored bank. All profiles have five plotted choices.
Observed arbitrary local orientation patterns are parameterized through slope
values/coordinate arithmetic and are not asserted as recovered student errors.
Moderate/hard are authored arithmetic domains (three substitutions, no DE solving,
quadrant inference or whole-field recognition). Explicit inputs never resample.
Matplotlib uses the declared runtime; assets go to the explicit output directory.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,tempfile,uuid,math,os,sys
from pathlib import Path
import sympy as sp
from math_format import validate_generated_record,normalize_prose
KP_ID=17592186172038
KP_UUID='b0e7e0a0-9388-5346-ab96-f2dec237c9f5'
TITLE='Sketching the Slope Field of a Differential Equation at Some Isolated Points'
VERSION='isolated-slopes-v6-distinguishable-hard-rational-bank'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X,Y=sp.symbols('x y')
TEMPLATES=('constant_product','quadratic_linear','rational_square','two_quadratic','affine_fraction','affine')
# Complete observed profiles in captured choice order. s0,s1,s2 are correct slopes.
PROFILES={
 'q-50099':('constant_product',{'a':2,'b':1,'points':[[-1,2],[1,3],[0,-2]]},['s0,s1,0','s0,-s1,s2','-s0,s1,-s2','s0,s1,s2','0,s1,s2']),
 'q-80494':('quadratic_linear',{'a':1,'b':2,'points':[[1,2],[-1,-1],[2,-2]]},['s0,s1,s2','-s0,-s1,0','-s0,0,-s2','0,-s1,s2','-s0,s1,s2']),
 'q-119674':('rational_square',{'a':-1,'points':[[-1,-2],[2,-2],[2,2]]},['s0,s1,s2','s0,s1,-s2','0,s1,s2','s0,-s1,s2','-s0,0,-s2']),
 'q-49811':('two_quadratic',{'a':2,'b':'1/2','points':[[1,2],[1,0],[-1,-2]]},['oo,a/2,-a/2','s0,s1,s2','oo,a/2,a/2','oo,a/2,0','-a/2,a/2,-a/2']),
 'q-80499':('affine_fraction',{'a':1,'b':2,'d':4,'points':[[4,-2],[2,1],[-1,3]]},['s0,-s1,s2','s2,-s1,s0','-s1,s1,s0','s0,s1,s2','-s1,s0,s2']),
 'q-80497':('affine',{'a':1,'b':-2,'points':[[-2,-1],[2,-1],[2,1]]},['-s1,s1,s1','s1,0,s1','0,0,0','s0,s1,s2','-s1,-s1,-s1']),
 'q-96089':('affine',{'a':1,'b':2,'points':[[-2,1],[1,1],[2,1]]},['0,0,a','s0,s1,s2','-s1,a,-a','a,a,0','a,a,-a']),
}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(v):return str(uuid.uuid5(uuid.UUID(KP_UUID),v))
def tex(v):return sp.latex(sp.sympify(v))
def eq(template,p):
 a=sp.Rational(p['a']);b=sp.Rational(p.get('b',1));d=sp.Rational(p.get('d',1))
 return {'constant_product':a-b*X*Y,'quadratic_linear':a*X**2-b*Y,'rational_square':a*Y**2/X,'two_quadratic':a*X**2-b*Y**2,'affine_fraction':(a*X+b*Y)/d,'affine':a*X+b*Y}[template]
def validate_parameters(level,t,p):
 if t not in TEMPLATES:raise ValueError('Unknown template')
 expected={'a','points'}|({'b'} if t!='rational_square' else set())|({'d'} if t=='affine_fraction' else set())
 if set(p)!=expected:raise ValueError('Exact parameter keys required: '+str(expected))
 vals=[sp.Rational(v) for k,v in p.items() if k!='points']
 limit={'easy':4,'moderate':4,'hard':6}[level]
 if any(v==0 or abs(v)>limit or v.q>({'easy':4,'moderate':2,'hard':4}[level]) for v in vals):raise ValueError('Coefficient domain')
 if 'd' in p and (sp.Rational(p['d']).q!=1 or sp.Rational(p['d'])<=0):raise ValueError('Positive integral denominator required')
 if len(p['points'])!=3 or any(len(pt)!=2 for pt in p['points']):raise ValueError('Exactly three coordinates')
 coords=[[sp.Rational(v) for v in pt] for pt in p['points']]
 if any(abs(v)>({'easy':4,'moderate':3,'hard':sp.Rational(7,2)}[level]) for pt in coords for v in pt):raise ValueError('Coordinate domain')
 if len({tuple(v) for v in coords})!=3:raise ValueError('Distinct points required')
 if t=='rational_square' and any(x==0 for x,y in coords):raise ValueError('x cannot vanish')
 if level=='easy':
  if any(v.q!=1 for pt in coords for v in pt):raise ValueError('Easy integral coordinates')
  if any(sp.Rational(v).q!=1 and not (t=='two_quadratic' and k=='b' and sp.Rational(v).q==2) for k,v in p.items() if k!='points'):raise ValueError('Observed-compatible easy coefficients')
 if level=='moderate':
  if any(sp.Rational(v).q!=1 for k,v in p.items() if k not in ('a','points')):raise ValueError('Moderate remaining coefficients integral')
  if sp.Rational(p['a']).q!=2 or any(v.q!=1 for pt in coords for v in pt):raise ValueError('Moderate nonintegral half leading coefficient, integral coordinates')
 if level=='hard':
  if t not in ('two_quadratic','rational_square','affine_fraction') or sp.Rational(p['a']).q not in (2,4) or any(v.q!=2 for pt in coords for v in pt):raise ValueError('Hard fractional leading coefficient and two half coordinates at every point')
 if level!='easy' and not any(v<0 for pt in coords for v in pt):raise ValueError('Signed substitution required')

def sample(level,t,r):
 bound={'easy':3,'moderate':3,'hard':4}[level]
 p={'a':r.choice([1,2,3,-1,-2])}
 if t!='rational_square':p['b']=r.choice([1,2,3,-1,-2])
 if level=='moderate':p['a']=str(r.choice([sp.Rational(1,2),sp.Rational(-3,2),sp.Rational(5,2),sp.Rational(-7,2)]))
 if level=='hard':p['a']=str(r.choice([sp.Rational(1,2),sp.Rational(-3,2),sp.Rational(3,4),sp.Rational(-5,4)]))
 if t=='affine_fraction':p['d']=r.choice([2,3,4])
 p['points']=r.sample([[x,y] for x in range(-bound,bound+1) for y in range(-bound,bound+1) if t!='rational_square' or x!=0],3)
 if level=='hard':p['points']=r.sample([[str(sp.Rational(x,2)),str(sp.Rational(y,2))] for x in (-7,-5,-3,-1,1,3,5,7) for y in (-7,-5,-3,-1,1,3,5,7)],3)
 return p

def coefficient_cases(level,t,p,r):
 # Build the bank before assigning correctness. No row has a special error role.
 leading=[1,2,3,-1,-2]
 if level=='moderate':leading=['1/2','-3/2','5/2','-7/2','3/2']
 if level=='hard':leading=['1/2','-3/2','3/4','-1/2','5/4']
 # The old−3/2,−5/4 pair can never separate by8degrees for a common multiplier.
 leading=list(dict.fromkeys(map(str,leading+[p['a']])))
 secondary=list(dict.fromkeys(map(str,[1,2,3,-1,-2]+([p['b']] if 'b' in p else []))))
 candidates=[{**p,'a':a,**({'b':b} if t!='rational_square' else {})}
             for a in leading for b in (secondary if t!='rational_square' else [None])]
 key=lambda q:tuple(str(sp.Rational(q[k])) for k in ('a','b') if k in q)
 others=[q for q in candidates if key(q)!=key(p)]
 if len(others)<4:raise ValueError('Not enough coefficient cases')
 return [p]+r.sample(others,4)

def banks(t,p,profile,alternatives=None):
 expr=eq(t,p);s=[sp.simplify(expr.subs({X:x,Y:y})) for x,y in [[sp.Rational(v) for v in pt] for pt in p['points']]]
 if profile!='authored':
  env={f's{i}':v for i,v in enumerate(s)}|{k:sp.Rational(v) for k,v in p.items() if k!='points'}|{'oo':sp.oo}
  bank=[[sp.sympify(v,locals=env) for v in recipe.split(',')] for recipe in PROFILES[profile][2]]
 else:
  alternatives=alternatives or coefficient_cases('easy',t,p,random.Random(digest(p)))
  bank=[[eq(t,q).subs({X:sp.Rational(x),Y:sp.Rational(y)}) for x,y in p['points']] for q in alternatives]
 bank=[[sp.simplify(v) for v in row] for row in bank]
 if any(v.has(sp.zoo,sp.nan) for row in bank for v in row):raise ValueError('Invalid bank member')
 if len({tuple(row) for row in bank})!=5 or bank.count(s)!=1:raise ValueError('Whole-bank ambiguity')
 if profile=='authored':
  for i,row in enumerate(bank):
   for other in bank[:i]:
    diffs=[]
    for a,b in zip(row,other):
     aa=math.pi/2 if a==sp.oo else math.atan(float(a));bb=math.pi/2 if b==sp.oo else math.atan(float(b));delta=abs(aa-bb);diffs.append(min(delta,math.pi-delta))
    if max(diffs)<math.radians(8):raise ValueError('Visually indistinguishable whole bank')
 return s,bank

def render_plots(instance,output_dir=None):
 if output_dir is None:
  configured=os.environ.get('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR')
  if not configured:raise ValueError('COURSE_ACADEMY_GENERATOR_OUTPUT_DIR is required')
  output_dir=Path(configured)
 output_dir=Path(output_dir).resolve()
 if output_dir==HERE or output_dir.is_relative_to(HERE):
  raise ValueError('Generated assets must be outside the bundled runtime data directory')
 records=[];paths=[]
 exact_points=instance['points'];points=[[float(sp.Rational(v)) for v in pt] for pt in exact_points];xs=[0]+[p[0] for p in points];ys=[0]+[p[1] for p in points]
 bounds=[min(xs)-1,max(xs)+1,min(ys)-1,max(ys)+1]
 for slopes in instance['bank']:
  data={'points':points,'exact_points':exact_points,'slopes':['inf' if v==sp.oo else str(v) for v in slopes],'bounds':bounds}
  if any(sp.Rational(v).q!=1 for pt in exact_points for v in pt):data['coordinate_labels']='exact-half-v2'
  # The runner binds relative references against the runtime, not output_dir.
  # Emit the configured absolute output path so both directories may relocate.
  path=Path(output_dir)/(digest(data)+'.png');paths.append(str(path))
  if not path.exists() or not path.with_suffix('.json').exists():records.append(dict(data,path=str(path)))
 if records:
  Path(output_dir).mkdir(parents=True,exist_ok=True)
  with tempfile.NamedTemporaryFile('w',dir=output_dir,prefix='render-input-',suffix='.json',delete=False) as f:json.dump(records,f);name=f.name
  try:subprocess.run([sys.executable,str(HERE/'render_plots.py'),name],check=True,capture_output=True,env={**os.environ,'MPLCONFIGDIR':str(Path(output_dir)/'.mplconfig')})
  finally:Path(name).unlink(missing_ok=True)
 return {'choices':paths,'solution':paths[instance['correct_index']]}

def factor_tex(v):
 # Keep signed multiplicative coefficients grouped; never emit bare -- or +-.
 return '('+tex(v)+')' if sp.Rational(v)<0 else tex(v)

def substitute_tex(t,p,x,y):
 # Unevaluated complete component masks preserve the substitution stage.
 a=tex(p['a']);af=factor_tex(p['a']);b=tex(p.get('b',1));bf=factor_tex(p.get('b',1));d=tex(p.get('d',1));xx=f'({tex(x)})';yy=f'({tex(y)})'
 return {'constant_product':f'{a}-{bf}{xx}{yy}','quadratic_linear':f'{af}{xx}^{{2}}-{bf}{yy}','rational_square':rf'{af}\frac{{{yy}^{{2}}}}{{{xx}}}','two_quadratic':f'{af}{xx}^{{2}}-{bf}{yy}^{{2}}','affine_fraction':rf'\frac{{{af}{xx}+({b}){yy}}}{{{d}}}','affine':f'{af}{xx}+({b}){yy}'}[t]

def evaluated_tex(t,p,x,y):
 a=sp.Rational(p['a']);b=sp.Rational(p.get('b',1));d=sp.Rational(p.get('d',1));x=sp.Rational(x);y=sp.Rational(y)
 return {'constant_product':f'{tex(a)}-({tex(b*x*y)})','quadratic_linear':f'{tex(a*x*x)}-({tex(b*y)})','rational_square':rf'{factor_tex(a)}\frac{{{tex(y*y)}}}{{{tex(x)}}}','two_quadratic':f'{tex(a*x*x)}-({tex(b*y*y)})','affine_fraction':rf'\frac{{{tex(a*x)}+({tex(b*y)})}}{{{tex(d)}}}','affine':f'{tex(a*x)}+({tex(b*y)})'}[t]

def rhs_tex(t,p):
 a=tex(p['a']);af=factor_tex(p['a']);b=tex(p.get('b',1));d=tex(p.get('d',1))
 return {'constant_product':f'{a}-({b})xy','quadratic_linear':f'{af}x^{{2}}-({b})y','rational_square':rf'{af}\frac{{y^{{2}}}}{{x}}','two_quadratic':f'{af}x^{{2}}-({b})y^{{2}}','affine_fraction':rf'\frac{{{af}x+({b})y}}{{{d}}}','affine':f'{af}x+({b})y'}[t]

def presentation(t,p,profile,s,assets,level):
 rhs=rhs_tex(t,p);rows=[rf' & {{\frac{{\text{{d}}y}}{{\text{{d}}x}}|}}_{{({tex(x)},{tex(y)})}}={substitute_tex(t,p,x,y)}'+('='+evaluated_tex(t,p,x,y) if profile=='authored' and level!='easy' else '')+f'={tex(v)}'+(',' if i<2 else '.') for i,((x,y),v) in enumerate(zip(p['points'],s))]
 aligned=r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'
 if profile!='authored':
  q=QUESTIONS[profile];source_params=PROFILES[profile][1];original_rhs=q[':question/problem'].split('=',1)[1].rstrip('?$').rstrip('$?')
  # A complete RHS slot; no global symbol/text replacement.
  problem=q[':question/problem'].split('=',1)[0]+'='+rhs+('?$' if q[':question/problem'].endswith('?$') else '$?')
  if sp.simplify(eq(t,p)-eq(t,source_params))==0:problem=q[':question/problem']
  raw=q.get(':question/worked-solution')
  if raw:
   solution=re.sub(r'\\begin\{aligned\}.*?\\end\{aligned\}',lambda m:aligned,raw,flags=re.S)
   opening=solution.split('\n\n',1)[0];original_pts=source_params['points']
   for i,(x,y) in enumerate(original_pts):opening=opening.replace(f'({x},{y})',f'<<P{i}>>')
   for i,(x,y) in enumerate(p['points']):opening=opening.replace(f'<<P{i}>>',f'({x},{y})')
   solution=opening+'\n\n'+solution.split('\n\n',1)[1]
   solution=re.sub(r'!\[\]\([^)]*\)',lambda m:f'![]({assets["solution"]})',solution)
   return problem,solution,rows
 else:problem=rf'Which of the following diagrams gives the slope field at the points indicated for the differential equation $\frac{{\text{{d}}y}}{{\text{{d}}x}}={rhs}?$'
 pts=','.join(f'$({tex(x)},{tex(y)})$' for x,y in [[sp.Rational(v) for v in pt] for pt in p['points']])
 solution=f'We have to sketch the slope field at the points {pts}.\n\nTo sketch the slope field at the given points, we substitute their coordinates into the right-hand side of the differential equation.\n\n$$\n{aligned}\n$$\n\nSetting up our points and drawing our line segments, we get the following diagram.\n\n![]({assets["solution"]})'
 return problem,solution,rows

# Easy observed/source domains, moderate and hard authored domains.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None,bank_parameters=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Radio only')
 profile=profile or 'authored'
 if profile not in ('authored',*PROFILES):raise ValueError('Unknown bank profile')
 r=random.Random(seed)
 eligible=TEMPLATES if level!='hard' else ('two_quadratic','rational_square','affine_fraction')
 t=template or (PROFILES[profile][0] if profile!='authored' else r.choice(eligible))
 if profile!='authored' and t!=PROFILES[profile][0]:raise ValueError('Profile/template mismatch')
 for attempt in range(1000):
  p=dict(parameters) if parameters is not None else sample(level,t,r)
  try:
   validate_parameters(level,t,p)
   alternatives=None
   if profile=='authored':
    alternatives=bank_parameters or coefficient_cases(level,t,p,r)
    if len(alternatives)!=5:raise ValueError('Five coefficient cases required')
    for q in alternatives:
     validate_parameters(level,t,q)
     if q['points']!=p['points'] or sp.Rational(q.get('d',1))!=sp.Rational(p.get('d',1)):raise ValueError('Common points and denominator required')
   s,bank=banks(t,p,profile,alternatives)
   if profile=='authored' and parameters is None:
    # Validity and all rejection decisions precede the answer assignment.
    chosen=r.randrange(5);p=dict(alternatives[chosen]);s=bank[chosen]
   break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('No valid whole bank')
 p={k:([[int(sp.Rational(v)) if sp.Rational(v).q==1 else str(sp.Rational(v)) for v in pt] for pt in value] if k=='points' else str(sp.Rational(value))) for k,value in p.items()}
 canonical={k:([list(pt) for pt in v] if k=='points' else str(sp.Rational(v))) for k,v in p.items()}
 ci=bank.index(s);assets=render_plots({'points':p['points'],'bank':bank,'correct_index':ci})
 problem,solution,rows=presentation(t,p,profile,s,assets,level)
 problem,solution=normalize_prose(problem),normalize_prose(solution)
 task=digest({'equation':str(eq(t,p)),'points':sorted(p['points'])})
 # Output paths locate bytes, but do not define mathematical/content identity.
 identity=digest({'version':VERSION,'level':level,'problem':problem,'solution':solution.replace(assets['solution'],Path(assets['solution']).name),'bank':sorted(Path(v).name for v in assets['choices'])})
 fid=uid(identity+'field');answers=[{':answer/id':uid(fid+'answer:'+Path(v).name),':answer/type':':answer.type/image',':answer/value':v} for v in assets['choices']]
 correct=answers[ci][':answer/id'];r.shuffle(answers)
 record={'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]},'generation':{'version':VERSION,'template':t,'bank_profile':profile,'bank_parameters':alternatives,'sampling_attempts':attempt+1,'seed':seed,'parameters':canonical,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},'source_ids':[profile] if profile!='authored' else [],'authored':profile=='authored' or level!='easy','mathematical_fingerprint':task,'content_fingerprint':identity,'exact_slopes':list(map(str,s)),'choice_geometry':{path:list(map(str,row)) for path,row in zip(assets['choices'],bank)},'worked_rows':rows,'domain':{'point_count':3,'equation':str(eq(t,p)),'x_nonzero':t=='rational_square'}}}
 validate_generated_record(record)
 return record
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n\n'.join(f'{i+1}. ![]({a[":answer/value"]})' for i,a in enumerate(f[':answer-field/choices']))+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 records=[generate(l,args.seed+i,template=args.template,profile=args.profile) for l in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
