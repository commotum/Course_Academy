#!/usr/bin/env python3
"""Finite conceptual generator for Describing Properties of the Cosine Function.

Captured math basis 1356; no database imports or writes. Extracted source masks
are in 17592186176047/recipes.json. Their complete categorical banks are explicit
observed profiles, never a pool of distractors. The masks have mathematical slots
(angle, family, interval, output); all normal answers follow exact truth tests.
Source solutions retain all captured sentences and mathematical stages. Missing
keys/solutions are derived/ authored separately and never count as exact fidelity.
The sine mislink remains in explicit observed replay; normal blank generation
repairs the function to cosine. Captured blank values have valid single slashes.

All graphs show the SAME untransformed function, so changing a claim does not
change geometry. The three original rasters were inspected and may be reused;
no new plot renderer is necessary (plot rating none: unchanged assets).

Meaningful variety is finite: easy 32, moderate 72, hard 216 semantic claim sets.
No coefficients, variable aliases, reordered statements or bank profiles inflate
these counts. Easy/Hard are authored missing-level labels, not observed labels.
Hard tests COMPLETE sets of zeros/extrema, not periodicity/evenness calculations.
CLI: --difficulty easy|moderate|hard|all --seed N --count N --format markdown|json.
"""
from __future__ import annotations

# Standalone source eligibility: immutable policy ledger, seeded CLI guard.
import sys as _ca_sys, os as _ca_os
from pathlib import Path as _ca_Path
_ca_sys.path.insert(0,str(_ca_Path(__file__).resolve().parent))
if __name__ == "__main__" and not _ca_os.environ.get("_CA_SOURCE_POLICY_CHILD"):
    from ca_source_runtime import cli as _ca_source_cli
    _ca_source_cli(__file__,_ca_Path(__file__).with_name('17592186176047-source-policy.json'))
    raise SystemExit(0)

import argparse, hashlib, itertools, json, random, re, uuid
from pathlib import Path
import sympy as sp
from math_format import normalize_prose,normalize_tex

KP_ID=17592186176047
KP_UUID='542df339-5020-5680-a39c-a1ae161083e7'
TITLE='Describing Properties of the Cosine Function'
VERSION='cosine-properties-checkbox-finite-2-format-audit-9122-v1'
HERE=Path(__file__).resolve().with_suffix('')
RECIPES=json.loads((HERE/'recipes.json').read_text())
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
COS='images/88/88378ece5b1721cdc533d07d69c004901539c7f8fda9a5a3e5c5648ed32905c5.png'
SIN='images/96/96bd60d23237f836b77a26c5c0461a5c2a474554f0a14266b53fc5e7d999f1b7.png'
PLOT=str(HERE/'assets/cosine.png')
ROMAN=('I','II','III')
TEMPLATES={**{k:{'level':'moderate','kind':'blank' if k=='q-167631' else 'radio','origin':'observed'} for k in RECIPES},
 'local_facts':{'level':'easy','kind':'radio','origin':'authored'},
 'mixed_properties':{'level':'moderate','kind':'radio','origin':'authored'},
 'complete_families':{'level':'hard','kind':'radio','origin':'authored'}}
BANK_PROFILES={**{'observed-'+k:k for k in RECIPES},'authored-local':'local_facts','authored-mixed':'mixed_properties','authored-families':'complete_families','repaired-cosine-facts':'q-167631'}

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def number(x):
 s=sp.sympify(x)
 if not (s.is_Rational or s in (sp.pi,-sp.pi)): raise ValueError('Only catalog rational numbers or ±pi are eligible')
 return s

def numtex(x): return sp.latex(number(x)).replace('- ', '-')
def angle(value,style='compact'):
 v=sp.Rational(value); pi='π' if style=='unicode' else r'\pi'+(' ' if style.startswith('space') else '')
 if v==0: return '0'
 sign='-' if v<0 else '';a=abs(v);n,d=a.as_numer_denom()
 prefix='' if n==1 else str(n)
 return sign+(prefix+pi if d==1 else r'\frac{'+prefix+pi+'}{'+str(d)+'}')
def family(offset,step,style='compact'):
 v=sp.Rational(offset);st=int(step);space=' + ' if style=='unicode' else '+'
 pi='π' if style=='unicode' else r'\pi'+(' ' if style.startswith('space') else '')
 tail=('' if st==1 else str(st))+'n'+pi
 return (angle(v,style)+space if v else '')+tail+('.' if style=='spaceperiod' else '')
