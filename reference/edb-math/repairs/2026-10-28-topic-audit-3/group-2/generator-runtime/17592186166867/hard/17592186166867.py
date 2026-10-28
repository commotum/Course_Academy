#!/usr/bin/env python3
"""Origin-vertex horizontal parabolas: graph reading, y²=4px, implicit derivative.

Basis 1356. Easy is authored (given equation with positive integral coefficient); moderate and
hard retain observed right/left geometry. All levels use integer marked points
1<=|a|,|b|<=8. No radicals/real-coefficient escape in any profile. Observed radio
banks are public evidence-only parameterized profiles, not default teaching
banks; their numerical transformations do not establish original author intent.
Raw profiles preserve absent difficulty, solution and correct-ref attributes.
Completed profiles infer missing answers and repair q-127510's vertex prose.
"""
from __future__ import annotations
import argparse,hashlib,json,random,subprocess,tempfile,uuid,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().with_suffix(''); VERSION='parabola-graph-v1'
KP_ID=17592186166867;TITLE='Calculating the Slope of the Tangent to a Parabola'
KP_UUID='53a1649d-4279-5b7c-839c-728f333b2c3f'
X,Y=sp.symbols('x y',real=True)
DY=r'\frac{\text{d}y}{\text{d}x}';DX=r'\frac{\text{d}}{\text{d}x}'
SOURCES=json.loads((HERE/'source.json').read_text());QS={q[':question/math-academy-id']:q for q in SOURCES['record'][':knowledge-point/questions']}
SOURCE_PARAMS={'q-127372':(1,2),'q-127374':(-2,2),'q-127510':(3,6),'q-127515':(-1,2),'q-127520':(-8,4),'q-312780':(5,7),'q-342215':(-3,-1),'q-342218':(-6,6),'q-342354':(8,-8),'q-342355':(6,-2)}
CURRENT_SOURCES=json.loads((HERE/'source-current.json').read_text())
CURRENT_QS={q[':question/math-academy-id']:q for q in CURRENT_SOURCES['record'][':knowledge-point/questions']}
SOURCE_PARAMS['q-127503']=(2,-3)
TEMPLATES=('point_radio','point_blank','equation_radio','equation_blank')
def tex(v): return sp.latex(sp.sympify(v)).replace(' ','')
def uid(v):return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(v,sort_keys=True,separators=(',',':'))))
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def domain(level):
 sign=-1 if level=='hard' else 1
 return [(sign*a,b) for a in range(1,9) for b in range(-8,9) if b and (level!='easy' or sp.Rational(b*b,a).q==1)]
def parameters_valid(level,p):
 if set(p)!={'a','b'} or any(isinstance(v,bool) or not isinstance(v,int) for v in p.values()):raise ValueError('Exact integer a,b required')
 if (p['a'],p['b']) not in domain(level):raise ValueError('Outside finite same-level marked-point domain')
 return p['a'],p['b']
def render_plots(a,b,output_dir=None):
 out=(Path(output_dir) if output_dir else HERE/'plots')/f'{digest(['plot-v2',a,b])}.png';out.parent.mkdir(parents=True,exist_ok=True)
 if not(out.exists() and out.with_suffix('.json').exists() and 'dependencies' in json.loads(out.with_suffix('.json').read_text())):
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-',dir=HERE,delete=False) as f:json.dump({'a':a,'b':b,'out':str(out)},f);inp=Path(f.name)
  try:subprocess.run([str(Path('.venv/bin/python').resolve()),str(HERE/'render_plot.py'),str(inp)],check=True,stdout=subprocess.DEVNULL)
  finally:inp.unlink(missing_ok=True)
 return str(out.resolve())
def bank(profile,a,b):
 c=sp.Rational(b*b,a);m=c/(2*Y);p=c/4
 # Complete banks, never first-valid members of a pooled list.
 if profile=='authored-method':return [m,-m,c/Y,2*Y/c,c/2],['correct','wrong sign','omit chain factor 2','invert derivative','omit chain factor y']
 if profile=='q-127372':return [-2*Y/c,-m,m,-c/Y,c*Y],['negative inverse','negative correct','correct','negative omit 2','multiply by y']
 if profile=='q-127374':return [-Y/c,-m,m,c/Y,c/(4*Y)],['negative inverse','negative correct','correct','omit 2','extra factor 2']
 if profile=='q-127510':return [-sp.Rational(a,b)/Y,m,-2/(c*Y),sp.Rational(b,a)/Y,p/(2*Y)],['negative inverse point ratio (opaque)','correct','negative inverse coefficient','point ratio (opaque)','differentiate p as c (opaque)']
 if profile=='q-127515':return [m,c/(4*Y),-2/(c*Y),-m,-c/Y],['correct','extra factor 2','negative inverse coefficient','negative correct','negative omit 2']
 if profile=='q-127503':return [-c*Y,sp.Rational(b,2*a)/Y,-sp.Rational(b,2*a)*Y,c/Y,m],['negative coefficient times y','signed point ratio (opaque)','negative signed point ratio times y (opaque)','omit 2','correct']
 if profile=='q-127520':return [c/Y,m,-1/(2*c*Y),c/(4*Y),-2*c/Y],['omit 2','correct','negative inverse double coefficient','extra factor 2','negative double coefficient']
 return [m],['correct']
