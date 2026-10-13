#!/usr/bin/env python3
"""Sketching a 2D vector field, basis 1356. No database writes.

Ten observed five-image banks; q-122756's unkeyed legacy duplicate is retained
in raw evidence and shares the same geometric bank. Empirical profiles encode
complete per-point linear geometric operations; their author intent is unknown.
They are replay/explicit-variation profiles, never default error recipes.
Default five-option banks use the correct arrows, each component sign reversal,
component interchange and reversal of both components. Whole-bank collisions
reject an instance. The six evaluated components use the SAME field/points as
all plots. Matplotlib only, private concurrent JSON input, atomic PNG/sidecars.

Easy preserves source three-point substitution workload. Missing moderate/hard
levels are authored: canonical product/square field, three signed points, half-
and quarter-grid coordinate reading respectively. No derivatives, divergence,
3D vector fields, or inverse field identification are introduced. Explicit
inputs obey the same reduced coordinate/grid and component bounds as samplers.
"""
from __future__ import annotations
import argparse,hashlib,json,math,random,re,subprocess,tempfile,uuid
from pathlib import Path
import sympy as s
KP_ID=17592186172083
KP_UUID='a5b00f0c-fc7f-5262-b1a3-cdd6c1560cd6'
TITLE='Sketching a Two-Dimensional Vector Field'
VERSION='vector-field-2d-v1'
HERE=Path(__file__).with_suffix('');SOURCE=json.loads((HERE/'source.json').read_text())
SOURCE_QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
X,Y=s.symbols('x y',real=True)
A,B=s.symbols('a b',real=True)
# Every family is a complete mathematical component; prose and basis labels
# never participate in blind global single-letter replacement.
FAMILIES={
 'square_linear':(A*X**2,B*Y),
 'trig':(A*s.cos(s.pi*X),B*s.sin(s.pi*Y/2)),
 'trig_product':(A*s.sin(s.pi*X/2),B*X*Y),
 'linear_exp':(A*X,B**Y),
 'ratio_abs':(-A*X/Y,-B*s.Abs(X)),
 'rational_shift':(A*Y/(1-Y),B*X/(Y-1)),
 'rational_product':(A*Y/(X*Y+1),B*X/(X*Y+1)),
 'linear_shared':(Y-A*X,B*Y-A*B*X),
 'affine':(Y-A,X+B),
 'inward':(A*X,B*Y),
 'product_square':(A*X*Y,B*X**2)}