def interval(low,high,style='compact'):
 def item(v):
  val=number(v)
  if abs(val)==sp.pi:
   return ('- ' if val<0 and style=='unicode' else '-' if val<0 else '')+('π' if style=='unicode' else r'\pi'+(' ' if style=='space' else ''))
  return ('- ' + str(abs(val)) if style=='unicode' and val<0 else numtex(val))
 return '['+item(low)+(','+' ' if style=='unicode' else ',')+item(high)+']'
def slot(spec,p):
 kind=spec['kind'];style=spec['style']
 if kind=='angle': return angle(p['value'],style)
 if kind=='family': return family(p['offset'],p['step'],style)
 if kind=='range': return interval(p['low'],p['high'],style)
 return numtex(p['value'])
def render_mask(mask,recipe,p):
 if mask is None:return None
 for spec in recipe['slots']:mask=mask.replace('@@'+spec['name']+'@@',slot(spec,p[spec['name']]))
 if '@@function@@' in mask: mask=mask.replace('@@function@@',p['function']+'⁡x').replace('@@plot@@',SIN if p['function']=='sin' else COS)
 if '@@' in mask:raise ValueError('Unrendered slot')
 return mask

def family_truth(kind,offset,step):
 """Completeness matters: a subset of zeros is not THE full zero set."""
 o=sp.Rational(offset);s=sp.Integer(step)
 if kind=='zero_family':return bool(s==1 and (o-sp.Rational(1,2)).is_integer)
 if kind=='max_family':return bool(s==2 and (o/2).is_integer)
 if kind=='min_family':return bool(s==2 and ((o-1)/2).is_integer)
 raise ValueError(kind)

def truth(c):
 kind=c['kind']
 if kind.endswith('_family'):return family_truth(kind,c['offset'],c['step'])
 if kind in ('zero','max','min'):
  y=sp.cos(sp.Rational(c['value'])*sp.pi)
  return bool(y=={'zero':0,'max':1,'min':-1}[kind])
 if kind=='intercept':return number(c['value'])==1
 if kind=='range':return number(c['low'])==-1 and number(c['high'])==1
 if kind=='output':return bool(-1<=number(c['value'])<=1)
 if kind=='point':return sp.cos(sp.Rational(c['x'])*sp.pi)==number(c['y'])
 raise ValueError(kind)

def semantics(c):
 """Equivalent shifts/family parameterizations and claim ordering deduplicate."""
 d=dict(c)
 if 'offset' in d:d['offset']=str(sp.Rational(d['offset'])%int(d['step']))
 if d['kind'] in ('zero','max','min'):d['value']=str(sp.Rational(d['value'])%2)
 if d['kind']=='point':d['x']=str(sp.Rational(d['x'])%2)
 if d['kind']=='range':
  # Only relative endpoint position affects this categorical assessment.
  # Oversized bounds 2, 3 and pi are presentation variants of one task.
  d={'kind':'range','low_position':str(sp.sign(number(d['low'])+1)),'high_position':str(sp.sign(number(d['high'])-1))}
 if d['kind']=='output':
  v=number(d['value']);d={'kind':'output','position':'below' if v < -1 else 'above' if v > 1 else 'within'}
 return d

def text(c):
 k=c['kind']
 if k=='zero':return 'The function is zero at $x='+angle(c['value'])+'.$'
 if k in ('max','min'):return 'The function has a '+('maximum' if k=='max' else 'minimum')+' value at $x='+angle(c['value'])+'.$'
 if k.endswith('_family'):
  tag={'zero_family':'zeros','max_family':'maximum values','min_family':'minimum values'}[k]
  return 'The complete set of inputs at which the function has '+tag+' is $x='+family(c['offset'],c['step'])+'.$'
 if k=='range':return 'The range of the function is $'+interval(c['low'],c['high'])+'.$'
 if k=='output':return '$y='+numtex(c['value'])+'$ is an output of the function.'
 if k=='intercept':return 'The graph intersects the $y$-axis at $y='+numtex(c['value'])+'.$'
 if k=='point':return 'The graph passes through $('+angle(c['x'])+','+numtex(c['y'])+')$.'
 raise ValueError(k)

