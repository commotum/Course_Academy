#!/usr/bin/env python3
"""Exact consistent-system Gauss–Jordan generator, math basis 1356.

All 11 observed banks compile into complete-component affine templates, rather
than returning source payloads. Source profiles preserve row-operation sequence
and every sentence; all scalar/vector mathematics is recomputed under the
invertible change X_new = scale*X_old + offsets. Thus unknown distractor intent
is not guessed: these profiles transport complete observed mathematical objects.
Normal defaults use explicitly authored complete operation-error banks and
coefficient variety. Moderate/hard are authored curriculum-bounded extensions.
No plots are required: captured SVGs are mathematical typesetting only.
"""
from pathlib import Path
import argparse, hashlib, json, random, re, uuid, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts/question_capture'))
from math_format import normalize_prose, normalize_tex, matrix_tex as format_matrix, system_tex as format_system, checked_math_content
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP=17592186115241
HERE=Path(__file__).resolve().with_suffix('')
VERSION='1.0.0'
FAMILIES={'q-32234':'unrated_constant_x','q-42040':'unrated_sign_coupled','q-131715':'two_additions_subscript','q-131717':'two_additions_subscript','q-32247':'two_additions_subscript','q-32244':'rank_one_three_operations','q-131712':'rank_one_three_operations','q-32517':'scale_then_eliminate_constant_pivot','q-42041':'scale_then_eliminate_full_vector','q-42019':'one_addition_constant_pivot','q-32220':'one_addition_latter_prose'}
RAW=json.loads((HERE/'source.json').read_text())
RECORD=RAW['record']
QUESTIONS={q[':question/math-academy-id']:q for q in RECORD[':knowledge-point/questions']}
VARS=sp.symbols('x y z w')
TRANSFORMS=standard_transformations+(implicit_multiplication_application,)
INNER=re.compile(r'\\begin\{aligned\}((?:(?!\\begin\{aligned\}).)*?)\\end\{aligned\}',re.S)
BASE={
 'q-32234':[[1,1,2,19],[3,1,2,31]], 'q-42040':[[1,0,3,-2],[1,1,0,0]],
 'q-131715':[[1,-1,2,2],[1,0,-3,1]],'q-131717':[[1,3,1,-1],[-2,-5,0,3]],
 'q-32244':[[2,2,5],[-10,-10,-25],[8,8,20]],'q-32517':[[2,2,4,-4],[0,1,2,-6]],
 'q-42041':[[2,0,-4,2],[4,1,-5,4]],'q-131712':[[2,8,-6],[-4,-16,12],[6,24,-18]],
 'q-32247':[[1,2,-2,4],[-2,-3,-2,-2]],'q-42019':[[1,-2,2,2],[0,1,-1,-1]],
 'q-32220':[[1,1,1,2],[0,1,2,0]]}

def load_expr(s):
 s=s.strip().rstrip('.,').replace('−','-')
 s=re.sub(r'\{x\}_\{([1234])\}',lambda m:str(VARS[int(m[1])-1]),s)
 s=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',s)
 return parse_expr(s,local_dict={str(v):v for v in VARS},transformations=TRANSFORMS)

def tex(e,subscript=False):
 out=sp.latex(sp.expand(e),order='lex').replace(' ','')
 if subscript:
  for i,v in enumerate(VARS):out=re.sub(r'(?<![A-Za-z\\])'+str(v)+r'(?![A-Za-z])',r'{x}_{'+str(i+1)+'}',out)
 return out

def matrix_tex(M, *, augmented=True):
 return format_matrix([[tex(v) for v in row] for row in M.tolist()], augmented=augmented)

def vector_tex(values,free,subscript=False,bmatrix=False):
 body=r' \\ '.join(tex(v,subscript) for v in values)
 vector='\\begin{bmatrix}'+body+'\\end{bmatrix}'
 return vector+r',\,'+tex(free,subscript)+r'\in (-\infty ,\infty )'

def fingerprint(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.NAMESPACE_URL,'course-academy:'+str(KP)+':'+x))
def serialize(M):return [[str(v) for v in row] for row in M.tolist()]

def affine_matrix(M,scale,offsets):
 M=sp.Matrix(M); out=M.copy();out[:,-1]=scale*M[:,-1]+M[:,:-1]*sp.Matrix(offsets);return out

def affine_expr(e,index,scale,offsets):
 return sp.expand(scale*e.subs({VARS[i]:(VARS[i]-offsets[i])/scale for i in range(len(offsets))},simultaneous=True)+offsets[index])