def solution(a,b,style=None,repair=True):
 c=sp.Rational(b*b,a);p=c/4;m=c/(2*Y); left=a<0
 head=f'The diagram shows that the parabola has its vertex at $O,$ and passes through the point $({a},{b}).$'
 origin=f'({a},{b})' if style=='q-127510' and not repair else '(0,0)'
 adjective='general' if left else 'standard'
 square=('{'+str(b)+'}^{2}') if style=='q-342218' else '('+str(b)+')^{2}'
 return head+f'\n\nThe {adjective} equation of a left- or right-opening parabola whose vertex is at ${origin}$ is given by\n\n$$\n'+r'{y}^{2}=4px.'+'\n$$\n\n'+f'Substituting $x={a}$ and $y={b}$ into the equation above, we get\n\n$$\n'+r'\begin{aligned}'+square+f' & =4p({a}) '+r'\\ '+str(b*b)+f' & ={4*a}p '+r'\\ p & ='+tex(p)+r'.\end{aligned}'+'\n$$\n\nTherefore, the equation of our parabola is \n\n$$\n'+r'{y}^{2}='+tex(c)+'x.\n$$\n\nFinally, to calculate $'+DY+r',$ we use implicit differentiation:'+'\n\n$$\n'+r'\begin{aligned}'+DX+r'({y}^{2}) & ='+DX+'('+tex(c)+r'x) \\ 2y'+DY+' & ='+tex(c)+r' \\ '+DY+' & ='+tex(m)+r'\end{aligned}'+'\n$$'
def solution_easy(c):
 # Supplying the equation removes graph-to-p reconstruction; retain the source's
 # formal derivative, chain factor and isolation as separate displayed rows.
 return 'The equation of our parabola is \n\n$$\n'+r'{y}^{2}='+tex(c)+'x.\n$$\n\nFinally, to calculate $'+DY+r',$ we use implicit differentiation:'+'\n\n$$\n'+r'\begin{aligned}'+DX+r'({y}^{2}) & ='+DX+'('+tex(c)+r'x) \\ 2y'+DY+' & ='+tex(c)+r' \\ '+DY+' & ='+tex(c/(2*Y))+r'\end{aligned}'+'\n$$'
