#!/usr/bin/env python3
"""KP classification generator; this module never writes to the database.

Basis 1356 source masks contain full mathematical-component slots. Column scales
and variable translations parameterize *every* observed matrix/equation stage;
row operations are executed exactly, never replayed by returning source payloads.
15 observed moderate layouts preserve current checkbox/radio response contracts.
q-32242's unstated R1 negation is repaired (raw evidence retained). Easy 2x2 and
hard 3x3 are authored scope claims anchored to the lesson's Gaussian elimination
and pivot/free-variable definitions. Read the evidence README for validation.
"""
from __future__ import annotations
import argparse,hashlib,json,random,re,sys,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/question_capture'))
from math_format import normalize_prose, matrix_tex as format_matrix, checked_math_content
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
KP_ID=17592186115299
KP_UUID='f9469d5c-e097-590c-8ddb-2c7fda353fac'
TITLE='Classifying a System as Consistent Dependent, Consistent Independent, or Inconsistent'
VERSION='classification-2'
D=Path(__file__).with_suffix('')
TEMPLATES=json.loads((D/'templates.json').read_text())
X=sp.symbols('x y z')
MATRIX_RE=r'\[\\begin\{aligned\}(.*?)\\end\{aligned\}\]'
SYSTEM_RE=r'\\begin\{aligned\}(.*?)\\end\{aligned\}'
WORDS={'dependent':'The system is consistent dependent','independent':'The system is consistent independent','inconsistent':'The system is inconsistent'}
ROMAN=['I','II','III']
BANKS={}
for t in TEMPLATES.values():
 key='bank-'+hashlib.sha256(json.dumps(sorted(t['bank'])).encode()).hexdigest()[:8]
 BANKS[key]=sorted(t['bank']);t['profile']=key

def number(s):
 s=s.strip().replace(' ','')
 s=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',s)
 return sp.Rational(sp.sympify(s))

def tex(v):
 return sp.latex(sp.Rational(v)).replace(' ','')

def parse_matrix(s):
 body=re.search(MATRIX_RE,s,re.S).group(1)
 return sp.Matrix([[number(c) for c in row.split('&')] for row in body.split(r'\\')])

def parse_system(s):
 body=re.search(SYSTEM_RE,s,re.S).group(1)
 rows=body.split(r'\\');n=3 if 'z' in body else 2
 out=[]
 for row in rows:
  row=row.replace('&','').strip().rstrip('.,');left,right=row.split('=')
  def expr(v):
   v=re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',v)
   return parse_expr(v,local_dict=dict(zip('xyz',X)),transformations=standard_transformations+(implicit_multiplication_application,))
  e=sp.expand(expr(left));out.append([e.coeff(x) for x in X[:n]]+[expr(right)])
 return sp.Matrix(out)

def matrix_tex(m):
 return format_matrix([[tex(v) for v in m.row(i)] for i in range(m.rows)], augmented=True)

def lhs(row,zero=False):
 out=''
 for c,x in zip(row[:-1],'xyz'):
  if c==0 and not zero:continue
  term=(('' if abs(c)==1 else tex(abs(c)))+x) if c else '0'+x
  out+=('-' if c<0 else '+' if out else '')+term
 return out or '0'

def equation(row,zero=False):return lhs(row,zero)+'='+tex(row[-1])

def fill_system(component,m):
 # Preserve original wrapper, row prefixes, final punctuation, and whitespace.
 body=re.search(SYSTEM_RE,component,re.S).group(1);rows=body.split(r'\\');new=[]
 assert len(rows)==m.rows
 for i,old in enumerate(rows):
  match=re.fullmatch(r'(\s*(?:&\s*)?)(.*?)([.,]?)(\s*)',old,re.S)
  new.append(match[1]+equation(list(m.row(i)))+match[3]+match[4])
 return component.replace(body,r'\\'.join(new),1)

def stages(m,ops):
 result=[m.copy()]
 for op in ops:
  m=m.copy();kind,i,*rest=op
  if kind=='swap':m.row_swap(i,rest[0])
  elif kind=='scale':m[i,:]=m[i,:]*sp.Rational(rest[0])
  else:j,c=rest;m[i,:]=m[i,:]+sp.Rational(c)*m[j,:]
  result.append(m)
 return result

