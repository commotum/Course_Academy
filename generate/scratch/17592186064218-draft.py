#!/usr/bin/env python3
"""Source-faithful inverse-sine profiles and bounded authored combined normalization.

Only sibling draft assets are imported; registered numeric package is immutable.
Source originals remain raw evidence. Every source bank is selected as a whole.
"""
import argparse,hashlib,json,random,re,sys,uuid,copy,importlib.util
sys.dont_write_bytecode=True
from pathlib import Path
import sympy as sp
KP_ID=17592186064218
H=Path(__file__).with_suffix('');SOURCE=json.loads((H/'source.json').read_text())
KP_UUID=SOURCE['record'][':knowledge-point/id'];TITLE=SOURCE['record'][':knowledge-point/title']
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'));VERSION='inverse-sine-substitution-v2-draft'
SUPPORTED_LEVELS=('easy','moderate','hard')
_spec=importlib.util.spec_from_file_location('inverse_sine_private_formatter',H/'math_format.py');_fmt=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_fmt)
normalize_prose=_fmt.normalize_prose;normalize_tex=_fmt.normalize_tex
_spec=importlib.util.spec_from_file_location('inverse_sine_private_parser',H/'math_parser.py');_parser=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(_parser)
X=_parser.X;U=_parser.U;C=_parser.C
def builtin_int(value,name):
 if type(value) is not int:raise ValueError(name+' must be a builtin int, excluding bool')
