"""Private TeX reader: reads rendered expressions and formal operator inputs.

Supports only this KP's polynomials, rational powers, radicals, trig and sums.
Rejects unknown commands; no numeric approximation or answer-key substitutions.
"""
import re
from functools import lru_cache
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
X=sp.Symbol('x',positive=True)

def group(text,i):
 while i<len(text) and text[i].isspace():i+=1
 if text[i]!='{':raise ValueError(('group required',text,i))
 depth=1;j=i+1
 while depth:
  if j>=len(text):raise ValueError('unterminated group')
  depth+=(text[j]=='{')-(text[j]=='}');j+=1
 return text[i+1:j-1],j

def translate(text):
 text=text.strip().rstrip('.,').replace(r'\,','').replace(r'\!','').replace(r'\left','').replace(r'\right','').replace(r'\dfrac',r'\frac')
 text=text.replace(r'\operatorname{sin}',r'\sin').replace(r'\operatorname{cos}',r'\cos')
 out='';i=0
 while i<len(text):
  if text.startswith(r'\frac',i):
   a,j=group(text,i+5);b,i=group(text,j);out+='('+translate(a)+')/('+translate(b)+')'
  elif text.startswith(r'\sqrt',i):
   a,i=group(text,i+5);out+=' sqrt('+translate(a)+') '
  elif text.startswith(r'\sin',i) or text.startswith(r'\cos',i):
   fn=text[i+1:i+4];i+=4
   while i<len(text) and text[i].isspace():i+=1
   if text[i]!='x':raise ValueError('only direct x trig allowed')
   out+=' '+fn+'(x) ';i+=1
  elif text.startswith(r'\cdot',i):out+='*';i+=5
  elif text[i]=='{':a,i=group(text,i);out+='('+translate(a)+')'
  elif text[i]=='^':out+='**';i+=1
  elif text[i]=='\\':raise ValueError(('unsupported command',text[i:]))
  else:out+=text[i];i+=1
 return out

@lru_cache(None)
def parse(text):
 value=parse_expr(translate(text),local_dict={'x':X,'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos},transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)
 if value.free_symbols-{X}:raise ValueError(('unparsed symbols',text,value))
 return value

def derivative_input(text):
 match=re.fullmatch(r'\\left\((.*)\\right\)\^\{\\prime\}',text.strip(),re.S)
 if not match:raise ValueError(('formal derivative operator expected',text))
 return parse(match[1]),1

def blocks(text):return re.findall(r'\$\$(.*?)\$\$',text,re.S)
def rows(block):
 block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip()
 return [r.replace(r'\,','').strip().rstrip('.,') for r in block.split(r'\\')]

def expression_parts(block):
 return [r.replace('&','').split('=',1) for r in rows(block)]

def original_operand(text):
 """Read captured formal derivative operators without altering immutable evidence."""
 text=text.replace('′',"'").replace('″',"''").strip().rstrip('.,').replace('&','').strip()
 prefix=r'\frac{\text{d}}{\text{d}x}'
 if text.startswith(prefix):return parse(text[len(prefix):]),1
 match=re.fullmatch(r"(.*)\^\{('+)\}",text,re.S)
 if not match:raise ValueError(('captured operator expected',text))
 operand=match[1].strip()
 if operand.startswith('{'):
  inner,end=group(operand,0)
  if end==len(operand):operand=inner
 return parse(operand),len(match[2])

def original_label(text):
 text=text.replace('′',"'").replace('″',"''").replace('{f}','f').replace('{g}','g').replace('&','').strip()
 match=re.fullmatch(r"([fg])\^\{('+)\}\((x|-?[0-9]+)\)",text)
 if not match:raise ValueError(('captured label expected',text))
 return match[1],len(match[2]),match[3]

def check_original_solution(question):
 """Check every printed source formal operand/intermediate against its derivative stage.

Derive the function from printed formal input (or the supplied first derivative),
then check all evaluation references and field keys. No copied answer-key algebra.
"""
 solution=question.get(':question/worked-solution')
 prompt=question[':question/problem']
 supplied_match=re.search(r'([fg])\(x\)\s*=\s*([^$]+)',prompt)
 supplied=parse(supplied_match[2]) if supplied_match else None
 normalized_prompt=prompt.replace('′',"'").replace('″',"''").replace('{f}','f').replace('{g}','g')
 requested=re.search(r"([fg])\^\{('+)\}\((x|-?[0-9]+)\)",normalized_prompt)
 assert requested and len(requested[2])==2
 if solution is None:
  assert supplied is not None
  second=sp.diff(supplied,X,2)
  for field in question.get(':question/answer-fields',[]):
   matches=[a for a in field[':answer-field/choices'] if sp.simplify(parse(a[':answer/value'])-second)==0]
   assert len(matches)==1
  return {'printed_rows':0,'formal_operators':0,'classification':'worked solution absent; unique mathematically correct original choice verified without inventing a missing key'}
 derivatives={};names=set();row_count=0;operators=0;last=None;point=None
 for block in blocks(solution):
  parts=expression_parts(block);name,order,target=original_label(parts[0][0]);names.add(name)
  first_rhs=parts[0][1].replace('&','').strip()
  try:
   operand,actual_order=original_operand(first_rhs);assert actual_order==1
   operators+=1
   if order==1:derivatives[0]=operand
   else:assert sp.simplify(operand-derivatives[order-1])==0,('source operator input',question[':question/math-academy-id'])
   output=sp.diff(operand,X,actual_order);assert target=='x'
  except ValueError:
   output=parse(first_rhs)
   if target=='x' and order not in derivatives and order==1:derivatives[1]=output
   else:
    assert order in derivatives
    assert sp.simplify(output-derivatives[order].subs(X,int(target)))==0
  if target=='x':derivatives[order]=output
  else:
   assert order==2 and len(names)==1;point=int(target)
   assert re.search(r'x='+str(point),solution)
  for _,rhs in parts:
   rhs=rhs.replace('&','').strip()
   try:
    operand,actual_order=original_operand(rhs);assert actual_order==1
    value=sp.diff(operand,X,actual_order);assert sp.simplify(operand-(derivatives[order-1]))==0
   except ValueError:value=parse(rhs)
   assert sp.simplify(value-output)==0,(question[':question/math-academy-id'],'source printed row',rhs,output)
   row_count+=1
  last=output
 assert len(names)==1 and 2 in derivatives
 assert requested[1] in names
 assert (requested[3]=='x' and point is None) or (requested[3]!='x' and int(requested[3])==point)
 if supplied is not None:assert sp.simplify(supplied-derivatives[0])==0
 for field in question.get(':question/answer-fields',[]):
  correct=field.get(':answer-field/correct')
  if correct:
   correct_value=correct[':answer/value'] if isinstance(correct,dict) else next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==correct[1])
   assert sp.simplify(parse(correct_value)-last)==0
 return {'printed_rows':row_count,'formal_operators':operators,'function_names':sorted(names),'derivative_orders':sorted(derivatives),'evaluation_point':point,'classification':'all existing source mathematics correct'}
