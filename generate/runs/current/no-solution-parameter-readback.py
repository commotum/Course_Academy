"""Root affine parameter readback: coefficients, contradictions and equation equivalence."""
import importlib.util,re
from pathlib import Path
import sympy as s
z=importlib.util.spec_from_file_location('root_parameter_scalar',Path(__file__).with_name('ode-scalar-parser.py'));P=importlib.util.module_from_spec(z);z.loader.exec_module(P)
X,U=P.x,P.u
def group(t,at):
 assert t[at]=='{';depth=1;j=at+1
 while depth:
  assert j<len(t);depth+=(t[j]=='{')-(t[j]=='}');j+=1
 return t[at+1:j-1],j
def clean(raw):
 raw=raw.strip().rstrip('.,?').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('&','')
 while r'\underbrace' in raw:
  pos=raw.index(r'\underbrace');arg,end=group(raw,pos+len(r'\underbrace'));suffix=re.match(r'_\{([ab])\}',raw[end:]);assert suffix;raw=raw[:pos]+'('+arg+')'+raw[end+len(suffix[0]):]
 return raw
def scalar(raw,variable,parameter):
 text=clean(raw)
 # These names occur only as the supplied equation variable and coefficient
 # parameter; protect TeX command words and replace individual variable tokens.
 text=re.sub(r'\\[A-Za-z]+|[A-Za-z]',lambda m:m[0] if m[0].startswith('\\') else 'x' if m[0]==variable else 'u' if m[0]==parameter else m[0],text)
 value=P.scalar(text);assert value.free_symbols<={X,U};return value
def equivalent(residual,reference):
 if s.expand(residual)==0:return True
 ratio=s.cancel(residual/reference)
 return not ratio.free_symbols and ratio.is_finite and ratio!=0
def givens(prompt):
 variable=re.search(r'variable \$([a-z])',prompt);parameter=re.search(r'where \$([a-z])\$ is a constant',prompt);assert variable and parameter;variable,parameter=variable[1],parameter[1];assert variable!=parameter
 blocks=re.findall(r'\$\$(.*?)\$\$',prompt,re.S);assert len(blocks)==1;pieces=blocks[0].split('=');assert len(pieces)==2
 lhs,rhs=[scalar(z,variable,parameter) for z in pieces];delta=s.expand(lhs-rhs);assert s.Poly(delta,X).degree()==1
 coefficient=delta.coeff(X);constant=delta.subs(X,0);assert not constant.free_symbols and constant!=0 and s.Poly(coefficient,U).degree()==1
 answer=s.solve(coefficient,U);assert len(answer)==1 and answer[0].is_Rational
 return variable,parameter,lhs,rhs,coefficient,-constant,answer[0]
def stages(solution,variable,parameter,lhs,rhs,coefficient,right_constant):
 blocks=re.findall(r'\$\$(.*?)\$\$',solution,re.S);assert clean(blocks[0])=='ax=b';counts=dict(rows=0,bindings=0,condition_rows=0,equation_rows=0,annotations=0)
 for block in blocks[1:]:
  block=re.sub(r'\\(?:begin|end)\{aligned\}','',block).strip();has_annotation=r'\underbrace' in block
  cursor=0
  while r'\underbrace' in block[cursor:]:
   start=block.index(r'\underbrace',cursor);arg,end=group(block,start+len(r'\underbrace'));label=re.match(r'_\{([ab])\}',block[end:]);assert label
   wanted=coefficient if label[1]=='a' else right_constant
   assert s.expand(scalar(arg,variable,parameter)-wanted)==0,('coefficient annotation',label[1],arg,wanted)
   cursor=end+len(label[0])
  if re.search(r'\ba=',block) and re.search(r'\bb=',block):
   for name,text in re.findall(r'([ab])=(.*?)(?=,|$)',block):assert s.expand(scalar(text,variable,parameter)-(coefficient if name=='a' else right_constant))==0;counts['bindings']+=1
   continue
  carry=None
  for row in block.split(r'\\'):
   parts=row.split('=');assert len(parts)>=2
   if parts[0].replace('&','').strip():carry=parts[0]
   else:assert carry is not None;parts[0]=carry
   vals=[scalar(z,variable,parameter) for z in parts]
   for a,b in zip(vals,vals[1:]):
    delta=s.expand(a-b)
    if equivalent(delta,lhs-rhs):counts['equation_rows']+=1
    elif equivalent(delta,coefficient):counts['condition_rows']+=1
    else:raise AssertionError((row,delta,coefficient,lhs-rhs))
    counts['rows']+=1
  counts['annotations']+=has_annotation
 assert counts['condition_rows']>=1 and counts['rows']>=2
 return counts
