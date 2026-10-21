# Reused verbatim independent parser and math/shortcut witnesses from review-0 audit.py.
def matrix(text,captured=False):
 if captured and text.startswith('\\\\'):text=text.replace('\\\\','\\')
 ms=[]
 for env,body in re.findall(r'\\begin\{(array|bmatrix)\}(?:\{[^}]*\})?(.*?)\\end\{\1\}',text,re.S):
  ms.append([[int(v.strip()) for v in row.split('&')] for row in body.split('\\\\') if row.strip()])
 return ms

def equation_blocks(text):
 return [[r.replace('&','').strip() for r in body.split('\\\\') if r.strip()] for body in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)]
def linear(s,n):
 s=re.sub(r'\s+','',s);out=[0]*(n+1)
 assert re.fullmatch(r'[+\-0-9xyz]+',s),s
 for term in re.findall(r'[+-]?[^+-]+',s):
  if term[-1] in 'xyz':
   j='xyz'.index(term[-1]);num=term[:-1]; out[j]+=int(num) if num not in ('','+','-') else (-1 if num=='-' else 1)
  else:out[-1]+=int(term)
 return out

def expected(rows):
 n=3 if any('z' in r for r in rows) else 2
 out=[]
 for r in rows:
  a,b=r.split('=');lhs,rhs=linear(a,n),linear(b,n)
  out.append([lhs[i]-rhs[i] for i in range(n)]+[rhs[-1]-lhs[-1]])
 return out

def field(r):return r['question'][':question/answer-fields'][0]
def correct_id(f):
 c=f[':answer-field/correct'];return c[':answer/id'] if isinstance(c,dict) else c[1]
def correct_matrix(r):
 f=field(r);return matrix(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct_id(f)))[0]
def sign(m):return [[(v>0)-(v<0) for v in row] for row in m]
def check_math(r):
 q=r['question']; f=field(r); m=expected(equation_blocks(q[':question/problem'])[0]);assert correct_matrix(r)==m
 bank=[matrix(a[':answer/value'])[0] for a in f[':answer-field/choices']]
 assert len(bank)==5 and bank.count(m)==1 and len({str(v) for v in bank})==5
 sol=q[':question/worked-solution'];assert matrix(sol)==[[row[:-1] for row in m],m]
 for rows in equation_blocks(sol):assert expected(rows)==m
 return {'id':q[':question/id'],'profile':r['generation']['template'],'expected':m,'passed':True}

def sign_strategy(r):
 # Template can be recognized by surface equation layout. No coefficients are calculated.
 profile=r['generation']['template'];target=SIGNATURES[profile]
 candidates=[a for a in field(r)[':answer-field/choices'] if sign(matrix(a[':answer/value'])[0])==target]
 return len(candidates)==1 and candidates[0][':answer/id']==correct_id(field(r)),len(candidates)
def negative_corner(r):
 choices=[a for a in field(r)[':answer-field/choices'] if matrix(a[':answer/value'])[0][-1][-1]<0]
 return len(choices)==1 and choices[0][':answer/id']==correct_id(field(r))

