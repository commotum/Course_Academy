#!/usr/bin/env python3
"""Isolated source-faithful inverse-secant substitution draft with role-based slots."""
import argparse,math,hashlib,importlib.util,itertools,json,random,re,sys,uuid
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
H=Path(__file__).with_suffix('');KP=17592186064250
SOURCE=json.loads((H/'source.json').read_text());KP_UUID=SOURCE['record'][':knowledge-point/id']
CAPACITIES={'easy':22,'moderate':99,'hard':356}
VERSION='3.0.0-draft';GENERATOR_ID=str(uuid.uuid5(uuid.UUID(KP_UUID),'question-generator'))
spec=importlib.util.spec_from_file_location('arcsec_draft_format',H/'math_format.py');fmt=importlib.util.module_from_spec(spec);spec.loader.exec_module(fmt)
EASY_RATIONALS=tuple((p,q) for p in range(1,7) for q in range(1,7) if math.gcd(p,q)==1 and p!=q)
NUMERATORS=range(2,10);SLOPES=range(2,13);RADICANDS=tuple(t for t in range(2,25) if not sp.sqrt(t).is_Integer)
PROFILES={
'q-69476':('moderate','m-prefactor',8,lambda t:(t,t),lambda n,a,b:[(n/2,'sec',n),(1,'sec',n*n),(a/n,'sec',n),(1/n,'sec',n),(2/n,'sec',n/2)],2),
'q-69475':('moderate','m-prefactor',7,lambda t:(t,t),lambda n,a,b:[(a/n,'sec',n),(1/n,'sec',n),(1/n,'sec',n*n),(1/n**2,'sec',n),(1,'sec',n*n)],0),
'q-69477':('moderate','m-prefactor',3,lambda t:(t*t,t),lambda n,a,b:[(1,'sec',n),(a/n,'sec',n),(1/n,'sec',n),(1/n**2,'sec',a),(1,'sec',a)],1),
'q-73715':('moderate','m-prefactor',3,lambda t:(2*t,t),lambda n,a,b:[(1/n,'sec',n),(1/n**2,'sec',n),(a/n,'sec',n),(1/n,'sec',n*n),(1,'sec',n*n)],2),
'q-73716':('moderate','m-unit',4,lambda t:(t,sp.Integer(1)),lambda n,a,b:[(1/n,'sec',n),(1,'sec',n),(n,'sec',n),(1/n,'tan',n),(1,'tan',n)],0),
'q-73717':('hard','h-prefactor',2,lambda t:(t,t),lambda n,a,b:[(a*n,'sec',n),(1/(a*n),'sec',n),(a,'sec',n),(1,'sec',n),(1/a,'sec',n)],2),
'q-114051':('hard','h-root-unit',5,lambda t:(sp.sqrt(t),sp.Integer(1)),lambda n,a,b:[(1,'sec',n),(b,'sec',n),(b,'sec',b),(n,'sec',n),(1,'sec',b)],0),
'q-114052':('hard','h-root-unit',2,lambda t:(sp.sqrt(t),sp.Integer(1)),lambda n,a,b:[(n,'sec',1),(1,'sec',1/n),(1,'sec',n),(n,'sec',n),(b,'sec',n)],2),
'q-114053':('hard','h-root-unit',3,lambda t:(sp.sqrt(t),sp.Integer(1)),lambda n,a,b:[(1,'sec',1/n),(1,'sec',n),(1/n,'sec',1),(1,'sec',b),(n,'sec',1)],1),
'q-114054':('hard','h-root-unit',6,lambda t:(sp.sqrt(t),sp.Integer(1)),lambda n,a,b:[(1/n,'sec',1),(1,'sec',n),(b,'sec',n),(1,'sec',1/n),(n,'sec',1)],1),
'q-114055':('hard','h-root-prefactor',7,lambda t:(sp.sqrt(t),t),lambda n,a,b:[(1,'sec',n),(1,'sec',b),(b*n,'sec',1),(1/n,'sec',1),(a,'sec',n)],4),
'q-114056':('hard','h-root-prefactor',8,lambda t:(sp.sqrt(t),t),lambda n,a,b:[(b*n,'sec',1),(a,'sec',n),(1,'sec',n),(1/n,'sec',1),(b,'sec',1/n)],1),
'q-114057':('hard','h-square-calculate-prefactor',5,lambda t:(2*t,t),lambda n,a,b:[(1,'sec',a*n),(1,'sec',n),(1/a,'sec',n),(a,'sec',n),(a,'sec',1)],3),
'q-49519':('hard','h-denominator',4,lambda t:(t,1/t),lambda n,a,b:[(1/n,'sin',n),(1/n,'tan',n),(n,'sec',n),(2/n,'sec',n*n),(1/n,'sec',n)],4),
'q-49554':('hard','h-denominator',3,lambda t:(t,1/t),lambda n,a,b:[(1/n,'sec',1),(1/n,'sec',n*n),(1/n,'sin',n),(1/n,'sin',n*n),(1/n,'sec',n)],4),
'q-49555':('hard','h-denominator',6,lambda t:(t,1/t),lambda n,a,b:[(1/n,'sin',n),(1/n,'sec',n*n),(1,'sec',n),(1/n,'sec',n),(1,'sec',n*n)],3),
'q-73718':('hard','h-denominator',5,lambda t:(t,1/t),lambda n,a,b:[(n,'tan',n),(1/n,'sec',n),(1/n,'tan',n),(1,'sec',n),(n,'sec',n)],1),
}
ORIGINALS={q[':question/math-academy-id']:q for q in SOURCE['record'][':knowledge-point/questions']}