def explanation(c):
 k=c['kind']
 if k.endswith('_family'):
  return {'zero_family':r'The zeros occur at $x=\frac{\pi}{2}+n\pi$. Every zero must be included.',
   'max_family':r'The maximum value is $1$, attained at $x=2n\pi$. Every maximum input must be included.',
   'min_family':r'The minimum value is $-1$, attained at $x=\pi+2n\pi$. Every minimum input must be included.'}[k]
 if k in ('zero','max','min','point'):
  a=c['x'] if k=='point' else c['value']; y=sp.cos(sp.Rational(a)*sp.pi)
  return '$\\cos('+angle(a)+')='+sp.latex(y)+'$.'
 if k=='intercept':return r'At $x=0$, the function has value $\cos 0=1$.'
 if k in ('range','output'):return r'The minimum value is $-1$ and the maximum value is $1$. The range is $[-1,1]$.'
 raise ValueError(k)

def subset_label(bits):
 vals=[ROMAN[i] for i,b in enumerate(bits) if b]
 if not vals:return 'None of the statements'
 if len(vals)==3:return 'I, II, and III'
 return (vals[0] if len(vals)==1 else ' and '.join(vals))+' only'
def parse_label(label):return tuple(r in re.findall(r'\bI{1,3}\b',label) for r in ROMAN)

def source_claims(name,p):
 def claim(key):return {'kind':key,**p[key]}
 if name=='q-27015':return [claim('max_family'),claim('zero'),claim('range')]
 if name=='q-27021':return [claim('zero_family'),claim('max_family'),claim('range')]
 if name=='q-103230':return [claim('zero'),claim('range'),claim('output')]
 if name=='q-103233':return [claim('zero_family'),{'kind':'point','x':'0','y':'1'},claim('max_family')]
 if name=='q-27009':return [claim('zero'),claim('min'),{'kind':'intercept','value':'0'}]
 if name=='q-70666':return [claim('max_family'),claim('zero'),claim('range')]
 if name=='q-70667':return [{'kind':'intercept','value':'1'},claim('min'),claim('range')]
 return []

# EASY: three independent local facts, same three unit-graph readings each time.
# Four distinct landmarks each have exactly one true and one false claim.
# Choosing three distinct landmarks prevents duplicate demands at one point.
EASY_CATALOG={
 'origin':[{'kind':'intercept','value':'1'},{'kind':'intercept','value':'0'}],
 'quarter':[{'kind':'zero','value':'1/2'},{'kind':'max','value':'1/2'}],
 'half':[{'kind':'min','value':'1'},{'kind':'max','value':'1'}],
 'three_quarter':[{'kind':'zero','value':'3/2'},{'kind':'min','value':'3/2'}]}

def authored_catalog(level):
 if level=='easy':
  return [{'claims':[dict(c) for c in items]} for cats in itertools.combinations(EASY_CATALOG,3) for items in itertools.product(*(EASY_CATALOG[c] for c in cats))]
 if level=='moderate':
  # One local zero claim, one completeness claim, one range claim, always.
  return [{'claims':[{'kind':'zero','value':str(a)}, {'kind':'max_family','offset':str(b),'step':step}, {'kind':'range','low':low,'high':high}]}
   for a in ('0','1/2','1','3/2') for b,step in FAMILY_SHAPES for low,high in (('-1','1'),('-2','2'),('-1','0'))]
 if level=='hard':
  return [{'claims':[{'kind':k,'offset':str(o),'step':s} for k,(o,s) in zip(('zero_family','max_family','min_family'),shapes)]} for shapes in itertools.product(FAMILY_SHAPES,repeat=3)]
 raise ValueError(level)
# Six DISTINCT sets after reducing offsets modulo family step. No shifting
# by the family period creates another task. These are unordered same-workload
# alternatives, not a progression. Step 2 zero sets assess subset completeness.
FAMILY_SHAPES=(('0',1),('1/2',1),('0',2),('1/2',2),('1',2),('3/2',2))

# MODERATE: captured slots constrained to the captured sentence truth pattern.
SOURCE_TRUTHS={'q-27015':(False,True,False),'q-27021':(True,False,False),'q-103230':(True,False,False),'q-103233':(False,True,False),'q-27009':(True,False,False),'q-70666':(False,True,False),'q-70667':(True,True,False)}
SOURCE_DEFAULTS={case['template']:case['parameters'] for case in json.loads((HERE/'source-cases.json').read_text())}

