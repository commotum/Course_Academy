"""Rendered-only independent calculus audit; no generator recipes or metadata."""
import re
import sympy as sp
import parser as p

def clean(s):
 s=re.sub(r'\\(?:begin|end)\{aligned\}','',s).replace('&','').strip().rstrip('.,')
 s=s.replace(r'{\int }',r'\int').replace(r'\displaystyle','').replace(r'{|}','|').replace('[','(').replace(']',')')
 s=re.sub(r'(?<![A-Za-z\\])(sin|cos|tan|cot|sec|csc)(?=\\|\s|\()',r'\\\1',s)
 return s

def balance(s):
 s=s.replace(r'\left','').replace(r'\right','')
 # Closing outer parentheses follow endpoint markers rather than the primitive.
 if s.count('(')>s.count(')'):s+=')'*(s.count('(')-s.count(')'))
 return s

def term(s,slope):
 s=clean(s)
 if r'\int' in s:
  at=s.index(r'\int');end=at+4;lo=hi=None
  if s[end:end+1]=='_':
   a,end=p.group(s,end+1)if s[end+1]=='{'else(s[end+1],end+2);assert s[end]=='^';b,end=p.group(s,end+1)if s[end+1]=='{'else(s[end+1],end+2);lo,hi=p.scalar(a),p.scalar(b)
  diffs=list(re.finditer(r'\\(?:text|textrm)\s*\{?\s*d\s*\}?\s*([xu])',s));assert len(diffs)==1,(s,diffs)
  diff=diffs[0];var=diff[1]
  expr=p.scalar(s[:at]+s[end:diff.start()]+'1'+s[diff.end():])
  if var=='u':
   expr=expr.subs(p.u,slope*p.x)*slope
   if lo is not None:lo,hi=lo/slope,hi/slope
  return ('integral',expr,lo,hi)
 if '|' in s:
  prim,limits=s.split('|',1);prim=balance(prim)
  # Ignore grouping around the original | glyph.
  prim=prim.rstrip('{');limits=limits.lstrip('}')
  assert limits[0]=='_',s
  lo,i=p.group(limits,1)if limits[1]=='{'else(limits[1],2);assert limits[i]=='^'
  hi,i=p.group(limits,i+1)if limits[i+1]=='{'else(limits[i+1],i+2)
  e=p.scalar(prim);lo,hi=p.scalar(lo),p.scalar(hi);var=p.u if e.has(p.u)else p.x
  return ('value',sp.simplify(e.subs(var,hi)-e.subs(var,lo)),(str(e.subs(var,hi)),str(-e.subs(var,lo))),sp.diff(e.subs(p.u,slope*p.x),p.x),(lo/slope,hi/slope)if var==p.u else(lo,hi))
 e=p.scalar(s)
 if e.has(p.x)or e.has(p.u):return ('primitive',sp.diff(e.subs(p.u,slope*p.x),p.x))
 return ('value',e)

def interval_audit(expr,lo,hi):
 if lo is None:return {'kind':'indefinite','restriction':'original quotient poles and cancelled zeros excluded on each connected component'}
 conditions=[]
 for z in expr.atoms(sp.tan,sp.sec,sp.cot,sp.csc):
  conditions.append(sp.cos(z.args[0])if z.func in [sp.tan,sp.sec]else sp.sin(z.args[0]))
 # The unsimplified quotient denominator still carries cancellation holes.
 denominator=sp.denom(expr)
 if denominator!=1:conditions.append(denominator)
 holes=[]
 for condition in conditions:
  roots=sp.solveset(condition,p.x,domain=sp.Interval(lo,hi))
  assert roots==sp.EmptySet or isinstance(roots,sp.FiniteSet),('unresolved real pole set',condition,roots)
  for z in roots:
   assert z in [lo,hi],('interior original-domain hole',condition,z)
   # Only source removable boundary holes are admitted, with a finite one-sided value.
   normalized=sp.trigsimp(expr)
   value=sp.limit(normalized,p.x,z,dir='+'if z==lo else '-')
   assert value.is_finite,('nonintegrable endpoint',condition,z,value)
   holes.append(str(z))
 return {'interval':[str(lo),str(hi)],'original_conditions':[str(z)for z in conditions],'boundary_holes':sorted(set(holes)),'interior_poles':[]}