def strict_int(v,name):
 if type(v) is not int:raise ValueError(name+' must be a built-in integer')

def kind(p):return 'e-direct' if p=='authored-e-direct' else PROFILES[p][1]
def difficulty(p):return 'easy' if p=='authored-e-direct' else PROFILES[p][0]
def source_parameters(p):
 v=PROFILES[p];n,a=v[3](sp.Integer(v[2]));template=v[1]
 if 'root' in template:return {'radicand':int(n*n),**({'numerator':int(a)} if template=='h-root-prefactor' else {})}
 if template=='h-denominator':return {'slope':int(n),'denominator_scale':int(1/a)}
 return {'slope':int(n),**({'numerator':int(a)} if template in ['m-prefactor','h-prefactor','h-square-calculate-prefactor'] else {})}

def all_parameters(p):
 template=kind(p)
 if template=='e-direct':return [{'slope_numerator':a,'slope_denominator':b} for a,b in EASY_RATIONALS]
 if template in ['m-prefactor','h-prefactor','h-square-calculate-prefactor']:
  return [{'slope':n,'numerator':a} for n in SLOPES for a in NUMERATORS]
 if template=='h-denominator':return [{'slope':n,'denominator_scale':d} for n in SLOPES for d in NUMERATORS]
 if template=='h-root-prefactor':return [{'radicand':b,'numerator':a} for b in RADICANDS for a in NUMERATORS]
 if template=='h-root-unit':return [{'radicand':b} for b in RADICANDS]
 return [{'slope':n} for n in SLOPES]

def parameters(p,slots):
 if slots not in all_parameters(p):raise ValueError('Parameters outside declared role bounds')
 for k,v in slots.items():strict_int(v,k)
 template=kind(p);n=sp.Rational(slots['slope_numerator'],slots['slope_denominator']) if template=='e-direct' else sp.sqrt(slots['radicand']) if 'radicand' in slots else sp.Integer(slots['slope'])
 a=sp.Integer(slots.get('numerator',1));d=sp.Integer(slots.get('denominator_scale',1))
 if template=='e-direct':a=n
 c=a/n if template.startswith('m-') or template=='e-direct' else 1/d if template=='h-denominator' else a
 return n,a,d,sp.simplify(c)

def recipe_values(p,n,a,d):
 if p=='authored-e-direct':values=[(1,'sec',n),(n,'sec',n),(1/n,'sec',n),(1,'sec',n*n),(1/n**2,'sec',n)]
 elif kind(p)=='h-denominator':
  # Here the independent supplied denominator scale is d, not the inner slope.
  values={
   'q-49519':[(1/d,'sin',n),(1/d,'tan',n),(d,'sec',n),(2/d,'sec',n*n),(1/d,'sec',n)],
   'q-49554':[(1/d,'sec',1),(1/d,'sec',n*n),(1/d,'sin',n),(1/d,'sin',n*n),(1/d,'sec',n)],
   'q-49555':[(1/d,'sin',n),(1/d,'sec',n*n),(1,'sec',n),(1/d,'sec',n),(1,'sec',n*n)],
   'q-73718':[(d,'tan',n),(1/d,'sec',n),(1/d,'tan',n),(1,'sec',n),(d,'sec',n)]}[p]
 else:values=PROFILES[p][4](n,a,n*n)
 return [(sp.simplify(z),f,sp.simplify(k)) for z,f,k in values]