def dependency_metadata(asset):
 if asset.startswith('images/'):
  plot={'kind':'captured original raster','renderer_dependencies':'unknown historical renderer','asset':asset}
 else:
  side=json.loads(Path(asset).with_suffix('.json').read_text())
  plot={'kind':'Matplotlib parameterized plot','sidecar':str(Path(asset).with_suffix('.json')),'dependencies':side['dependencies']}
 return {'python':sys.version,'sympy':sp.__version__,'plot':plot}
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed);source=None;mode=None
 if profile and ':' in profile:
  mode,source=profile.split(':',1)
  if mode not in ('raw','completed','current') or source not in (CURRENT_QS if mode=='current' else QS):raise ValueError('Unknown source profile')
 if source:
  q0=(CURRENT_QS if mode=='current' else QS)[source];kind=q0[':question/answer-fields'][0][':answer-field/type'][':db/ident'].rsplit('/',1)[1]
  template=template or 'point_'+kind
  expected='hard' if SOURCE_PARAMS[source][0]<0 else 'moderate'
  if level!=expected:raise ValueError('Source geometry requires its documented level')
 else:kind=field_type or (template.split('_')[-1] if template else 'radio' if profile=='authored-method' else 'blank' if profile=='blank' else rng.choice(('blank','radio')));template=template or ('equation_' if level=='easy' else 'point_')+kind
 if template not in TEMPLATES or template!=('equation_' if level=='easy' else 'point_')+kind or field_type and field_type!=kind:raise ValueError('Template/layout mismatch')
 chosen=source or profile or ('authored-method' if kind=='radio' else 'blank')
 if profile and not source and profile not in ('authored-method','blank'):raise ValueError('Unknown profile')
 if kind=='blank' and chosen=='authored-method' or kind=='radio' and chosen=='blank':raise ValueError('Profile/layout mismatch')
 # Select profile first; rejected parameters invalidate the whole complete bank.
 choices=[]
 for attempt in range(500):
  p=parameters or dict(zip(('a','b'),rng.choice(domain(level))));a,b=parameters_valid(level,p)
  vals,recipes=bank(chosen,a,b)
  if all(sp.simplify(x-y)!=0 for i,x in enumerate(vals) for y in vals[i+1:]):break
  if parameters:raise ValueError('Complete bank collision')
 else:raise RuntimeError('No eligible whole instance')
 c=sp.Rational(b*b,a);answer=c/(2*Y)
 # Original assets are reused only with their exact marked geometry. Changed
 # parameters ALWAYS call the same parameter-driven Matplotlib renderer.
 if source and (a,b)==SOURCE_PARAMS[source]:asset=q0[':question/problem'].split(')')[0].split('(')[1]
 else:asset=render_plots(a,b)
 direction='left' if a<0 else 'right'
 deriv=r'\frac{dy}{dx}' if source in ('q-127372','q-127374') and mode!='current' else DY
 prompt=f'![]({asset})\n\n'+('The parabola shown above has equation\n\n$$\n'+r'{y}^{2}='+tex(c)+'x.\n$$\n\n' if level=='easy' else '')+f'Find ${deriv}$ for the {direction}-opening parabola shown above.'
 if kind=='blank':prompt+=' Express the answer in terms of the variable $y.$\n\n$'+DY+'=$\n{{field-1}}'
 sol=solution_easy(c) if level=='easy' else solution(a,b,source,repair=mode not in ('raw','current'))
 present_solution=not(mode in ('raw','current') and ':question/worked-solution' not in q0)
 present_diff=not(mode in ('raw','current') and ':question/difficulty' not in q0)
 correct_present=not(mode in ('raw','current') and ':answer-field/correct' not in q0[':question/answer-fields'][0])
 # Presentation identity excludes seed, option order, profile aliases, and inputs
 # that did not change actual displayed content. Task identity is the curve.
 key='selection' if kind=='radio' else 'field-1'
 content={'version':VERSION,'prompt':prompt,'solution':sol if present_solution else None,'difficulty':level if present_diff else None,'field':kind,'key':key,'bank':sorted(tex(v) for v in vals),'correct':tex(answer) if correct_present else None}
 qid=uid(content);fid=uid([qid,key]);ads=[{':answer/id':uid([fid,tex(v)]),':answer/type':':answer.type/math',':answer/value':tex(v)} for v in vals]
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':ads}
 if correct_present:field[':answer-field/correct']=[':answer/id',uid([fid,tex(answer)])]
 if kind=='radio':rng.shuffle(ads)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':[field]}
 if present_solution:q[':question/worked-solution']=sol
 if present_diff:q[':question/difficulty']=':question.difficulty/'+level
 evidence_only=bool(source and kind=='radio') or mode=='raw'
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile or chosen,'parameters':p,'domain':'integer marked-point finite '+level,'assessment_mode':'given equation' if level=='easy' else 'reconstruct equation from plot','mathematical_fingerprint':digest(['given equation' if level=='easy' else 'reconstruct equation from plot','y²=cx',str(c)]),'dependencies':dependency_metadata(asset),'content_fingerprint':digest(content),'source_id':source,'origin':'raw observed evidence' if mode=='raw' else 'completed observed template' if source else 'authored same-method variation','evidence_only':evidence_only,'eligible_for_learning':not evidence_only,'recipes':recipes,'coefficient':str(c),'plot':asset,'source':{k:(CURRENT_SOURCES if mode=='current' else SOURCES)[k] for k in ('database','basis','lineage')},'difficulty_assignment':'authored missing easy' if level=='easy' else 'inferred unrated right/left alignment' if source in ('q-127372','q-127374') else 'observed right/moderate or left/hard scope'}}
# EASY: explicitly authored supplied equation; formal derivative/chain/isolation.
# Removing graph-to-p reconstruction separates its demand from moderate/hard.
def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
# MODERATE: positive integer marked points, rational p/c; observed right-opening.
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
# HARD: signed left-opening relation; same bounded arithmetic as observed sources.
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)
def markdown(r):
 q=r['question'];g=r['generation'];s=f"### {q.get(':question/difficulty','unrated raw evidence')} | {g['origin']} | {g['bank_profile']}\n\n"+q[':question/problem']+'\n\n'
 for f in q.get(':question/answer-fields',[]):
  correct=f.get(':answer-field/correct',[None,None])[1]
  for a in f[':answer-field/choices']:s+=('- [correct] ' if a[':answer/id']==correct else '- [unkeyed] ' if correct is None else '- ')+ '$'+a[':answer/value']+'$\n'
 return s+'\n'+q.get(':question/worked-solution','(Original has no worked solution.)')+'\n'
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1:ap.error('count must be positive')
 rows=[]
 for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]):
  candidates=domain(level);random.Random(args.seed).shuffle(candidates);selected=[];seen=set()
  for index,(a,b) in enumerate(candidates):
   task=digest(['given equation' if level=='easy' else 'reconstruct equation from plot','y²=cx',str(sp.Rational(b*b,a))])
   if task in seen:continue
   try:r=generate(level,args.seed+index,template=args.template,profile=args.profile,parameters={'a':a,'b':b})
   except ValueError:continue
   selected.append(r);seen.add(task)
   if len(selected)==args.count:break
  if len(selected)<args.count:ap.error(f'finite-limit: {level} profile has only {len(selected)} distinct valid tasks; requested {args.count}')
  rows.extend(selected)
 print(json.dumps(rows,indent=2) if args.format=='json' else '\n'.join(map(markdown,rows)))