def source_record(source_id,raw=False):
 if type(source_id) is not str or type(raw) is not bool:raise ValueError('source_id/raw types')
 if source_id not in ORIGINALS:raise ValueError('Unknown source')
 return copy.deepcopy(ORIGINALS[source_id])
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}
# level, Markdown/value template, observed t, numeric slot recipes.
# Source bank values are structural templates, not a pool of inferred errors.
PROFILES={
 'q-2505':('easy','unit-square-equality',2,lambda t:{2:t,4:t*t}),
 'q-2506':('easy','unit-square-equality',3,lambda t:{3:t,9:t*t}),
 'q-49535':('easy','scaled-square-equality',4,lambda t:{2:t//2,4:t,16:t*t}),
 'q-114022':('easy','equal-numerator-calculate',5,lambda t:{5:t,25:t*t}),
 'q-114023':('easy','reciprocal-numerator-calculate',6,lambda t:{6:t,36:t*t}),
 'q-114025':('easy','reciprocal-numerator-calculate',9,lambda t:{9:t,81:t*t}),
 'q-114024':('easy','root-square-numerator-calculate',2,lambda t:{2:t,4:t*t}),
 'q-114027':('easy','root-fixed-numerator-calculate',3,lambda t:{3:t}),
 'q-114032':('easy','root-equal-numerator-calculate',3,lambda t:{3:t}),
 'q-2503':('moderate','unit-constant-equality',3,lambda t:{3:t,9:t*t}),
 'q-4334':('moderate','unit-constant-equality',6,lambda t:{2:t//3,3:t//2,6:t,36:t*t}),
 'q-49547':('moderate','fixed-numerator-equality',7,lambda t:{7:t,49:t*t}),
 'q-114030':('moderate','fixed-numerator-calculate',5,lambda t:{5:t,25:t*t}),
 'q-73712':('moderate','rational-numerator-equality',2,lambda t:{2:t,4:t*t,8:t**3}),
}
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def uid(s):return str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),s))
def mathematical_fingerprint(profile,t):
 t=sp.Integer(t);level=PROFILES[profile][0]
 if level=='moderate':
  amplitude={'q-2503':1,'q-4334':1,'q-49547':3,'q-114030':2,'q-73712':t**3/3}[profile];constant=t*t;square=1
 else:
  constant=1;square=t if profile in ('q-114024','q-114027','q-114032')else t*t
  amplitude={'q-2505':1,'q-2506':1,'q-49535':2,'q-114022':t,'q-114023':1/t,'q-114025':1/t,'q-114024':t*t,'q-114027':8,'q-114032':t}[profile]
 return digest(sp.sstr(sp.simplify(amplitude/sp.sqrt(constant)))+'|'+sp.sstr(sp.Rational(square,constant)))

def domain(profile):
 if profile=='q-49535':return (4,) # repeated numeric slots have incompatible roles; replay/completion only
 if profile=='q-4334':return (6,12,18,24)
 if profile=='q-73712':return (2,3,4)
 if profile=='q-49547':return tuple(t for t in range(2,13)if t!=9) # 3/t and 1/3 collide at t=9
 if profile in ('q-114024','q-114027','q-114032'):return (2,3,5,6,7,8,10,11,12)
 return tuple(range(2,13))
def candidates(profile):return [{'t':t}for t in domain(profile)]
def transform(s,mapping):
 # Exponents, including the source arcsec-square alternative, are not slots.
 protected=[]
 def hold(m):protected.append(m[0]);return '@POWER'+chr(65+len(protected)-1)+'@'
 s=re.sub(r'\^\{\d+\}|\^\d+',hold,s)
 s=re.sub(r'(?<!\d)\d+(?!\d)',lambda m:str(mapping.get(int(m[0]),int(m[0]))),s)
 for i,value in enumerate(protected):s=s.replace('@POWER'+chr(65+i)+'@',value)
 return s

def generate(difficulty,seed=0,template=None,parameters=None,*,profile=None,replay=False):
 builtin_int(seed,'seed')
 if type(difficulty) is not str or difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 for selector in (profile,template):
  if selector is not None and type(selector) is not str:raise ValueError('Profile must be str')
 if type(replay) is not bool:raise ValueError('replay must be bool')
 if template is not None and profile is not None and template!=profile:raise ValueError('Conflicting profile selectors')
 if difficulty=='hard':return authored_hard(seed,profile or template,parameters,replay)
 profile=profile or template
 rng=random.Random(seed)
 available=[p for p,v in PROFILES.items()if v[0]==difficulty]
 profile=profile or rng.choice(available)
 if profile not in PROFILES or PROFILES[profile][0]!=difficulty:raise ValueError('Profile/level mismatch')
 if replay and (parameters is None or parameters!={'t':PROFILES[profile][2]}):raise ValueError('Raw evidence replay requires original parameters')
 if parameters is None:parameters={'t':rng.choice(domain(profile))}
 if type(parameters) is not dict or set(parameters)!={'t'}or type(parameters['t']) is not int or parameters['t']not in domain(profile):raise ValueError('Outside bounded profile domain')
 t=parameters['t'];old=ORIGINALS[profile];mapping=PROFILES[profile][3](t)
 problem=transform(old[':question/problem'],mapping);solution=transform(old[':question/worked-solution'],mapping)
 if profile=='q-49535'and not replay:
  # Source first displayed integral loses its numerator. Preserve raw replay.
  solution=solution.replace(rf'\int \frac{{1}}{{\sqrt{{1-{t*t}',rf'\int \frac{{{t//2}}}{{\sqrt{{1-{t*t}',1)
 if not replay:
  problem=normalize_prose(problem);solution=normalize_prose(solution)
 qid=uid(VERSION+'|'+profile+'|'+str(t)+'|'+str(replay));fid=uid(qid+'|0')
 f=old[':question/answer-fields'][0];values=[transform(a[':answer/value'],mapping)for a in f[':answer-field/choices']]
 if not replay:values=list(map(normalize_tex,values))
 if len(set(values))!=5:raise ValueError('Colliding bank')
 answers=[{':answer/id':uid(fid+'|'+v),':answer/type':':answer.type/math',':answer/value':v}for v in values]
 correct=transform(f[':answer-field/correct'][':answer/value'],mapping)
 if not replay:correct=normalize_tex(correct)
 q={':question/id':qid,':question/problem':problem+(''if replay else '\n\n{{0}}'),':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/type':':answer-field.type/radio',':answer-field/key':'0',':answer-field/choices':answers,':answer-field/correct':[':answer/id',next(a[':answer/id']for a in answers if a[':answer/value']==correct)]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':PROFILES[profile][1],'profile':profile,'parameters':{'t':t},'source_question_id':old[':db/id'],'source_math_academy_id':profile,'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'domain':'real x; radicand strictly positive, principal arcsin','sampling':'positive bounded source-related slots; nonsquare root profiles','evidence_only':replay,'eligible_for_learning':not replay,'replay':replay,'repairs':['opening-integral-numerator']if profile=='q-49535'and not replay else [],'mathematical_fingerprint':mathematical_fingerprint(profile,t),'numeric_slot_recipes':{str(k):v for k,v in mapping.items()},'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':[]}}