def classify(m):
 r=m[:,:-1].rank();a=m.rank()
 return 'inconsistent' if r<a else 'independent' if r==m.cols-1 else 'dependent'

def statements(prompt):
 values=[]
 for line in prompt.splitlines():
  if re.match(r'^(?:-|I\.|II\.|III\.) ',line):
   values.append('dependent' if 'consistent dependent' in line else 'independent' if 'independent' in line or 'unique solution' in line else 'inconsistent')
 assert len(values)==3 and len(set(values))==3
 return values

def correct_for(prompt,m):return ROMAN[statements(prompt).index(classify(m))]+' only'

def observed(name,p):
 t=TEMPLATES[name];base=parse_matrix(t['math_components'][1]);n=base.cols-1
 if set(p)!={'scales','translations'}:raise ValueError('Observed parameters require scales and translations')
 if len(p['scales'])!=n or len(p['translations'])!=n:raise ValueError('Wrong variable count')
 if any(type(v)!=int or not 1<=abs(v)<=2 for v in p['scales']):raise ValueError('Scale magnitudes must be 1 or 2')
 if any(type(v)!=int or abs(v)>2 for v in p['translations']):raise ValueError('Translation magnitudes at most 2')
 s=sp.diag(*p['scales']);a=base[:,:-1]*s;b=base[:,-1]-base[:,:-1]*sp.Matrix(p['translations']);m=a.row_join(b)
 st=stages(m,t['operations']);final=st[-1];values={}
 unique=classify(m)=='independent'
 sol=list(a.inv()*b) if unique and a.rows==a.cols else list(sp.linsolve((a,b)))[0] if unique else None
 for i,c in enumerate(t['math_components']):
  if i==0:out=fill_system(c,m)
  elif i==1:out=re.sub(MATRIX_RE,lambda _:matrix_tex(m),c,flags=re.S)
  elif i==2:
   counter=iter(st);out=re.sub(MATRIX_RE,lambda _:matrix_tex(next(counter)),c,flags=re.S)
  elif '\\begin{aligned}' in c:out=fill_system(c,final[:2,:])
  elif '⟹' in c:
   row=list(final.row(0));yv=sol[1];co=row[1]
   sub=('-' if co<0 else '+')+('' if abs(co)==1 else tex(abs(co)))+'('+tex(yv)+')'
   out='$$\n'+lhs([row[0],0,row[-1]])+sub+'='+tex(row[-1])+r'\,⟹\,x='+tex(sol[0])+'.\n$$'
  elif re.search(r'\$[xyz]=',c):
   var=c[1];punct='.' if c.endswith('.$') else ''
   out='$'+var+'='+tex(sol['xyz'.index(var)])+punct+'$'
  elif c.startswith('$0x'):
   punct=',' if c.endswith(',$') else ''
   out='$'+equation(list(final.row(final.rows-1)),True)+punct+'$'
  else:out=c
  values['slot_'+str(i)]=out
 def fill(mask):
  return re.sub(r'\{\{(slot_\d+)\}\}',lambda v:values[v[1]],mask)
 return re.sub(r'(?<!\\)\{(?=\\begin\{aligned\})',lambda _:r'\{',fill(t['problem_mask'])),re.sub(r'(?<!\\)\{(?=\\begin\{aligned\})',lambda _:r'\{',fill(t['solution_mask'])),m,st,t['operations']

