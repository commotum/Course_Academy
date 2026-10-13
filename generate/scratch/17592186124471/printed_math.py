"""Independent, strict parser of the actual printed elementary LaTeX subset.
No generator model or stored intermediate expressions are used to derive checks.
"""
import re
import sympy as s
X,Y,Z,T=s.symbols('x y z t',real=True)
SYMBOLS={'x':X,'y':Y,'z':Z,'t':T,'pi':s.pi}

def prepare(text):
 text=text.strip().rstrip('.')
 text=re.sub(r'\\operatorname\{(sin|cos|ln)\}',r'\\\1',text)
 text=text.replace('⁡','').replace('−','-').replace(r'\left','').replace(r'\right','')
 text=text.replace('{sin}',r'\sin').replace('{cos}',r'\cos')
 text=text.replace(r'\,',' ').replace(r'\!',' ').replace(r'\cdot','*')
 text=text.replace(r'\dfrac',r'\frac').replace('∂',r'\partial')
 # Scalar/vector formal derivative components are converted to explicit tokens.
 text=text.replace(r'\frac{\text{d}}{\text{d}t}',r'\Dt')
 text=re.sub(r'\\frac\{\\partial\}\{\\partial([xyz])\}',r'\\D\1',text)
 # A lone nested brace around a function name is handled in prepare above.
 return text

class Parser:
 def __init__(self,text):
  text=prepare(text)
  pat=r'\\(?:frac|sqrt|sin|cos|ln|log|pi|Dt|Dx|Dy|Dz)|[0-9]+|[xyz t]|[{}()+*/^,⟨⟩-]'
  self.tokens=re.findall(pat,text)
  residue=re.sub(pat,'',text)
  if residue.strip():raise ValueError('Unparsed math bytes '+repr(residue)+' in '+repr(text))
  self.tokens=[q for q in self.tokens if q.strip()];self.i=0
 def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
 def take(self):q=self.peek();self.i+=1;return q
 def need(self,x):
  if self.take()!=x:raise ValueError('Expected '+x)
 def atom(self):
  token=self.take()
  if token in ('-','+'):return (-1 if token=='-' else 1)*self.power()
  if token in ('{','('):
   q=self.expr();self.need('}' if token=='{' else ')');return q
  if token=='⟨':
   q=[self.expr()]
   while self.peek()==',':self.take();q.append(self.expr())
   self.need('⟩');return s.Matrix(q)
  if token==r'\frac':
   a=self.atom();b=self.atom();return a/b
  if token==r'\sqrt':return s.sqrt(self.atom())
  if token in (r'\sin',r'\cos',r'\ln',r'\log'):
   exponent=1
   if self.peek()=='^':self.take();exponent=self.atom()
   arg=self.atom()
   return {r'\sin':s.sin,r'\cos':s.cos,r'\ln':s.log,r'\log':s.log}[token](arg)**exponent
  if token in (r'\Dt',r'\Dx',r'\Dy',r'\Dz'):
   return s.diff(self.atom(),{r'\Dt':T,r'\Dx':X,r'\Dy':Y,r'\Dz':Z}[token])
  if token==r'\pi':return s.pi
  if token in SYMBOLS:return SYMBOLS[token]
  if token and token.isdigit():return s.Integer(token)
  raise ValueError('Unknown atom '+repr(token))
 def power(self):
  q=self.atom()
  if self.peek()=='^':self.take();q=q**self.atom()
  return q
 def term(self):
  q=self.power()
  while self.peek() is not None and self.peek() not in ('+','-',')','}',',','⟩'):
   op=self.peek()
   if op in ('*','/'):self.take()
   else:op='*'
   v=self.power()
   if isinstance(q,s.MatrixBase) and isinstance(v,s.MatrixBase):
    if op!='*':raise ValueError('Vector quotient')
    q=q.dot(v)
   else:q=q*v if op=='*' else q/v
  return q
 def expr(self):
  q=self.term()
  while self.peek() in ('+','-'):
   op=self.take();v=self.term();q=q+v if op=='+' else q-v
  return q
 def parse(self):
  q=self.expr()
  if self.peek() is not None:raise ValueError('Trailing mathematical token')
  return q

def parse(text):return Parser(text).parse()
def equal(a,b):
 if isinstance(a,s.MatrixBase) or isinstance(b,s.MatrixBase):
  return isinstance(a,s.MatrixBase) and isinstance(b,s.MatrixBase) and a.shape==b.shape and all(s.simplify(x-y)==0 for x,y in zip(a,b))
 return s.simplify(a-b)==0