def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
HARD_PROFILE='authored-combined-normalization'
HARD_DOMAIN={'n':tuple(range(2,8)),'m':(2,3,5,6,7),'a':tuple(range(2,10)),'d':(2,3,4,5)}
def authored_hard(seed,profile=None,parameters=None,replay=False):
 if replay:raise ValueError('Authored profile has no source replay')
 if profile not in (None,HARD_PROFILE):raise ValueError('Unknown hard profile')
 rng=random.Random(seed)
 if parameters is None:
  parameters={key:rng.choice(values)for key,values in HARD_DOMAIN.items()}
  while parameters['n']==parameters['m']:parameters={key:rng.choice(values)for key,values in HARD_DOMAIN.items()}
 if type(parameters) is not dict or set(parameters)!=set(HARD_DOMAIN):raise ValueError('Expected hard slots n,m,a,d')
 for key,value in parameters.items():
  builtin_int(value,key)
  if value not in HARD_DOMAIN[key]:raise ValueError('Outside hard slot bounds')
 if parameters['n']==parameters['m']:raise ValueError('n=m collides two authored distractors')
 n,m,a,d=[sp.Integer(parameters[k])for k in ('n','m','a','d')]
 k=sp.sqrt(m)/n;amplitude=a/d;coef=amplitude/sp.sqrt(m)
 tex=lambda z:sp.latex(z).replace(r'\operatorname{asin}',r'\operatorname{arcsin}')
 original=rf'\frac{{{a}}}{{{d}\sqrt{{{n*n}-{m}x^{{2}}}}}}'
 normalized=rf'\frac{{{a}}}{{{d*n}}}\int \frac{{1}}{{\sqrt{{1-({tex(k*X)})^{{2}}}}}}\,\text{{d}}x'
 transformed=rf'\frac{{{a}}}{{{d*n}}}\int \frac{{1}}{{\sqrt{{1-u^{{2}}}}}}\cdot ({tex(1/k)}\,\text{{d}}u)'
 primitive=coef*sp.asin(k*X)
 values=[primitive,a/(d*n)*sp.asin(k*X),a/(d*m)*sp.asin(k*X),coef*sp.asin(m*X/n),coef*sp.asin(X/n)]
 values=[normalize_tex(tex(z)+'+C')for z in values]
 problem=normalize_prose(rf'Calculate $\int {original}\,\text{{d}}x.$'+'\n\n{{0}}')
 solution=normalize_prose("Let's rewrite our integral as follows:\n\n$$\n"+rf'\int {original}\,\text{{d}}x={normalized}'+"\n$$\n\nThis integral resembles the basic integral for inverse sine,\n\n$$\n"+r'\int \frac{1}{\sqrt{1-u^{2}}}\,\text{d}u=\operatorname{arcsin}(u)+C.'+"\n$$\n\n"+rf"So, let's substitute $u={tex(k*X)}.$ Differentiating, we get"+"\n\n$$\n"+rf'\frac{{\text{{d}}u}}{{\text{{d}}x}}={tex(k)}\,⟹\,\text{{d}}x={tex(1/k)}\,\text{{d}}u.'+"\n$$\n\nUsing the above, we can write the integral in terms of $u$ and evaluate:\n\n$$\n"+rf'\begin{{aligned}}\int {original}\,\text{{d}}x & ={normalized} \\ & ={transformed} \\ & ={tex(coef)}\int \frac{{1}}{{\sqrt{{1-u^{{2}}}}}}\,\text{{d}}u \\ & ={tex(coef*sp.asin(U))}+C \\ & ={tex(primitive)}+C\end{{aligned}}'+"\n$$")
 qid=uid(VERSION+'|'+HARD_PROFILE+'|'+json.dumps(parameters,sort_keys=True));fid=uid(qid+'|0')
 answers=[{':answer/id':uid(fid+'|'+v),':answer/type':':answer.type/math',':answer/value':v}for v in values]
 q={':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/hard',':question/answer-fields':[{':answer-field/id':fid,':answer-field/type':':answer-field.type/radio',':answer-field/key':'0',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[0][':answer/id']]}]}
 e=amplitude/sp.sqrt(n*n-m*X**2)
 task=digest(sp.sstr(a/(d*n))+'|'+sp.sstr(m/(n*n)))
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'generator_id':GENERATOR_UUID,'version':VERSION,'seed':seed,'template':HARD_PROFILE,'profile':HARD_PROFILE,'parameters':dict(parameters),'source_basis':SOURCE['basis'],'source_lineage':SOURCE['lineage'],'source_question_ids':['q-114024','q-114027','q-73712'],'relationship_to_source_templates':'Authored combination of observed nonsquare x coefficient and constant-radicand/fractional numerator normalization; unchanged linear substitution and inverse-sine primitive stages.','domain':f'real x in (-{n}/sqrt({m}), {n}/sqrt({m})); positive square root and principal arcsin; arbitrary real C','evidence_only':False,'eligible_for_learning':True,'authored':True,'recipes':['correct','a/(d*n)*asin(sqrt(m)*x/n)','a/(d*m)*asin(sqrt(m)*x/n)','a/(d*sqrt(m))*asin(m*x/n)','a/(d*sqrt(m))*asin(x/n)'],'mathematical_fingerprint':task,'dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':[]}}