# All authored levels assess the same categorical distinction; there is no
# within-level sequence, constant-parameter puzzle, or request for general vectors.
def authored(level,p):
 if set(p)!={'matrix','order'}:raise ValueError('Authored parameters require matrix and order')
 m=sp.Matrix([[sp.Rational(str(v)) for v in row] for row in p['matrix']]);n=2 if level=='easy' else 3
 if m.shape!=(n,n+1) or sorted(p['order'])!=sorted(WORDS):raise ValueError('Wrong shape or statement order')
 bound=16 if level=='easy' else 40
 if any(v.q!=1 or abs(v)>bound for v in m):raise ValueError('Authored integral coefficient magnitude bound exceeded')
 if any(m[i,i]==0 for i in range(n-1)):raise ValueError('First elimination pivots cannot be zero')
 ops=[];work=m.copy()
 for j in range(n-1):
  if work[j,j]==0:raise ValueError('Unsupported zero pivot')
  for i in range(j+1,n):
   c=-work[i,j]/work[j,j]
   if c==0:raise ValueError('Authored rows must require each substantive elimination')
   ops.append(['add',i,j,str(c)]);work[i,:]+=c*work[j,:]
 st=stages(m,ops)
 if level=='easy' and any(v.q>2 for z in st for v in z):raise ValueError('Easy arithmetic requires integral or half-integral stages')
 if level=='hard' and any(v.q>6 for z in st for v in z):raise ValueError('Hard arithmetic denominator bound is six')
 prompt='Consider the following system of equations.\n\n$$\n'+r'\{\begin{aligned}'+r' \\ '.join(equation(list(m.row(i))) for i in range(n))+r'\end{aligned}'+'\n$$\n\nWhich of the following statements are true?\n\n'+'\n'.join(ROMAN[i]+'. '+WORDS[k] for i,k in enumerate(p['order']))
 chain=matrix_tex(st[0])
 for op,z in zip(ops,st[1:]):
  _,i,j,c=op;chain+=' & '+r'{R}_{'+str(i+1)+r'}:={R}_{'+str(i+1)+'}+('+tex(c)+r'){R}_{'+str(j+1)+r'} \\ & ∼'+matrix_tex(z)
 kind=classify(m)
 if kind=='inconsistent':
  row=next(list(z.row(i)) for i in range(z.rows) if all(v==0 for v in z.row(i)[:-1]) and z[i,-1]!=0)
  conclusion='The final row corresponds to the equation $'+equation(row,True)+',$ and this has no solution. Therefore, our system has no solution, and we conclude that the system is inconsistent.'
 elif kind=='dependent':
  pivots=m[:,:-1].rref()[1];free=[v for i,v in enumerate('xyz'[:n]) if i not in pivots]
  conclusion='The basic variables are the variables whose coefficients are pivots. Here there '+('is one free variable, $'+free[0]+'$.' if len(free)==1 else 'are free variables, $'+', '.join(free)+'$.')+' Therefore, since there are infinitely many solutions, we conclude that the system is *consistent dependent*.'
 else:conclusion='There is a pivot for each variable and no contradictory row. The system has a unique solution, so we conclude that the system is consistent independent.'
 solution='To classify the system, we first need to find its solution. The augmented matrix for this system is\n\n$$\nM='+matrix_tex(m)+'.\n$$\n\nUsing the method of Gaussian elimination, we can reduce this matrix to row echelon form as follows:\n\n$$\n'+r'\begin{aligned}M & ='+chain+r'\end{aligned}'+'\n$$\n\n'+conclusion+'\n\nAs a result, only statement '+correct_for(prompt,m).split()[0]+' is true.'
 return prompt,solution,m,st,ops

