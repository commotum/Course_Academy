"""Source-backed distributive-law matrix templates; exact SymPy arithmetic.
Easy/moderate only. Source profiles remain separate. No plot generation: the
canonical SVG is mathematical notation, and practice matrices are native LaTeX.
"""
import argparse, hashlib, json, random, re, uuid
from pathlib import Path
try:
 import sympy as s
except ModuleNotFoundError:
 import os,sys
 interpreter=Path(__file__).resolve().parents[2]/'.venv/bin/python'
 os.execv(str(interpreter),[str(interpreter),str(Path(__file__).resolve()),*sys.argv[1:]])
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
KP_ID=17592186115226
KP_UUID='a7ad52ce-d408-5390-b91f-c855274f39ea'
GENERATOR_UUID=str(uuid.uuid5(uuid.UUID(KP_UUID),'distributive-matrix-generator-v1'))
HERE=Path(__file__).with_suffix('')
SOURCES={q[':question/math-academy-id']:q for q in json.loads((HERE/'source.json').read_text())['record'][':knowledge-point/questions']}
SUPPORTED_LEVELS=('easy','moderate')
RX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def scalar(t):
 t=re.sub(r'\{t\}_\{(\d+)\}',r't_\1',t)
 t=re.sub(r'\\text\{.*?\}','',t).strip()
 t=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 t=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',t)
 return s.simplify(parse_expr(t,transformations=standard_transformations+(implicit_multiplication_application,)))
def matrices(text):return [s.Matrix([[scalar(v) for v in row.split('&')] for row in m[1].split(r'\\')]) for m in RX.finditer(text)]
def tex(M):return r'\begin{bmatrix}'+' \\\\ '.join(' & '.join(s.latex(v) for v in row) for row in s.Matrix(M).tolist())+r'\end{bmatrix}'
def expression(q):return re.search(r'\$([ABC]{2}[+-][ABC]{2})\$',q[':question/problem'].replace(' ',''))[1]
def evaluate(expr,env):
 a,sign,b=re.fullmatch(r'([ABC]{2})([+-])([ABC]{2})',expr).groups()
 return env[a[0]]*env[a[1]]+(1 if sign=='+' else -1)*env[b[0]]*env[b[1]]
def signature(q):
 m=matrices(q[':question/problem']);return hashlib.sha256(json.dumps([expression(q) if 'X+Y' not in q[':question/problem'] else 'XZ+YZ',[[str(v) for v in a] for a in m[:(2 if 'X+Y' in q[':question/problem'] else 3)]]]).encode()).hexdigest()
def source_data(profile):
 q=SOURCES[profile];M=matrices(q[':question/problem'])
 if profile=='q-138783':return M[:2]
 return M[:3]
def bank(profile,M):
 A,B,C=M;Z=s.zeros(3);I=s.eye(3);J=I[:,::-1]
 if profile=='q-42263':return [B,-B,Z,-2*B,-I]
 if profile=='q-130269':return [s.Matrix([[B[1,2],B[0,1],B[0,2]],list(B.row(0)),list(B.row(2))]),B,J,I,Z]
 if profile=='q-75635':
  V=C.copy();V[1,1]=4
  return [-2*C,2*C,Z,V,4*C]
 if profile=='q-130259':
  U=Z.copy();U[1,0]=C[0,1];U[1,1]=C[1,1];V=Z.copy();V[0,1]=C[0,1];V[1,1]=C[1,1];W=Z.copy();W[1,:]=C.row(0)
  L=Z.copy();L[1,:]=C.row(1)
  return [U,Z,V,W,L]
 if profile=='q-130275':
  U=B.copy()
  for i in range(3):U[i,i]*=5
  V=s.Matrix([[B[0,0],5*B[0,1],5*B[0,2]],[B[1,0],B[1,1],5*B[1,0]],[5*B[2,0],B[2,1],B[2,2]]])
  return [5*J,U,V,5*B,-5*I]
 if profile=='q-75612':return [3*C,Z,s.diag(*[3*C[i,i] for i in range(3)]),-C,C]
 raise ValueError(profile)
def category(v):return 'zero' if v==0 else 'radical' if v.has(s.Pow) and not v.is_Rational else 'rational'
def targets(q,result):
 rows=[line for line in q[':question/problem'].splitlines() if line.startswith('|') and '---' not in line]
 out={}
 for i,line in enumerate(rows):
  cells=line.split('|')[3:6]
  for j,cell in enumerate(cells):
   z=re.search(r'\{\{(field-\d+)\}\}',cell)
   if z:out[z[1]]=[i,j]
 return out

