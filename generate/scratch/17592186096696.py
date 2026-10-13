#!/usr/bin/env python3
"""Direct integration of first-order ODEs; scratch generation only, steps 3–7.

Observed profiles are parameterized dependent-function rescalings. They preserve
all original banks and solution stages, including absent raw attributes. Their
opaque distractor intent is NOT claimed recovered. Authored default banks use
actual direct-integration operations. No plots or database operations.
"""
from pathlib import Path
import argparse, copy, hashlib, json, random, re, uuid
import sympy as s
KP_ID=17592186096696
ROOT=Path(__file__).with_suffix('')
CAPTURE=json.loads((ROOT/'source.json').read_text())
SOURCE=CAPTURE['record']
VERSION='direct-integration-1'
x=s.Symbol('x',real=True)
C=s.Symbol('C',real=True)
QUESTIONS={q[':question/math-academy-id']:q for q in SOURCE[':knowledge-point/questions']}
TEMPLATES={'linear':'easy','sine':'easy','reciprocal':'easy','exponential':'easy','exp_linear':'moderate','polynomial_pair':'moderate','scaled_cosine':'moderate','exp_constant':'moderate','three_poly_exp':'hard','three_trig_exp':'hard','three_reciprocal_exp':'hard'}
CASES=[('q-14245','linear','easy'),('q-50136','exp_linear','moderate'),('q-119032','sine','easy'),('q-119034','reciprocal','easy'),('q-119035','polynomial_pair','moderate'),('q-99006','scaled_cosine','moderate'),('q-119033','exponential','easy'),('q-119037','exp_constant','moderate')]
BANK_PROFILES={sid:{'template':t,'level':l,'origin':'observed-opaque-rescaling'} for sid,t,l in CASES}
BASE={'linear':{'d':1,'terms':[['poly',-11,1]]},'sine':{'d':1,'terms':[['sin','1/2',4]]},'reciprocal':{'d':1,'terms':[['reciprocal',3,1]]},'exponential':{'d':1,'terms':[['exp',-3,-1]]},'exp_linear':{'d':1,'terms':[['exp',-4,2],['poly',-2,1]]},'polynomial_pair':{'d':1,'terms':[['poly',4,1],['poly',-6,2]]},'scaled_cosine':{'d':-5,'terms':[['cos',-3,3]]},'exp_constant':{'d':1,'terms':[['poly',1,0],['exp',6,-3]]}}

def tex(e):
 return s.latex(e).replace(r'\log',r'\ln')
def uid(value):return str(uuid.uuid5(uuid.NAMESPACE_URL,json.dumps(value,sort_keys=True,ensure_ascii=False)))
def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def enum(v):return v[':db/ident'] if isinstance(v,dict) else v
def term(kind,a,b):
 a=s.Rational(a);b=int(b)
 if kind=='poly':return a*x**b,a*x**(b+1)/(b+1),b+1
 if kind=='exp':return a*s.exp(b*x),a*s.exp(b*x)/b,b
 if kind=='sin':return a*s.sin(b*x),-a*s.cos(b*x)/b,b
 if kind=='cos':return a*s.cos(b*x),a*s.sin(b*x)/b,b
 if kind=='reciprocal':return a/(x-b),a*s.log(s.Abs(x-b)),1
 raise ValueError('Unsupported integration component')
def sumtex(items):
 return ''.join(('+' if i and not z.startswith('-') else '')+z for i,z in enumerate(items))
def aligned(rows):return '$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$'
def scale_dep(text,k):
 # Only full dependent-function components are masked; never bare x/y symbols.
 forms=[r'\frac{\text{d}y}{\text{d}x}',r'{f}^{′}(x)',r'f^{′}(x)','f(x)']
 slots={}
 for i,z in enumerate(forms):
  marker=f'@@DEP{i}@@';slots[marker]=z if k==1 else r'\left('+tex(k)+r'\cdot '+z+r'\right)'
  text=text.replace(z,marker)
 # y is a standalone LHS of source equations, not any command or argument.
 text=re.sub(r'(?<![A-Za-z\\])y(?=\s*(?:&|=))','@@DEPY@@',text)
 slots['@@DEPY@@']='y' if k==1 else r'\left('+tex(k)+r'\cdot y\right)' 
 for z,v in slots.items():text=text.replace(z,v)
 return text