def triples(p,slots):
 n,a,d,c=parameters(p,slots);return recipe_values(p,n,a,d)

def correct_index(p):return 0 if p=='authored-e-direct' else PROFILES[p][-1]
def eligible(p,slots):
 try:
  n,a,d,c=parameters(p,slots);bank=triples(p,slots)
  return len(set(bank))==5 and bank[correct_index(p)]==(c,'sec',n)
 except ValueError:return False

def tex(e):return sp.latex(sp.sympify(e))
def coefficient(e):return '' if e==1 else tex(e)+r'\,'
def arg(n):return 'x' if n==1 else tex(n)+'x'
def value(v):
 c,f,n=v;return coefficient(c)+r'\text{arc'+f+'}('+arg(n)+')+C'
def mathematical_key(n,c):return 'inverse-secant-integral:'+sp.sstr(sp.simplify(c))+':'+sp.sstr(sp.simplify(n*n))+':x'
def kernel(z):return r'\frac{1}{|'+z+r'|\sqrt{('+z+r')^{2}-1}}'
def integral(k,z='x',outside=sp.Integer(1)):
 return coefficient(outside)+r'\int '+k+r'\,\text{d}'+z

def render(p,slots):
 n,a,d,c=parameters(p,slots);template=kind(p);nx=arg(n);kn=kernel(nx);ku=kernel('u');dx=r'\text{d}x';du=r'\text{d}u'
 if template.startswith('m-') or template=='e-direct':body=r'\frac{'+tex(a)+r'}{|'+nx+r'|\sqrt{('+nx+r')^{2}-1}}'
 elif template=='h-denominator':body=r'\frac{1}{'+tex(d)+r'|x|\sqrt{'+tex(n*n)+r'x^{2}-1}}'
 else:body=r'\frac{'+tex(a)+r'}{|x|\sqrt{'+tex(n*n)+r'x^{2}-1}}'
 I=integral(body)
 basic=r'\int \frac{1}{|u|\sqrt{u^{2}-1}}\text{d}u=\text{arcsec}(u)+C.'
 diff=r'\frac{\text{d}u}{\text{d}x}='+tex(n)+r'\,⟹\,\text{d}x=\frac{1}{'+tex(n)+r'}\text{d}u.'
 def primitive(z,amplitude=c):return coefficient(amplitude)+r'\text{arcsec}('+z+')+C'
 if template=='e-direct':
  diff=r'\frac{\text{d}u}{\text{d}x}='+tex(n)+r'\quad\Longrightarrow\quad '+tex(n)+r'\,\text{d}x=\text{d}u.'
  chain=[I,integral(ku,'u'),primitive('u'),primitive(nx)]
  solution='This resembles the basic integral for $\\text{arcsec},$\n\n$$\n'+basic+'\n$$\n\nLet $u='+nx+'.$ Then\n\n$$\n'+diff+'\n$$\n\nTherefore,\n\n$$\n'+aligned(chain)+'\n$$'
  problem='$'+I+'=$'
 else:
  source=ORIGINALS[p];blocks=re.findall(r'\$\$([\s\S]*?)\$\$',source[':question/worked-solution'])
  if template.startswith('m-'):
   chain=[integral(kn,outside=a),coefficient(a)+r'\int '+ku+r'\cdot (\frac{1}{'+tex(n)+'}'+du+')',integral(ku,'u',c),primitive('u'),primitive(nx)]
   newblocks=([I+'='+integral(kn,outside=a)+'.'] if template=='m-prefactor' else [])+[basic,diff,aligned(chain)]
  else:
   normal=n/d if template=='h-denominator' else a*n
   normalized=integral(kn,outside=normal)
   if template in ['h-root-unit','h-root-prefactor','h-square-calculate-prefactor']:
    # Retain the explicit numerator scaling and uncollapsed cancellation stage.
    normalized=integral(r'\frac{'+tex(normal)+r'}{|'+nx+r'|\sqrt{('+nx+r')^{2}-1}}')
    cancellation=coefficient(normal)+r'\cdot\frac{1}{'+tex(n)+r'}\int '+ku+r'\,\text{d}u'
   else:cancellation=integral(ku,'u',c)
   chain=[I,normalized,coefficient(normal)+r'\int '+ku+r'\cdot (\frac{1}{'+tex(n)+'}'+du+')',cancellation,primitive('u'),primitive(nx)]
   newblocks=[I+'='+normalized+'.',basic,diff,aligned(chain)]
  assert len(blocks)==len(newblocks)
  it=iter(newblocks);solution=re.sub(r'\$\$([\s\S]*?)\$\$',lambda m:'$$\n'+next(it)+'\n$$',source[':question/worked-solution'])
  solution=re.sub(r'\$([^$]*x\.)\$',lambda m:'$'+('u=' if m[1].lstrip().startswith('u=') else '')+nx+'.$',solution)
  raw=source[':question/problem'];problem=raw[:raw.index('$')]+'$'+I+('=' if '=' in raw else '.')+'$'+raw[raw.rindex('$')+1:]
 return fmt.normalize_prose(problem),fmt.normalize_prose(solution)