def sample(level,name,rng):
 if level=='moderate':
  n=parse_matrix(TEMPLATES[name]['math_components'][1]).cols-1
  return {'scales':[rng.choice([-2,-1,1,2]) for _ in range(n)],'translations':[rng.randint(-2,2) for _ in range(n)]}
 kind=rng.choice(list(WORDS));n=2 if level=='easy' else 3
 # Construct complete rank patterns before mixing rows. These are same-method
 # variations with integer/short rational Gaussian elimination, not extra skills.
 t=sp.zeros(n,n+1)
 for i in range(n-1):
  t[i,i]=1
  for j in range(i+1,n):t[i,j]=rng.choice([-3,-2,-1,1,2,3])
  t[i,-1]=rng.randint(-5,5)
 if kind=='independent':t[n-1,n-1]=rng.choice([-2,-1,1,2]);t[n-1,-1]=rng.randint(-5,5)
 elif kind=='inconsistent':t[n-1,-1]=rng.choice([-4,-3,-2,-1,1,2,3,4])
 # Reversed elementary row additions require all n(n-1)/2 reductions.
 for i in range(n-1,0,-1):
  for j in range(i-1,-1,-1):t[i,:]+=rng.choice([-2,-1,1,2])*t[j,:]
 order=list(WORDS);rng.shuffle(order)
 return {'matrix':[[int(v) for v in t.row(i)] for i in range(n)],'order':order}

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def generate_legacy(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ['easy','moderate','hard']:raise ValueError('Unknown level')
 if field_type not in [None,'radio',':answer-field.type/radio']:raise ValueError('Only observed radio layout is supported')
 rng=random.Random(seed)
 if template is None:template=rng.choice(list(TEMPLATES)) if level=='moderate' else level+'_authored'
 if level=='moderate' and template not in TEMPLATES or level!='moderate' and template!=level+'_authored':raise ValueError('Template not available at requested level')
 profile=profile or (TEMPLATES[template]['profile'] if level=='moderate' else sorted(BANKS)[0])
 if profile not in BANKS:raise ValueError('Unknown complete bank')
 explicit=parameters is not None
 for _ in range(500):
  p=parameters if explicit else sample(level,template,rng)
  try:prompt,solution,m,st,ops=observed(template,p) if level=='moderate' else authored(level,p);break
  except ValueError:
   if explicit:raise
 else:raise ValueError('Sampling failed')
 correct=correct_for(prompt,m);bank=BANKS[profile]
 if correct not in bank or len(bank)!=5 or len(set(bank))!=5:raise ValueError('Incomplete/ambiguous bank')
 # Mathematical task identity normalizes each printed equation up to nonzero
 # scalar and ignores row order/bank/layout. Arbitrary row combinations change
 # the assessed elimination arithmetic and are not deduplicated by solution set.
 normalized=[]
 for row in m.tolist():
  first=next((v for v in row if v!=0),sp.Integer(1))
  normalized.append([str(v/first) for v in row])
 mf=digest({'variables':list('xyz'[:m.cols-1]),'normalized_equations':sorted(normalized)})
 cf=digest({'version':VERSION,'mathematical_fingerprint':mf,'prompt':prompt,'solution':solution,'bank':sorted(bank),'correct':correct})
 qid=uuid.uuid5(uuid.NAMESPACE_URL,KP_UUID+'/'+cf);fid=uuid.uuid5(qid,'selection')
 answers=[{':answer/id':str(uuid.uuid5(fid,v)),':answer/type':':answer.type/text',':answer/value':v} for v in bank]
 cid=next(a[':answer/id'] for a in answers if a[':answer/value']==correct);rng.shuffle(answers)
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':TITLE},'question':{':question/id':str(qid),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':solution,':question/answer-fields':[{':answer-field/id':str(fid),':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',cid]}]},'generation':{'version':VERSION,'seed':seed,'template':template,'parameters':p,'bank_profile':profile,'mathematical_fingerprint':mf,'parameter_fingerprint':mf,'content_fingerprint':cf,'authored_extension':level!='moderate','parameter_extension':level=='moderate' and any(v!=1 for v in p['scales']) or level=='moderate' and any(p['translations']),'source_analysis':{'database':'math','basis':1356,'lineage':'01a12a15-3e0a-75a1-9dac-f8b8c5d5c3f1','question_ids':[template] if level=='moderate' else [],'curriculum_topic':17592186048445},'source_repairs':(['q-32242 unstated R1 negation removed'] if template=='q-32242' else [])+(['Unmatched unescaped system opening brace escaped'] if template in TEMPLATES and any(re.search(r'(?<!\\)\{(?=\\begin\{aligned\})',c) for c in TEMPLATES[template]['math_components']) else []),'plot_rating':'none','plot_assets':{},'operations':ops,'stages':[[[str(v) for v in row] for row in z.tolist()] for z in st],'classification':classify(m)}}

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 """Preserve the captured current response contract, with field-owned identities.

 Historical radio banks remain replayable through generate_legacy. Current
 checkbox templates have three Boolean banks; the added q-74834 remains radio.
 Easy/hard use the current three-checkbox contract as a documented extension.
 """
 rec=generate_legacy(level,seed,template,None,parameters,profile)
 q=rec['question'];meta=rec['generation'];name=meta['template']
 layouts=json.loads((D/'current-layouts.json').read_text())
 kind=layouts[name]['type'] if level=='moderate' else 'checkbox'
 truth=next(a[':answer/value'].split()[0] for f in q[':question/answer-fields'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
 if field_type not in [None,kind,':answer-field.type/'+kind]:raise ValueError('Field type differs from current template')
 if kind=='checkbox':
  prefix,tail=q[':question/problem'].split('Which of the following statements are true?',1)
  lines=[s for s in tail.splitlines() if re.match(r'^(?:-|I\.|II\.|III\.) ',s)]
  texts=[re.sub(r'^(?:-|I\.|II\.|III\.)\s*','',s) for s in lines]
  q[':question/problem']=prefix+'Which of the following statements are true?\n\nSelect all that apply.\n\n'+'\n'.join('- **'+roman+'.** '+value for roman,value in zip(ROMAN,texts))
 q[':question/problem']=normalize_prose(q[':question/problem'])
 q[':question/worked-solution']=normalize_prose(q[':question/worked-solution'])
 cf=digest({'version':VERSION,'mathematical_fingerprint':meta['mathematical_fingerprint'],'problem':q[':question/problem'],'solution':q[':question/worked-solution'],'response':kind,'bank':sorted(BANKS[meta['bank_profile']]) if kind=='radio' else ['false','true']})
 qid=uuid.uuid5(uuid.NAMESPACE_URL,KP_UUID+'/'+cf);q[':question/id']=str(qid)
 if kind=='checkbox':
  fields=[]
  for roman in ROMAN:
   fid=uuid.uuid5(qid,roman)
   answers=[{':answer/id':str(uuid.uuid5(fid,value)),':answer/type':':answer.type/text',':answer/value':value} for value in ['false','true']]
   correct='true' if roman==truth else 'false'
   fields.append({':answer-field/id':str(fid),':answer-field/key':roman,':answer-field/type':':answer-field.type/checkbox',':answer-field/choices':answers,':answer-field/correct':[':answer/id',str(uuid.uuid5(fid,correct))]})
  q[':question/answer-fields']=fields
 else:
  f=q[':question/answer-fields'][0];old=f[':answer-field/correct'][1];correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==old)
  fid=uuid.uuid5(qid,'selection');f[':answer-field/id']=str(fid)
  for a in f[':answer-field/choices']:a[':answer/id']=str(uuid.uuid5(fid,a[':answer/value']))
  f[':answer-field/correct']=[':answer/id',str(uuid.uuid5(fid,correct))]
 meta.update(content_fingerprint=cf,response_layout=kind,current_source_basis=2304)
 meta['source_analysis']['basis']=2304
 meta['dependencies']={'python':sys.version.split()[0],'sympy':sp.__version__}
 meta['domain']='Real linear systems; exact rational Gaussian elimination. Arithmetic and parameter bounds: classification-current.md and template-extraction.md.'
 return rec

def generate_easy(seed=0,**kwargs):return generate('easy',seed,**kwargs)
def generate_moderate(seed=0,**kwargs):return generate('moderate',seed,**kwargs)
def generate_hard(seed=0,**kwargs):return generate('hard',seed,**kwargs)
def render_plots(instance,output_dir=None):return {}

def markdown(record):
 q=record['question'];f=q[':question/answer-fields'][0]
 if f[':answer-field/type']==':answer-field.type/checkbox':
  return q[':question/problem']+'\n\nWorked solution:\n\n'+q[':question/worked-solution']
 return q[':question/problem']+'\n\n'+'\n'.join('- '+a[':answer/value'] for a in f[':answer-field/choices'])+'\n\nWorked solution:\n\n'+q[':question/worked-solution']


# Every learner-facing checkbox question has a nonempty correct selection.
import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(next(p for p in _PolicyPath(__file__).resolve().parents if (p / "scripts/generator_policy.py").is_file())))
from scripts.generator_policy import nonempty_checkbox as _nonempty_checkbox
for _policy_name in ['generate', 'generate_easy', 'generate_hard', 'generate_legacy', 'generate_moderate']:
    globals()[_policy_name] = _nonempty_checkbox(globals()[_policy_name], none_label='None of the above')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['json','markdown'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 records=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(records,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in records))
