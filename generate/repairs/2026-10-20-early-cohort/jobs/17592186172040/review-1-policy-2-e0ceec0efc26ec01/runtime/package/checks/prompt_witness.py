"""Retained prompt parser, extended to implicit multiplication of powers."""
import re
import sympy as sp
X,Y=sp.symbols("x y",real=True)
def load_rhs(prompt):
 # Read the actual displayed complete RHS, independently of generation metadata.
 t=prompt.split('x}=')[-1].split('?$')[0]
 def group(text,i):
  assert text[i]=='{';depth=1;j=i+1
  while depth:
   if text[j]=='{':depth+=1
   if text[j]=='}':depth-=1
   j+=1
  return text[i+1:j-1],j
 def convert(text):
  text=text.replace(r'\left','').replace(r'\right','').replace(' ','').replace('{e}', 'e');out='';i=0
  while i<len(text):
   if text.startswith(r'\frac',i):
    num,j=group(text,i+5);den,j=group(text,j);out+='(('+convert(num)+')/('+convert(den)+'))';i=j
   elif text.startswith('e^{',i):
    exponent,j=group(text,i+2);out+='exp('+convert(exponent)+')';i=j
   elif text.startswith('^{',i):
    power,j=group(text,i+1);out+='**('+convert(power)+')';i=j
   elif text[i]=='{':
    sub,j=group(text,i);out+='('+convert(sub)+')';i=j
   else:out+=text[i];i+=1
  return out
 t=convert(t);t=re.sub(r'(?<=\d)(?=[xy])','*',t);t=t.replace('xy','x*y')
 from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
 return parse_expr(t,local_dict={'x':X,'y':Y,'exp':sp.exp},transformations=standard_transformations+(implicit_multiplication_application,))
