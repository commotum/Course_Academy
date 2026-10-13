#!/usr/bin/env python3
"""Identity classification for three real linear equations (basis 1356).

Five easy sources, four complete radio banks, one direct affine template.
Moderate and hard are authored prerequisite-supported distribution templates;
all levels assess exactly the same identity classification. No unknown parameter
is solved. See the adjacent evidence folder for route, bounds and fidelity.
Explicit parameters use {'equations': [...]}: easy affine quadruples; moderate
[k,b,c,d] for k(x+b)=cx+d; hard [k,a,b,t,s,m,c,d,u,v] for
k(ax+b)+tx+s=m(cx+d)+ux+v. Fractions are exact integer or 'p/q' strings.
The complete profile is selected before equations. Every bank is retained whole.
No learner feedback is invented. All five observed shared solutions replay exactly.
"""
from __future__ import annotations
import argparse, hashlib, json, random, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186110719
KP_UUID='ff4e9141-5743-55f1-a8be-3e28cb047eca'
TITLE='Identifying Equations With Infinitely Many Solutions'
VERSION='affine-identities-radio-3'
PACKAGE=Path(__file__).with_suffix('')
SOURCE={'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1'}
ROMAN=('I','II','III')
TEMPLATES={'direct':'easy','one_distribution':'moderate','two_distributions':'hard'}
BANKS={
 'observed_a':('II only','III only','I and II only','II and III only','I, II, and III'),
 'observed_b':('None','I and II only','II only','III only','I and III only'),
 'observed_c':('I and II only','II only','I only','II and III only','III only'),
 'observed_d':('II and III only','III only','None','I and III only','II only'),
}
SOURCE_CASES={
 'q-287966':([[2,0,1,1],[2,1,2,1],[2,1,2,3]],'observed_a'),
 'q-288419':([[3,0,2,5],[4,-2,4,-2],[5,3,5,1]],'observed_a'),
 'q-288425':([[-3,2,-3,7],[6,1,6,5],[7,-4,6,-6]],'observed_b'),
 'q-288427':([[2,-5,1,-2],[6,1,6,9],[-4,3,-4,3]],'observed_d'),
 'q-288591':([[3,2,4,1],[2,-5,3,-3],[5,-4,5,-4]],'observed_c'),
}
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def ident(v): return str(uuid.uuid5(uuid.UUID(KP_UUID),digest(v)))
def rat(v):
 if type(v) not in (int,str): raise ValueError('exact integers or rational strings required')
 try: r=sp.Rational(v)
 except Exception as e: raise ValueError('invalid exact rational') from e
 if str(v) not in (str(r),str(int(r)) if r.q==1 else str(r)): raise ValueError('canonical reduced rational required')
 return r
def tex(v): return sp.latex(sp.Rational(v))
def linear(a,b):
 z=('x' if a==1 else '-x' if a==-1 else tex(a)+'x') if a else ''
 return z+('+' if b>0 and z else '')+(tex(b) if b or not z else '')
def added(z,n,variable=False):
 if not n:return z
 return z+('+' if n>0 else '-')+(linear(abs(n),0) if variable else tex(abs(n)))
def eq(v): return linear(v[0],v[1])+'='+linear(v[2],v[3])
def kind(v):
 a,b,c,d=v
 return 'identity' if a==c and b==d else 'empty' if a==c else 'unique'
def subset(kinds):
 labels=[r for r,k in zip(ROMAN,kinds) if k=='identity']
 return 'None' if not labels else labels[0]+' only' if len(labels)==1 else ' and '.join(labels)+' only' if len(labels)==2 else 'I, II, and III'
def truths(value):
 masked=value.replace('III','C').replace('II','B').replace('I','A')
 return tuple(r for r in ROMAN if {'I':'A','II':'B','III':'C'}[r] in masked)
def factor(k,a,b):return tex(k)+r'\left('+linear(a,b)+r'\right)'
def parts(row,level):
 if level=='easy':return tuple(row), (linear(row[0],row[1]),linear(row[2],row[3])),[]
 if level=='moderate':
  k,b,c,d=row; l=factor(k,1,b);r=linear(c,d)
  # Keep both independently multiplied components before evaluation.
  stage=tex(k)+r'\cdot x'+('+' if b>0 else '-')+tex(abs(k))+r'\cdot '+tex(abs(b)) if k>0 else tex(k)+r'\cdot x'+r'+\left('+tex(k)+r'\right)\cdot\left('+tex(b)+r'\right)'
  return (k,k*b,c,d),(l,r),[(l,r),(stage,r)]
 k,a,b,t,s,m,c,d,u,v=row
 l=added(added(factor(k,a,b),t,True),s);r=added(added(factor(m,c,d),u,True),v)
 def distributed(k,a,b,t,s):
  term=r'\left('+tex(k)+r'\right)\cdot\left('+tex(a)+r'x\right)'
  term+=r'+\left('+tex(k)+r'\right)\cdot\left('+tex(b)+r'\right)'
  return added(added(term,t,True),s)
 return (k*a+t,k*b+s,m*c+u,m*d+v),(l,r),[(l,r),(distributed(k,a,b,t,s),distributed(m,c,d,u,v)),(added(added(linear(k*a,k*b),t,True),s),added(added(linear(m*c,m*d),u,True),v))]