# Source geometries are extracted from inspected plots (units, NOT pixels).
# Geometry of the q-122745 small unlabelled arrow is approximate; raw reuse at
# original parameters guarantees its full fidelity, without exact-value claims.
OBSERVED={
 'q-122264':('square_linear',1,-2,[[-2,1],[0,-2],[2,3]],[
 [[4,-2],[0,4],[4,-6]],[[-2,-2],[0,4],[2,-6]],[[-2,'1/2'],[0,-1],[2,'3/2']],[[-4,-2],[0,4],[-4,-6]],[[4,-1],[0,2],[4,-3]]],0),
 'q-122756':('trig',2,2,[[-3,1],[-2,-1],[4,-4]],[
 [[0,2],[-2,-2],[0,2]],[[-2,2],[2,-2],[2,0]],[[0,2],[2,-2],[0,2]],[[-2,0],[2,2],[-2,0]],[[-2,0],[2,-2],[-2,0]]],1),
 'q-122742':('trig_product',3,1,[[-1,1],[1,2],[2,-1]],[
 [[0,-1],[0,2],[-3,-2]],[[-3,-1],[3,2],[0,-2]],[[3,1],[-3,2],[0,-1]],[[0,-1],[0,2],[3,-2]],[[-3,-1],[3,1],[0,2]]],1),
 'q-122744':('linear_exp',-2,2,[[-4,2],[-1,1],[2,0]],[
 [[4,5],[1,3],[-2,1]],[[8,2],[2,1],[-4,0]],[[-4,-1],[-1,-1],[2,-1]],[[0,3],[1,1],[4,-1]],[[8,4],[2,2],[-4,1]]],4),
 'q-122759':('ratio_abs',1,1,[[-3,1],[2,-1],[4,2]],[
 [[3,-2],[2,-2],[-2,-2]],[[3,-3],[2,-2],[-2,-4]],[[-3,-2],[-2,-2],[2,-2]],[[3,3],[2,2],[-2,4]],[[-3,-3],[-2,-2],[2,-4]]],1),
 'q-122764':('rational_shift',2,1,[[-2,3],[2,-1],[4,2]],[
 [[-1,-3],[-1,-1],[4,-4]],[[-1,1],[1,1],[-2,-4]],[[-3,1],[-1,1],[-4,-4]],[[-3,-1],[-1,-1],[-4,4]],[[1,3],[1,1],[-4,4]]],3),
 'q-122745':('rational_product',1,1,[[-2,0],[1,-2],[0,2]],[
 [[0,-2],[-1,-1],[2,0]],[[0,-4],[4,-2],['5/4',0]],[[0,2],[-1,'1/2'],[2,0]],[[0,2],[4,-2],[2,0]],[[0,-2],[2,-1],[2,0]]],4),
 'q-122752':('linear_shared',2,2,[[1,3],[-1,-1],[3,2]],[
 [[1,2],[1,2],[-4,-8]],[[-1,2],[-1,2],[4,-8]],[[-2,-4],[0,2],[1,-5]],[[5,-1],[-1,-1],[1,4]],[[2,1],[0,1],[-1,-4]]],0),
 'q-122754':('affine',2,2,[[-5,3],[0,0],[2,-3]],[
 [[4,-4],[1,1],[-2,3]],[[1,-3],[-2,2],[-5,4]],[[6,-2],[1,1],[-1,4]],[[2,-4],[-1,1],[-4,3]],[[7,-5],[2,-2],[0,1]]],1),
 'q-122758':('inward',-1,-1,[[1,4],[2,-2],[4,-2]],[
 [[-1,2],[-2,-1],[-4,-1]],[[4,1],[-2,2],[-2,4]],[[-4,1],[2,2],[2,4]],[[-1,-4],[-2,2],[-4,2]],[[1,4],[2,-2],[4,-2]]],3)}
TEMPLATES={v[0]:'easy' for v in OBSERVED.values()}|{'product_square_moderate':'moderate','product_square_hard':'hard'}
RUNTIME='/home/jake/.local/share/uv/python/cpython-3.10.13-linux-x86_64-gnu/bin/python3.10'
DRAW_PROSE='We now draw our vectors. At each point, we draw the vector associated with that point, placing the tail end of the vector on the point itself. This gives the following diagram.'
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(name):return str(uuid.uuid5(uuid.UUID(KP_UUID),name))
def rat(v):
 z=s.Rational(str(v));return z

def field_components(template,p):
 family='product_square' if template.startswith('product_square_') else template
 return tuple(s.simplify(z.subs({A:rat(p['a']),B:rat(p['b'])})) for z in FAMILIES[family])
def evaluate(template,p):
 fs=field_components(template,p)
 return [[s.simplify(f.subs({X:rat(x),Y:rat(y)})) for f in fs] for x,y in p['points']]
def source_parameters(source_id):
 t,a,b,points,bank,k=OBSERVED[source_id]
 return {'a':a,'b':b,'points':points}
def exact_lists(v):return [[str(z) for z in row] for row in v]
def empirical_bank(source_id,correct):
 """Parameterize each empirical plotted arrow with an explicit linear map.

 Prefer its corresponding nonzero component. If that component vanishes in
 the original, use the other original component. A zero arrow component stays
 zero. These are geometric replay operations, NOT recovered misconceptions.
 """
 t,a,b,pts,banks,k=OBSERVED[source_id];base=evaluate(t,source_parameters(source_id));out=[]
 for bank in banks:
  arrows=[]
  for i,row in enumerate(bank):
   coords=[]
   for j,target in enumerate(row):
    target=rat(target)
    if not target:coords.append(s.Integer(0));continue
    axis=j if base[i][j]!=0 else 1-j
    assert base[i][axis]!=0
    coords.append(s.simplify(target/base[i][axis]*correct[i][axis]))
   arrows.append(coords)
  out.append(arrows)
 # The true bank member is always evaluated from the field; maps cannot make
 # original zero components artificially remain zero at changed coordinates.
 out[k]=correct
 return out,k

