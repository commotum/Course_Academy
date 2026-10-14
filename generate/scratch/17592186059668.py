#!/usr/bin/env python3
"""Source-backed transformed-point radio generator; see sibling extraction."""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
import sympy as sp
KP_ID=17592186059668
ROOT=Path(__file__).with_suffix('')
SOURCE=json.loads((ROOT/'source.json').read_text()); KP_UUID=SOURCE['record'][':knowledge-point/id']; TITLE=SOURCE['record'][':knowledge-point/title']
VERSION='transformed-point-1'
SUPPORTED_LEVELS=('easy','moderate')
# Each complete source bank is a separate profile; incomplete sources are evidence only.
CASES={
 'quadratic':('q-121220','easy',{'h':1,'k':2}),
 'exponential':('q-121383','easy',{'h':2,'k':3}),
 'absolute':('q-121385','easy',{'h':-3,'k':-2}),
 'horizontal_scale':('q-121399','easy',{'s':2,'k':1}),
 'numeric_shift':('q-26398','moderate',{'a':1,'b':4,'h':1,'k':1}),
 'numeric_reflection':('q-26594','moderate',{'a':3,'b':1,'k':-1})}
a,b,x=sp.symbols('a b x', real=True)

def canonical(z):
 if isinstance(z,dict):return {k:canonical(v) for k,v in z.items()}
 if isinstance(z,(tuple,list)):return [canonical(v) for v in z]
 return int(z) if isinstance(z,sp.Integer) else z

def digest(z):return hashlib.sha256(json.dumps(canonical(z),sort_keys=True).encode()).hexdigest()
def uid(z):return str(uuid.uuid5(uuid.UUID(KP_UUID),z))
def mathtex(z):return sp.latex(sp.sympify(z)).replace(' ','')
def pair(u,v):return '('+mathtex(u)+','+mathtex(v)+')'
def plus(z,k):return mathtex(z)+(('+'+str(k)) if k>0 else str(k) if k<0 else '')
def structures(template,p):
 h=p.get('h',0); k=p['k']; s=p.get('s',1)
 A,B=(p['a'],p['b']) if template.startswith('numeric') else (a,b)
 if template=='quadratic':base=r'x^{2}';inner='('+plus(x,-h)+')^{2}';function=lambda t:t**2; horizontal=A+h;vertical=B+k;relation=a**2
 elif template=='exponential':base=r'2^{x}';inner='2^{'+plus(x,-h)+'}';function=lambda t:2**t;horizontal=A+h;vertical=B+k;relation=2**a
 elif template=='absolute':base='|x|';inner='|'+plus(x,-h)+'|';function=lambda t:sp.Abs(t);horizontal=A+h;vertical=B+k;relation=sp.Abs(a)
 elif template=='horizontal_scale':base='3^{x}';inner='3^{x/'+str(s)+'}';function=lambda t:3**t;horizontal=s*A;vertical=B+k;relation=3**a
 elif template=='numeric_shift':base='f(x)';inner='f('+plus(x,-h)+')';function=None;horizontal=A+h;vertical=B+k;relation=None
 elif template=='numeric_reflection':base='f(x)';inner='-f(x)';function=None;horizontal=A;vertical=-B+k;relation=None
 else:raise ValueError(template)
 target=inner+(('+'+str(k)) if k>0 else str(k));right=(horizontal,vertical)
 if template=='quadratic':bank=[(A,B+k+h),(A,B+k),right,(A-h,B+k),(A+k,B+h)]
 elif template=='exponential':bank=[(A-h,B+k),(A-h,B-k),(A-h,k*B),right,(A+h,B-k)]
 elif template=='absolute':bank=[(A+k,B+h),right,(A-h,B+k),(A-h,B-k),(A+h,B-k)]
 elif template=='horizontal_scale':bank=[(A/s,B-k),(A+s,B+k),(A**sp.Rational(s+1,s),B+k),right,(A/s,B+k)]
 elif template=='numeric_shift':bank=[(A,B+k),(A-h,B+k),(A-h,B-k),right,(A+h,B-k)]
 else:bank=[right,(-A,-B+k),(A,B-k),(-A,-B+2*k),(A,-B+2*k)]
 return A,B,base,inner,target,right,bank,function,relation

def domain(t,p):
 assert all(isinstance(v,int) and not isinstance(v,bool) for v in p.values())
 assert 1<=abs(p['k'])<=8
 if 'h' in p:assert 1<=abs(p['h'])<=8
 if 's' in p:assert 2<=p['s']<=5
 if 'a' in p:assert 1<=abs(p['a'])<=10 and 1<=abs(p['b'])<=10

def mathematical_fingerprint(t,p):
 # Symbol labels, bank order and seed omitted. Different mathematical transformations retained.
 return digest({'template':t,'parameters':p})