def generate(difficulty='easy',seed=0,template=None,parameters=None,bank_profile=None):
 if difficulty not in SUPPORTED_LEVELS:raise ValueError('Unsupported difficulty '+difficulty)
 rng=random.Random(seed);profiles=[k for k,q in SOURCES.items() if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+difficulty]
 profile=bank_profile or template or rng.choice(profiles)
 if profile not in profiles:raise ValueError('Unrated or wrong-level source')
 q=SOURCES[profile];base=source_data(profile);M=[a.copy() for a in base]
 if parameters is not None:M=[s.Matrix([[scalar(v) for v in row] for row in a]) for a in parameters['matrices']]
 else:
  # Vary the supplied common matrix, preserving zero structure and number forms.
  # Sparse AB+AC instead varies the active row of B+C, retaining its E21 map.
  if profile=='q-138783':index=1
  elif profile=='q-319890':index=2
  else:
   expr0=expression(q);left,right=expr0[:2],expr0[3:];index='ABC'.index(left[0] if left[0]==right[0] else left[1])
  for i,v in enumerate(M[index]):
   if v!=0:M[index][i]=s.expand(v*rng.choice([-3,-2,-1,1,2,3]))
  if profile=='q-319890':
   M[2][0,1]=rng.choice([s.sqrt(2),s.sqrt(3),s.sqrt(5),s.sqrt(7)])-M[1][0,1]
 if profile=='q-138783':
  result=M[0]*M[1];original=base[0]*base[1];expr='XZ+YZ';fact='(X+Y)Z';D=M[0];common=M[1];oldD=base[0]
 else:
  expr=expression(q);result=evaluate(expr,dict(zip('ABC',M)));original=evaluate(expr,dict(zip('ABC',base)))
  a,sign,b=re.fullmatch(r'([ABC]{2})([+-])([ABC]{2})',expr).groups();env=dict(zip('ABC',M));oldenv=dict(zip('ABC',base));sg=1 if sign=='+' else -1
  if a[1]==b[1]:D=env[a[0]]+sg*env[b[0]];oldD=oldenv[a[0]]+sg*oldenv[b[0]];common=env[a[1]];fact='('+a[0]+sign+b[0]+')'+a[1]
  else:D=env[a[1]]+sg*env[b[1]];oldD=oldenv[a[1]]+sg*oldenv[b[1]];common=env[a[0]];fact=a[0]+'('+a[1]+sign+b[1]+')'
 # Retain source prose and ordered solution stages; every matrix is dependent data.
 replacements=list(zip(base,M))+[(oldD,D),(original,result)]
 def replace(match):
  V=matrices(match[0])[0]
  for old,new in replacements:
   if V==old:return tex(new)
  raise ValueError('Unmapped solution matrix '+profile+' '+str(V))
 solution=RX.sub(replace,q[':question/worked-solution'])
 # Replace by occurrence to distinguish equal source matrices.
 n=[0]
 def pm(m):
  i=n[0];n[0]+=1
  return tex(M[i]) if i<len(M) else m[0]
 problem=RX.sub(pm,q[':question/problem'])
 fields=q[':question/answer-fields'];isradio=len(fields)==1 and fields[0][':answer-field/type'][':db/ident']==':answer-field.type/radio'
 selected={}
 if not isradio:
  if profile=='q-138783':selected={'field-'+str(i+1):list(divmod(i,2)) for i in range(4)}
  else:
   selected=targets(q,original);assert len(selected)==len(fields)
   if parameters is not None:selected=parameters['targets']
   else:
    taken=set()
    for key,(i,j) in sorted(selected.items()):
     candidates=[(r,c) for r in range(3) for c in range(3) if category(result[r,c])==category(original[i,j]) and (r,c) not in taken]
     if not candidates:raise ValueError('Target roles unavailable')
     pos=rng.choice(candidates);selected[key]=list(pos);taken.add(pos)
   inverse={tuple(pos):key for key,pos in selected.items()}
   table=[]
   for i in range(3):
    cells=['{{'+inverse[i,j]+'}}' if (i,j) in inverse else '$'+s.latex(result[i,j])+'$' for j in range(3)]
    table.append('| '+('$'+expr+r'=\,\,$' if i==1 else '')+' |  | '+' | '.join(cells)+' |  |')
    if i==0:table.append('| --- | --- | --- | --- | --- | --- |')
   problem=problem.split('\n|')[0]+'\n\n'+'\n'.join(table)
  if profile=='q-138783':problem=re.sub(r'\n[ \t]+','\n',problem)
 fp=signature({':question/problem':problem});qid=str(uuid.uuid5(uuid.UUID(GENERATOR_UUID),fp+json.dumps(selected,sort_keys=True)+profile))
 out=[]
 for sourcefield in sorted(fields,key=lambda f:f[':answer-field/key']):
  key=sourcefield[':answer-field/key'];fid=str(uuid.uuid5(uuid.UUID(qid),key))
  values=bank(profile,M) if isradio else [result[tuple(selected[key])]]
  if isradio:
   assert len({tuple(v) for v in values})==5 and values.count(result)==1,'Colliding bank'
  answers=[{':answer/id':str(uuid.uuid5(uuid.UUID(fid),str(v))),':answer/type':':answer.type/math',':answer/value':tex(v) if isradio else s.latex(v)} for v in values]
  correct=values.index(result) if isradio else 0
  out.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/radio' if isradio else ':answer-field.type/blank',':answer-field/choices':answers,':answer-field/correct':[':answer/id',answers[correct][':answer/id']]})
 return {'knowledge_point':{'db_id':KP_ID,'id':KP_UUID,'title':'Calculating a Matrix Product Using the Distributive Law'},'question':{':question/id':qid,':question/problem':problem,':question/worked-solution':solution,':question/difficulty':':question.difficulty/'+difficulty,':question/answer-fields':out},'generation':{'version':1,'seed':seed,'template':profile,'bank_profile':profile if isradio else None,'parameters':{'matrices':[[[str(v) for v in row] for row in a.tolist()] for a in M],'targets':selected},'parameter_fingerprint':fp,'generator_id':GENERATOR_UUID,'sympy_version':s.__version__}}
def batch(difficulty,count,seed):
 profiles=[k for k,q in SOURCES.items() if q.get(':question/difficulty',{}).get(':db/ident')==':question.difficulty/'+difficulty];out=[]
 for i in range(count):
  for retry in range(100):
   try:r=generate(difficulty,seed+i+retry*1000,bank_profile=profiles[i%len(profiles)]);break
   except (AssertionError,ValueError):continue
  else:raise ValueError('Bounded sampling exhausted')
  out.append(r)
 return out
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--count',type=int,default=5);p.add_argument('--seed',type=int,default=0);p.add_argument('--format',choices=['json','markdown'],default='json');a=p.parse_args();rows=batch(a.difficulty,a.count,a.seed);print(json.dumps(rows,indent=2) if a.format=='json' else '\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution'] for r in rows))