def solution(v,index,display,prefix):
 a,b,c,d=v;class_=kind(v);left,right=linear(a,b),linear(c,d)
 remove=a if a==c else min(a,c)
 rows=prefix+[(left,right),(added(left,-remove,True),added(right,-remove,True)),(linear(a-remove,b),linear(c-remove,d))]
 if class_=='unique':
  coeff=abs(a-c)
  if a>c:
   if b: rows += [(added(linear(coeff,b),-b),added(tex(d),-b)),(linear(coeff,0),tex(d-b))]
   value=(d-b)/(a-c)
  else:
   if d: rows += [(added(tex(b),-d),added(linear(coeff,d),-d)),('x' if coeff==1 else tex(b-d),tex(b-d) if coeff==1 else linear(coeff,0))]
   elif coeff==1: rows += [('x',tex(b))]
   value=(d-b)/(a-c)
  if coeff!=1:rows += [('x',tex(value))]
  conclusion=f'Therefore, the equation ${display}$ has the unique solution $x={tex(value)}.$'
 elif class_=='identity':conclusion=f'This equation is true for all values of $x.$ Therefore, the equation ${display}$ has infinitely many solutions.'
 else:conclusion='This equation is false for all values of $x.$'
 steps=r' \\ '.join(l+' & ='+r for l,r in rows)
 return '- For the '+('first','second','third')[index]+' equation, we have\n\n$$\n'+r'\begin{aligned}'+steps+r'.\end{aligned}'+'\n$$\n\n'+conclusion

def guard(row,level):
 if level=='easy': reduced=tuple(row)
 elif level=='moderate':
  k,shift,c,d=row;reduced=(k,k*shift,c,d)
 else:
  k,aa,bb,t,s,m,cc,dd,u,v=row;reduced=(k*aa+t,k*bb+s,m*cc+u,m*dd+v)
 a,b,c,d=reduced
 if not a or not c:raise ValueError('nonzero reduced slopes required')
 if level=='easy':
  if any(v.q!=1 for v in row) or not (abs(a)<=7 and abs(c)<=7 and abs(b)<=9 and abs(d)<=9):raise ValueError('easy integer bounds')
  if a!=c and (a<=0 or c<=0 or abs(a-c)!=1):raise ValueError('easy unique positive unit-gap slopes')
 elif level=='moderate':
  k,shift,c,d=row
  if any(v.q!=1 for v in row) or not (2<=abs(k)<=5 and 1<=abs(shift)<=5 and 1<=abs(c)<=6 and 1<=abs(d)<=25):raise ValueError('moderate bounds/nonunit distribution')
  if abs(b)>25:raise ValueError('moderate reduced constants')
 elif level=='hard':
  k,aa,bb,t,s,m,cc,dd,u,v=row
  if any(z.q!=1 for z in row) or not (2<=abs(k)<=4 and 2<=abs(m)<=4 and all(1<=abs(z)<=4 for z in (aa,bb,t,s,cc,dd,u,v))):raise ValueError('hard component bounds')
  if any(not z or abs(z)>15 for z in reduced):raise ValueError('hard reduced affine bounds')
  if abs(k*aa)==abs(t) or abs(m*cc)==abs(u):raise ValueError('hard cannot cancel or duplicate slope collection terms')
  if abs(k*bb)==abs(s) or abs(m*dd)==abs(v):raise ValueError('hard cannot cancel or duplicate constant collection terms')
 return reduced

def fingerprint(rows,level):
 # Common equation scaling and side reversal are incidental. Hard retains the
 # substantive distribution/collection tree, as simplifying it erases workload.
 objects=[]
 for row in rows:
  reduced,_,_=parts(row,level)
  if level=='easy':
   values=list(reduced);gcd=sp.gcd_list(values);normalized=[str(v/abs(gcd)) for v in values]
   sides=sorted([normalized[:2],normalized[2:]])
   objects.append(sides)
  else:objects.append([str(v) for v in row])
 return digest([level,sorted(objects)])