def compile_math(text,scale,offsets):
 """Mask complete innermost matrices, systems, and vectors, preserving prose.
 Source operations have unchanged coefficients under the affine transformation.
 No short expression is replaced globally.
 """
 sub='{x}_{' in text
 def replace(m):
  body=m[1];rows=body.split(r'\\');new=[]
  if '&' in body and '=' not in body:
   mat=sp.Matrix([[load_expr(v) for v in row.split('&')] for row in rows])
   mat=affine_matrix(mat,scale,offsets)
   return r'\begin{array}{'+'c'*(mat.cols-1)+'|c}'+r' \\ '.join(' & '.join(tex(v) for v in row) for row in mat.tolist())+r'\end{array}'
  if '=' in body:
   for row in rows:
    lead=re.match(r'\s*(?:&\s*)?',row)[0];clean=row[len(lead):];lhs,rhs=clean.split('=',1)
    punctuation=rhs[-1] if rhs and rhs[-1] in '.,' else ''
    L=load_expr(lhs);R=load_expr(rhs)
    newrhs=sp.expand(scale*R.subs({VARS[i]:(VARS[i]-offsets[i])/scale for i in range(len(offsets))},simultaneous=True)+L.subs({VARS[i]:offsets[i] for i in range(len(offsets))}))
    new.append(lead+lhs+'='+tex(newrhs,sub)+punctuation)
  else:
   for i,row in enumerate(rows):new.append(tex(affine_expr(load_expr(row),i,scale,offsets),sub))
  return r'\begin{aligned}'+r' \\ '.join(new)+r'\end{aligned}'
 out=INNER.sub(replace,text)
 # Literal source system braces are unclosed TeX groups; escaped brace is a glyph.
 out=re.sub(r'(?<!\\)\{(?=\\begin\{aligned\})',lambda _:r'\{',out)
 return out

def parse_vector(value):
 normalized=value.replace('\\\\','\\') if r'\\begin' in value else value
 m=re.search(r'\\begin\{(?:aligned|bmatrix)\}(.*?)\\end\{(?:aligned|bmatrix)\}',normalized,re.S)
 if not m:return None
 return [load_expr(s) for s in m[1].split(r'\\')]

def rref_steps(M):
 """Standard deterministic Gauss–Jordan operations, never skip displayed stages."""
 out=M.copy();states=[out.copy()];ops=[];r=0
 for c in range(M.cols-1):
  pivot=next((i for i in range(r,M.rows) if out[i,c]!=0),None)
  if pivot is None:continue
  if pivot!=r:
   out.row_swap(pivot,r);ops.append(('swap',r,pivot,sp.Integer(1)));states.append(out.copy())
  if out[r,c]!=1:
   a=1/out[r,c];out.row_op(r,lambda v,j:a*v);ops.append(('scale',r,r,a));states.append(out.copy())
  for i in range(M.rows):
   if i!=r and out[i,c]!=0:
    a=-out[i,c];out.row_op(i,lambda v,j:v+a*out[r,j]);ops.append(('add',i,r,a));states.append(out.copy())
  r+=1
  if r==M.rows:break
 return states,ops

def operation_tex(op):
 kind,i,j,a=op;ri=r'{R}_{'+str(i+1)+'}';rj=r'{R}_{'+str(j+1)+'}'
 if kind=='swap':return ri+r'\leftrightarrow '+rj
 if kind=='scale':return ri+':='+tex(a)+ri
 return ri+':='+ri+'+('+tex(a)+')'+rj

def solution_vector(M):
 R,piv=M.rref(); n=M.cols-1
 if n in piv:raise ValueError('inconsistent instance')
 free=[i for i in range(n) if i not in piv];out=list(VARS[:n])
 for row,col in enumerate(piv):out[col]=sp.expand(R[row,-1]-sum(R[row,j]*VARS[j] for j in free))
 return R,list(piv),free,out

def linear_tex(coefficients,sub=False):
 # Follow the declared augmented-matrix columns, never SymPy's lexical w-first order.
 parts=[]
 for coefficient,variable in zip(coefficients,VARS):
  if coefficient==0:continue
  sign='-' if coefficient<0 else ('+' if parts else '')
  magnitude=abs(coefficient)
  parts.append(sign+('' if magnitude==1 else tex(magnitude))+tex(variable,sub))
 return ''.join(parts) or '0'
def equation_tex(row,sub=False):
 return linear_tex(row[:-1],sub)+'='+tex(row[-1])
def system_tex(M,sub=False):
 rows=[equation_tex(row,sub) for row in M.tolist() if any(row)]
 rows[-1]+='.'
 return format_system(rows)