def validate_parameters(name,p,level,profile):
 if name in RECIPES:
  if set(p)!=set(SOURCE_DEFAULTS[name]):raise ValueError('Explicit source parameters require all and only documented slots')
  if name=='q-167631':
   if p['function'] not in ('sin','cos'):raise ValueError('Only untransformed sine evidence or corrected cosine is allowed')
   if profile!='observed-q-167631' and p['function']!='cos':raise ValueError('Normal properties questions must assess cosine')
   return
  for slot_spec in RECIPES[name]['slots']:
   v=p[slot_spec['name']];kind=slot_spec['kind']
   expected={'angle':{'value'},'number':{'value'},'range':{'low','high'},'family':{'offset','step'}}[kind]
   if set(v)!=expected:raise ValueError('Invalid mathematical slot shape')
   if kind=='family':
    if (str(sp.Rational(v['offset'])),v['step']) not in FAMILY_SHAPES:raise ValueError('Only documented finite family shapes are allowed')
   elif kind=='angle':
    if str(sp.Rational(v['value'])) not in ('-2','-3/2','-1','-1/2','0','1/2','1','3/2','2'):raise ValueError('Angle is outside unit-graph reading bounds')
   elif kind=='number':
    if str(number(v['value'])) not in ('-2','-3/2','3/2','2'):raise ValueError('Source output claim must be outside the range with familiar rational magnitude')
   else:
    if (str(number(v['low'])),str(number(v['high']))) not in (('-1','0'),('-2','2'),('-3','3'),('-pi','pi')):raise ValueError('Only captured/supported incorrect range shapes are allowed')
  if tuple(map(truth,source_claims(name,p)))!=SOURCE_TRUTHS[name]:raise ValueError('These parameters change the source solution truth pattern')
 else:
  canonical={digest(x) for x in authored_catalog(level)}
  if digest(p) not in canonical:raise ValueError('Explicit parameters must belong to the finite authored workload catalog')

def source_sample(name,rng):
 p=json.loads(json.dumps(SOURCE_DEFAULTS[name]))
 if name=='q-167631':return {'function':'cos'}
 for spec in RECIPES[name]['slots']:
  key=spec['name'];kind=spec['kind']
  if kind=='angle':
   old=sp.Rational(p[key]['value']); options=[str(x) for x in (sp.Rational(-3,2),sp.Rational(-1,2),sp.Rational(1,2),sp.Rational(3,2))] if old.q==2 else [str(x) for x in (-2,0,2)] if old%2==0 else ['-1','1']
   p[key]['value']=rng.choice(options)
  elif kind=='range':
   hi=rng.choice(('2','3','pi','0'));p[key]={'low':'-1','high':'0'} if hi=='0' else {'low':'-'+hi,'high':hi}
  elif kind=='number':p[key]={'value':rng.choice(('-2','-3/2','3/2','2'))}
  elif kind=='family' and sp.Rational(p[key]['offset']).q==2 and p[key]['step']==2:p[key]['offset']=rng.choice(('1/2','3/2'))
 return p