def sample_row(level,class_,rng):
 if level=='easy':
  if class_=='unique':a=rng.randint(1,6);c=a+rng.choice([-1,1]);c=c or a+1
  else:a=rng.choice([v for v in range(-7,8) if v]);c=a
  b=rng.randint(-9,9);d=b if class_=='identity' else rng.choice([v for v in range(-9,10) if v!=b])
  return [a,b,c,d]
 if level=='moderate':
  k=rng.choice([-5,-4,-3,-2,2,3,4,5]);b=rng.choice([v for v in range(-5,6) if v])
  c=k if class_!='unique' else rng.choice([v for v in range(-6,7) if v and v!=k])
  d=k*b if class_=='identity' else rng.choice([v for v in range(-25,26) if v and v!=k*b])
  return [k,b,c,d]
 # Hard: select complete pairs of factor/collection structures whose reduced
 # slopes agree/differ as required; rejection keeps every signed component.
 while True:
  row=[rng.choice([-4,-3,-2,2,3,4]) if i in (0,5) else rng.choice([-4,-3,-2,-1,1,2,3,4]) for i in range(10)]
  # Equal reduced slopes/constants are sampled structurally, not found by a
  # lookup or repaired option bank. Reject the whole row if a component fails.
  if class_ in ('identity','empty'):
   row[8]=row[0]*row[1]+row[3]-row[5]*row[6]
   if class_=='identity':row[9]=row[0]*row[2]+row[4]-row[5]*row[7]
  try:reduced=guard(list(map(sp.Integer,row)),level)
  except ValueError:continue
  if kind(reduced)==class_:return row

def generate(level='easy',seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('unknown difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('radio required')
 template=template or next(t for t,l in TEMPLATES.items() if l==level)
 if TEMPLATES.get(template)!=level:raise ValueError('template/difficulty mismatch')
 rng=random.Random(seed)
 profile=profile or rng.choice(list(BANKS))
 if profile not in BANKS:raise ValueError('unknown complete bank profile')
 bank=BANKS[profile]
 if parameters is None:
  target=rng.choice(bank);labels=truths(target)
  classes=['identity' if r in labels else rng.choice(['unique','empty']) for r in ROMAN]
  while True:
   rows=[sample_row(level,c,rng) for c in classes]
   try:return generate(level,seed,template,field_type,{'equations':rows},profile)
   except ValueError:continue
 if not isinstance(parameters,dict) or set(parameters)!={'equations'}:raise ValueError('equations parameter dictionary required')
 raw=parameters['equations'];n={'easy':4,'moderate':4,'hard':10}[level]
 if not isinstance(raw,list) or len(raw)!=3 or any(not isinstance(r,list) or len(r)!=n for r in raw):raise ValueError('three complete parameter rows required')
 rows=[list(map(rat,row)) for row in raw];reduced=[guard(row,level) for row in rows]
 displays=[parts(row,level)[1] for row in rows]
 if len({tuple(sorted(d)) for d in displays})!=3:raise ValueError('repeated equation')
 classes=[kind(r) for r in reduced];correct=subset(classes)
 if correct not in bank:raise ValueError('complete bank lacks the mathematically correct subset')
 equations=[l+'='+r for l,r in displays]
 prompt='Which of the following equations has infinitely many solutions?\n\n'+'\n'.join('- $'+e+'$' for e in equations)
 worked="Let's attempt to solve each equation in turn:\n\n"+'\n\n'.join(solution(r,i,e,parts(row,level)[2]) for i,(row,r,e) in enumerate(zip(rows,reduced,equations)))+'\n\nTherefore, the correct answer is "'+correct+'."'
 key=fingerprint(rows,level)
 content={'version':VERSION,'prompt':prompt,'solution':worked,'bank':sorted(bank),'level':level}
 qid=ident(content);fid=ident([qid,'selection'])
 choices=[{':answer/id':ident([fid,v]),':answer/type':':answer.type/text',':answer/value':v} for v in bank]
 correct_id=next(a[':answer/id'] for a in choices if a[':answer/value']==correct)
 random.Random(str(seed)+':'+qid+':shuffle').shuffle(choices)
 canonical={'equations':[[int(v) if v.q==1 else str(v) for v in row] for row in rows]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':qid,':question/problem':prompt,':question/worked-solution':worked,':question/difficulty':':question.difficulty/'+level,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':choices,':answer-field/correct':[':answer/id',correct_id]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'profile':profile,'origin':'observed template' if level=='easy' else 'authored missing-level template','parameters':canonical,'domain':'x real','source':SOURCE,'mathematical_fingerprint':key,'parameter_fingerprint':digest(canonical),'sympy':sp.__version__}}
# Easy: directly compare integer affine coefficients/constants; unit-gap unique peers.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# Moderate: one nonunit distribution (two products) in every equation.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# Hard: two nonunit distributions (four products), two nonzero slope and constant
# collections in every equation, bounded again after reduction.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)
def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');p.add_argument('--seed',type=int,default=0);p.add_argument('--count',type=int,default=1);p.add_argument('--format',choices=['markdown','json'],default='markdown');p.add_argument('--template');p.add_argument('--profile');a=p.parse_args()
 if a.count<1:p.error('positive count required')
 records=[generate(level,a.seed+i,a.template,profile=a.profile) for level in (['easy','moderate','hard'] if a.difficulty=='all' else [a.difficulty]) for i in range(a.count)]
 print(json.dumps(records,indent=2) if a.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