def authored_solution(M,states,ops,sub=False):
 R,piv,free,vec=solution_vector(M);n=M.cols-1
 def names(cols):return ' and '.join('$'+tex(VARS[i],sub)+'$' for i in cols)
 rows=[]
 for i,S in enumerate(states):rows.append(('M & =' if i==0 else ' & ∼')+matrix_tex(S)+((' & '+operation_tex(ops[i])) if i<len(ops) else ''))
 return ('The augmented matrix for this system is\n\n$$\nM='+matrix_tex(M)+'.\n$$\n\n'
  'Using the standard Gauss-Jordan method, we can reduce this matrix to reduced row echelon form as follows:\n\n$$\n'+r'\begin{aligned}'+r' \\ '.join(rows)+r'\end{aligned}'+'\n$$\n\n'
  'The corresponding system is now\n\n$$\n'+system_tex(R,sub)+'\n$$\n\n'
  'The basic variables are the variables whose coefficients are pivots. In this case, the basic variables are '+names(piv)+', and we have one free variable, '+names(free)+'. That means we need to find '+names(piv)+' in terms of '+names(free)+'.\n\n'
  'Therefore, the general solution is\n\n$$\n'+r'\{\begin{aligned}'+r' \\ '.join(tex(VARS[i],sub)+'='+tex(vec[i],sub) for i in range(n))+r',\end{aligned}'+'\n$$\n\nwhere '+names(free)+' (the free variable) is an arbitrary number.\n\n'
  'In vector form, the solution can be written as\n\n$$\n'+matrix_tex(sp.Matrix(VARS[:n]), augmented=False)+'='+vector_tex(vec,VARS[free[0]],sub)+'.\n$$')

def observed(qid,parameters):
 q=QUESTIONS[qid];B=sp.Matrix(BASE[qid]);n=B.cols-1
 if set(parameters)!= {'scale','offsets'}:raise ValueError('observed parameters require scale and offsets')
 scale=sp.Rational(str(parameters['scale']));offs=[sp.Rational(str(v)) for v in parameters['offsets']]
 if scale==0 or scale.q>2 or len(offs)!=n or abs(scale)>5 or any(abs(d)>10 or d.q>2 for d in offs):raise ValueError('affine source domain')
 M=affine_matrix(B,scale,offs);R,piv,free,vec=solution_vector(M)
 sub='{x}_{' in q[':question/problem'];bmatrix=qid in ('q-32234','q-42040')
 if bmatrix:
  prompt='Consider the system of linear equations\n\n$$\n'+system_tex(M)+'\n$$\nUse the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.'
 else:prompt=compile_math(q[':question/problem'],scale,offs)
 sol=q.get(':question/worked-solution')
 if sol:
  sol=compile_math(sol,scale,offs)
  # This source's one explicit numeric prose assertion belongs to a whole equation slot.
  if qid=='q-32517':sol=sol.replace('${x}_{1}=4$', '$'+tex(VARS[0],True)+'='+tex(vec[0],True)+'$')
 else:
  states,ops=rref_steps(M);sol=authored_solution(M,states,ops)
 bank=[]
 for a in q[':question/answer-fields'][0][':answer-field/choices']:
  vals=parse_vector(a[':answer/value'])
  if vals is None:bank.append(('No solution',None));continue
  changed=[affine_expr(e,i,scale,offs) for i,e in enumerate(vals)]
  normalized=a[':answer/value'].replace('\\\\','\\')
  domain=re.split(r'\\end\{(?:aligned|bmatrix)\}',normalized)[-1]
  if '{x}_{2}' in domain:fv=VARS[1]
  elif '{x}_{3}' in domain:fv=VARS[2]
  else:fv=next(v for v in VARS if re.search(r'\b'+str(v)+r'\s*(?:∈|\\in)',domain))
  bank.append((vector_tex(changed,fv,sub,bmatrix),changed))
 return M,prompt,sol,bank,{'source_id':qid,'authored_solution':not bool(q.get(':question/worked-solution')),'presentation_repair':True,'profile_interpretation':'invertible affine transport; original distractor intent underdetermined'}

