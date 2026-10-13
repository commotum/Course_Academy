#!/usr/bin/env python3
"""Draft tangent stretch/vertical-shift generator; stops at guide step 7.

Frozen math basis 1356. Private source masks, raster evidence, validation and
review are in 17592186184236/. No database access. All original banks are
public parameterized evidence profiles; opaque interpretations remain
ineligible for learning. Normal defaults use observed prompt/solution masks
with complete method-derived banks, selected before parameters.

Easy: directly labelled adjacent asymptotes and y-intercept (observed).
Moderate: authored two-subdivision x calibration and half-unit y reading.
Hard: authored three-subdivision x calibration and quarter-unit y reading.
Each asks B+D or D-B for y=tan(Bx)+D; never a phase-shift problem.
"""
from __future__ import annotations
import argparse, hashlib, json, os, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
import sympy as sp

HERE=Path(__file__).resolve().with_suffix('')
KP_ID=17592186184236
VERSION='tangent-stretch-vertical-1'
SNAPSHOT=json.loads((HERE/'source.json').read_text())
KP=SNAPSHOT['record']
QUESTIONS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
ASSETS=json.loads((HERE/'source-assets.json').read_text())
SOURCE_PARAMETERS={
 'q-65448':('1/2','1','sum'), 'q-65547':('2/3','-2','difference'),
 'q-117795':('3','-3','sum'), 'q-141974':('2/3','1','difference'),
 'q-143638':('2','-2','sum'), 'q-117796':('5/4','1/2','sum')}
MASKS=json.loads((HERE/'masks.json').read_text()) if (HERE/'masks.json').exists() else {}
TEMPLATES={'sum':['q-65448','q-117795','q-143638','q-117796'],
           'difference':['q-65547','q-141974']}
BANK_PROFILES={
 'period-sign':{'origin':'authored','recipes':['correct','double-period','half-period','reverse-shift','reciprocal-scale']},
 'omitted-sign':{'origin':'authored','recipes':['correct','omit-scale','omit-shift','reverse-both','reverse-shift']},
}
for sid in QUESTIONS:
 BANK_PROFILES['raw-'+sid]={'origin':'observed','source':sid,'evidence_only':True}
 BANK_PROFILES['repair-'+sid]={'origin':'explicit-authored-repair','source':sid,'evidence_only':sid!='q-65448'}

def rat(value):
 v=sp.Rational(str(value))
 return v

def tex(value):
 return sp.latex(sp.sympify(value)).replace(r'- \frac',r'-\frac')

def source_tex(value):
 # The captured operatorname masks put a space after every pi token.
 return tex(value).replace(r' \pi',r'\pi').replace(r'\pi',r'\pi ')

def signed(value, spaces=False):
 return (' - ' if spaces else '-')+tex(-value) if value<0 else (' + ' if spaces else '+')+tex(value)

def bx_tex(B):
 n,d=int(B.p),int(B.q)
 if d==1:return (str(n) if n!=1 else '')+'x'
 return r'\frac{'+(str(n) if n!=1 else '')+'x}{'+str(d)+'}'

def assessed(template,B,D):
 return B+D if template=='sum' else D-B

def bank_values(profile,template,B,D):
 """Compute a complete selected bank; never pool or replace its members."""
 f=lambda b,d:assessed(template,b,d)
 if profile=='period-sign':return [f(B,D),f(B/2,D),f(2*B,D),f(B,-D),f(1/B,D)]
 if profile=='omitted-sign':return [f(B,D),f(0,D),f(B,0),f(-B,-D),f(B,-D)]
 sid=BANK_PROFILES[profile]['source']
 # Source scalar banks underdetermine intent. These exact component masks
 # are evidence operations, not claimed recovered learner-error mechanisms.
 if sid=='q-65448':return [D,B,B+D,-B,2*(B+D)]
 if sid=='q-65547':return [2*D,D-B,-3*D,B/2,1/B-D/2]
 if sid=='q-117795':return [B+D,B,D/3,2*D/3,2*B/3]
 if sid=='q-141974':return [(D-B)/2,D-B,-B,B-D,(B-D)/2]
 if sid=='q-143638':return [D/2,B-D/2,B,B-D,B+D]
 if sid=='q-117796':return [2*(B+D),B+D,2*B,2*B+D,2*B+3*D]
 raise ValueError(profile)

def valid_bank(values):
 return len(values)==5 and len(set(values))==5 and all(v.is_finite is True and v.is_real is True for v in values)