# HARD: exactly three complete-family claims, one each for zeros/maxima/minima.
def _generate_legacy(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if profile is not None:
  if profile not in BANK_PROFILES:raise ValueError('Unknown complete bank profile')
  implied=BANK_PROFILES[profile]
  if template is not None and template!=implied:raise ValueError('Profile/template mismatch')
  template=implied
 name=template or {'easy':'local_facts','moderate':'mixed_properties','hard':'complete_families'}[level]
 if name not in TEMPLATES or TEMPLATES[name]['level']!=level:raise ValueError('Template does not belong to requested level')
 kind=TEMPLATES[name]['kind']
 if field_type is not None and kind!=field_type:raise ValueError('Answer field type mismatch')
 profile=profile or ('repaired-cosine-facts' if name=='q-167631' else 'observed-'+name if name in RECIPES else {'easy':'authored-local','moderate':'authored-mixed','hard':'authored-families'}[level])
 rng=random.Random(seed)
 p=json.loads(json.dumps(parameters)) if parameters is not None else source_sample(name,rng) if name in RECIPES else rng.choice(authored_catalog(level))
 validate_parameters(name,p,level,profile)
 raw=profile.startswith('observed-')
 if name in RECIPES:
  recipe=RECIPES[name];prompt=render_mask(recipe['prompt_mask'],recipe,p);solution=render_mask(recipe['solution_mask'],recipe,p);claims=source_claims(name,p)
 else:
  claims=p['claims'];prompt='Which of the following statements are true regarding the function $y=\\cos x$?'+(' Assume that $n$ is an integer.' if level in ('moderate','hard') else '')+'\n\n'+'\n\n'.join(r+'. '+text(c) for r,c in zip(ROMAN,claims))
  solution=None
 bits=tuple(map(truth,claims))
 if solution is None:
  solution="Let's plot the graph of $y=\\cos x$.\n\n![]("+PLOT+")\n\nLet's go through each statement.\n\n"+'\n\n'.join('- Statement '+r+' is '+('true' if t else 'false')+'. '+explanation(c) for r,t,c in zip(ROMAN,bits,claims))
 if not raw:solution=solution.replace(COS,PLOT).replace('images/9c/9c77bec4ebb04668fbff5176418ed9c09143a8660879fdf523a158c5f109006c.png',str(HERE/'assets/cosine-extrema.png'))
 fields=[]
 if kind=='blank':
  # Preserve observed answer whitespace in the explicit replay profile.
  values={'field-1':r'-\infty ' if raw else r'-\infty','field-2':r'\infty ' if raw else r'\infty','field-3':'-1','field-4':'1','field-5':r'2\pi ' if raw else r'2\pi'}
  for key in ('field-3','field-5','field-2','field-4','field-1'):fields.append((key,'math',[values[key]],values[key]))
 else:
  correct=subset_label(bits)
  if name in RECIPES:bank=list(RECIPES[name]['bank'])
  else:
   # Five complete categorical outcomes: correct plus four deterministic wrong
   # subsets. No numerical perturbation or per-option first-valid fallback.
   wrong=[subset_label(b) for b in itertools.product((False,True),repeat=3) if b!=bits]
   bank=[correct]+sorted(wrong,key=lambda v:digest({'claims':sorted([semantics(c) for c in claims],key=digest),'subset':v}))[:4]
  if len(bank)!=5 or len(set(bank))!=5 or bank.count(correct)!=1:raise ValueError('Reject whole instance: incomplete/ambiguous bank')
  fields=[('selection','text',bank,correct)]
 fingerprint=digest({'function':p.get('function','cos') if raw else 'cos','claims':sorted([semantics(c) for c in claims],key=digest),'facts':('domain','range','period') if kind=='blank' else None})
 content=digest({'version':VERSION,'prompt':prompt,'solution':solution,'fields':[(key,typ,sorted(vals),cor) for key,typ,vals,cor in fields]})
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content)); out=[]
 for key,typ,values,correct in fields:
  fid=str(uuid.uuid5(uuid.UUID(qid),key));answers=[];cid=None
  for value in values:
   aid=str(uuid.uuid5(uuid.UUID(fid),value));answers.append({':answer/id':aid,':answer/type':':answer.type/'+typ,':answer/value':value})
   if value==correct:cid=aid
  if kind=='radio':rng.shuffle(answers)
  out.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':out},'generation':{'version':VERSION,'seed':seed,'template':name,'bank_profile':profile,'parameters':p,'parameter_fingerprint':fingerprint,'mathematical_task_fingerprint':fingerprint,'content_fingerprint':content,'source_analysis':SOURCE,'source_ids':[name] if name in RECIPES else [],'authored_extension':name not in RECIPES,'source_repairs':(['sine mislink to cosine'] if name=='q-167631' and not raw else ['missing correct designation inferred','missing solution authored'] if name in ('q-27015','q-27021') else []),'plot_rating':'none','plot_assets':{'solution':re.findall(r'!\[\]\((.*?)\)',solution)},'claims':claims,'truth_vector':list(bits),'catalog_task_count':{'easy':32,'moderate':72,'hard':216}[level] if name not in RECIPES else None,'sympy_version':sp.__version__}}

