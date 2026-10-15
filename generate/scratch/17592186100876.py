#!/usr/bin/env python3
"""Basis-vector matrix selection. Deterministic, local previews; no writes."""
import argparse, copy, hashlib, json, random, re, sys, uuid
from pathlib import Path
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts/question_capture'))
from math_format import checked_math_content, normalize_prose, normalize_tex, matrix_tex
ID=17592186100876;VERSION='basis-vector-1';HERE=Path(__file__).with_suffix('')
SOURCE=json.loads((HERE/'source.json').read_text());KP=SOURCE['record'];QS={q[':question/math-academy-id']:q for q in KP[':knowledge-point/questions']}
SUPPORTED=('easy','moderate');EXCLUDED=('q-41950',)
MATRIX=re.compile(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',re.S)
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,default=str).encode()).hexdigest()
def uid(x):return str(uuid.uuid5(uuid.UUID(KP[':knowledge-point/id']),digest(x)))
def scalar(t):
 t=normalize_tex(t).replace('\u2061','').replace(' ','').replace(r'\operatorname{ln}',r'\ln')
 # Restricted exact parser for the observed real scalar grammar, not eval.
 sign=-1 if t.startswith('-') else 1;t=t.lstrip('+-')
 if t.startswith(r'\frac'):
  m=re.fullmatch(r'\\frac\{(.+)\}\{([^{}]+)\}',t);assert m,t
  return sign*scalar(m[1])/scalar(m[2])
 m=re.fullmatch(r'(\d*)\\sqrt\{(\d+)\}',t)
 if m:return sign*s.Integer(m[1] or 1)*s.sqrt(int(m[2]))
 m=re.fullmatch(r'\\ln\((\d+)\)',t)
 if m:return sign*s.log(int(m[1]))
 if t in (r'\pi','e'):return sign*(s.pi if t==r'\pi' else s.E)
 return sign*s.Rational(t)
def raw_matrices(text):return [[[x.strip() for x in row.split('&')] for row in m[1].split(r'\\')] for m in MATRIX.finditer(text)]
def matrix(text):return s.Matrix([[scalar(x) for x in row] for row in raw_matrices(text)[0]])
def tex(rows):return matrix_tex(rows,augmented=False)
def spec(k):
 q=QS[k];a,b=raw_matrices(q[':question/problem']);column=len(a)>1
 m=a if column else b;v=b if column else a;j=next(i for i,x in enumerate(sum(v,[])) if scalar(x)==1)
 return m,column,j
def task(q):
 a,b=[s.Matrix([[scalar(x) for x in row] for row in m]) for m in raw_matrices(q[':question/problem'])[:2]]
 column=b.cols==1;m=a if column else b;v=b if column else a;j=list(v).index(1)
 return digest([m.rows,m.cols,list(m),'column' if column else 'row',j])
def ordn(j):return f'${j+1}$'+('st','nd','rd','th')[j]
def vector(n,j,column):return [[str(int(i==j))] for i in range(n)] if column else [[str(int(i==j)) for i in range(n)]]
def result(m,j,column):return [[row[j]] for row in m] if column else [m[j][:]]
def expanded(m,j):
 return [['+'.join(('('+x+')' if x.startswith('-') else x)+r'\cdot '+str(int(c==j)) for c,x in enumerate(row))] for row in m]
def bank(k,m,j):
 n=len(m);original_j=spec(k)[2];delta=(j-original_j)%n
 def R(i):return [m[(i+delta)%n][:]]
 def C(i):return [[row[(i+delta)%n]] for row in m]
 if k=='q-41949':return [R(1),C(2),C(1),C(0),R(0)]
 if k=='q-41943':return [C(2),C(1),[sum(C(1),[])],C(0),[sum(C(0),[])]]
 if k=='q-41944':return [R(2),C(0),C(1),R(0),R(1)]
 if k=='q-41979':return [C(1),R(0),C(0),R(2),R(1)]
 if k=='q-41977':
  altered=R(0);rad=int(re.search(r'\\sqrt\{(\d+)\}',m[0][2])[1]);assert rad>4
  altered[0][2]='-'+s.latex(s.sqrt(rad-4))
  return [C(1),altered,R(1),C(2),R(2)]
 if k=='q-41950':return [C(0),R(0),C(2),R(2),R(1)]
 if k=='q-130247':
  assert j==1
  a=m[0][0];d=int(re.search(r'\\frac\{.*\}\{(\d+)\}',a)[1]);t=s.latex(s.Rational(1,d))
  return [result(m,j,True),C(2),[['-'+a],[t],['0']],R(1),[['-'+t],[t],['0']]]
 return None
def sample_scalar(t,rng):
 if scalar(t)==0:return '0'
 negative=t.startswith('-');sign='-' if negative else '';u=t.lstrip('-')
 if r'\sqrt' in u:
  rad=rng.choice([2,3,5,6,7,10,11,13,17,19]);coef=rng.randint(1,4)
  return sign+('' if coef==1 else str(coef))+rf'\sqrt{{{rad}}}'
 if r'\frac' in u:
  if r'\pi' in u:return sign+rf'\frac{{\pi}}{{{rng.randint(2,7)}}}'
  if 'e' in u:return sign+rf'\frac{{e}}{{{rng.randint(2,7)}}}'
  return sign+rf'\frac{{{rng.randint(1,5)}}}{{{rng.randint(2,7)}}}'
 if 'ln' in u:return sign+rf'\operatorname{{ln}}({rng.randint(2,9)})'
 if '.' in u:return sign+str(rng.randint(11,49)/10)
 return sign+str(rng.randint(1,14 if len(u)>1 else 9))
