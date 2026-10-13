#!/usr/bin/env python3
"""Finding two vector scalar factors, private steps 3–7 generator.

Observed math basis 1356: 21 sources, 12 five-choice radios and 9 two-blank
questions. Component masks preserve each observed solution sequence. Source
banks are explicit proportional-expression replay profiles with limited error
interpretation; default radio banks are separately authored method errors.
No DB writes, registration, or source literal-answer return paths.

Easy: positive whole-number factors, at most 4. Moderate: one/two direction
reversals, integer/half/quarter factors of magnitude at most 4; preserves
positive-radio observed prototypes. Hard is an authored missing-level design:
two noninteger factors, reversed path order, magnitude below 4 and denominators
2–4; requires two independent length-ratio readings plus coefficient ordering.
No coordinate systems, simultaneous equations, section formula, or new skill.

Rendering invokes the private Matplotlib renderer with unique temporary inputs;
unchanged source diagrams are retained when complete mathematical geometry is
unchanged. Every changed instance receives new prompt and solution plots.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,subprocess,tempfile,uuid
from pathlib import Path
import sympy as sp
KP=17592186096652;VERSION='vector-two-scalars-1';D=Path(__file__).resolve().with_suffix('');ROOT=Path(__file__).resolve().parents[2]
CAPTURE=json.loads((D/'source.json').read_text());RECORD=CAPTURE['record'];TEMPLATES=json.loads((D/'templates.json').read_text())
NS=uuid.UUID('45b6a076-8795-5510-aabc-62a925826dd0')
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(NS,x))
def tex(v,decimal=False):
 v=sp.Rational(v)
 if decimal and v.q in (1,2):return str(int(v)) if v.q==1 else str(float(v))
 return str(v) if v.q==1 else ('-' if v<0 else '')+r'\frac{'+str(abs(v.p))+'}{'+str(v.q)+'}'
def term(v,n,decimal=False,force=False):
 if abs(v)==1 and not force:return ('-' if v<0 else '')+n
 return tex(v,decimal)+n
def total(a,b,u,v,decimal=False,force=False):return term(a,u,decimal,force)+('+' if b>0 else '')+term(b,v,decimal,force)
def slots(mask,values):
 result=re.sub(r'\{\{([a-z_0-9]+)\}\}',lambda m:str(values[m[1]]),mask)
 return result

def _parameters(level,rng,template,explicit):
 if explicit is not None:
  if set(explicit)!={'lambda','mu'}:raise ValueError('Exactly lambda and mu required')
  p={k:sp.Rational(v) for k,v in explicit.items()}
 else:
  if template in TEMPLATES:
   orig={k:sp.Rational(v) for k,v in TEMPLATES[template]['original_parameters'].items()}
   values=[sp.Rational(i,2) for i in range(1,9)] if level=='moderate' else list(map(sp.Rational,range(1,5)))
   p={k:(1 if orig[k]>0 else -1)*rng.choice(values) for k in orig}
  elif level=='easy':p={k:sp.Rational(rng.randint(1,4)) for k in ('lambda','mu')}
  elif level=='moderate':
   p={'lambda':-rng.choice([sp.Rational(i,2) for i in range(1,9)]),'mu':rng.choice([sp.Rational(i,2) for i in range(1,9)])*rng.choice([-1,1])}
  else:
   values=sorted({sp.Rational(n,d) for d in (2,3,4) for n in range(1,4*d) if sp.Rational(n,d).q>1})
   p={k:rng.choice(values)*rng.choice([-1,1]) for k in ('lambda','mu')}
 a,b=p['lambda'],p['mu']
 if any(x==0 or abs(x)>4 or x.q not in (1,2,3,4) for x in (a,b)):raise ValueError('Nonzero rational factors; magnitude <=4 and denominator <=4')
 if level=='easy' and any(x<=0 or x.q!=1 for x in (a,b)):raise ValueError('Easy requires positive integer factors <=4')
 if level=='moderate' and any(x.q not in (1,2,4) for x in (a,b)):raise ValueError('Moderate factors are integers, halves, quarters')
 if template in TEMPLATES:
  orig={k:sp.Rational(v) for k,v in TEMPLATES[template]['original_parameters'].items()}
  if any((p[k]>0)!=(orig[k]>0) for k in p):raise ValueError('Observed prose template fixes factor signs')
 elif level=='moderate' and a>0 and b>0 and a.q==b.q==1:raise ValueError('Authored moderate requires reversal or fractional reading')
 if level=='hard' and any(x.q==1 or abs(x)>=4 for x in (a,b)):raise ValueError('Hard requires two nonintegral factors below magnitude 4')
 return p

def render_plots(p,spec):
 a,b=p['lambda'],p['mu'];names=spec['names'];path=spec['path_names'];segments=spec['segments']
 original=spec.get('original_parameters')
 if original and all(p[k]==sp.Rational(original[k]) for k in p):
  # Reuse only the captured geometry's exact complete factor pair, names and path.
  return [str(D/x) for x in spec['assets']],{'reused_original':True,'source_assets':spec['assets']}
 u=[int(a.q),0];v=[0,int(b.q)]
 if spec.get('oblique',True):u=[int(a.q)*2,int(a.q)];v=[-int(b.q),int(b.q)*2]
 target=[float(a*u[i]+b*v[i]) for i in (0,1)];first=0 if path[0]==names[1] else 1
 c1=a if first==0 else b;c2=b if first==0 else a;basis=u if first==0 else v;corner=[float(c1*x) for x in basis]
 geometry={'style_version':2,'u':u,'v':v,'target':target,'corner':corner,'names':names,'segments':segments,'first_index':first,'path_labels':[term(c1,path[0],spec['decimal']),term(c2,path[1],spec['decimal'])]}
 refs=[]
 for solution in (False,True):
  payload={**geometry,'solution':solution};name=digest(payload);dest=D/'plots'/f'{name}.png';payload['destination']=str(dest)
  # New render inputs per process/call; final paths identical only for identical geometry.
  if not(dest.exists() and dest.with_suffix('.json').exists()):
   with tempfile.NamedTemporaryFile(mode='w',suffix='.json',prefix='plot-input-',dir=D,delete=False) as f:json.dump(payload,f);tmp=Path(f.name)
   try:subprocess.run([str(ROOT/'.venv/bin/python'),str(D/'render_plot.py'),str(tmp)],check=True,stdout=subprocess.DEVNULL)
   finally:tmp.unlink(missing_ok=True)
  refs.append(str(dest))
 return refs,geometry

def _observed_text(spec,p,assets):
 a,b=p['lambda'],p['mu'];target,u,v=spec['names'];n1,n2=spec['path_names'];first,second=spec['segments'];c1=a if n1==u else b;c2=a if n2==u else b;decimal=spec['decimal']
 mag=lambda x:'' if abs(x)==1 else tex(abs(x),decimal)
 values={'prompt_asset':assets[0],'solution_asset':assets[1],
  'length1':first+'='+(tex(abs(c1),decimal) if spec.get('length_dot') else mag(c1))+(r'\cdot ' if spec.get('length_dot') else '')+'|'+n1+'|','length2':second+'='+mag(c2)+'|'+n2+'|',
  'hence1':r'\overset{\to }{'+first+'}='+term(c1,n1,decimal)+'.','hence2':r'\overset{\to }{'+second+'}='+term(c2,n2,decimal)+'.',
  'path_terms':total(c1,c2,n1,n2,decimal),'answer_terms':total(a,b,u,v,decimal,spec['force_one']),
  'lambda_eq':r'\lambda ='+tex(a,decimal),'mu_eq':r'\mu ='+tex(b,decimal),'pair_eq':r'\lambda ='+tex(a,decimal)+r',\,\mu ='+tex(b,decimal)+'.'}
 return slots(spec['prompt'],values),slots(spec['solution'],values)

def _authored_spec(level,field_type):
 # A single equal-workload family per level, names independent of numerical values.
 reverse=level=='hard';names=['r','p','q'];path=['q','p'] if reverse else ['p','q'];segments=['OM','MR'] if reverse else ['OP','PR']
 return {'names':names,'path_names':path,'segments':segments,'decimal':False,'oblique':level!='hard','fields':[{'key':'selection','type':'radio'}] if field_type=='radio' else [{'key':'field-1','type':'blank'},{'key':'field-2','type':'blank'}]}

def _authored_text(spec,p,assets):
 a,b=p['lambda'],p['mu'];target,u,v=spec['names'];n1,n2=spec['path_names'];seg1,seg2=spec['segments'];c1=a if n1==u else b;c2=a if n2==u else b
 if spec['fields'][0]['type']=='radio':request=r'Given that $r=\lambda p+\mu q$, find $\lambda $ and $\mu .$'
 else:request='If $r=\\lambda p+\\mu q$, then$\\,\\lambda =$\n{{field-1}}\nand \n$\\mu =$\n{{field-2}}.'
 problem=f'![]({assets[0]})\n\nConsider the picture above. '+request
 mag=lambda c:('' if abs(c)==1 else tex(abs(c)))
 direction=lambda c,n,seg:f'$\\overset{{\\to }}{{{seg}}}$ and ${n}$ have the same direction' if c>0 else f'$\\overset{{\\to }}{{{seg}}}$ has the opposite direction to ${n}$'
 sol=f'![]({assets[1]})\n\nIn $△{seg1[0]}{seg1[1]}{seg2[1]}$ shown above, we have:\n\n- ${seg1}={mag(c1)}|{n1}|$\n\n- '+direction(c1,n1,seg1)+f'\n\nHence, $\\overset{{\\to }}{{{seg1}}}={term(c1,n1)}.$\n\nSimilarly:\n\n- ${seg2}={mag(c2)}|{n2}|$\n\n- '+direction(c2,n2,seg2)+f'\n\nHence, $\\overset{{\\to }}{{{seg2}}}={term(c2,n2)}.$\n\nAdditionally, \n\n$$\n\\begin{{aligned}}r & =\\overset{{\\to }}{{{seg1}}}+\\overset{{\\to }}{{{seg2}}} \\\\  & ={total(c1,c2,n1,n2)}'
 if n1!=u:sol+=f' \\\\  & ={total(a,b,u,v)}'
 sol+='.'+r'\end{aligned}'+'\n$$\n\n'+f'Consequently, $r=\\lambda p+\\mu q={total(a,b,u,v)}.$\n\nSince $p∦q,$ the linear combination can only be written in one way. Equating the coefficients, we get:\n\n- $\\lambda ={tex(a)}$ and $\\mu ={tex(b)}$'
 return problem,sol

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 rng=random.Random(seed);template=template or 'authored-'+level
 if template in TEMPLATES:
  spec=TEMPLATES[template]
  if spec['level']!=level:raise ValueError('Observed template belongs to '+spec['level'])
 else:
  if template!='authored-'+level:raise ValueError('Unknown template')
  spec=_authored_spec(level,field_type or 'blank')
 kind=spec['fields'][0]['type']
 if field_type and field_type!=kind:raise ValueError('Observed layout cannot change field type')
 profile=profile or ('authored-sign-order' if kind=='radio' else 'no-bank')
 if kind=='blank' and profile!='no-bank':raise ValueError('Blank has no bank profile')
 if kind=='radio' and profile not in ('authored-sign-order','observed-'+template):raise ValueError('Unknown complete bank profile')
 if profile.startswith('observed-') and not spec.get('bank'):raise ValueError('No observed radio profile')
 # Entire bank selected before sampling; collisions reject the whole instance.
 for attempt in range(200):
  p=_parameters(level,rng,template,parameters);a,b=p['lambda'],p['mu']
  if kind=='radio':
   if profile.startswith('observed-'):pairs=[(a*sp.Rational(x['lambda_factor']),b*sp.Rational(x['mu_factor'])) for x in spec['bank']]
   else:pairs=[(a,b),(-a,b),(a,-b),(-a,-b),(b,a)]
   if len(set(pairs))!=len(pairs) or sum(x==(a,b) for x in pairs)!=1:
    if parameters is not None:raise ValueError('Ambiguous complete bank')
    continue
  break
 else:raise ValueError('Cannot sample a complete eligible bank')
 assets,plot=render_plots(p,spec);problem,solution=(_observed_text(spec,p,assets) if template in TEMPLATES else _authored_text(spec,p,assets))
 rawfields=[]
 for f in spec['fields']:
  if f['type']=='radio':values=[f'$\\lambda ={tex(x,spec.get("bank_decimal",spec["decimal"]))}$ and $\\mu ={tex(y,spec.get("bank_decimal",spec["decimal"]))}$' for x,y in pairs];correct=values[pairs.index((a,b))]
  else:correct=tex(a if f['key']=='field-1' else b);values=[correct]
  rawfields.append((f,values,correct))
 identity=digest({'version':VERSION,'level':level,'problem':problem,'solution':solution,'fields':[(f['key'],f['type'],sorted(vals),c) for f,vals,c in rawfields]})
 qid=uid(identity);fields=[]
 for f,vals,c in rawfields:
  fid=uid(qid+'/'+f['key']);answers=[{':answer/id':uid(fid+'/'+val),':answer/type':':answer.type/'+('text' if f['type']=='radio' else 'math'),':answer/value':val} for val in vals]
  correct=next(x[':answer/id'] for x in answers if x[':answer/value']==c)
  if f['type']=='radio':rng.shuffle(answers)
  fields.append({':answer-field/id':fid,':answer-field/key':f['key'],':answer-field/type':':answer-field.type/'+f['type'],':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]})
 return {'knowledge_point':{'db_id':KP,'id':str(NS),'title':RECORD[':knowledge-point/title']},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':fields},'generation':{'version':VERSION,'seed':seed,'template':template,'bank_profile':profile,'parameters':{k:str(v) for k,v in p.items()},'source':{k:CAPTURE[k] for k in ('database','basis','lineage')},'source_id':spec.get('source_id'),'authored':template not in TEMPLATES,'presentation_repair':template=='q-275128','parameter_fingerprint':digest([str(a),str(b),spec['path_names'].index(spec['names'][1]),plot.get('u'),plot.get('v')]),'content_fingerprint':identity,'plot':plot,'domain':{'nonparallel':True,'factor_bound':4,'grid_increment':1}}}

# EASY: positive whole-number length multiples; observed dual blanks retained.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: signed/reordered/half or quarter vector ratios; all source layouts.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored two noninteger readings with reversed path; no extra vector topic.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];lines=[q[':question/problem'],'']
 for f in q[':question/answer-fields']:
  lines.append(f[':answer-field/key']+':')
  lines.extend('- '+a[':answer/value'] for a in f[':answer-field/choices'])
 lines.extend(['','Worked solution:',q[':question/worked-solution']]);return '\n'.join(lines)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');parser.add_argument('--field-type',choices=['blank','radio']);args=parser.parse_args()
 records=[generate(level,args.seed+i,args.template,args.field_type,profile=args.profile) for level in (('easy','moderate','hard') if args.difficulty=='all' else (args.difficulty,)) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
