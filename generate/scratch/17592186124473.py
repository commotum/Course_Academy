#!/usr/bin/env python3
"""Graph/interval invertibility generator with current checkbox response layout.

Raw observed profiles reconstruct complete interval/prose/bank masks and retain
original raster ink at its original parameters. Changed evidence coordinates use
an explicitly qualitative polygonal surrogate, never eligible for learning.
Normal defaults are authored analytic graphs, with source-grounded methods and
complete banks. No source formula can be inferred uniquely from a raster.
See the private classification, plot specification, validation and review.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, random, re, subprocess, sys, tempfile, uuid
from pathlib import Path
from fractions import Fraction as F
import sympy as sp
KP_ID=17592186124473
HERE=Path(__file__).resolve().with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text())
REC=SOURCE['record'];TITLE=REC[':knowledge-point/title'];VERSION='interval-invertibility-2'
QUESTIONS={q[':question/math-academy-id']:q for q in REC[':knowledge-point/questions']}
NS=uuid.UUID('3b6b8762-b3ed-4b42-872a-95f6d1bf32ec')
OPEN="A function is invertible on a particular interval if and only if it's a one-to-one function on that interval. To determine the intervals on which the function is invertible, we use the horizontal line test."
# Qualitative source landmarks. These recover monotonic pieces, endpoint inclusion
# and output overlap, not the original unlabelled analytic curves.
# A piece is [x0,y0,x1,y1,left_closed,right_closed]. +/-99 denotes visible continuation.
LANDMARKS={
'q-36039':[[-4,1,-2,3,1,0],[-2,5,3,0,1,1]],
'q-36941':[[-99,99,-2,2,0,1],[-2,-2,0,F(-1,4),0,1],[0,F(-1,4),2,-2,1,1],[2,2,99,99,0,0]],
'q-108667':[[-99,-99,-3,1,0,1],[-3,1,0,-1,1,1],[0,-1,3,1,1,1],[3,1,99,-99,1,0]],
'q-108673':[[-99,-99,-2,3,0,1],[-2,3,0,1,1,1],[0,1,99,99,1,0]],
'q-108791':[[-3,-4,-2,-1,1,1],[-2,-1,1,1,1,1],[1,1,3,1,1,1],[3,1,5,3,1,1]],
'q-108795':[[-2,-2,0,-2,1,1],[0,-2,4,2,1,1]],
'q-36002':[[-99,99,0,0,0,1],[0,0,99,99,1,0]],
'q-36004':[[-6,-F(25,2),0,-F(1,2),1,1],[0,-F(1,2),4,-F(23,2),1,1],[4,-F(23,2),10,-F(11,2),1,1]],
'q-36008':[[-99,99,0,0,0,1],[0,0,1,2,1,1],[1,2,99,-99,1,0]],
'q-36011':[[-99,-99,-2,3,0,0],[-2,4,3,2,1,1]],
'q-36061':[[-3,3,1,-1,1,1],[1,-1,4,-1,1,0]],
'q-36066':[[-99,99,0,1,0,1],[0,1,2,3,1,1],[2,3,99,-99,1,0]],
'q-36934':[[-99,99,-2,1,0,1],[-2,1,-1,2,1,1],[-1,2,99,-99,1,0]],
}
# Source 36066 genuinely curved right piece: y=3-(x-2)^2, so at x=4
# it is -1. Its interval union outputs (-1,3) and [3,4), disjoint.
# Generic polygonal evidence pieces use the landmark at x=4, not tail extent.
LANDMARKS['q-36066']=[[-99,100,0,1,0,1],[0,1,2,3,1,1],[2,3,4,-1,1,1],[4,-1,99,-99,1,0]]


def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,default=str,separators=(',',':')).encode()).hexdigest()
def uid(v): return str(uuid.uuid5(NS,v))
GENERATOR_UUID=uid('generator/'+str(KP_ID))
def num(x):
 x=F(x);return str(x.numerator) if x.denominator==1 else r'\frac{'+str(x.numerator)+'}{'+str(x.denominator)+'}'
def interval(a,b,lc=True,rc=True):return [a,b,bool(lc),bool(rc)]
def itex(i):return ('[' if i[2] else '(')+num(i[0])+','+num(i[1])+(']' if i[3] else ')')
def settex(ss):return r'\cup '.join(itex(i) for i in ss)
def spset(ss):return sp.Union(*[sp.Interval(sp.Rational(str(i[0])),sp.Rational(str(i[1])),left_open=not i[2],right_open=not i[3]) for i in ss])
def subset_label(bits):
 names=[r for r,b in zip(('I','II','III'),bits) if b]
 return (' and '.join(names)+' only') if len(names)<3 and names else ('I, II and III' if names else 'None')
def parse_intervals(text):
 """Read actual displayed finite intervals, allowing captured doubled TeX slashes."""
 text=text.replace('\\\\','\\')
 out=[]
 for m in re.finditer(r'([\[(])\s*(-?\d+|[-]?\\infty)\s*,\s*(-?\d+|\\infty)\s*([\])])',text):
  a,b=m[2],m[3]
  out.append([-99 if a==r'-\infty' else int(a),99 if b==r'\infty' else int(b),m[1]=='[',m[4]==']'])
 return out

def transformed_intervals(text,h):
 # Entire interval components only; source scalar y witnesses remain untouched.
 def repl(m):
  def tr(s):return s if 'infty' in s else str(int(s)+h)
  return m[1]+tr(m[2])+m[3]+tr(m[4])+m[5]
 return re.sub(r'([\[(])\s*(-?\d+|[-]?\\+infty)(\s*,\s*)(-?\d+|\\+infty)\s*([\])])',repl,text)

def injective(pieces,ss):
 """Independent exact line-segment range test on the requested set.

