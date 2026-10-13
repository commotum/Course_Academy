"""Independent small TeX reader for the displayed scalar/vector grammar here.
It parses original source banks and generated function/solution/choice math.
No generation metadata or answer lookups are needed to derive displayed math.
"""
import re
import sympy as S
t,u=S.symbols('t u',real=True)

def scalar(s):
 s=s.strip().replace('⁡','').replace(r'\,','').replace(r'\left','').replace(r'\right','').replace(r'\cdot','*')
 s=re.sub(r'\\operatorname\{(\w+)\}',r'\1',s)
 s=re.sub(r'\{(sin|cos|tan|sec|ln)\}',r'\1',s)
 s=s.replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\tan','tan').replace(r'\sec','sec').replace(r'\ln','ln').replace(r'\log','ln').replace(r'\exp','exp')
 tokens=re.findall(r'\\frac|\\sqrt|sin|cos|tan|sec|ln|exp|\d+|[tue]|[{}()^+*/-]',s)
 residue=re.sub(r'\\frac|\\sqrt|sin|cos|tan|sec|ln|exp|\d+|[tue]|[{}()^+*/-]|\s','',s)
 if residue:raise ValueError(('Unparsed scalar',s,residue))
 i=0
 def expr(bp=0):
  nonlocal i
  if i>=len(tokens):raise ValueError(('Missing atom',s))
  tok=tokens[i];i+=1
  if tok in ('-','+'):left=(-1 if tok=='-' else 1)*expr(25)
  elif tok in ('{','('):
   left=expr();end='}' if tok=='{' else ')'
   if i>=len(tokens) or tokens[i]!=end:raise ValueError(('Unbalanced scalar',s))
   i+=1
  elif tok==r'\frac':left=atom()/atom()
  elif tok==r'\sqrt':left=S.sqrt(atom())
  elif tok in ('sin','cos','tan','sec','ln','exp'):
   fn={'sin':S.sin,'cos':S.cos,'tan':S.tan,'sec':S.sec,'ln':S.log,'exp':S.exp}[tok]
   power=S.Integer(1)
   if i<len(tokens) and tokens[i]=='^':i+=1;power=atom()
   left=fn(atom() if i<len(tokens) and tokens[i]=='(' else expr(20))**power
  elif tok.isdigit():left=S.Integer(tok)
  elif tok in ('t','u','e'):left={'t':t,'u':u,'e':S.E}[tok]
  else:raise ValueError(('Unexpected token',s,tok))
  while i<len(tokens) and tokens[i] not in ('}',')'):
   tok=tokens[i]
   if tok in ('+','-'):lb=10;op=tok
   elif tok in ('*','/'):lb=20;op=tok
   elif tok=='^':lb=30;op=tok
   else:lb=20;op='implicit'
   if lb<bp:break
   if op!='implicit':i+=1
   right=expr(lb if op=='^' else lb+1)
   left={'+':lambda:left+right,'-':lambda:left-right,'*':lambda:left*right,'implicit':lambda:left*right,'/':lambda:left/right,'^':lambda:left**right}[op]()
  return left
 def atom():return expr(31)
 result=expr()
 if i!=len(tokens):raise ValueError(('Unused tokens',s,tokens[i:]))
 return result

def vector(s):
 s=s.strip().replace(r'\,','')
 if s.startswith('['):
  prefix=r'[\begin{aligned}';suffix=r'\end{aligned}]'
  if not s.startswith(prefix) or not s.endswith(suffix):raise ValueError(('Matrix form',s))
  return [scalar(x) for x in s[len(prefix):-len(suffix)].split(r'\\')]
 if s.startswith('⟨'):
  return [scalar(x) for x in s[1:-1].split(',')]
 v=[S.Integer(0)]*3;prev=0
 for m in re.finditer(r'([ijk])(?![A-Za-z])',s):
  text=s[prev:m.start()].strip().removesuffix(r'\,').strip()
  if text in ('','+','-'):text+='1'
  v['ijk'.index(m[1])]+=scalar(text);prev=m.end()
 if s[prev:].strip():raise ValueError(('Vector trailing data',s[prev:]))
 if prev==0:raise ValueError(('No vector basis',s))
 return v

def split_rows(s):
 """Split only outer aligned rows; preserve complete nested column vectors."""
 start=r'\begin{aligned}';end=r'\end{aligned}'
 if s.startswith(start):s=s[len(start):-len(end)]
 out=[];depth=0;i=0;last=0
 while i<len(s):
  if s.startswith(start,i):depth+=1;i+=len(start)
  elif s.startswith(end,i):depth-=1;i+=len(end)
  elif s.startswith(r'\\',i) and depth==0:out.append(s[last:i].strip());i+=2;last=i
  else:i+=1
 out.append(s[last:].strip());return out

def read_prompt(record):
 prompt=record['question'][':question/problem']
 spans=re.findall(r'\$([^$]+)\$',prompt)
 f=vector(spans[0].split('=',1)[1]);h=scalar(spans[1].split('=',1)[1])
 return f,h

# Derivative statements are evaluated independently. This fixed prefix/suffix
# grammar is exactly the generated derivative notation, not a value table.
def derivatives(s):
 prefixes=[(r'\frac{\text{d}}{\text{d}u}\left(',u),(r'\frac{\text{d}}{\text{d}t}\left(',t)]
 for prefix,var in prefixes:
  while prefix in s:
   start=s.index(prefix);a=start+len(prefix);depth=1;i=a
   while depth:
    if s.startswith(r'\right)',i):depth-=1
    elif s.startswith(r'\left(',i):depth+=1
    if depth:i+=1
   raw=s[a:i];val=S.diff(scalar(raw),var)
   s=s[:start]+'('+S.latex(val)+')'+s[i+len(r'\right)'):]
 return s

def scaled_vector(s,h,hp):
 s=derivatives(s).replace(r'u^{′}(t)', '('+S.latex(hp)+')').replace('u(t)','('+S.latex(h)+')')
 # u(t)' is printed by SymPy as a derivative for symbolic composition rows.
 s=s.replace(r'\frac{d}{d t} u{\left(t \right)}','('+S.latex(hp)+')')
 # Find a complete column or angle vector, or a parenthesized basis vector.
 if s.startswith('['):
  end=s.index(r'\end{aligned}]')+len(r'\end{aligned}]');v=vector(s[:end]);rest=s[end:]
 elif s.startswith('⟨'):
  end=s.index('⟩')+1;v=vector(s[:end]);rest=s[end:]
 elif s.startswith(r'\left('):
  # Parenthesized basis vectors can themselves have component parentheses.
  a=len(r'\left(');i=a;depth=1
  while depth:
   if s.startswith(r'\left(',i):depth+=1;i+=len(r'\left(')
   elif s.startswith(r'\right)',i):depth-=1;i+=len(r'\right)')
   else:i+=1
  v=vector(s[a:i-len(r'\right)')]);rest=s[i:]
 else:return vector(s)
 return [x*scalar(rest.removeprefix(r'\cdot ').strip()) for x in v] if rest.strip() else v
