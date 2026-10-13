#!/usr/bin/env python3
"""Finding parameter intervals for quarter/half ellipses; local scratch only.

Basis 1356 source fidelity precedes variation: fifteen extracted prose/layout
skeletons and ten COMPLETE geometric interval banks are in the evidence folder.
Every replay passes through the same parameterized equations, center/radius
substitution, computed endpoint answers, owned UUIDs and Matplotlib renderer.
There is no source-payload return branch or correct-answer lookup. The categorical
interval distractors do not depend on ellipse radii: each denotes a different
quarter/half/full traversal, so these are explicit geometric recipes. Their author
intent is unresolved; no feedback or distractor diagnosis is invented.

Easy: origin-centered first-quarter and upper half. Moderate: origin-centered
other quarters and lower/left halves. Hard: translated quarters and halves.
All three levels are observed. Radii 2..8, unequal; hard centers -4..4 with at
least one nonzero component. This adds objects within each observed method,
not new algebra, arc lengths, arbitrary angles, rotations or direction changes.
Source teaching errors are corrected and counted separately in validation.

API generate(level, seed=0, template=None, field_type=None, parameters=None,
profile=None); generate_easy/moderate/hard mirror it. Explicit invalid inputs
raise instead of resampling. JSON records are reviews, never database data.
CLI --difficulty easy|moderate|hard|all --seed N --count N --format markdown|json
and --template/--profile. Stop after docs step 7; no registration or DB clients.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,uuid
from pathlib import Path
from fractions import Fraction
import sympy as sp
KP_ID=17592186152190
KP_UUID='9b51a7bc-7701-539f-9e20-dfc7f2574559'
TITLE='Parametrizing Part of an Ellipse'
VERSION='ellipse-part-1'
HERE=Path(__file__).resolve().with_suffix('')
DATA=json.loads((HERE/'templates.json').read_text())
TEMPLATES=DATA['templates'];BANK_PROFILES=DATA['profiles']
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}

def canonical(p):
 if set(p)!=set(('a','b','h','k','lo','hi')):raise ValueError('Parameters must be exactly a,b,h,k,lo,hi')
 if any(type(p[n]) is not int for n in ('a','b','h','k')):raise ValueError('Integer radii/center required')
 if not 2<=p['a']<=8 or not 2<=p['b']<=8 or p['a']==p['b']:raise ValueError('Unequal radii in 2..8 required')
 if not -4<=p['h']<=4 or not -4<=p['k']<=4:raise ValueError('Center outside -4..4')
 p={**p,'lo':str(Fraction(p['lo'])),'hi':str(Fraction(p['hi']))}
 if not 0<=Fraction(p['lo'])<Fraction(p['hi'])<=2:raise ValueError('Require 0 <= lo < hi <= 2, in units of pi')
 return p

def fingerprint(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def uid(value):return str(uuid.uuid5(uuid.UUID(KP_UUID),str(value)))
def angle(value):return sp.latex(sp.Rational(value)*sp.pi)
def interval(bounds):
 lo,hi,closed=bounds
 return r'\theta \in ['+angle(lo)+','+angle(hi)+(']' if closed else ')')
def substitute(text,p,assets):
 values={**p,'h_sign':('+' if p['h']>0 else '')+str(p['h']) if p['h'] else '',
         'k_sign':('+' if p['k']>0 else '')+str(p['k']) if p['k'] else '',**assets}
 for key,value in values.items():text=text.replace('@@'+key+'@@',str(value))
 if '@@' in text:raise ValueError('Unfilled template slot')
 return text

def render_plots(instance,output_dir=None):
 """Render exact instance via cached read-only Matplotlib runtime. Never resample."""
 p=instance['parameters'];directory=Path(output_dir or HERE/'plots');directory.mkdir(parents=True,exist_ok=True)
 key=fingerprint({'p':p,'prompt_context':instance['prompt_context'],'renderer':'4'})[:24]
 assets={role:str(directory/(key+'-'+role+'.png')) for role in ('prompt','solution')}
 if not all(Path(v).exists() for v in assets.values()):
  spec={**instance,'assets':assets,'endpoint_labels':[r'\theta='+angle(p['lo']),r'\theta='+angle(p['hi'])]}
  specfile=directory/(key+'.json');specfile.write_text(json.dumps(spec,indent=2)+'\n')
  subprocess.run([str(Path('.venv/bin/python').resolve()),str(HERE/'render.py'),str(specfile)],check=True)
 return assets

def sample_parameters(level,t,rng):
 """Same-method object sampler, exposed for finite-domain variety audits."""
 a,b=rng.sample(range(2,9),2);h=k=0
 if level=='hard':
  while h==k==0:h,k=rng.randint(-4,4),rng.randint(-4,4)
 return canonical({'a':a,'b':b,'h':h,'k':k,'lo':t['arc'][0],'hi':t['arc'][1]})

# EASY: observed first-quarter and upper-half origin-centered arcs.
# MODERATE: observed third/fourth quarters and left/lower origin-centered halves.
# HARD: observed translated first quarter, upper half and left half.
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown level')
 if field_type not in (None,'blank','radio'):raise ValueError('Unsupported field type')
 if profile is not None and profile not in BANK_PROFILES:raise ValueError('Unknown profile')
 eligible=[name for name,t in TEMPLATES.items() if t['level']==level and (field_type is None or t['layout'][0]['type']==field_type) and (profile is None or profile in t['profiles'])]
 if template is not None and template not in eligible:raise ValueError('Template, profile, field type or difficulty mismatch')
 if not eligible:raise ValueError('No eligible template')
 # For explicit parameters choose a stable eligible template, independent of seed.
 if parameters is not None:
  p=canonical(parameters)
  eligible=[n for n in eligible if TEMPLATES[n]['arc']==[p['lo'],p['hi']] and (level=='hard')==(p['h']!=0 or p['k']!=0)]
  if template is not None and template not in eligible:raise ValueError('Parameters violate template arc/center conditions')
  if not eligible:raise ValueError('No compatible template')
  name=template or sorted(eligible)[0]
 else:
  rng=random.Random(seed);name=template or rng.choice(eligible);t=TEMPLATES[name]
  p=sample_parameters(level,t,rng)
 t=TEMPLATES[name]
 profile=profile or (sorted(t['profiles'])[0] if t['profiles'] else None)
 if t['layout'][0]['type']=='radio':
  bank=BANK_PROFILES[profile]['intervals'];correct=interval([p['lo'],p['hi'],True]);values=[interval(z) for z in bank]
  if len(values)!=5 or len(set(values))!=5 or values.count(correct)!=1:raise ValueError('Reject whole ambiguous or incomplete bank')
 else:correct=None;values=[]
 assets=render_plots({'parameters':p,'prompt_context':t['prompt_context']})
 problem=substitute(t['problem'],p,assets);solution=substitute(t['solution'],p,assets)
 physical=fingerprint(p)
 content=fingerprint({'version':VERSION,'problem':problem,'solution':solution,'bank':sorted(values),'blank_answers':[angle(p['lo']),angle(p['hi'])] if not profile else [],'layout':t['layout']})
 qid=uid(content);fields=[]
 for layout in t['layout']:
  key=layout['key'];kind=layout['type'];fid=uid(content+'/'+key)
  vals=values if kind=='radio' else [angle(p['lo'] if key=='field-1' else p['hi'])]
  answer=correct if kind=='radio' else vals[0]
  choices=[{':answer/id':uid(fid+'/'+v),':answer/type':':answer.type/math',':answer/value':v} for v in vals]
  correctid=next(z[':answer/id'] for z in choices if z[':answer/value']==answer)
  random.Random(seed).shuffle(choices)
  fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':choices,':answer-field/correct':[':answer/id',correctid]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},
         'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},
         'generation':{'version':VERSION,'seed':seed,'template':name,'parameters':p,'parameter_fingerprint':physical,'content_fingerprint':content,'bank_profile':profile,'bank_origin':'observed' if profile else None,'source_analysis':{**SOURCE,'question_ids':t['sources']},'plot_rating':'heavy','plot_assets':assets,'plot_renderer':'Matplotlib','sympy_version':sp.__version__,'domain':'theta in closed ['+p['lo']+'*pi,'+p['hi']+'*pi]','distractor_recipes':BANK_PROFILES[profile]['intervals'] if profile else [],'authored_extension':False,'parameter_extension':p not in [c['parameters'] for c in json.loads((HERE/'source-cases.json').read_text())], 'parameter_sampling_policy':'Unequal radii 2..8; hard centers -4..4, not both zero','source_prose_repairs':['parameter angle is not ellipse polar angle']+(['copied center/radii'] if 'q-274866' in t['sources'] else [])+(['final p,q changed to x,y'] if 'q-327831' in t['sources'] else [])+(['missing generic-equation separator'] if 'q-79282' in t['sources'] else [])}}

def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(r):
 q=r['question'];g=r['generation'];parts=[f"## Generated {q[':question/difficulty'].split('/')[-1]} — {g['template']}",q[':question/problem']]
 for f in q[':question/answer-fields']:
  parts.append('\nField '+f[':answer-field/key']+':')
  parts.extend('- $'+a[':answer/value']+'$'+(' **correct**' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])
 parts+=['\nWorked solution:',q[':question/worked-solution']];return '\n\n'.join(parts)
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=('easy','moderate','hard','all'),default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=('markdown','json'),default='markdown');parser.add_argument('--template',choices=tuple(TEMPLATES));parser.add_argument('--profile',choices=tuple(BANK_PROFILES));parser.add_argument('--field-type',choices=('radio','blank'));args=parser.parse_args()
 if args.count<1:parser.error('Positive count required')
 if args.difficulty=='all' and (args.template or args.profile):parser.error('Specific difficulty required with template/profile')
 levels=('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)
 records=[generate(l,args.seed+i,args.template,args.field_type,None,args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