Restriction must lie in shown domain. Each nonconstant piece is one-to-one;
intersecting output ranges from distinct input pieces violate injectivity unless
intersection consists only of their shared (identical) input point.
"""
 requested=spset(ss)
 domain=sp.Union(*[sp.Interval(sp.Rational(str(a)),sp.Rational(str(c)),left_open=not lc,right_open=not rc) for a,b,c,d,lc,rc in pieces])
 if requested-domain!=sp.EmptySet:return False
 branches=[]
 for a,b,c,d,lc,rc in pieces:
  source=sp.Interval(sp.Rational(str(a)),sp.Rational(str(c)),left_open=not lc,right_open=not rc)
  part=requested.intersect(source)
  components=list(part.args) if isinstance(part,sp.Union) else [part]
  for s in components:
   if s==sp.EmptySet:continue
   slope=(sp.Rational(str(d))-sp.Rational(str(b)))/(sp.Rational(str(c))-sp.Rational(str(a)))
   intercept=sp.Rational(str(b))-slope*a
   if isinstance(s,sp.FiniteSet):
    for x in s:branches.append((sp.FiniteSet(slope*x+intercept),s,slope,intercept))
   elif slope==0:
    return False
   else:
    ya,yb=slope*s.start+intercept,slope*s.end+intercept
    image=sp.Interval(min(ya,yb),max(ya,yb),left_open=s.left_open if slope>0 else s.right_open,right_open=s.right_open if slope>0 else s.left_open)
    branches.append((image,s,slope,intercept))
 for i,(image,domain1,m1,b1) in enumerate(branches):
  for image2,domain2,m2,b2 in branches[i+1:]:
   overlap=image.intersect(image2)
   if overlap==sp.EmptySet:continue
   if not isinstance(overlap,sp.FiniteSet):return False
   for y in overlap:
    x1=next(iter(domain1)) if m1==0 and isinstance(domain1,sp.FiniteSet) else ((y-b1)/m1 if m1 else None)
    x2=next(iter(domain2)) if m2==0 and isinstance(domain2,sp.FiniteSet) else ((y-b2)/m2 if m2 else None)
    if x1 is None or x2 is None or x1!=x2:return False
 return True

def make_record(level,prompt,solution,values,correct,atype,seed,meta,raw_presence=None):
 # Exact Fraction metadata uses rational strings in the public JSON interface.
 meta=json.loads(json.dumps(meta,default=str))
 if len(values)!=5 or len(set(values))!=5 or correct not in values:raise ValueError('Incomplete or ambiguous bank')
 identity=digest([VERSION,level,prompt,solution,sorted(values),correct,atype])
 fid=uid(identity+'/selection')
 answers=[{':answer/id':uid(fid+'/'+v),':answer/type':atype,':answer/value':v} for v in values]
 random.Random(seed).shuffle(answers)
 q={':question/id':uid(identity),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,
 ':question/answer-fields':[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',uid(fid+'/'+correct)]}]}
 if raw_presence is not None:
  for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
   if k not in raw_presence:q.pop(k,None)
 return {'knowledge_point':{'db_id':KP_ID,'id':REC[':knowledge-point/id'],'title':TITLE},'question':q,'generation':{'version':VERSION,'python':sys.version.split()[0],'sympy':sp.__version__,'seed':seed,'content_identity':identity,'source':{k:SOURCE[k] for k in ('database','basis','lineage')},**meta}}

def render_plots(pieces,ss,stem,mode='prompt'):
 """Shared Matplotlib renderer. Unique input and atomic final assets/sidecars."""
 plotdata={'pieces':[[str(v) if isinstance(v,F) else v for v in p] for p in pieces],'restrictions':json.loads(json.dumps(ss,default=str)),'mode':mode}
 token=digest([plotdata,hashlib.sha256((HERE/'renderer.py').read_bytes()).hexdigest()]);out=HERE/'plots'/('plot-'+token+'.png');side=out.with_suffix('.json')
 out.parent.mkdir(exist_ok=True)
 if not out.exists() or not side.exists():
  with tempfile.NamedTemporaryFile('w',dir=out.parent,prefix='input-',suffix='.json',delete=False) as f:
   json.dump({'output':str(out),'data':plotdata},f);inp=f.name
  try:subprocess.run([sys.executable,str(HERE/'renderer.py'),inp],check=True,stdout=subprocess.DEVNULL)
  finally:Path(inp).unlink(missing_ok=True)
 return str(out)

NORMAL={'easy':['single_turn'],'moderate':['two_turns','jump_ranges'],'hard':['union_ranges','disconnected_ranges','plateau_interval','plateau_union']}

def normal_geometry(level,template,p):
 h=p['h']; left=p['left'];right=p['right'];mid=p['mid'];orient=p['orient'];closure=p['closure'];perm=p['permutation']
 if template=='single_turn':
  a,b=h-left,h+right
  pieces=[[a,left,h,0,True,True],[h,0,b,right,True,True]]
  tests=[[interval(a,h,closure,True)],[interval(h,b,True,not closure)],[interval(h-left//2,b,True,True)]]
 elif template=='two_turns':
  a,t,u,b=h-left,h,h+mid,h+mid+right
  pieces=[[a,0,t,3,1,1],[t,3,u,1,1,1],[u,1,b,4,1,1]]
  tests=[[interval(a,t,closure,True)],[interval(t,u,True,not closure)],[interval(a,u,True,True)]]
 elif template=='jump_ranges':
  a,t,b=h-left,h,h+right
  pieces=[[a,0,t,2,1,0],[t,4,b,1,1,1]]
  # range on left is [0,2), on restricted right [3,4], so whole
  # nonmonotone but one-to-one; extending right reaches overlapping levels.
  z=t+F(right,3)
  tests=[[interval(a,z,closure,True)],[interval(a,t,closure,False)],[interval(a,b,True,True)]]
 elif template=='union_ranges':
  a,t,u,b=h-left,h,h+mid,h+mid+right
  pieces=[[a,0,t,2,1,1],[t,2,u,0,1,1],[u,0,b,-3,1,1]]
  z=a+F(left,2)
  tests=[[interval(a,z,closure,True),interval(u,b,False,not closure)],[interval(t,u,True,True)],[interval(a,u,True,True)]]
 elif template=='disconnected_ranges':
  a,t,u,b=h-left-mid,h-left,h+right,h+right+mid
  pieces=[[a,4,t,2,1,1],[t,-3,h,-1,0,1],[h,-1,u,-3,1,1],[u,2,b,4,0,1]]
  tests=[[interval(t,h,False,True)],[interval(t,u,False,True)],[interval(a,t,closure,True),interval(u,b,True,not closure)]]
 elif template=='plateau_interval':
  a,t,b=h-left,h,h+right
  pieces=[[a,left,t,0,1,1],[t,0,b,0,1,not closure]]
  tests=None
 elif template=='plateau_union':
  a,t,u,b=h-left,h,h+mid,h+mid+right
  pieces=[[a,-3,t,0,1,1],[t,0,u,0,1,1],[u,0,b,3,1,1]]
  tests=None
 else:raise ValueError('unsupported family')
 pieces=[[a,orient*b,c,orient*d,lc,rc] for a,b,c,d,lc,rc in pieces]
 if tests:tests=[tests[j] for j in perm]
 return pieces,tests

def guard(level,template,p):
 if level not in NORMAL or template not in NORMAL[level]:raise ValueError('Template outside difficulty scope')
 if set(p)!=set(('h','left','right','mid','orient','closure','permutation')):raise ValueError('Unexpected/missing parameters')
 if type(p['h'])!=int or not -2<=p['h']<=2:raise ValueError('h must be integer -2..2')
 for k in ('left','right','mid'):
  if type(p[k])!=int or not 2<=p[k]<=4:raise ValueError(k+' must be integer 2..4')
 if type(p['orient'])!=int or p['orient'] not in (-1,1) or type(p['closure']) is not bool:raise ValueError('orientation/closure')
 if not all(type(x)==int for x in p['permutation']) or sorted(p['permutation'])!=[0,1,2]:raise ValueError('permutation')
 # These unused inputs must not manufacture identities or variety.
 if template in ('single_turn','jump_ranges','plateau_interval') and p['mid']!=2:raise ValueError('unused mid must be canonical 2')
 if template=='plateau_union' and p['closure'] is not True:raise ValueError('unused closure must be canonical True')
 if template.startswith('plateau') and p['permutation']!=[0,1,2]:raise ValueError('unused permutation must be canonical')


def authored(level,seed,template,p,profile):
 rng=random.Random(seed)
 if p is None:
  p={'h':rng.randint(-2,2),'left':rng.randint(2,4),'right':rng.randint(2,4),'mid':rng.randint(2,4) if template in ('two_turns','union_ranges','disconnected_ranges','plateau_union') else 2,'orient':rng.choice([-1,1]),'closure':True if template=='plateau_union' else rng.choice([True,False]),'permutation':rng.sample([0,1,2],3) if not template.startswith('plateau') else [0,1,2]}
 guard(level,template,p)
 if profile not in (None,'authored_method'):raise ValueError('unsupported authored profile')
 pieces,tests=normal_geometry(level,template,p)
 plot=render_plots(pieces,tests,'normal')
 atype=':answer.type/text';prompt=f'![]({plot})\n\n'
 if tests:
  bits=[injective(pieces,s) for s in tests]
  correct=subset_label(bits)
  # Complete five-member bank, chosen as a single operation profile: omit each
  # valid interval, include each invalid interval, complement, and claim none/all.
  # Catalog depends only on correct subset; no first-valid choice harvesting.
  catalog={
   (True,False,False):[(True,False,False),(False,True,False),(False,False,True),(True,True,False),(True,False,True)],
   (False,True,False):[(False,True,False),(True,False,False),(False,False,True),(True,True,False),(False,True,True)],
   (False,False,True):[(False,False,True),(True,False,False),(False,True,False),(True,False,True),(False,True,True)],
   (True,True,False):[(True,True,False),(True,False,False),(False,True,False),(True,False,True),(False,True,True)],
   (True,False,True):[(True,False,True),(True,False,False),(False,False,True),(True,True,False),(False,True,True)],
   (False,True,True):[(False,True,True),(False,True,False),(False,False,True),(True,True,False),(True,False,True)]}
  values=[subset_label(x) for x in catalog[tuple(bits)]]
  prompt+='On which of the following intervals is the function $f(x)$ (shown above) invertible?\n\n'+'\n\n'.join(r+'. $x\\in '+settex(s)+'$' for r,s in zip(('I','II','III'),tests))
  # Structured full shared horizontal-line explanation. Every restriction is
  # checked, including a union's cross-component output overlap.
  lines=[]
  for r,s,b in zip(('I','II','III'),tests,bits):
   if b:reason='Indeed, any horizontal line will intersect the restricted graph at most once, no matter where we draw the line.'
   else:reason='Some horizontal lines will intersect the restricted graph more than once.'
   lines.append(f'- On interval {r}, $x\\in {settex(s)}$, the function is '+('invertible. ' if b else '**not** invertible. ')+reason)
  sol=OPEN+'\n\n'+'\n\n'.join(lines)+f'\n\nTherefore, the correct answer is "{correct}".'
  mathematical=digest([template,[[str(F(x-p['h'],p['left'])) if i in (0,2) else str(F(x*p['orient'],p['left'])) if i in (1,3) and template=='single_turn' else str(x*p['orient']) if i in (1,3) else x for i,x in enumerate(z)] for z in pieces],[[[str(F(v-p['h'],p['left'])) if i<2 else v for i,v in enumerate(q)] for q in t] for t in tests]])
 else:
  atype=':answer.type/math';h=p['h'];a=h-p['left'];b=h+p['right'];end=not p['closure']
  if template=='plateau_interval':
   sets=[[interval(a,h)],[interval(a,h,True,False)],[interval(a,b,True,end)],[interval(h,b,True,end)],[interval(a+1,h)]]
   correct=r'x\in '+settex(sets[0])
   prompt+='Which listed interval is greatest by inclusion among the listed intervals on which the function $f(x)$ (shown above) is invertible?'
   sol=f'First, notice that the domain of our function is $x\\in {itex(interval(a,b,True,end))}$.\n\n'+OPEN+f'\n\n- The function does not pass the horizontal line test on $x\\in {itex(interval(h,b,True,end))}$. The horizontal line $y=0$ intersects the graph at more than one point.\n\n- The function is invertible on $x\\in {itex(interval(a,h))}$. On this interval, a horizontal line will intersect the curve at most once, no matter where we draw the line.\n\nTherefore, the greatest listed interval on which the function is invertible is:\n\n$$\nx\\in {itex(interval(a,h))}\n$$'
  else:
   u=h+p['mid'];b=u+p['right']
   sets=[[interval(a,h),interval(u,b,False,True)],[interval(a,b)],[interval(a,h,True,False)],[interval(h,b)],[interval(a,u)]]
   correct=r'x\in '+settex(sets[0])
   # Specify among listed choices: maximal domains of a plateau are not unique.
   prompt+='Which listed domain retains every input outside the constant segment and is maximal by inclusion among the listed domains on which $f(x)$ is invertible?'
   sol=OPEN+f'\n\n- On $x\\in {itex(interval(h,u))}$ the graph is constant, so we can retain only one point at output $y=0$.\n\n- On $x\\in {settex(sets[0])}$ the left piece has output at most zero and the right piece has output greater than zero. Each piece is one-to-one, and their ranges do not overlap.\n\n- Adding any excluded plateau point repeats the output zero. Every other listed domain either omits a nonconstant piece or fails the horizontal line test.\n\nTherefore, the correct listed domain is:\n\n$$\nx\\in {settex(sets[0])}\n$$'
  values=[r'x\in '+settex(s) for s in sets]
  # Maximal criterion: smaller injective intervals remain mathematically
  # invertible, but do not satisfy the explicit requested maximal response.
  if not injective(pieces,sets[0]):raise ValueError('Correct maximal set fails HLT')
  mathematical=digest([template,str(F(p['right'],p['left'])),str(F(p['mid'],p['left'])) if template=='plateau_union' else None,end if template=='plateau_interval' else None])
 return make_record(level,prompt,sol,values,correct,atype,seed,{'template':template,'bank_profile':'authored_method','parameters':p,'authored':True,'eligible_for_learning':True,'evidence_only':False,'mathematical_fingerprint':mathematical,'plot':plot,'pieces':pieces,'restrictions':tests})


def observed(level,seed,profile,p):
 q=QUESTIONS[profile];original_level=q[':question/difficulty'][':db/ident'].rsplit('/',1)[-1]
 if level!=original_level:raise ValueError('Observed difficulty guard')
 p={'x_shift':0} if p is None else p
 if set(p)!= {'x_shift'} or type(p['x_shift'])!=int or not -2<=p['x_shift']<=2:raise ValueError('Evidence translation -2..2 only')
 h=p['x_shift'];pieces=[[a+h,b,c+h,d,lc,rc] for a,b,c,d,lc,rc in LANDMARKS[profile]]
 # Extracted interval masks produce every prompt/prose/bank component through
 # the same coordinate operation. Original raster slots are filled separately.
 def textmask(text):return transformed_intervals(text,h)
 prompt=textmask(q[':question/problem']);sol=textmask(q[':question/worked-solution'])
 if h:
  finite=[v for z in pieces for v in (z[0],z[2]) if abs(v-h)<20]
  clipped=[[max(a,h-5),b if a>=h-5 else b+(d-b)*(h-5-a)/(c-a),min(c,h+6),d if c<=h+6 else b+(d-b)*(h+6-a)/(c-a),lc,rc] for a,b,c,d,lc,rc in pieces]
  plot=render_plots(clipped,None,'evidence')
  prompt=re.sub(r'!\[\]\([^)]*\)',f'![]({plot})',prompt)
  # Surrogate solution plots are explicitly evidence-only, rather than claiming
  # their exact horizontal-line witnesses or shape recovered from source ink.
  sol=re.sub(r'!\[\]\([^)]*\)',f'![]({plot})',sol)
 fields=q[':question/answer-fields'];f=fields[0]
 values=[textmask(a[':answer/value']) for a in f[':answer-field/choices']]
 def evidence_set(text):
  ss=parse_intervals(text)
  return [[a+h if abs(a)==99 else a,b+h if abs(b)==99 else b,lc,rc] for a,b,lc,rc in ss]
 if 'following intervals' in prompt:
  requested=[evidence_set(line) for line in prompt.split('invertible?',1)[-1].splitlines() if parse_intervals(line)]
  true_label=subset_label([injective(pieces,ss) for ss in requested])
  matches=[v for v in values if ' '.join(v.split())==true_label]
 else:
  sets=[evidence_set(v) for v in values];valid=[injective(pieces,ss) for ss in sets]
  matches=[v for i,(v,ss) in enumerate(zip(values,sets)) if valid[i] and all(not valid[j] or spset(other).is_subset(spset(ss)) for j,other in enumerate(sets))]
 if len(matches)!=1:raise ValueError('Raw evidence bank has no unique eligible displayed response')
 correct=matches[0];atype=f[':answer-field/choices'][0][':answer/type'][':db/ident']
 r=make_record(level,prompt,sol,values,correct,atype,seed,{'template':'source_'+profile,'bank_profile':profile,'parameters':p,'authored':False,'source_id':profile,'eligible_for_learning':False,'evidence_only':True,'geometry_status':'original raster at x_shift=0; qualitative landmark surrogate otherwise','mathematical_fingerprint':digest(['source_geometry',profile]),'pieces':[[str(v) if isinstance(v,F) else v for v in z] for z in pieces]},q)
 for key in (':db/id',':question/math-academy-id'):
  if key in q:r['question'][key]=q[key]
 nf=r['question'][':question/answer-fields'][0]
 if ':db/id' in f:nf[':db/id']=f[':db/id']
 for na in nf[':answer-field/choices']:
  old=next(a for a in f[':answer-field/choices'] if textmask(a[':answer/value'])==na[':answer/value'])
  if ':db/id' in old:na[':db/id']=old[':db/id']
 return r


def current_layout(record):
 """Preserve the assessed restrictions; each now owns a true/false bank."""
 if record['generation']['evidence_only'] or record['generation']['restrictions'] is None:return record
 q=record['question'];bits=[injective(record['generation']['pieces'],s) for s in record['generation']['restrictions']]
 q[':question/problem']=q[':question/problem'].replace('invertible?\n\n','invertible?\n\nSelect all that apply.\n\n')
 identity=digest([VERSION,q[':question/difficulty'],q[':question/problem'],q[':question/worked-solution'],bits])
 q[':question/id']=uid(identity);q[':question/answer-fields']=[]
 for key,bit in zip(('I','II','III'),bits):
  fid=uid(identity+'/'+key)
  choices=[{':answer/id':uid(fid+'/'+value),':answer/type':':answer.type/text',':answer/value':value} for value in ('false','true')]
  q[':question/answer-fields'].append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':choices,':answer-field/correct':[':answer/id',uid(fid+'/'+str(bit).lower())]})
 record['generation'].update(content_identity=identity,bank_profile='current_boolean_fields',response_layout='three independent checkbox fields')
 return record

def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if field_type not in (None,'radio',':answer-field.type/radio','checkbox',':answer-field.type/checkbox'):raise ValueError('unsupported field layout')
 if profile in QUESTIONS:
  if template not in (None,'source_'+profile):raise ValueError('evidence template mismatch')
  return observed(level,seed,profile,parameters)
 if template and template.startswith('source_'):
  return observed(level,seed,template[7:],parameters)
 if level not in NORMAL:raise ValueError('unknown difficulty')
 template=template or random.Random(seed).choice(NORMAL[level])
 return current_layout(authored(level,seed,template,parameters,None if profile=='current_boolean_fields' else profile))

# EASY: authored missing level, one turning point and three finite restrictions.
def generate_easy(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('easy',seed,template,field_type,parameters,profile)
# MODERATE: two turns or a jump requiring cross-piece output-range comparison.
def generate_moderate(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('moderate',seed,template,field_type,parameters,profile)
# HARD: disconnected restrictions or maximal set/interval with a plateau.
def generate_hard(seed=0,template=None,field_type=None,parameters=None,profile=None):return generate('hard',seed,template,field_type,parameters,profile)

def markdown(record):
 q=record['question'];gen=record['generation'];raw=gen['evidence_only']
 label=('Original source evidence' if gen['parameters']['x_shift']==0 else 'Generated evidence variant') if raw else 'Generated variant'
 level=q.get(':question/difficulty','unrated').split('/')[-1]
 lines=['## '+label+' — '+level+' ('+('observed' if raw else 'authored')+')','',q[':question/problem'],'','Choices:']
 for f in q.get(':question/answer-fields',[]):
  lines.append('Field '+f[':answer-field/key']+':')
  for a in f[':answer-field/choices']:
   value='$'+a[':answer/value']+'$' if a[':answer/type']==':answer.type/math' else a[':answer/value']
   lines.append('- '+value+(' **(source designation)**' if raw else ' **(correct)**' if a[':answer/id']==f[':answer-field/correct'][1] else '') if a[':answer/id']==f[':answer-field/correct'][1] else '- '+value)
 lines+=['','Worked solution'+(' (original evidence; ineligible)' if raw else '')+':','',q.get(':question/worked-solution','Absent')]
 return '\n'.join(lines).replace('![](images/','![](/media/jake/SSD/EDB/math/images/')

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');ap.add_argument('--seed',type=int,default=0);ap.add_argument('--count',type=int,default=1);ap.add_argument('--format',choices=['markdown','json'],default='markdown');ap.add_argument('--template');ap.add_argument('--profile');args=ap.parse_args()
 levels=list(NORMAL) if args.difficulty=='all' else [args.difficulty]
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in levels for i in range(args.count)]
 if args.format=='json':print(json.dumps(records,indent=2,default=str))
 else:print('\n\n---\n\n'.join(markdown(r) for r in records))

# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':main()
