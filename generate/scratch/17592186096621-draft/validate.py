#!/usr/bin/env python3
"""Independent rendered expression reader. Does not trust generation parameters."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
g=load('draft',HERE.with_suffix('.py'));p=load('independent_scalar',HERE/'math_parser.py');X=p.x

def save(name,z):(HERE/name).write_text(json.dumps(z,indent=2,default=str)+'\n')
def eq(a,b):
 z=(a-b).subs(s.tan(X),s.sin(X)/s.cos(X)).subs(s.sec(X),1/s.cos(X))
 n=s.expand(s.together(z).as_numer_denom()[0])
 if n==0:return True
 if n.has(s.sin(X)):
  try:n=s.rem(s.Poly(n,s.sin(X)),s.Poly(s.sin(X)**2+s.cos(X)**2-1,s.sin(X))).as_expr()
  except s.PolynomialError:pass
 return s.expand(n)==0

def group(text,i,opening='{',closing='}'):
 while i<len(text) and text[i].isspace():i+=1
 assert text[i]==opening,(text,i,opening)
 start=i+1;depth=1;i+=1
 while depth:
  assert i<len(text),text
  if text[i]==opening:depth+=1
  if text[i]==closing:depth-=1
  i+=1
 return text[start:i-1],i

def parse(raw):
 text=raw.strip().rstrip('.,').replace('[','(').replace(']',')').replace(r'\cancel','')
 return p.scalar(text)

def fraction(raw):
 raw=raw.strip();assert raw.startswith(r'\frac'),raw
 a,i=group(raw,5);b,i=group(raw,i);assert not raw[i:].strip().rstrip('.,'),raw
 return a,b

def displayed_parts(prompt):
 if '$h(x)=' in prompt:
  return parse(re.search(r'\$f\(x\)=(.*?)\$',prompt)[1]),parse(re.search(r'\$h\(x\)=(.*?)\$',prompt)[1])
 m=re.search(r'\$[fy](?:\(x\))?\s*=\s*(.*?)\$',prompt)
 if m and m[1].strip().startswith(r'\frac'):
  a,b=fraction(m[1].strip().rstrip('.,'));return parse(a),parse(b)
 # Context-completed function-pair questions.
 a=re.search(r'\$f\(x\)=(.*?)\$',prompt)[1]
 b=re.search(r'\$h\(x\)=(.*?)\$',prompt)[1]
 return parse(a),parse(b)

def derivatives(raw):
 text=raw;seen=[];sub={}
 while r'^{\prime}' in text:
  end=text.index(r'^{\prime}');assert text[end-1]==')',text
  depth=1;start=end-2
  while depth:
   assert start>=0,text
   if text[start]==')':depth+=1
   elif text[start]=='(':depth-=1
   start-=1
  start+=1;operand=parse(text[start+1:end-1]);seen.append(operand)
  name=['i','j','k'][len(seen)-1];sub[p.locals_[name]]=s.diff(operand,X);text=text[:start]+name+text[end+len(r'^{\prime}'):]
 return parse(text).subs(sub),seen,text

def rows(sol):
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 return [[z.split('&=',1)[1].strip() for z in b.split(r'\\') if '&=' in z] for b in blocks]

def read(record):
 q=record['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 g.FMT.validate_generated_record(copy.deepcopy(record));u,v=displayed_parts(prompt);der=s.diff(u/v,X)
 # Independently check declarations in all source solutions, including recall f,h.
 if '$u(x)=' in sol:
  assert eq(parse(re.search(r'\$u\(x\)=(.*?)\$',sol)[1]),u)
  assert eq(parse(re.search(r'\$v\(x\)=(.*?)\$',sol)[1]),v)
 elif sol.startswith('Recall'):
  assert eq(parse(re.search(r'\$f\(x\)=(.*?)\$',sol)[1]),u)
  assert eq(parse(re.search(r'\$h\(x\)=(.*?)\$',sol)[1]),v)
 rs=rows(sol);assert rs and rs[0]
 assert rs[0][0]==r'\frac{u^{\prime}(x)\cdot v(x)-u(x)\cdot v^{\prime}(x)}{[v(x)]^{2}}','ordered formal quotient rule'
 formal_inputs=0
 derivative_rows=rs[0][1:]+[row for b in (rs[1:-1] if 'slope of the tangent line' in prompt else rs[1:]) for row in b]
 for row in derivative_rows:
  if r'^{\prime}' in row:
   value,operands,substituted=derivatives(row);assert len(operands)==2 and eq(operands[0],u) and eq(operands[1],v),'formal derivative input changed'
   # Check the ordered four quotient operands separately, before zero products collapse.
   num,den=fraction(substituted);m=re.fullmatch(r'i\\cdot \((.*)\)-\((.*)\)\\cdot j',num);assert m,'ordered derivative-products erased/swapped'
   assert eq(parse(m[1]),v) and eq(parse(m[2]),u) and eq(parse(den),v**2)
   formal_inputs+=2
  else:value=parse(row)
  assert eq(value,der),('unequal derivative stage',row,value,der)
 # Read target from actual prompt and every target-specific row/prose.
 target=None
 if 'slope of the tangent line' in prompt:
  matches=re.findall(r'\$x=(.*?)\$',prompt);assert matches
  target=parse(matches[0]);assert not target.free_symbols and v.subs(X,target)!=0
  if u.has(s.log) or v.has(s.log):assert target.is_positive
  answer=s.simplify(der.subs(X,target));assert len(rs)>=2
  target_lhs=re.findall(r'f[^&\n]*?\((.*?)\)\s*&=',re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[-1])
  assert target_lhs and eq(parse(target_lhs[0].replace(r'\,','')),target),('stale evaluated target',target_lhs)
  for row in rs[-1]:assert eq(parse(row),answer),('unequal evaluated stage',row)
  for text_target in re.findall(r'substitute \$x=(.*?)\$',sol):assert eq(parse(text_target),target)
  ending=re.search(r'Therefore, the slope of the tangent line(?: at \$x=.*?\$)? is \$(.*?)\$',sol);assert ending and eq(parse(ending[1]),answer)
 else:answer=der
 original_counts={'q-17921':5,'q-47999':5,'q-340318':8,'q-9908':11,'q-167328':5,'q-167782':5,'q-166075':5,'q-2385':5,'q-340308':4,'q-340309':4,'q-340316':7,'q-47943':4,'q-47998':5,'q-48504':8,'q-48507':9}
 expected_stages=5 if record['generation']['template']==g.HARD else original_counts[record['generation']['template']]
 assert sum(map(len,rs))==expected_stages,'operative equal stage erased/added'
 # Authored evaluated substitution retains all four ordered factors, including zeros.
 if record['generation']['authored_extension'] and record['generation']['template'] in ['q-17921','q-47999','q-340318','q-9908','q-340309','q-340316','q-48504','q-48507',g.HARD]:
  numerator,denominator=fraction(rs[0][2]);m=re.fullmatch(r'\((.*?)\)\\cdot \((.*?)\)-\((.*?)\)\\cdot \((.*?)\)',numerator);assert m,'evaluated ordered operands erased'
  for actual,want in zip(m.groups(),[s.diff(u,X),v,u,s.diff(v,X)]):assert eq(parse(actual),want),'wrong evaluated quotient operand'
  assert eq(parse(denominator),v**2)
 field=q[':question/answer-fields'][0];vals=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
 if '{{field-1}}' in prompt and '| --- | --- |' in prompt:
  assert field[':answer-field/type'].endswith('/blank')
  table=[line for line in prompt.splitlines() if line.startswith('|')]
  assert len(table)==3 and table[0].count('{{field-1}}')==1
  numerator=table[0].split('|')[2].replace('$','').replace('{{field-1}}','('+field[':answer-field/choices'][0][':answer/value']+')')
  denominator=table[2].split('|')[2].replace('$','')
  assert eq(parse(numerator)/parse(denominator),der),'partial blank full context'
  answer=s.cos(X)-s.sin(X)
 assert sum(eq(z,answer) for z in vals)==1,'unique correct value'
 assert all(not eq(z,y) for i,z in enumerate(vals) for y in vals[:i]),'bank collision'
 correct=field[':answer-field/correct'][1];assert next(a[':answer/id'] for a,z in zip(field[':answer-field/choices'],vals) if eq(z,answer))==correct
 assert record['generation']['mathematical_fingerprint']==g.task_identity(u,v,target),'rendered task identity'
 return {'u':u,'v':v,'target':target,'derivative':der,'answer':answer,'formal_inputs':formal_inputs,'stages':sum(map(len,rs))}

def main():
 records=[];failures=[]
 for t in g.SPEC:
  for n,params in enumerate([g.original_parameters(t),dict(g.original_parameters(t),scale=2),dict(g.original_parameters(t),scale=-3)]):
   try:
    r=g.generate(g.SPEC[t][3],n,t,params);z=read(r);records.append(r);print(t,n,'PASS',flush=True)
   except Exception as e:failures.append([t,params,str(e)]);print(t,n,'FAIL',str(e)[:120],flush=True);continue
 for params in [{'a':1,'b':1},{'a':2,'b':3},{'a':-1,'b':1},{'a':-2,'b':1}]:
  try:r=g.generate('hard',0,g.HARD,params);z=read(r);records.append(r)
  except Exception as e:failures.append([g.HARD,params,str(e)])
 save('review.json',records);save('first-validation.json',{'records':len(records),'failures':failures});print(json.dumps({'records':len(records),'failures':failures},indent=2))
if __name__=='__main__':main()
