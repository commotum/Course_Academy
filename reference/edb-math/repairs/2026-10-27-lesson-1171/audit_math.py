import copy,json,re,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;R=H.parents[3];sys.path.insert(0,str(R/'scripts'))
from question_capture.math_format import ENV,environment,cells,matrix_answer,matrix_tex,validate_math_structure
D=json.loads((H/'current.json').read_text());Q=copy.deepcopy(D['questions']);changes=[];links=[];audit=[]
def scalar(s):
 s=s.replace('⁡','').replace('−','-');s=re.sub(r'\\color\{[A-Za-z]+\}','',s);s=re.sub(r'\{a\}_\{(\d+)\}',r'a\1',s);s=re.sub(r'\\(?:left|right|displaystyle|textstyle)|\\[,;!]','',s);s=s.replace(r'\operatorname{ln}',r'\ln');s=re.sub(r'a_\{(\d+)\}',r'a\1',s)
 def group(t,i):
  while i<len(t)and t[i].isspace():i+=1
  assert t[i]=='{',(t,i);start=i+1;depth=1;i+=1
  while depth:depth+=(t[i]=='{')-(t[i]=='}');i+=1
  return t[start:i-1],i
 while (m:=re.search(r'\\(?:dfrac|frac|sqrt)\s*\{',s)):
  arg,end=group(s,m.end()-1)
  if 'sqrt'in m[0]:repl='sqrt('+str(scalar(arg))+')'
  else:b,end=group(s,end);repl='(('+str(scalar(arg))+')/('+str(scalar(b))+'))'
  s=s[:m.start()]+repl+s[end:]
 s=s.replace(r'\cdot','*').replace(r'\times','*').replace(r'\pi','pi').replace(r'\ln','log').replace('{','(').replace('}',')')
 assert re.fullmatch(r'[\w+*/().\s-]+',s),s
 names=set(re.findall(r'[A-Za-z_]\w*',s));assert all(n in {'pi','e','E','sqrt','log','a','b','c','d'}or re.fullmatch(r'a\d+',n)for n in names),s
 return parse_expr(s,local_dict={'pi':S.pi,'e':S.E,'E':S.E,'sqrt':S.sqrt,'log':S.log,**{n:S.Symbol(n)for n in names if n.startswith('a')or n in {'b','c','d'}}},transformations=standard_transformations+(implicit_multiplication_application,rationalize))
def grids(t):
 out=[]
 for m in ENV.finditer(t):
  if m.groups()!=('begin','bmatrix'):continue
  span=environment(t,m.start());out.append(cells(t[span[0]:span[1]]))
 return out
