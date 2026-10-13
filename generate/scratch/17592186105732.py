#!/usr/bin/env python3
"""Given-vector triangle/parallelogram area, basis 1356; no database operations.

Observed source bank profiles are scaling-ray evidence recipes ONLY. Their scalar
patterns do not identify the author's mistakes; default banks instead assess
omitted squares and omitted area-halving. Exact source layout is parameterized
by component/minor/product/norm nodes, never returned as a stored question.
Hard is authored: primitive dense signed integer given vectors, same determinant,
magnitude and half-area method, without vertex subtraction/altitude/new branches.
API generate(level, seed, template, field_type, parameters, profile); explicit
invalid parameters reject. Changing order/seed never changes content identity.
"""
from __future__ import annotations
import argparse, hashlib, json, math, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186105732
KP_UUID='f88dd688-449b-5a6d-8b91-78d00d0c932b'
TITLE='Calculating the Area of the Triangle Spanned by Two Vectors'
VERSION='given-vector-area-1'
PROVENANCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
# Templates split by genuine response/row structure; dot operand order is a style.
TEMPLATES={
 'parallelogram_radio_radical':('easy','radio',False,'radical'),
 'parallelogram_radio_simplified':('easy','radio',False,'simplified'),
 'parallelogram_radio_unrated':('easy','radio',False,'radical'),
 'parallelogram_blank_direct':('easy','blank',False,'direct'),
 'parallelogram_blank_expanded':('easy','blank',False,'expanded'),
 'triangle_radio_radical':('moderate','radio',True,'radical'),
 'triangle_blank_direct':('moderate','blank',True,'direct'),
 'triangle_blank_expanded':('moderate','blank',True,'expanded'),
 'triangle_hard_radio':('hard','radio',True,'expanded'),
 'triangle_hard_blank':('hard','blank',True,'expanded'),
}
# Baselines describe domains of observed-pattern recipes, not answer lookups.
# Values are sqrt(radicand)*coefficient, scaled by the product of vector scales.
SOURCE_SPECS={
 'q-19983':('triangle_radio_radical',[1,3,2],[4,1,-2],'a','b','ba',[(273,1,2),(285,1,2),(825,1,2),(177,1,1),(582,1,2)]),
 'q-20003':('parallelogram_radio_unrated',[-2,-3,-1],[1,2,1],'a','b','ab',[(3,3,2),(3,1,2),(2,1,2),(2,3,2),(3,1,1)]),
 'q-18580':('triangle_radio_radical',[1,-2,3],[0,1,-2],'r','t','ab',[(6,1,1),(3,1,2),(6,1,2),(3,2,1),(6,2,1)]),
 'q-19981':('parallelogram_radio_radical',[2,1,-1],[1,2,0],'u','v','ba',[(14,1,2),(14,1,3),(14,1,1),(7,1,1),(7,1,2)]),
 'q-19997':('parallelogram_radio_simplified',[1,1,-2],[3,2,1],'f','g','ba',[(3,3,1),(5,3,1),(5,2,3),(3,5,2),(3,5,1)]),
 'q-20004':('parallelogram_radio_simplified',[2,0,3],[4,1,3],'h','l','ba',[(3,1,2),(2,1,2),(1,7,2),(1,5,1),(1,7,1)]),
 'q-275220':('parallelogram_blank_direct',[-4,-2,1],[0,-2,-1],'a','b','ba',None),
 'q-275222':('triangle_blank_direct',[-2,-1,0],[-4,2,-2],'a','b','ba',None),
 'q-316345':('parallelogram_blank_expanded',[-3,5,0],[4,-1,2],'a','b','ab',None),
 'q-316350':('parallelogram_blank_expanded',[1,0,0],[0,3,4],'a','b','ab',None),
 'q-316355':('triangle_blank_expanded',[0,5,-1],[6,0,1],'p','q','ab',None),
}
BANK_PROFILES={s:{'template':v[0],'origin':'observed-pattern','scope':'scaling rays only; scalar error intent unresolved'} for s,v in SOURCE_SPECS.items() if v[-1]}
BANK_PROFILES['authored_omitted_squares']={'origin':'authored','scope':'whole four-recipe bank'}
class SampleRejected(ValueError):pass