def batch(difficulty,count=5,seed=0):
 builtin_int(seed,'seed');builtin_int(count,'count')
 if count<1:raise ValueError('positive count required')
 if type(difficulty) is not str or difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty')
 rng=random.Random(seed);out=[];seen=set()
 if difficulty=='hard':
  if count>960:raise ValueError('Bounded output exhausted')
  import itertools
  selected=[dict(zip(HARD_DOMAIN,vs))for vs in itertools.product(*HARD_DOMAIN.values())if vs[0]!=vs[1]];rng.shuffle(selected)
  for params in selected:
   rec=generate('hard',seed,parameters=params);key=rec['generation']['mathematical_fingerprint']
   if key not in seen:out.append(rec);seen.add(key)
   if len(out)==count:return out
 else:
  selected=[(p,t)for p,v in PROFILES.items()if v[0]==difficulty for t in domain(p)];rng.shuffle(selected)
  for p,t in selected:
   key=mathematical_fingerprint(p,t)
   if key not in seen:out.append(generate(difficulty,seed,p,{'t':t}));seen.add(key)
   if len(out)==count:return out
 raise ValueError('Bounded output exhausted')
def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' [correct]'if a[':answer/id']==f[':answer-field/correct'][1]else '')for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
_unchecked_generate=generate
_checked_generate=_fmt.checked_math_content(generate)
def generate(*args,**kwargs):
 if kwargs.get('replay') is True:return _unchecked_generate(*args,**kwargs)
 return _checked_generate(*args,**kwargs)

def main():
 p=argparse.ArgumentParser();p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=5);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args()
 if a.count<1:p.error('positive count required')
 rows=[r for level in (SUPPORTED_LEVELS if a.difficulty=='all'else[a.difficulty])for r in batch(level,a.count,a.seed)]
 print(json.dumps(rows,indent=2,ensure_ascii=False)if a.format=='json'else '\n\n---\n\n'.join(map(markdown,rows)))
if __name__=='__main__':main()