# Current source migration: three owned boolean checkbox fields. Historical
# radio banks remain evidence in recipes.json; live source content is preserved.
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
CURRENT=json.loads((HERE/'current-source.json').read_text())
CURRENT_QUESTIONS={q[':question/math-academy-id']:q for q in CURRENT['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate','hard')

def checkbox_prompt(prompt):
 lines=prompt.splitlines();statements=[];header=[]
 for line in lines:
  if re.match(r'^(?:- |[1-3]\. |I{1,3}\. )',line):
   statements.append(re.sub(r'^(?:- |[1-3]\. |I{1,3}\. )','',line))
  elif not statements:header.append(line)
 if len(statements)!=3:raise ValueError('Expected three statement slots')
 return '\n'.join(header).strip()+'\n\nSelect all that apply.\n\n'+'\n'.join('- **'+roman+'.** '+statement for roman,statement in zip(ROMAN,statements))

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'checkbox','blank'):raise ValueError('Live bank uses checkbox or blank')
 r=_generate_legacy(level,seed,template,None,parameters,profile)
 name=r['generation']['template'];q=r['question'];meta=r['generation']
 if name=='q-167631' and profile=='observed-q-167631':
  raise ValueError('Mislinked sine and malformed source TeX are evidence only, excluded from supported generation')
 if meta['claims']:
  q[':question/problem']=checkbox_prompt(q[':question/problem'])
  if name in CURRENT_QUESTIONS and '\n\n- **II.' in CURRENT_QUESTIONS[name][':question/problem']:
   q[':question/problem']=q[':question/problem'].replace('\n- **II.', '\n\n- **II.').replace('\n- **III.', '\n\n- **III.')
  if name in ('q-27015','q-27021'):
   # Live repair uses ASCII mathematical explanation. At changed parameters
   # use the same three-verdict method with independently computed values.
   if meta['parameters']==SOURCE_DEFAULTS[name]:q[':question/worked-solution']=CURRENT_QUESTIONS[name][':question/worked-solution']
  values=[(roman,('true' if bit else 'false')) for roman,bit in zip(ROMAN,meta['truth_vector'])]
  fields=[(key,'text',['false','true'],correct) for key,correct in values]
  typ='checkbox'
 else:
  fields=[(f[':answer-field/key'],'math',[a[':answer/value'] for a in f[':answer-field/choices']],next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])) for f in q[':question/answer-fields']]
  typ='blank'
 q[':question/problem']=normalize_prose(q[':question/problem']);q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
 fields=[(key,atype,[normalize_tex(v)for v in bank]if atype=='math'else bank,normalize_tex(correct)if atype=='math'else correct)for key,atype,bank,correct in fields]
 content=digest({'version':VERSION,'prompt':q[':question/problem'],'solution':q[':question/worked-solution'],'fields':fields})
 qid=str(uuid.uuid5(uuid.UUID(KP_UUID),content));q[':question/id']=qid;out=[]
 for key,atype,bank,correct in fields:
  fid=str(uuid.uuid5(uuid.UUID(qid),key))
  answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),value)),':answer/type':':answer.type/'+atype,':answer/value':value} for value in bank]
  out.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+typ,':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id'] for a in answers if a[':answer/value']==correct)]})
 q[':question/answer-fields']=out;meta['content_fingerprint']=content;meta['source_analysis']={'database':'math','basis':CURRENT['basis'],'lineage':CURRENT['lineage']};meta['response_profile']='live-three-boolean-checkbox' if typ=='checkbox' else 'repaired-cosine-facts'
 return r

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Authored missing easy: three local facts, 32 finite semantic claim sets."""
 return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Observed masks/banks or equal-workload mixed finite authored catalog."""
 return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Authored missing hard: completeness of three families; 216 semantic sets."""
 return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];lines=[q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  lines+=['Field '+f[':answer-field/key']+':']
  for a in f[':answer-field/choices']:lines+=['- '+a[':answer/value']+(' **(correct)**' if a[':answer/id']==f[':answer-field/correct'][1] else '')]
 return '\n'.join(lines+['','Worked solution:','',q[':question/worked-solution']])
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template',choices=TEMPLATES);parser.add_argument('--profile',choices=BANK_PROFILES);parser.add_argument('--field-type',choices=('checkbox','blank'))
 a=parser.parse_args()
 if a.count<1:parser.error('count must be positive')
 if a.difficulty=='all' and (a.template or a.profile):parser.error('Use a specific difficulty with template/profile')
 try:records=[generate(l,a.seed+i,a.template,a.field_type,profile=a.profile) for l in (('easy','moderate','hard') if a.difficulty=='all' else (a.difficulty,)) for i in range(a.count)]
 except ValueError as e:parser.error(str(e))
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name])


from ca_source_runtime import install as _ca_source_install
_ca_source_install(globals(),_ca_Path(__file__).with_name('17592186176047-source-policy.json'))

if __name__=='__main__':main()
