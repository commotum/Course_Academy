#!/usr/bin/env python3
"""Interpret derivatives by identifying output change / input change.

Read-only source provenance: math basis 1356. Seven observed parameterized
sentence/layout templates and complete banks; all figures absent from practice.
An unrated source has a supported authored easy classification and missing key
and solution repairs. Source evidence is preserved beside this file.

Variation is finite and categorical: geometric quantities and independently
varying dimensions, not computed derivatives, evaluated rates, units, or formulas.
Symbol changes are presentation variety only and never inflate task counts.
Easy: a directly described circle/sphere size to aggregate measure.
Moderate: choose the varying dimension when another dimension is held fixed,
or recognize perimeter dependence on a regular polygon's side.
Hard: inverse size/aggregate roles, or two axes of an ellipse with one fixed.
All explicit parameters obey the same finite domain as random samples.

Each observed profile applies its complete set of semantic operations together.
No source payload is loaded at generation time. Correctness uses output/input
role semantics; equal numerical geometry formulas are not the response criterion
(the circle's circumference option is a quantity, not an interpretation as a rate).
Observed solution wording uses Change in as qualitative differential shorthand.
Authored solutions explicitly say instantaneous change to avoid finite-difference
interpretations. Field-owned identities include actual prompt, fixed solution,
complete sorted bank and designation; order and seed do not affect identities.
"""
from __future__ import annotations
import argparse, hashlib, json, random, re, uuid
import sympy as sp