def domain(level):
 if level=='easy':
  return [rat(x) for x in ('1/3','1/2','2/3','1','3/2','2','5/2','3','4')],[rat(x) for x in range(-4,5) if x]
 if level=='moderate':
  return [rat(x) for x in ('2/3','3/4','4/3','5/4','5/3','3/2','5/2')],[sp.Rational(x,2) for x in range(-7,8,2)]
 if level=='hard':
  return sorted({sp.Rational(n,d) for n in range(2,7) for d in range(3,7) if sp.Rational(n,d).q>=3}),[sp.Rational(x,4) for x in range(-11,12,2)]
 raise ValueError('difficulty must be easy, moderate or hard')

def check_parameters(level,B,D,source=False):
 if not (0<B<=6 and abs(D)<=4):raise ValueError('B must be positive and <=6; |D| <=4')
 if source:return
 bs,ds=domain(level)
 if B not in bs or D not in ds:raise ValueError('parameters outside the documented '+level+' workload')

def normal_solution(template,B,D,level):
 H=sp.pi/(2*B); T=2*H; result=assessed(template,B,D)
 expr='B+D' if template=='sum' else 'D-B'
 arithmetic=tex(B)+'+'+('('+tex(D)+')' if D<0 else tex(D)) if template=='sum' else tex(D)+'-('+tex(B)+')'
 shift=tex(abs(D))+' '+('unit' if abs(D)==1 else 'units')+' '+('up' if D>0 else 'down')
 return ('The period $T$ of the function is\n\n$$\nT='+tex(H)+'-(-'+tex(H)+')='+tex(T)+'.\n$$\n\n'
  'The formula for the period $T$ of the function $y=A\\tan(Bx+C)+D$ is given by \n\n$$\nT=\\frac{\\pi}{B}.\n$$\n\n'
  'Applying the formula of the period, we get\n\n$$\n'+tex(T)+'=\\frac{\\pi}{B}\\quad\\Longrightarrow\\quad B=\\frac{\\pi}{('+tex(T)+')}='+tex(B)+'.\n$$\n\n'
  'The parameter $D$ represents the vertical shift of the tangent function. We see that the function has been translated by $'+shift.split(' ',1)[0]+'$ '+shift.split(' ',1)[1]+'. Hence, $D='+tex(D)+'.$\n\n'
  'Therefore, $'+expr+'='+arithmetic+'='+tex(result)+'.$\n\nFinally, the equation of the curve is\n\n$$\ny=\\tan('+bx_tex(B)+')'+signed(D)+'.\n$$')

def source_slots(sid,B,D):
 """Complete mathematical components; source-specific stage masks, no fits."""
 H=sp.pi/(2*B); T=2*H; f=source_tex
 out={'H':f(H),'T':f(T),'B':f(B),'D':f(D),'absD':f(abs(D)),
      'direction':'up' if D>0 else 'down','result':f(assessed(SOURCE_PARAMETERS[sid][2],B,D)),
      'Bx':bx_tex(B),'shift':signed(D),'Daddition':'('+f(D)+')' if D<0 else f(D)}
 if sid=='q-141974':
  # Retain unsimplified doubling of the same displayed endpoint fraction.
  c=sp.Rational(1,2)/B
  out['Traw']=r'\frac{'+str(2*c.p)+r'\pi }{'+str(c.q)+'}' if c.q!=1 else str(2*c.p)+r'\pi '
 if sid=='q-143638':
  c=1/B
  out['inverse']=r'\frac{'+(('' if c.q==1 else str(c.q))+r'\pi ')+r'}{'+(('' if c.p==1 else str(c.p))+r'\pi ')+r'}'
 return out

def fill(mask,slots):
 for k,v in slots.items():mask=mask.replace('{{'+k+'}}',v)
 if '{{' in mask:raise AssertionError('unfilled source mask: '+mask)
 return mask