# Easy authored peers: same two pivots, three variables, exactly two row additions.
# Moderate: three equations, rank two, one free variable, exactly six operations.
# Hard: three equations, rank three, four variables, exactly nine operations.
def authored(level,p):
 expected={'free_coefficients','constants','mix'}
 if set(p)!=expected:raise ValueError('authored parameters require '+str(expected))
 free=[sp.Rational(str(v)) for v in p['free_coefficients']];constants=[sp.Rational(str(v)) for v in p['constants']];mix=[sp.Rational(str(v)) for v in p['mix']]
 rank=3 if level=='hard' else 2;n=rank+1
 if len(free)!=rank or len(constants)!=rank or len(mix)!={'easy':2,'moderate':4,'hard':6}[level]:raise ValueError('wrong parameter dimensions')
 bound={'easy':5,'moderate':4,'hard':3}[level]
 if any(v==0 or abs(v)>bound or v.q>({'hard':3}.get(level,2)) for v in free) or any(abs(v)>6 or v.q>2 for v in constants):raise ValueError('coefficient/constant bounds')
 if any(v==0 or abs(v)>2 or v.q!=1 for v in mix):raise ValueError('nonzero integer mixing bounds')
 R=sp.eye(rank).row_join(sp.Matrix(free)).row_join(sp.Matrix(constants));rows=[R.row(i) for i in range(rank)]
 if level=='easy':
  a,d=mix;M=sp.Matrix.vstack(rows[0]+d*rows[1],a*(rows[0]+d*rows[1])+rows[1]);ops=[('add',1,0,-a),('add',0,1,-d)]
 elif level=='moderate':
  a,b,c,d=mix;s=rows[0]+d*rows[1];M=sp.Matrix.vstack(2*s,a*s+3*rows[1],b*s+c*rows[1]);ops=[('scale',0,0,sp.Rational(1,2)),('add',1,0,-a),('scale',1,1,sp.Rational(1,3)),('add',2,0,-b),('add',2,1,-c),('add',0,1,-d)]
 else:
  a,b,c,d,e,f=mix;s=rows[0]+d*rows[1]+e*rows[2];t=rows[1]+f*rows[2];M=sp.Matrix.vstack(2*s,a*s+3*t,b*s+c*t+2*rows[2]);ops=[('scale',0,0,sp.Rational(1,2)),('add',1,0,-a),('add',2,0,-b),('scale',1,1,sp.Rational(1,3)),('add',2,1,-c),('scale',2,2,sp.Rational(1,2)),('add',1,2,-f),('add',0,2,-e),('add',0,1,-d)]
 if any(abs(v)>48 for v in M):raise ValueError('printed matrix workload bound 48')
 S=M.copy();states=[S.copy()]
 for kind,i,j,a in ops:
  if kind=='scale':S.row_op(i,lambda v,k:a*v)
  else:S.row_op(i,lambda v,k:v+a*S[j,k])
  states.append(S.copy())
 if S!=M.rref()[0]:raise ValueError('authored operation recipe failed')
 _,piv,freecols,vec=solution_vector(M);fv=VARS[freecols[0]]
 # Complete bank selected in advance: sign of free term, sign of constant,
 # omitting a free contribution, exchanging two basic coordinates, correct.
 variants=[vec.copy() for _ in range(5)]
 variants[0][0]=constants[0]+free[0]*fv
 variants[1][0]=-constants[0]-free[0]*fv
 variants[2][1]=constants[1]
 variants[3][0],variants[3][1]=variants[3][1],variants[3][0]
 bank=[(vector_tex(v,fv),v) for v in variants]
 prompt='Consider the system of linear equations\n\n$$\n'+system_tex(M)+'\n$$\n\nUse the standard Gauss-Jordan method to reduce the augmented matrix $M$ of the system to reduced row echelon form, and then solve the linear system.'
 return M,prompt,authored_solution(M,states,ops),bank,{'authored':True,'operations':len(ops),'authored_bank':'free-term sign, constant sign, omitted free term, coordinate exchange'}

def bank_valid(M,bank):
 _,_,_,sol=solution_vector(M);correct=[];objects=[]
 for i,(_,v) in enumerate(bank):
  if v is None:objects.append('No solution');continue
  # Canonical affine sets compare parametrizations, including wrong parameter names.
  syms=sorted(set().union(*(x.free_symbols for x in v)),key=str)
  if len(syms)!=1:raise ValueError('choice needs one free parameter')
  t=syms[0];direction=sp.Matrix([sp.diff(e,t) for e in v]);point=sp.Matrix([e.subs(t,0) for e in v]);pivot=next((i for i,e in enumerate(direction) if e!=0),None)
  if pivot is None:raise ValueError('constant vector answer')
  direction=direction/direction[pivot];point=point-point[pivot]*direction
  objects.append((tuple(point),tuple(direction)))
  residual=M[:,:-1]*sp.Matrix(v)-M[:,-1]
  if all(sp.expand(e)==0 for e in residual):correct.append(i)
 if len(correct)!=1 or len(set(objects))!=5:raise ValueError('invalid complete bank')
 return correct[0]