KP_ID = 17592186064152
KP_UUID = '159b4d58-b34d-52cd-aad2-2c058f772ad2'
TITLE = 'Interpreting the Derivative of a Function'
VERSION = 'interpret-derivative-1'
SOURCE = {'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
NB = '\u00a0'

# Complete component masks. {dep}/{ind} are whole mathematical symbols;
# replacement occurs only in masks, never arbitrary source strings.
OBSERVED = {
 'circle': dict(level='easy',source='q-48616', dep='A',ind='r', out='area',inp='radius',shape='circle',
  prompt='Consider a circle such that the radius ${ind}$ can vary. If ${dep}$ is the area of the circle, what is the best interpretation of ${dep}^{{′}}({ind})$?',
  opening='The function ${dep}({ind})$ gives the area of a circle with radius ${ind}.$ So',
  bank=[('value_out','The area of a circle with radius ${ind}$'),('reverse','The rate at which the radius changes as the area changes'),('value_in','The length of the radius of the circle'),('other_value','The circumference of the circle'),('correct','The rate at which the area changes as the radius changes')], missing=True),
 'rectangle': dict(level='moderate',source='q-48684',dep='A',ind='b',out='area',inp='base',shape='rectangle',
  prompt='Consider a rectangle such that the height is fixed but its base ${ind}$ can vary. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the area of the rectangle?',
  opening='The function ${dep}({ind})$ gives the area of a rectangle with base ${ind}.$ So',
  bank=[('value_out','The area of a rectangle with base ${ind}$'),('fixed_reverse','The rate at which the height changes as the area changes'),('value_in','The length of the base of the rectangle'),('fixed','The rate at which the area changes as the height changes'),('correct','The rate at which the area changes as the base changes')]),
 'ellipse': dict(level='hard',source='q-112063',dep='S',ind='a',out='area',inp='major axis',shape='ellipse',
  prompt='Consider an ellipse such that its major axis ${ind}$ can vary while its minor axis is fixed. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the area enclosed by the ellipse?',
  opening='The function ${dep}({ind})$ gives the area of the ellipse with major axis ${ind}.$ So,',
  bank=[('correct','The rate at which the area changes as the major axis changes'),('value_in','The major axis of an ellipse with area {dep}'),('other_rate','The rate at which the perimeter changes as the major axis changes'),('two_inputs','The rate at which the major axis changes as the minor axis changes'),('value_out','The area of an ellipse with major axis ${ind}$')]),
 'cube': dict(level='moderate',source='q-48685',dep='V',ind='s',out='volume',inp='each side',shape='cube',
  prompt='Consider a cube such that the length of each side ${ind}$ varies. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the volume of the cube?',
  opening='The function ${dep}({ind})$ gives the volume of a cube with side ${ind}.$ So,',
  bank=[('value_in','The length of each side of the cube'),('reverse','The rate at which each side changes as the volume changes'),('correct','The rate at which the volume changes as each side changes'),('value_out','The volume of a cube with side ${ind}$'),('other_rate','The rate at which the surface area of the cube changes as each side changes')]),
 'square_inverse': dict(level='hard',source='q-48686',dep='s',ind='A',out='each side',inp='area',shape='square',
  prompt='Consider a square such that its area ${ind}$ can vary. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the length of each side of the square?',
  opening='The function ${dep}({ind})$ gives the length of each side of a square with area ${ind}.$ So,',
  bank=[('correct','The rate at which each side changes as the area changes'),('value_out','The length of each side of the square'),('other_rate','The rate at which each side of the square changes as the perimeter changes'),('reverse','The rate at which the area changes as each side changes'),('value_in','The area of a square with side ${dep}$')]),
 'sphere_inverse': dict(level='hard',source='q-72099',dep='r',ind='V',out='radius',inp='volume',shape='sphere',
  prompt='Consider a sphere such that its volume ${ind}$ can vary. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the length of the radius of the sphere?',
  opening='The function ${dep}({ind})$ gives the length of the radius of a sphere with volume ${ind}.$ So,',
  bank=[('other_inverse','The rate at which the volume changes as the surface area changes'),('reverse','The rate at which the volume changes as the radius changes'),('other_rate','The rate at which the surface area changes as the radius changes'),('correct','The rate at which the radius changes as the volume changes'),('other_input','The rate at which the radius changes as the surface area changes')]),
 'polygon': dict(level='moderate',source='q-72104',dep='P',ind='s',out='perimeter',inp='each side',shape='pentagon',
  prompt='Consider a regular {shape} such that the length ${ind}$ of each side varies. What is the best interpretation of ${{{dep}}}^{{′}}({ind})$ if ${dep}$ is the perimeter of the {shape}?',
  opening='The function ${dep}({ind})$ gives the perimeter of a {shape} with side ${ind}.$ So,',
  bank=[('correct','The rate at which the perimeter changes as each side changes'),('other_rate','The rate at which the area changes as each side changes'),('reverse','The rate at which each side changes as the perimeter changes'),('other_input','The rate at which the perimeter changes as the area changes'),('other_inverse','The rate at which each side changes as the area changes')]),
}

# (shape, dependent physical quantity, independent physical quantity, fixed
# dimension, alternative physical quantity). Every entire tuple is eligible.
EASY_CONTEXTS = [(s,o,i,None,a) for s,o,a in [('circle','area','circumference'),('circle','circumference','area'),('sphere','volume','surface area'),('sphere','surface area','volume')] for i in ['radius','diameter']]
MODERATE_CONTEXTS = [
 ('rectangle','area','base','height','perimeter'),('rectangle','area','height','base','perimeter'),
 ('triangle','area','base','height','perimeter'),('triangle','area','height','base','perimeter'),
 ('parallelogram','area','base','height','perimeter'),('parallelogram','area','height','base','perimeter'),
 ('cylinder','volume','radius','height','surface area'),('cylinder','volume','height','radius','surface area'),
 ('cone','volume','radius','height','surface area'),('cone','volume','height','radius','surface area')]
# Triangle/parallelogram perimeter is not determined by base/height alone;
# authored bank uses the fixed coordinate as its fourth distractor, never that
# unspecified alternative function. It is metadata only in these contexts.
HARD_CONTEXTS = [
 ('circle','radius','area',None,'circumference'),('circle','diameter','area',None,'circumference'),
 ('sphere','radius','volume',None,'surface area'),('sphere','diameter','volume',None,'surface area'),
 ('square','each side','area',None,'perimeter'),('cube','each side','volume',None,'surface area'),
 ('ellipse','area','major axis','minor axis','perimeter'),('ellipse','area','minor axis','major axis','perimeter')]
CONTEXTS = {'easy_direct':EASY_CONTEXTS,'moderate_fixed':MODERATE_CONTEXTS,'hard_roles':HARD_CONTEXTS}
LEVELS = {'easy_direct':'easy','moderate_fixed':'moderate','hard_roles':'hard'}
TEMPLATES = {k:v['level'] for k,v in OBSERVED.items()} | LEVELS
SYMBOLS = ('A','B','P','S','V','a','b','h','r','s','x','y')
POLYGONS = ('triangle','square','pentagon','hexagon','heptagon','octagon','nonagon','decagon','dodecagon')

def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
def definite(quantity): return quantity if quantity=='each side' else 'the '+quantity
def quantity_phrase(quantity): return 'the length of each side' if quantity=='each side' else 'the '+quantity
def rate(out, inp): return f'The rate at which {definite(out)} changes as {definite(inp)} changes'
def symbol_for(quantity): return {'area':'A','circumference':'C','volume':'V','surface area':'S','radius':'r','diameter':'d','base':'b','height':'h','each side':'s','major axis':'a','minor axis':'b'}[quantity]
# Include canonical C and d in the explicit symbol domain.
SYMBOLS += ('C','d')

def resolve_parameters(template, p, rng):
 if template in OBSERVED:
  t=OBSERVED[template]; defaults={'dep':t['dep'],'ind':t['ind']}
  if template=='polygon': defaults['shape']='pentagon'
  p=defaults if p is None else dict(p)
  if set(p)!=set(defaults): raise ValueError('Observed parameter keys must be '+str(sorted(defaults)))
  if template=='polygon' and p['shape'] not in POLYGONS: raise ValueError('Invalid regular polygon')
 else:
  n=rng.randrange(len(CONTEXTS[template])) if p is None else p.get('context')
  if type(n) is not int or not 0<=n<len(CONTEXTS[template]): raise ValueError('Context outside finite level domain')
  c=CONTEXTS[template][n]
  p={'context':n,'dep':symbol_for(c[1]),'ind':symbol_for(c[2])} if p is None else dict(p)
  if set(p)!={'context','dep','ind'}: raise ValueError('Authored parameter keys are context, dep, ind')
 if p['dep'] not in SYMBOLS or p['ind'] not in SYMBOLS or p['dep']==p['ind']: raise ValueError('Distinct supported dependent/independent symbols required')
 return p

def build_observed(template,p):
 t=OBSERVED[template]; slots={**t,**p}
 prompt=t['prompt'].format(**slots)
 opening=t['opening'].format(**slots)
 dep,ind=p['dep'],p['ind']; derivative=dep+'^{′}('+ind+')' if template=='circle' else '{'+dep+'}^{′}('+ind+')'
 equation=derivative+'=\\frac{\\text{d}'+dep+'}{\\text{d}'+ind+'}=\\frac{\\text{Change in'+NB+'}'+dep+'}{\\text{Change in'+NB+'}'+ind+'}.'
 conclusion=f'Therefore, ${derivative}$ is the rate at which {definite(t["out"])} changes as {definite(t["inp"])} changes.'
 solution=opening+'\n\n$$\n'+equation+'\n$$\n\n'+conclusion
 bank=[(label,mask.format(**slots)) for label,mask in t['bank']]
 semantic=(p.get('shape',t['shape']),t['out'],t['inp'], 'height' if template=='rectangle' else 'minor axis' if template=='ellipse' else None)
 return prompt,solution,bank,semantic

def build_authored(template,p):
 shape,out,inp,fixed,other=CONTEXTS[template][p['context']];dep,ind=p['dep'],p['ind']
 # Complete, explicit role declarations; derivative interpretation is the sole task.
 article='an' if shape=='ellipse' else 'a'
 prompt=f'Consider {article} {shape}. Let ${dep}$ denote {quantity_phrase(out)} and let ${ind}$ denote {quantity_phrase(inp)}.'
 if fixed: prompt+=f' The {fixed} is fixed while the {inp} can vary.'
 else: prompt+=f' {definite(inp).capitalize()} can vary.'
 prompt+=f' What is the best interpretation of ${{{dep}}}^{{′}}({ind})$?'
 correct=rate(out,inp)
 solution=f'The function ${dep}({ind})$ gives {quantity_phrase(out)} of the {shape} as a function of {quantity_phrase(inp)}. So,\n\n$$\n'+'{'+dep+'}^{′}('+ind+')=\\frac{\\text{d}'+dep+'}{\\text{d}'+ind+'}=\\frac{\\text{Instantaneous change in }'+dep+'}{\\text{Change in }'+ind+'}.\n$$\n\n'+f'Therefore, ${{{dep}}}^{{′}}({ind})$ is the rate at which {definite(out)} changes as {definite(inp)} changes.'
 bank=[('correct',correct),('reverse',rate(inp,out)),('value_out',f'{quantity_phrase(out).capitalize()} of the {shape}'),('value_in',f'{quantity_phrase(inp).capitalize()} of the {shape}'),('fixed' if fixed else 'other_rate',rate(out,fixed) if fixed else rate(other,inp))]
 return prompt,solution,bank,(shape,out,inp,fixed)

def semantic_catalog():
 """Finite semantic tasks (8 easy, 20 moderate, 8 hard), canonical symbols.

 Default generation samples uniformly over this catalog. Observed masks win
 duplicates; parameterized bank extensions remain explicitly accessible.
 """
 catalog={level:[] for level in ('easy','moderate','hard')};seen=set()
 for template,t in OBSERVED.items():
  for shape in (POLYGONS if template=='polygon' else [t['shape']]):
   p={'dep':t['dep'],'ind':t['ind']}
   if template=='polygon':p['shape']=shape
   semantic=(shape,t['out'],t['inp'],'height' if template=='rectangle' else 'minor axis' if template=='ellipse' else None)
   seen.add((t['level'],semantic));catalog[t['level']].append((template,p))
 for template,contexts in CONTEXTS.items():
  for i,(shape,out,inp,fixed,other) in enumerate(contexts):
   key=(TEMPLATES[template],(shape,out,inp,fixed))
   if key in seen:continue
   seen.add(key);catalog[TEMPLATES[template]].append((template,{'context':i,'dep':symbol_for(out),'ind':symbol_for(inp)}))
 return catalog

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'): raise ValueError('Unsupported difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'): raise ValueError('Only observed radio layout is supported')
 rng=random.Random(seed)
 if profile and template is None:
  if profile.startswith('observed_'): template=profile.removeprefix('observed_')
  elif profile.startswith('authored_'): template=profile.removeprefix('authored_')
 if template is None:
  if parameters is not None: raise ValueError('Explicit parameters require a template or profile')
  template,parameters=rng.choice(semantic_catalog()[level])
 if template not in TEMPLATES or TEMPLATES[template]!=level: raise ValueError('Template outside difficulty scope')
 expected=('observed_' if template in OBSERVED else 'authored_')+template
 if profile not in (None,expected): raise ValueError('Complete bank profile is incompatible with template')
 p=resolve_parameters(template,parameters,rng)
 prompt,solution,bank,semantic=(build_observed if template in OBSERVED else build_authored)(template,p)
 if len(bank)!=5 or len({v for _,v in bank})!=5: raise ValueError('Reject entire colliding bank')
 correct=next(v for label,v in bank if label=='correct')
 # Canonical task excludes symbol spelling, bank/profile, seed and order.
 task_key=digest({'output':semantic[1],'input':semantic[2],'shape':semantic[0],'fixed':semantic[3]})
 content_key=digest({'version':VERSION,'prompt':prompt,'solution':solution,'bank':sorted(v for _,v in bank),'correct':correct,'level':level})
 qid=uuid.uuid5(uuid.NAMESPACE_URL,f'course-academy/{KP_UUID}/{content_key}'); fid=uuid.uuid5(qid,'selection')
 answers=[{':answer/id':str(uuid.uuid5(fid,v)),':answer/type':':answer.type/text',':answer/value':v} for _,v in bank]
 correct_id=next(a[':answer/id'] for a in answers if a[':answer/value']==correct)
 rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':expected,'parameters':p,'parameter_fingerprint':task_key,'mathematical_task_fingerprint':task_key,'content_fingerprint':content_key,'source_analysis':SOURCE,'source_ids':[OBSERVED[template]['source']] if template in OBSERVED else [],'bank_origin':'observed' if template in OBSERVED else 'authored','authored_extension':template not in OBSERVED or template=='polygon' and p['shape']!='pentagon','source_repairs':['missing original correct designation; inferred by derivative role','missing worked solution; authored','unrated; authored easy assignment'] if template=='circle' else [],'domain':'Positive geometric dimensions; held dimensions fixed; regular polygon sides equal; ellipse major axis remains at least its minor axis. No numerical derivative or unit computation is assessed.','plot_requirement':'none','sympy_version':sp.__version__}}

# EASY: unrated circle supported easy assignment; direct circle/sphere extensions.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: three observed layouts, fixed-dimension and regular-polygon variation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: three observed role/axis layouts and finite inverse/axis extensions.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None): return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join(f'{i}. {a[":answer/value"]}' for i,a in enumerate(f[':answer-field/choices'],1))+'\n\n'+q[':question/worked-solution']+'\n'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 if args.count<1: ap.error('count must be positive')
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n---\n'.join(markdown(r) for r in records))
if __name__=='__main__': main()
