import json,re,sys,subprocess,hashlib
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
R=Path('/home/jake/Developer/Course_Academy');sys.path.insert(0,str(R));from scripts.generator_publish import normalized_question
H=Path(__file__).resolve().parent;ROOT=Path('/media/jake/SSD/EDB/math');SEEDS=[17,83,291];X=S.symbols('x y z');TRANS=standard_transformations+(implicit_multiplication_application,)
def clean(t):
 t=re.sub(r'\\(?:d?frac)\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',t)
 t=re.sub(r'\{?\\color\{[^{}]*\}([^{}]*)\}?',r'\1',t)
 for cmd in ['\\left','\\right','\\quad','\\qquad','\\,','\\cdot','$']:t=t.replace(cmd,'')
 return t.replace('{','').replace('}','').replace('−','-').strip().rstrip('.')
def num(t):return S.sympify(clean(t))
def matrices(t):
 return [S.Matrix([[num(v)for v in row.split('&')]for row in s.split('\\\\')])for s in re.findall(r'\\begin\{array\}\{[^}]*\}(.*?)\\end\{array\}',t,re.S)]
def given(q):
 ms=matrices(q[':question/problem'])
 if ms:return ms[0]
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/problem'],re.S).group(1);out=[]
 for eq in block.split('\\\\'):
  a,b=eq.replace('&','').split('=');a=parse_expr(clean(a),local_dict=dict(zip('xyz',X)),transformations=TRANS);out.append([a.coeff(x)for x in X]+[num(b)])
 return S.Matrix(out)
def tuplevalue(t):
 if '='in t:
  vs=[]
  for name in 'xyz':
   m=re.search(name+r'\s*=\s*(.*?)(?=,|\$|\\quad|\\qquad|$)',t);vs.append(num(m.group(1)))
  return tuple(vs)
 t=t.replace(r'\left(', '').replace(r'\right)', '').replace(r'\langle','').replace(r'\rangle','').strip('⟨⟩ ');return tuple(num(v)for v in t.split(','))
def ref(m):
 pivots=[]
 for i in range(m.rows):
  p=next((j for j in range(m.cols)if m[i,j]!=0),m.cols);pivots.append(p)
 return all(a<b or a==m.cols==b for a,b in zip(pivots,pivots[1:]))
def standard(m):
 m=m.copy();swap=False;states=[]
 for j in range(3):
  if m[j,j]==0:
   k=next(k for k in range(j+1,3)if m[k,j]!=0);m.row_swap(j,k);swap=True
  if m[j,j]!=1:
   pivot=m[j,j];m.row_op(j,lambda v,k:v/pivot);states.append(m.copy())
  for i in range(j+1,3):
   coef=m[i,j]
   if coef:m.row_op(i,lambda v,k:v-coef*m[j,k]);states.append(m.copy())
 return m,swap,states
def audit(q,tag):
 M=given(q);U,swap,states=standard(M);assert M.shape==(3,4) and M[:,:3].det()!=0
 actual=tuple(M[:,:3].inv()*M[:,3]);f=q[':question/answer-fields'][0];key=f[':answer-field/correct'];key=key[':answer/id']if isinstance(key,dict)else key[1]if isinstance(key,list)else key
 valid=[];exact=[];bad=[];answers=[]
 for a in f[':answer-field/choices']:
  v=a[':answer/value'];ms=matrices(v)
  ok=bool(ms and ref(ms[0]) and ms[0].rref()[0]==M.rref()[0])if ms else tuplevalue(v)==actual
  ex=bool(ms and ms[0]==U)if ms else ok
  if ok:valid.append(a[':answer/id'])
  if ex:exact.append(a[':answer/id'])
  answers.append(str(ms[0])if ms else str(tuplevalue(v)))
 if key not in valid:bad.append('wrong_or_missing_key')
 if len(valid)!=1:bad.append('ambiguous_or_no_valid_option')
 if len(set(answers))!=len(answers):bad.append('equivalent_duplicate_choices')
 for i,m in enumerate(matrices(q.get(':question/worked-solution',''))):
  if m.shape!=(3,4)or m.rref()[0]!=M.rref()[0]:bad.append(f'wrong_solution_matrix_{i}')
 prompt=q[':question/problem'];hints=bool(re.search(r'R_[123].*:?=|pivot.*zero|exchange.*R_|Using.*R_',prompt,re.I))
 if hints:bad.append('supplied_operation_or_pivot')
 return {'id':tag,'source_id':q.get(':question/math-academy-id'),'difficulty':q.get(':question/difficulty'),'input':'matrix'if matrices(prompt)else'equations','endpoint':'echelon'if matrices(f[':answer-field/choices'][0][':answer/value'])else'solve','swap':swap,'correct_key':key,'valid_options':valid,'exact_standard_options':exact,'solution_matrices_checked':len(matrices(q.get(':question/worked-solution',''))),'issues':bad}
summary={};allissues=[]
for kp in [17592186096672,17592186096673]:
 d=H/str(kp);source=json.loads((d/'source/source.json').read_text());script=ROOT/source['registered_generator'][':question-generator/script'];stored=json.loads((d/'kp.json').read_text())[':knowledge-point/questions'];rows=[]
 for q in stored:
  try:row=audit(q,q[':db/id'])
  except Exception as e:row={'id':q[':db/id'],'source_id':q.get(':question/math-academy-id'),'issues':['parser_or_math_error:'+repr(e)]}
  rows.append(row)
 (d/'stored-audit.json').write_text(json.dumps(rows,indent=2)+'\n');samp=[];records=[]
 for band in ['easy','moderate','hard']:
  for seed in SEEDS:
   out=json.loads(subprocess.check_output([sys.executable,str(script),'--difficulty',band,'--count','12','--seed',str(seed),'--format','json'],env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'}));(d/f'{band}-{seed}.json').write_text(json.dumps(out,indent=2)+'\n')
   for i,r in enumerate(out):
    tag=f'{band}/{seed}/{i}';row=audit(r['question'],tag);row['seed']=seed;row['index']=i;row['parameters']=r.get('metadata',r.get('generation',{})).get('parameters');samp.append(row);records.append(r)
 (d/'sampled.json').write_text(json.dumps(records,indent=2)+'\n');(d/'sample-audit.json').write_text(json.dumps(samp,indent=2)+'\n')
 bad=[r for r in rows+samp if r['issues']];summary[str(kp)]={'stored':len(rows),'imported':sum(':question/math-academy-id'in q for q in stored),'sampled':len(samp),'issues':bad,'package':str(script),'package_sha256':script.parent.name,'bands':{b:sum(b in str(r.get('id'))for r in samp)for b in ['easy','moderate','hard']}};allissues+=bad
 (d/'stored-records.json').write_text(json.dumps([{'knowledge_point':{'db_id':kp,'id':json.loads((d/'kp.json').read_text())[':knowledge-point/id']},'question':normalized_question(q)}for q in stored],indent=2)+'\n')
(H/'math-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
