"""Parent parser of actual substitution systems, blanks, banks and all equations."""
import importlib.util,re
from pathlib import Path
sp=importlib.util.spec_from_file_location('parent_system_scalar',Path(__file__).with_name('ode-scalar-parser.py'));p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p);s=p.s
def scalar(raw,names):
 raw=raw.replace(r'\dfrac',r'\frac').replace(r'\tfrac',r'\frac')
 pieces=re.split(r'(\\[A-Za-z]+)',raw.strip().rstrip('.,'));mapping=dict(zip(names,('x','y')))
 raw=''.join(z if z.startswith('\\') else re.sub('[a-z]',lambda m:mapping.get(m[0],m[0]),z) for z in pieces)
 return p.scalar(raw)
def eq(raw,names):
 parts=raw.replace('&','').split('=');assert len(parts)==2,raw;return scalar(parts[0],names)-scalar(parts[1],names)
def blocks(text):return [next(z for z in b if z) for b in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',text,re.S)]
def system(prompt,worked):
 if '$a' in prompt or '$b' in prompt or 'a - b' in prompt:names=('a','b')
 elif 'p - q' in prompt:names=('p','q')
 else:names=('x','y')
 equations=[]
 for b in blocks(prompt):
  for row in b.strip().removeprefix(r'\{').removeprefix('{').split(';'):
   if row.count('=')!=1 or not all(t.strip() for t in row.split('=')):continue
   if row.split('=')[0].strip().startswith('('):continue
   try:v=eq(row,names)
   except (ValueError,AssertionError):continue
   if v.has(p.x,p.y) and v.is_polynomial(p.x,p.y):equations.append(v)
 if len(equations)<2:
  # Only raw contextual replay may rely on the previously supplied first equation.
  b=blocks(worked)[0];assert r'\begin{aligned}' in b
  b=b.strip().removeprefix(r'\{').removeprefix('{');b=re.sub(r'\\(?:begin|end)\{aligned\}','',b);equations=[eq(row,names) for row in b.split(r'\\')]
 assert len(equations)==2,(prompt,equations)
 M,R=s.linear_eq_to_matrix(equations,(p.x,p.y));assert M.det()!=0;sol=M.inv()*R;return names,equations,dict(zip((p.x,p.y),sol))
def check(record):
 q=record['question'];prompt=q[':question/problem'];worked=q[':question/worked-solution'];names,equations,solution=system(prompt,worked);rows=0;substitution=0;operations=0
 for b in blocks(worked):
  b=b.strip().removeprefix(r'\{').removeprefix('{');b=re.sub(r'\\(?:begin|end)\{aligned\}','',b)
  # Final pairs occur together in one inline span, separated by a TeX comma.
  for row in [piece for line in b.split(chr(92)*2) for piece in line.split(','+chr(92)+',')]:
   if '=' not in row:continue
   parts=row.replace('&','').strip().rstrip('.,').split('=');assert all(z.strip() for z in parts)
   vals=[scalar(z,names) for z in parts];assert all(s.simplify((vals[0]-z).subs(solution))==0 for z in vals[1:]),(row,solution)
   # A nonconstant affine equation after substitution must preserve the full
   # isolated root, beyond satisfying its final numeric answer.
   for z in vals[1:]:
    residual=s.expand(vals[0]-z)
    if residual.has(p.x) and not residual.has(p.y):assert s.solve(residual,p.x)==[solution[p.x]];substitution+=1
    elif residual.has(p.y) and not residual.has(p.x):assert s.solve(residual,p.y)==[solution[p.y]];substitution+=1
   rows+=len(vals)-1
 assert rows>=8,(record,rows)
 for group in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',worked,re.S):
  lines=group.split(chr(92)*2);residuals=[eq(z,names) for z in lines]
  if len(lines)>=4 and len(residuals[0].free_symbols)==2 and len(residuals[1].free_symbols)==1:
   removed=next(iter(residuals[0].free_symbols-residuals[1].free_symbols));candidates=[z for e in equations for z in s.solve(e,removed)]
   assert any(s.expand(residuals[0].subs(removed,z)-residuals[1])==0 for z in candidates);operations+=1
   for previous,current in zip(residuals[1:-2],residuals[2:-1]):assert s.expand(previous-current)==0;operations+=1
 fs=q[':question/answer-fields'];count=0
 for n,f in enumerate(fs):
  values=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']]
  if f[':answer-field/type'].endswith('/radio'):
   assert len(fs)==1;want=solution[p.x]-solution[p.y];good=[z==want for z in values];assert sum(good)==1 and len(set(values))==len(values)
  else:
   assert '{{'+f[':answer-field/key']+'}}' in prompt
   # Tuple blanks are ordered coordinates; named standalone fragments are read
   # from the actual printed assignment immediately before each placeholder.
   before=prompt.split('{{'+f[':answer-field/key']+'}}')[0];matches=re.findall(r'\$([a-z])(?:\\,)?\s*=\s*\$',before)
   variable=names.index(matches[-1]) if matches else n;want=solution[(p.x,p.y)[variable]];good=[z==want for z in values];assert all(good)
  assert good[next(i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1])];count+=len(values)
 return {'values':count,'equation_rows':rows,'isolated_equivalent_equations':substitution,'substitution_distribution_operations':operations},names,equations,solution
