#!/usr/bin/env python3
"""KP 17592186087823: recognize a shifted/stretched growth curve or its intercept.

Captured math basis 1356; never writes EDB. Source fidelity precedes the authored
banks; historical scalar distractor interpretations and ungridded curve bases are
not inferred. Raw replay profiles preserve missing attributes. See the evidence
folder for complete banks, extraction, source geometry, scope and native grading.

Easy: integer-coefficient graph selection. Moderate: the observed intercept method,
integer/half-integer arithmetic. Hard: authored graph selection with nonintegral
half-integer stretch AND shift, retaining the same three transformation steps.
Within a level all instances have equal workload; no parameter recovery is asked.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as sp

KP_ID=17592186087823
KP_UUID='40eeb5a8-3ffe-54d2-b263-f2b1c41fed93'
TITLE='Identifying a Vertically Shifted and Stretched Exponential Growth Curve'
VERSION='shift-stretch-growth-v4'
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
QUESTIONS=SOURCE['record'][':knowledge-point/questions']
BASES=('1.5','2','3','4','6','10')
PROFILES={
 'graph_unrated':('graph','q-26910',('growth_zero','reverse_input','reverse_asym_omit_stretch','scale_asym_reverse_curve','correct')),
 'intercept_base':('intercept','q-30270',('base_plus_scale','transpose_base_plus_scale','base_times_shift','correct','transpose_correct')),
 'intercept_components':('intercept','q-170594',('shift','scale','base','correct','double_correct')),
 'intercept_swap':('intercept','q-30269',('successor','transpose_correct','correct','shift_minus_scale','transpose_shift_minus_scale')),
 'intercept_signed':('intercept','q-30873',('negative_base','negative_correct','correct','successor','base')),
 'graph_observed':('graph','q-7121',('reverse_input','omit_stretch','reverse_asym_preserve_intercept','correct','horizontal_shift')),
 'graph_authored':('graph',None,('reverse_input','omit_stretch','reverse_asym_preserve_intercept','correct','horizontal_shift')),
 'intercept_authored':('intercept',None,('correct','transpose_correct','scale','shift','scale_minus_shift')),
}
for presentation in ('comma','axis'):
 PROFILES['intercept_authored_'+presentation]=PROFILES['intercept_authored']
PRESENTATIONS={'intercept':'intercept_authored','intercept_comma':'intercept_authored_comma','intercept_axis':'intercept_authored_axis'}

PARAMETERS={
 'q-26910':{'k':'4','b':'6','c':'-2'},'q-30270':{'k':'5','b':'6','c':'2'},
 'q-170594':{'k':'1.5','b':'4','c':'1'},'q-30269':{'k':'2.5','b':'1.5','c':'8'},
 'q-30873':{'k':'1.5','b':'10','c':'-8.5'},'q-7121':{'k':'2','b':'3','c':'-4'},
}
class Rejected(ValueError): pass

def number(v):
 v=sp.Rational(v)
 if v.q not in (1,2): raise ValueError('Only integers and exact halves are supported')
 return str(v.p) if v.q==1 else str(float(v))
def sign(c): return ('+' if c>=0 else '-')+number(abs(c))
def formula(k,b,c,power='x'):
 return number(k)+'({'+number(b)+'}^{'+power+'})'+sign(c)
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x): return str(uuid.uuid5(uuid.NAMESPACE_URL,'kp:'+str(KP_ID)+':'+x))
def source_question(profile):
 return next(q for q in QUESTIONS if q[':question/math-academy-id']==PROFILES[profile][1])

def parameters_ok(level,p,raw=False):
 if set(p)!={'k','b','c'}: raise ValueError('Exactly k, b and c required')
 k,b,c=(sp.Rational(p[n]) for n in ('k','b','c'))
 if b<=1 or number(b) not in BASES or k<=1 or abs(c)>sp.Rational(17,2) or c==0: raise Rejected('Outside supported growth/stretch/shift domain')
 if k>8: raise Rejected('Stretch exceeds source-grounded arithmetic ceiling')
 if not raw:
  if level=='easy' and (k.q!=1 or c.q!=1 or not 2<=k<=8 or abs(c)>8): raise Rejected('Easy requires integer stretch and shift')
  if level=='moderate' and (not sp.Rational(3,2)<=k<=8 or k.q not in (1,2) or c.q not in (1,2)): raise Rejected('Moderate bounded integer/half arithmetic')
  if level=='hard' and (k.q!=2 or c.q!=2 or not sp.Rational(3,2)<=k<=sp.Rational(13,2)): raise Rejected('Hard requires nonintegral half-integer stretch and shift')
 return k,b,c

def curve_bank(k,b,c,recipes):
 # Every member is a complete curve, plus its own labelled point. Base is fixed
 # to the prompt for authored plots; source distractor bases remain uncertain.
 curves={
 'correct':(k,b,c,0,1,0),'reverse_input':(k,b,c,0,-1,0),
 'omit_stretch':(sp.Integer(1),b,c,0,1,0),
 'reverse_asym_preserve_intercept':(k+2*c,b,-c,0,1,0),
 'horizontal_shift':(k,b,c,k,1,k),
 'growth_zero':(k+c,b,0,0,1,0),
 'reverse_asym_omit_stretch':(k+c,b,-c,0,1,0),
 'scale_asym_reverse_curve':(c-k,b,k,0,1,0),
 }
 out=[]
 for recipe in recipes:
  a,base,d,h,s,mx=curves[recipe]
  if a==0: raise Rejected('Constant curve in complete bank')
  my=a*base**(s*(mx-h))+d
  out.append({'recipe':recipe,'a':str(a),'b':str(base),'c':str(d),'h':str(h),'s':s,'mark':[str(mx),str(my)]})
 # Canonical monomial coefficient absorbs a horizontal translation. Comparing
 # complete (exponent sign, coefficient, asymptote) objects is exact and avoids
 # numeric curve approximation as an ambiguity check.
 signatures=[(o['s'],sp.simplify(sp.Rational(o['a'])*b**(-o['s']*sp.Rational(o['h']))),sp.Rational(o['c'])) for o in out]
 if len(set(signatures))!=5: raise Rejected('Equivalent complete curves')
 return out

def intercept_bank(k,b,c,recipes):
 v=k+c
 values={'correct':(0,v),'transpose_correct':(v,0),'scale':(0,k),'shift':(0,c),
 'scale_minus_shift':(0,k-c),'base_plus_scale':(0,b+k),'transpose_base_plus_scale':(b+k,0),
 'base_times_shift':(0,b*c),'base':(0,b),'double_correct':(0,2*v),'successor':(0,v+1),
 'shift_minus_scale':(0,c-k),'transpose_shift_minus_scale':(c-k,0),'negative_base':(0,-b),'negative_correct':(0,-v)}
 out=[{'recipe':r,'value':'('+number(values[r][0])+','+number(values[r][1])+')'} for r in recipes]
 if len({o['value'] for o in out})!=5: raise Rejected('Collision in complete point bank')
 return out

def render_curves(curves):
 HERE.joinpath('plots').mkdir(exist_ok=True)
 requested=[]
 for curve in curves:
  spec={'renderer_version':VERSION,'curve':curve,'style':'source-ungridded-marked-features'}
  key=digest(spec);path=HERE/'plots'/(key+'.png');side=path.with_suffix('.json')
  if not (path.exists() and side.exists()): requested.append({'path':str(path),'spec':spec})
 if requested:
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='render-',dir=HERE/'plots',delete=False) as f:
   json.dump(requested,f);inp=Path(f.name)
  try: subprocess.run([sys.executable,str(HERE/'render.py'),str(inp)],check=True,capture_output=True,text=True)
  finally: inp.unlink(missing_ok=True)
 return [str(HERE/'plots'/(digest({'renderer_version':VERSION,'curve':curve,'style':'source-ungridded-marked-features'})+'.png')) for curve in curves]

def graph_solution(k,b,c,paths):
 v=k+c;direction='up' if c>0 else 'down'; units='unit' if abs(c)==1 else 'units'
 return ('First, we plot the graph of $y={'+number(b)+'}^{x}:$\n\n![]('+paths[0]+')\n\n'
 'Next, we plot the graph of $y='+number(k)+'({'+number(b)+'}^{x}).$ To do this, we scale the graph above by a factor of $'+number(k)+'.$ The $y$-intercept moves from $(0,1)$ to $(0,'+number(k)+'),$ but the horizontal asymptote stays at $y=0.$\n\n![]('+paths[1]+')\n\n'
 'Finally, we plot the graph of $y='+formula(k,b,c)+'.$ To do this, we shift the above graph $'+number(abs(c))+'$ '+units+' '+direction+'. The $y$-intercept moves from $(0,'+number(k)+')$ to $(0,'+number(v)+'),$ and the horizontal asymptote moves from $y=0$ to $y='+number(c)+'.$\n\n![]('+paths[2]+')')

def intercept_solution(k,b,c,profile):
 v=k+c;equ=formula(k,b,c)
 # Complete formal substitution, evaluated exponential, product, sum, conclusion.
 comma=',' if profile in ('intercept_components','intercept_authored_comma') else ''
 return ('**Method 1**\n\n- For the curve $y={'+number(b)+'}^{x},$ the point of intersection with the $y$-axis is $(0,1).$\n\n'
 '- For the scaled function $y='+number(k)+'({'+number(b)+'}^{x}),$ the $y$-coordinate becomes\n\n$$\ny='+number(k)+'\\cdot 1='+number(k)+'.\n$$\n\n'
 '- Finally, after a vertical shift of $'+number(abs(c))+'$ '+('unit' if abs(c)==1 else 'units')+' '+('up' if c>0 else 'down')+', we get a point with the $y$-coordinate\n\n$$\ny='+number(k)+sign(c)+'='+number(v)+'.\n$$\n\n'
 '**Method 2** \n\nTo find the $y$-intercept, we substitute $x=0$ into the equation of the curve:\n\n$$\n\\begin{aligned}y & ='+formula(k,b,c,'0')+' \\\\  & ='+number(k)+'\\cdot 1'+sign(c)+' \\\\  & ='+number(k)+sign(c)+' \\\\  & ='+number(v)+'\\end{aligned}\n$$\n\n'
 'Therefore, $y='+equ+comma+'$ intercepts the $y$-axis at $(0,'+number(v)+').$')

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'): raise ValueError('Unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only source radio fields supported')
 rng=random.Random(seed)
 if profile is None:
  profile=(PRESENTATIONS[template] if template in PRESENTATIONS else rng.choice(tuple(PRESENTATIONS.values()))) if level=='moderate' else 'graph_authored'
 if profile not in PROFILES: raise ValueError('Unknown profile')
 kind,source_id,recipes=PROFILES[profile]
 if template not in (None,kind) and not (template in PRESENTATIONS and PRESENTATIONS[template]==profile): raise ValueError('Profile/template mismatch')
 raw=source_id is not None
 if raw:
  source=source_question(profile);source_level=source.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or 'easy'
  if level!=source_level: raise ValueError('Raw source level mismatch; unrated graph assigned easy only in author metadata')
 elif kind!=('intercept' if level=='moderate' else 'graph'): raise ValueError('Authored level/template boundary')
 for attempt in range(200):
  if parameters is not None: p={n:number(v) for n,v in parameters.items()}
  elif raw: p=dict(PARAMETERS[source_id])
  elif level=='easy': p={'k':str(rng.randint(2,8)),'b':rng.choice(BASES),'c':str(rng.choice([i for i in range(-8,9) if i]))}
  elif level=='moderate': p={'k':number(sp.Rational(rng.randint(3,16),2)),'b':rng.choice(BASES),'c':number(sp.Rational(rng.choice([i for i in range(-17,18) if i]),2))}
  else: p={'k':number(sp.Rational(rng.choice(range(3,14,2)),2)),'b':rng.choice(BASES),'c':number(sp.Rational(rng.choice([i for i in range(-17,18,2) if i]),2))}
  try:
   k,b,c=parameters_ok(level,p,raw)
   correct=k+c  # Compute answer before constructing any complete bank.
   bank=curve_bank(k,b,c,recipes) if kind=='graph' else intercept_bank(k,b,c,recipes)
   break
  except Rejected:
   if parameters is not None or raw: raise
 else: raise Rejected('No eligible whole instance')
 raw_original=raw and p==PARAMETERS[source_id]
 if kind=='graph':
  if raw_original:
   extracted=json.loads((HERE/'source-geometry.json').read_text())['plots']
   assets={o['recipe']:o for o in extracted if o.get('profile')==profile}
   values=[]
   for curve in bank:
    evidence=assets[curve['recipe']]
    if evidence['marked_point']!=curve['mark'] or evidence['asymptote']!=curve['c']: raise ValueError('Source raster feature recipe mismatch')
    values.append(evidence['path'])
  else: values=render_curves(bank)
  if raw_original and ':question/worked-solution' in source:
   solution_paths=re.findall(r'!\[\]\(([^)]+)\)',source[':question/worked-solution'])
  else:
   stages=[{'recipe':'stage','a':str(a),'b':str(b),'c':str(d),'h':'0','s':1,'mark':['0',str(a+d)]} for a,d in ((1,0),(k,0),(k,c))]
   solution_paths=render_curves(stages) if not (raw and ':question/worked-solution' not in source) else []
  solution=graph_solution(k,b,c,solution_paths) if solution_paths else None
  problem='Which of the following is the graph of $y='+formula(k,b,c)+'?$'
  if profile=='graph_unrated': problem='Which of the following is the graph of $y = '+number(k)+'('+number(b)+'^{x}) '+('-' if c<0 else '+')+' '+number(abs(c))+'$?'
 else:
  values=[o['value'] for o in bank];solution=intercept_solution(k,b,c,profile)
  if profile in ('intercept_swap','intercept_signed','intercept_authored_axis'): problem='For the curve $y='+formula(k,b,c)+'$, find the point of intersection with the $y-$axis.'
  else: problem='For the curve $y='+formula(k,b,c)+',$ find the point of intersection with the $y$-axis.'
 visible_level=source.get(':question/difficulty',{}).get(':db/ident') if raw else ':question.difficulty/'+level
 # Mathematical fingerprint excludes incidental base, bank and spelling. Shape is
 # recognized by transformation features; b>1 makes all eligible bases growth.
 task=digest({'kind':kind,'k':str(k),'c':str(c),'level':visible_level or 'unrated'})
 content=digest({'version':VERSION,'prompt':problem,'solution':solution,'bank':sorted(values),'level':visible_level})
 field_id=uid(content+':selection');answers=[{':answer/id':uid(field_id+':'+v),':answer/type':':answer.type/'+('image' if kind=='graph' else 'math'),':answer/value':v} for v in values]
 correct_idx=recipes.index('correct');correct_id=answers[correct_idx][':answer/id']
 rng.shuffle(answers)
 field={':answer-field/id':field_id,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if not raw or ':answer-field/correct' in source[':question/answer-fields'][0]: field[':answer-field/correct']=[':answer/id',correct_id]
 question={':question/id':uid(content),':question/problem':problem,':question/answer-fields':[field]}
 if visible_level: question[':question/difficulty']=visible_level
 if solution is not None: question[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':question,
 'generation':{'version':VERSION,'python_version':sys.version.split()[0],'sympy_version':sp.__version__,'seed':seed,'parameters':p,'template':next((t for t,pf in PRESENTATIONS.items() if pf==profile),kind),'bank_profile':profile,'recipes':list(recipes),'bank_geometry':bank if kind=='graph' else None,'parameter_fingerprint':task,'content_fingerprint':content,'source':{n:SOURCE[n] for n in ('database','basis','lineage')},'source_id':source_id,'raw_source_replay':raw,'evidence_only':raw,'eligible_for_learning':not raw,'authored_extension':not raw,'difficulty_design':level,'inferred_correct_recipe':'correct' if profile=='graph_unrated' else None,'original_asset_reuse':raw_original and kind=='graph','base_identification':'prompt base used in authored curves; ungridded source distractor bases unresolved' if kind=='graph' else 'incidental to x=0'}}

# EASY — integer graph recognition, three transformation stages.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE — observed y-intercept calculation; two source methods retained.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)
# HARD — authored fractional graph recognition, same scope and stage count.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r,label='Generated'):
 q,g=r['question'],r['generation'];f=q[':question/answer-fields'][0]
 lines=['## '+label+' — '+q.get(':question/difficulty','unrated').split('/')[-1], 'Profile: `'+g['bank_profile']+'`; '+('raw source evidence' if g['evidence_only'] else 'authored extension')+'.','',q[':question/problem'],'']
 for letter,a in zip('ABCDE',f[':answer-field/choices']):
  mark=' **Correct**' if f.get(':answer-field/correct',[None,None])[1]==a[':answer/id'] else ''
  display_value=str(Path('/media/jake/SSD/EDB/math')/a[':answer/value']) if a[':answer/value'].startswith('images/') else a[':answer/value']
  val='![]('+display_value+')' if a[':answer/type'].endswith('/image') else '$'+a[':answer/value']+'$'
  lines += ['**'+letter+'.**'+mark+' '+val,'']
 if ':answer-field/correct' not in f: lines+=['Original correct designation absent; independently inferred correct graph is recorded in author metadata.','']
 preview_solution=q.get(':question/worked-solution','Absent in original evidence.')
 preview_solution=re.sub(r'!\[\]\((images/[^)]+)\)',lambda m:'![]('+str(Path('/media/jake/SSD/EDB/math')/m.group(1))+')',preview_solution)
 lines+=['**Worked solution**','',preview_solution]
 return '\n'.join(lines)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=('json','markdown'),default='markdown');ap.add_argument('--template',choices=('graph',*PRESENTATIONS));ap.add_argument('--profile',choices=tuple(PROFILES));args=ap.parse_args()
 if args.count<1: ap.error('count must be positive')
 levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
 try: records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 except ValueError as e: ap.error(str(e))
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
