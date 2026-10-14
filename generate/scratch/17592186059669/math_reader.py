"""Independent reader of displayed curve expressions and point pairs."""
import re
import sympy as sp
x=sp.Symbol('x');f=sp.Function('f')
def expression(s):
 s=re.sub(r'\\(?:d?frac)\s*\{([^{}]+)\}\s*\{([^{}]+)\}',r'((\1)/(\2))',s)
 s=s.replace(r'\cdot','*').replace(' ','').replace('−','-').rstrip('.')
 s=re.sub(r'(?<=[\d)])(?=[xf(])','*',s)
 return sp.expand(sp.sympify(s,locals={'x':x,'f':f}))
def coordinate(s):
 z=s.strip().rstrip('.');assert z[0]=='(' and z[-1]==')'
 a,b=z[1:-1].split(',');return expression(a),expression(b)
def read_prompt(prompt):
 pt,src,dst=re.search(r'point\s+\$(.*?)\$.*?curve\s+\$y\s*=\s*(.*?)\$.*?lie on\s+\$y\s*=\s*(.*?)\$',prompt,re.S).groups()
 return coordinate(pt),expression(src),expression(dst.rstrip('?'))
def required(prompt):
 point,src,dst=read_prompt(prompt);calls=list(src.atoms(sp.Function));assert len(calls)==1
 call=calls[0];u=call.args[0].subs(x,point[0]);symbol=sp.Symbol('w')
 w=sp.solve(src.subs(call,symbol).subs(x,point[0])-point[1],symbol)[0]
 targetcall=list(dst.atoms(sp.Function));assert len(targetcall)==1
 tx=sp.solve(targetcall[0].args[0]-u,x)[0];ty=dst.subs(x,tx).subs(f(u),w)
 assert ty.is_Rational and tx.is_Rational
 return point,(u,w),(tx,ty),src,dst