def blocks(solution):
 out=[]
 for value in re.findall(r'\$\$([\s\S]*?)\$\$',solution):
  if 'aligned' not in value:out.append([value.strip()]);continue
  value=value.strip().removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}')
  rows=re.split(r'\\\\\s*&\s*=',value)
  first=rows[0].split('& =',1)
  out.append([first[1].strip()]+[q.strip() for q in rows[1:]])
 return out

def validate(record):
 q=record['question'];g=record['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 F=parse(re.search(r'\$f\([^$]*?=\s*([^$]+)\$',prompt)[1])
 curve_text=re.search(r'\$r\(t\)\s*=\s*([^$]+)\$',prompt)[1]
 r=list(parse(curve_text));at=parse(re.search(r'at the point \$t\s*=\s*([^$]+)\$',prompt)[1])
 variables=[X,Y,Z][:len(r)]
 grad=s.Matrix([s.diff(F,v) for v in variables]);comp=grad.subs(dict(zip(variables,r)),simultaneous=True)
 vel=s.Matrix([s.diff(v,T) for v in r]);derivative=s.diff(F.subs(dict(zip(variables,r)),simultaneous=True),T)
 correct=s.simplify(derivative.subs(T,at));stages=blocks(sol)
 assert len(stages)==6,('six teaching blocks',len(stages))
 assert len(stages[1])==2 and len(stages[3])==2
 problems=[]
 for block_index,expected in ((1,grad),(2,comp),(3,vel)):
  for row_index,row in enumerate(stages[block_index]):
   got=parse(row)
   if not equal(got,expected):problems.append({'block':block_index,'row':row_index,'printed':row,'actual':str(got),'expected':str(expected)})
 for i,row in enumerate(stages[4][1:],1):
  got=parse(row)
  if not equal(got,derivative):problems.append({'block':4,'row':i,'printed':row,'actual':str(got),'expected':str(derivative)})
 for i,row in enumerate(stages[5]):
  got=parse(row)
  if not equal(got,correct):problems.append({'block':5,'row':i,'printed':row,'actual':str(got),'expected':str(correct)})
 # Check actual prose equations, not only aligned math or stored parameters.
 prose=re.sub(r'\$\$[\s\S]*?\$\$','',sol)
 for variable,body in re.findall(r'([xyzt])\s*=\s*([^$]+)\$',prose):
  body=body.rstrip(':, .')
  # source combines assignments in one inline span; split into full slots.
  for slot in re.split(r',\s*(?=[xyz]\s*=)',variable+'='+body):
   if not re.match(r'^[xyzt]\s*=',slot):continue
   var,expr=slot.split('=',1);expr=expr.rstrip(', .')
   if ' and ' in expr:continue
   got=parse(expr);wanted=at if var.strip()=='t' else r[variables.index(SYMBOLS[var.strip()])]
   assert equal(got,wanted),('stale prose',slot,wanted)
 f=q[':question/answer-fields'][0];values=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 for i,v in enumerate(values):
  designated=f[':answer-field/choices'][i][':answer/id']==f[':answer-field/correct'][1]
  assert equal(v,correct)==designated,('wrong printed correct choice',v,correct)
 assert len(values)==5 and all(not equal(v,w) for i,v in enumerate(values) for w in values[i+1:])
 if not g['raw_source_notation']:
  assert g['eligible_for_learning'] and not g['evidence_only']
  assert 'f('+','.join(map(str,variables))+')' in prose.split('with respect')[0]
  assert '∇f('+','.join(map(str,variables))+')' in sol
  terms=[s.simplify(a*b) for a,b in zip(comp,vel)]
  name=g['template']
  if name in ('radical_square','log_norm'):
   wrong=[terms[0],terms[-1],sum(comp),sum(a*b*b for a,b in zip(comp,vel))]
  elif len(r)==2:
   wrong=[terms[0],terms[1],sum(comp),terms[0]-terms[1]]
  else:
   wrong=[sum(terms[1:]),sum(terms[:-1]),sum(comp),sum(terms[:-1])-terms[-1]]
  expected=[correct]+[s.simplify(v.subs(T,at)) for v in wrong]
  assert all(sum(equal(v,w) for w in expected)==1 for v in values),('printed complete operation bank',values,expected)
  row_counts={'quadratic_affine':[1,2,2,2,4,2],'sine_difference':[1,2,2,2,4,2],'mixed_product':[1,2,2,2,4,2],
   'quotient':[1,2,1,2,5,2],'trig_powers':[1,2,1,2,4,4],'square_difference':[1,2,2,2,4,2],
   'triple_product':[1,2,2,2,5,2],'radical_square':[1,2,2,2,5,3],'log_norm':[1,2,2,2,5,3]}
  assert [len(q) for q in stages]==row_counts[name],('teaching sequence',name)
 else:
  assert g['evidence_only'] and not g['eligible_for_learning']
 return problems
