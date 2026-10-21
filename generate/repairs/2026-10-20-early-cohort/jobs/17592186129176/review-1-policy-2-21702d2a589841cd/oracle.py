import re
def unpack(r):
 q=r['question']; text=q[':question/problem'];body=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',text,re.S)[1]
 matrix=[[int(x.strip()) for x in row.split('&')] for row in body.split('\\\\')]
 rows=[int(n)-1 for n in re.findall(r'\$(\d)(?:\$|\\text\{)',text.split('rows')[0])]
 vals=[next(x for x in matrix[i] if x!=0) for i in rows];f=q[':question/answer-fields'][0];choices=f[':answer-field/choices']; key=next(a for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);v=int(key[':answer/value'])
 return dict(matrix=matrix,rows=rows,values=vals,total=sum(vals),key=v,bank=[int(a[':answer/value']) for a in choices],position=choices.index(key),rank=sorted(int(a[':answer/value']) for a in choices).index(v))
def oracle(r):
 a=unpack(r);s=r['question'][':question/worked-solution'];eq=re.search(r'So, the answer is \$(.*?)\.\$',s)[1];lhs,rhs=eq.split('=');import ast
 # evaluate only independent integer/addition expressions
 def ev(n):
  if isinstance(n,ast.Expression):return ev(n.body)
  if isinstance(n,ast.Constant) and type(n.value)is int:return n.value
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.USub):return -ev(n.operand)
  if isinstance(n,ast.BinOp) and isinstance(n.op,ast.Add):return ev(n.left)+ev(n.right)
  raise ValueError(ast.dump(n))
 expected_terms='+'.join(str(v) if i==0 or v>=0 else '('+str(v)+')' for i,v in enumerate(a['values']))
 assert a['key']==a['total']==int(rhs)==ev(ast.parse(lhs,mode='eval'))
 assert lhs==expected_terms,(lhs,expected_terms)
 assert len(set(a['bank']))==5
 assert all(-9*len(a['rows'])<=b<=9*len(a['rows']) for b in a['bank'])
 return a