def render_plots(instance,output_dir=HERE/'plots'):
 """Matplotlib subprocess, unique input and atomic asset+sidecar writes."""
 output_dir=Path(output_dir);output_dir.mkdir(exist_ok=True,parents=True)
 name=hashlib.sha256(json.dumps(instance,sort_keys=True).encode()).hexdigest()[:22]
 png=output_dir/(name+'.png'); sidecar=output_dir/(name+'.json')
 if not (png.exists() and sidecar.exists()):
  with tempfile.NamedTemporaryFile('w',suffix='.json',prefix='render-',dir=output_dir,delete=False) as f:
   json.dump({'instance':instance,'png':str(png),'sidecar':str(sidecar)},f);input_path=f.name
  try:subprocess.run([sys.executable,str(HERE/'renderer.py'),input_path],check=True,stdout=subprocess.DEVNULL)
  finally:Path(input_path).unlink(missing_ok=True)
 return {'prompt':str(png),'spec':str(sidecar)}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Public API including omission-faithful raw-q-* evidence replay."""
 if level not in ('easy','moderate','hard'):raise ValueError(level)
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio only')
 rng=random.Random(seed)
 profile=profile or rng.choice(('period-sign','omitted-sign')) # bank before params
 if profile not in BANK_PROFILES:raise ValueError('unknown profile')
 bp=BANK_PROFILES[profile];sid=bp.get('source')
 raw=profile.startswith('raw-'); repaired=profile.startswith('repair-')
 if sid and level!='easy':raise ValueError('source profiles replay observed easy/unrated workload only')
 if sid:
  observed_template=SOURCE_PARAMETERS[sid][2]
  if template and template not in (observed_template,sid):raise ValueError('source template mismatch')
  template=observed_template
 else:
  template=template or rng.choice(tuple(TEMPLATES))
  if template not in TEMPLATES:raise ValueError('unknown template')
  sid=TEMPLATES[template][0]
 if parameters is not None:
  if set(parameters)-{'B','D','source_mask'}:raise ValueError('unknown parameters')
  B=rat(parameters['B']);D=rat(parameters['D'])
  sid=parameters.get('source_mask',sid)
  if sid not in TEMPLATES[template]:raise ValueError('source mask does not match assessed expression')
  check_parameters(level,B,D,source=raw or repaired)
  vals=bank_values(profile,template,B,D)
  if not valid_bank(vals):raise ValueError('whole-bank collision')
 else:
  bs,ds=domain(level)
  if raw or repaired:B,D=map(rat,SOURCE_PARAMETERS[sid][:2]);vals=bank_values(profile,template,B,D)
  else:
   for _ in range(1000):
    B,D=rng.choice(bs),rng.choice(ds);vals=bank_values(profile,template,B,D)
    if valid_bank(vals):break
   else:raise ValueError('no eligible complete bank')
 solution_present=not raw or ':question/worked-solution' in QUESTIONS[sid]
 if not bp.get('source') and not (parameters and 'source_mask' in parameters):
  component_hash=hashlib.sha256((str(B)+'|'+str(D)+'|'+template).encode()).digest()
  eligible_masks=[s for s in TEMPLATES[template] if s!='q-141974' or (sp.Rational(1,2)/B).q%2==0]
  sid=eligible_masks[int.from_bytes(component_hash[:4],'big')%len(eligible_masks)]
 if sid=='q-141974' and (sp.Rational(1,2)/B).q%2!=0:
  raise ValueError('q-141974 requires a genuine unreduced-to-reduced period row')
 source_exact_geometry=(raw or repaired) and (B,D)==tuple(map(rat,SOURCE_PARAMETERS[sid][:2]))
 if source_exact_geometry:
  assets={'prompt':ASSETS[sid]['path'].removeprefix('/media/jake/SSD/EDB/math/') if raw else ASSETS[sid]['path'],'spec':str(HERE/'source-geometry.json')}
 else:assets=render_plots({'B':str(B),'D':str(D),'level':level,'calibration':{'easy':1,'moderate':2,'hard':3}[level],'renderer_version':2})
 if raw or repaired:
  prompt=fill(MASKS[sid]['prompt'],{'asset':assets['prompt']})
  if sid=='q-65547':solution=normal_solution(template,B,D,level)
  else:solution=fill(MASKS[sid]['solution'],source_slots(sid,B,D))
 else:
  # All source prompt masks participate in defaults; notation normalized only.
  prompt=fill(MASKS[sid]['prompt'],{'asset':assets['prompt']}).replace(r'\operatorname{tan}⁡',r'\tan')
  if sid=='q-65547':solution=normal_solution(template,B,D,level)
  else:
   solution=fill(MASKS[sid]['solution'],source_slots(sid,B,D)).replace(r'\operatorname{tan}⁡',r'\tan')
   solution=re.sub(r'(\$[^$]+\$) units? (up|down)',lambda m:m[1]+' '+('unit' if abs(D)==1 else 'units')+' '+m[2],solution)
 result=assessed(template,B,D)
 value_text=[tex(v) for v in vals]
 eligibility=not raw and not bp.get('evidence_only',False)
 # Source-mask names, seeds, layout aliases and paths are not content identity.
 meaningful={'B':str(B),'D':str(D),'requested':template,'calibration':{'easy':1,'moderate':2,'hard':3}[level]}
 mf=hashlib.sha256(json.dumps(meaningful,sort_keys=True).encode()).hexdigest()
 content={'version':VERSION,'level':level if not raw or ':question/difficulty' in QUESTIONS[sid] else None,
          'prompt':prompt,'solution':solution if solution_present else None,'bank':sorted(value_text),
          'field-layout':'legacy-duplicate' if raw and sid=='q-65448' else 'single',
          'correct_presence':not (raw and sid=='q-65547')}
 digest=hashlib.sha256(json.dumps(content,sort_keys=True).encode()).hexdigest()
 qid=str(uuid.uuid5(uuid.NAMESPACE_URL,digest));fields=[]
 count=2 if raw and sid=='q-65448' else 1
 for i in range(count):
  fid=str(uuid.uuid5(uuid.UUID(qid),'selection:'+str(i)))
  answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),v)),':answer/type':':answer.type/math',':answer/value':v} for v in value_text]
  rng.shuffle(answers)
  field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
  if not raw or ':answer-field/correct' in QUESTIONS[sid][':question/answer-fields'][i]:
   correct=next(a for a in answers if a[':answer/value']==tex(result))
   field[':answer-field/correct']=[':answer/id',correct[':answer/id']]
  fields.append(field)
 q={':question/id':qid,':question/problem':prompt,':question/answer-fields':fields}
 if not raw or ':question/difficulty' in QUESTIONS[sid]:q[':question/difficulty']=':question.difficulty/'+level
 if solution_present:q[':question/worked-solution']=solution
 return {'knowledge_point':{'db_id':KP_ID,'id':KP[':knowledge-point/id'],'title':KP[':knowledge-point/title']},
  'question':q,'generation':{'version':VERSION,'seed':seed,'template':template,'source_mask':sid,'parameters':{'B':str(B),'D':str(D)},
  'bank_profile':profile,'bank_origin':bp['origin'],'evidence_only':not eligibility,'eligible_for_learning':eligibility,
  'difficulty_origin':'observed' if raw and sid!='q-65547' else 'authored' if level!='easy' or sid=='q-65547' else 'source-shaped-extension',
  'source_analysis':{'database':SNAPSHOT['database'],'basis_t':SNAPSHOT['basis'],'lineage':SNAPSHOT['lineage']},
  'mathematical_fingerprint':mf,'content_fingerprint':digest,'plot_rating':'heavy','plot_assets':assets,
  'domain':{'B':'positive','phase_shift':0,'vertical_scale':1},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}}

# Easy: original graph-reading demand; integer shifts in normal authored bank.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('easy',seed,template,field_type,parameters,profile)

# Moderate: two horizontal subdivisions; nonintegral half-unit vertical reading.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('moderate',seed,template,field_type,parameters,profile)

# Hard: three horizontal subdivisions; non-half quarter-unit vertical reading.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):
 return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r,label='GENERATED VARIANT'):
 q=r['question'];g=r['generation']
 def preview(z):return re.sub(r'(!\[[^]]*\]\()(images/[^)]+)(\))',lambda m:m[1]+'/media/jake/SSD/EDB/math/'+m[2]+m[3],z)
 difficulty=q.get(':question/difficulty','not rated').split('/')[-1]
 text='### '+label+' — '+difficulty+' / '+g['template']+' / '+g['bank_profile']+'\n\n'+preview(q[':question/problem'])+'\n\n'
 for i,f in enumerate(q.get(':question/answer-fields',[])):
  text+='Field '+str(i)+' ('+f[':answer-field/type']+'): '+('correct ref present' if ':answer-field/correct' in f else 'correct ref omitted')+'\n\n'
  text+='\n'.join('- $'+a[':answer/value']+'$'+(' **designated correct**' if ':answer-field/correct' in f and a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'
 text+=preview(q.get(':question/worked-solution','[Source worked solution omitted.]'))+'\n\n'
 return text+'Author metadata: `'+json.dumps(g['parameters'])+'`; eligible='+str(g['eligible_for_learning'])+'; mathematical fingerprint `'+g['mathematical_fingerprint']+'`.\n\n'

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all')
 ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=2);ap.add_argument('--format',choices=['json','markdown'],default='markdown')
 ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,args.template,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n'.join(markdown(r) for r in records))