def audit(q):
 problem=q[':question/problem'];expr,lo,hi=p.integral(problem);domain=interval_audit(expr,lo,hi);solution=q[':question/worked-solution'];slope=sp.Integer(1)
 m=re.search(r'Let \$u=([^$]+)',solution)
 if m:
  slope=sp.simplify(p.scalar(m[1].rstrip('.'))/p.x);assert slope>0 and not slope.has(p.x)
  dm=re.search(r'Then \$([^$]+)',solution);assert dm
  ds=dm[1].rstrip('.');left,right=ds.split('=')
  differential=lambda z:p.scalar(re.sub(r'\\(?:text|textrm)\{d\}u','('+str(slope)+')',re.sub(r'\\(?:text|textrm)\{d\}x','1',z)))
  assert p.same(differential(left),differential(right)),('false differential',ds)
  # Read the two rows of any transformed endpoint table.
  lines=[z for z in solution.splitlines()if z.startswith('| $x$')or z.startswith('| $u$')]
  if lines:
   assert len(lines)==2
   vals=[[p.scalar(v.strip().strip('$'))for v in z.split('|')[2:-1]]for z in lines]
   assert vals[0]==[lo,hi] and all(p.same(a*slope,b)for a,b in zip(*vals)),('false bound table',vals)
 expected=None
 if lo is not None:
  for block in re.findall(r'\$\$([\s\S]*?)\$\$',solution):
   for z in re.split(r'\\\\\s*&?\s*=?|&?\s*=',block):
    if '|' in z:
     witness=term(z,slope);assert len(witness)==5 and p.same(witness[3],expr) and witness[4]==(lo,hi),('false evaluated primitive',z,witness)
     expected=witness[1];break
   if expected is not None:break
  assert expected is not None,'missing evaluated primitive'
 checked=[];signed=[]
 for b in re.findall(r'\$\$([\s\S]*?)\$\$',solution):
  terms=[clean(z)for z in re.split(r'\\\\\s*&?\s*=?|&?\s*=',b)if clean(z)]
  for s in terms:
   result=term(s,slope)
   if result[0]=='integral':assert p.same(result[1],expr) and (result[2],result[3])==(lo,hi),('false formal stage',s,result,(expr,lo,hi))
   elif result[0]=='primitive':assert lo is None and p.same(result[1],expr),('false primitive',s,result,expr)
   else:
    assert lo is not None and p.same(result[1],expected),('false value',s,result,expected)
    if len(result)>2:
     assert p.same(result[3],expr) and result[4]==(lo,hi),('false primitive at intermediate evaluation',s,result)
     signed.append(result[2])
   checked.append(s)
 f=q[':question/answer-fields'][0];values=[p.scalar(z[':answer/value'])for z in f[':answer-field/choices']];correct=f[':answer-field/correct'][1]
 ci=[z[':answer/id']for z in f[':answer-field/choices']].index(correct)
 equivalent=lambda z:p.same(sp.diff(z,p.x),expr) if lo is None else p.same(z,expected)
 assert equivalent(values[ci]);assert sum(equivalent(z)for z in values)==1
 same_choice=(lambda a,b:p.same(sp.diff(a-b,p.x),0))if lo is None else p.same
 assert all(not same_choice(a,b)for i,a in enumerate(values)for b in values[i+1:]),'duplicate complete bank, including arbitrary-C equivalence'
 assert checked
 return {'real_domain':domain,'operative_terms':len(checked),'terms':checked,'signed_endpoint_contributions':signed,'bank_choices':len(values),'computed_value':str(expected)}