def pack(problem,solution,values,correct,level,meta,key='selection',raw=None):
 body={'problem':problem,'solution':solution,'bank':sorted(values),'level':level,'key':key,'presence':sorted(raw) if raw else None,'version':VERSION}
 qid=uid(body);fid=uid([qid,key]);answers=[{':answer/id':uid([fid,v]),':answer/type':':answer.type/math',':answer/value':v} for v in values]
 field={':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers}
 if correct is not None:field[':answer-field/correct']=[':answer/id',uid([fid,correct])]
 q={':question/id':qid,':question/problem':problem,':question/answer-fields':[field]}
 if level is not None:q[':question/difficulty']=':question.difficulty/'+level
 if solution is not None:q[':question/worked-solution']=solution
 rng=random.Random(meta['seed']);rng.shuffle(answers)
 meta.update({'version':VERSION,'source_provenance':{k:CAPTURE[k] for k in ('database','basis','lineage')},'content_sha256':digest(body)})
 return {'knowledge_point':{'db_id':KP_ID,'id':SOURCE[':knowledge-point/id'],'title':SOURCE[':knowledge-point/title']},'question':q,'generation':meta}

def observed(level,seed,template,parameters,profile):
 cfg=BANK_PROFILES[profile]
 if cfg['level']!=level or template not in (None,cfg['template']):raise ValueError('Observed profile/template/level mismatch')
 p={'dependent_scale':1} if parameters is None else parameters
 if set(p)!={'dependent_scale'}:raise ValueError('Raw profile accepts dependent_scale only')
 k=s.Rational(p['dependent_scale'])
 if k==0 or abs(k)>8 or k.q>4:raise ValueError('Nonzero rational dependent scale bounded by 8, denominator <=4')
 q=QUESTIONS[profile];f=q[':question/answer-fields'][0]
 values=[scale_dep(a[':answer/value'],k) for a in f[':answer-field/choices']]
 correct=scale_dep(f[':answer-field/correct'][':answer/value'],k) if ':answer-field/correct' in f else None
 spec=BASE[cfg['template']];g=sum(term(*z)[0] for z in spec['terms'])/(s.Rational(spec['d'])*k)
 meta={'seed':seed,'template':cfg['template'],'parameters':{'dependent_scale':str(k)},'bank_profile':profile,'origin':'observed-opaque-parameterized-evidence','evidence_only':True,'eligible_for_learning':False,'raw_source_id':profile,'mathematical_fingerprint':digest(s.srepr(g)),'domains':['connected interval avoiding poles']}
 return pack(scale_dep(q[':question/problem'],k),scale_dep(q[':question/worked-solution'],k) if ':question/worked-solution' in q else None,values,correct,enum(q[':question/difficulty']).split('/')[-1] if ':question/difficulty' in q else None,meta,raw=q)

def sample(template,rng):
 a=lambda:rng.choice([-8,-6,-4,-3,-2,2,3,4,6,8]);k=lambda:rng.choice([-4,-3,-2,2,3,4])
 rows={'linear':[['poly',a(),1]],'sine':[['sin',a(),k()]],'reciprocal':[['reciprocal',a(),rng.randint(-3,3)]],'exponential':[['exp',a(),k()]],'exp_linear':[['exp',a(),k()],['poly',a(),1]],'polynomial_pair':[['poly',a(),1],['poly',a(),2]],'scaled_cosine':[['cos',a(),k()]],'exp_constant':[['poly',a(),0],['exp',a(),k()]],'three_poly_exp':[['poly',a(),1],['poly',a(),2],['exp',a(),k()]],'three_trig_exp':[['sin',a(),k()],['exp',a(),k()],['poly',a(),1]],'three_reciprocal_exp':[['reciprocal',a(),rng.randint(-3,3)],['exp',a(),k()],['poly',a(),1]]}
 return {'d':rng.choice([-5,-4,-3,-2,2,3,4,5]) if template=='scaled_cosine' or template.startswith('three_') else 1,'terms':rows[template]}

def guard(template,p):
 if set(p)!={'d','terms'}:raise ValueError('Expected d and ordered terms')
 d=s.Rational(p['d']);rows=p['terms'];ref=sample(template,random.Random(0))
 if d.q!=1 or (template=='scaled_cosine' or template.startswith('three_')) and abs(d) not in (2,3,4,5) or not(template=='scaled_cosine' or template.startswith('three_')) and d!=1:raise ValueError('Derivative coefficient outside level bounds')
 if len(rows)!=len(ref['terms']):raise ValueError('Wrong primitive count')
 for row,example in zip(rows,ref['terms']):
  kind,a,b=row;a=s.Rational(a)
  if kind!=example[0] or a==0 or abs(a)>11 or a.q>2:raise ValueError('Component/scale outside supported workload')
  if not isinstance(b,int):raise ValueError('Integral parameter must be integer')
  if kind=='poly' and b!=example[2] or kind in ('exp','sin','cos') and abs(b) not in (1,2,3,4) or kind=='reciprocal' and abs(b)>3:raise ValueError('Component parameter outside supported workload')
 return d

def normal(level,seed,template,parameters):
 rng=random.Random(seed);template=template or rng.choice([t for t,l in TEMPLATES.items() if l==level])
 if TEMPLATES.get(template)!=level:raise ValueError('Template/level mismatch')
 for attempt in range(100):
  p=parameters if parameters is not None else sample(template,rng);d=guard(template,p)
  components=[term(*z) for z in p['terms']];gs=[z[0] for z in components];prims=[z[1]/d for z in components];G=sum(gs)/d;F=sum(prims)
  # Choose the entire authored method bank, then reject the whole instance.
  wrong=[-F,sum(gs)/d,sum(z[1]*z[2]**2/d if row[0]!='reciprocal' else z[1]/(d*s.Rational(row[1])**2) for z,row in zip(components,p['terms'])),sum(prims[:-1]) if len(prims)>1 else F/s.Rational(p['terms'][0][1])]
  values=[F]+wrong
  if any(s.simplify(s.diff(a-b,x))==0 for i,a in enumerate(values) for b in values[:i]):
   if parameters is not None:raise ValueError('Complete bank collision')
   continue
  break
 else:raise ValueError('No eligible complete instance')
 lhs=('' if d==1 else tex(d))+"f'(x)";forcing=sumtex([tex(z) for z in gs]);isolated=sumtex([tex(z/d) for z in gs]);primitive=sumtex([tex(z) for z in prims])
 problem='Find the general solution to the differential equation $'+lhs+'='+forcing+'.$'
 opening=('First, notice that the derivative term is already isolated on the left:' if d==1 else 'First, we rearrange the equation to isolate the derivative term:')
 sol=opening+'\n\n'+aligned(["f'(x) &="+isolated])+ '\n\nThen, we integrate both sides of the equation with respect to $x,$ and we get\n\n'
 formal=r'\int f\prime(x)\,\text{d}x &=\int ('+isolated+r')\,\text{d}x'
 distributed=sumtex([('' if d==1 else tex(1/d)+r'\cdot ')+r'\int ('+tex(z)+r')\,\text{d}x' for z in gs])
 # Preserve each primitive evaluation before collecting terms.
 evaluated=sumtex([tex(1/d)+r'\cdot \left('+tex(z[1])+r'\right)' for z in components])
 sol+=aligned([formal,'f(x) &='+distributed,'&='+evaluated+'+C','&='+primitive+'+C.'])
 rendered=['f(x)='+tex(z)+'+C' for z in values]
 meta={'seed':seed,'template':template,'parameters':p,'bank_profile':'authored-direct-operations','origin':'authored-missing-hard' if level=='hard' else 'authored-method-bank','evidence_only':False,'eligible_for_learning':True,'recipe_operations':['correct','reverse primitive signs','retain derivative components','multiply instead of divide by power/inner factor','omit last primitive or omit outer coefficient'],'mathematical_fingerprint':digest(s.srepr(G)),'domains':['connected interval avoiding x='+str(z[2]) for z in p['terms'] if z[0]=='reciprocal'] or ['all real x'],'primitive_count':len(prims)}
 return pack(problem,sol,rendered,rendered[0],level,meta)

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard') or field_type not in (None,'radio'):raise ValueError('Unsupported level/field type')
 if profile in BANK_PROFILES:return observed(level,seed,template,parameters,profile)
 if profile not in (None,'authored-direct-operations'):raise ValueError('Unknown complete bank profile')
 return normal(level,seed,template,parameters)
# EASY: one primitive; at most one rearrangement, familiar linear argument.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: two primitives, or divide nonunit derivative coefficient + cosine.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: authored equal-workload three primitive terms and nonunit derivative.
# No dependent-variable forcing, IVP, second derivative, parts, or extra branch.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 correct=next((a[':answer/value'] for a in f[':answer-field/choices'] if ':answer-field/correct' in f and a[':answer/id']==f[':answer-field/correct'][1]),None)
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in f[':answer-field/choices'])+'\n\n'+('**Correct:** $'+correct+'$' if correct is not None else '*Raw source has no correct designation.*')+'\n\n'+q.get(':question/worked-solution','*Raw source has no worked solution.*')
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');a=ap.parse_args()
 if a.count<1:ap.error('count must be positive')
 levels=['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]
 records=[generate(l,a.seed+i,a.template,profile=a.profile) for l in levels for i in range(a.count)]
 print(json.dumps(records,indent=2,ensure_ascii=False) if a.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
if __name__=='__main__':main()