@checked_math_content
def generate(level,seed=0,template=None,field_type=None,parameters=None,profile=None):
 if level not in ('easy','moderate','hard'):raise ValueError('difficulty')
 if field_type not in (None,'radio',':answer-field.type/radio'):raise ValueError('only observed radio layout supported')
 rng=random.Random(seed)
 if profile=='authored_operations' and (template in QUESTIONS or template in FAMILIES.values()):raise ValueError('authored profile conflicts with observed template')
 source=profile if profile in QUESTIONS else template if template in QUESTIONS else None
 if source is None and template in FAMILIES.values():source=rng.choice(sorted(q for q,f in FAMILIES.items() if f==template))
 if profile and profile not in QUESTIONS and profile!='authored_operations':raise ValueError('unknown profile')
 if source and level!='easy':raise ValueError('observed/unrated source profiles assigned easy only')
 expected=FAMILIES[source] if source else 'authored_'+level
 if template and template not in (expected,source):raise ValueError('template/profile mismatch')
 for attempt in range(1000):
  if parameters is None:
   if source:p={'scale':rng.choice([-3,-2,-1,1,2,3]),'offsets':[rng.randint(-5,5) for _ in range(len(BASE[source][0])-1)]}
   else:
    rank=3 if level=='hard' else 2;bound={'easy':5,'moderate':4,'hard':3}[level]
    p={'free_coefficients':[rng.choice([i for i in range(-bound,bound+1) if i]) for _ in range(rank)],'constants':[rng.choice([i for i in range(-6,7) if i]) for _ in range(rank)],'mix':[rng.choice([-2,-1,1,2]) for _ in range({'easy':2,'moderate':4,'hard':6}[level])]}
  else:p=parameters
  try:
   M,prompt,sol,bank,extra=observed(source,p) if source else authored(level,p);correct=bank_valid(M,bank);break
  except ValueError:
   if parameters is not None:raise
 else:raise ValueError('could not sample an eligible COMPLETE bank')
 prompt,sol=normalize_prose(prompt),normalize_prose(sol)
 bank=[(normalize_tex(value) if value!='No solution' else value,obj) for value,obj in bank]
 canonical=[row for row in serialize(M.rref()[0]) if any(sp.Rational(v)!=0 for v in row)];mathfp=fingerprint({'rref':canonical,'n':M.cols-1})
 content=fingerprint({'version':VERSION,'prompt':prompt,'solution':sol,'bank':sorted(v for v,_ in bank),'profile':source or 'authored_operations','level':level})
 fid=uid(content+':field:selection');answers=[];correctid=None
 for i,(value,_) in enumerate(bank):
  aid=uid(fid+':answer:'+value);answers.append({':answer/id':aid,':answer/type':':answer.type/text' if value=='No solution' else ':answer.type/math',':answer/value':value})
  if i==correct:correctid=aid
 rng.shuffle(answers)
 field={':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correctid]}
 return {'knowledge_point':{'db_id':KP,'id':RECORD[':knowledge-point/id'],'title':RECORD[':knowledge-point/title']},'question':{':question/id':uid(content),':question/difficulty':':question.difficulty/'+level,':question/problem':prompt,':question/worked-solution':sol,':question/answer-fields':[field]},'generation':{'generator_version':VERSION,'seed':seed,'template':expected,'bank_profile':source or 'authored_operations','parameters':p,'mathematical_fingerprint':mathfp,'content_fingerprint':content,'matrix':serialize(M),'source_basis':RAW['basis'],'source_lineage':RAW['lineage'],'sympy_version':sp.__version__,'plots':'none',**extra}}

def generate_easy(seed=0,**kw):return generate('easy',seed,**kw)
def generate_moderate(seed=0,**kw):return generate('moderate',seed,**kw)
def generate_hard(seed=0,**kw):return generate('hard',seed,**kw)

def markdown(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 return q[':question/problem']+'\n\n'+'\n'.join('- '+('$'+a[':answer/value']+'$' if a[':answer/type'].endswith('/math') else a[':answer/value']) for a in f[':answer-field/choices'])+'\n\n'+q[':question/worked-solution']
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--difficulty',choices=['easy','moderate','hard','all'],default='all');parser.add_argument('--seed',type=int,default=0);parser.add_argument('--count',type=int,default=1);parser.add_argument('--format',choices=['markdown','json'],default='markdown');parser.add_argument('--template');parser.add_argument('--profile');args=parser.parse_args()
 result=[generate(level,args.seed+i,template=args.template,profile=args.profile) for level in (['easy','moderate','hard'] if args.difficulty=='all' else [args.difficulty]) for i in range(args.count)]
 print(json.dumps(result,indent=2) if args.format=='json' else '\n\n---\n\n'.join(markdown(r) for r in result))