def authored_bank(correct):
 return [correct,[[u,-v] for u,v in correct],[[-u,v] for u,v in correct],[[v,u] for u,v in correct],[[-u,-v] for u,v in correct]],0

def validate_parameters(level,template,p):
 if set(p)!={'a','b','points'}:raise ValueError('Parameters must be a, b, points')
 a,b=rat(p['a']),rat(p['b']);pts=[[rat(z) for z in r] for r in p['points']]
 if not a or not b or max(abs(a),abs(b))>4:raise ValueError('Nonzero coefficients of magnitude at most 4 required')
 if template=='linear_exp' and (b.q!=1 or b<2):raise ValueError('Exponential base must be a nonunit positive integer 2..4')
 if len(pts)!=3 or any(len(r)!=2 for r in pts) or len(set(map(tuple,pts)))!=3:raise ValueError('Three distinct coordinate pairs required')
 if any(abs(z)>5 for r in pts for z in r):raise ValueError('Coordinates bounded by 5')
 if level=='easy' and any(z.q!=1 for r in pts for z in r):raise ValueError('Easy coordinates must be integers')
 if level in ('moderate','hard'):
  den=2 if level=='moderate' else 4
  if not template.endswith('_'+level) or abs(a)>2 or abs(b)>2 or a.q!=1 or b.q!=1:raise ValueError('Authored level requires canonical product/square workload')
  if any(x.q!=1 or not x or abs(x)>2 or y.q not in (1,den) or not y or abs(y)>2 for x,y in pts):raise ValueError('Signed small x integers and small y grid coordinates required')
  if any(y.q!=den for x,y in pts):raise ValueError('Every y requires the advertised reduced half/quarter grid reading')
  if not(any(y>0 for x,y in pts) and any(y<0 for x,y in pts)):raise ValueError('Mixed signed points required')
 values=evaluate(template,p)
 if any(not z.is_Rational or abs(z)>8 for r in values for z in r):raise ValueError('Undefined or oversized field vectors')
 return {'a':str(a),'b':str(b),'points':exact_lists(pts)}

def tex(z):return s.latex(s.sympify(z)).replace('\\log','\\ln')
def vector_tex(u,v):
 parts=[]
 for z,label in [(u,'i'),(v,'j')]:
  z=s.sympify(z)
  if z==0:continue
  sign='-' if z.could_extract_minus_sign() else '+'
  mag=-z if sign=='-' else z
  body=((r'\left('+tex(mag)+r'\right)' if mag.is_Add else tex(mag))+r'\,') if mag!=1 else ''
  if not parts and sign=='+':sign=''
  parts.append(sign+body+label)
 return ''.join(parts) or '0'
def point_tex(pt):return '('+','.join(tex(z) for z in pt)+')'
def substitution_tex(template,p,pt):
 # Unevaluated complete operation masks retain the two coordinate substitutions.
 x,y=map(tex,pt);a,b=tex(p['a']),tex(p['b']);px='('+x+')';py='('+y+')';pa='('+a+')';pb='('+b+')'
 family='product_square' if template.startswith('product_square_') else template
 masks={
 'square_linear':(pa+px+'^{2}',pb+py),
 'trig':(pa+r'\cos(\pi '+px+')',pb+r'\sin(\frac{\pi '+py+'}{2})'),
 'trig_product':(pa+r'\sin('+tex(s.pi*rat(pt[0])/2)+')',pb+px+py),
 'linear_exp':(pa+px,'{'+b+'}^{'+y+'}'),
 'ratio_abs':('-'+pa+r'\frac{'+x+'}{'+y+'}','-'+pb+'|'+x+'|'),
 'rational_shift':(r'\frac{'+pa+py+'}{1-'+py+'}',r'\frac{'+pb+px+'}{'+py+'-1}'),
 'rational_product':(r'\frac{'+pa+py+'}{'+px+py+'+1}',r'\frac{'+pb+px+'}{'+px+py+'+1}'),
 'linear_shared':(py+'-'+pa+px,pb+py+'-'+pa+pb+px),
 'affine':(py+'-'+pa,px+'+'+pb),
 'inward':(pa+px,pb+py),
 'product_square':(pa+px+py,pb+px+'^{2}')}
 u,v=masks[family];return r'\left('+u+r'\right)\,i+'+r'\left('+v+r'\right)\,j'