def tex(e):return sp.latex(sp.simplify(e)).replace(' ', '')
def fingerprint(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def block(x):return '\n$$\n'+x+'\n$$'
def scalar(n):return '('+str(n)+')' if n<0 else str(n)
def vector(v):return '⟨'+','.join(map(str,v))+'⟩'
def determinant(rows):return r'|\begin{aligned}'+r' \\ '.join(' & '.join(map(str,r)) for r in rows)+r'\end{aligned}|'
def cross(a,b):return list(sp.Matrix(a).cross(sp.Matrix(b)))
def reduced(v):
 d=math.gcd(*v)
 return tuple(x//d for x in v) if d else tuple(v)
def task_key(p,triangle):
 # Swapping vectors or reversing either sign gives the same assessed area task.
 # Preserve magnitudes: scaling changes the given area; variable letters do not.
 def signcanon(v):return min(tuple(v),tuple(-x for x in v))
 return fingerprint({'vectors':sorted([signcanon(p['a']),signcanon(p['b'])]),'triangle':triangle})
def validate_parameters(level,p,profile):
 if set(p)!={'a','b','names','order'}:raise ValueError('Expected a,b,names,order parameters')
 for v in (p['a'],p['b']):
  if len(v)!=3 or any(type(n)!=int for n in v):raise ValueError('Three integer coordinates required')
 if p['names'] not in [['a','b'],['r','t'],['u','v'],['f','g'],['h','l'],['p','q']]:raise ValueError('Unsupported names')
 if p['order'] not in ('ab','ba'):raise ValueError('Unknown product order')
 c=cross(p['a'],p['b'])
 if not any(c):raise SampleRejected('Degenerate given vectors')
 if profile in SOURCE_SPECS:
  spec=SOURCE_SPECS[profile]
  for supplied,base in zip((p['a'],p['b']),spec[1:3]):
   scale=None
   for x,y in zip(supplied,base):
    if y:
     r=sp.Rational(x,y)
     if scale is None:scale=r
     elif scale!=r:raise ValueError('Observed scalar patterns support source scaling rays only')
    elif x:raise ValueError('Observed scalar patterns support source scaling rays only')
   if not scale or scale.q!=1 or abs(scale)>3:raise ValueError('Source scaling bound is nonzero integer |scale|<=3')
  return
 bound=5 if level=='easy' else 6
 if any(abs(n)>bound for v in (p['a'],p['b']) for n in v):raise ValueError('Coordinate bounds exceeded')
 if level=='easy' and (max(map(abs,c))>30 or sum(x*x for x in c)>1800):raise ValueError('Easy evaluated workload exceeds bounds')
 if level=='moderate' and (max(map(abs,c))>45 or sum(x*x for x in c)>4000):raise ValueError('Moderate evaluated workload exceeds bounds')
 if level=='hard':
  flat=p['a']+p['b']
  if any(n==0 for n in flat) or sum(abs(n)>=2 for n in flat)<4 or not any(n<0 for n in flat):raise ValueError('Hard requires six nonzero signed coordinates, four |n|>=2')
  if any(math.gcd(*v)!=1 for v in (p['a'],p['b'])):raise ValueError('Hard requires primitive reduced given vectors')
  if any(x==0 for x in c) or max(map(abs,c))<8:raise ValueError('Hard cross-product workload reduced')
  if sum(x*x for x in c)>20000:raise ValueError('Hard magnitude workload too large')

def worked(p,triangle,style,template):
 a,b=p['a'],p['b'];u,v=p['names']; c=list(map(int,cross(a,b))); n=sum(x*x for x in c); magnitude=sp.sqrt(n)
 minors=[([a[1],a[2]],[b[1],b[2]]),([a[0],a[2]],[b[0],b[2]]),([a[0],a[1]],[b[0],b[1]])]
 det=determinant([['i','j','k'],a,b])
 minor=determinant(minors[0])+'i-'+determinant(minors[1])+'j+'+determinant(minors[2])+'k'
 terms=[]
 for top,bottom in minors:
  x,y=top;z,w=bottom
  first=scalar(x)+r'\cdot '+scalar(w)
  second=(scalar(y)+r'\cdot '+scalar(z)) if p['order']=='ab' else (scalar(z)+r'\cdot '+scalar(y))
  terms.append('('+first+'-'+second+')')
 products=terms[0]+'i-'+terms[1]+'j+'+terms[2]+'k'
 coeff=[]
 for x,letter in zip(c,'ijk'):
  if x==0 and template!='parallelogram_blank_expanded':continue
  value=(str(abs(x)) if abs(x)!=1 else '')+letter
  if x==0:value='0'+letter
  coeff.append(('-' if x<0 else '+' if coeff else '')+value)
 basis=''.join(coeff)
 sq='+'.join((scalar(x) if x<0 else '{'+str(x)+'}')+'^{2}' for x in c)
 rows=[u+r'\times '+v+' & ='+det,' & ='+minor,' & ='+products,' & ='+basis,' & ='+vector(c)+'.']
 solution='Using the formula, we have\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
 norms=['A & ='+r'|\,'+u+r'\times '+v+r'\,|',' & ='+r'\sqrt{'+sq+'}']
 if style=='expanded':norms.append(' & ='+r'\sqrt{'+ '+'.join(str(x*x) for x in c)+'}')
 if style in ('radical','simplified','expanded'):norms.append(' & ='+r'\sqrt{'+str(n)+'}')
 if style in ('direct','simplified','expanded'):
  # Source expansion omits redundant final simplification when no factor exists.
  if style=='direct' or tex(magnitude)!=r'\sqrt{'+str(n)+'}':norms.append(' & ='+tex(magnitude))
 norms[-1]+='.'
 solution+='\n\nTherefore, the area of the corresponding parallelogram is\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(norms)+r'\end{aligned}'+'\n$$'
 if triangle:
  half=sp.simplify(magnitude/2)
  expression=r'{A}_{△}=\frac{1}{2}A='
  mt=tex(magnitude)
  expression+=(r'\frac{'+mt+'}{2}' if magnitude.is_Integer is not True or int(magnitude)%2==0 else tex(half))
  if sp.simplify(half)!=sp.Mul(magnitude,sp.Rational(1,2),evaluate=False) or (not magnitude.is_Integer and mt[0].isdigit()):
   if expression.split('=')[-1]!=tex(half):expression+='='+tex(half)
  solution+='\n\nThe area of the triangle is half of the area of the respective parallelogram. So, the area of the triangle is\n\n$$\n'+expression+'.\n$$'
 return solution,{'cross':c,'radicand':n,'magnitude':str(magnitude),'area':str(sp.simplify(magnitude/(2 if triangle else 1))),'products':products,'minors':minor,'norm_rows':norms}

def prompt(p,triangle,kind,template):
 a,b=p['a'],p['b'];u,v=p['names'];shape='triangle' if triangle else 'parallelogram'
 area='${A}_{△}$' if triangle else '$A$'
 if template=='parallelogram_radio_unrated':
  # Complete slots preserve the observed spaces; never replace scalar substrings.
  av='⟨ '+str(a[0]).replace('-','- ')+','+str(a[1])+','+str(a[2])+'⟩'
  bv='⟨'+str(b[0])+', '+str(b[1])+', '+str(b[2])+'⟩'
  return 'Calculate the area of the parallelogram spanned by $'+u+' = '+av+'$ and $'+v+' = '+bv+'$.'
 text='Calculate the area '+(area+' ' if kind=='blank' else '')+'of the '+shape+' spanned by $'+u+'='+vector(a)+'$ and $'+v+'='+vector(b)+'.$'
 if kind=='blank':text+='\n\n'+area[:-1]+'=${{field-1}}'
 return text

def bank(p,triangle,profile):
 c=cross(p['a'],p['b']);n=sum(x*x for x in c);correct=sp.sqrt(n)/(2 if triangle else 1)
 if profile in SOURCE_SPECS:
  baseline=SOURCE_SPECS[profile];scales=[]
  for supplied,base in zip((p['a'],p['b']),baseline[1:3]):
   i=next(i for i,x in enumerate(base) if x);scales.append(sp.Rational(supplied[i],base[i]))
  scale=abs(scales[0]*scales[1])
  values=[scale*sp.Rational(num,den)*sp.sqrt(rad) for rad,num,den in baseline[-1]]
  recipes=[{'operation':'observed scalar radical pattern times absolute product of uniform vector scales','radicand':r,'numerator':num,'denominator':den,'interpretation':'unresolved original error intent; replay-domain only'} for r,num,den in baseline[-1]]
 else:
  values=[correct,sp.sqrt(n) if triangle else sp.sqrt(n)/2]+[sp.sqrt(n-c[i]*c[i])/(2 if triangle else 1) for i in range(3)]
  recipes=[{'operation':'correct cross-product norm with area factor'}, {'operation':'omit triangle halving' if triangle else 'halve parallelogram area'}]+[{'operation':'omit squared cross component','component':i} for i in range(3)]
 if any(v<=0 for v in values) or len(set(map(sp.simplify,values)))!=5:raise SampleRejected('Reject entire bank: domain or mathematical equivalence collision')
 if sum(sp.simplify(x-correct)==0 for x in values)!=1:raise SampleRejected('Bank lacks unique correct answer')
 return values,recipes

def sample(level,rng):
 limit=5 if level=='easy' else 6
 return {'a':[rng.randint(-limit,limit) for _ in range(3)],'b':[rng.randint(-limit,limit) for _ in range(3)],'names':rng.choice([['a','b'],['r','t'],['p','q']]),'order':'ab'}

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('Unknown difficulty')
 if profile in SOURCE_SPECS and not SOURCE_SPECS[profile][-1]:raise ValueError('Blank source has no bank profile')
 if profile in SOURCE_SPECS:
  implied=SOURCE_SPECS[profile][0]
  if template and template!=implied:raise ValueError('Profile/template mismatch')
  template=implied
 elif profile not in (None,'authored_omitted_squares'):raise ValueError('Unknown profile')
 eligible=[t for t,s in TEMPLATES.items() if s[0]==level and (field_type is None or s[1]==field_type)]
 if template and template not in eligible:raise ValueError('Template/difficulty/field mismatch')
 if not eligible:raise ValueError('Unsupported field type/difficulty')
 rng=random.Random(seed);template=template or rng.choice(eligible)
 _,kind,triangle,style=TEMPLATES[template]
 profile=profile or ('authored_omitted_squares' if kind=='radio' else None)
 if profile=='authored_omitted_squares' and kind!='radio':raise ValueError('Bank profile requires radio')
 if parameters is not None:
  p={**parameters,'names':parameters.get('names',['a','b']),'order':parameters.get('order','ab')}
 else:p=None
 for attempt in range(1000):
  if p is not None:candidate=p
  elif profile in SOURCE_SPECS:
   spec=SOURCE_SPECS[profile];sa=rng.choice([-3,-2,-1,1,2,3]);sb=rng.choice([-3,-2,-1,1,2,3])
   candidate={'a':[sa*x for x in spec[1]],'b':[sb*x for x in spec[2]],'names':list(spec[3:5]),'order':spec[5]}
  else:candidate=sample(level,rng)
  try:
   validate_parameters(level,candidate,profile)
   n=sum(x*x for x in cross(candidate['a'],candidate['b']))
   if style in ('simplified','expanded','direct') and tex(sp.sqrt(n))==r'\sqrt{'+str(n)+'}':raise SampleRejected('Template requires actual norm simplification')
   if profile not in SOURCE_SPECS and style=='radical' and (n<=1 or any(n%(i*i)==0 for i in range(2,math.isqrt(int(n))+1))):raise SampleRejected('Radical template requires squarefree norm radicand >1')
   solution,stages=worked(candidate,triangle,style,template)
   correct=sp.sympify(stages['area'])
   if kind=='radio':values,recipes=bank(candidate,triangle,profile)
   else:values,recipes=[correct],[{'operation':'correct cross-product norm with area factor'}]
  except ValueError:
   if p is not None:raise
   continue
  problem=prompt(candidate,triangle,kind,template)
  content=fingerprint({'version':VERSION,'problem':problem,'solution':solution,'bank':sorted(map(tex,values)),'kind':kind})
  qid=str(uuid.uuid5(uuid.NAMESPACE_URL,KP_UUID+'/'+content)); key='selection' if kind=='radio' else 'field-1';fid=str(uuid.uuid5(uuid.UUID(qid),key))
  answers=[];recipe_map={}
  for value,recipe in zip(values,recipes):
   aid=str(uuid.uuid5(uuid.UUID(fid),tex(value)));answers.append({':answer/id':aid,':answer/type':':answer.type/math',':answer/value':tex(value)})
   recipe_map[aid]=recipe
   if sp.simplify(value-correct)==0:correct_id=aid
  rng.shuffle(answers)
  return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/difficulty':':question.difficulty/'+level,':question/problem':problem,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/'+kind,':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':candidate,'bank_profile':profile,'bank_origin':'observed-pattern' if profile in SOURCE_SPECS else 'authored' if kind=='radio' else 'no-bank','authored_extension':level=='hard','source_analysis':{**PROVENANCE,'question_ids':[profile] if profile in SOURCE_SPECS else [sid for sid,spec in SOURCE_SPECS.items() if spec[0]==template],'method_reference_ids':['e-4344','q-19983','q-316355']},'source_repair':{'inferred_missing_correct':True,'authored_easy_assignment':True,'authored_worked_solution':True} if profile=='q-20003' else {},'plot_rating':'none','plot_assets':{},'parameter_fingerprint':task_key(candidate,triangle),'content_fingerprint':content,'stages':stages,'recipes':recipe_map,'sympy_version':sp.__version__}}
 raise SampleRejected('Bounded full-bank sampler exhausted')

# EASY: observed parallelogram norm; integer coordinates |n|<=5.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: observed triangle adds half-area, integer coordinates |n|<=6.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored dense primitive signed vectors, same six-product determinant.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];g=r['generation'];f=q[':question/answer-fields'][0]
 text='## Generated '+q[':question/difficulty'].split('/')[-1]+' — '+g['template']+'\n\n'+q[':question/problem']+'\n\n'
 for a in f[':answer-field/choices']:text+='- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '')+'\n'
 return text+'\n'+q[':question/worked-solution']
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template',choices=list(TEMPLATES));ap.add_argument('--profile',choices=list(BANK_PROFILES));ap.add_argument('--field-type',choices=['radio','blank']);args=ap.parse_args()
 if args.count<1:ap.error('Positive count required')
 levels=['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]
 records=[generate(l,args.seed+i,args.template,args.field_type,profile=args.profile) for l in levels for i in range(args.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
if __name__=='__main__':main()