def aligned(terms):return r'\begin{aligned}'+terms[0]+' &='+r' \\ &='.join(terms[1:])+r'\end{aligned}'

def generate(level,seed=0,*,profile=None,parameters=None):
 strict_int(seed,'seed')
 if level not in ['easy','moderate','hard']:raise ValueError('Invalid difficulty')
 rng=random.Random(seed);profiles=['authored-e-direct'] if level=='easy' else [p for p,v in PROFILES.items() if v[0]==level]
 p=rng.choice(profiles) if profile is None else profile
 if p not in profiles:raise ValueError('Profile/difficulty mismatch')
 if parameters is None:
  while True:
   slots=rng.choice(all_parameters(p))
   if eligible(p,slots):break
 else:slots=dict(parameters)
 if not eligible(p,slots):raise ValueError('Invalid/ambiguous complete bank')
 n,a,d,c=globals()['parameters'](p,slots);bank=triples(p,slots);key=mathematical_key(n,c)
 qid=str(uuid.uuid5(uuid.UUID(GENERATOR_ID),key+':'+p));fid=str(uuid.uuid5(uuid.UUID(qid),'selection'))
 choices=[]
 for v in bank:
  val=fmt.normalize_tex(value(v));choices.append({':answer/id':str(uuid.uuid5(uuid.UUID(fid),val)),':answer/type':':answer.type/math',':answer/value':val})
 problem,solution=render(p,slots)
 q={':question/id':qid,':question/problem':problem+'\n\n{{selection}}',':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',choices[correct_index(p)][':answer/id']]}]}
 meta={'generator_id':GENERATOR_ID,'version':VERSION,'seed':seed,'template':kind(p),'profile':p,'parameters':slots,'derived':{'slope':str(n),'numerator':str(a),'denominator_scale':str(d),'normalized_amplitude':str(c)},'mathematical_key':key,'source_question_ids':[] if level=='easy' else [ORIGINALS[p][':db/id']],'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'authored_extension':level=='easy','domain':'Real x with |slope*x|>1; principal real arcsec. Each connected component has an independent arbitrary constant C.','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':[],'answer_recipes':[[str(z),f,str(k)] for z,f,k in bank]}
 return fmt.validate_generated_record({'knowledge_point':{'db_id':KP,'id':KP_UUID,'title':SOURCE['record'][':knowledge-point/title']},'question':q,'generation':meta})

def batch(level,count,seed):
 strict_int(count,'count');strict_int(seed,'seed')
 if count<=0:raise ValueError('count must be positive')
 if level not in ['easy','moderate','hard','all']:raise ValueError('Invalid difficulty')
 levels=['easy','moderate','hard'] if level=='all' else [level]
 for lev in levels:
  if count>CAPACITIES[lev]:raise ValueError(f'Requested {count} {lev} tasks exceeds validated finite capacity {CAPACITIES[lev]}')
 result=[]
 for lev in levels:
  rng=random.Random(seed);profiles=['authored-e-direct'] if lev=='easy' else [p for p,v in PROFILES.items() if v[0]==lev];used=set();rows=[]
  for attempt in range(100000):
   p=rng.choice(profiles);slots=rng.choice(all_parameters(p))
   if not eligible(p,slots):continue
   r=generate(lev,seed,profile=p,parameters=slots);key=r['generation']['mathematical_key']
   if key in used:continue
   used.add(key);rows.append(r)
   if len(rows)==count:break
  if len(rows)!=count:raise ValueError('Requested count exceeds bounded distinct task capability')
  result+=rows
 return result

def markdown(r):
 q=r['question'];return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',required=True,choices=['easy','moderate','hard','all']);p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['json','markdown'],default='json');args=p.parse_args()
 if args.count<=0:p.error('count must be positive')
 rows=batch(args.difficulty,args.count,args.seed);print(json.dumps(rows,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,rows)))