def render_plots(points,banks,grid_increment=1,output_dir=None):
 """One bounds/scale across the complete bank. Private unique input and assets.

Each plot's hash uses the exact arrow geometry. Cache requires PNG AND sidecar.
Bounds include all tails/tips with one grid-unit padding, all arrows to scale.
"""
 allxy=[(rat(x),rat(y)) for x,y in points]
 for bank in banks:
  allxy.extend((rat(x)+u,rat(y)+v) for (x,y),(u,v) in zip(points,bank))
 lo=min(min(x for x,y in allxy),min(y for x,y in allxy),-1);hi=max(max(x for x,y in allxy),max(y for x,y in allxy),1)
 bounds=[int(math.floor(lo))-1,int(math.ceil(hi))+1]*2
 plot_dir=Path(output_dir) if output_dir is not None else HERE/'plots'
 plot_dir.mkdir(exist_ok=True);items=[];paths=[]
 for bank in banks:
  data={'points':points,'vectors':exact_lists(bank),'bounds':bounds,'grid_increment':grid_increment,'render_version':VERSION}
  path=plot_dir/(digest(data)+'.png');paths.append(str(path))
  if not(path.exists() and path.with_suffix('.json').exists()):items.append({**data,'points':[[float(rat(z)) for z in r] for r in points],'vectors':[[float(z) for z in r] for r in bank],'path':str(path),'exact_points':points,'exact_vectors':exact_lists(bank)})
 if items:
  with tempfile.TemporaryDirectory(prefix='render-',dir=plot_dir) as private:
   inp=Path(private)/'input.json';inp.write_text(json.dumps(items));subprocess.run([RUNTIME,str(HERE/'render.py'),str(inp)],check=True,capture_output=True)
 return paths

