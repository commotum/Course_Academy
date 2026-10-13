"""Parent exact physical model and printed cooling-stage interpreter."""
import importlib.util,re,functools
from pathlib import Path
import sympy as s
from decimal import Decimal as D,localcontext,ROUND_HALF_UP
P=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('parent_cooling_elementary',P/'ode-scalar-parser.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);t=p.t
TEMP=re.compile(r'\{?(\d+)\}?\^\{(?:∘|\\circ)\}(?:\\text\{([CF])\}|([CF]))')
def question(q):
 text=q[':question/problem'];level=q[':question/difficulty'].split('/')[-1];temperatures=[int(m[1]) for m in TEMP.finditer(text)];units={m[2] or m[3] for m in TEMP.finditer(text)};assert len(units)==1
 if level=='easy':
  m=re.search(r'=-([\d.]+)\(T-(\d+)\)',text);assert m;rate=s.Rational(m[1]);A=int(m[2]);I=int(re.search(r'initial temperature .*?\$\{(\d+)\}',text)[1]);time=int(re.search(r'after \$(\d+)\$',text)[1]);constant=s.Integer(I-A);exact=A+constant*s.exp(-rate*time);times=[(0,I)]
 elif level=='moderate':
  if text.startswith('Simon'):I,O,Z,A=temperatures[:4]
  else:I,A,O,Z=temperatures[:4]
  time=int(re.search(r'After \$(\d+)\$',text)[1]);rate=-s.log(s.Rational(O-A,I-A))/time;constant=s.Integer(I-A);exact=-s.log(s.Rational(Z-A,I-A))/rate;times=[(0,I),(time,O)]
 else:
  A,O,L,Z=temperatures;times0=[int(z) for z in re.findall(r'after \$(\d+)\$',text)];a,b=times0;assert 0<a<b;h=b-a;rate=-s.log(s.Rational(L-A,O-A))/h;constant=(O-A)*s.exp(rate*a);exact=a+h*s.log(s.Rational(Z-A,O-A))/s.log(s.Rational(L-A,O-A));times=[(a,O),(b,L)]
 assert A>0 and rate.is_positive and constant.is_positive
 model=A+constant*s.exp(-rate*t)
 with localcontext() as c:
  c.prec=60
  if level=='easy':oracle=D(A)+D(I-A)*(-((D(int(rate.p))/D(int(rate.q)))*D(time))).exp()
  elif level=='moderate':oracle=D(time)*((D(Z-A)/D(I-A)).ln())/((D(O-A)/D(I-A)).ln())
  else:oracle=D(a)+D(h)*(D(Z-A)/D(O-A)).ln()/(D(L-A)/D(O-A)).ln()
  rounded=int(oracle.to_integral_value(rounding=ROUND_HALF_UP))
 assert rounded==int(s.floor(s.N(exact,45)+s.Rational(1,2)))
 return dict(level=level,ambient=A,rate=rate,constant=constant,model=model,exact=exact,target_time=exact if level!='easy' else s.Integer(time),oracle=str(oracle),rounded=rounded,times=times,unit=next(iter(units)))

def scalar(raw,d):
 raw=raw.strip().rstrip('.,').replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\!','').replace(r'\,','')
 raw=re.sub(r'\^\{∘\}(?:\\text\{[CF]\}|[CF])','',raw);raw=raw.replace(r'\text{min}','');raw=re.sub(r'\{T\}_\{S\}',str(d['ambient']),raw).replace(r'{t}_{1}','z')
 raw=raw.replace(r'\text{d}T','dT').replace(r'\text{d}t','dt');raw=raw.replace('dT','i').replace('dt','(1)')
 # Evaluate the actual specified function input, never treating T(a) as T*a.
 replacements={p.i:s.diff(d['model'],t)};tokens=('j','x')
 for slot,m in zip(tokens,list(re.finditer(r'T\(([^()]*)\)',raw))):
  argument=scalar(m[1],d);replacements[p.locals_[slot]]=d['model'].subs(t,argument)
 # Replace backwards, keeping original mathematical argument text intact.
 matches=list(re.finditer(r'T\(([^()]*)\)',raw));assert len(matches)<=2
 for slot,m in reversed(list(zip(tokens,matches))):raw=raw[:m.start()]+slot+raw[m.end():]
 if '|' in raw:
  a=raw.index('|');b=raw.index('|',a+1);raw=raw[:a]+'Abs('+raw[a+1:b]+')'+raw[b+1:]
 raw=re.sub(r'\\[A-Za-z]+|[TKC]',lambda m:{'T':'y','K':'v','C':'u'}.get(m[0],m[0]),raw)
 result=p.scalar(raw);replacements.update({p.y:d['model'],p.v:d['constant'],p.u:s.log(d['constant']),p.k:d['rate'],p.z:d['target_time']})
 return result.subs(replacements,simultaneous=True)
@functools.lru_cache(maxsize=4096)
def equal(a,b):
 delta=a-b
 if s.simplify(s.expand_power_base(s.expand_power_exp(delta),force=True))==0:return True
 delta=s.expand_log(delta,force=True);delta=s.powsimp(delta,force=True)
 return s.simplify(s.expand_power_base(s.expand_power_exp(delta),force=True))==0

def stages(q,d):
 counts=dict(exact_sides=0,integral_sides=0,rounded_sides=0,function_inputs=0,prose_equations=0,blocks=0)
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',sol,re.S)
 for block in blocks:
  counts['blocks']+=1;block=block.split(r'\qquad')[0].strip().rstrip(',')
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','');previous=None
  for row in block.split(r'\\'):
   if '=' not in row and '≈' not in row:continue
   row=row.strip();rounded=None
   if '≈' in row:row,rounded=row.split('≈',1)
   parts=row.split('=');vals=[]
   if any(r'\int' in part for part in parts):
    # First separation integral step: independently check both integrands as
    # differential rates along the actual physical model. Differentiating each
    # indefinite integral removes its independently arbitrary additive constant.
    for part in parts:
     assert r'\int' in part,parts;clean=part.replace(r'\int','');vals.append(scalar(clean,d))
    assert all(equal(value,vals[0]) for value in vals),row;counts['integral_sides']+=len(vals)-1;previous=None;continue
   for j,part in enumerate(parts):
    if not part.strip():assert j==0 and previous is not None;value=previous
    else:value=scalar(part,d)
    vals.append(value);counts['function_inputs']+=part.count('T(')
   assert all(equal(value,vals[0]) for value in vals),('False exact cooling stage',row,vals)
   counts['exact_sides']+=len(vals)-1;previous=vals[-1]
   if rounded is not None:
    actual=scalar(rounded,d);assert actual.is_Integer and int(actual)==d['rounded'];assert int(s.floor(s.N(previous,45)+s.Rational(1,2)))==int(actual);counts['rounded_sides']+=1
 # Independently read the time/temperature conditions embedded in shared prose.
 for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',sol,re.S):
  if '=' not in inline or 'T(' not in inline:continue
  lhs,rhs=inline.split('=',1);assert equal(scalar(lhs,d),scalar(rhs,d)),inline;counts['prose_equations']+=1
 assert counts['rounded_sides']==1 and counts['integral_sides']==1 and counts['exact_sides']>=12,counts
 return counts