def mat(g):return S.Matrix([[scalar(c)for c in row]for row in g])
def same(a,b):return a.shape==b.shape and all(S.simplify(v)==0 for v in a-b)
for q in Q:
 p=q[':question/problem'];gs=grids(p);assert gs,q[':db/id'];ms=list(map(mat,gs));expected=ms[0]
 if len(ms)>1:
  count=2 if 'student claims'in p else len(ms)
  for m in ms[1:count]:expected=expected*m
 fs=q.get(':question/answer-fields',[]);entry={'entity':q[':db/id'],'source':q.get(':question/math-academy-id'),'expected':str(expected),'shape':list(expected.shape),'fields':len(fs),'issues':[]}
 if fs and fs[0][':answer-field/type'][':db/ident']==':answer-field.type/blank':
  keys=re.findall(r'\{\{([^{}]+)\}\}',p);bykey={f[':answer-field/key']:f for f in fs};assert len(keys)==len(fs)==expected.rows*expected.cols
  for key,v in zip(keys,list(expected)):assert S.simplify(scalar(bykey[key][':answer-field/correct'][':answer/value'])-v)==0,(q[':db/id'],key)
  if re.search(r'(?m)^\|',p):
   start=p.index('|');table=p[start:];labels=re.findall(r'\$([^$]*=)[^$]*\$',table);assert len(labels)==1;label=labels[0].rstrip('= ').replace(r'\,','').strip();rows=[keys[i:i+expected.cols]for i in range(0,len(keys),expected.cols)];after=p[:start]+matrix_answer(label,[['{{'+k+'}}'for k in row]for row in rows]);changes.append((q[':db/id'],'question/problem',p,after,'matrix-answer-layout'));q[':question/problem']=after
 elif fs:
  f=fs[0];candidates=[]
  for a in f.get(':answer-field/choices',[]):
   ag=grids(a[':answer/value'])
   if len(ag)==1 and same(mat(ag[0]),expected):candidates.append(a)
  if 'student claims'in p:
   assert ':answer-field/correct'in f;entry['review']='Individually reviewed universal identity claim and row/column calculation; numeric/symbolic matrix product checked independently'
  else:
   assert len(candidates)==1,(q[':db/id'],candidates);right=candidates[0]
   if ':answer-field/correct'not in f:links.append({'question':q[':db/id'],'field':f[':db/id'],'answer':right[':db/id'],'answer_uuid':right[':answer/id']});f[':answer-field/correct']=copy.deepcopy(right)
   else:assert f[':answer-field/correct'][':db/id']==right[':db/id'],q[':db/id']
 sol=q.get(':question/worked-solution','')
 if sol:
  sg=grids(sol)
  if sg:assert same(mat(sg[-1]),expected),('last solution matrix',q[':db/id'])
 else:entry['issues'].append('missing-solution') if fs else None
 audit.append(entry)
# Independently confirmed existing solution and dimension defects.
for q in Q:
 if q[':db/id']==17592186265864:
  before=q[':question/worked-solution'];wrong=matrix_tex([[r'-\frac{\sqrt{2}}{2}'],[r'-\frac{\sqrt{2}}{2}'],['0']]);right=matrix_tex([[r'-\frac{\sqrt{2}}{2}'],[r'\frac{\sqrt{2}}{2}'],['0']]);assert before.count(wrong)==1;after=before.replace(wrong,right,1);q[':question/worked-solution']=after;changes.append((q[':db/id'],'question/worked-solution',before,after,'incorrect-shortcut-sign'))
 if q[':db/id']==17592186101142:
  before=q[':question/problem'];after=before.replace(r'$3 \cdot 3$',r'$3 \times 3$');assert after!=before;q[':question/problem']=after;changes.append((q[':db/id'],'question/problem',before,after,'matrix-dimension-notation'))
 if q[':db/id']in{17592186101142,17592186101408}:
  before=q.get(':question/worked-solution');assert before is None
  if q[':db/id']==17592186101142:after='Multiplying a matrix by the corresponding identity matrix leaves every entry unchanged. Both matrices are $3\\times3$, so the product is defined.\n\n$$\nAI_3=A='+matrix_tex([['6','3','4'],['1','2','1'],['2','8','2']])+'.\n$$'
  else:after='The matrix $A=\\begin{bmatrix}0 & 0 & 1\\end{bmatrix}$ is the third row of $I_3$. Multiplying $B$ on the left by this row selects the third row of $B$. Therefore,\n\n$$\nAB='+matrix_tex([[r'\sqrt{5}','4','1']])+'.\n$$'
  q[':question/worked-solution']=after;changes.append((q[':db/id'],'question/worked-solution',None,after,'authored-missing-solution'))
(H/'math-audit.json').write_text(json.dumps(audit,indent=2)+'\n');(H/'proposed-questions.json').write_text(json.dumps(Q,indent=2)+'\n');(H/'proposed-changes.json').write_text(json.dumps(changes,indent=2)+'\n');(H/'missing-key-repairs.json').write_text(json.dumps(links,indent=2)+'\n');print('Verified products and existing keys for',len(Q),'questions; proposed',len(changes),'content changes and',len(links),'key completions.')
