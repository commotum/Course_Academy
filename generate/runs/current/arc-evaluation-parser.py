"""Parent definite integral and antiderivative stages, read from printed TeX."""
import importlib.util,re
from pathlib import Path
import sympy as s
spec=importlib.util.spec_from_file_location('root_arc_eval_base',Path(__file__).with_name('arc-vector-parser.py'));p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
t=p.p.t;u=p.p.u

def integral(raw):
 raw=raw.strip().rstrip('.,?').replace(r'\displaystyle','').replace(r'{\int }',r'\int').replace(r'{\int}',r'\int')
 raw=raw.replace(r'\left','').replace(r'\right','')
 raw=re.sub(r'\\(?:mathrm|text)\s+d([tu])',r'\\mathrm{d}\1',raw)
 wrapper=re.fullmatch(r'(\d+)\((.*)\)',raw,re.S)
 if wrapper:
  a,b,fn,var=integral(wrapper[2]);return a,b,s.Integer(wrapper[1])*fn,var
 start=raw.index(r'\int');prefix=raw[:start].strip();factor=p.math(prefix) if prefix else s.Integer(1)
 pos=start+len(r'\int');assert raw[pos]=='_';lo,pos=p.group(raw,pos+1);assert raw[pos]=='^';hi,pos=p.group(raw,pos+1)
 tail=raw[pos:].strip();m=re.search(r'(?:\\(?:text|mathrm)\{d\}\s*([tu])|d([tu]))\s*$',tail);assert m,raw
 body=tail[:m.start()].rstrip().removesuffix(r'\,');fn=p.math(body) if body else s.Integer(1);v=t if (m[1] or m[2])=='t' else u
 return p.math(lo),p.math(hi),s.simplify(factor*fn),v

def evaluated(raw):
 raw=raw.strip().rstrip('.,?').replace(r'\left','').replace(r'\right','')
 raw=re.sub(r'\\(?:big|Big|bigg|Bigg)(?:l|r)?','',raw).replace(r'\,','').replace('{|}','|')
 pos=raw.index('|')
 if raw[pos+1:pos+2]=='}':
  depth=1;i=pos-1
  while depth:
   assert i>=0,raw;depth+=(raw[i]=='}')-(raw[i]=='{');i-=1
  raw=raw[:i+1]+raw[i+2:pos+1]+raw[pos+2:];pos=raw.index('|')
 assert raw[pos+1]=='_';lo,end=p.group(raw,pos+2);assert raw[end]=='^';hi,end=p.group(raw,end+1)
 prefix=raw[:pos];suffix=raw[end:];balance=prefix.count('(')-prefix.count(')')
 assert balance>=0 and suffix.strip()==')'*balance,(raw,prefix,suffix,balance)
 anti=p.math(prefix+')'*balance);var=u if u in anti.free_symbols else t
 a,b=p.math(lo),p.math(hi);return anti,var,a,b,s.simplify(anti.subs(var,b)-anti.subs(var,a))

def substitution(text):
 found=re.search(r'substitution \$u=(.*?)\$',text)
 if not found:return None
 expr=p.math(found[1].rstrip(','));assert t in expr.free_symbols and u not in expr.free_symbols
 # Check the displayed differential factor, including commas/math boundaries.
 differential=re.search(r'\\(?:mathrm|text)\{d\}u=(.*?)\\(?:mathrm|text)\{d\}t',text);assert differential,text
 assert p.same(p.math(differential[1]),s.diff(expr,t)),(expr,differential[1])
 return expr

def groups(text):return [re.split(r'\\\\',z) for z in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',text,re.S)]
def replace_norm(raw,speed):return re.sub(r'(?:‖|\\\|)\{?[rfgh]\}?(?:\^\{(?:′|\\prime)\}|\x27)\(t\)(?:‖|\\\|)',lambda _: '('+s.latex(speed)+')',raw)
def stages(text,curve,bounds):
 speed=p.speed(curve);expected=s.integrate(p.on_interval(speed,bounds),(t,*bounds));sub=substitution(text)
 roles=[];counts=dict(integral_stages=0,antiderivative_stages=0,evaluation_stages=0,substitutions=bool(sub))
 # All groups following the derivative/norm derivation must compute the same length.
 for group in groups(text)[1:]:
  for row in group:
   for rhs in row.split('=')[1:]:
    raw=replace_norm(rhs.replace('&','').strip().rstrip('.,?'),speed)
    if r'\int' in raw:
     a,b,fn,var=integral(raw)
     if var==t:assert (a,b)==bounds and p.same_on(fn,speed,bounds),(raw,fn,speed,bounds)
     else:
      assert sub is not None and (a,b)==tuple(sub.subs(t,v) for v in bounds)
      assert p.same_on(fn.subs(u,sub)*s.diff(sub,t),speed,bounds),(raw,sub,fn,speed)
     roles.append('integral');counts['integral_stages']+=1
    elif '|' in raw:
     anti,var,a,b,value=evaluated(raw);assert p.same(value,expected),(raw,value,expected)
     if var==t:assert (a,b)==bounds and p.same_on(s.diff(anti,t),speed,bounds),(raw,anti,speed)
     else:assert sub is not None and (a,b)==tuple(sub.subs(t,z) for z in bounds) and p.same_on(s.diff(anti,u).subs(u,sub)*s.diff(sub,t),speed,bounds)
     roles.append('antiderivative');counts['antiderivative_stages']+=1
    else:
     value=p.math(raw);assert p.same(value,expected),(raw,value,expected);roles.append('evaluation');counts['evaluation_stages']+=1
 return expected,tuple(roles),counts