@checked_math_content
def generate(level='easy',seed=0,template=None,parameters=None,replay=False):
 if level not in SUPPORTED:raise ValueError('unsupported band '+level)
 rng=random.Random(seed);k=template or rng.choice([k for k,q in QS.items() if q.get(':question/difficulty',{}).get(':db/ident','').endswith('/'+level)])
 if k in EXCLUDED and not replay:raise ValueError('unrated incomplete source')
 old=QS[k];original,column,oj=spec(k);n=len(original)
 if k not in EXCLUDED:assert old[':question/difficulty'][':db/ident'].endswith('/'+level)
 if parameters is not None:m=copy.deepcopy(parameters['matrix']);j=parameters['target']
 elif replay:m=copy.deepcopy(original);j=oj
 else:
  m=[[sample_scalar(x,rng) for x in row] for row in original];j=rng.randrange(n)
  if k=='q-130247':
   d=rng.choice([2,3,5,7]);a=rf'\frac{{\sqrt{{{d}}}}}{{{d}}}';m=[[a,'-'+a,'0'],[a,a,'0'],['0','0','1']];j=1
  if k=='q-41977':
   # Source profile's altered radical retains radicand-minus-four; keep its radicand anchor in cell (1,3).
   row=0;m[row][2]='-'+rf'\sqrt{{{rng.choice([7,10,11,13,17,19])}}}'
 assert 0<=j<n and len(m)==n and all(len(row)==n for row in m)
 if k=='q-130247':assert j==1
 m=[[x.replace('\u2061','') for x in row] for row in m]
 v=vector(n,j,column);out=result(m,j,column);choices=bank(k,m,j)
 if choices is not None:
  objects=[s.Matrix([[scalar(x) for x in row] for row in c]) for c in choices]
  assert len(set(map(str,objects)))==5,'choice collision'
  assert sum(o==s.Matrix([[scalar(x) for x in row] for row in out]) for o in objects)==1
 a,b=(m,v) if column else (v,m);it=iter([tex(a),tex(b)])
 prompt=MATRIX.sub(lambda _:next(it),old[':question/problem'],count=2)
 solution=old.get(':question/worked-solution')
 if solution:
  solution=re.sub(r'\$[1-4]\$(?:st|nd|rd|th)',lambda _:ordn(j),solution)
  replacements=[tex(out),tex(m),tex(v),tex(expanded(m,j)),tex(out)] if column else [tex(out),tex(v),tex(m),tex(out)]
  assert len(MATRIX.findall(solution))==len(replacements)
  it=iter(replacements);solution=MATRIX.sub(lambda _:next(it),solution)
 else:solution='The basis row selects the corresponding row. Therefore, $AB='+tex(out)+'$.'
 q={':question/problem':normalize_prose(prompt),':question/worked-solution':normalize_prose(solution),':question/difficulty':':question.difficulty/'+level}
 fp=task(q);qid=uid([VERSION,k,fp]);q[':question/id']=qid;fields=[]
 if choices is not None:
  fid=uid([qid,'selection']);answers=[{':answer/id':uid([fid,normalize_tex(tex(c))]),':answer/type':':answer.type/math',':answer/value':normalize_tex(tex(c))} for c in choices]
  correct=next(a for a,c in zip(answers,choices) if s.Matrix([[scalar(x) for x in row] for row in c])==s.Matrix([[scalar(x) for x in row] for row in out]))
  fields=[{':answer-field/id':fid,':answer-field/key':'selection',':answer-field/type':':answer-field.type/radio',':answer-field/choices':answers,':answer-field/correct':[':answer/id',correct[':answer/id']]}]
 else:
  for i,x in enumerate(sum(out,[])):
   key='field-'+str(i+1);fid=uid([qid,key]);value=normalize_tex(x);answer={':answer/id':uid([fid,value]),':answer/type':':answer.type/math',':answer/value':value}
   fields.append({':answer-field/id':fid,':answer-field/key':key,':answer-field/type':':answer-field.type/blank',':answer-field/choices':[answer],':answer-field/correct':[':answer/id',answer[':answer/id']]})
 q[':question/answer-fields']=fields
 return {'knowledge_point':{'db_id':ID,'title':KP[':knowledge-point/title']},'question':q,'generation':{'version':VERSION,'template':k,'profile':k if choices is not None else None,'seed':seed,'parameters':{'matrix':m,'target':j},'source_question':k,'source_basis':SOURCE['basis'],'lineage':SOURCE['lineage'],'sympy':s.__version__,'eligible_for_learning':k not in EXCLUDED,'task_fingerprint':fp,'domain':'exact real entries, square source dimensions, one basis row or column'}}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--difficulty',default='easy');p.add_argument('--seed',type=int,default=0);p.add_argument('--template');p.add_argument('--count',type=int);p.add_argument('--output',type=Path);p.add_argument('--format',choices=('json','markdown'),default='json');a=p.parse_args()
 seen={task(q) for q in QS.values()};records=[]
 for i in range(1000):
  if len(records)>=(a.count if a.count is not None else 1):break
  try:r=generate(a.difficulty,a.seed+i,a.template)
  except AssertionError as e:
   if str(e)=='choice collision':continue
   raise
  fp=task(r['question'])
  if fp not in seen:records.append(r);seen.add(fp)
 if len(records)!=(a.count if a.count is not None else 1):raise ValueError('bounded variant limit')
 obj=records if a.count is not None else records[0];text=json.dumps(obj,indent=2) if a.format=='json' else '\n\n---\n\n'.join(r['question'][':question/problem']+'\n\n'+r['question'][':question/worked-solution']+'\n\n'+json.dumps(r['question'][':question/answer-fields'],indent=2) for r in records)
 a.output.write_text(text+'\n') if a.output else print(text)