def sample(level,template,rng):
 if level=='easy':
  source_id=next(q for q,v in OBSERVED.items() if v[0]==template)
  p=source_parameters(source_id);p={'a':p['a'],'b':p['b'],'points':[r[:] for r in p['points']]}
  # Keep complete operation/number forms familiar, vary signed coordinates.
  p['points']=[[rng.randint(-4,4),rng.randint(-3,3)] for _ in range(3)]
  return p
 den=2 if level=='moderate' else 4
 ys=[s.Rational(i,den) for i in range(-2*den+1,2*den) if i and s.Rational(i,den).q==den]
 points=[[rng.choice([-2,-1,1,2]),str(rng.choice(ys))] for _ in range(3)]
 return {'a':rng.choice([-2,-1,1,2]),'b':rng.choice([-2,-1,1,2]),'points':points}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('Only image radio fields supported')
 rng=random.Random(seed)
 if profile and profile.startswith('observed_'):
  sid=profile[len('observed_'):];sid=sid.removesuffix('_legacy')
  if sid not in OBSERVED:raise ValueError('Unknown observed profile')
  template=template or OBSERVED[sid][0]
  if template!=OBSERVED[sid][0]:raise ValueError('Source profile/template mismatch')
 else:
  if profile not in (None,'authored_sign_swap'):raise ValueError('Unknown profile')
  sid=None
 template=template or rng.choice([t for t,l in TEMPLATES.items() if l==level])
 if TEMPLATES.get(template)!=level:raise ValueError('Template/level mismatch')
 for attempt in range(1000):
  try:
   p=validate_parameters(level,template,parameters if parameters is not None else sample(level,template,rng));correct=evaluate(template,p)
   banks,k=empirical_bank(sid,correct) if sid else authored_bank(correct)
   if len({json.dumps(exact_lists(z)) for z in banks})!=5:raise ValueError('Complete bank collision')
   break
  except ValueError:
   if parameters is not None:raise
 else:raise RuntimeError('Sampler failed to build complete bank')
 original=sid is not None and p==validate_parameters('easy',template,source_parameters(sid))
 paths=render_plots(p['points'],banks,1 if level=='easy' else .5 if level=='moderate' else .25)
 if original:
  paths=[str(Path('/media/jake/SSD/EDB/math')/a[':answer/value']) for a in SOURCE_QUESTIONS[sid][':question/answer-fields'][0][':answer-field/choices']]
 fs=field_components(template,p);formula=vector_tex(*fs)
 prompt='Which of the following diagrams represents the vector field $F(x,y)='+formula+'$ at the indicated points?'
 pts=[point_tex(r) for r in p['points']]
 intro='We have to sketch the vector field at the points $'+','.join(pts[:2])+',$ and $'+pts[2]+'.$'
 opening='To sketch the vector field at the given points, we substitute their coordinates into the function $F(x,y)='+formula+(':' if template=='trig' else r'\,:')+'$'
 rows=[r'F'+pt+' & ='+substitution_tex(template,p,xy)+'='+vector_tex(*v) for pt,xy,v in zip(pts,p['points'],correct)]
 solution=intro+'\n\n'+opening+'\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\n'+DRAW_PROSE+'\n\n![]('+paths[k]+')'
 # Exact source image reuse is geometry cache only; all changed mathematical
 # parameters pass through the same linear-bank operations and renderer above.
 bank_geometry=exact_lists(correct)
 identity=digest({'version':VERSION,'problem':prompt,'solution':solution,'images':sorted(paths),'geometry':sorted(json.dumps(exact_lists(b)) for b in banks),'difficulty':level})
 fid=uid(identity+'/field/selection');answers=[]
 for i,(path,bank) in enumerate(zip(paths,banks)):
  aid=uid(fid+'/'+digest({'geometry':exact_lists(bank),'path':path}));answers.append({':answer/id':aid,':answer/type':':answer.type/image',':answer/value':path})
 correct_id=answers[k][':answer/id'];rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}
 question={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[field]}
 task=digest({'field':[s.srepr(f) for f in fs],'points':sorted(p['points']),'grid_increment':1 if level=='easy' else str(s.Rational(1,2 if level=='moderate' else 4))})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,'generation':{'version':VERSION,'level':level,'seed':seed,'template':template,'parameters':p,'profile':profile or 'authored_sign_swap','bank_profile':profile or 'authored_sign_swap','source':{k:SOURCE[k] for k in ('database','basis','lineage')},'content_identity':identity,'mathematical_fingerprint':task,'correct_vectors':bank_geometry,'plot_banks':[{'path':path,'vectors':exact_lists(bank)} for path,bank in zip(paths,banks)],'source_original_geometry':original,'source_refs':[sid] if sid else [],'authored_level':level!='easy','source_repairs':['legacy duplicate field reduced to one authoritative widget'] if sid=='q-122756' else ['correct designation inferred mathematically; source missing designation and solution'] if sid=='q-122264' else [],'empirical_precision_limit':sid=='q-122745','domain':{'ratio_abs':'y != 0','rational_shift':'y != 1','rational_product':'xy != -1','linear_exp':'real x,y; positive integer base 2..4'}.get(template,'real x,y')}}

# EASY: observed three signed integer points; six scalar component evaluations.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE (authored): canonical product/square, three half-grid y coordinates.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD (authored): same six evaluations/placement; three reduced quarter-grid y.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(rec):
 q=rec['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n\n'.join('![]('+a[':answer/value']+')' for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,args.template,profile=args.profile) for level in levels for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