def generate(difficulty,seed=0,template=None,parameters=None,profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('unsupported difficulty '+difficulty)
 rng=random.Random(seed);templates=[t for t,c in CASES.items() if c[1]==difficulty]
 t=template or rng.choice(templates)
 if t not in templates:raise ValueError('template difficulty mismatch')
 if profile is not None and profile!=t:raise ValueError('banks cannot be mixed')
 if parameters is None:
  for attempt in range(100):
   p={k:rng.choice([z for z in range(-8,9) if z]) for k in CASES[t][2]}
   if 's' in p:p['s']=rng.randint(2,5)
   try:return generate(difficulty,seed,t,p,t)
   except (ValueError,AssertionError):continue
  raise ValueError('bounded resampling exhausted')
 p=canonical(parameters);domain(t,p)
 A,B,base,inner,target,right,bank,function,relation=structures(t,p)
 assert len({pair(*z) for z in bank})==5 and bank.count(right)==1,'bank collision'
 h=p.get('h',0);k=p['k'];s=p.get('s',1)
 if t=='numeric_reflection':stage=pair(A,-B);action='reflect the graph across the $x$-axis'
 elif t=='horizontal_scale':stage=pair(s*A,B);action=f'stretch the graph by a scale factor of ${s}$ parallel to the $x$-axis'
 else:stage=pair(A+h,B);action=f'shift the graph horizontally by ${abs(h)}$ '+('unit' if abs(h)==1 else 'units')+' to the '+('right' if h>0 else 'left')
 vertical=f'shift the result vertically by ${abs(k)}$ '+('unit' if abs(k)==1 else 'units')+' '+('up' if k>0 else 'down')
 prompt=f'The point ${pair(A,B)}$ lies on the curve $y={base}.$ Which of the following points **must** lie on $y={target}?$'
 X,Y=right
 if t.startswith('numeric'):
  old=f'f({A})={B}'
  sub=f'-f({A})'+(('+'+str(k)) if k>0 else str(k)) if t=='numeric_reflection' else f'f({plus(X,-h)})'+(('+'+str(k)) if k>0 else str(k))
  middle=plus(-B if t=='numeric_reflection' else B,k)
  known=('-( '+mathtex(B)+' )' if t=='numeric_reflection' else f'f({A})')+(('+'+str(k)) if k>0 else str(k))
 else:
  old=mathtex(relation)+'=b'
  arg=plus(X,-h) if t!='horizontal_scale' else r'\frac{'+mathtex(X)+'}{'+str(s)+'}'
  sub={'quadratic':'('+arg+')^{2}','exponential':'2^{'+arg+'}','absolute':'|'+arg+'|','horizontal_scale':'3^{'+arg+'}'}[t]+(('+'+str(k)) if k>0 else str(k))
  middle=mathtex(relation)+(('+'+str(k)) if k>0 else str(k))
 extra=(known+chr(32)+chr(92)*2+' &=') if t.startswith('numeric') else ''
 solution=f'**Method 1**\n\nTo plot $y={target},$ we apply the following steps:\n\n- First, we take the graph $y={base}.$\n\n- Then, we {action} and get the graph of $y={inner}.$ After this transformation, the point ${pair(A,B)}$ will be mapped to the point\n\n$$\n{stage}.\n$$\n\n- Finally, we {vertical} and obtain the graph of $y={target}.$ After this transformation, the point ${stage}$ will be mapped to the point\n\n$$\n{pair(X,Y)}.\n$$\n\n**Method 2**\n\nSince the point ${pair(A,B)}$ lies on the graph of $y={base}$, we have that ${old}.$\n\nNow consider the graph of $y={target}.$ Substituting $x={mathtex(X)}$, we get\n\n$$\n\\begin{{aligned}}y &={sub} \\\\ &={extra}{middle} \\\\ &={mathtex(Y)}.\\end{{aligned}}\n$$\n\nTherefore, the point ${pair(X,Y)}$ must lie on $y={target}.$'
 fp=mathematical_fingerprint(t,p);qid=uid('question:'+fp+':'+t);fid=uid(qid+':selection')
 answers=[{':answer/id':uid(fid+':'+pair(*z)),':answer/type':':answer.type/math',':answer/value':pair(*z)} for z in bank]
 correct=next(z[':answer/id'] for z in answers if z[':answer/value']==pair(*right))
 q={':question/id':qid,':question/problem':prompt,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct]}]}
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':q,'generation':{'version':VERSION,'seed':seed,'template':t,'parameters':p,'bank_profile':t,'mathematical_fingerprint':fp,'eligible_for_learning':True,'evidence_only':False,'source_references':[CASES[t][0]],'domains':{'parameters':'nonzero integers in [-8,8]; scale in [2,5]; numeric coordinates nonzero in [-10,10]'},'dependencies':{'sympy':sp.__version__},'plot_assets':[]}}

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' (correct)' if a[':answer/id']==f[':answer-field/correct'][1] else '') for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--difficulty',choices=SUPPORTED_LEVELS,required=True);parser.add_argument('--template',choices=list(CASES));parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--parameters',type=json.loads);parser.add_argument('--format',choices=['json','markdown'],default='json');args=parser.parse_args()
 records=[generate(args.difficulty,args.seed+i,args.template,args.parameters) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(map(markdown,records)))
